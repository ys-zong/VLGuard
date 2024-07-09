# VLGuard
[[Website]](https://ys-zong.github.io/VLGuard/) [[Paper]](https://arxiv.org/abs/2402.02207) [[Data]](https://huggingface.co/datasets/ys-zong/VLGuard) [[🤗Weights]](https://huggingface.co/collections/ys-zong/vlguard-6671c22a97ffa934dd8fd520)

Safety Fine-Tuning at (Almost) No Cost: A Baseline for Vision Large Language Models.

## Updates
- [2024/07/09] We released the evaluation code for VLGuard test set.
- [2024/06/19] We released the fine-tuned model weights that we used for experiments.
- [2024/05/01] VLGuard is accepted to ICML 2024!
- [2024/02/06] We released [arXiv](https://arxiv.org/abs/2402.02207) and [data](https://huggingface.co/datasets/ys-zong/VLGuard) for VLGuard. With our safety fine-tuning, the we substantially improve the safety of vision large language models while maintaining the helpfulness.

## Dataset
You can find the dataset at [Huggingface](https://huggingface.co/datasets/ys-zong/VLGuard). `train.json` and `test.json` are the meta data of VLGuard and the images are in `train.zip` and `test.zip`. 

## Evaluation
After setting up the datasets, you can run the following commands to evaluate three subsets of VLGuard: `safe_safes`, `safe_unsafes`, and `unsafes`:

```bash
CUDA_VISIBLE_DEVICES=0 python VLGuard_eval.py --dataset unsafes --engine llava15-7b --metaDir /path/to/test.json --imageDir /path/to/VLGuard/test
CUDA_VISIBLE_DEVICES=0 python VLGuard_eval.py --dataset safe_unsafes --engine llava15-7b --metaDir /path/to/test.json --imageDir /path/to/VLGuard/test
CUDA_VISIBLE_DEVICES=0 python VLGuard_eval.py --dataset safe_safes --engine llava15-7b --metaDir /path/to/test.json --imageDir /path/to/VLGuard/test
```

The scripts will print out the ASR for `safe_unsafes`, and `unsafes` with string match (keywords [here]()). The generated predictions will be saved to `results` folder. 

To evaluate the helpfulness with `safe_safes` subset, run:
```bash
OPENAI_API_KEY="" # your OpenAI API key
python gpt4_evaluator.py --file_path results/safe_safes/{the_model_to_evaluate}.json --image_path /path/to/VLGuard/test --reference_path ./data/gpt4_safe_safes.json --output_path /path/to/save/results
```
It will calculate the win rate against GPT-4V.

## Model Weights
We release the weights below. You can use them in exactly the same way as the original [LLaVA](https://github.com/haotian-liu/LLaVA/tree/main).

**Weights from Mixed Fine-tuning**

| Model | Original VLLM | Fine-tuning | 🤗 Checkpoint |   
|----------|----------|-----------|-----------|
| LLaVA-v1.5-7B-Mixed | LLaVA-v1.5-7B | Full FT | [ys-zong/llava-v1.5-7b-Mixed](https://huggingface.co/ys-zong/llava-v1.5-7b-Mixed) |  
| LLaVA-v1.5-7B-Mixed-LoRA | LLaVA-v1.5-7B | LoRA | [ys-zong/llava-v1.5-7b-Mixed-lora](https://huggingface.co/ys-zong/llava-v1.5-7b-Mixed-lora) |   
| LLaVA-v1.5-13B-Mixed | LLaVA-v1.5-13B | Full FT | [ys-zong/llava-v1.5-13b-Mixed](https://huggingface.co/ys-zong/llava-v1.5-13b-Mixed) |   
| LLaVA-v1.5-13B-Mixed-LoRA | LLaVA-v1.5-13B | LoRA | [ys-zong/llava-v1.5-13b-Mixed-lora](https://huggingface.co/ys-zong/llava-v1.5-13b-Mixed-lora) |   

----
We have also released the weights of "Clean" LLaVA-v1.5 that we re-trained after removing the harmful samples from the training data (Table 1).

| Model | LLM | Fine-tuning | 🤗 Checkpoint |  
|----------|----------|-----------|-----------|
| LLaVA-v1.5-7B-Clean | Vicuna-7B | Full FT | [ys-zong/llava-v1.5-7b-Clean](https://huggingface.co/ys-zong/llava-v1.5-7b-Clean) |  
| LLaVA-v1.5-7B-Clean-LoRA  | Vicuna-7B | LoRA | [ys-zong/llava-v1.5-7b-Clean-lora](https://huggingface.co/ys-zong/llava-v1.5-7b-Clean-lora) |   
| LLaVA-v1.5-13B-Clean | Vicuna-13B | Full FT  | [ys-zong/llava-v1.5-13b-Clean](https://huggingface.co/ys-zong/llava-v1.5-13b-Clean) |   
| LLaVA-v1.5-13B-Clean-LoRA | Vicuna-13B | LoRA | [ys-zong/llava-v1.5-13b-Clean-lora](https://huggingface.co/liuhaotian/llava-v1.6-34b) |   

## Usage

To fine-tune [LLaVA](https://github.com/haotian-liu/LLaVA) or [MiniGPT-v2](https://github.com/haotian-liu/LLaVA), you can first run
```bash
python convert_to_llava_format.py
```
to convert VLGuard to LLaVA data format and follow their fine-tuning scripts to do the fine-tuning.

## Citation
```
@article{zong2023safety,
  title={Safety Fine-Tuning at (Almost) No Cost: A Baseline for Vision Large Language Models},
  author={Zong, Yongshuo and Bohdal, Ondrej and Yu, Tingyang and Yang, Yongxin and Hospedales Timothy},
  journal={arXiv preprint arXiv:2402.02207},
  year={2024}
}
```