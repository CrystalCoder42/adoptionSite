from species import *


class MissingInformation(Exception):
    def __init__(self, table, missing_columns=None):
        if not missing_columns:
            missing_columns = []
        super().__init__(f"Missing {', '.join(missing_columns)} for table {table}")


class InvalidTarget(Exception):
    def __init__(self, table, _id):
        super().__init__(f"Could not find id {_id} in {table}")


class CannotRemoveInfo(Exception):
    def __init__(self, _id, table, columns=None):
        if not columns:
            columns = []
        super().__init__(f"Could not remove info from {', '.join(columns)} for {_id} in {table}")


class DuplicateInformation(Exception):
    def __init__(self, column, value, table):
        super().__init__(f"A row with {column} = '{value}' in {table} already exists and this value must be unique.")
