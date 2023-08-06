import unittest
from unittest.mock import patch, mock_open
from click.testing import CliRunner
from stellanow_cli.commands import configure


class TestConfigureCommand(unittest.TestCase):
    def setUp(self):
        self.runner = CliRunner()

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.expanduser')
    def test_configure_default_profile(self, mock_expanduser, mock_exists, mock_file):
        mock_expanduser.return_value = "/home/test_user"

        result = self.runner.invoke(
            configure,
            input="default_access_key\ndefault_access_token\na3fb6c97-b231-471e-8a5a-92a55f33ca5e\nf45cd487-7c98-4b72-a2da-c409f662b1e2\n"
        )
        mock_file.assert_called_once_with("/home/test_user/.stellanow/config.ini", "w")

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration for profile 'DEFAULT' saved successfully", result.output)

    @patch('builtins.open', new_callable=mock_open)
    @patch('os.path.exists', return_value=True)
    @patch('os.path.expanduser')
    def test_configure_custom_profile(self, mock_expanduser, mock_exists, mock_file):
        mock_expanduser.return_value = "/home/test_user"

        result = self.runner.invoke(
            configure,
            ["--profile", "custom"],
            input="custom_access_key\ncustom_access_token\na3fb6c97-b231-471e-8a5a-92a55f33ca5e\nf45cd487-7c98-4b72-a2da-c409f662b1e2\n"
        )
        mock_file.assert_called_once_with("/home/test_user/.stellanow/config.ini", "w")

        self.assertEqual(result.exit_code, 0)
        self.assertIn("Configuration for profile 'custom' saved successfully", result.output)


if __name__ == "__main__":
    unittest.main()
