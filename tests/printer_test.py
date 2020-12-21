import pytest


@pytest.mark.parametrize("use_colours", [True, False])
def test_colour(use_colours):
    from sheetwork.core.ui.printer import colour, CL_RED

    plain_msg = "dummy test message"
    red_message = "\x1b[31mdummy test message\x1b[0m"

    ret_msg = colour(message=plain_msg, colour=CL_RED, use_colours=use_colours)

    if use_colours:
        assert ret_msg == red_message
    else:
        assert ret_msg == plain_msg
