#!/usr/bin/python3
import pathlib, os, warnings, json, random, textwrap, uuid, shutil, codecs
from urllib import request, parse
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
__location__ = pathlib.Path(__file__).parent.resolve()
__source__ = __location__ / "source_images"
__resized__ = __location__ / "resized_images"
__data__ = __location__ / "data.json"
__results__ = __location__  / "results"

warnings.filterwarnings("ignore", category=DeprecationWarning)

def resize_image(image_path: str, quality: int = 90, width: int = 800, height: int = 600) -> bool:
    img = Image.open(image_path)
    result = False

    img = img.resize((width, height), Image.ANTIALIAS)
    file_name, ext = os.path.splitext(image_path)
    new_path = __resized__ / f"{os.path.basename(file_name)}.jpg"
    
    try:
        img.save(new_path, quality=quality, optimize=True)
        result = True
    except OSError:
        img = img.convert("RGB")
        img.save(new_path, quality=quality, optimize=True)

    return result

def prepare() -> None:
    if os.path.exists(__results__):
        shutil.rmtree(__results__)
    __results__.mkdir(parents=True, exist_ok=True)

    if os.path.exists(__resized__):
        shutil.rmtree(__resized__)
    __resized__.mkdir(parents=True, exist_ok=True)

    for file in pathlib.Path(__source__).glob('*'):
        _ = resize_image(file)

    output = {}

    with open(__location__ / "jokes.txt", 'r', encoding="utf-8") as r_txt:
        jokes = r_txt.read().split('\n')
        output["jokes"] = jokes

    img_data = []
    for file in pathlib.Path(__resized__).glob('*'):
        with open(file, 'rb') as r_bin:
            img_data.append(r_bin.read().hex())
    output["images"] = img_data

    with open(__data__, 'w') as w_json:
        w_json.write(json.dumps(output, indent=2))

def create_image(joke: str, img_data: str) -> Image:
    img = Image.open(BytesIO(bytes.fromhex(img_data)))
    font = ImageFont.truetype("impact.ttf", size=25)
    (black, white) = ((0, 0, 0), (255, 255, 255))

    pos = (10, 10)
    offset = 40
    margin = 5
    draw = ImageDraw.Draw(img)
    wrapped = textwrap.wrap(joke, width=50)

    for i in range(len(wrapped)):
        (x, y) = (pos[0], pos[1] + offset * i)
        (left, top, right, bottom) = draw.textbbox((x, y), wrapped[i], font=font)
        draw.rectangle((left - margin, top - margin, right + margin, bottom + margin), fill = black)
        draw.text((x, y), wrapped[i], font=font, fill = white)
    
    return img

def run(_: list[str]) -> None:
    random.seed()
    prepare()

    with open(__data__, 'r') as r_json:
        data = json.loads(r_json.read())

    joke = random.choice(data["jokes"])
    hex_data = random.choice(data["images"])
    img = create_image(joke, hex_data)
    img.save(__location__ / "chuck_norris.jpg")
    print(__location__ / "chuck_norris.jpg")

    # with open(__location__ / "result.jpg", 'rb') as r_bin:
    #     data = r_bin.read().hex()
    # post_data = {
    #     "image": codecs.encode(codecs.decode(data, "hex"), "base64").decode(),
    #     "title": "chuck_norris",
    # }
    # req = request.Request("https://api.imgur.com/3/image", data = parse.urlencode(post_data).encode())
    # resp = request.urlopen(req)
    # print(resp)

    # for _ in range(10):
    #     joke = random.choice(data["jokes"])
    #     hex_data = random.choice(data["images"])
    #     img = create_image(joke, hex_data)
        # img.save(__results__ / f"{uuid.uuid4()}.jpg")
        # img.show()

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])