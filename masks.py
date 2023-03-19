import cv2
import numpy as np

"""
This module takes an image and generates its countours and the mask in black and white only.

I used it to convert the original mask images into black and white images.
After removing the background using a seperate photo editor, masks worked very well. 
"""

PATH = "Assets\Images/Borders/Originals"

# Asset Definitions - Scene Masks
#image = cv2.imread(PATH + "scene_1_mask_left_pl.png",cv2.IMREAD_UNCHANGED)
image = cv2.imread(PATH + "scene_1_mask_right_rbt.png",cv2.IMREAD_UNCHANGED)

# convert image to grayscale
image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# convert image to black and white
thresh, image_edges = cv2.threshold(image_gray, 100, 255, cv2.THRESH_BINARY)

# create canvas
canvas = np.zeros(image.shape, np.uint8)
canvas.fill(255)

# create background mask
mask = np.zeros(image.shape, np.uint8)
mask.fill(255)

# create new background
new_background = np.zeros(image.shape, np.uint8)
new_background.fill(255)

# get all contours
contours_draw, hierachy = cv2.findContours(image_edges, cv2.RETR_LIST, cv2.CHAIN_APPROX_NONE)

# get most significant contours
contours_mask, hierachy = cv2.findContours(image_edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

# contours traversal
for contour in range(len(contours_draw)):
    # draw current contour
    cv2.drawContours(canvas, contours_draw, contour, (0, 0, 0))

# most significant contours traversal
for contour in range(len(contours_draw)):
    # create mask
    if contour != 1:
        cv2.fillConvexPoly(mask, contours_mask[contour], (0, 0, 0))

    # create background
    if contour != 1:
        cv2.fillConvexPoly(new_background, contours_mask[contour], (0, 255, 0))

cv2.imshow("original", image)
cv2.imshow("Black and white",image_edges)
cv2.imshow("Contours", canvas)

#cv2.imwrite(PATH + "scene_1_mask_right_pl_contours.png", canvas)
#cv2.imwrite(PATH + "scene_1_mask_right_pl_bw.png", image_edges)

#cv2.imwrite(PATH + "scene_1_mask_left_rbt_contours.png", canvas)
cv2.imwrite(PATH + "scene_1_mask_right_rbt_bw.png", image_edges)

cv2.waitKey(0)

cv2.destroyAllWindows()