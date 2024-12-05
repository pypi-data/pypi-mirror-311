import requests

API_URL = "https://nyxiannetwork.web.id/uploader/dorodoto.php"

class NyxianXD:
    def __init__(self, api_key):
        self.api_key = api_key
        self.headers = {"X-API-KEY": self.api_key}

    def get_user_info(self):
        response = requests.get(API_URL, headers=self.headers)
        if response.status_code == 200:
            data = response.json()
            if data.get("status") == "success":
                return data["user_data"]
            else:
                raise Exception(data.get("message", "Unknown error"))
        else:
            raise Exception(f"HTTP Error: {response.status_code}")

    def upload_file(self, file_path):
        with open(file_path, "rb") as file:
            response = requests.post(API_URL, headers=self.headers, files={"file": file})
            if response.status_code == 200:
                data = response.json()
                if data.get("status") == "success":
                    return data["url"]
                else:
                    raise Exception(data.get("message", "Unknown error"))
            else:
                raise Exception(f"HTTP Error: {response.status_code}")
