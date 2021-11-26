from scipy.misc import imread

im1 = imread("highlight23.png")
im2 = imread("highlight25.png")
difference = im1 - im2
# distance is a W x H array indicating the pixelwise distance between images
distance = difference.astype(float)**2.
distance = distance.sum(axis=2)
print("Distance %s" % distance)
# distance is an array with a numbers between 0 and ~440
print(distance.sum())
if distance.sum() > 100:
    print("Movement detected !")
