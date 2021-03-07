COLUMN_NAMES = ['date', 'transaction', 'amount', 'from', 'to']

COLUMN_SYNONYMS = {
    'date': ['date', 'timestamp', 'date_readable'],
    'transaction': ['transaction', 'type'],
    'amount': ['amounts', 'amount', 'euro,cents'],
    'from': ['from'],
    'to': ['to']
}

COLUMNS_TO_CONCAT = {
    'amount': [('euro', 'cents')]  # list of tuples - for multiple options, ex. different currency
}
