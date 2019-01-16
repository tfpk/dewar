import pytest
from dewar import dewar

from pathlib import Path
import shutil

FILE_DIR = Path(__file__).absolute().parent


@pytest.fixture
def site():
    s = dewar.Site()
    return s


@pytest.fixture
def full_site(tmpdir):
    SITE_PATH = 'site'
    site_path = FILE_DIR / 'full_site'
    s = dewar.Site(path=site_path)
    return s
