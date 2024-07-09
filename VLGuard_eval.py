import torch
import os
import json
import argparse
import numpy as np
import gc
from utils import utils, model_utils

model_mappings = {
    'llava15-7b': 'liuhaotian/llava-v1.5-7b',
    'llava15-13b': 'liuhaotian/llava-v1.5-13b',
    'llava15-7b-mixed': 'ys-zong/llava-v1.5-7b-Mixed',
    'llava15-13b-mixed': 'ys-zong/llava-v1.5-13b-Mixed',
    'llava15-7b-clean': 'ys-zong/llava-v1.5-7b-CLean',
    'llava15-13b-clean': 'ys-zong/llava-v1.5-13b-CLean',
}

def parse_args():
    parser = argparse.ArgumentParser(description='VLGuard Evaluation')

    parser.add_argument('--metaDir', default='data/test.json', type=str)
    parser.add_argument('--imageDir', default='data/VLGuard/test', type=str)
    parser.add_argument('--dataset', default='unsafes', type=str, choices=['safe_unsafes', 'safe_safes', 'unsafes'])

    parser.add_argument("--engine", "-e", default=["llava15-7b"], nargs="+")

    parser.add_argument('--max_new_tokens', default=256, type=int, help='Max tokens for generation.')
    parser.add_argument('--debug', default=False, action='store_true', help='If debug, take a subset.')

    return parser.parse_args()


def eval_questions(args, questions, model, tokenizer, processor, root_path, engine):

    results = {}
    total_succ = []

    with torch.no_grad():
        for question in questions:
            img_id = question['image']
            image, image_path = utils.load_image(img_id, root_path)
            question_text = question['question']

            predicted_answers = model_utils.model_inference(engine, model, tokenizer, image, question_text, processor, args.max_new_tokens)
            results[question['image']] = predicted_answers

            succ = utils.check_success_attack(predicted_answers)
            total_succ.append(succ)

    if args.dataset != 'safe_safes':
        succ_rate = round(np.mean(total_succ) * 100, 2)
        print(f'{args.dataset} ASR of {engine}: ', f"{succ_rate}", flush=True)

    return results
    

if __name__ == "__main__":
    args = parse_args()

    all_questions = utils.load_data(args)

    for engine in args.engine:

        model, tokenizer, processor = model_utils.load_model(model_mappings[engine], args)
        print("Loaded model: {}\n".format(engine))

        results_dict = eval_questions(args, all_questions, model, tokenizer, processor, args.imageDir, engine)
        os.makedirs(f'results/{args.dataset}', exist_ok=True)
        with open(f'results/{args.dataset}/{engine}.json', 'w') as f:
            json.dump(results_dict, f, indent=4)
        
        del model, tokenizer, processor
        torch.cuda.empty_cache()
        gc.collect()