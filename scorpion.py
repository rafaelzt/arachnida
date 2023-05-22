# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    scorpion.py                                        :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: rzamolo- <rzamolo-@student.42.fr>          +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/05/20 15:56:50 by rzamolo-          #+#    #+#              #
#    Updated: 2023/05/22 21:06:41 by rzamolo-         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

from exiftool import ExifTool  # Import the ExifTool class from the exiftool module
import argparse  # Import the argparse module for command-line argument parsing
import glob  # Import the glob module for file pattern matching

def read_metadata(file):
    with ExifTool() as file_data:  # Create an instance of ExifTool and ensure proper cleanup
        try:
            # Retrieve metadata in JSON format using the execute_json method
            metadata = file_data.execute_json('-G', '-j', file)
            for item in metadata:  # Iterate over each metadata item
                for tag, value in item.items():  # Iterate over each tag-value pair
                    if isinstance(value, list):  # Check if the value is a list
                        value_str = ", ".join(str(v) for v in value)  # Join list elements into a string
                        print("{}:\t{:^50}".format(tag, value_str))  # Print formatted tag and value
                    else:
                        print("{}:\t{:^50}".format(tag, value))  # Print formatted tag and value
        except Exception as e:  # Handle exceptions
            print(f">> ERROR: Reading file tag - {str(e)}")  # Print error message

def remove_metadata(file, tags="all"):
    with ExifTool() as file_data:  # Create an instance of ExifTool and ensure proper cleanup
        if tags == "all":  # Check if all tags should be removed
            file_data.execute("-all=", file)  # Execute exiftool command to remove all metadata
            print(">> Removed all tags")  # Print message indicating all tags have been removed
        else:
            for tag in tags:  # Iterate over specified tags
                file_data.execute("-{}=".format(tag), file)  # Execute exiftool command to remove specific tag
                print(">> Removed tag", tag)  # Print message indicating the removed tag

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Read or remove metadata from an image')
    parser.add_argument('image', nargs='+', help='image names or wildcard patterns')
    parser.add_argument('-r', '--remove', dest="remove", action='store_true', help='Remove metadata')
    parser.add_argument('-t', '--tags', metavar="[TAGS]", dest='tags', type=str, default="all", help='Tags to remove (default all)')
    args = parser.parse_args()

    image_files = []
    for pattern in args.image:  # Iterate over image file patterns
        image_files.extend(glob.glob(pattern))  # Use glob to find files matching the patterns

    if args.remove:  # Check if metadata removal is requested
        for image_file in image_files:  # Iterate over the found image files
            print("-> Removing metadata from", image_file)
            remove_metadata(image_file, args.tags)  # Remove metadata from the file
    else:
        for image_file in image_files:  # Iterate over the found image files
            print("-> Reading metadata from", image_file)
            read_metadata(image_file)  # Read and print metadata from the file
