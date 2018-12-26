import pytest
import dewar

@pytest.fixture
def site():
    return dewar.Site()
