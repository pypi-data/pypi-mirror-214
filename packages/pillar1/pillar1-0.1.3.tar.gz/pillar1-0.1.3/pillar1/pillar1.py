import json
import boto3

MODEL_META = {
    'falcon-7b-instruct': {
        'endpoint_name': 'huggingface-pytorch-tgi-inference-2023-06-19-20-08-19-092',
    }
}


class Model:
    def __init__(self, user_name: str = '', password: str = '', model_name: str = 'falcon-7b-instruct', prompt: str = '', max_new_tokens: int = 200):
        self.model_name = model_name
        self.prompt = prompt
        self.max_new_tokens = max_new_tokens

        self.endpoint_name = MODEL_META[self.model_name]['endpoint_name']
        self.client = boto3.client(
            'sagemaker-runtime',
            aws_access_key_id=user_name,
            aws_secret_access_key=password,
            region_name='us-west-2'
        )

    def query(self, prompt):
        if prompt:
            self.prompt = prompt
        payload = {
            'inputs': prompt,
            "parameters": {
                "do_sample": True,
                "top_p": 0.7,
                "temperature": 0.7,
                "top_k": 50,
                "max_new_tokens": self.max_new_tokens,
                "repetition_penalty": 1.03,
                "stop": ["<|endoftext|>"]
            }
        }

        response = self.client.invoke_endpoint(
            EndpointName=self.endpoint_name,
            ContentType='application/json',
            Body=json.dumps(payload)
        )

        return json.loads(response['Body'].read())[0]['generated_text']
