import cv2 as cv
import numpy as np
from cmath import inf

#image preperation
input = cv.imread("project/panel4.jpg", 1)

print("dims:", input.shape[0], input.shape[1])

#convert to gray scale:
gray = cv.cvtColor(input, cv.COLOR_BGR2GRAY)
cv.imshow("gray", gray)
cv.waitKey()
cv.destroyAllWindows()

#apply a blur:
blurred = cv.medianBlur(gray,7)
blurred = cv.medianBlur(blurred,7) #testing additional blur

#threshold the image to binary for contour func:
thr_val, threshed = cv.threshold(blurred, 60, 255, cv.THRESH_BINARY)
#threshed = cv.adaptiveThreshold(blurred,255,cv.ADAPTIVE_THRESH_GAUSSIAN_C,  cv.THRESH_BINARY,11,2) #dont delete, this works for first imgs
cv.imshow("threshed", threshed)
cv.waitKey()
cv.destroyAllWindows()

print("dims threshed:", threshed.shape[0], threshed.shape[1])

#get contours:
#contour, heirachy = cv.findContours(threshed, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE) #this works
contour, heirarchy = cv.findContours(threshed, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE) #testing this 
print("length cont: ", len(contour))
#print("contour points: ", contour[0])

painted = blurred.copy()

#shows all contours in green, only really for debugging:
showContour = cv.drawContours(input, contour, -1, (0, 255, 0), 1)
cv.imshow("contours", showContour)
cv.waitKey()
cv.destroyAllWindows()


COMs = []
dims = input.shape

#center of mass stuff, not used rn but might be useful later for something:
use_COMs = False
if use_COMs == True:
    for i in range(0, len(contour)):

        #Get COM of each contour
        moments = cv.moments(contour[i])
        COM_X = int(moments['m10'] / moments['m00'])
        COM_Y = int(moments['m01'] / moments['m00'])
        coords = COM_X, COM_Y
        COMs.append(coords)

        #draw COM point
        painted = cv.circle(input, (COM_X, COM_Y), 5, (0, 0, 255), -1)

        #draw contour
        #painted = cv.drawContours(input, contour, i, (255,0,0), 2)
        #cv.imshow("painted", painted)
        #cv.waitKey(1000)

#testing ellipse:
#(x,y),(MA,ma),angle = cv.fitEllipse(contour[1])
#painted = cv.ellipse(input, (x, y), (MA, ma), angle, color=(255, 0, 0))

#testing grabbing mask points:
#mask = np.zeros(gray.shape,np.uint8)
#cv.drawContours(mask,[contour],0,255,-1)
#pixelpoints = np.transpose(np.nonzero(mask))
#pixelpoints = cv.findNonZero(mask)


print(" ")
print(" ==== Next Section ====")
print(" " )

font = cv.FONT_HERSHEY_COMPLEX
colors = [(255, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255), (255, 0, 255), (0, 255, 0), (255, 0, 0), (0, 0, 255)]


c = 0        #for color switching
r_test = 15  #magnitude for unit vector

#getting rid of smaller discrepency contours (this is an issue with thresholding)
#should replace this section with a heirachy check method
contours = []
for cnt in contour:
    print("len(cnt):", len(cnt))
    if len(cnt) > 700:             #this static value wont work in real life, will need to make this value a function of camera distance from the car
        contours.append(cnt)

print("length contours:", len(contours))

Text = True
for cnt in contours:
    color = colors[c]
    i = 0
    label_counter = 0
    while True:
        
        if i < (len(cnt) - 5):
            #neighbor contour points
            
            x1, y1 = cnt[i][0][0], cnt[i][0][1]
            x2, y2 = cnt[i+5][0][0], cnt[i+5][0][1]
            label_counter += 1

        #Calculate normal direction form contour            #this last bit may cause issues for flat sections
        if x1 != 0 and y1 != 0 and x1 != 0 and x2 != 0 and (np.sqrt((x2-x1)**2 + (y2-y1)**2) < 150): #neccessary conditions to avoid jumping out of feasible range

            if np.sqrt((x2 - x1)**2 + (y2 - y1)**2) < 100:
                f = 0 #placeholder
                #painted = cv.line(input, (x1, y1), (x2,  y2), color, 2)

            #calculate midpoint between those contour points
            x_midPoint, y_midPoint = int((x1 + x2)/2), int((y1 + y2)/2)
            
            #vector from midpoint to 2nd point:
            u = x2 - x_midPoint
            v = y2 - y_midPoint

            #normalize to unit vector
            magnitude = np.sqrt(u**2 + v**2)
            u = u/magnitude
            v = v/magnitude
            
            #rotate 90 degree to get ortho unit vector:
            u_norm = -v
            v_norm = u
            
            #check first direction (90* rotated vector), if point is not within home contour, continue searching for next contour,
            # if point is within home contour, flip 180* and search opposite direction
            ###### should add a bool so that this doesnt need to be repeated every itteration ####
            #unused at the moment. I bleieve that contours always move CW, so rotating by -90 is sufficient to garuntee not within host contour
            check = cv.pointPolygonTest(cnt, ((y_midPoint + int(r_test*v)), (x_midPoint + int(r_test*u))), False) #returns 1 if inside, -1 if outside, 0 if on contour
            
            #measurement section:
            r = 5   #reset beggining radius for checking pixel value
            while True:
                x_endPoint, y_endPoint = int(x_midPoint + r*u_norm), int((y_midPoint + r*v_norm))
                #print("in:", r)


                if (0 <= x_endPoint <= input.shape[1]) and (0 <= y_endPoint <= input.shape[0]):
                    
                    #check if new pixel is not a black pixel in the threshed image
                    if threshed[y_endPoint, x_endPoint] != 0:
                        
                        #calculate euclidian distance to next contour
                        dist = np.sqrt((r*u_norm)**2 + (r*v_norm)**2)
                        dist = np.round(dist, 1) #round to first decimal

                        #color map the line intensity to distance measurement
                        normalized = dist/(50) 
                        color_scale = normalized * 255

                        #paint the measurment line with mapped intensity value
                        painted = cv.line(input, (x_midPoint, y_midPoint), (x_endPoint,  y_endPoint), (0, 0, color_scale), 1)

                        #only put text every 5 measurements to reduce clutter, only for debugging
                        if label_counter > 5 and Text == True:
                            painted = cv.putText(input, str(dist), (x_midPoint, y_midPoint), font, 1, (255, 0, 130), 2)
                            label_counter = 0
                        break

                #if no contour is found within 100 units, break and move on (probably not a panel gap)
                if r > 100:
                    break

                r += 1 

            cv.imshow("points", painted)
            cv.waitKey(1)

            #if check == 1:
            #    u = -1*u
            #    u_norm = -1*u_norm
            #    v = -1*v
            #    v_norm = -1*v_norm
            #    check = cv.pointPolygonTest(cnt, ((y_midPoint + int(r_test*v)), (x_midPoint + int(r_test*u))), False) #returns 1 if inside, -1 if outside, 0 if on contour
            
            #print("check: ", check )             

            #x_endPoint, y_endPoint = int((x_midPoint + r_test*u_norm)), int((y_midPoint + r_test*v_norm))
            #if (0 <= x_endPoint <= input.shape[1]) and (0 <= y_endPoint <= input.shape[0]):
            #    painted = cv.line(input, (x_midPoint, y_midPoint), (x_endPoint,  y_endPoint), color, 1)

        #cv.imshow("points", painted)
        #cv.waitKey(1)

        if i < (len(cnt) - 10):
            i += 10 #skip distance, dont want to compute this program at every single line point 
        else:
            break
    Text = False
    c += 1 #next color in list


cv.waitKey()
cv.destroyAllWindows()

#cv.imwrite('panel4_measured.jpg', painted)
  
# Showing the final image.
#cv.imshow('image2', input) 

#cv.imshow("gray", dst)
#cv.waitKey()
cv.destroyAllWindows()
