#!/usr/bin/env python3
"""Validate the dependency-free Selah GitHub bundle."""

from __future__ import annotations

import json
import hashlib
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SITE = ROOT / "site"
DATA = SITE / "data"
MAX_GITHUB_FILE_BYTES = 100 * 1024 * 1024
DISALLOWED_SUFFIXES = {
    ".doc",
    ".docx",
    ".mhtml",
    ".pdf",
    ".sfm",
    ".usfm",
    ".zip",
}


def load_assignment(path: Path, variable: str) -> object:
    text = path.read_text(encoding="utf-8")
    match = re.fullmatch(
        rf"\s*(?:window\.)?{re.escape(variable)}\s*=\s*(.+?)\s*;?\s*",
        text,
        flags=re.DOTALL,
    )
    if not match:
        raise ValueError(f"{path.name} does not assign {variable}")
    return json.loads(match.group(1))


def main() -> int:
    errors: list[str] = []

    for relative in (
        "site/index.html",
        "site/app.js",
        "site/styles.css",
        "site/data/index.js",
        "reports/project-validation.json",
        "reports/completion-register.json",
        "schema/annotation.v0.4.schema.json",
        "RIGHTS-AND-ATTRIBUTIONS.md",
        "PUBLIC-RELEASE-CHECKLIST.md",
        "VERSION",
        "MANIFEST.sha256",
    ):
        path = ROOT / relative
        if not path.is_file():
            errors.append(f"Missing required file: {relative}")

    psalm_files = sorted(DATA.glob("PSA[0-9][0-9][0-9].js")) if DATA.is_dir() else []
    expected_names = {f"PSA{number:03d}.js" for number in range(1, 151)}
    actual_names = {path.name for path in psalm_files}
    if actual_names != expected_names:
        missing = sorted(expected_names - actual_names)
        extra = sorted(actual_names - expected_names)
        errors.append(f"Psalm package mismatch; missing={missing}, extra={extra}")

    found_psalms: list[int] = []
    for path in psalm_files:
        try:
            package = load_assignment(path, "SELAH_PSALM")
            psalm = int(package["psalm"])
            found_psalms.append(psalm)
            expected = int(path.stem[3:])
            if psalm != expected:
                errors.append(f"{path.name} contains Psalm {psalm}")
            for key in ("verses", "annotations", "metadata"):
                if key not in package:
                    errors.append(f"{path.name} lacks {key}")
        except (OSError, ValueError, TypeError, KeyError, json.JSONDecodeError) as exc:
            errors.append(f"Could not parse {path.name}: {exc}")

    if found_psalms != list(range(1, 151)):
        errors.append("Parsed Psalm numbers are not the complete ordered range 1-150")

    try:
        register = json.loads((ROOT / "reports/completion-register.json").read_text(encoding="utf-8"))
        if len(register) != 150:
            errors.append(f"Completion register has {len(register)} entries instead of 150")
        pilot = sum(row.get("mode") == "PILOT" for row in register)
        systematic = sum(row.get("mode") == "SYSTEMATIC" for row in register)
        close_read = sum(row.get("stage") == "CLOSE_READ" for row in register)
        if (pilot, systematic, close_read) != (8, 142, 150):
            errors.append(
                "Completion register split is "
                f"pilot={pilot}, systematic={systematic}, close_read={close_read}"
            )
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"Could not validate completion register: {exc}")

    try:
        report = json.loads((ROOT / "reports/project-validation.json").read_text(encoding="utf-8"))
        if report.get("errors"):
            errors.append(f"Stored project report contains errors: {report['errors']}")
        if report.get("counts", {}).get("psalms") != 150:
            errors.append("Stored project report does not record 150 Psalms")
    except (OSError, ValueError, TypeError, json.JSONDecodeError) as exc:
        errors.append(f"Could not validate project report: {exc}")

    if (ROOT / "sources").exists():
        errors.append("Raw sources directory must not be included in the GitHub bundle")

    manifest_path = ROOT / "MANIFEST.sha256"
    manifest: dict[str, str] = {}
    try:
        for line_number, line in enumerate(manifest_path.read_text(encoding="utf-8").splitlines(), 1):
            match = re.fullmatch(r"([0-9a-f]{64})  (.+)", line)
            if not match:
                errors.append(f"Malformed manifest line {line_number}")
                continue
            manifest[match.group(2)] = match.group(1)
    except OSError as exc:
        errors.append(f"Could not read checksum manifest: {exc}")

    release_files: dict[str, Path] = {}
    for path in ROOT.rglob("*"):
        if not path.is_file() or ".git" in path.parts:
            continue
        relative = path.relative_to(ROOT)
        relative_posix = relative.as_posix()
        if relative_posix != "MANIFEST.sha256":
            release_files[relative_posix] = path
        if path.stat().st_size >= MAX_GITHUB_FILE_BYTES:
            errors.append(f"File exceeds GitHub's 100 MiB limit: {relative}")
        if path.suffix.lower() in DISALLOWED_SUFFIXES:
            errors.append(f"Raw/private source file type is not allowed: {relative}")

    if set(manifest) != set(release_files):
        missing = sorted(set(release_files) - set(manifest))
        extra = sorted(set(manifest) - set(release_files))
        errors.append(f"Checksum manifest inventory mismatch; missing={missing}, extra={extra}")
    else:
        for relative, path in release_files.items():
            actual = hashlib.sha256(path.read_bytes()).hexdigest()
            if actual != manifest[relative]:
                errors.append(f"Checksum mismatch: {relative}")

    if errors:
        print("Selah GitHub bundle validation FAILED")
        for error in errors:
            print(f"- {error}")
        return 1

    total_bytes = sum(path.stat().st_size for path in SITE.rglob("*") if path.is_file())
    print("Selah GitHub bundle validation PASSED")
    print(f"- Psalm packages: {len(psalm_files)}")
    print("- Draft split: 8 pilot + 142 systematic")
    print(f"- Static site size: {total_bytes / (1024 * 1024):.2f} MiB")
    print("- Stored project validation errors: 0")
    print("- Raw source archive: excluded")
    return 0


if __name__ == "__main__":
    sys.exit(main())
