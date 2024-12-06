import requests
from kdocpyxl.utils.wps_cloud_excel import WpsCloudExcel

class WpsCloudExcelWriter(WpsCloudExcel):
    def write_excel(self, file_id, sheet_name, data):
        """
        写入数据到 Excel 文件
        :param file_id: 文件 ID
        :param sheet_name: 工作表名称
        :param data: 要写入的数据
        :return: 写入结果
        """
        script_params = [file_id, sheet_name, data]
        result = self.execute_airscript(script_params)
        return result