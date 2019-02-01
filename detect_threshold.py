import cv2 as cv
import numpy as np
import os
import matplotlib.pyplot as plt

WITH_QT = True
try:
    cv.namedWindow("Test")
    cv.displayOverlay("Test", "Test QT", 10000)
except:
    WITH_QT = False
cv.destroyAllWindows()

threshold_value = 170
max_binary_value = 255
window_name = "Detect by threshold"
trackbar_image = "Image"

def change_image_index(x):
    global img_index, img
    img_index = x
    img_path = image_list[img_index]
    img = cv.imread(img_path)
    if WITH_QT:
        cv.displayOverlay(window_name, "Showing image "
                                    "" + str(img_index) + "/"
                                    "" + str(last_img_index), 1000)
    else:
        print("Showing image "
                "" + str(img_index) + "/"
                "" + str(last_img_index) + " path:" + img_path)

def threshold(img_path):
	img = cv.imread(img_path)
	blur = cv.blur(img,(5,5))
	img_gray = cv.cvtColor(blur, cv.COLOR_BGR2GRAY)

	retval, threshold = cv.threshold(img_gray, threshold_value, max_binary_value, cv.THRESH_BINARY)
	average = threshold.mean(axis=0).mean(axis=0)
	cv.imshow(window_name, threshold)
	write_message(img, average)
	return average

def write_message(img, average):
	font                   = cv.FONT_HERSHEY_SIMPLEX
	bottomLeftCornerOfText = (10,230)
	topLeftCornerOfText	   = (10, 20)
	fontScale              = 1
	fontScale_2			   = 0.75
	fontColor              = (0, 0, 255)
	lineType               = 2

	cv.putText(img, str(round(average)), topLeftCornerOfText, font, fontScale_2,fontColor, lineType)

	if average < 175:
		cv.putText(img, "Small", bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
		cv.imshow("original",img)
	else:
		cv.putText(img, "Big", bottomLeftCornerOfText, font, fontScale, fontColor, lineType)
		cv.imshow("original",img)

def decrease_index(current_index, last_index):
    current_index -= 1
    if current_index < 0:
        current_index = last_index
    return current_index


def increase_index(current_index, last_index):
    current_index += 1
    if current_index > last_index:
        current_index = 0
    return current_index

img_dir = "hexagon2/"
image_list = []
for f in os.listdir(img_dir):
    f_path = os.path.join(img_dir, f)
    test_img = cv.imread(f_path)
    if test_img is not None:
        image_list.append(f_path)

last_img_index = len(image_list) - 1
print(image_list)

cv.namedWindow(window_name)
cv.resizeWindow(window_name,500, 500)
cv.createTrackbar(trackbar_image, window_name, 0, last_img_index, change_image_index)

change_image_index(0)

average_list = []
class_list = []

for i in range(0, len(image_list) - 1):
	average = threshold(image_list[i])
	average_list.append(average)
	if average < 170:
		class_list.append(0)
	else:
		class_list.append(1)

plt.plot(average_list, class_list, 'ro')
plt.xlabel('average color')
plt.ylabel('Class(0 = small, 1 = big)')
plt.show()


while True:
	img_path = image_list[img_index]

	pressed_key = cv.waitKey(50)
	threshold(img_path)

	if pressed_key == ord('a') or pressed_key == ord('d'):
        # show previous image key listener
		if pressed_key == ord('a'):
		    img_index = decrease_index(img_index, last_img_index)
		# show next image key listener
		elif pressed_key == ord('d'):
		    img_index = increase_index(img_index, last_img_index)
		cv.setTrackbarPos(trackbar_image, window_name, img_index)

	elif pressed_key == ord('q'):
		break

	if WITH_QT:
	# if window gets closed then quit
		if cv.getWindowProperty(window_name,cv.WND_PROP_VISIBLE) < 1:
		    break
cv.destroyAllWindows()