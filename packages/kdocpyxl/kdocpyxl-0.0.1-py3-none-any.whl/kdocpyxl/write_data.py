from kdocpyxl.wps_cloud_excel import WpsCloudExcel

class WpsCloudExcelWriter(WpsCloudExcel):

    def write_cell(self, sheet_name, row, column, value):
        """
        写入数据至单元格中

        参数:
            sheet_name (str): 表格名称
            row (int): 行号
            column (int): 列号
            value (str): 要写入的值

        返回:
            dict: 包含执行结果的字典
        """
        params = {
            "sheet_name": sheet_name,
            "row": row,
            "column": column,
            "value": value
        }
        return self.execute_airscript(params)

    def write_row(self, sheet_name, row_index, values):
        """
        写入指定行的数据

        参数:
            sheet_name (str): 表格名称
            row_index (int): 行号
            values (list): 要写入的值列表

        返回:
            dict: 包含执行结果的字典
        """
        params = {
            "sheet_name": sheet_name,
            "row": row_index,
            "values": values
        }
        return self.execute_airscript(params)

    def write_column(self, sheet_name, column_index, values):
        """
        写入指定列的数据

        参数:
            sheet_name (str): 表格名称
            column_index (int): 列号
            values (list): 要写入的值列表

        返回:
            dict: 包含执行结果的字典
        """
        params = {
            "sheet_name": sheet_name,
            "column": column_index,
            "values": values
        }
        return self.execute_airscript(params)
