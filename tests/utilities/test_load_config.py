from pathlib import Path

import pytest
import yaml
from unittest.mock import patch
from area_classification.utilities.load_config import load_config


@pytest.fixture(scope="class")
def filepath():
    return Path("tests/data/utilities")

@pytest.fixture(scope="class")
def expected_config(filepath):
    expected_config_path = filepath / "expected_config.yaml"
    with expected_config_path.open("r") as file:
        return yaml.safe_load(file)
    

def test_load_config(filepath, expected_config):
                    
    # Mock the getpass.getuser function
    with patch("getpass.getuser", return_value="test_user"):
        
        config_path = filepath / "test_config.yaml"
        
        result = load_config(config_path=config_path, placeholder="{USERNAME}")
        
        assert result == expected_config