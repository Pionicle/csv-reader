import argparse

from tabulate import tabulate

from table_operations import (
    get_table,
    where_table,
    aggregate_table,
    order_by_table,
)


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
