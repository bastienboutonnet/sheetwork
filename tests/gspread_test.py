import os


def test_importing_gspread():
    # import gspread
    print(os.environ["APPDATA"])


def test_importing_with_get():
    print(os.environ)
    print(os.getenv("APPDATA"))
