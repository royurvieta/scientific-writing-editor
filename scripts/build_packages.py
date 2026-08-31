#!/usr/bin/env python3
"""Build reproducible Codex and Claude skill archives."""

from __future__ import annotations

from pathlib import Path
import sys
import zipfile


ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "scientific-writing-editor"
SKILL_DIR = ROOT / "skills" / SKILL_NAME
FIXED_TIMESTAMP = (2020, 1, 1, 0, 0, 0)


def _source_files() -> list[Path]:
    files: list[Path] = []
    for path in SKILL_DIR.rglob("*"):
        if not path.is_file():
            continue
        if "__pycache__" in path.parts or path.name.startswith("._") or path.name == ".DS_Store":
            continue
        files.append(path)
    return sorted(files, key=lambda path: path.as_posix())


def _write_archive(path: Path, prefix: str) -> None:
    with zipfile.ZipFile(path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for source in _source_files():
            relative = source.relative_to(SKILL_DIR).as_posix()
            arcname = f"{prefix}/{relative}" if prefix else relative
            info = zipfile.ZipInfo(arcname, FIXED_TIMESTAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (0o755 if source.stat().st_mode & 0o111 else 0o644) << 16
            archive.writestr(info, source.read_bytes())


def build_packages(output_dir: Path) -> tuple[Path, Path]:
    if not (SKILL_DIR / "SKILL.md").is_file():
        raise FileNotFoundError(f"Missing skill entrypoint: {SKILL_DIR / 'SKILL.md'}")

    output_dir.mkdir(parents=True, exist_ok=True)
    codex_zip = output_dir / f"{SKILL_NAME}-codex.zip"
    claude_zip = output_dir / f"{SKILL_NAME}-claude.zip"
    _write_archive(codex_zip, SKILL_NAME)
    _write_archive(claude_zip, "")
    return codex_zip, claude_zip


def main() -> int:
    output = Path(sys.argv[1]) if len(sys.argv) > 1 else ROOT / "dist"
    for archive in build_packages(output):
        print(archive)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
