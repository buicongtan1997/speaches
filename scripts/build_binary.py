from __future__ import annotations

import shutil
import subprocess
import sys
from pathlib import Path


def main() -> int:
    project_root = Path(__file__).parent.parent
    spec_file = project_root / "speaches.spec"
    dist_dir = project_root / "dist"
    build_dir = project_root / "build"

    if not spec_file.exists():
        print(f"Error: spec file not found at {spec_file}")
        return 1

    print(f"Cleaning previous build artifacts...")
    if dist_dir.exists():
        shutil.rmtree(dist_dir)
    if build_dir.exists():
        shutil.rmtree(build_dir)

    print(f"Building binary with PyInstaller...")
    result = subprocess.run(
        ["pyinstaller", "--clean", str(spec_file)],
        cwd=project_root,
        check=False,
    )

    if result.returncode != 0:
        print(f"Build failed with exit code {result.returncode}")
        return result.returncode

    binary_path = dist_dir / "speaches"
    if binary_path.exists():
        print(f"\nBuild successful!")
        print(f"Binary location: {binary_path}")
        print(f"Binary size: {binary_path.stat().st_size / (1024 * 1024):.2f} MB")
    else:
        print(f"Build completed but binary not found at expected location: {binary_path}")
        return 1

    return 0


if __name__ == "__main__":
    sys.exit(main())
