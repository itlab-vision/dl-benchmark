from .table import Table  # pylint: disable=E0402


class BenchmarkConfigTable(Table):
    def __init__(self, parent):
        super().__init__(parent)
        self._count_col = 15
        self._count_row = 150
        self.__headers = ['Model', 'Dataset', 'InferenceFramework', 'BatchSize', 'Device', 'IterationCount',
                          'TestTimeLimit', 'Mode', 'Extension', 'AsyncRequestCount', 'ThreadCount', 'StreamCount',
                          'ChannelSwap', 'Mean', 'InputScale']
        self.setColumnCount(self._count_col)
        self.setRowCount(self._count_row)
        self.setHorizontalHeaderLabels(self.__headers)
        self._resize_columns()
        self.clear()

    def update(self, tests):
        self.clear()
        count = 0
        for i in range(len(tests)):
            self.setItem(i, 0, self._create_cell(tests[i].model))
            self.setItem(i, 1, self._create_cell(tests[i].dataset))
            self.setItem(i, 2, self._create_cell(tests[i].framework))
            self.setItem(i, 3, self._create_cell(tests[i].batch_size))
            self.setItem(i, 4, self._create_cell(tests[i].device))
            self.setItem(i, 5, self._create_cell(tests[i].iter_count))
            self.setItem(i, 6, self._create_cell(tests[i].test_time_limit))
            if tests[i].mode:
                self.setItem(i, 7, self._create_cell(tests[i].mode))
            if tests[i].extension:
                self.setItem(i, 8, self._create_cell(tests[i].extension))
            if tests[i].async_req_count:
                self.setItem(i, 9, self._create_cell(tests[i].async_req_count))
            if tests[i].thread_count:
                self.setItem(i, 10, self._create_cell(tests[i].thread_count))
            if tests[i].stream_count:
                self.setItem(i, 11, self._create_cell(tests[i].stream_count))
            if tests[i].channel_swap:
                self.setItem(i, 12, self._create_cell(tests[i].channel_swap))
            if tests[i].mean:
                self.setItem(i, 13, self._create_cell(tests[i].mean))
            if tests[i].input_scale:
                self.setItem(i, 14, self._create_cell(tests[i].input_scale))
            count += 1
