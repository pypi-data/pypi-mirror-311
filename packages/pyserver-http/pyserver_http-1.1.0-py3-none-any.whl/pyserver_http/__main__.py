import argparse
from .server import start_server  # from .utils import get_local_ip  # i may need it later

def main():
    parser = argparse.ArgumentParser(description="Simple HTTP server in Python")
    subparsers = parser.add_subparsers(dest="command")

    # Add subparser for the 'serve' command
    server_parser = subparsers.add_parser("serve", help="Start the sendfile server")
    server_parser.add_argument(
        "--host", default="0.0.0.0", help="Host to bind the server (default: 0.0.0.0)"
    )
    server_parser.add_argument(
        "--port", type=int, default=80, help="Port to bind the server (default: 80)"
    )

    # Parse arguments and call start_server
    args = parser.parse_args()

    # Start the server with provided arguments
    start_server(host=args.host, port=args.port)

if __name__ == "__main__":
    main()
