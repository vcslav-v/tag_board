import os
import zipfile

import tinify

from tags_agr import RESULT_FOLDER_RESIZE, UPLOAD_FOLDER_RESIZE

tinify.key = os.environ.get('TINIFY_KEY')


def uploaded_files():
    for img_file in os.listdir(UPLOAD_FOLDER_RESIZE):
        yield img_file
        os.remove(os.path.join(UPLOAD_FOLDER_RESIZE, img_file))


def run(resize_width=None):
    resize_width = int(resize_width) if resize_width and resize_width.isdecimal() else None
    if os.path.exists('tiny_result.zip'):
        os.remove('tiny_result.zip')
    if not os.path.isdir(RESULT_FOLDER_RESIZE):
        os.mkdir(RESULT_FOLDER_RESIZE)
    for img_file_name in uploaded_files():
        img_path = os.path.join(UPLOAD_FOLDER_RESIZE, img_file_name)
        result_img_path = os.path.join(RESULT_FOLDER_RESIZE, img_file_name)
        source = tinify.from_file(img_path)
        if not resize_width:
            source.to_file(result_img_path)
            continue
        resized = source.resize(
            method='scale',
            width=resize_width,
        )
        resized.to_file(result_img_path)
    if os.listdir(RESULT_FOLDER_RESIZE):
        with zipfile.ZipFile('tiny_result.zip', 'w') as result_zip:
            for img_file_name in os.listdir(RESULT_FOLDER_RESIZE):
                result_zip.write(os.path.join(RESULT_FOLDER_RESIZE, img_file_name))
        for img_file_name in os.listdir(RESULT_FOLDER_RESIZE):
            os.remove(os.path.join(RESULT_FOLDER_RESIZE, img_file_name))