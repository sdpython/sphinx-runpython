import sys
import unittest
from sphinx_runpython.runpython.run_cmd import run_cmd, parse_exception_message
from sphinx_runpython.ext_test_case import ExtTestCase


class TestRunCmdException(ExtTestCase):
    def test_run_cmd_exc(self):
        cmd = "unexpectedcommand"
        ex = "not affected"
        try:
            out, err = run_cmd(
                cmd,
                wait=True,
                log_error=False,
                catch_exit=True,
                communicate=False,
                tell_if_no_output=120,
            )
            no_exception = True
            ex = None
        except Exception as e:
            no_exception = False
            out, err = parse_exception_message(e)
            ex = e
        self.assertTrue(not no_exception)
        if sys.platform.startswith("win"):
            if out is None or err is None:
                raise AssertionError("A\n" + str(ex))
            if len(out) > 0:
                raise AssertionError("B\n" + str(ex))
            if len(err) == 0:
                raise AssertionError("C\n" + str(ex))
        else:
            self.assertTrue(out is None)
            self.assertTrue(err is None)
            self.assertTrue(isinstance(ex, Exception))


if __name__ == "__main__":
    unittest.main()
