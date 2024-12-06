import requests

class WpsCloudExcel:
    def __init__(self, webhook_url, api_token):
        self.webhook_url = webhook_url
        self.api_token = api_token
        self.headers = {
        'Content-Type': 'application/json',
        'AirScript-Token': self.api_token }

    def execute_airscript(self, script_params):
        """
        执行 AirScript 并返回结果
        """
        payload = {
            'Context': {
                'argv': script_params
            }
        }

        response = requests.post(self.webhook_url, headers=self.headers, json=payload)

        if response.status_code == 200:
            return response.json()['data']['result']['message']
        else:
            return {"status": "error", "message": f"HTTP Error: {response.status_code}"}