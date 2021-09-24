from PIL import Image
import string
from django.conf import settings


def image_compress(path: string, resolution: dict = (326, 326)):
    if path and resolution:
        image_path = f'{settings.MEDIA_ROOT}/{path}'
        image = Image.open(image_path)
        image = image.resize(resolution)
        image.save(image_path, quantity=100, optimize=True)

