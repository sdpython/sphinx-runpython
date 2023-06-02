import sys
import os
import unittest
from sphinx_runpython.runpython.run_cmd import run_cmd, skip_run_cmd
from sphinx_runpython.ext_test_case import ExtTestCase


class TestRunCmd(ExtTestCase):
    def test_run_cmd_1(self):
        cmd = "set" if sys.platform.startswith("win") else "env"
        out1, _ = run_cmd(cmd, wait=True)
        out2, _ = run_cmd(cmd, wait=True, communicate=False)
        self.maxDiff = None
        self.assertEqual(out1.strip(), out2.strip())

    def test_run_cmd_2(self):
        cmd = "set" if sys.platform.startswith("win") else "env"

        out3, err = run_cmd(cmd, wait=True, communicate=False, tell_if_no_output=600)
        out, err = skip_run_cmd(cmd, wait=True)
        assert len(out) == 0
        assert len(err) == 0
        counts = dict(out=[], err=[])

        def stop_running_if(out, err, counts=counts):
            if out:
                counts["out"].append(out)
            if err:
                counts["err"].append(err)

        out4, err = run_cmd(
            cmd,
            wait=True,
            communicate=False,
            tell_if_no_output=600,
            stop_running_if=stop_running_if,
        )

        out, err = skip_run_cmd(cmd, wait=True)
        self.assertEqual(len(out), 0)
        self.assertEqual(len(err), 0)
        self.maxDiff = None
        self.assertEqual(out3.strip(), out4.strip())
        assert len(counts["out"]) > 0
        if len(counts["err"]) > 0:
            raise AssertionError(counts["err"])

    def test_run_cmd_more(self):
        cmd = "more " + os.path.abspath(__file__)

        try:
            run_cmd(
                cmd,
                wait=True,
                communicate=False,
                tell_if_no_output=600,
                sin="\n\n\n" * 100,
            )
        except Exception as e:
            self.assertIn("ERROR", str(e))

        out, err = run_cmd(cmd, wait=True, communicate=True, sin="\n\n\n" * 100)
        self.assertGreater(len(out), 10)
        self.assertEqual(len(err), 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
