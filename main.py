import argparse
import csv

from tabulate import tabulate


def get_table(file: str) -> tuple[list[str], list[str]]:
    with open(file, "r") as csv_file:
        reader = csv.DictReader(csv_file)
        headers = reader.fieldnames
        table = [list(row.values()) for row in reader]
        return headers, table


def aggregate_table(aggregate: str | None):
    pass


def where_table(where: str | None):
    pass


def print_table(headers: list[str], table: list[list[str]]) -> None:
    print(tabulate(table, headers, tablefmt="psql"))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--file", type=str, required=True)
    parser.add_argument("--where", type=str, required=False)
    parser.add_argument("--aggregate", type=str, required=False)
    args = parser.parse_args()
    headers, table = get_table(args.file)
    print_table(headers, table)


if __name__ == "__main__":
    main()
