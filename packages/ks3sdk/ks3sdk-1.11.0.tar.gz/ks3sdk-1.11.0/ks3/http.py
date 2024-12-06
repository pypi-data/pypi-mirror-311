# coding:utf-8
import logging
import time
import re
import os
import select

from ks3 import utils
from ks3.utils import get_default_user_agent

try:
    import http.client as httpcli  # for Python 3
    import urllib.parse as parse
    from urllib import parse as urlparse
except ImportError:
    print('python@2.x no longer supported by ks3sdk@2.x, please refer to ks3sdk@1.x for python@2.x support')

from ks3.auth import canonical_string, add_auth_header, url_encode, encode
from ks3.authV4 import add_auth_header as add_auth_header_v4

logger = logging.getLogger(__name__)


class CallingFormat:
    PATH = 1
    SUBDOMAIN = 2
    VANITY = 3


class AuthingFormat:
    V2 = 1
    V4 = 2


def merge_meta(headers, metadata):
    final_headers = headers.copy()
    for k in list(metadata.keys()):
        final_headers["x-kss-" + "meta-" + k] = metadata[k]

    return final_headers


def query_args_hash_to_string(query_args):
    pairs = []
    for k, v in list(query_args.items()):
        piece = k
        if v is not None:
            piece += "=%s" % parse.quote_plus(str(v).encode('utf-8'))
            # piece += "=%s" % v
        pairs.append(piece)

    return '&'.join(pairs)


def get_object_url(age, bucket="", key="", secret_access_key="", access_key_id="", query_args={}):
    expire = str(int(time.time()) + age)
    headers = {"Date": expire}
    c_string = canonical_string("GET", bucket, key, query_args, headers)
    path = c_string.split("\n")[-1]

    signature = parse.quote_plus(encode(secret_access_key, c_string))
    if "?" in path:
        url = "http://kss.ksyun.com%s&Expires=%s&AccessKeyId=%s&Signature=%s" % \
              (path, expire, access_key_id, signature)
    else:
        url = "http://kss.ksyun.com%s?Expires=%s&AccessKeyId=%s&Signature=%s" % \
              (path, expire, access_key_id, signature)
    return url


def make_request(server, port, access_key_id, access_key_secret, bucket="", key="", query_args=None, headers=None,
                 data="", metadata=None, method="PUT", calling_format=None, is_secure=False,
                 domain_mode=False, need_auth_header=True, timeout=10, ua_addon='', block_size=8192, proxy_host=None,
                 proxy_port=None):
    if not headers:
        headers = {}
    # if not query_args:
    #    query_args = {}
    if not metadata:
        metadata = {}

    if bucket and not domain_mode:
        server = calling_format.get_bucket_server(server, bucket)
    path = calling_format.build_path_base(bucket, key)
    # path += "/%s" % url_encode(key)
    # path = path.replace('//', '/%2F')

    if query_args:
        if isinstance(query_args, dict):
            path += "?" + query_args_hash_to_string(query_args)
        else:
            path += "?" + query_args

    host = "%s:%d" % (server, port)

    if proxy_host is not None:
        if is_secure:
            connection = KS3HTTPSConnection(host=proxy_host, port=proxy_port, blocksize=block_size)
        else:
            connection = KS3HTTPConnection(host=proxy_host, port=proxy_port, blocksize=block_size)
        connection.set_tunnel(host)
    else:
        if is_secure:
            connection = KS3HTTPSConnection(host=host, blocksize=block_size)
        else:
            connection = KS3HTTPConnection(host=host, blocksize=block_size)

    connection.timeout = timeout
    headers['User-Agent'] = get_default_user_agent() + ' ' + ua_addon
    final_headers = merge_meta(headers, metadata)
    if method == "PUT" and "Content-Length" not in final_headers and not data:
        final_headers["Content-Length"] = "0"
    if method.upper() == "POST" and "Content-Length" not in final_headers and not data:
        final_headers["Content-Length"] = str(len(data))
    if need_auth_header:
        add_auth_header(access_key_id, access_key_secret, final_headers, method,
                        bucket, key, query_args)

    logger.info('send [{method}] request, host: {host}, port: {port}, path: {path}, headers: {headers}'
                .format(method=method, host=host, port=port, path=path, headers=final_headers))
    connection.request(method, path, data, final_headers)
    if connection.early_resp:
        resp = connection.early_resp
    else:
        resp = connection.getresponse()
    logger.info(
        'complete [{method}] request, host: {host}, port: {port}, path: {path}, request_id: {request_id}, status_code:{status}'
        .format(
            method=method,
            host=host,
            port=port,
            path=path,
            request_id=resp.getheader('x-kss-request-id') if resp else '',
            status=resp.status,
        )
    )
    if 300 <= resp.status < 400:
        loc = resp.getheader('location')
        if loc:
            reg = re.findall('http[s]?://(.*?)(:\d+)?/', loc)
            if reg:
                # 如果返回的是bucket style域名，需要提取region域名出来
                if len(reg[0][0].split('.')) == 4:
                    new_server = reg[0][0].split('.', 1)[1]
                else:
                    new_server = reg[0][0]
                loc_parse = urlparse.urlparse(loc)
                if 'Signature' in loc_parse.query:
                    connection_temp = httpcli.HTTPSConnection(new_server)
                    connection_temp.request('GET', loc_parse.path + '?' + loc_parse.query)
                    try:
                        resp_temp = connection_temp.getresponse()
                        return resp_temp
                    except Exception as err:
                        print(str(err))
                else:
                    if hasattr(data, 'read'):
                        data.seek(0, os.SEEK_SET)
                        if isinstance(data, utils.FpAdapter):
                            data.reset_crc_process()
                    return make_request(new_server, port, access_key_id, access_key_secret, bucket, key, query_args,
                                        headers, data, metadata, method=method, calling_format=calling_format, is_secure=is_secure,
                                        need_auth_header=True, ua_addon=ua_addon)
    return resp


# 发送awsv4的请求
def make_request_v4(access_key_id, access_key_secret, method='', service='', region='', query_args=None, headers={},
                    body="", is_secure=False, timeout=10, inner_api=False):
    inner_string = '.inner' if inner_api else ''
    host = service + inner_string + '.api.ksyun.com'

    if (is_secure):
        connection = httpcli.HTTPSConnection(host)
    else:
        connection = httpcli.HTTPConnection(host)
    connection.timeout = timeout

    path = "/"
    if query_args:
        if isinstance(query_args, dict):
            query_args = query_args_hash_to_string(query_args)
    path += "?" + query_args

    headers = add_auth_header_v4(access_key_id, access_key_secret, region, service, host, method, query_args, body,
                                 headers)

    connection.request(method, path, body, headers)
    resp = connection.getresponse()
    return resp


class KS3HTTPConnection(httpcli.HTTPConnection):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.early_resp = None

    def _send_output(self, message_body=None, encode_chunked=False):
        """Send the currently buffered request and clear the buffer.

        Appends an extra \\r\\n to the buffer.
        A message_body may be specified, to be appended to the request.
        """
        self._buffer.extend((b"", b""))
        msg = b"\r\n".join(self._buffer)
        del self._buffer[:]
        self.send(msg)
        if message_body is not None:

            # create a consistent interface to message_body
            if hasattr(message_body, 'read'):
                # Let file-like take precedence over byte-like.  This
                # is needed to allow the current position of mmap'ed
                # files to be taken into account.
                chunks = self._read_readable(message_body)
            else:
                try:
                    # this is solely to check to see if message_body
                    # implements the buffer API.  it /would/ be easier
                    # to capture if PyObject_CheckBuffer was exposed
                    # to Python.
                    memoryview(message_body)
                except TypeError:
                    try:
                        chunks = iter(message_body)
                    except TypeError:
                        raise TypeError("message_body should be a bytes-like "
                                        "object or an iterable, got %r"
                                        % type(message_body))
                else:
                    # the object implements the buffer interface and
                    # can be passed directly into socket methods
                    chunks = (message_body,)
            for chunk in chunks:
                ready_to_read, ready_to_write, _ = select.select([self.sock], [self.sock], [], self.timeout)
                if ready_to_read:
                    self.early_resp = self.getresponse()
                    return
                if not chunk:
                    if self.debuglevel > 0:
                        print('Zero length chunk ignored')
                    continue

                if encode_chunked and self._http_vsn == 11:
                    # chunked encoding
                    chunk = f'{len(chunk):X}\r\n'.encode('ascii') + chunk \
                            + b'\r\n'
                if ready_to_write:
                    try:
                        self.send(chunk)
                    except Exception as e:
                        pos = None
                        if message_body != b'' and hasattr(message_body, 'tell'):
                            pos = message_body.tell()
                        # if e.errno == errno.EPIPE:
                        #     print("捕获到Broken pipe错误")
                        # 有可能写的时候，发生了BrokenPipeError；为了读取到响应的内容，最后再尝试读取一次
                        if isinstance(e, (BrokenPipeError, ConnectionAbortedError, ConnectionResetError)):
                            last_read_ready, _, _ = select.select([self.sock], [self.sock], [], self.timeout)
                            if last_read_ready:
                                self.early_resp = self.getresponse()
                                return
                            else:
                                logger.error('send chunk error, message body read position={pos}, error: {e}'
                                             .format(pos=pos, e=str(e)),
                                             exc_info=True)
                                raise e
                        else:
                            logger.error('send chunk error, message body read position={pos}, error: {e}'
                                         .format(pos=pos, e=str(e)),
                                         exc_info=True)
                            raise e

            if encode_chunked and self._http_vsn == 11:
                # end chunked transfer
                self.send(b'0\r\n\r\n')


class KS3HTTPSConnection(httpcli.HTTPSConnection, KS3HTTPConnection):
    ...
