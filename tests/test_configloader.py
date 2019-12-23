from .mockers import EXPECTED_CONFIG


def test_set_config():
    from sheetload.config import ConfigLoader

    config = ConfigLoader(test=True)
    config.sheet_config

    assert ConfigLoader(test=True).sheet_config == EXPECTED_CONFIG
