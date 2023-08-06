import requests, json, boto3, io, logging, sys, os
class Agent:
    def __init__(self, api_id, mock):
        self.cfg_path = os.path.join(sys.path[0],'.dalphacfg')
        self.__load_config(self.cfg_path)
        self.token = os.environ['TOKEN']
        self.base_url = os.environ['BASE_URL']
        self.evaluate_url = os.path.join(self.base_url, f"inferences/{api_id}/evaluate")
        self.api_id = api_id
        self.mock = mock
        self.s3 = boto3.client('s3')
        
        
    def __load_config(self,file_path):
        if not os.path.isfile(file_path):
            logging.warning(f"{file_path} 파일을 찾을 수 없습니다.")
            return
        
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        for line in lines:
            line = line.strip()
            if line and not line.startswith("#"):
                key, value = line.split("=")
                os.environ[key] = value

    def poll(self, mock=True):
        if mock:
            return self.mock
        
        url = f"{self.evaluate_url}/poll"

        headers = {
        'token': self.token
        }
        response = requests.request("GET", url, headers=headers)
        if response.status_code == 422:
            return None
        elif response.status_code != 200:
            raise Exception(f'error from poll / response status_code {response.status_code}')
        
        return response.json()

    def validate(self, evaluate_id, output, mock=True):
        if mock:
            logging.debug(output)
            return
        payload = json.dumps({
            "id": evaluate_id,
            "json": output
        })

        url = f"{self.evaluate_url}/validate"

        headers = {
            'token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f'error from validate / response status_code {response.status_code}')
        
    def validate_error(self, evaluate_id, output, mock=True):
        if mock:
            logging.debug(output)
            return
        payload = json.dumps({
            "id": evaluate_id,
            "error": output
        })

        url = f"{self.evaluate_url}/error"

        headers = {
            'token': self.token,
            'Content-Type': 'application/json'
        }

        response = requests.request("PUT", url, headers=headers, data=payload)
        if response.status_code != 200:
            raise Exception(f'error from validate / response status_code {response.status_code}')
        
    def download_from_url(self, url):
        r = requests.get(url, stream=True)
        if r.status_code != 200:
            raise Exception(f"can't download from url")
        else:
            return io.BytesIO(r.content)
            # return Image.open(io.BytesIO(r.content)).convert('RGB')

    def download_from_s3(self, bucket, key, download_path):
        try:
            self.s3.download_file(bucket, key, download_path)
        except Exception as e:
            logging.error(f"failed to download from s3\n{e}")

    def upload_s3(self, upload_path, bucket, key):
        try:
            self.s3.upload_file(upload_path, bucket, key)
        except Exception as e:
            logging.error(f"failed to upload s3\n{e}")

    def stop_instance(self):
        try:
            res = requests.request("GET", 'http://169.254.169.254/latest/meta-data/instance-id')
            if res.status_code != 200:
                raise Exception("get instance-id failed!")
            instance_id = res.text[2:]
            
            url = f"https://api.dalpha.so/instances/{instance_id}/stop/@sdk"

            headers = {
                'token': self.token,
                'Content-Type': 'application/json'
            }

            response = requests.request("PUT", url, headers=headers)
            if response.status_code != 200:
                raise Exception(f'error from stop_instance / response status_code {response.status_code}')

        except Exception as e:
            raise Exception(f"error from stop_instance\n{e}")