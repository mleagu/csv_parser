import csv
import dateutil.parser
import json
import logging

from constants import COLUMN_NAMES, COLUMN_SYNONYMS, COLUMNS_TO_CONCAT


def get_cols_map(column_names: list) -> dict:
    # Create relation between column headers and column index from current file
    columns_mapping = {}

    for idx, original_column in enumerate(column_names):
        for synonym in COLUMN_SYNONYMS:
            if original_column in COLUMN_SYNONYMS[synonym]:
                columns_mapping.update({synonym: idx})
                break
        else:
            for col_to_concat, values in COLUMNS_TO_CONCAT.items():
                # Values is a list of tuples
                for val in values:
                    if original_column in val:
                        columns_mapping.update({col_to_concat: [column_names.index(v) for v in val]})

    return columns_mapping


def build_data(csv_reader: csv.reader, col_mapping: dict) -> list:
    data = []
    for row in csv_reader:
        data_row = []
        for column_name in COLUMN_NAMES:
            row_index = col_mapping[column_name]
            if type(row_index) is list:
                data_row.append('.'.join(row[r_idx] for r_idx in row_index))
            else:
                # Unify date format
                if column_name == 'date':
                    row[row_index] = dateutil.parser.parse(row[row_index]).strftime('%b %-d% %Y')
                data_row.append(row[row_index])
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

    # Write headers for unified csv
    with open(output, 'w') as f:
        writer = csv.writer(f)
        writer.writerow(COLUMN_NAMES)

    for file_path in file_paths:
        logging.debug(f'Parsing csv: {file_path}')
        with open(file_path, 'r') as f:
            reader = csv.reader(f)
            # Get headers
            column_names = []
            for row in reader:
                column_names = row
                break

            mapping = get_cols_map(column_names)
            data = build_data(reader, mapping)

        # Write parsed data
        logging.debug(f'Writing parsed data for: {file_path}')
        with open(output, 'a') as f:
            writer = csv.writer(f)
            for d in data:
                writer.writerow(d)


if __name__ == '__main__':
    parse()
