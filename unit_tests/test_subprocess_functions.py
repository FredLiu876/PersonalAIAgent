import unittest
import subprocess
from unittest.mock import patch, MagicMock
from functions.subprocess_functions import run_bash_command

class TestSubprocessFunctions(unittest.TestCase):

    @patch('subprocess.run')
    def test_run_bash_command_success(self, mock_run):
        mock_run.return_value = MagicMock(stdout='Command executed successfully', stderr='', returncode=0)
        result = run_bash_command("echo 'Hello World'")
        self.assertEqual(result, 'Command executed successfully')

    @patch('subprocess.run')
    def test_run_bash_command_failure(self, mock_run):
        mock_run.side_effect = subprocess.CalledProcessError(1, 'cmd', output='', stderr='Error occurred')
        with self.assertRaises(Exception) as context:
            run_bash_command("exit 1")
        self.assertEqual(str(context.exception), 'Error occurred')

if __name__ == '__main__':
    unittest.main()