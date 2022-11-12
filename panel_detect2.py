import cv2 as cv
import numpy as np
from cmath import inf

#image preperation
input = cv.imread("project/panel4.jpg", 1)

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

#Trying to pull line data straight from contour data:
c = 0        #for color switching
r_test = 15  #magnitude for unit vector

#getting rid of small contours
#contours = []
#for cnt in contour:
#    print("len(cnt):", len(cnt))
#    if len(cnt) > 100:
#        contours.append(cnt)

for cnt in contour:
#for cnt in contours:
    color = colors[c]
    i = 0
    while True:
        
        if i < (len(cnt) - 5):
            #neighbor contour points
            x1, y1 = cnt[i][0][0], cnt[i][0][1]
            x2, y2 = cnt[i+5][0][0], cnt[i+5][0][1]

        #Calculate normal direction form contour
        if x1 != 0 and y1 != 0 and x1 != 0 and x2 != 0: #neccessary conditions to avoid jumping out of feasible range

            #paint the tangent line (connection line between contour points)
            painted = cv.line(input, (x1, y1), (x2,  y2), color, 2)

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

            check = cv.pointPolygonTest(cnt, ((y_midPoint + int(r_test*v)), (x_midPoint + int(r_test*u))), False) #returns 1 if inside, -1 if outside, 0 if on contour
            
            #if check == 1:
            #    u = -1*u
            #    u_norm = -1*u_norm
            #    v = -1*v
            #    v_norm = -1*v_norm
            #    check = cv.pointPolygonTest(cnt, ((y_midPoint + int(r_test*v)), (x_midPoint + int(r_test*u))), False) #returns 1 if inside, -1 if outside, 0 if on contour
            
            print("check: ", check )             

            x_endPoint, y_endPoint = int((x_midPoint + r_test*u_norm)), int((y_midPoint + r_test*v_norm))
            if (0 <= x_endPoint <= input.shape[1]) and (0 <= y_endPoint <= input.shape[0]):
                painted = cv.line(input, (x_midPoint, y_midPoint), (x_endPoint,  y_endPoint), color, 1)

        cv.imshow("points", painted)
        cv.waitKey(1)

        if i < (len(cnt) - 10):
            i += 10 #skip distance, dont want to do this at every single line point 
        else:
            break
    
    c += 1 #next color in list


cv.waitKey()
cv.destroyAllWindows()

#cv.imwrite('panel1_withNorms1.jpg', painted)
  
# Showing the final image.
#cv.imshow('image2', input) 

#cv.imshow("gray", dst)
#cv.waitKey()
cv.destroyAllWindows()
