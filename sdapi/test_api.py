import json
import argparse
import time
import requests
import io
import base64
from PIL import Image, PngImagePlugin

url = "http://106.75.74.59:3000"


# 文本生成图片
def test_txt2img():
    parser = argparse.ArgumentParser(description="manual to this script")
    parser.add_argument("--prompt", type=str, default=None)
    parser.add_argument("--batch-size", type=int, default=4)
    parser.add_argument("--width", type=int, default=512)
    parser.add_argument("--height", type=int, default=512)
    parser.add_argument("--steps", type=int, default=50)
    args = parser.parse_args()
    if args.prompt is None:
        print("Prompt can't empty!")
        return

    payload = {
        "prompt": args.prompt,
        "batch_size": args.batch_size,
        "width": args.width,
        "height": args.height,
        "steps": args.steps
    }

    response = requests.post(url=f'{url}/sdapi/v1/txt2img', json=payload)
    res = response.json()
    index = 1
    for i in res['images']:
        image = Image.open(io.BytesIO(base64.b64decode(i.split(",", 1)[0])))

        # png_payload = {
        #     "image": "data:image/png;base64," + i
        # }
        # response2 = requests.post(url=f'{url}/sdapi/v1/png-info', json=png_payload)
        #
        # pnginfo = PngImagePlugin.PngInfo()
        # pnginfo.add_text("parameters", response2.json().get("info"))

        file_prefix = int(time.time())
        image.save(f'output-{file_prefix}-{index}.png')

        index += 1


def test_img2img():
    pass


if __name__ == "__main__":
    test_txt2img()


