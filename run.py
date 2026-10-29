"""Start the Digital Eye API server."""

import config
from api import create_app

app = create_app()


def main() -> None:
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)


if __name__ == "__main__":
    main()
