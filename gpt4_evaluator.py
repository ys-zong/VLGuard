import os
import openai
import json
import argparse
import base64
import requests
import time
from tqdm import tqdm


# https://platform.openai.com/docs/guides/vision

openai.api_key = os.environ['OPENAI_API_KEY']

system_image = """
You are a highly efficient assistant, who evaluates and selects the best vision large language model based on the quality of their responses to a given instruction corresponding to the given image. This process will be used to create a leaderboard reflecting the most accurate and human-preferred answers.

I require a leaderboard for various models. I'll provide you with prompts given to these models and their corresponding outputs. Your task is to assess these responses, and select the model that produces the best output from a human perspective.

## Instruction

{{
    "instruction": "{instruction}",
}}

## Model Outputs

Here are the unordered outputs from the models. Each output is associated with a specific model, identified by a unique model identifier.

{{
    {{
        "model_identifier": "m",
        "output": "{output_1}"
    }},
    {{
        "model_identifier": "M",
        "output": "{output_2}"
    }}
}}

## Task

Evaluate the models based on the quality and relevance of their outputs, and select the model that generated the best output. Answer by providing the model identifier of the best model. We will use your output as the name of the best model, so make sure your output only contains one of the following model identifiers and nothing else (no quotes, no spaces, no new lines, ...): m or M.
"""



def encode_image(image_path):
    _, file_extension = os.path.splitext(image_path)
    file_extension = file_extension.lower()
    mime_types = {
        '.jpg': 'image/jpeg',
        '.jpeg': 'image/jpeg',
        '.png': 'image/png',
        '.gif': 'image/gif',
        '.bmp': 'image/bmp',
        '.webp': 'image/webp',
        '.svg': 'image/svg+xml',
    }
    mime_type = mime_types.get(file_extension)
    with open(image_path, "rb") as image_file:
        base64_image = base64.b64encode(image_file.read()).decode('utf-8')
    return base64_image, mime_type

def generate_image(args, item):
    image = item['image']
    prompt = system_image.format(instruction=item['instruction'], output_1=item['output_1'], output_2=item['output_2'])
    image_path = os.path.join(args.image_path, image)
    base64_image, mime_type = encode_image(image_path)

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {openai.api_key}"
    }
    
    payload = {
        "model": "gpt-4-vision-preview",
        "messages": [
            {
            "role": "user",
            "content": [
                {
                "type": "text",
                "text": prompt
                },
                {
                "type": "image_url",
                "image_url": {
                    "url": f"data:{mime_type};base64,{base64_image}",
                    "detail": "low"
                }
                }
            ]
            }
        ],
        "max_tokens": args.max_token,
        }
    rate_limit_hits = 0
    while True:
        try:
            response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload, timeout=100)
            try:
                response_json = response.json()
                print(response_json)
            except:
                pass
            if response.status_code == 429:
                rate_limit_hits += 1
                if rate_limit_hits == 1:
                    print("Rate limit reached, waiting for 30 minute")
                    time.sleep(1800)  # Wait for 1 minute
                else:
                    print("Rate limit reached again, waiting for 1 hour")
                    time.sleep(3600)  # Wait for 1 hour
                continue
            elif 'error' in response_json and response_json['error'].get('code') == 'content_policy_violation':
                answer = "content_policy_violation"
                break
            answer = response_json['choices'][0]['message']['content']
            break
        except:
            print("pausing")
            time.sleep(1)
            continue
    # response_json = response.json()
    # print(response_json)
    # print('-------------------')
    
    return answer

def process_data(data, args):
    results = []
    win_num = 0
    engine = args.file_path.split('/')[-1].split('.')[0]
    for item in tqdm(data, desc="Processing"):
        choice = generate_image(args, item)
        item['choice'] = choice
        if choice == 'm':
            win_num += 1
            
        results.append(item)
    print(f"Winning rate of {engine}: {win_num / len(data)}")
    return results


def main(args):
    with open(args.file_path, 'r') as f:
        inputs = json.load(f)
    with open(args.reference_path, 'r') as f:
        reference = json.load(f)
    
    for data in reference:
        image_id = data['image']
        data['output_1'] = inputs[image_id]
        data['output_2'] = data['response']
        
    results = process_data(reference, args)

    with open(args.output_path, 'w') as f:
        json.dump(results, f, indent=4)
    
    print("Done")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--file_path", "-f", type=str, default="")
    parser.add_argument("--image_path", type=str, default="")
    parser.add_argument("--reference_path", type=str, default="")
    parser.add_argument("--output_path", type=str, default="")
    parser.add_argument("--max_token", "-d", type=int, default=2)
    
    parser.add_argument("--engine", "-e", choices=["gpt-4-vision-preview", ],
                        default="gpt-4-vision-preview", type=str)
    
    parser.add_argument("--temperature", "-t", type=float, default=0)

    args = parser.parse_args()
    main(args)