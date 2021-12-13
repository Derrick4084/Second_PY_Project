from PIL import Image
import glob

# print(glob.glob("PNG/**/*.png", recursive=True))

print(glob.glob("PNG/*.png"))

for file in glob.glob("PNG/*.png"):
    im = Image.open(file)
    im_rgb = im.convert("RGB")

    im_rgb.save(file.replace("png", "jpg"), quality=95)
