# Importing libraries
import sys, random, argparse
import numpy as np
import math

# Allow us to manipulate images using Pillow library
from PIL import Image

# These string are used to represent differents level of grayscale
# Darker
gray_scale_1 = "$@B%8&WM#*oahkbdpqwmZO0QLCJUYXzcvunxrjft/\|()1{}[]?-_+~<>i!lI;:,\"^`'. "
# Lighter
gray_scale_2 = '@%#*+=-:. '

# Function that calculates the gray intensity of an image
def get_average_L(image):
    
    # Convert an image into an array
    img = np.array(image)

    # Extract the image size from its shape
    width, height = img.shape

    # Calculate the grayscale value intensity of the image
    return np.average(img.reshape(width * height))

# Function that converts the image into ASCII
def convert_image_to_ascii(file_name, columns, scale, darker_level):
    
    # Indicates that these variables are globals
    global gray_scale_1, gray_scale_2

    # Convert image to grayscale
    image = Image.open(file_name).convert('L')



    # Store image dimensions
    Width, Height = image.size[0], image.size[1]
    print("input image dimensions: %d x %d" % (Width, Height))

    # Calculates tiles dimension (width and height)
    width = Width / columns
    #height = Height / scale

    # compute the number of rows
    #rows = int(columns / Width)
    aspect_ratio = Width / Height

    desired_width = int(Width * scale)
    desired_height = int(desired_width / aspect_ratio)


    columns = desired_width
    #tile_height = int(desired_height / 50)
    tile_width = int(Width / columns)
    tile_height = int(tile_width / aspect_ratio)

    rows = int(Height / tile_height)


    print("columns: %d, rows: %d" % (columns,rows))
    print("tiles dimensions: %d x %d" % (tile_width, tile_height))

    # Checks if the image size is too small
    if columns > Width or rows > Height:
        print("The image is too small")
        exit(0)
    
    # Initialize and empty array to hold ASCII
    aimg = []

    # Create a loop through each row
    for j in range(rows):
        y1 = int( j * tile_height) #Calculate starting pixel row
        y2 = int((j + 1)*tile_height) #Calculate ending pixel row

        if j == rows - 1: # Check if this is the lats row
            y2 = Height # Correct the ending row for the last tile
        
        aimg.append("") # Append an empty string

        # Create a loop throught each column
        for i in range(columns):
            # Crop image
            x1 = int(i * width)
            x2 = int((i + 1) * width)

            # Correct the last tile
            if i == columns - 1:
                x2 = Width
            
            # Crop image to extract tile
            img = image.crop((i * tile_width, y1, (i + 1) * tile_width, y2))

            # Get average luminance
            average = int(get_average_L(img))

            if darker_level:
                gray_value = gray_scale_1[int((average * 69) / 255 )]
            else:
                gray_value = gray_scale_2[int((average * 9) / 255)]
            
            aimg[j] += gray_value
    
    #return text file
    return aimg

# Starting point of the program
def main():
    descStr = "This program converts an image into ASCII art."
    parser = argparse.ArgumentParser(description=descStr)

    # Add parameters to the ASCII art

    parser.add_argument('--file', dest='imgFile', required=True)
    parser.add_argument('--scale', dest='scale', required=False)
    parser.add_argument('--out', dest='outFile', required=False)
    parser.add_argument('--columns', dest='columns', required=False)
    parser.add_argument('--darkerlevels',dest='darker_level',action='store_true')

    args = parser.parse_args()
    imgFile = args.imgFile

    # Set output file
    outFile = "out.txt"
    if args.outFile:
        outFile = args.outFile

    # Set a default scale of 0.43
    scale = 0.43
    if args.scale:
        scale = float(args.scale)
    
    # Set columns
    columns = 80
    if args.columns:
        columns = int(args.columns)
    
    print("Generating ASCII art...")

    # Convert image to ASCII txt file
    aimg = convert_image_to_ascii(imgFile, columns, scale, args.darker_level)

        # open file
    f = open(outFile, 'w')

    # write to file
    for row in aimg:
        f.write(row + '\n')

    # cleanup
    f.close()
    print("ASCII art written to %s" % outFile)

# call main
if __name__ == '__main__':
    main()