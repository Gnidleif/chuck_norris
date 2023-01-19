#!/usr/bin/python3
import urllib.request, random, textwrap, certifi, imgbbpy, uuid, pathlib, os, warnings
from io import BytesIO
from PIL import Image, ImageFont, ImageDraw
__location__ = pathlib.Path(__file__).parent.resolve()
warnings.filterwarnings("ignore", category=DeprecationWarning)

__config__ = {
    "api_key": "783b3cab68a7c0bccee085dfd3bb2648",
    "base_url": "https://api.imgbb.com/1/upload",
    "image_urls": [
        "t2YTzzB/59d3c7d5-1b8c-4551-ae6a-3d543bcecd3e",
        "JkxYdzZ/455c5599-1467-4def-84e8-59512c97e0e2",
        "V2d5GVF/f65e78fe-91c3-4265-9bfc-6eee9e91c64d",
        "djg6HL7/de04a8f3-f851-46b2-ac5d-5593ac45a418",
        "dWdDqxF/5273bc65-297c-433b-967b-1fee0ba55f83",
        "pZqrTGb/672beb26-404c-4f27-991e-83f43c4f0801"
    ]
}

def create_image(joke: str, img_data: str) -> Image:
    img = Image.open(BytesIO(bytes.fromhex(img_data)))
    font = ImageFont.truetype("impact.ttf", size=25)
    (black, white) = ((0, 0, 0), (255, 255, 255))

    (m, o) = (5, 40)
    draw = ImageDraw.Draw(img)
    wrapped = textwrap.wrap(joke, width = 35)
    (_, h) = img.size
    pos = (10, h - (len(wrapped) * o))

    for i in range(len(wrapped)):
        (x, y) = (pos[0], pos[1] + o * i)
        (l, t, r, b) = draw.textbbox((x, y), wrapped[i], font=font)
        draw.rectangle((l - m, t - m, r + m, b + m), fill = black)
        draw.text((x, y), wrapped[i], font=font, fill = white)
    
    return img

def get_resp(url: str) -> str:
    req = urllib.request.Request(url)
    return urllib.request.urlopen(req, cafile=certifi.where()).read()

def run(_: list[str]) -> None:
    random.seed()
    jokes = get_resp("https://raw.githubusercontent.com/Gnidleif/chuck_norris/main/jokes.txt").splitlines()
    joke = str(random.choice(jokes), "utf-8")

    url = random.choice(__config__["image_urls"])
    url = "https://i.ibb.co/" + url +".jpg"
    resp = get_resp(url)

    img = create_image(joke, resp.hex())
    result = __location__ / f"result.jpg"
    img.save(result)

    client = imgbbpy.SyncClient(__config__["api_key"])
    url = client.upload(file=result, name=uuid.uuid4()).url
    os.remove(result)

    print("Chuck Norris image generated here: " + url)

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])