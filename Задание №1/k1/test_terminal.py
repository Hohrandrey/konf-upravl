import pytest
from terminal import MyTerminal
from zipfile import ZipFile
from window_mode import Window


@pytest.fixture
def terminal():
    start_path = 'test.zip'
    user_name = 'Andrew'
    comp_name = 'Computer'
    zip_path = 'test.zip'
    t = MyTerminal(user_name, comp_name, zip_path, start_path, ZipFile(start_path, 'a'))
    return t


@pytest.fixture
def empty_terminal():
    return MyTerminal(None)


def test_init_1(terminal):
    assert terminal.window is None


def test_init_2(terminal):
    assert terminal.fs is not None


def test_attach_1(terminal):
    assert terminal.window is None


def test_attach_2(terminal):
    terminal.attach(Window(terminal))
    assert terminal.window is not None


def test_cd_1(terminal):
    assert terminal.cd([]) == ''


def test_cd_2(terminal):
    assert terminal.cd(['IloveKIS']) == 'test/IloveKIS/'


def test_ls_1(terminal):
    assert all(i in terminal.ls([]) for i in "\nIloveKIS\n[eq.bmp\nqwerty.docx\nПрезентация.pptx")


def test_ls_2(terminal):
    terminal.cur_d = terminal.cd(['IloveKIS'])
    assert terminal.ls([]) == "\ntopsecret\n1.txt\nЯЛКВМОМ.txt"


def test_ls_3(terminal):
    assert all(i in terminal.ls(['user']) for i in "me secrets.txt top_secret.txt".split())


def test_uptime_1(terminal):
    assert terminal.uptime() == "up 1 min"


def test_find_1(terminal):
    assert terminal.find(['.']) == "up 1 min"


def test_find_2(terminal):
    assert terminal.find(['1.txt']) == "IloveKIS/1.txt"
