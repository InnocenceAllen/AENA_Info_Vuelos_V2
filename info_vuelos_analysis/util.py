import csv


def create_csv(filename, field_names, delimiter):
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f, delimiter=delimiter)
        writer.writerow(field_names)


def save_to_csv(filename, data):
    with open(filename, 'a', newline='', encoding='utf8') as f:
        writer = csv.writer(f)
        writer.writerows(map(lambda x: [repr(x)], data))
