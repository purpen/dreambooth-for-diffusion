import os
import shutil
import argparse
import operator
from PIL import Image


def fixed_files(path):
    """
    修正图片文件数据
    Args:
        path:

    Returns:

    """
    image_list = os.listdir(path)
    for image in image_list:
        # 如为目录
        if os.path.isdir(image):
            fixed_files(os.path.join(path, image))
            continue
        # 如为文件
        _rename_file(path, image)


def _rename_file(path, name):
    """
    修改目标文件名称
    Args:
        path: 目录路径
        name: 目录名称
    Returns:
    """
    if operator.contains(name, "Guide的副本"):
        new_name = name.replace("Guide的副本", "")
        new_name = new_name.replace("-", "")
        print("目录新名称：" + os.path.join(path, new_name))
        os.rename(os.path.join(path, name), os.path.join(path, new_name))


def convert_tiff2png(path):
    """
    tiff格式转换成png
    """
    for image in os.listdir(path):
        if os.path.isdir(os.path.join(path, image)):
            convert_tiff2png(os.path.join(path, image))
            continue

        if os.path.splitext(os.path.join(path, image))[1].lower() != ".tiff":
            continue

        jpg_path = os.path.join(path, "jpg")
        if not os.path.exists(jpg_path):
            os.makedirs(jpg_path)

        out_image = os.path.join(jpg_path, os.path.splitext(image)[0] + ".jpg")
        try:
            im = Image.open(os.path.join(path, image))
            im.thumbnail(im.size)
            im.save(out_image, "JPEG", quality=100)
        except Exception as err:
            print(path + ":" + str(err))


def merge_images(input_path, out_path):
    """
    合并图片数据集
    """
    if not os.path.exists(out_path):
        os.makedirs(out_path)

    i = 0
    for image in os.listdir(input_path):
        i += 1
        if os.path.isdir(os.path.join(input_path, image)):
            merge_images(os.path.join(input_path, image), out_path)
            continue

        dir_name = input_path.split('/')[-1]
        out_image = os.path.join(out_path, f"{dir_name}-{i}.jpg")
        if os.path.splitext(image)[1].lower() == ".tiff":
            try:
                im = Image.open(os.path.join(input_path, image))
                im.thumbnail(im.size)
                im.save(out_image, "JPEG", quality=100)
            except Exception as err:
                print(input_path + ":" + str(err))
        else:
            shutil.copy(os.path.join(input_path, image), out_image)


def clear_tmpfiles(path):
    """
    清除临时文件
    Returns:
    """
    for image in os.listdir(path):
        if os.path.isfile(os.path.join(path, image)):
            print("skip: " + image)
            continue

        png_path = os.path.join(path, image, "png")
        if os.path.exists(png_path):
            shutil.rmtree(png_path, ignore_errors=True)

        jpg_path = os.path.join(path, image, "jpg")
        if os.path.exists(jpg_path):
            shutil.rmtree(jpg_path, ignore_errors=True)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="manual to this script")
    parser.add_argument("fn", type=str, default="merge")  # merge, fixed, clear
    parser.add_argument("origin_image_path", type=str, default=None)
    parser.add_argument("output_image_path", type=str, default=None)
    args = parser.parse_args()
    origin_image_path = args.origin_image_path
    output_image_path = args.output_image_path

    if args.fn == "merge":
        merge_images(origin_image_path, output_image_path)
    elif args.fn == "fixed":
        fixed_files(origin_image_path)
    else:
        clear_tmpfiles(origin_image_path)
