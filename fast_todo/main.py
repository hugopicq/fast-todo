import argparse
import uvicorn

from fast_todo.app.config import config

def parse_command() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=("Starts a web server that serves a REST API for TODO app"),
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )

    parser.add_argument(
        "--host",
        help="The host to bind to.",
        type=str,
        default="0.0.0.0",
    )
    parser.add_argument(
        "--port",
        help="The port to bind to.",
        type=int,
        default=8080,
    )

    parser.add_argument(
        "--reload",
        help="Enable auto-reload of the server.",
        action="store_true",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = parse_command()
    
    uvicorn.run(
        "fast_todo.app.app:app",
        reload=args.reload,
        log_level="info",
        host=args.host,
        port=args.port,
    )
