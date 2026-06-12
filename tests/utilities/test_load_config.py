import getpass
import unittest

from area_classification.utilities.load_config import load_config


class TestLoadConfig(unittest.TestCase):
    def test_load_config_with_placeholder(self):
        # Arrange
        config_path = "tests/data/utilities/test_config.yaml"  # Path to your test YAML file
        placeholder = "{USERNAME}"
        expected_username = getpass.getuser()
        expected_filepath = f"C:/Users/{expected_username}/Repos/Area_Classification"

        # Act
        result = load_config(config_path, placeholder)

        # Assert
        self.assertIn("filepath", result)
        self.assertEqual(result["filepath"], expected_filepath)


if __name__ == "__main__":
    unittest.main()
