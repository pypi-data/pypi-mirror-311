import argparse
from .server import start_server
# from .utils import get_local_ip # i may need it later

def main():
    parser = argparse.ArgumentParser(description="simple http server in python")
    subparsers = parser.add_subparsers(dest="command")

    server_parser = subparsers.add_parser("serve", help="Start the sendfile server")
    server_parser.add_argument("--host", default="0.0.0.0", help="Host to bind the server (default: 0.0.0.0)")
    server_parser.add_argument("--port", type=int, default=80, help="Port to bind the server (default: 80)")

    args = parser.parse_args()

    print(f"Starting server at {args.host}:{args.port}")
    start_server(host=args.host, port=args.port)


if __name__ == "__main__":
    main()
