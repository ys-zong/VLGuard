# VLGuard
[[Website]](https://github.com/ys-zong/VLGuard) [[Paper]](https://arxiv.org/abs/2402.02207)

Safety Fine-Tuning at (Almost) No Cost: A Baseline for Vision Large Language Models.

## Dataset
You can find the dataset in `data/`. `train.json` and `test.json` are the meta data of VLGuard and the images are in `train.zip` and `test.zip`.

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