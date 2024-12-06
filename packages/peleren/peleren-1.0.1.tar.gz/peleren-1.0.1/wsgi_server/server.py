import asyncio  # Added for asynchronous I/O
import io
import socket
import sys
import time
from functools import lru_cache
from email.utils import formatdate  # Added for dynamic date header
import logging  # Added for logging
import ssl  # Added for SSL/TLS support
import argparse  # Moved import to the top for better organization

class WSGIServer:
    # Removed threading and ThreadPoolExecutor imports and usages

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    timeout = 30  # Timeout for long connections

    def __init__(self, server_address, application, use_ssl=False, certfile=None, keyfile=None):
        # Added parameters for SSL support

        # Create listening socket
        self.listen_socket = socket.socket(self.address_family, self.socket_type)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(server_address)
        self.listen_socket.listen(self.request_queue_size)
        self.listen_socket.settimeout(self.timeout)

        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []

        self.application = application

        # SSL context setup
        self.use_ssl = use_ssl  # Added SSL flag
        if self.use_ssl:
            self.context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
            self.context.load_cert_chain(certfile, keyfile)
        else:
            self.context = None

        # Initialize logger
        logging.basicConfig(level=logging.INFO)  # Added logging

    async def serve_forever(self):
        logging.info(f"Optimized server listening on {self.server_name}:{self.server_port}")
        # Start the server with asyncio
        server = await asyncio.start_server(
            self.handle_request, self.server_name, self.server_port, ssl=self.context
        )
        async with server:
            await server.serve_forever()

    async def handle_request(self, reader, writer):
        start_time = time.time()
        client_address = writer.get_extra_info('peername')
        logging.info(f"New connection from {client_address}")

        try:
            request_data = await asyncio.wait_for(reader.read(1024), timeout=self.timeout)
            if not request_data:
                raise ValueError("Empty request or client disconnected.")
            request_text = request_data.decode('utf-8')
            logging.debug(''.join(f'< {line}\n' for line in request_text.splitlines()))

            # Parse and handle request
            self.parse_request(request_text)
            env = self.get_environ(request_text, client_address)
            result = await self.process_request_with_cache(env)
            await self.finish_response(writer, result)
        except asyncio.TimeoutError:
            logging.warning("Client did not send data within the timeout period.")
            writer.write(b"HTTP/1.1 408 Request Timeout\r\n\r\n")
        except Exception as e:
            logging.error(f"Error during request handling: {e}")
            writer.write(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        finally:
            writer.close()
            await writer.wait_closed()
            end_time = time.time()
            logging.info(f"Request handled in {end_time - start_time:.2f} seconds.")

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        parts = request_line.split()
        if len(parts) != 3:
            raise ValueError("Malformed request line")  # Improved error handling
        self.request_method, self.path, self.request_version = parts

    def get_environ(self, request_text, client_address):
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'https' if self.use_ssl else 'http',
            'wsgi.input': io.StringIO(request_text),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': False,  # Updated for asyncio
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.request_method,
            'PATH_INFO': self.path,
            'SERVER_NAME': self.server_name,
            'SERVER_PORT': str(self.server_port),
            'SERVER_PROTOCOL': self.request_version,
            'QUERY_STRING': '',
            'REMOTE_ADDR': client_address[0],
            'CONTENT_TYPE': '',
            'CONTENT_LENGTH': '0',
        }
        # Parse headers and add them to env
        headers = self.parse_headers(request_text)
        env.update(headers)
        return env

    def parse_headers(self, request_text):
        headers = {}
        lines = request_text.splitlines()
        for line in lines[1:]:
            if line == '':
                break  # End of headers
            try:
                key, value = line.split(':', 1)
                key = key.strip().upper().replace('-', '_')
                headers[f'HTTP_{key}'] = value.strip()
            except ValueError:
                pass  # Skip malformed headers
        return headers

    async def process_request_with_cache(self, env):
        cache_key = (env['REQUEST_METHOD'], env['PATH_INFO'], env.get('QUERY_STRING', ''))
        return await self._cached_application(cache_key, env)

    @lru_cache(maxsize=100)
    async def _cached_application(self, cache_key, env):
        return self.application(env, self.start_response)

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', formatdate(timeval=None, localtime=False, usegmt=True)),  # Dynamic date header
            ('Server', 'WSGIServer Optimized 1.0'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    async def finish_response(self, writer, result):
        try:
            status, response_headers = self.headers_set
            response_headers_str = '\r\n'.join(f'{header}: {value}' for header, value in response_headers)
            response_status_line = f'HTTP/1.1 {status}\r\n'
            response = response_status_line + response_headers_str + '\r\n\r\n'
            writer.write(response.encode('utf-8'))

            # Ensure result is an iterable of bytes
            if isinstance(result, bytes):
                writer.write(result)
            else:
                for data in result:
                    if isinstance(data, bytes):
                        writer.write(data)
                    else:
                        writer.write(data.encode('utf-8'))
            await writer.drain()
        except Exception as e:
            logging.error(f"Error sending response: {e}")

def make_server(server_address, application, use_ssl=False, certfile=None, keyfile=None):
    server = WSGIServer(server_address, application, use_ssl=use_ssl, certfile=certfile, keyfile=keyfile)
    return server

def main():
    parser = argparse.ArgumentParser(description="Run an optimized WSGI server.")
    parser.add_argument('app', help='The WSGI application as module:callable (e.g., myapp:app)')
    parser.add_argument('--host', default='', help='Host to bind to')
    parser.add_argument('--port', type=int, default=8888, help='Port to bind to')
    parser.add_argument('--ssl', action='store_true', help='Use SSL/TLS')
    parser.add_argument('--certfile', help='SSL certificate file')
    parser.add_argument('--keyfile', help='SSL key file')
    args = parser.parse_args()

    app_path = args.app
    module_name, application_name = app_path.split(':')
    module = __import__(module_name)
    application = getattr(module, application_name)

    server_address = (args.host, args.port)
    httpd = make_server(server_address, application, use_ssl=args.ssl, certfile=args.certfile, keyfile=args.keyfile)
    logging.info(f'WSGIServer: Serving HTTP on port {args.port} ...')

    # Run the server using asyncio
    asyncio.run(httpd.serve_forever())

if __name__ == '__main__':
    main()
