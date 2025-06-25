import csv
from typing import Callable


def check_arg(slpit_signs: list[str], values: list[str] = None):
    """
    Checks the user arguments for a function.
    """

    def wrapper(func: Callable):
        def inner(table: list[dict[str]], arg: str):
            for split_sign in slpit_signs:
                if split_sign in arg:
                    param, value = arg.split(split_sign)
                    columns = list(table[0].keys())
                    if param not in columns:
                        raise Exception(f"{param} is not one of {columns}")
                    if values is not None and value not in values:
                        raise Exception(f"{value} is not one of {values}")
                    return func(table, arg)
            raise Exception(f"{arg} is not one of {slpit_signs}")

        return inner

    return wrapper


def convert_type(value: str) -> int | float | bool | str | None:
    """
    Converts a string to an integer or float.
    """
    if value in ["None", ""]:
        return None
    if value in ["True", "true"]:
        return True
    if value in ["False", "false"]:
        return False
    try:
        return int(value)
    except ValueError:
        try:
            return float(value)
        except ValueError:
            return value


def get_table(file: str) -> list[dict[str]]:
    """
    Reads a CSV file and returns a list of dictionaries.
    """
    with open(file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        table = []
        for line in reader:
            row = {}
            for key, value in line.items():
                row[key] = convert_type(value)
            table.append(row)
        return table


@check_arg([">", "<", "="])
def where_table(table: list[dict[str]], where: str) -> list[dict[str]]:
    """
    Filters a table based on the given where clause.
    """
    sign = ""
    if ">" in where:
        sign = ">"
    elif "<" in where:
        sign = "<"
    elif "=" in where:
        sign = "="

    param, value_param = where.split(sign)
    value_param = convert_type(value_param)

    new_table = []
    for row in table:
        match sign:
            case ">":
                if row[param] > value_param:
                    new_table.append(row)
            case "<":
                if row[param] < value_param:
                    new_table.append(row)
            case "=":
                if row[param] == value_param:
                    new_table.append(row)
    return new_table


@check_arg(["="], ["avg", "min", "max"])
def aggregate_table(table: list[dict[str]], aggregate: str) -> list[dict[str]]:
    """
    Aggregates a table based on the given aggregate function.
    """
    param, value_param = aggregate.split("=")

    result_dict = {}
    result = 0
    first = True
    for row in table:
        match value_param:
            case "avg":
                result += row[param]
            case "min":
                if first:
                    result = row[param]
                    first = False
                if row[param] < result:
                    result = row[param]
            case "max":
                if first:
                    result = row[param]
                    first = False
                if row[param] > result:
                    result = row[param]
    else:
        match value_param:
            case "avg":
                result_dict[value_param] = result / len(table)
            case "min":
                result_dict[value_param] = result
            case "max":
                result_dict[value_param] = result
    return [result_dict]


@check_arg(["="], ["asc", "desc"])
def order_by_table(table: list[dict[str]], order: str) -> list[dict[str]]:
    """
    Order the table by a specified parameter in ascending or descending order.
    """
    param, value_param = order.split("=")

    reverse = True if value_param == "desc" else False
    return sorted(table, key=lambda row: row[param], reverse=reverse)
