import pytest
from interpreter import Interpreter


@pytest.fixture
def setup_binary_file(tmp_path):
    binary_file = tmp_path / "test.bin"
    result_file = tmp_path / "test_result.json"
    return binary_file, result_file


def test_load(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x5B, 0x54, 0x03, 0x00, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:5")
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "    {\n        \"address\": 2,\n        \"value\": 426\n    }" in f.read()


def test_read(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x63, 0xDA, 0x23, 0x00, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:300")
    interpreter.registers[13] = 1
    interpreter.registers[287] = 100
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "    {\n        \"address\": 3,\n        \"value\": 100\n    }" in f.read()


def test_write(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x8B, 0x70, 0x02, 0x00, 0x00, 0x00, 0x00]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:320")
    interpreter.registers[4] = 42
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "    {\n        \"address\": 312,\n        \"value\": 42\n    }" in f.read()


def test_sqrt(setup_binary_file):
    binary_file, result_file = setup_binary_file
    binary_file.write_bytes(bytes([0x73, 0x53, 0x07, 0x00, 0x00, 0x86, 0x01]))
    interpreter = Interpreter(str(binary_file), str(result_file), "0:1000")
    interpreter.registers[11] = 123
    interpreter.registers[513] = 426
    interpreter.interpret()
    with open(result_file, "r", encoding="utf-8") as f:
        assert "    {\n        \"address\": 937,\n        \"value\": 426\n    }" in f.read()