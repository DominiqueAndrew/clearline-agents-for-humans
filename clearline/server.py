from __future__ import annotations

import json
import mimetypes
from http import HTTPStatus
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from urllib.parse import urlparse

from .store import ClearlineStore
from .worker import BackgroundWorker


STATIC_ROOT = Path(__file__).parent / "static"


class ClearlineHandler(BaseHTTPRequestHandler):
    store: ClearlineStore
    static_root: Path = STATIC_ROOT

    def do_GET(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/state":
            self._json(self.store.snapshot())
            return
        if path == "/health":
            self._json({"ok": True, "service": "clearline"})
            return
        self._static(path)

    def do_POST(self) -> None:  # noqa: N802
        path = urlparse(self.path).path
        if path == "/api/run":
            self._json(self.store.run_sweep())
            return
        prefix = "/api/invoices/"
        suffix = "/decision"
        if path.startswith(prefix) and path.endswith(suffix):
            invoice_id = path[len(prefix) : -len(suffix)]
            try:
                payload = self._read_json()
                snapshot = self.store.decide(invoice_id, str(payload.get("action", "")))
            except (KeyError, ValueError, json.JSONDecodeError) as exc:
                self._json({"error": str(exc)}, HTTPStatus.BAD_REQUEST)
                return
            self._json(snapshot)
            return
        self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)

    def _static(self, path: str) -> None:
        requested = "index.html" if path in {"", "/"} else path.lstrip("/")
        candidate = (self.static_root / requested).resolve()
        if self.static_root.resolve() not in candidate.parents and candidate != self.static_root.resolve():
            self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        if not candidate.is_file():
            self._json({"error": "not found"}, HTTPStatus.NOT_FOUND)
            return
        content_type = mimetypes.guess_type(candidate.name)[0] or "application/octet-stream"
        data = candidate.read_bytes()
        self.send_response(HTTPStatus.OK)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-cache")
        self.end_headers()
        self.wfile.write(data)

    def _read_json(self) -> dict[str, object]:
        length = int(self.headers.get("Content-Length", "0"))
        return json.loads(self.rfile.read(length) or b"{}")

    def _json(self, payload: object, status: HTTPStatus = HTTPStatus.OK) -> None:
        data = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.end_headers()
        self.wfile.write(data)

    def log_message(self, format: str, *args: object) -> None:
        return


def create_server(host: str = "127.0.0.1", port: int = 8787, store: ClearlineStore | None = None) -> ThreadingHTTPServer:
    bound_store = store or ClearlineStore()
    BackgroundWorker(bound_store).run_once()
    ClearlineHandler.store = bound_store
    return ThreadingHTTPServer((host, port), ClearlineHandler)
