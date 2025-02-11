import pytest
from unittest.mock import patch
import subprocess
from main import get_dependencies

# Test for the get_dependencies function
@patch('subprocess.run')
def test_get_dependencies(mock_subprocess):
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=['pip', 'show', 'package'],
        returncode=0,
        stdout='Requires: dep1, dep2\n',
        stderr=''
    )

    # Package to test
    package_name = 'package'
    visited = set()

    dependencies, dependency_hierarchy = get_dependencies(package_name, visited)

    assert sorted(dependencies) == sorted(['dep2', 'dep1'])
    assert package_name in visited

@patch('subprocess.run')
def test_get_dependencies_error(mock_subprocess):
    mock_subprocess.return_value = subprocess.CompletedProcess(
        args=['pip', 'show', 'pipjh'],
        returncode=1,
        stdout='',
        stderr='Error: Package not found'
    )

    with pytest.raises(ValueError, match="Не удалось получить информацию о пакете pipjh"):
        get_dependencies('pipjh', set())
