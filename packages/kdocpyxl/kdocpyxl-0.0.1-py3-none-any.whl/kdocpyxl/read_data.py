from kdocpyxl.wps_cloud_excel import WpsCloudExcel

class WpsCloudExcelReader(WpsCloudExcel):

    def read_cell(self, sheet_name, row, column):
        """
        读取单个单元格的数据

        参数:
        sheet_name (str): 要读取的工作表名称
        row (int): 要读取的单元格所在的行号
        column (int): 要读取的单元格所在的列号

        返回:
        str: 读取到的单元格数据
        """
        params = {
            "sheet_name": sheet_name,
            "row": row,
            "column": column
        }
        return self.execute_airscript(params)

    def read_row(self, sheet_name, row_index):
        """
        读取指定工作表中的一行数据

        参数:
        sheet_name (str): 要读取的工作表名称
        row_index (int): 要读取的行号

        返回:
        list: 包含该行中所有单元格数据的列表
        """
        params = {
            "sheet_name": sheet_name,
            "row": row_index
        }
        return self.execute_airscript(params)

    def read_column(self, sheet_name, column_index):
        """
        读取指定工作表中的一列数据

        参数:
        sheet_name (str): 要读取的工作表名称
        column_index (int): 要读取的列号

        返回:
        list: 包含该列中所有单元格数据的列表
        """
        params = {
            "sheet_name": sheet_name,
            "column": column_index
        }
        return self.execute_airscript(params)

    def get_sheet_rows_and_columns(self, sheet_name):
        """
        获取指定 sheet 的有效行数和列数

        参数:
        sheet_name (str): 要获取行数和列数的 sheet 名称

        返回:
        dict: 包含指定 sheet 有效行数和列数的字典
        """
        params = {
            "sheet_name": sheet_name,
            "get_rows_and_columns": True
        }
        return self.execute_airscript(params)
