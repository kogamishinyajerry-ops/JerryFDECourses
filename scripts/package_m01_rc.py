#!/usr/bin/env python3
"""Build a review-only M01 RC package.

The package is deliberately labelled RC1_CANDIDATE. Creating it does not
publish the course and does not change the module to RELEASED.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import shutil
import stat
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODULE_SOURCE = ROOT / "modules" / "M01"
PACKAGE_NAME = "M01_RC1_CANDIDATE"
FIXED_ZIP_TIME = (2026, 1, 1, 0, 0, 0)

INCLUDE_ROOT_FILES = (
    "README.md",
    "CHANGELOG.md",
    "LICENSE",
)

INCLUDE_DOCS = (
    "docs/00_PROJECT_CHARTER.md",
    "docs/01_TEACHING_AND_BUILD_STANDARD.md",
    "docs/02_PUBLIC_RELEASE_AND_SECURITY.md",
    "docs/03_COURSE_MAP.md",
)

IGNORE_NAMES = {
    ".DS_Store",
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--output-dir",
        type=Path,
        default=ROOT / "dist",
        help="Directory that receives the package directory and ZIP file.",
    )
    parser.add_argument(
        "--source-commit",
        default=os.environ.get("GITHUB_SHA", "UNKNOWN"),
        help="Commit SHA recorded inside the review package.",
    )
    return parser.parse_args()


def should_ignore(path: Path) -> bool:
    if path.name in IGNORE_NAMES:
        return True
    if path.suffix == ".pyc":
        return True
    if path.name.startswith("output") and path.parent.name == "lab":
        return True
    return False


def copy_tree(source: Path, destination: Path) -> None:
    if not source.is_dir():
        raise FileNotFoundError(f"missing module source: {source}")

    for source_path in sorted(source.rglob("*")):
        relative = source_path.relative_to(source)
        if any(should_ignore(part) for part in [source_path, *source_path.parents]):
            continue
        if source_path.is_symlink():
            raise ValueError(f"symlink is not allowed in RC package: {relative}")
        target = destination / relative
        if source_path.is_dir():
            target.mkdir(parents=True, exist_ok=True)
        elif source_path.is_file():
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source_path, target)


def copy_file(relative_path: str, package_root: Path) -> None:
    source = ROOT / relative_path
    if not source.is_file():
        raise FileNotFoundError(f"missing package input: {relative_path}")
    target = package_root / relative_path
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_status(package_root: Path, source_commit: str) -> None:
    status = {
        "course": "AI 时代的工业 FDE",
        "module": "M01｜从一条模糊需求开始",
        "package_status": "RC1_CANDIDATE",
        "source_commit": source_commit,
        "released": False,
        "pilot_complete": False,
        "contains_final_video": False,
        "remaining_gates": [
            "真人素材与正式旁白",
            "正式屏幕录制与第一版剪辑",
            "逐帧公开安全和版权复核",
            "3–5 名目标学员试讲",
            "试讲勘误和最终版本冻结",
        ],
    }
    (package_root / "PACKAGE_STATUS.json").write_text(
        json.dumps(status, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    (package_root / "READ_THIS_FIRST.md").write_text(
        "# M01 RC1 审阅包\n\n"
        "本包用于课程录制、人工复核和试讲。\n\n"
        "```text\nstatus = RC1_CANDIDATE\nreleased = false\n```\n\n"
        "它包含课程工程、Build Lab、互动课件、视觉资产和制作交接文件，"
        "不包含最终成片，也没有通过真实学员验证。\n\n"
        "从 `M01/RC1_STATUS.md` 开始阅读。\n",
        encoding="utf-8",
    )


def write_manifest(package_root: Path) -> None:
    lines: list[str] = []
    for path in sorted(package_root.rglob("*")):
        if path.is_file() and path.name != "MANIFEST.sha256":
            relative = path.relative_to(package_root).as_posix()
            lines.append(f"{sha256(path)}  {relative}")
    (package_root / "MANIFEST.sha256").write_text(
        "\n".join(lines) + "\n", encoding="utf-8"
    )


def create_deterministic_zip(package_root: Path, zip_path: Path) -> None:
    with zipfile.ZipFile(zip_path, "w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as archive:
        for path in sorted(package_root.rglob("*")):
            if not path.is_file():
                continue
            relative = (Path(package_root.name) / path.relative_to(package_root)).as_posix()
            info = zipfile.ZipInfo(relative, FIXED_ZIP_TIME)
            info.compress_type = zipfile.ZIP_DEFLATED
            info.external_attr = (stat.S_IFREG | 0o644) << 16
            archive.writestr(info, path.read_bytes())


def main() -> int:
    args = parse_args()
    output_dir = args.output_dir.resolve()
    package_root = output_dir / PACKAGE_NAME
    short_commit = args.source_commit[:12] if args.source_commit != "UNKNOWN" else "UNKNOWN"
    zip_path = output_dir / f"JerryFDECourses_{PACKAGE_NAME}_{short_commit}.zip"

    if package_root.exists():
        shutil.rmtree(package_root)
    output_dir.mkdir(parents=True, exist_ok=True)
    package_root.mkdir(parents=True)

    copy_tree(MODULE_SOURCE, package_root / "M01")
    for relative_path in INCLUDE_ROOT_FILES:
        copy_file(relative_path, package_root)
    for relative_path in INCLUDE_DOCS:
        copy_file(relative_path, package_root)

    write_status(package_root, args.source_commit)
    write_manifest(package_root)
    create_deterministic_zip(package_root, zip_path)

    print(f"package_dir={package_root}")
    print(f"package_zip={zip_path}")
    print(f"package_status=RC1_CANDIDATE")
    print(f"source_commit={args.source_commit}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
