import pprint


def extract_lists(data):
    output = []
    for item in data:
        item = item.strip()
        if not item:
            continue
        if item == "TOTAL":
            break
        if len(item) >= 1 and item[0] in "0123456789" and item[-1] in "my":
            yield output
            output = []
        output.append(item)


def contains_number(item):
    return any(char.isdigit() for char in item)


def filter_non_numbers(row):
    return tuple([item if contains_number(item) else "" for item in row])


def truncate(table):
    header = next(table)
    header = [item for item in header if not contains_number(item)]
    yield header
    size = len(header)
    for row in table:
        yield filter_non_numbers((row + [""] * size)[:size])


def main(data):
    table = truncate(extract_lists(data))
    print(", ".join(f'"{item}"' for item in next(table)))
    for row in table:
        print(row)


if __name__ == "__main__":
    main(
        [
            "COP",
            "\t\t\t",
            "Basis",
            "Notl",
            "dv01",
            "6m",
            "9m",
            "1y",
            "18m",
            "2y",
            "3y",
            "15.6",
            "mm",
            "4.6",
            "4y",
            "5y",
            "10",
            "mm",
            "4.6",
            "6y",
            "7y",
            "8y",
            "9y",
            "10y",
            "20y",
            "TOTAL",
            "\t\t9.2",
        ]
    )
