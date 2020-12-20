def test_consume_cli_arguments():
    from sheetwork.core.flags import FlagParser
    from sheetwork.core.main import parser

    flag_parser = FlagParser(parser)
    print("AKJKSDJHSKDJHS")
    flag_parser.consume_cli_arguments(["init", "--project-name", "sheetwork_test"])
    assert flag_parser.task == "init"
    assert flag_parser.project_name == "sheetwork_test"
    assert flag_parser.force_credentials is False
