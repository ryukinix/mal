from queue import Queue
from urllib import parse
from pprint import pprint
from dataclasses import dataclass
import http.server
import secrets
import webbrowser

from authlib.integrations.requests_client import OAuth2Session


@dataclass
class AuthConfig:
    client_id: str = 'd67c22659ba9bfe600ea035c564f43c7'
    authorization_url: str = "https://myanimelist.net/v1/oauth2/authorize"
    token_url = "https://myanimelist.net/v1/oauth2/token"
    home_project = "https://github.com/ryukinix/mal"
    callback_port: int = 8000
    callback_host = "0.0.0.0"
    code_challenge = secrets.token_hex(50)
    grant_type: str = "authorization_code"

    @property
    def redirect_uri(self):
        return f"http://{self.callback_host}:{self.callback_port}/"

    @property
    def client(self):
        return OAuth2Session(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri
        )

    def create_authorization_url(self):
        return self.client.create_authorization_url(
            self.authorization_url,
            code_challenge=self.code_challenge,
            code_challenge_method="plain",
            response_type="code",
        )


auth_config = AuthConfig()


class AuthHandler(http.server.SimpleHTTPRequestHandler):
    queue: Queue = Queue()

    def log_message(self, *args, **kwargs):
        """Silence logs"""
        pass

    def do_GET(self):
        self.send_response(301)
        self.send_header('Location', auth_config.home_project)
        self.queue.put(self._parse_query_params(self.path))
        self.end_headers()

    @staticmethod
    def _parse_query_params(url: str) -> dict:
        return dict(parse.parse_qsl(parse.urlparse(url).query))


def get_token(authorization_code: str, state: str) -> dict:
    return auth_config.client.fetch_access_token(
        auth_config.token_url,
        client_id=auth_config.client_id,
        grant_type=auth_config.grant_type,
        redirect_uri=auth_config.redirect_uri,
        code_verifier=auth_config.code_challenge,
        code=authorization_code,
        state=state,
    )


def login(open_browser=True) -> dict:
    print("Authorize application access your myanimelist account...")
    url, state = auth_config.create_authorization_url()
    if open_browser:
        webbrowser.open(url)
    else:
        print("Authorize: ", url)
    server_address = (auth_config.callback_host, auth_config.callback_port)
    httpd = http.server.HTTPServer(server_address, AuthHandler)
    httpd.handle_request()
    authorization_code = AuthHandler.queue.get()["code"]
    return get_token(authorization_code, state)


if __name__ == "__main__":
    pprint(login())
