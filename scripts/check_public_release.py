#!/usr/bin/env python3
"""Lightweight public-release checks for JerryFDECourses.

This script catches common accidental disclosures and malformed course assets.
It does not replace human confidentiality review.
"""

from __future__ import annotations

import json
import py_compile
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF_PATH = Path(__file__).resolve()
MAX_FILE_BYTES = 2 * 1024 * 1024
ALLOWED_LARGE_EXTENSIONS = {".mp4", ".mov", ".webm"}
TEXT_EXTENSIONS = {
    ".md",
    ".txt",
    ".json",
    ".py",
    ".js",
    ".css",
    ".html",
    ".svg",
    ".yml",
    ".yaml",
    ".toml",
    ".csv",
    ".srt",
}

PATTERNS = {
    "AWS access key": re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    "GitHub token": re.compile(r"\bgh[pousr]_[A-Za-z0-9]{30,}\b"),
    "OpenAI-style secret": re.compile(r"\bsk-[A-Za-z0-9_-]{20,}\b"),
    "generic bearer token": re.compile(r"(?i)authorization\s*:\s*bearer\s+[A-Za-z0-9._-]{16,}"),
    "private IPv4": re.compile(
        r"\b(?:10\.\d{1,3}\.\d{1,3}\.\d{1,3}|"
        r"192\.168\.\d{1,3}\.\d{1,3}|"
        r"172\.(?:1[6-9]|2\d|3[01])\.\d{1,3}\.\d{1,3})\b"
    ),
    "absolute macOS user path": re.compile(r"/Users/[^/\s]+/"),
    "absolute Windows user path": re.compile(r"(?i)\bC:\\Users\\[^\\\s]+\\"),
    "email address": re.compile(r"\b[A-Z0-9._%+-]+@[A-Z0-9.-]+\.[A-Z]{2,}\b", re.I),
}

BOUNDARY_SENTENCE = "本模块使用合成案例"
IGNORE_DIRS = {".git", ".venv", "node_modules", "dist", "build", "output"}


def iter_files() -> list[Path]:
    files: list[Path] = []
    for path in ROOT.rglob("*"):
        if not path.is_file():
            continue
        if any(part in IGNORE_DIRS for part in path.parts):
            continue
        files.append(path)
    return files


def read_text(path: Path) -> str | None:
    if path.suffix.lower() not in TEXT_EXTENSIONS:
        return None
    try:
        return path.read_text(encoding="utf-8")
    except UnicodeDecodeError:
        return None


def check_file_sizes(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        size = path.stat().st_size
        if size > MAX_FILE_BYTES and path.suffix.lower() not in ALLOWED_LARGE_EXTENSIONS:
            errors.append(
                f"large file: {path.relative_to(ROOT)} is {size} bytes; review before publishing"
            )
    return errors


def check_sensitive_patterns(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        # Detection regexes are intentionally present in this script. Scanning
        # the scanner itself creates false positives without testing any course
        # content, so this one file is excluded from pattern matching only.
        if path.resolve() == SELF_PATH:
            continue
        text = read_text(path)
        if text is None:
            continue
        for name, pattern in PATTERNS.items():
            for match in pattern.finditer(text):
                line = text.count("\n", 0, match.start()) + 1
                errors.append(
                    f"{name}: {path.relative_to(ROOT)}:{line}: {match.group(0)[:80]}"
                )
    return errors


def check_json(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if path.suffix.lower() != ".json":
            continue
        try:
            json.loads(path.read_text(encoding="utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as exc:
            errors.append(f"invalid JSON: {path.relative_to(ROOT)}: {exc}")
    return errors


def check_svg(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if path.suffix.lower() != ".svg":
            continue
        try:
            ET.parse(path)
        except ET.ParseError as exc:
            errors.append(f"invalid SVG XML: {path.relative_to(ROOT)}: {exc}")
    return errors


def check_python(files: list[Path]) -> list[str]:
    errors: list[str] = []
    for path in files:
        if path.suffix.lower() != ".py":
            continue
        try:
            py_compile.compile(str(path), doraise=True)
        except py_compile.PyCompileError as exc:
            errors.append(f"Python syntax error: {path.relative_to(ROOT)}: {exc.msg}")
    return errors


def check_module_boundaries() -> list[str]:
    errors: list[str] = []
    modules_dir = ROOT / "modules"
    if not modules_dir.exists():
        return ["missing modules directory"]

    for module_dir in sorted(path for path in modules_dir.iterdir() if path.is_dir()):
        readme = module_dir / "README.md"
        if not readme.exists():
            errors.append(f"missing module README: {module_dir.relative_to(ROOT)}")
            continue
        text = readme.read_text(encoding="utf-8")
        if BOUNDARY_SENTENCE not in text:
            errors.append(
                f"missing public boundary statement: {readme.relative_to(ROOT)}"
            )
    return errors


def check_symlinks() -> list[str]:
    errors: list[str] = []
    for path in ROOT.rglob("*"):
        if path.is_symlink():
            errors.append(f"symlink requires review: {path.relative_to(ROOT)}")
    return errors


def main() -> int:
    files = iter_files()
    checks = [
        check_file_sizes(files),
        check_sensitive_patterns(files),
        check_json(files),
        check_svg(files),
        check_python(files),
        check_module_boundaries(),
        check_symlinks(),
    ]
    errors = [error for group in checks for error in group]

    if errors:
        print("Public release check failed:\n")
        for error in errors:
            print(f"- {error}")
        print("\nAutomatic checks are only one release gate; complete human review as well.")
        return 1

    print(f"Public release check passed for {len(files)} files.")
    print("Human confidentiality and copyright review is still required.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
