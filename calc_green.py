from matplotlib import image
from skimage.color import rgb2hsv
import numpy as np
import os
from PIL import Image

Files = os.listdir("./data_2")
current_directory = os.getcwd()
os.chdir(current_directory+"/data_2")
n = len(Files)
Y = np.zeros(n)
X_rgb = []
X_hsv = []
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
    if filename[-3:] =='JPG':
        img = image.imread(filename)
        hsv_img = rgb2hsv(img)
        arr = np.array(img)
        arr2 = np.array(hsv_img)
        lst = get_all(arr[0][:50])
        if sum(lst) > 20000:
            Y[i] = 1
        X_rgb.append(arr[top_pixels_to_be_removed:min_bottom_pixel,:,:])
        X_hsv.append(arr2[top_pixels_to_be_removed:min_bottom_pixel,:,:])
        #takes pixel rows between top_pixels_to_be_removed and min_bottom_pixel
        #of pixels eliminates the part of the image that includes the tag for good or not and the number written on the page
        i+=1

print("X, X_hsv, and Y data in arrays")

def distance(pixel,background_pixel):
    #vals and standard have to be lists of lenth 3
    #nonstandard distance formula
    return abs(sum(pixel-background_pixel))

def get_list(arr, arr2, tolerance, background):
    #puts relevant pixels from arr (a np array) into a list that it returns
    #background has to be an np array
    pixel_list = []
    height,width = arr.shape[0],arr.shape[1]
    total_pixels = height*width
    for i in range(height):
        for j in range(width):
            print(float(i*width+j) / float(total_pixels), "percent of list done")
            pixel = arr[i,j]
            hue,saturation = arr2[i,j][0]*360,arr2[i,j][1]
            if distance(pixel,background) > tolerance and saturation > 0.2 and hue < 165:
                pixel_list.append(pixel)
    return pixel_list

def average(vals):
    #vals should be list of pixel np array with one RGB list for each pixel
    #average returns the average RGB values in the list that is inputted
    totals = np.zeros(len(vals[0]))
    for val in vals:
        totals = totals + val
    return totals/len(vals)

lists = []
background = np.array([255,255,255])

for i in range(len(X_rgb)):
    lists.append(get_list(X_rgb[i],X_hsv[i],25,background))
    print(i+1, "pixel lists gotten")


print("Pixel lists have been found")
image_array = []
ln = len(lst)


def calculate_green_percentage(pixel_list,n2):
    n = len(pixel_list)
    greens_n = 0
    greens_n_strict = 0
    done = 0
    for pixel in pixel_list:
        done+=1
        if pixel[1]-pixel[0] > 20:
            #this formula only works in the yellow/green/brown areas (where these pixels are)
            greens_n_strict+=1
            greens_n+=1
        elif pixel[1]-pixel[0] > 10:
            #if green color is most dominant of red, green and blue
            greens_n += 1
        print("On",n2,"image; ",100*float(done)/n,"percent done")
    if greens_n:
        return float(greens_n) / float(n) , float(greens_n_strict) / float(n)
    else:
        return 0

percentage_list = []
strict_pl = []
for i in range(len(X_rgb)):
    normal,strict = calculate_green_percentage(lists[i],i+1)
    percentage_list.append(normal)
    strict_pl.append(strict)

good_percent_list = []
bad_percent_list = []
for i in range(len(Y)):
    if Y[i]:
        good_percent_list.append(strict_pl[i])
    else:
        bad_percent_list.append(strict_pl[i])

good_avg_grn = sum(good_percent_list) / len(good_percent_list)
bad_avg_grn = sum(bad_percent_list) / len(bad_percent_list)
print("average green among good images:",good_avg_grn)
print("average green among bad images:",bad_avg_grn)
