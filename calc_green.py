from matplotlib import image
import numpy as np
import os

Files = os.listdir("./data_2")
current_directory = os.getcwd()
os.chdir(current_directory+"/data_2")
n = len(Files)
Y = np.zeros(n)
X = []
i = 0
top_pixels_to_be_removed = 50
min_bottom_pixel = 480

def get_all(arr):
    pixel_list = []
    height, width = arr.shape[0], arr.shape[1]
    for i in range(height):
        for j in range(width):
            pixel = arr[i, j]
            pixel_list.append(pixel)
    return pixel_list

for filename in Files:
    arr = np.array(image.imread(filename))
    lst = get_all(arr[0][:50])
    if sum(lst) > 20000:
        Y[i] = 1
    X.append(arr[top_pixels_to_be_removed:min_bottom_pixel,:,:])
    #takes pixel rows between top_pixels_to_be_removed and min_bottom_pixel
    #of pixels eliminates the part of the image that includes the tag for good or not and the number written on the page
    i+=1

print("X and Y data in arrays")

def distance(pixel,background_pixel):
    #vals and standard have to be lists of lenth 3
    #nonstandard distance formula
    return abs(sum(pixel-background_pixel))

def get_list(arr, tolerance, background):
    #puts relevant pixels from arr (a np array) into a list that it returns
    #background has to be an np array
    pixel_list = []
    height,width = arr.shape[0],arr.shape[1]
    for i in range(height):
        for j in range(width):
            pixel = arr[i,j]
            if distance(pixel,background) > tolerance:
                pixel_list.append(pixel)
    return pixel_list

def average(vals):
    #vals should be list of pixel np array with one RGB list for each pixel
    #average returns the average RGB values in the list that is inputted
    totals = np.zeros(len(vals[0]))
    for val in vals:
        totals = totals + val
    return totals/len(vals)

i = 0
lists = []
background = np.array([250,250,250])
for arr in X:
    lst = get_list(arr,25,background)
    lists.append(lst)
    i+=1
    print("Finished", i, "lists")

def calculate_green_percentage(pixel_list):
    n = len(pixel_list)
    greens_n = 0
    for pixel in pixel_list:
        if (pixel[1] - max(pixel)) > -30:
            #if green color is close to the most dominant of red, green and blue
            greens_n += 1
    if greens_n:
        return float(greens_n) / float(n)
    else:
        return 0

percentage_list = []

i = 0
for lst in lists:
    i+=1
    percentage_list.append(calculate_green_percentage(lst))
    print("Finished",i,"ratio_list elements")

print(ratio_list)
good_percent_list = []
bad_percent_list = []
for i in range(n):
    if Y[i]:
        good_percent_list.append(percentage_list[i])
    else:
        bad_percent_list.append(percentage_list[i])