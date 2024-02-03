import json
import os
import random

with open('data/train.json', 'r') as f:
    train_data = json.load(f)

random.seed(0)
def format_conversation(instruction_key, response, from_human='human', from_gpt='gpt', prepend_image=False):
    if prepend_image:
        human_value = f'<image>{response[instruction_key]}'
    else:
        human_value = response[instruction_key]
    return [
        {"from": from_human, "value": human_value},
        {"from": from_gpt, "value": response['response']}
    ]

for item in train_data:
    item['conversations'] = []
    instruction_responses = item['instr-resp']

    # Randomly shuffle the instruction-response pairs if there are both safe and unsafe
    if len(instruction_responses) > 1:
        random.shuffle(instruction_responses)

        item['conversations'].extend(format_conversation(list(instruction_responses[0].keys())[0], instruction_responses[0], prepend_image=True))
        item['conversations'].extend(format_conversation(list(instruction_responses[1].keys())[0], instruction_responses[1], prepend_image=False))
    else:
        item['conversations'].extend(format_conversation('instruction', instruction_responses[0], prepend_image=True))
    
    item.pop('instr-resp')

with open('data/train_llava_format.json', 'w') as f:
    json.dump(train_data, f, indent=2)