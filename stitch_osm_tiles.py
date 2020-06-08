import argparse
import os
import sys
import time
import xmltodict

from glob import glob
from pathlib import Path
from PIL import Image

suffix = "_new"


def is_contain_png(path):
    for sub in Path(path).rglob('*.png'):
        return True
    return False


def is_contain_dir(path):
    dirs = [name for name in os.listdir(path) if os.path.isdir(os.path.join(path, name))]
    if len(dirs) > 0:
        return True
    return False


def scan_dir_self():
    dirs = [name for name in os.listdir('.') if os.path.isdir(os.path.join('.', name))]
    for sub_dir in dirs:
        if is_contain_png(sub_dir):
            if not os.path.exists(sub_dir + suffix):
                os.mkdir(sub_dir + suffix)

            sub_dirs = [name for name in os.listdir(sub_dir) if os.path.isdir(os.path.join(sub_dir, name))]
            for sub in sub_dirs:
                new_dirname = sub_dir + suffix + '/' + os.path.basename(sub)
                if not os.path.exists(new_dirname):
                    os.mkdir(new_dirname)
                scan_dir_h(sub_dir + '/' + sub, new_dirname)


def scan_dir(dirname):
    if is_contain_png(dirname):
        if not os.path.exists(dirname + suffix):
            os.mkdir(dirname + suffix)

        dirs = [name for name in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, name))]
        for sub_dir in dirs:
            if is_contain_png(dirname + '/' + sub_dir):
                if not os.path.exists(dirname + suffix + '/' + sub_dir):
                    os.mkdir(dirname + suffix + '/' + sub_dir)
                scan_dir_h(dirname + '/' + sub_dir, dirname + suffix + '/' + sub_dir)


def scan_dir_h(dirname, newname):
    dirs = [name for name in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, name))]
    if len(dirs) > 0:
        for sub_dir in dirs:
            new_dirname = newname + '/' + os.path.basename(sub_dir)
            if is_contain_dir(dirname + '/' + sub_dir):
                if not os.path.exists(new_dirname):
                    os.mkdir(new_dirname)
                scan_dir_v(dirname + '/' + sub_dir, new_dirname)

                img_names = []
                images = []
                for img_name in glob(new_dirname + '/*.png'):
                    img_name = os.path.basename(img_name)

                    img_names.append(img_name[:-4])

                img_names.sort(key=int)

                for img_name in img_names:
                    print(new_dirname, img_name + '.png')

                    images.append(Image.open(new_dirname + '/' + img_name + '.png'))

                if len(images) > 0:
                    get_concat_h(images).save(new_dirname + '.png')


def scan_dir_v(dirname, newname):
    dirs = [name for name in os.listdir(dirname) if os.path.isdir(os.path.join(dirname, name))]

    if len(dirs) > 0:
        for sub_dir in dirs:
            new_dirname = newname + '/' + os.path.basename(sub_dir)

            img_names = []
            images = []
            for img_name in glob(dirname + '/' + sub_dir + '/*.png'):
                img_name = os.path.basename(img_name)

                img_names.append(img_name[:-4])

            img_names.sort(key=int)

            for img_name in img_names:
                print(dirname + '/' + sub_dir, img_name + '.png')

                images.append(Image.open(dirname + '/' + sub_dir + '/' + img_name + '.png'))

            if len(images) > 0:
                get_concat_v(images).save(new_dirname + '.png')


def get_concat_h(im_list):
    total_width = sum(im.width for im in im_list)
    max_height = max(im.height for im in im_list)

    dst = Image.new('RGB', (total_width, max_height))

    pos_x = 0
    for im in im_list:
        dst.paste(im, (pos_x, 0))
        pos_x += im.width
    return dst


def get_concat_v(im_list):
    max_width = max(im.width for im in im_list)
    total_height = sum(im.height for im in im_list)

    dst = Image.new('RGB', (max_width, total_height))

    pos_y = 0
    for im in im_list:
        dst.paste(im, (0, pos_y))
        pos_y += im.height
    return dst


def read_xml(xmlname):
    keys = []
    with open(xmlname) as fd:
        doc = xmltodict.parse(fd.read())

        for contents in doc:
            if isinstance(doc[contents], dict):
                for content in doc[contents]:
                    if isinstance(doc[contents][content], list):
                        for item in doc[contents][content]:
                            # print([item['Key'], item['Size']])
                            keys.append([item['Key'], item['Size']])
                    elif isinstance(doc[contents][content], dict):
                        for item in doc[contents][content]:
                            print(doc[contents][content][item])
                    else:
                        # print(content)
                        pass
            else:
                # print(contents)
                pass

    return keys


def main():
    parser = argparse.ArgumentParser()

    parser.add_argument('--dirname', action='store', dest='dirname', help='Input osm tiles directory name', required=False)
    #parser.add_argument('--input', action='store', dest='input', help='Input xml file name', required=False)

    args = parser.parse_args()

    # if args.input is None:
    #     args.input = "download.xml"
    # keys = read_xml(args.input)
    # print(keys)

    if args.dirname is None:
        scan_dir_self()
    else:
        scan_dir(args.dirname)


if __name__ == '__main__':
    print("Start! : " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    start = time.time()

    main()

    print("End! : " + time.strftime("%Y-%m-%d %H:%M:%S", time.gmtime()))
    end = time.time()

    t = end - start
    hours = int(t / 3600)
    minutes = int(t / 60) % 60
    seconds = int(t) % 60

    print('Wested Time %02d:%02d:%02d' % (hours, minutes, seconds))