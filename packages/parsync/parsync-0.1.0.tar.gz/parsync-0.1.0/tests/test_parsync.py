import os
import tempfile
import re

import pytest
from parsync import enumerate_copies


@pytest.fixture
def src_dir():
    with tempfile.TemporaryDirectory() as d:
        os.mkdir(f"{d}/a")
        os.mkdir(f"{d}/b")
        os.mkdir(f"{d}/c")
        open(f'{d}/a/1.md', 'a').close()
        open(f'{d}/a/2.md', 'a').close()
        open(f'{d}/a/3.md', 'a').close()
        open(f'{d}/a/1.txt', 'a').close()
        open(f'{d}/a/2.txt', 'a').close()
        open(f'{d}/a/3.txt', 'a').close()
        yield d


@pytest.fixture
def dst_dir():
    with tempfile.TemporaryDirectory() as d:
        yield d


def test_basic(src_dir, dst_dir):
    expected = {
        (src_dir + "/a/1.md", dst_dir + "/a/1.md"),
        (src_dir + "/a/2.md", dst_dir + "/a/2.md"),
        (src_dir + "/a/3.md", dst_dir + "/a/3.md"),
        (src_dir + "/a/1.txt", dst_dir + "/a/1.txt"),
        (src_dir + "/a/2.txt", dst_dir + "/a/2.txt"),
        (src_dir + "/a/3.txt", dst_dir + "/a/3.txt"),
    }

    actual = set(enumerate_copies(src_dir + '/a', dst_dir))

    assert expected == actual

def test_filters(src_dir, dst_dir):
    expected = {
        (src_dir + "/a/1.md", dst_dir + "/a/1.md"),
        (src_dir + "/a/2.md", dst_dir + "/a/2.md"),
        (src_dir + "/a/3.md", dst_dir + "/a/3.md"),
    }

    filters = [re.compile("\.md$")]
    actual = set(enumerate_copies(src_dir + '/a', dst_dir, filters))

    expected = {
        (src_dir + "/a/1.md", dst_dir + "/a/1.md"),
        (src_dir + "/a/2.md", dst_dir + "/a/2.md"),
        (src_dir + "/a/3.md", dst_dir + "/a/3.md"),
    }

    excludes = [re.compile("\.txt$")]
    actual = set(enumerate_copies(src_dir + '/a', dst_dir, excludes=excludes))

    assert expected == actual
