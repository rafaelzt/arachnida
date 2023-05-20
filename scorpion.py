# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/20 15:56:50 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/20 16:04:28 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import exiftool

def read_metadata(file):
    with exiftool.ExifToolHelper() as file_data:
        metadata = file_data.get_metadata(file)
        for item in metadata:
            for tag, value in item.items():
                print("{:<40}:\t{:<30}".format(tag, value))

def remove_metadata(file, tags):
    with ExifTool() as file_data:
        file_data.delete_tags(file, tags)


if __name__ == "__main__":
    # for item in sys.argv[1:]:
    #     print("\n->", item)
    #     try:
    #         meta = read_metadata(item)
    #     except:
    #         print("ERROR: Image name")
    read_metadata("42-lyon.jpg")