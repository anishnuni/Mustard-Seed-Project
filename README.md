# Mustard-Seed-Project
Tools for mustard seed purchasing and accurately estimating the quality of mustard seeds based on an image

Things Tested:
Checked if there was any significant difference in the average color between good and bad samples. It turns out that there was not.
The average RGB pixel values for the good images was [183.0, 197.0, 191.0] while the 
average RGB pixel values for the bad images was [187.0, 200.0, 192.0] (the average value was found using floor division).
Also, for all the images, pixels that were less than 25 away in absolute distance from 
250,250,250 were removed, as these were likely a part of the white background and not part of the mustard sample.

Also looked at ratio of green, brown, and yellow pixels in the good images and bad images.
On average, good and bad mustard seeds have the pretty similar ratios of green, brown and yellow.
Average Ratio for good samples: [0.8948526111378393, 0.08891013899404458, 0.016237249868116112]
Average Ratio for bad samples: [0.8951194226072755, 0.09114753044779142, 0.013733046944932903]
In this order: (yellow, green, brown)
（standard colors for yellow, green and brown: standard_colors = [np.array([246,202,79]),np.array([60,145,47]),np.array([122,67,54])]_
Quickly tried training SVM on just the overall ratio of each color in each image. It did not work.
Looks like it will require a higher level of detail than three numbers for each sample, as seen because neither average
nor ratios seems to get good results. 

