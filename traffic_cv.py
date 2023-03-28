# Development of a traffic light control method based on a vision system

import cv2 as cv
import numpy as np
import time

print("Cross: 1")
# read the image file
print("1. Import and show image.")
img = cv.imread(f'cross.jpg', cv.IMREAD_UNCHANGED)
img_small = cv.resize(img, (960, 960))

# show image
cv.imshow("Cross", img_small)
cv.waitKey(500)
cv.destroyAllWindows()

# cut ROI  (230x900  [y1:y2,x1:x2])
print("2. Cut and show ROI.")
road_left = img[1235:1465, 15:915]
road_top  = img[15:915, 920:1150]
road_right = img[930:1160, 1490:2390]
road_down = img[1490:2390, 1245:1475]

cv.imwrite('road_left.png',road_left)

# show images
cv.imshow("road_left", road_left)
cv.imshow("road_right", road_right)
cv.imshow("road_top", road_top)
cv.imshow("road_down", road_down)
cv.waitKey(1000)
cv.destroyAllWindows()

# convert img to grey
print("3. Convert image from RGB to grayscale.")
road_left = cv.cvtColor(road_left,cv.COLOR_RGB2GRAY)
road_top = cv.cvtColor(road_top,cv.COLOR_RGB2GRAY)
road_right = cv.cvtColor(road_right,cv.COLOR_RGB2GRAY)
road_down = cv.cvtColor(road_down,cv.COLOR_RGB2GRAY)

cv.imwrite('road_left_gray.png',road_left)

# show images
cv.imshow("road_left", road_left)
cv.imshow("road_right", road_right)
cv.imshow("road_top", road_top)
cv.imshow("road_down", road_down)
cv.waitKey(1000)
cv.destroyAllWindows()

print("4. Use median filter")
road_left = cv.medianBlur(road_left,5)
road_right = cv.medianBlur(road_right,5)
road_top = cv.medianBlur(road_top,5)
road_down = cv.medianBlur(road_down,5)

cv.imwrite('road_left_filtred.png',road_left)

#convert img to binary
print("5. Convert image from grayscale to binary.")

rat,road_left = cv.threshold (road_left,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
rat,road_top = cv.threshold (road_top,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
rat,road_right = cv.threshold (road_right,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)
rat,road_down = cv.threshold (road_down,0,255,cv.THRESH_BINARY+cv.THRESH_OTSU)

# show images
cv.imshow("road_left", road_left)
cv.imshow("road_right", road_right)
cv.imshow("road_top", road_top)
cv.imshow("road_down", road_down)
cv.waitKey(1000)
cv.destroyAllWindows()

# morphological operation
print("6. Perform morphological operations.")
kernel = np.ones((15,15),np.uint8)
road_left = cv.morphologyEx(road_left, cv.MORPH_DILATE, kernel)
road_top = cv.morphologyEx(road_top, cv.MORPH_DILATE, kernel)
road_right = cv.morphologyEx(road_right, cv.MORPH_DILATE, kernel)
road_down = cv.morphologyEx(road_down, cv.MORPH_DILATE, kernel)

cv.imwrite('road_left_dilate.png',road_left)

# show images
cv.imshow("road_left", road_left)
cv.imshow("road_right", road_right)
cv.imshow("road_top", road_top)
cv.imshow("road_down", road_down)
cv.waitKey(1000)
cv.destroyAllWindows()

# put frames and counting vehicles
print("7. Put frames and count the vehicles.")
roads = [road_left] + [road_right] + [road_top] + [road_down]
points_all = []
for road in roads:

    contours,hierarchy = cv.findContours(road, 1, 2)
    points = 0
    print("---")
    for i in range (len(contours)):
            x,y,w,h = cv.boundingRect(contours[i])

            if x == 0 or y == 0 or y + h == road.shape[0] or x + w == road.shape[1] or w*h < 5000 or w < 50 or h < 50:
                pass

            else:
                road = cv.rectangle(road,(x,y),(x+w,y+h),(120,120,120),2)
                area = w * h
                if area < 15000:
                    points = points + 1
                    print("Bike or motorbike")
                elif area > 15000 and area < 85000:
                    points = points + 3
                    print("Car")
                elif area > 85000:
                    points = points + 5
                    print("Truck or bus")

    points_all = points_all + [points]
    

points_all_HV = [0,0]
points_all_HV[0] = points_all[0] + points_all[1]
points_all_HV[1] = points_all[2] + points_all[3]

print("Left & Right - " + str(points_all_HV[0]) + " traffic points")
print("Road Top & Down - " + str(points_all_HV[1]) + " traffic points")

cv.imwrite('road_left_frame.png',road_left)

# show images
cv.imshow("road_left", road_left)
cv.imshow("road_right", road_right)
cv.imshow("road_top", road_top)
cv.imshow("road_down", road_down)
cv.waitKey(500)

#Traffic light control
print("7. Traffic light control")
for i in range(2):

    if points_all_HV[0] > points_all_HV[1]:
        print('Road Left & Right - GO')
        print("Road Top & Down - yellow light.")
        cv.waitKey(1000)
        print("Road Top & Down - red light.")
        cv.waitKey(1000)
        print("Road Left & Right - yellow light.")  
        cv.waitKey(1000)
        print("Road Left & Right - green light.")
        cv.waitKey(1000)

        for i in range (5,0, -1):
            print("Road Left & Right - Time: " + "* " * i)
            time.sleep(1)
        cv.destroyAllWindows()
        points_all_HV[0] = 0

    else:
        print('Road Top & Down - GO')
        print("Road Left & Right - yellow light.")
        cv.waitKey(1000)
        print("Road Left & Right - red light.")
        cv.waitKey(1000)
        print("Road Top & Down - yellow light.")       
        cv.waitKey(1000)
        print("Road Top & Down - green light.")
        cv.waitKey(1000)
        
        for i in range (5,0, -1):
            print("Road Top & Down - Time: " + "* " * i)
            time.sleep(1)
        points_all_HV[1] = 0


