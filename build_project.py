#!/usr/bin/env python3
"""Create the runnable Python archive required in the build directory."""

from pathlib import Path
import os
import zipapp


def main() -> None:
    project_root = Path(__file__).resolve().parent
    source_dir = project_root / "src"
    build_dir = project_root / "build"
    output = build_dir / "ic_project.pyz"

    build_dir.mkdir(parents=True, exist_ok=True)
    zipapp.create_archive(
        source=source_dir,
        target=output,
        interpreter="/usr/bin/env python3",
        main="main:main",
        compressed=True,
    )
    output.chmod(output.stat().st_mode | 0o111)
    print(f"Build completed: {output.relative_to(project_root)}")
    print("Run it with: python3 build/ic_project.pyz --help")


if __name__ == "__main__":
    main()
