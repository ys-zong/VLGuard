import torch
from llava.model.builder import load_pretrained_model as load_llava_model
from llava.conversation import conv_templates
from llava.constants import IMAGE_TOKEN_INDEX, DEFAULT_IMAGE_TOKEN, DEFAULT_IM_START_TOKEN, DEFAULT_IM_END_TOKEN
from llava.mm_utils import tokenizer_image_token


def model_inference(engine, model, tokenizer, image, prompt, processor, max_new_tokens):
    
    image_tensor =  processor.preprocess([image], return_tensors='pt')['pixel_values'].to(torch.float16).cuda()
    
    if model.config.mm_use_im_start_end:
        inp = DEFAULT_IM_START_TOKEN + DEFAULT_IMAGE_TOKEN + DEFAULT_IM_END_TOKEN + '\n' + prompt
    else:
        inp = DEFAULT_IMAGE_TOKEN + '\n' + prompt
    
    conv_mode = 'llava_v1'
    conv = conv_templates[conv_mode].copy()
    conv.append_message(conv.roles[0], inp)
    conv.append_message(conv.roles[1], None)
    prompt = conv.get_prompt()
    input_ids = tokenizer_image_token(prompt, tokenizer, IMAGE_TOKEN_INDEX, return_tensors='pt').unsqueeze(0).cuda()
    with torch.inference_mode():
        generated_ids = model.generate(
            input_ids,
            images=image_tensor.unsqueeze(0),
            do_sample=False,
            temperature=1,
            max_new_tokens=max_new_tokens,
            min_new_tokens=1,
            )
    predicted_answers = tokenizer.batch_decode(generated_ids, skip_special_tokens=True)[0]
    return predicted_answers

def load_model(model_path, args=None):
    tokenizer, model, image_processor, context_len = load_llava_model(model_path=model_path, model_base=None, model_name='llava', 
                                                                      attn_implementation='flash_attention_2', torch_dtype='float16', device_map='cuda',)
    processor = image_processor
    return model, tokenizer, processor
