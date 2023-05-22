# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/20 15:56:50 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/22 18:13:43 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
from exiftool import ExifTool
import argparse
import glob

def read_metadata(file):
    with ExifTool() as file_data:
        metadata = file_data.execute_json('-G', '-j', file)
        for item in metadata:
            try:
                for tag, value in item.items():
                    if isinstance(value, list):
                        value_str = ", ".join(str(v) for v in value)
                        print("{:<40}:\t{:<30}".format(tag, value_str))
                    else:
                        print("{:<40}:\t{:<30}".format(tag, value))
            except:
                print(">> ERROR: Reading file tag")

def remove_metadata(file, tags="all"):
    with ExifTool() as file_data:
        if tags == "all":
            file_data.execute("-all=", file)
            print(">> Removed all tags")
        else:
            for tag in tags:
                file_data.execute("-{}=".format(tag), file)
                print(">> Removed tag", tag)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read or remove metadata from an image')
    parser.add_argument('image', nargs='+', help='image names or wildcard patterns')
    parser.add_argument('-r', '--remove', dest="remove", action='store_true', help='Remove metadata')
    parser.add_argument('-t', '--tags', metavar="[TAGS]", dest='tags', type=str, default="all", help='Tags to remove (default all)')
    args = parser.parse_args()

    image_files = []
    for pattern in args.image:
        image_files.extend(glob.glob(pattern))

    if args.remove:
        for image_file in image_files:
            print("-> Removing metadata from", image_file)
            remove_metadata(image_file, args.tags)
    else:
        for image_file in image_files:
            print("-> Reading metadata from", image_file)
            read_metadata(image_file)
