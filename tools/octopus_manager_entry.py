from __future__ import annotations

import os
import sys
from pathlib import Path


def _add_product_repo_to_syspath() -> None:
    """
    Build-time helper for PyInstaller.

    The manager implementation lives in the main product repository (octopusos/octopusos),
    which is checked out by the release workflow next to this repo.
    """

    repo_dir_name = (os.getenv("OCTOCTL_PRODUCT_REPO_DIR", "").strip() or "octopusos-product")
    product_repo = (Path(__file__).resolve().parents[1] / repo_dir_name).resolve()

    # Main repo uses "os/octopusos/..." layout.
    sys.path.insert(0, str(product_repo / "os"))


def main() -> int:
    _add_product_repo_to_syspath()
    from octopusos.manager.__main__ import main as manager_main  # type: ignore

    manager_main()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

