import pytest
from assembler import Assembler


@pytest.fixture
def setup_files(tmp_path):
    asm_file = tmp_path / "test.asm"
    bin_file = tmp_path / "test.bin"
    log_file = tmp_path / "test_log.json"
    return asm_file, bin_file, log_file


def test_load(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("LOAD 27 2 426\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x5B, 0x54, 0x03, 0x00, 0x00, 0x00, 0x00])


def test_read(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("READ 3 3 13 286\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x63, 0xDA, 0x23, 0x00, 0x00, 0x00, 0x00])


def test_write(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("WRITE 11 4 312\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x8B, 0x70, 0x02, 0x00, 0x00, 0x00, 0x00])


def test_sqrt(setup_files):
    asm_file, bin_file, log_file = setup_files
    asm_file.write_text("SQRT 19 11 937 390\n")
    assembler = Assembler(str(asm_file), str(bin_file), str(log_file))
    assembler.assemble()
    with open(bin_file, "rb") as f:
        assert f.read() == bytes([0x73, 0x53, 0x07, 0x00, 0x00, 0x86, 0x01])