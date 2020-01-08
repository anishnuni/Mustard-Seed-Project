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

def calculate_ratios(pixel_list,colors):
    #colors is a list of RGB values. It can be of any length (can calculate ratios for
    #any number of colors)
    ratios = np.zeros(len(colors))
    y = [i for i in range(len(colors))]
    for pixel in pixel_list:
        find_dist = lambda x: distance(pixel,colors[x])
        ratios[min(y,key=find_dist)] += 1
    return ratios/len(pixel_list)

standard_colors = [np.array([246,202,79]),np.array([204,204,0]),np.array([204,0,0]), np.array([204,102,0]),np.array([60,145,47]),np.array([122,67,54]),np.array([112,165,21]),np.array([0,153,76]),np.array([0,102,204])]

ratio_list = []
i = 0
for lst in lists:
    i+=1
    ratio_list.append(calculate_ratios(lst,standard_colors))
    print("Finished",i,"ratio_list elements")

print(ratio_list)
good_ratio_list = []
bad_ratio_list = []
for i in range(n):
    if Y[i]:
        good_ratio_list.append(ratio_list[i])
    else:
        bad_ratio_list.append(ratio_list[i])

from sklearn.svm import SVC
svclassifier = SVC(kernel='rbf')

X2 = np.zeros((36,len(standard_colors)))
for i in range(36):
    X2[i] = ratio_list[i]

svclassifier.fit(X2, Y)
y_pred = svclassifier.predict(X2)

from sklearn.metrics import classification_report, confusion_matrix
print(confusion_matrix(Y,y_pred))
print(classification_report(Y,y_pred))