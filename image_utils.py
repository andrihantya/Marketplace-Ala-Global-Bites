import base64
import io
from PIL import Image

def save_image_from_base64(base64_string, filename):
    """Simpan gambar dari string base64 ke file."""
    image_data = base64.b64decode(base64_string)
    image = Image.open(io.BytesIO(image_data))
    image.save(filename)

def encode_image_to_base64(filename):
    """Encode gambar ke dalam string base64."""
    with open(filename, "rb") as image_file:
        image_data = image_file.read()
    base64_string = base64.b64encode(image_data).decode("utf-8")
    return base64_string
