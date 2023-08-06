def create_html_table(records: list[dict[str, str]]) -> str:
    """output a str of html table for the list of records"""
    if not records:
        return ""

    # get headers from the keys of the first dictionary in the records
    headers = records[0].keys()

    html_str = '<table>\n'

    # create header row
    html_str += '<tr>\n'
    for header in headers:
        html_str += f'<th>{header}</th>\n'
    html_str += '</tr>\n'

    # create data rows
    for record in records:
        html_str += '<tr>\n'
        for header in headers:
            html_str += f'<td>{record[header]}</td>\n'
        html_str += '</tr>\n'

    html_str += '</table>'
    return html_str
