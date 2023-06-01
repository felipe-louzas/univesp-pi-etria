from PIL import Image
import io

class UnsupportedFileTypeError(Exception):
    pass

def make_preview(file_type: str, file_bytes: bytes):
    if file_type.startswith('image/'):
        return _make_image_preview(file_type, file_bytes)
    else:
        raise UnsupportedFileTypeError(file_type)

def _make_image_preview(file_type, file_bytes):
    img = Image.open(io.BytesIO(file_bytes))
    img.thumbnail((380, 200))
    img_bytes = io.BytesIO()
    img.save(img_bytes, format='jpeg')
    return img_bytes.getvalue()