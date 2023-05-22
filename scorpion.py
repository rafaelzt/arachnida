# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/20 15:56:50 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/22 13:49:15 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import exiftool
import argparse

def read_metadata(file):
    with exiftool.ExifToolHelper() as file_data:
        metadata = file_data.get_metadata(file)
        for item in metadata:
            try:
                for tag, value in item.items():
                    print("{:<40}:\t{:<30}".format(tag, value))
            except:
                print(">> ERROR: Reading file tag")

def remove_metadata(file, tags):
    with ExifTool() as file_data:
        file_data.delete_tags(file, tags)


if __name__ == "__main__":
    
    for item in sys.argv[1:]:
        parser = argparse.ArgumentParser(description='Read or remove metadata from image')

        parser.add_argument('image',
                            help='image name')
        parser.add_argument('-r', '--remove',
                            dest="remove",
                            action='store_true',
                            help='Remove metadata')
        parser.add_argument('-t', '--tags',
                            metavar="[TAGS]",
                            dest='tags',
                            type=str,
                            default="all",
                            help='Tags to remove (default all)')
        args = parser.parse_args()
        if args.remove:
            print("-> Removing metadata from", item)
            remove_metadata(item, args.tags)
        else:        
            print("-> Reading metadata from", item)
            read_metadata(item)
        