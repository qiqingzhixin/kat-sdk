from __future__ import annotations

import importlib.util
import unittest

import kat


class WorkflowTest(unittest.TestCase):
    def test_sdk_does_not_need_cli_runtime(self):
        self.assertIsNone(importlib.util.find_spec("_kat_runtime"))

    def test_declaration_preserves_callable_and_copies_metadata(self):
        descriptions = {"value": " Input value "}

        def example(ctx: kat.Context, value: str):
            return None

        decorated = kat.workflow(
            name="example", description=" Example ", parameters=descriptions
        )(example)
        descriptions["value"] = "Changed"
        self.assertIs(decorated, example)
        self.assertEqual(decorated.__kat_workflow__.description, "Example")
        self.assertEqual(decorated.__kat_workflow__.parameters, (("value", "Input value"),))
        with self.assertRaises(ValueError):
            kat.workflow(name="again", description="Again")(example)

    def test_context_requires_execution_binding(self):
        ctx = kat.Context()
        for name in ("datasource_root", "scratch_root"):
            with self.subTest(name=name), self.assertRaises(RuntimeError):
                getattr(ctx, name)
        with self.assertRaises(RuntimeError):
            ctx.run("example", "example")

    def test_temporal_values_remain_available_without_runtime(self):
        self.assertEqual(str(kat.Duration("0.125ms")), "0.125ms")
        self.assertEqual(str(kat.WallClockTimestamp("2026-09-16T08:00:00+08:00")), "2026-09-16T00:00:00Z")


if __name__ == "__main__":
    unittest.main()
