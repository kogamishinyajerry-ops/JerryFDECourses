from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LAB_DIR = Path(__file__).resolve().parents[1]
if str(LAB_DIR) not in sys.path:
    sys.path.insert(0, str(LAB_DIR))

import task_pipeline as pipeline  # noqa: E402


REQUEST = "请把上个月收到的用户问题整理一下，下周评审时用。"

CONFIRMATION = {
    "source": "feedback.csv",
    "time_range": {"start": "2026-07-01", "end": "2026-07-31"},
    "expected_output": ["Excel 汇总表", "一页摘要"],
    "due_date": "2026-08-10T17:00:00+08:00",
    "owner": "Alex",
    "reviewer": "Morgan",
    "acceptance_criteria": [
        "全部问题完成分类",
        "重复项已合并",
        "每项保留原始编号",
    ],
    "confirmed_by": "DEMO_REQUESTER",
}


class ExtractorTests(unittest.TestCase):
    def test_extracts_only_explicit_source_text(self) -> None:
        card = pipeline.extract_explicit_fields(REQUEST)

        self.assertEqual(card["objective"], "整理用户问题")
        self.assertEqual(card["time_range_text"], "上个月")
        self.assertIn("评审", card["usage_context"])

        self.assertIsNone(card["source"])
        self.assertIsNone(card["expected_output"])
        self.assertIsNone(card["due_date"])
        self.assertIsNone(card["owner"])
        self.assertEqual(card["acceptance_criteria"], [])

        self.assertEqual(
            card["field_provenance"]["objective"], "SOURCE_TEXT"
        )


class PipelineTests(unittest.TestCase):
    def test_v0_demonstrates_unconfirmed_defaults(self) -> None:
        result = pipeline.run_pipeline(
            request_text=REQUEST,
            request_name="request.txt",
            mode="v0",
        )

        self.assertEqual(result.status, pipeline.STATUS_READY)
        self.assertEqual(result.missing_fields, ())
        self.assertEqual(result.task_card["expected_output"], ["PPT"])
        self.assertEqual(result.task_card["due_date"], "NEXT_FRIDAY")
        self.assertEqual(result.task_card["owner"], "CURRENT_USER")
        self.assertEqual(
            result.task_card["field_provenance"]["owner"],
            "SYSTEM_DEFAULT_UNCONFIRMED",
        )
        self.assertIsNone(result.task_card["confirmed_by"])

    def test_v1_stops_when_required_information_is_missing(self) -> None:
        result = pipeline.run_pipeline(
            request_text=REQUEST,
            request_name="request.txt",
            mode="v1",
        )

        self.assertEqual(result.status, pipeline.STATUS_NEEDS_CLARIFICATION)
        self.assertIn("source", result.missing_fields)
        self.assertIn("time_range", result.missing_fields)
        self.assertIn("owner", result.missing_fields)
        self.assertGreaterEqual(len(result.questions), 5)
        self.assertEqual(result.run_record["confirmed_fields"], [])

    def test_v1_becomes_ready_after_human_confirmation(self) -> None:
        result = pipeline.run_pipeline(
            request_text=REQUEST,
            request_name="request.txt",
            mode="v1",
            confirmation=CONFIRMATION,
        )

        self.assertEqual(result.status, pipeline.STATUS_READY)
        self.assertEqual(result.missing_fields, ())
        self.assertEqual(result.questions, ())
        self.assertEqual(result.task_card["owner"], "Alex")
        self.assertEqual(result.task_card["confirmed_by"], "DEMO_REQUESTER")
        self.assertEqual(
            result.task_card["field_provenance"]["due_date"],
            "HUMAN_CONFIRMED",
        )
        self.assertIn("source", result.run_record["confirmed_fields"])

    def test_confirmation_requires_confirmed_by(self) -> None:
        invalid = dict(CONFIRMATION)
        invalid.pop("confirmed_by")

        with self.assertRaises(pipeline.InputError):
            pipeline.run_pipeline(
                request_text=REQUEST,
                request_name="request.txt",
                mode="v1",
                confirmation=invalid,
            )

    def test_confirmation_rejects_incomplete_time_range(self) -> None:
        invalid = dict(CONFIRMATION)
        invalid["time_range"] = {"start": "2026-07-01"}

        with self.assertRaises(pipeline.InputError):
            pipeline.run_pipeline(
                request_text=REQUEST,
                request_name="request.txt",
                mode="v1",
                confirmation=invalid,
            )

    def test_write_result_creates_four_course_artifacts(self) -> None:
        result = pipeline.run_pipeline(
            request_text=REQUEST,
            request_name="request.txt",
            mode="v1",
        )

        with tempfile.TemporaryDirectory() as temp_dir:
            output_dir = Path(temp_dir)
            pipeline.write_result(output_dir, result)

            self.assertTrue((output_dir / "task_card.json").exists())
            self.assertTrue((output_dir / "questions.md").exists())
            self.assertTrue((output_dir / "run_record.json").exists())
            self.assertTrue((output_dir / "status.txt").exists())

            card = json.loads(
                (output_dir / "task_card.json").read_text(encoding="utf-8")
            )
            self.assertEqual(card["status"], pipeline.STATUS_NEEDS_CLARIFICATION)


class CliTests(unittest.TestCase):
    def test_cli_exit_codes_reflect_readiness(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            root = Path(temp_dir)
            request_path = root / "request.txt"
            confirmation_path = root / "confirmation.json"
            request_path.write_text(REQUEST, encoding="utf-8")
            confirmation_path.write_text(
                json.dumps(CONFIRMATION, ensure_ascii=False), encoding="utf-8"
            )

            needs_clarification = pipeline.main(
                [
                    "--mode",
                    "v1",
                    "--request",
                    str(request_path),
                    "--output",
                    str(root / "needs-clarification"),
                ]
            )
            ready = pipeline.main(
                [
                    "--mode",
                    "v1",
                    "--request",
                    str(request_path),
                    "--confirmation",
                    str(confirmation_path),
                    "--output",
                    str(root / "ready"),
                ]
            )

            self.assertEqual(needs_clarification, 2)
            self.assertEqual(ready, 0)


if __name__ == "__main__":
    unittest.main()
