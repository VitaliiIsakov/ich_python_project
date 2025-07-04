from tabulate import tabulate


def print_table(data, headers):
    """
    Prints tabular data in a formatted grid using the tabulate library.

    Args:
        data (list): A list of rows, where each row is a list of values.
        headers (list): A list of column headers.
    """
    if not data:
        print("No data available.")
        return

    print(tabulate(data, headers=headers, tablefmt="grid"))