import unittest
from sphinx_runpython.runpython.run_cmd import run_cmd
from sphinx_runpython.ext_test_case import ExtTestCase


class TestRunCmdTimeout(ExtTestCase):
    def test_run_cmd_timeout(self):
        if __name__ == "__main__":
            cmd = "more"
            out, err = run_cmd(
                cmd, wait=True, tell_if_no_output=1, communicate=False, timeout=3
            )
            self.assertIn("Process killed", err)
            # kill does not work


if __name__ == "__main__":
    unittest.main()
