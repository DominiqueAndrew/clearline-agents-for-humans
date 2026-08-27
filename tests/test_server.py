import json
from threading import Thread
from urllib.error import HTTPError
from urllib.request import Request, urlopen

from clearline.server import create_server
from clearline.store import ClearlineStore


def test_http_demo_serves_state_and_human_action():
    server = create_server("127.0.0.1", 0, ClearlineStore(db_path=":memory:"))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    base = f"http://127.0.0.1:{server.server_port}"
    try:
        with urlopen(f"{base}/api/state") as response:
            state = json.load(response)
        assert state["stats"]["pending"] == 3

        request = Request(
            f"{base}/api/invoices/inv_1002/decision",
            data=json.dumps({"action": "approve"}).encode(),
            headers={"Content-Type": "application/json"},
            method="POST",
        )
        with urlopen(request) as response:
            updated = json.load(response)
        assert updated["invoices"][1]["decision"]["status"] == "approved"
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)


def test_http_rejects_non_object_decision_payload():
    server = create_server("127.0.0.1", 0, ClearlineStore(db_path=":memory:"))
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()
    request = Request(
        f"http://127.0.0.1:{server.server_port}/api/invoices/inv_1002/decision",
        data=b"[]",
        headers={"Content-Type": "application/json"},
        method="POST",
    )
    try:
        urlopen(request)
    except HTTPError as exc:
        assert exc.code == 400
        assert json.load(exc)["error"] == "JSON body must be an object"
    else:
        raise AssertionError("non-object JSON payload should be rejected")
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=2)
