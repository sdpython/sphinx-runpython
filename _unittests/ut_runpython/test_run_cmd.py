import sys
import os
import tempfile
import unittest
from sphinx_runpython.runpython.run_cmd import (
    run_cmd,
    skip_run_cmd,
    get_interpreter_path,
    split_cmp_command,
    decode_outerr,
    RunCmdException,
)
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
            self.assertIn("Argument 'communicate' should be True", str(e))

        out, err = run_cmd(cmd, wait=True, communicate=True, sin="\n\n\n" * 100)
        self.assertGreater(len(out), 10)
        self.assertEqual(len(err), 0)

    def test_get_interpreter_path(self):
        path = get_interpreter_path()
        self.assertIsNotNone(path)
        self.assertIn("python", path.lower())

    def test_split_cmp_command_simple(self):
        result = split_cmp_command("echo hello world")
        self.assertEqual(result, ["echo", "hello", "world"])

    def test_split_cmp_command_with_quotes(self):
        result = split_cmp_command('echo "hello world"')
        self.assertEqual(result, ["echo", "hello world"])

    def test_split_cmp_command_no_remove_quotes(self):
        result = split_cmp_command('echo "hello world"', remove_quotes=False)
        self.assertEqual(result, ["echo", '"hello world"'])

    def test_split_cmp_command_list(self):
        cmd = ["echo", "hello"]
        result = split_cmp_command(cmd)
        self.assertIs(result, cmd)

    def test_decode_outerr_bytes(self):
        result = decode_outerr(b"hello world", "utf-8", "ignore", "test")
        self.assertEqual(result, "hello world")

    def test_decode_outerr_none_encoding(self):
        result = decode_outerr(b"hello", None, "ignore", "test")
        self.assertEqual(result, "hello")

    def test_decode_outerr_not_bytes(self):
        self.assertRaise(
            lambda: decode_outerr("hello", "utf-8", "ignore", "test"), TypeError
        )

    def test_run_cmd_with_change_path(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            out, err = run_cmd("pwd", wait=True, change_path=tmpdir)
            self.assertIn(os.path.realpath(tmpdir), os.path.realpath(out.strip()))

    def test_run_cmd_with_logf(self):
        logs = []

        def logf(prefix, msg):
            logs.append((prefix, msg))

        cmd = "echo hello"
        out, err = run_cmd(cmd, wait=True, logf=logf)
        self.assertGreater(len(logs), 0)

    def test_run_cmd_list_cmd(self):
        out, err = run_cmd(["echo", "test"], wait=True)
        self.assertIn("test", out)

    def test_run_cmd_preprocess_false(self):
        out, err = run_cmd("echo hello", wait=True, preprocess=False, shell=True)
        self.assertIn("hello", out)

    def test_run_cmd_exception_class(self):
        exc = RunCmdException("test error")
        self.assertIsInstance(exc, Exception)


if __name__ == "__main__":
    unittest.main(verbosity=2)


class TestRunCmdExtra(ExtTestCase):
    def test_decode_outerr_unicode_fallback(self):
        # Bytes that fail ASCII but succeed with utf8 fallback
        # 0xc3 0xa9 is the UTF-8 encoding of 'é'
        result = decode_outerr(b"\xc3\xa9 hello", "ascii", "strict", "test")
        self.assertIn("hello", result)

    def test_decode_outerr_unicode_error(self):
        # Bytes that fail both ASCII and UTF-8 strict decoding
        # 0x80 is not valid in ascii strict or utf-8 strict
        self.assertRaise(
            lambda: decode_outerr(b"\x80\x81\x82", "ascii", "strict", "test"),
            RuntimeError,
        )

    def test_run_cmd_with_logf_list(self):
        logs = []

        def logf(prefix, msg):
            logs.append((prefix, msg))

        out, err = run_cmd(["echo", "hello"], wait=True, logf=logf)
        self.assertGreater(len(logs), 0)
        self.assertIn("hello", out)

    def test_run_cmd_catch_exit(self):
        out, err = run_cmd("echo hello", wait=True, catch_exit=True)
        self.assertIn("hello", out)

    def test_run_cmd_with_prefix_log(self):
        logs = []

        def logf(prefix, msg):
            logs.append((prefix, msg))

        out, err = run_cmd("echo hello", wait=True, logf=logf, prefix_log="[test] ")
        self.assertGreater(len(logs), 0)
        self.assertTrue(any("[test]" in str(log) for log in logs))

    def test_run_cmd_nowait(self):
        # run_cmd with wait=False returns (pproc, None)
        result = run_cmd("echo hello", wait=False)
        pproc, _ = result
        pproc.__exit__(None, None, None)


if __name__ == "__main__":
    unittest.main(verbosity=2)
