#!/usr/bin/env python3
"""
Initialize zprezto git submodules after chezmoi deploys the repo.

The .chezmoiexternal.yaml clones zprezto via chezmoi's git-repo external type,
but submodule initialization is not guaranteed on all chezmoi versions.
This script ensures syntax-highlighting and history-substring-search submodules
are always populated, preventing shell startup errors on fresh installs.

Fixes: https://github.com/nehalecky/dotfiles/issues/5
"""
import os
import subprocess
import sys
from pathlib import Path


def main() -> None:
    zdotdir = os.environ.get("ZDOTDIR")
    zprezto = (Path(zdotdir) if zdotdir else Path.home()) / ".zprezto"

    if not zprezto.is_dir():
        print(f"zprezto not found at {zprezto}, skipping submodule init")
        return

    if not (zprezto / ".gitmodules").exists():
        print(f"No .gitmodules found in {zprezto}, skipping submodule init")
        return

    print("Initializing zprezto submodules...")
    result = subprocess.run(
        ["git", "submodule", "update", "--init", "--recursive"],
        cwd=zprezto,
    )
    if result.returncode != 0:
        print("❌ Failed to initialize zprezto submodules", file=sys.stderr)
        sys.exit(result.returncode)
    print("zprezto submodules initialized")


if __name__ == "__main__":
    main()
