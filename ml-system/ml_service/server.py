import argparse
import json
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from .service import MLService


service = MLService()


class MLRequestHandler(BaseHTTPRequestHandler):
    server_version = "MLSystemHTTP/1.0"

    def _send_json(self, status: int, payload: dict) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_json(self) -> dict:
        length = int(self.headers.get("Content-Length", "0"))
        if length <= 0:
            return {}
        data = self.rfile.read(length)
        try:
            payload = json.loads(data.decode("utf-8"))
        except json.JSONDecodeError as exc:
            raise ValueError("Request body must be valid JSON") from exc
        if not isinstance(payload, dict):
            raise TypeError("Request body must be a JSON object")
        return payload

    def do_GET(self) -> None:
        if self.path == "/health":
            self._send_json(200, {"status": "ok"})
            return
        self._send_json(404, {"error": "Not found"})

    def do_POST(self) -> None:
        try:
            payload = self._read_json()
            if self.path == "/score":
                result = service.score(
                    payload["resume_text"],
                    payload["job_description"],
                    include_semantic=payload.get("include_semantic", False),
                )
            elif self.path == "/gap":
                result = service.gap(payload["resume_text"], payload["benchmark"])
            elif self.path == "/rank":
                result = service.rank(payload["resume_text"], payload["benchmarks"])
            else:
                self._send_json(404, {"error": "Not found"})
                return
            self._send_json(200, result)
        except (KeyError, TypeError, ValueError) as exc:
            self._send_json(400, {"error": str(exc)})

    def log_message(self, format: str, *args) -> None:
        return


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the ml-system HTTP service")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8000)
    args = parser.parse_args(argv)

    server = ThreadingHTTPServer((args.host, args.port), MLRequestHandler)
    print(f"ml-system listening on http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
