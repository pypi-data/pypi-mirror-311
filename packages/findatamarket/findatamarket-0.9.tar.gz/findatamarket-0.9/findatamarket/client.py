import requests
import pandas as pd
import io
import zipfile

class Client:
    def __init__(self, API_TOKEN: str) -> None:
        if not API_TOKEN:
            raise ValueError("API token is required")
        self.api_token = API_TOKEN
        self.DOMAIN = 'https://ru.findata.market'

    

    def load_dataset(self, dataset_path: str) -> pd.DataFrame | None:
        try:
            username, dataset_slug = dataset_path.split('/')
            username = username.strip('@')
        except ValueError:
            raise ValueError("Invalid dataset path format. Use '@username/dataset_slug'")

        headers = {
            "Authorization": f"Bearer {self.api_token}"
        }

        url = f"{self.DOMAIN}/@{username}/datasets/{dataset_slug}/download"
        response = requests.get(url,headers=headers)

        if response.status_code == 200:
            if response.headers.get('Content-Type') == 'application/zip':
                zip_file = io.BytesIO(response.content)
                with zipfile.ZipFile(zip_file, 'r') as z:
                    for filename in z.namelist():
                        if filename.endswith('.csv'):
                            with z.open(filename) as f:
                                csv_data = pd.read_csv(f)
                                return csv_data
            else:
                raise ValueError("Unexpected file format. Expected a zip file.")
        elif response.status_code == 401:
            raise PermissionError("Unauthorized access. Please check your API token.")
        elif response.status_code == 404:
            raise FileNotFoundError(f"Dataset '@{username}/{dataset_slug}' not found.")
        else:
            raise RuntimeError(f"Unexpected error: {response.status_code} - {response.text}")

        return None
