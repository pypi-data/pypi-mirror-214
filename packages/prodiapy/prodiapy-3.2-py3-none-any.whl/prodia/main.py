import requests
import time
import asyncio
import re
from . import ext
endpoint = ext.endpoint
names = ext.names
models = ext.models
get_seed = ext.get_seed




class free_api:
    key1 = "89c5ea85-407c-4d57-b410-908f1a5e135c"


async def one_txt2img(key:str = None,
                      prompt: str = None,
                      negative_prompt: str = "badly drawn",
                      model: str = names.realisticvs14,
                      sampler: str = "DDIM",
                      aspect_ratio: str = "square",
                      steps: int = 30,
                      cfg_scale: int = 7,
                      seed: int = -1,
                      upscale: bool = False):
    payload = {
        "prompt": prompt,
        "model": model,
        "sampler": sampler,
        "negative_prompt": negative_prompt,
        "steps": steps,
        "cfg_scale": cfg_scale,
        "seed": seed,
        "upscale": upscale,
        "aspect_ratio": aspect_ratio
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": key
    }
    headers2 = {
        "accept": "application/json",
        "X-Prodia-Key": key
    }
    print(f"txt2img image with params:\n{payload}")
    response = requests.post(endpoint.txt2img, json=payload, headers=headers)
    job_id = response.json()['job']
    await asyncio.sleep(3)

    stt = True
    while stt is True:
        rec = requests.get(endpoint.retrieve.format(job_id=job_id), headers=headers2)
        status = rec.json()['status']
        if status == "succeeded":
            print(f"Image {job_id} generated!")
            image_url = rec.json()['imageUrl']
            stt = False
            return image_url
        elif status == "queued":
            print("Still working...")
            await asyncio.sleep(2)
        elif status == "generating":
            print("Still working...")
            await asyncio.sleep(2)
        else:
            print(f"Something went wrong! Please try later, error: {status}")
            stt = False
            return status

async def one_img2img(key:str = None,
                      image_url:str = None,
                      prompt: str = None,
                      negative_prompt: str = "badly drawn",
                      model: str = names.realisticvs14,
                      sampler: str = "DDIM",
                      denoising_strength: float=0.6,
                      steps: int = 30,
                      cfg_scale: int = 7,
                      seed: int = -1,
                      upscale: bool = False):
    payload = {
        "steps": steps,
        "sampler": sampler,
        "imageUrl": image_url,
        "model": model,
        "prompt": prompt,
        "denoising_strength": denoising_strength,
        "negative_prompt": negative_prompt,
        "cfg_scale": cfg_scale,
        "seed": seed,
        "upscale": upscale
    }
    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "X-Prodia-Key": key
    }
    headers2 = {
        "accept": "application/json",
        "X-Prodia-Key": key
    }
    print(f"img2img image with params:\n{payload}")
    response = requests.post(endpoint.img2img, json=payload, headers=headers)
    job_id = response.json()['job']
    await asyncio.sleep(3)

    stt = True
    while stt is True:
        rec = requests.get(endpoint.retrieve.format(job_id=job_id), headers=headers2)
        status = rec.json()['status']
        if status == "succeeded":
            print(f"Image {job_id} generated!")
            image_url = rec.json()['imageUrl']
            stt = False
            return image_url
        elif status == "queued":
            print("Still working...")
            await asyncio.sleep(2)
        elif status == "generating":
            print("Still working...")
            await asyncio.sleep(2)
        else:
            print(f"Something went wrong! Please try later, error: {status}")
            stt = False
            return status



async def gather(mode:str ="txt2img", key:str = None, image_url:str = None, prompt: str = None,
                             negative_prompt: str = "badly drawn",
                             model: str = names.realisticvs14,
                             sampler: str = "DDIM",
                             denoising_strength:float=0.6,
                             aspect_ratio: str = "square",
                             steps: int = 30,
                             cfg_scale: int = 7,
                             seed: int = -1,
                             upscale: bool = False,
                             number_outputs: int = 1, images: list = None):
        if mode == "txt2img":
            images = await asyncio.gather(*[one_txt2img(key=key, prompt=prompt, negative_prompt=negative_prompt, model=model, sampler=sampler, aspect_ratio=aspect_ratio, steps=steps, cfg_scale=cfg_scale, seed=seed, upscale=upscale) for _ in range(number_outputs)])
            return images
        elif mode == "img2img":
            images = await asyncio.gather(*[
                one_img2img(key=key, image_url=image_url, prompt=prompt, negative_prompt=negative_prompt, model=model, sampler=sampler,
                            denoising_strength=denoising_strength, steps=steps, cfg_scale=cfg_scale, seed=seed, upscale=upscale) for
                _ in range(number_outputs)])
            return images



class Client:
    def __init__(self, api_key:str) -> None:
        self.api_key = api_key

    def txt2img(self,
                          prompt: str = None,
                          negative_prompt: str = "badly drawn",
                          model: str = names.realisticvs14,
                          sampler: str = "DDIM",
                          aspect_ratio: str = "square",
                          steps: int = 30,
                          cfg_scale: int = 7,
                          seed: int = -1,
                          upscale: bool = False):
        if prompt is None:
            print("Prompt cant be empty")
            return
        payload = {
            "prompt": prompt,
            "model": model,
            "sampler": sampler,
            "negative_prompt": negative_prompt,
            "steps": steps,
            "cfg_scale": cfg_scale,
            "seed": seed,
            "upscale": upscale,
            "aspect_ratio": aspect_ratio
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": self.api_key
        }
        headers2 = {
            "accept": "application/json",
            "X-Prodia-Key": self.api_key
        }
        print(f"txt2img image with params:\n{payload}")
        response = requests.post(endpoint.txt2img, json=payload, headers=headers)
        try:
            job_id = response.json()['job']
        except ValueError:
            print(f"Invalid generation parameters || {response.status_code} || {response.content}")
            return
        time.sleep(3)

        stt = True
        while stt is True:
            rec = requests.get(endpoint.retrieve.format(job_id=job_id), headers=headers2)
            status = rec.json()['status']
            if status == "succeeded":
                print(f"Image {job_id} generated!")
                image_url = rec.json()['imageUrl']
                stt = False
                return image_url
            elif status == "queued":
                print("Still working...")
                time.sleep(2)
            elif status == "generating":
                print("Still working...")
                time.sleep(2)
            else:
                print(f"Something went wrong! Please try later, error: {status}")
                stt = False
                return status

    def img2img(self, image_url: str = None,
                          prompt: str = None,
                          negative_prompt: str = "badly drawn",
                          model: str = names.realisticvs14,
                          sampler: str = "DDIM",
                          denoising_strength: float = 0.6,
                          steps: int = 30,
                          cfg_scale: int = 7,
                          seed: int = -1,
                          upscale: bool = False):
        if image_url is None:
            print("image_url cant be none")
            return
        if prompt is None:
            print("Prompt cant be empty")
            return
        payload = {
            "steps": steps,
            "sampler": sampler,
            "imageUrl": image_url,
            "model": model,
            "prompt": prompt,
            "denoising_strength": denoising_strength,
            "negative_prompt": negative_prompt,
            "cfg_scale": cfg_scale,
            "seed": seed,
            "upscale": upscale
        }
        headers = {
            "accept": "application/json",
            "content-type": "application/json",
            "X-Prodia-Key": self.api_key
        }
        headers2 = {
            "accept": "application/json",
            "X-Prodia-Key": self.api_key
        }
        print(f"img2img image with params:\n{payload}")
        response = requests.post(endpoint.txt2img, json=payload, headers=headers)
        try:
            job_id = response.json()['job']
        except ValueError:
            print(f"Invalid generation parameters || {response.status_code} || {response.content}")
            return
        time.sleep(3)

        stt = True
        while stt is True:
            rec = requests.get(endpoint.retrieve.format(job_id=job_id), headers=headers2)
            status = rec.json()['status']
            if status == "succeeded":
                print(f"Image {job_id} generated!")
                image_url = rec.json()['imageUrl']
                stt = False
                return image_url
            elif status == "queued":
                print("Still working...")
                time.sleep(2)
            elif status == "generating":
                print("Still working...")
                time.sleep(2)
            else:
                print(f"Something went wrong! Please try later, error: {status}")
                stt = False
                return status

class AsyncClient:
    def __init__(self, api_key:str) -> None:
        self.api_key = api_key

    async def txt2img(self, prompt:str=None,
        negative_prompt:str="badly drawn",
        model:str=names.realisticvs14,
        sampler:str="DDIM",
        aspect_ratio:str="square",
        steps:int=30,
        cfg_scale:int=7,
        seed:int=-1,
        upscale:bool=False,
        number_outputs:int=1):
        if prompt is None:
            print("Prompt cant be empty")
            return
        images = await gather(mode="txt2img", key=self.api_key, prompt=prompt, negative_prompt=negative_prompt, model=model, sampler=sampler, aspect_ratio=aspect_ratio, steps=steps, cfg_scale=cfg_scale, seed=seed, upscale=upscale, number_outputs=number_outputs)
        return images

    async def img2img(self, image_url:str = None, prompt:str=None,
        negative_prompt:str="badly drawn",
        model:str=names.realisticvs14,
        sampler:str="DDIM",
        denoising_strength:float=0.6,
        steps:int=30,
        cfg_scale:int=7,
        seed:int=-1,
        upscale:bool=False,
        number_outputs:int=1):
        if image_url is None:
            print("image_url cant be none")
            return
        if prompt is None:
            print("Prompt cant be empty")
            return
        images = await gather(mode="img2img", key=self.api_key, image_url=image_url, prompt=prompt, negative_prompt=negative_prompt, model=model, sampler=sampler, denoising_strength=denoising_strength, steps=steps, cfg_scale=cfg_scale, seed=seed, upscale=upscale, number_outputs=number_outputs)
        return images


