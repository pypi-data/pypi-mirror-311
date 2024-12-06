import threading
import io
import socket
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from functools import lru_cache


class WSGIServer:

    address_family = socket.AF_INET
    socket_type = socket.SOCK_STREAM
    request_queue_size = 5
    timeout = 30  # Temps limite pour les connexions IA longues

    def __init__(self, server_address, max_workers=10):
        # Création du socket d'écoute
        self.listen_socket = socket.socket(self.address_family, self.socket_type)
        self.listen_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.listen_socket.bind(server_address)
        self.listen_socket.listen(self.request_queue_size)
        self.listen_socket.settimeout(self.timeout)

        host, port = self.listen_socket.getsockname()[:2]
        self.server_name = socket.getfqdn(host)
        self.server_port = port
        self.headers_set = []

        # Pool de threads pour gérer les connexions
        self.executor = ThreadPoolExecutor(max_workers=max_workers)

    def set_app(self, application):
        self.application = application

    def serve_forever(self):
        print(f"Serveur optimisé en écoute sur {self.server_name}:{self.server_port}")
        while True:
            try:
                client_connection, client_address = self.listen_socket.accept()
                print(f"Nouvelle connexion de {client_address}")
                client_connection.settimeout(self.timeout)
                self.executor.submit(self.handle_request, client_connection)
            except socket.timeout:
                print("Aucune requête reçue dans le délai imparti.")
            except Exception as e:
                print(f"Erreur serveur: {e}")

    def handle_request(self, client_connection):
        start_time = time.time()
        try:
            request_data = client_connection.recv(1024)
            if not request_data:
                raise ValueError("Requête vide ou client déconnecté.")
            request_data = request_data.decode('utf-8')
            print(''.join(f'< {line}\n' for line in request_data.splitlines()))

            # Analyse et traitement de la requête
            self.parse_request(request_data)
            env = self.get_environ(request_data)
            result = self.process_request_with_cache(env)
            self.finish_response(client_connection, result)
        except socket.timeout:
            print("Le client n'a pas envoyé de données dans le délai imparti.")
            client_connection.sendall(b"HTTP/1.1 408 Request Timeout\r\n\r\n")
        except Exception as e:
            print(f"Erreur pendant le traitement de la requête: {e}")
            client_connection.sendall(b"HTTP/1.1 500 Internal Server Error\r\n\r\n")
        finally:
            client_connection.close()
            end_time = time.time()
            print(f"Requête traitée en {end_time - start_time:.2f} secondes.")

    def parse_request(self, text):
        request_line = text.splitlines()[0]
        self.request_method, self.path, self.request_version = request_line.split()

    def get_environ(self, request_data):
        env = {
            'wsgi.version': (1, 0),
            'wsgi.url_scheme': 'http',
            'wsgi.input': io.StringIO(request_data),
            'wsgi.errors': sys.stderr,
            'wsgi.multithread': True,
            'wsgi.multiprocess': False,
            'wsgi.run_once': False,
            'REQUEST_METHOD': self.request_method,
            'PATH_INFO': self.path,
            'SERVER_NAME': self.server_name,
            'SERVER_PORT': str(self.server_port),
        }
        return env

    @lru_cache(maxsize=100)  # Mise en cache des réponses
    def process_request_with_cache(self, env):
        # Exécute l'application et met en cache les réponses répétées
        result = self.application(env, self.start_response)
        return result

    def start_response(self, status, response_headers, exc_info=None):
        server_headers = [
            ('Date', 'Fri, 29 Jul 2024'),
            ('Server', 'WSGIServer Optimized 1.0'),
        ]
        self.headers_set = [status, response_headers + server_headers]

    def finish_response(self, client_connection, result):
        try:
            status, response_headers = self.headers_set
            response = f'HTTP/1.1 {status}\r\n'
            for header in response_headers:
                response += '{0}: {1}\r\n'.format(*header)
            response += '\r\n'
            for data in result:
                response += data.decode('utf-8')
            client_connection.sendall(response.encode())
        except Exception as e:
            print(f"Erreur lors de l'envoi de la réponse: {e}")


SERVER_ADDRESS = (HOST, PORT) = '', 8888


def make_server(server_address, application):
    server = WSGIServer(server_address, max_workers=20)
    server.set_app(application)
    return server

def main():
    import argparse
    parser = argparse.ArgumentParser(description="Run a WSGI server.")
    parser.add_argument('app', help='The WSGI application as module:callable (e.g., myapp:app)')
    args = parser.parse_args()

    app_path = args.app
    module, application = app_path.split(':')
    module = __import__(module)
    application = getattr(module, application)

    SERVER_ADDRESS = ('', 8888)
    httpd = make_server(SERVER_ADDRESS, application)
    print(f'WSGIServer: Serving HTTP on port 8888 ...\n')
    httpd.serve_forever()

# if __name__ == '__main__':
#     if len(sys.argv) < 2:
#         sys.exit('Provide a WSGI application object as module:callable')
#     app_path = sys.argv[1]
#     module, application = app_path.split(':')
#     module = __import__(module)
#     application = getattr(module, application)
#     httpd = make_server(SERVER_ADDRESS, application)
#     print(f'WSGIServer: Serving HTTP on port {PORT} ...\n')
#     httpd.serve_forever()
