import yaml


class ConfigLoader:
    def __init__(self, sheet_name):
        self.sheet_name = sheet_name
        self.config = None
        self.sheet_config = None
        self.load_yml()

    def load_yml(self):
        with open("sheets.yml", "r") as stream:
            self.config = yaml.safe_load(stream)

    def get_sheet_config(self):
        sheets = self.config["sheets"]
        sheet_config = [sheet for sheet in sheets if sheet["sheet_name"] == "test_sheet"]
        if len(sheet_config) > 1:
            raise AttributeError(
                f"Found more than one config for {self.sheet_name}. Check your sheets.yml file."
            )
        self.sheet_config = sheet_config[0]
        return self.sheet_config

    def generate_column_dict(self):
        if self.sheet_config:
            columns = self.sheet_config.get("columns")
            column_dict = dict()
            for column in columns:
                column_dict.update(dict({column.get("name"): column.get("type")}))
