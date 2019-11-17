import numpy as np
from PIL import Image

#filename = input("What is image filename? ")
filename = "seeds1.jpg"

img = Image.open(filename)
arr = np.array(img)

def distance(pixel,standard_pixel):
    #vals and standard have to be lists of lenth 3
    #nonstandard distance formula
    return sum([abs(pixel[i]-standard_pixel[i]) for i in range(3)])


def get_list(arr, tolerance, standard):
    #automatically removes irrelevant pixels
    #in actual system, the box should have a white floor because black is a color
    #that could be part of the mustard seed sample
    pixel_list = []
    height,width = arr.shape[0],arr.shape[1]
    for i in range(height):
        for j in range(width):
            pixel = arr[i,j]
            if distance(pixel,standard) < tolerance:
                pixel_list.append(pixel)
    return pixel_list

def average(vals):
    #vals should be list of RGB lists with one RGB list for each pixel
    #average returns the average RGB values in the list that is inputted
    reds = []
    greens = []
    blues = []
    for pixel in vals:
        reds.append(pixel[0])
        greens.append(pixel[1])
        blues.append(pixel[2])
    l=len(reds)
    return [sum(reds)//l,sum(greens)//l,sum(blues)//l]

def create_color_image(color,name_of_image):
    #color is a three element list which is an RGB color.
    #name_of_image is a name with no file extension
    row = [color for _ in range(10)]
    all_rows = [row for _ in range(10)]
    array = np.array(all_rows, dtype=np.uint8)
    new_image = Image.fromarray(array)
    new_image.save(name_of_image+'.png')

def calculate_ratios(pixel_list,colors):
    #colors is a list of RGB values. It can be of any length (can calculate ratios for
    #any number of colors)
    ratios = np.zeros(len(colors))
    y = [i for i in range(len(colors))]
    for pixel in pixel_list:
        find_dist = lambda x: distance(pixel,colors[x])
        ratios[min(y,key=find_dist)] += 1
    return ratios/len(pixel_list)

standard_colors = [[246,202,79],[60,145,47],[122,67,54]]
print("Standard Colors RGB Values:")
print("Yellow, Green, Brown")
print(standard_colors)

pixel_list = get_list(arr,200,standard_colors[0])
print("Got pixel_list")
ratios = calculate_ratios(pixel_list,standard_colors)
print("Ratios")
print(ratios)
