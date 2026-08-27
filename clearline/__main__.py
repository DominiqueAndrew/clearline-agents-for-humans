from __future__ import annotations

import argparse

from .server import create_server


def main() -> None:
    parser = argparse.ArgumentParser(description="Run the Clearline local demo")
    parser.add_argument("--host", default="127.0.0.1")
    parser.add_argument("--port", type=int, default=8787)
    args = parser.parse_args()
    server = create_server(args.host, args.port)
    print(f"Clearline running at http://{args.host}:{args.port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nClearline stopped")
    finally:
        server.server_close()


if __name__ == "__main__":
    main()

