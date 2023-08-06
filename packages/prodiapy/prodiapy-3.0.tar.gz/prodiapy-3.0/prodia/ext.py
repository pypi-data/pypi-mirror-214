import requests
import re

class endpoint:
    txt2img = "https://api.prodia.com/v1/job"
    img2img = "https://api.prodia.com/v1/transform"
    retrieve = "https://api.prodia.com/v1/job/{job_id}"

class names:
    sd14 = "sdv1_4.ckpt [7460a6fa]"
    sd15 = "v1-5-pruned-emaonly.ckpt [81761151]"
    anyv3 = "anythingv3_0-pruned.ckpt [2700c435]"
    anyv4 = "anything-v4.5-pruned.ckpt [65745d25]"
    anyv5 = "anythingV5_PrtRE.safetensors [893e49b9]"
    aom = "AOM3A3_orangemixs.safetensors [9600da17]"
    analog = "analog-diffusion-1.0.ckpt [9ca13f02]"
    theallys = "theallys-mix-ii-churned.safetensors [5d9225a4]"
    evm = "elldreths-vivid-mix.safetensors [342d9d26]"
    deliberate = "deliberate_v2.safetensors [10ec4b29]"
    openjourney = "openjourney_V4.ckpt [ca2f377f]"
    dreaml1 = "dreamlike-diffusion-1.0.safetensors [5c9fd6e0]"
    dreaml2 = "dreamlike-diffusion-2.0.safetensors [fdcf65e7]"
    portrait = "portrait+1.0.safetensors [1400e684]"
    riffusion = "riffusion-model-v1.ckpt [3aafa6fe]"
    timeless = "timeless-1.0.ckpt [7c4971d4]"
    dreamshaper5 = "dreamshaper_5BakedVae.safetensors [a3fbf318]"
    dreamshaper6 = "dreamshaper_6BakedVae.safetensors [114c8abb]"
    sbp = "shoninsBeautiful_v10.safetensors [25d8c546]"
    rev = "revAnimated_v122.safetensors [3f4fefd9]"
    meina = "meinamix_meinaV9.safetensors [2ec66ab0]"
    lyriel15 = "lyriel_v15.safetensors [65d547c5]"
    lyriel16 = "lyriel_v16.safetensors [68fceea2]"
    realisticvs20 = "Realistic_Vision_V2.0.safetensors [79587710]"
    realisticvs14 = "Realistic_Vision_V1.4-pruned-fp16.safetensors [8d21810b]"
    euler = "Euler"
    euler_a = "Euler a"
    heun = "Heun"
    dpm = "DPM++ 2M Karras"
    ddim = "DDIM"
    decor_models = [
        "SD v1.4",
        "SD v1.5",
        "Anything v3",
        "Anything v4",
        "Anything v5",
        "AbyssOrangeMix v3",
        "Analog v1",
        "TheAlly's Mix II",
        "Elldreth's Vivid",
        "Deliberate v2",
        "Openjourney v4",
        "Dreamlike Diffusion v1",
        "Dreamlike Diffusion v2",
        "Portrait v1",
        "Timeless v1",
        "Riffusion v1",
        "DreamShaper v5",
        "DreamShaper v6",
        "revAnimated v1.2.2",
        "MeinaMix v9",
        "Lyriel v1.5",
        "Lyriel v1.6",
        "Realistic Vision v1.4",
        "Realistic Vision v2.0",
        "Shonin's Beautiful People"
    ]
    real_models = [
        "sdv1_4.ckpt [7460a6fa]",
        "v1-5-pruned-emaonly.ckpt [81761151]",
        "anythingv3_0-pruned.ckpt [2700c435]",
        "anything-v4.5-pruned.ckpt [65745d25]",
        "anythingV5_PrtRE.safetensors [893e49b9]",
        "AOM3A3_orangemixs.safetensors [9600da17]",
        "analog-diffusion-1.0.ckpt [9ca13f02]",
        "theallys-mix-ii-churned.safetensors [5d9225a4]",
        "elldreths-vivid-mix.safetensors [342d9d26]",
        "deliberate_v2.safetensors [10ec4b29]",
        "openjourney_V4.ckpt [ca2f377f]",
        "dreamlike-diffusion-1.0.safetensors [5c9fd6e0]",
        "dreamlike-diffusion-2.0.safetensors [fdcf65e7]",
        "portrait+1.0.safetensors [1400e684]",
        "riffusion-model-v1.ckpt [3aafa6fe]",
        "timeless-1.0.ckpt [7c4971d4]",
        "dreamshaper_5BakedVae.safetensors [a3fbf318]",
        "dreamshaper_6BakedVae.safetensors [114c8abb]",
        "shoninsBeautiful_v10.safetensors [25d8c546]",
        "revAnimated_v122.safetensors [3f4fefd9]",
        "meinamix_meinaV9.safetensors [2ec66ab0]",
        "lyriel_v15.safetensors [65d547c5]",
        "lyriel_v16.safetensors [68fceea2]",
        "Realistic_Vision_V2.0.safetensors [79587710]",
        "Realistic_Vision_V1.4-pruned-fp16.safetensors [8d21810b]"

    ]
    samplerlist = ["Euler", "Euler a", "Heun", "DPM++ 2M Karras", "DDIM"]

def models():
    for model in names.real_models:
        print(model)

def get_seed(image_url):
    string = requests.get(image_url)
    pattern = r'Seed: (\d+)'
    match = re.search(pattern, str(string.content[:4000]))
    if match:
        return match.group(1)
    else:
        return None

class free_api:
    key1 = "89c5ea85-407c-4d57-b410-908f1a5e135c"