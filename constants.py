COLUMN_NAMES = ['date', 'transaction', 'amount', 'from', 'to']

COLUMN_SYNONYMS = {
    'date': ['date', 'timestamp', 'date_readable'],
    'transaction': ['transaction', 'type'],
    'amount': ['amounts', 'amount'],
    'from': ['from'],
    'to': ['to']
}

COLUMNS_TO_CONCAT = {
    'amount': ['euro', 'cents']  # support multiple values, but it should keep order for concatenation
}
