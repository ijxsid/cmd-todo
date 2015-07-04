
"""Example of a Table, printed by GoodTable

    +===========+================+=============+
    | Todo name | Task           | Bounty      |
    +===========+================+=============+
    | todo396   | Loundry        | 95          |
    +-----------+----------------+-------------+
    | todo789   | Cleaning       | 189         |
    +-----------+----------------+-------------+
    | timmy10   | Write Docs     | 90          |
    +-----------+----------------+-------------+

"""
class Goodtable():

    def __init__(self, cols, label=None, headers=[], max_width=80):
        """
        inputs ->
            label - the name at the top of the table.
            cols - the data about widths of the colums.
            cols ex = [20, 20, 20, 20] should add up to max_width.
            headers - the top level Headings
            max_width - the maximum width of the terminal.
        """
        self._label = label
        self._cols = self._get_printable_width(cols)
        self._headers = headers
        self._max_width = max_width
        self._rows = []

    def _get_printable_width(self, cols):
        result = []
        max_ix = cols.index(max(cols))
        for i in range(len(cols)):
            col_width = cols[i] - 1
            if i == max_ix:
                col_width -= 1
            result.append(col_width)
        return result

    def add_row(self, row_data):
        """
        row_data should be an array of strings.
        """
        assert len(row_data) == len(self._cols), 'This row has more/less columns than expected. ' + str(len(row_data)) + '!=' + str(len(self._cols))
        self._rows.append(row_data)

    def print_table(self):
        if self._label is not None:
            self._print_label()
        self._print_header()
        for row in self._rows:
            self._print_row(row)
    def _print_label(self):
        label_string_1 =  "|{data:^{width}}|".format(data=self._label, width=(self._max_width/2))
        label_string_center1 = "{data:^{width}}".format(data=label_string_1, width=self._max_width)

        label_border_bottom = "+{data:^{width}}+".format(data='='*(self._max_width/2), width=(self._max_width/2))
        label_border_center = "{data:^{width}}".format(data=label_border_bottom, width=self._max_width)

        print label_border_center + "\n" +label_string_center1 + "\n" + label_border_center
    def _print_header(self):
        if len(self._headers) > 0:
            self._print_border()
            self._print_data(self._headers)
        self._print_border()

    def _print_row(self,row):
        self._print_data(row)
        self._print_border(style='-')

    def _print_border(self, style='='):
        result_string = ''
        for i in range(len(self._cols)):
            col = self._cols[i]
            result_string += '+' + (style*(col))
        result_string += "+"
        print result_string

    def _print_data(self, data):
        result = ''
        for i in range(len(data)):
            header = data[i]
            width = self._cols[i]
            if len(header) > width - 1:
                header = header[:width-2] + ">"
            result += "| {data:{width}}".format(data=header, width=width-1)
        result += "|"
        print result
