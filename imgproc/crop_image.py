import cv2
import numpy as np
 
img = cv2.imread('data/training_images/img_1.jpg')
print(img.shape) # Print image shape
cv2.imshow("original", img)
 
# Cropping an image [y,x]
cropped_image = img[900:1253, 693:777]
 
# Display cropped image
cv2.imshow("cropped", cropped_image)
 
# Save the cropped image
cv2.imwrite("imgproc/crop_image.jpg", cropped_image)