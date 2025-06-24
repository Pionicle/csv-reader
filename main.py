import argparse
import csv

from tabulate import tabulate


def convert_type(value: str):
    """
    Converts a string to an integer or float.
    """
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
    type_param = type(table[0][param])
    value_param = type_param(value_param)

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
    pass


def print_table(table: list[list[str]]) -> None:
    """
    Prints a table in a formatted way.
    """
    print(tabulate(table, headers="keys", tablefmt="psql"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--where", type=str, required=False)
    parser.add_argument("--aggregate", type=str, required=False)
    args = parser.parse_args()
    table = get_table(args.file)
    if args.where:
        table = where_table(table, args.where)
    if args.aggregate:
        table = aggregate_table(table, args.aggregate)
    print_table(table)


if __name__ == "__main__":
    main()
