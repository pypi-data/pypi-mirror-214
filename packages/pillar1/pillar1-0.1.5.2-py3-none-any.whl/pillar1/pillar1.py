import json
import boto3
import ipywidgets as widgets
from IPython.display import display

MODEL_META = {
    'falcon-7b-instruct': {
        'endpoint_name': 'huggingface-pytorch-tgi-inference-2023-06-19-20-08-19-092',
    }
}


class Model:
    def __init__(self, user_name: str = '', password: str = '', model_name: str = 'falcon-7b-instruct', max_new_tokens: int = 200):
        self.model_name = model_name
        self.prompt = None
        self.response = None
        self.max_new_tokens = max_new_tokens

        self.endpoint_name = MODEL_META[self.model_name]['endpoint_name']
        self.client = boto3.client(
            'sagemaker-runtime',
            aws_access_key_id=user_name,
            aws_secret_access_key=password,
            region_name='us-west-2'
        )

    def query(self, prompt):
        def submit_request(prompt):
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

            self.response = json.loads(response['Body'].read())[0]['generated_text']

        if prompt:
            self.prompt = prompt
            submit_request(self.prompt)
        else:
            textarea_bg = widgets.Textarea(description='What SQL are you looking for:', layout=widgets.Layout(width='80%', height='200px'), style={'description_width': 'initial'})
            input_text = widgets.Text(description='What SQL are you looking for:', layout=widgets.Layout(width='80%'), style={'description_width': 'initial'})
            button = widgets.Button(description='Submit')
            display(textarea_bg)
            display(input_text)
            display(button)

            # Define button click event
            def submit_button():
                prompt = f"Given this background \"{textarea_bg.value}\", answer this question \"{input_text.value}\""
                submit_request(prompt)

            # Bind button click event to function
            button.on_click(submit_request)
