import boto3    
import json

class BedrockInterface:
    def __init__(self, model_id):
        self.bedrock_client = boto3.client("bedrock-runtime")
        self.model_id = model_id
        self.accept = 'application/json'
        self.content_type = 'application/json'

    def generate_response(self, prompt, temperature=0.1, top_p=0.9):
        body = json.dumps({
            "prompt": prompt,
            "temperature": temperature,
            "top_p": top_p,
        })

        response = self.bedrock_client.invoke_model(body=body, modelId=self.model_id, accept=self.accept, contentType=self.content_type)

        output = json.loads(response.get('body').read())

        return output.get('generation')
    