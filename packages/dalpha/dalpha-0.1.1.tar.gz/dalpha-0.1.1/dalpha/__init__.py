import requests, json, boto3, io, logging, sys, os
class Agent:
    def __init__(self, api_id, mock, use_sqs = False):
        self.cfg_path = os.path.join(sys.path[0],'.dalphacfg')
        self.__load_config(self.cfg_path)
        self.token = os.environ['TOKEN']
        self.base_url = os.environ['BASE_URL']
        self.queue_url = os.environ['QUEUE_URL']
        self.evaluate_url = os.path.join(self.base_url, f"inferences/{api_id}/evaluate")
        self.api_id = api_id
        self.mock = mock
        self.s3 = boto3.client('s3')
        self.sqs = boto3.client('sqs', region_name='ap-northeast-2')
        self.evaluates = {}
        self.use_sqs = use_sqs
        
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

    def poll(self, max_number_of_messages = 1, mock=True):
        if mock:
            return self.mock
        
        if self.use_sqs:
            response = self.sqs.receive_message(
                QueueUrl = self.queue_url,
                MaxNumberOfMessages = max_number_of_messages,  # 가져올 메시지의 최대 수 (1개 이상 설정 가능)
                VisibilityTimeout = 15,   # 메시지의 가시성 제한 시간 (초 단위)
                WaitTimeSeconds = 0       # 긴 폴링을 위한 대기 시간 (초 단위)
            )
            ret = []
            messages = response.get('Messages', [])
            for message in messages:
                message_body = message['Body']
                try:
                    # message_body를 딕셔너리로 변환
                    message_dict = json.loads(message_body)
                except json.JSONDecodeError:
                    logging.error("유효한 JSON 형식이 아닙니다.")
                self.evaluates[message_dict['id']] = message['ReceiptHandle']
                ret.append(message_dict)

            if len(ret) == 0:
                return None
            elif len(ret) == 1:
                return ret[0]
            else:
                return ret

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
        
        if self.use_sqs:
            try: 
                response = self.sqs.delete_message(
                    QueueUrl = self.queue_url,
                    ReceiptHandle = self.evaluates[evaluate_id]
                )
            except Exception as e:
                logging.error("error from sqs.delete_message\n",e)
                del self.evaluates[evaluate_id]
        

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
        
        if self.use_sqs:
            try: 
                response = self.sqs.delete_message(
                    QueueUrl = self.queue_url,
                    ReceiptHandle = self.evaluates[evaluate_id]
                )
            except Exception as e:
                logging.error("error from sqs.delete_message\n",e)
                del self.evaluates[evaluate_id]
        
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