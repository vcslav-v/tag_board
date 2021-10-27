import os
from PIL import Image
from tags_agr import UPLOAD_FOLDER_LONG


def flush_upload():
    for img_file in os.listdir(UPLOAD_FOLDER_LONG):
        os.remove(os.path.join(UPLOAD_FOLDER_LONG, img_file))


def run():
    list_dir = os.listdir(UPLOAD_FOLDER_LONG)
    list_dir = sorted(list_dir)

    with Image.open(list_dir[0]) as first_img:
        wide, high = first_img.size

    for img_file_path in list_dir[1:]:
        with Image.open(img_file_path) as temp_img:
            high += temp_img.size[1]

    result_img = Image.new('RGB', (wide, high))
    point_high = 0
    for img_file_path in list_dir:
        with Image.open(img_file_path) as temp_img:
            result_img.paste(temp_img, (0, point_high))
            point_high += temp_img.size[1]

    result_img.save('long_result.jpg')
    flush_upload()
