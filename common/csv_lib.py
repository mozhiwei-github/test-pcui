import csv

"""CSV文件读写工具类"""


class CsvLib(object):
    def __init__(self, file_path, field_names=None, delimiter=',', quotechar='"'):
        """
        构造函数
        @param file_path: 文件路径
        @param field_names: csv 的 header 字段
        @param delimiter: 用于分隔字段的单字符
        @param quotechar: 用于包住含有特殊字符字段的单字符
        """
        self.file_path = file_path
        self.field_names = field_names
        self.delimiter = delimiter
        self.quotechar = quotechar
        self.csv_file = None
        self.reader = None
        self.writer = None

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def close(self):
        self.close_csv_file()
        self.reader = None
        self.writer = None

    def open_csv_file(self, mode='r', newline='', encoding='utf-8-sig'):
        """
        打开csv文件
        @param mode: 打开文件的模式
        @param newline: 如果 csvfile 是文件对象，则打开它时应使用 newline=''
        @param encoding: 文件编码
        @return:
        """
        self.close_csv_file()

        self.csv_file = open(self.file_path, mode=mode, newline=newline, encoding=encoding)

    def close_csv_file(self):
        """关闭csv文件"""
        if self.csv_file:
            self.csv_file.close()
            self.csv_file = None

    def get_reader(self):
        """获取csv reader对象"""
        self.open_csv_file()

        if self.field_names:
            self.reader = csv.DictReader(self.csv_file, fieldnames=self.field_names, delimiter=self.delimiter,
                                         quotechar=self.quotechar)
        else:
            self.reader = csv.reader(self.csv_file, delimiter=self.delimiter, quotechar=self.quotechar)

        return self.reader

    def get_writer(self):
        """获取csv writer对象"""
        self.open_csv_file(mode='w')

        if self.field_names:
            self.writer = csv.DictWriter(self.csv_file, self.field_names, delimiter=self.delimiter,
                                         quotechar=self.quotechar, quoting=csv.QUOTE_MINIMAL)
        else:
            self.writer = csv.writer(self.csv_file, delimiter=self.delimiter, quotechar=self.quotechar,
                                     quoting=csv.QUOTE_MINIMAL)
        if self.field_names:
            self.writer.writeheader()

        return self.writer

    def read_rows(self, field_names=None):
        """
        读取每行数据
        @param field_names: 获取指定列的数据，缺省时返回所有列的数据
        @return:
        """
        if not self.reader:
            self.get_reader()

        if not self.field_names:
            return self.reader

        if field_names is None:
            field_names = self.field_names

        result = {}
        for row in self.reader:
            for field_name in field_names:
                if field_name not in result:
                    result[field_name] = []

                result[field_name].append(row.get(field_name))

        return result

    def write_row(self, data, flush=True):
        if not self.writer:
            self.get_writer()

        self.writer.writerow(data)

        if flush:
            self.csv_file.flush()


if __name__ == '__main__':
    file_path = "test.csv"
    field_names = ["A", "B", "C"]

    # 写入不带header的csv文件
    with CsvLib(file_path) as csv_lib:
        csv_lib.write_row(["1", "2", "3"])
        csv_lib.write_row(["q"])
        csv_lib.write_row(["a"] + ["s"] + ["d"])

    # 读取不带header的csv文件
    with CsvLib(file_path) as csv_lib:
        for row in csv_lib.read_rows():
            print(row)

    # 写入带header的csv文件
    with CsvLib(file_path, field_names) as csv_lib:
        csv_lib.write_row({
            "A": 1,
            "B": 2,
            "C": 3,
        })
        csv_lib.write_row({
            "A": 'q',
        })
        csv_lib.write_row({
            "A": 'a',
            "B": 's',
            "C": 'd',
        })

    # 读取带header的csv文件
    with CsvLib(file_path, field_names) as csv_lib:
        print(csv_lib.read_rows())
        # print(csv_lib.read_rows(["B"]))
