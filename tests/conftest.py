import pytest

from dewar import dewar


@pytest.fixture(autouse=True, scope='function')
def site_cleanup():
    yield
    if hasattr(dewar, '_site_instances'):
        del dewar._site_instances
