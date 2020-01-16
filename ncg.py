from matplotlib import image
from skimage.color import rgb2hsv
import numpy as np
import os
from PIL import Image

Files = os.listdir("./Scaled_down_images")
current_directory = os.getcwd()
os.chdir(current_directory+"/Scaled_down_images")
n = len(Files)
X_rgb = []
i = 0
top_pixels_to_be_removed = 50
min_bottom_pixel = 480


for filename in Files:
    if filename[-3:] =='JPG':
        img = image.imread(filename)
        hsv_img = rgb2hsv(img)
        arr = np.array(img)
        X_rgb.append(arr[top_pixels_to_be_removed:min_bottom_pixel,:,:])
        #takes pixel rows between top_pixels_to_be_removed and min_bottom_pixel
        #of pixels eliminates the part of the image that includes the tag for good or not and the number written on the page
        i+=1

print("X data in arrays")

def distance(pixel,background_pixel):
    #vals and standard have to be lists of lenth 3
    #nonstandard distance formula
    return abs(sum(pixel-background_pixel))

background = np.array([255,255,255])

def hue_calc(pixel):
    #pixel is a list
    a = max(pixel)
    i = min(pixel)
    diff = (a - i)
    if diff == 0:
        diff = 1
    if pixel.index(a) == 1:
        return 60*(2 + (pixel[2]-pixel[0]) / diff)
    elif pixel.index(a) == 0:
        return 60*((pixel[1]-pixel[2]) / diff)
    else:
        return 60 * (4 + (pixel[0]-pixel[1]) / diff)

def saturation_calc(pixel):
    if max(pixel):
        return (max(pixel) - min(pixel)) / max(pixel)
    else:
        return 0

def calculate_green_percentage(arr, tolerance, background,n):
    #ONLY WORKS WHEN SAMPLE IS IN CENTER OF PAGE----REMOVE STREAK RETURN IF OTHERWISE
    streak = 0
    n_of_relevant_pixels = 0
    n_green_pixels = 0
    height, width = arr.shape[0], arr.shape[1]
    total_pixels = height*width
    for i in range(height):
        for j in range(width):
            if n_green_pixels > 100 and streak > width:
                return n_green_pixels/(n_of_relevant_pixels+1)
            pixel = arr[i, j]
            pixel2 = [int(pixel[0])/255, int(pixel[1])/255, int(pixel[2])/255]
            hue, saturation, value = hue_calc(pixel2), saturation_calc(pixel2), max(pixel2)
            print("On image", n, ":",100*float(i * width + j) / float(total_pixels), "percent done", " | ","Current Green %: ", 100*n_green_pixels/(n_of_relevant_pixels+1))
            if distance(pixel, background) > tolerance and saturation > 0.1 and hue < 150:
                streak = 0
                n_of_relevant_pixels+=1
                if (hue > 53 or (hue > 47 and value < 0.65)) and saturation > 0.3:
                    n_green_pixels += 1
            else:
                streak+=1
    return n_green_pixels/(n_of_relevant_pixels+1)


percentage_list = []

for i in range(len(X_rgb)):
    normal = calculate_green_percentage(X_rgb[i],20,background,i+1)
    percentage_list.append(normal)

good = ['DSC_0080.JPG','DSC_0097.JPG','DSC_0101.JPG','DSC_0105.JPG','DSC_0108.JPG','DSC_0111.JPG']

good_percent_list = []
bad_percent_list = []
i = -1
for filename in Files:
    i+=1
    if filename in good:
        good_percent_list.append(percentage_list[i])
    else:
        bad_percent_list.append(percentage_list[i])

good_avg_grn = sum(good_percent_list) / len(good_percent_list)
bad_avg_grn = sum(bad_percent_list) / len(bad_percent_list)
print("average green among good images:",good_avg_grn)
print("average green among bad images:",bad_avg_grn)

results = {}
i = 0
for filename in Files:
    results[filename] = percentage_list[i]
    i+=1

results_good = {}
results_bad = {}
i = -1
for filename in Files:
    i+=1
    if filename in good:
        results_good[filename] = percentage_list[i]
    else:
        results_bad[filename] = percentage_list[i]
