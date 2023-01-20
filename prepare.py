#!/usr/bin/python3
import pathlib, os, warnings, json, uuid, shutil, imgbbpy, re
from PIL import Image
__location__ = pathlib.Path(__file__).parent.resolve()
__source__ = __location__ / "source_images"
__resized__ = __location__ / "resized_images"
warnings.filterwarnings("ignore", category=DeprecationWarning)

def resize_image(image_path: str, quality: int = 90, width: int = 400, height: int = 300) -> pathlib.Path:
    img = Image.open(image_path)

    img = img.resize((width, height), Image.ANTIALIAS)
    file_name, _ = os.path.splitext(image_path)
    new_path = __resized__ / f"{os.path.basename(file_name)}.jpg"

    img.save(new_path, quality=quality, optimize=True)

    return new_path

def run(_: list[str]) -> None:
    if os.path.exists(__resized__):
        shutil.rmtree(__resized__)
    __resized__.mkdir(parents=True, exist_ok=True)

    with open(__location__ / "config.json", 'r', encoding="utf-8") as r_json:
        cfg = json.loads(r_json.read())

    for file in pathlib.Path(__source__).glob('*.jpg'):
        _ = resize_image(file)

    img_urls = []
    client = imgbbpy.SyncClient(cfg["api_key"])
    for file in pathlib.Path(__resized__).glob("*.jpg"):
        rgx = re.compile(r"https://[\w\.]+/([\w+\/-]+)")
        url = rgx.match(client.upload(file=file, name=uuid.uuid4()).url).group(1)

        img_urls.append(url)
    cfg["image_urls"] = img_urls

    with open(__location__ / "config.json", 'w', encoding='utf-8') as w_json:
        w_json.write(json.dumps(cfg, indent=4))

    with open(__location__ / "template.py", 'r', encoding="utf-8") as r_py:
        formatted = r_py.read().format(json.dumps(cfg, indent=4))
    
    with open(__location__ / "chuck_norris.py", 'w', encoding="utf-8") as w_py:
        w_py.write(formatted)

    shutil.rmtree(__resized__)

if __name__ == "__main__":
    import sys
    run(sys.argv[1:])