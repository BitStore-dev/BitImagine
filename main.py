from InquirerPy import prompt
import asyncio
import base64
import aiofiles
import requests
import os
import aiohttp
from pystyle import Write, Colors, Colorate
import time
import threading

def loading_animation(starttime):
    symbols = ['⣾', '⣷', '⣯', '⣟', '⡿', '⢿', '⣻', '⣽']
    i = 0
    while generating_image:
        i = (i + 1) % len(symbols)
        print('\r\033[K%s Generating Image...' % symbols[i], flush=True, end='')
        time.sleep(0.1)
    print('\r\033[K⣿ Finished Image Generation' , flush=True, end='')
    print(Colors.light_gray + "\n\nTime elapsed: " + Colors.white + str(round(time.time() - starttime, 2)) + " seconds")


def choose_model():
    question = [
        {
            'type': 'list',
            'name': 'model',
            'message': 'Which model do you want to use?',
            'choices': ['Stability Ai','SDXL 0.9', 'SDXL 1.0 [Recommended]']
        }
    ]
    answers = prompt(question)
    return answers['model']

def choose_number_of_images():
    question = [
        {
            'type': 'input',
            'name': 'number_of_images',
            'message': 'How many images do you want to generate?',
            'validate': lambda text: str.isdigit(text) and int(text) > 0,
            'filter': lambda val: int(val)
        }
    ]
    answers = prompt(question)
    return answers['number_of_images']

def choose_ratio(model):
    question = [
        {
            'type': 'list',
            'name': 'ratio',
            'message': 'Which ratio do you want to use?',
            'choices': ['Square', 'Landscape', 'Portrait']
        }
    ]
    # depending on each model, the w and h returned will be diffrent for each ratio
    answers = prompt(question)
    if answers['ratio'] == "Square":
        if model == "SDXL 0.9":
            return 1024, 1024
        elif model == "SDXL 1.0 [Recommended]":
            return 1024, 1024
        elif model == "Stability Ai":
            return 1024, 1024
    elif answers['ratio'] == "Portrait":
        if model == "SDXL 0.9":
            return 1024, 768
        elif model == "SDXL 1.0 [Recommended]":
            return 1152, 896
        elif model == "Stability Ai":
            return 1024, 768
    elif answers['ratio'] == "Landscape":
        if model == "SDXL 0.9":
            return 768, 1024
        elif model == "SDXL 1.0 [Recommended]":
            return 896, 1152
        elif model == "Stability Ai":
            return 768, 1024

def choose_style():
    question = [
        {
            'type': 'list',
            'name': 'style',
            'message': 'Which style do you want to use?',
            'choices': [
                'none',
                'photographic',
                'anime',
                '3d-model',
                'neon-punk',
                'origami',
                'pixel-art',
                'analog-film',
                'cinematic',
                'comic-book',
                'digital-art',
                'enhance',
                'fantasy-art',
                'isometric',
                'line-art',
                'low-poly',
                'modeling-compound',
                'tile-texture'
            ]
        }
    ]
    answers = prompt(question)
    return answers['style']


async def sdxl09(height, width, prompt, i):
        url = "https://imageapp.xyz/api/generate/stability"
        data = {
                "engine": "stable-diffusion-xl-1024-v0-9",
                "prompt": str(prompt),
                "style": "none",
                "ratio": {
                            "h": int(height),
                            "w": int(width)
                        }
                }
        headers = {
            "Connection": "keep-alive",
            "Origin": "https://imageapp.xyz",
            "Referer": "https://imageapp.xyz/",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    response_json = await response.json()
                    base64_image = response_json['artifacts'][0]['base64']
                    image_data = base64.b64decode(base64_image)
                    filename = os.path.join('images', f'image_{i}.png')
                    async with aiofiles.open(filename, 'wb') as image_file:
                        await image_file.write(image_data)
    
async def sdxl10(height, width, prompt, style, i):
        url = "https://imageapp.xyz/api/generate/stability"
        data = {
                "engine": "stable-diffusion-xl-1024-v1-0",
                "prompt": str(prompt),
                "style": style,
                "ratio": {
                            "h": int(height),
                            "w": int(width)
                        }
                }
        headers = {
            "Connection": "keep-alive",
            "Origin": "https://imageapp.xyz",
            "Referer": "https://imageapp.xyz/",
            "Content-Type": "application/json",
        }
        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    response_json = await response.json()
                    base64_image = response_json['artifacts'][0]['base64']
                    image_data = base64.b64decode(base64_image)
                    filename = os.path.join('images', f'image_{i}.png')
                    async with aiofiles.open(filename, 'wb') as image_file:
                        await image_file.write(image_data)
                

async def stability(height, width, prompt, i):
        url = "https://imageapp.xyz/api/generate/general-replicate"
        data = {
            "model": "stabilityai",
            "prompt": prompt,
            "ratio": {
                "w": int(width),
                "h": int(height)
            }
        }
        headers = {
            "Connection": "keep-alive",
            "Origin": "https://imageapp.xyz",
            "Referer": "https://imageapp.xyz/",
            "Content-Type": "application/json",
        }

        async with aiohttp.ClientSession() as session:
            async with session.post(url, json=data, headers=headers) as response:
                if response.status == 200:
                    image_urls = await response.json()
                    
                    # Download and save each image
                    for i, image_url in enumerate(image_urls):
                        async with session.get(image_url) as image_response:
                            if image_response.status == 200:
                                # Create images directory if it doesn't exist
                                if not os.path.exists('images'):
                                    os.makedirs('images')
                                # Write the image to a file
                                with open(f'images/image_{i}.png', 'wb') as f:
                                    f.write(await image_response.read())
                            else:
                                print(f"Failed to download image from {image_url}")
                else:
                    if response.content_type == 'application/json':
                        print("Failed to generate images: " + str(response.status) +" | " + str(await response.json()))
                    else:
                        print("Failed to generate images: " + str(response.status) +" | " + str(await response.text()))


logo = f'''

        .___                       .__               
        |   | _____ _____     ____ |__| ____   ____  
        |   |/     \\\\__  \   / ___\|  |/    \_/ __ \ 
        |   |  Y Y  \/ __ \_/ /_/  >  |   |  \  ___/ 
        |___|__|_|  (____  /\___  /|__|___|  /\___  >
                  \/     \//_____/         \/     \/ 
                
                    By @daniduese
            
'''

os.system('cls' if os.name == 'nt' else 'clear')
print(Colorate.Horizontal(Colors.green_to_blue, logo))
prompt2 = Write.Input("Enter a prompt: ", Colors.light_gray, interval=0.05)
model = choose_model()
if model == "SDXL 1.0 [Recommended]":
    style = choose_style()
height, width = choose_ratio(model)
number_of_images = choose_number_of_images()
generating_image = True
starttimetotal = time.time()
for i in range(number_of_images):
    starttime = time.time()
    generating_image = True
    t = threading.Thread(target=loading_animation, args=(starttime,))
    t.start()
    if model == "SDXL 0.9":
        asyncio.run(sdxl09(height, width, prompt2, i))
    elif model == "SDXL 1.0 [Recommended]":
        asyncio.run(sdxl10(height, width, prompt2, style, i))
    elif model == "Stability Ai":
        asyncio.run(stability(height, width, prompt2, i))
    generating_image = False
    t.join()
    print("\n")
    print(Colors.orange + "! " + Colors.light_gray + "Image saved in folder")
    # print file path
    print(Colors.orange + "! " + Colors.light_gray + "File path: " + Colors.white + os.path.join(os.getcwd(), 'images', f'image_{i}.png'))
    print("\n")
print(Colors.light_gray + "Total time elapsed: " + Colors.white + str(round(time.time() - starttimetotal, 2)) + " seconds")