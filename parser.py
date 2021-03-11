import csv
import dateutil.parser
import json
import logging

from constants import COLUMN_NAMES, COLUMN_SYNONYMS, COLUMNS_TO_CONCAT


def unify_value(col_name: str, value: str) -> str:
    if col_name == 'date':
        value = dateutil.parser.parse(value).strftime('%b %-d% %Y')
    return value


def build_data(csv_reader: csv.reader) -> list:
    data = []
    column_names = []
    for row in csv_reader:
        data_row = []

        # Get headers
        if not column_names:
            column_names = row
            continue

        for column_name in COLUMN_NAMES:
            try:
                row_index = column_names.index(column_name)
            except ValueError:
                # Column not found, search in synonyms and in columns to be concatenated
                synonyms = COLUMN_SYNONYMS[column_name]
                cols_to_concat = COLUMNS_TO_CONCAT[column_name] if COLUMNS_TO_CONCAT.get(column_name) else []
                matched_columns = list(set(column_names).intersection(synonyms))\
                    or list(set(column_names).intersection(cols_to_concat))

                if len(matched_columns) == 1:
                    row_index = column_names.index(matched_columns[0])
                    value = row[row_index]
                elif len(matched_columns) > 1:
                    row_indexes = [column_names.index(elm) for elm in set(cols_to_concat).intersection(matched_columns)]
                    value = '.'.join(row[r_idx] for r_idx in row_indexes)
                else:
                    raise ValueError(f'Invalid column name: {column_name}')
            else:
                value = row[row_index]

            data_row.append(unify_value(column_name, value))

        data.append(data_row)
    return data


def parse():
    logging.debug('Read for file paths')
    with open('file_paths.json', 'r') as f:
        json_data = json.loads(f.read())
        file_paths = json_data.get('paths') if type(json_data.get('paths')) is list else None
        output = json_data['output_path']

    if not file_paths:
        raise ValueError('Invalid file paths provided')

    for idx, file_path in enumerate(file_paths):
        logging.debug(f'Parsing csv: {file_path}')
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            data = build_data(reader)

        # Add headers to first parsed file
        if not idx:
            data.insert(0, COLUMN_NAMES)
            write_mode = 'w'
        else:
            write_mode = 'a'

        # Write parsed data
        logging.debug(f'Writing parsed data for: {file_path}')
        with open(output, write_mode) as f:
            writer = csv.writer(f)
            for d in data:
                writer.writerow(d)


if __name__ == '__main__':
    parse()
