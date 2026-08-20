#!/usr/bin/env python3
"""M01 public demo: turn a vague request into a reviewable task card.

This module deliberately does not call an LLM. It demonstrates the deterministic
skeleton that M02 will later augment with model-generated *candidates*.

All bundled data is synthetic and safe for public release.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Mapping

STATUS_DRAFT = "DRAFT"
STATUS_NEEDS_CLARIFICATION = "NEEDS_CLARIFICATION"
STATUS_READY = "READY"

REQUIRED_FIELDS = (
    "objective",
    "source",
    "time_range",
    "expected_output",
    "due_date",
    "owner",
    "acceptance_criteria",
)

QUESTION_MAP = {
    "objective": "需要完成的具体工作是什么？",
    "source": "用户问题存放在哪里？请给出一个明确的数据来源或演示文件。",
    "time_range": "“上个月”对应哪个具体日期范围？",
    "expected_output": "需要输出什么文件或材料？",
    "due_date": "评审的具体日期和截止时间是什么？",
    "owner": "谁负责完成这项任务？",
    "acceptance_criteria": "哪些条件满足后，可以认为整理工作完成？",
}

V0_DEFAULTS: dict[str, Any] = {
    "source": "feedback.csv",
    "time_range": {"relative": "LAST_MONTH"},
    "expected_output": ["PPT"],
    "due_date": "NEXT_FRIDAY",
    "owner": "CURRENT_USER",
    "acceptance_criteria": ["内容已整理"],
}


@dataclass(frozen=True)
class PipelineResult:
    """Files and state produced by a pipeline run."""

    status: str
    missing_fields: tuple[str, ...]
    task_card: dict[str, Any]
    questions: tuple[str, ...]
    run_record: dict[str, Any]


class InputError(ValueError):
    """Raised when a demo input cannot be read or validated."""


def read_text(path: Path) -> str:
    """Read a non-empty UTF-8 text file."""

    try:
        text = path.read_text(encoding="utf-8").strip()
    except FileNotFoundError as exc:
        raise InputError(f"找不到请求文件：{path}") from exc
    except UnicodeDecodeError as exc:
        raise InputError(f"请求文件不是 UTF-8：{path}") from exc

    if not text:
        raise InputError("原始请求为空。")
    return text


def read_json_object(path: Path) -> dict[str, Any]:
    """Read a UTF-8 JSON object."""

    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise InputError(f"找不到确认文件：{path}") from exc
    except UnicodeDecodeError as exc:
        raise InputError(f"确认文件不是 UTF-8：{path}") from exc
    except json.JSONDecodeError as exc:
        raise InputError(f"确认文件不是有效 JSON：{exc}") from exc

    if not isinstance(value, dict):
        raise InputError("确认文件必须是 JSON object。")
    return value


def new_task_card(request_id: str, request_text: str) -> dict[str, Any]:
    """Create the empty public-demo task card."""

    return {
        "request_id": request_id,
        "original_request": request_text,
        "objective": None,
        "source": None,
        "time_range_text": None,
        "time_range": None,
        "usage_context": None,
        "expected_output": None,
        "due_date": None,
        "owner": None,
        "reviewer": None,
        "acceptance_criteria": [],
        "confidentiality": "PUBLIC_DEMO",
        "confirmed_by": None,
        "field_provenance": {},
        "status": STATUS_DRAFT,
    }


def set_field(
    card: dict[str, Any],
    field: str,
    value: Any,
    provenance: str,
) -> None:
    """Set a field and record where the value came from."""

    card[field] = value
    card["field_provenance"][field] = provenance


def extract_explicit_fields(request_text: str, request_id: str = "REQ-001") -> dict[str, Any]:
    """Extract only information explicitly present in the synthetic request.

    This is a small deterministic teaching extractor, not a general Chinese NLP
    system. M02 will introduce an LLM candidate extractor behind the same task
    card contract.
    """

    card = new_task_card(request_id=request_id, request_text=request_text)

    if "用户问题" in request_text and "整理" in request_text:
        set_field(card, "objective", "整理用户问题", "SOURCE_TEXT")

    relative_time_match = re.search(r"(上个月|本月|最近\s*\d+\s*天)", request_text)
    if relative_time_match:
        set_field(
            card,
            "time_range_text",
            relative_time_match.group(1).replace(" ", ""),
            "SOURCE_TEXT",
        )

    if "评审" in request_text:
        context_match = re.search(r"(本周|下周|\d{1,2}月\d{1,2}日)?[^，。]*评审", request_text)
        usage_context = context_match.group(0) if context_match else "评审使用"
        set_field(card, "usage_context", usage_context, "SOURCE_TEXT")

    return card


def apply_v0_defaults(card: dict[str, Any]) -> dict[str, Any]:
    """Apply intentionally unsafe defaults used by the lesson's failure demo."""

    for field, default in V0_DEFAULTS.items():
        if is_missing(card.get(field)):
            set_field(card, field, default, "SYSTEM_DEFAULT_UNCONFIRMED")

    card["status"] = STATUS_READY
    return card


def validate_confirmation(confirmation: Mapping[str, Any]) -> None:
    """Validate the shape of human confirmation used in the public lab."""

    confirmed_by = confirmation.get("confirmed_by")
    if not isinstance(confirmed_by, str) or not confirmed_by.strip():
        raise InputError("confirmation.json 必须包含非空 confirmed_by。")

    if "time_range" in confirmation:
        time_range = confirmation["time_range"]
        if not isinstance(time_range, dict):
            raise InputError("time_range 必须是包含 start/end 的 object。")
        if not time_range.get("start") or not time_range.get("end"):
            raise InputError("time_range 必须同时包含 start 和 end。")

    if "expected_output" in confirmation:
        outputs = confirmation["expected_output"]
        if not isinstance(outputs, list) or not all(
            isinstance(item, str) and item.strip() for item in outputs
        ):
            raise InputError("expected_output 必须是非空字符串数组。")

    if "acceptance_criteria" in confirmation:
        criteria = confirmation["acceptance_criteria"]
        if not isinstance(criteria, list) or not all(
            isinstance(item, str) and item.strip() for item in criteria
        ):
            raise InputError("acceptance_criteria 必须是非空字符串数组。")


def merge_human_confirmation(
    card: dict[str, Any], confirmation: Mapping[str, Any]
) -> dict[str, Any]:
    """Merge explicitly human-confirmed fields into the task card."""

    validate_confirmation(confirmation)
    confirmed_by = str(confirmation["confirmed_by"]).strip()

    allowed_fields = {
        "objective",
        "source",
        "time_range",
        "expected_output",
        "due_date",
        "owner",
        "reviewer",
        "acceptance_criteria",
    }

    for field in allowed_fields:
        if field in confirmation:
            set_field(card, field, confirmation[field], "HUMAN_CONFIRMED")

    card["confirmed_by"] = confirmed_by
    card["field_provenance"]["confirmed_by"] = "HUMAN_CONFIRMED"
    return card


def is_missing(value: Any) -> bool:
    """Return True for values that cannot satisfy a required task field."""

    if value is None:
        return True
    if isinstance(value, str):
        return not value.strip()
    if isinstance(value, (list, tuple, set, dict)):
        return len(value) == 0
    return False


def find_missing_fields(card: Mapping[str, Any]) -> tuple[str, ...]:
    """Return required fields that are still missing."""

    return tuple(field for field in REQUIRED_FIELDS if is_missing(card.get(field)))


def build_questions(missing_fields: tuple[str, ...]) -> tuple[str, ...]:
    """Create deterministic clarification questions."""

    return tuple(QUESTION_MAP[field] for field in missing_fields)


def utc_now_iso() -> str:
    """Return an auditable UTC timestamp."""

    return datetime.now(timezone.utc).replace(microsecond=0).isoformat()


def run_pipeline(
    *,
    request_text: str,
    request_name: str,
    mode: str,
    confirmation: Mapping[str, Any] | None = None,
    request_id: str = "REQ-001",
) -> PipelineResult:
    """Run the v0 failure demo or v1 readiness pipeline."""

    card = extract_explicit_fields(request_text, request_id=request_id)

    if mode == "v0":
        card = apply_v0_defaults(card)
        missing_fields: tuple[str, ...] = ()
        questions: tuple[str, ...] = ()
        message = "v0 使用未确认默认值，将任务标记为 READY。"
    elif mode == "v1":
        if confirmation is not None:
            card = merge_human_confirmation(card, confirmation)

        missing_fields = find_missing_fields(card)
        questions = build_questions(missing_fields)
        card["status"] = (
            STATUS_NEEDS_CLARIFICATION if missing_fields else STATUS_READY
        )
        message = (
            "任务信息不足，尚未进入执行阶段。"
            if missing_fields
            else "当前必填信息已得到确认，可以进入执行准备阶段。"
        )
    else:
        raise InputError(f"未知 mode：{mode}")

    run_record = {
        "request_id": request_id,
        "run_at": utc_now_iso(),
        "mode": mode,
        "status": card["status"],
        "source_request": request_name,
        "missing_fields": list(missing_fields),
        "confirmed_fields": sorted(
            field
            for field, provenance in card["field_provenance"].items()
            if provenance == "HUMAN_CONFIRMED" and field != "confirmed_by"
        ),
        "confirmed_by": card.get("confirmed_by"),
        "message": message,
        "public_demo": True,
    }

    return PipelineResult(
        status=card["status"],
        missing_fields=missing_fields,
        task_card=card,
        questions=questions,
        run_record=run_record,
    )


def write_json(path: Path, value: Any) -> None:
    """Write stable, readable UTF-8 JSON."""

    path.write_text(
        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def render_questions(questions: tuple[str, ...]) -> str:
    """Render questions as Markdown."""

    if not questions:
        return "# 澄清问题\n\n当前没有待澄清的必填字段。\n"

    body = "\n".join(f"{index}. {question}" for index, question in enumerate(questions, 1))
    return f"# 澄清问题\n\n{body}\n"


def write_result(output_dir: Path, result: PipelineResult) -> None:
    """Write all public course artifacts."""

    output_dir.mkdir(parents=True, exist_ok=True)
    write_json(output_dir / "task_card.json", result.task_card)
    write_json(output_dir / "run_record.json", result.run_record)
    (output_dir / "questions.md").write_text(
        render_questions(result.questions), encoding="utf-8"
    )
    (output_dir / "status.txt").write_text(result.status + "\n", encoding="utf-8")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="M01: 把模糊请求变成可确认的任务卡（公开合成案例）"
    )
    parser.add_argument("--request", type=Path, required=True, help="UTF-8 请求文本")
    parser.add_argument(
        "--confirmation", type=Path, help="可选：人工确认 JSON 文件"
    )
    parser.add_argument("--output", type=Path, required=True, help="输出目录")
    parser.add_argument(
        "--mode", choices=("v0", "v1"), default="v1", help="v0 为静默默认值失败演示"
    )
    parser.add_argument("--request-id", default="REQ-001")
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)

    try:
        request_text = read_text(args.request)
        confirmation = (
            read_json_object(args.confirmation) if args.confirmation else None
        )
        result = run_pipeline(
            request_text=request_text,
            request_name=args.request.name,
            mode=args.mode,
            confirmation=confirmation,
            request_id=args.request_id,
        )
        write_result(args.output, result)
    except InputError as exc:
        print(f"input_error={exc}", file=sys.stderr)
        return 3

    print(f"status={result.status}")
    if result.missing_fields:
        print("missing=" + ",".join(result.missing_fields))

    return 0 if result.status == STATUS_READY else 2


if __name__ == "__main__":
    raise SystemExit(main())
