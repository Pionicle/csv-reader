import argparse
import csv
import traceback

from tabulate import tabulate


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
    except:
        try:
            return float(value)
        except:
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


def order_by_table(table: list[dict[str]], order: str) -> list[dict[str]]:
    """
    Order the table by a specified parameter in ascending or descending order.
    """
    param, value_param = order.split("=")

    reverse = False
    if value_param == "asc":
        reverse = False
    elif value_param == "desc":
        reverse = True
    else:
        raise ValueError(f"Invalid value parameter: {value_param}")
    return sorted(table, key=lambda row: row[param], reverse=reverse)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--where", type=str, required=False)
    parser.add_argument("--aggregate", type=str, required=False)
    parser.add_argument("--order-by", type=str, required=False)
    args = parser.parse_args()
    try:
        table = get_table(args.file)
        if args.where:
            table = where_table(table, args.where)
        if args.aggregate:
            table = aggregate_table(table, args.aggregate)
        if args.order_by:
            table = order_by_table(table, args.order_by)
        print_table = tabulate(table, headers="keys", tablefmt="psql")
        print(print_table)
    except Exception as ex:
        print(ex)


if __name__ == "__main__":
    main()
