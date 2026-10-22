"""Backwards-compatible entry point: ``python api/server.py``.

Prefer ``python run.py`` from the project root.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from run import main  # noqa: E402

if __name__ == "__main__":
    main()
