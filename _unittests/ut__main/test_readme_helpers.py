import unittest
from sphinx_runpython.ext_test_case import ExtTestCase
from sphinx_runpython.readme import (
    VirtualEnvError,
    NotImplementedErrorFromVirtualEnvironment,
    is_virtual_environment,
    build_venv_cmd,
)


class TestReadmeHelpers(ExtTestCase):
    def test_virtual_env_error(self):
        exc = VirtualEnvError("test error")
        self.assertIsInstance(exc, Exception)

    def test_not_implemented_from_virtual_environment(self):
        exc = NotImplementedErrorFromVirtualEnvironment("test error")
        self.assertIsInstance(exc, NotImplementedError)

    def test_is_virtual_environment(self):
        result = is_virtual_environment()
        self.assertIn(result, {True, False})

    def test_build_venv_cmd_no_params(self):
        cmd = build_venv_cmd({}, ["/tmp/venv"])
        self.assertIn("venv", cmd)
        self.assertIn("/tmp/venv", cmd)

    def test_build_venv_cmd_with_none_value(self):
        cmd = build_venv_cmd({"system-site-packages": None}, ["/tmp/venv"])
        self.assertIn("--system-site-packages", cmd)

    def test_build_venv_cmd_with_value(self):
        cmd = build_venv_cmd({"copies": "1"}, ["/tmp/venv"])
        self.assertIn("--copies=1", cmd)


if __name__ == "__main__":
    unittest.main(verbosity=2)
