#!/usr/bin/env python3

import argparse
import http.client
import socket
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit

HOP_BY_HOP_HEADERS = {
    "host",
    "connection",
    "keep-alive",
    "proxy-authenticate",
    "proxy-authorization",
    "te",
    "trailer",
    "transfer-encoding",
    "upgrade",
    "x-forwarded-for",
    "x-forwarded-host",
    "x-forwarded-proto",
}
MAX_REQUEST_BYTES = 2 * 1024 * 1024


class LoopbackIPv6Server(ThreadingHTTPServer):
    address_family = socket.AF_INET6
    daemon_threads = True
    upstream_host = "192.168.129.16"
    upstream_port = 8123


class ProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def do_GET(self):
        self.forward_request()

    def do_HEAD(self):
        self.forward_request()

    def do_POST(self):
        self.forward_request()

    def do_DELETE(self):
        self.forward_request()

    def log_request(self, code="-", size="-"):
        pass

    def log_message(self, format, *args):
        pass

    def forward_request(self):
        target = urlsplit(self.path)
        if target.scheme or target.netloc or not target.path.startswith("/"):
            self.send_error(400, "Origin-form request target required")
            return

        length_header = self.headers.get("Content-Length")
        try:
            length = int(length_header or "0")
        except ValueError:
            self.send_error(400, "Invalid Content-Length")
            return
        if length < 0 or length > MAX_REQUEST_BYTES:
            self.send_error(413, "Request body too large")
            return
        if self.headers.get("Transfer-Encoding"):
            self.send_error(501, "Chunked requests are not supported")
            return

        body = self.rfile.read(length) if length else None
        headers = {
            key: value
            for key, value in self.headers.items()
            if key.lower() not in HOP_BY_HOP_HEADERS
        }
        headers["Host"] = "localhost:8123"
        headers["Connection"] = "close"
        headers["Accept-Encoding"] = "identity"
        path = target.path + (f"?{target.query}" if target.query else "")

        upstream = http.client.HTTPConnection(
            self.server.upstream_host,
            self.server.upstream_port,
            timeout=300,
        )
        try:
            upstream.request(self.command, path, body=body, headers=headers)
            response = upstream.getresponse()
            self.send_response(response.status, response.reason)
            for key, value in response.getheaders():
                if key.lower() not in HOP_BY_HOP_HEADERS:
                    self.send_header(key, value)
            self.send_header("Connection", "close")
            self.end_headers()
            if self.command != "HEAD":
                while chunk := response.read(64 * 1024):
                    self.wfile.write(chunk)
                    self.wfile.flush()
        except (OSError, http.client.HTTPException) as error:
            if not self.wfile.closed:
                self.send_error(502, f"Upstream unavailable: {type(error).__name__}")
        finally:
            upstream.close()
            self.close_connection = True


def main():
    parser = argparse.ArgumentParser(description="Home Assistant MCP loopback-only relay")
    parser.add_argument("--upstream-host", default="192.168.129.16")
    parser.add_argument("--upstream-port", type=int, default=8123)
    args = parser.parse_args()
    LoopbackIPv6Server.upstream_host = args.upstream_host
    LoopbackIPv6Server.upstream_port = args.upstream_port
    with LoopbackIPv6Server(("::1", 8123), ProxyHandler) as server:
        print("Home Assistant relay listening on http://[::1]:8123", flush=True)
        server.serve_forever()


if __name__ == "__main__":
    main()
