from locale import normalize
import cv2 as cv
import sys
import numpy as np
import os
from matplotlib import cm
from matplotlib import pyplot as plt
from tkinter import *

user_input = 'calibration_img0(1).png' 

img = cv.imread(user_input, 1) 
cv.imshow("original", img)
cv.waitKey(10)




d1 = 0
d2 = 0
d3 = 0
d4 = 0
d5 = 0

fx = 0
fy = 0
s = 0
x0 = 0
y0 = 0

cameraMatrixOld = np.array([[255.0, 0.0, 231.0], [0.0, 249.0, 118.0], [0.0, 0.0, 1.0]])
cameraMatrix = np.array([[470.0, 0.0, 206.0], [0.0, 193.0, 156.0], [0.0, 0.0, 1.0]])
newCameraMatrix = np.array([[470.0, 0.0, 206.0], [0.0, 193.0, 156.0], [0.0, 0.0, 1.0]])
dist_old = np.array([[-0.054, 0.145, -0.047, -0.093, -0.096]]) #original output from checkerboard tuning
dist = np.array([[-0.141, 0.012, 0.0, 0.006, 0.018]]) #values detirmined from tuning previously


newCameraMatrix = cameraMatrix

fixed = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
#fixed = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
cv.imshow("fixed", fixed)
cv.waitKey(10000)

root = Tk()  
root.geometry("400x300") 
  
v1 = DoubleVar()
v2 = DoubleVar()
v3 = DoubleVar()
v4 = DoubleVar()
v5 = DoubleVar()

def correct_dist():  

    cv.destroyWindow("fixed")      
    sel = "d1 = " + str(v1.get()/1000)
    sel2 = "d2 = " + str(v2.get()/1000)
    sel3 = "d3 = " + str(v3.get()/1000)
    sel4 = "d4 = " + str(v4.get()/1000)
    sel5 = "d5 = " + str(v5.get()/1000)

    d1 = v1.get()/1000
    d2 = v2.get()/1000
    d3 = v3.get()/1000
    d2 = v4.get()/1000
    d3 = v5.get()/1000

    

    l1.config(text = sel, font =("Courier", 10))  
    l2.config(text = sel2, font =("Courier", 10))
    l3.config(text = sel3, font =("Courier", 10))
    l4.config(text = sel4, font =("Courier", 10))
    l5.config(text = sel5, font =("Courier", 10))


    dist[0,0] = d1
    dist[0,1] = d2
    dist[0,2] = d3
    dist[0,3] = d4
    dist[0,4] = d5

    fixed = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
    #fixed = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
    cv.imshow("fixed", fixed)
    cv.waitKey(5)
    
    print(newCameraMatrix)
    print("dist:", dist)

    
    #output = cv.vconcat([canny_img, img])
    
    #save = input("Save current itteration canny?: <Y/N>")
    save = False
    if save == Y:
        corrected_name = str(img_name + "-canny." + file_type) #use user input file to make edited name
        print("correctedname:", corrected_name)
        cv.imwrite(corrected_name, img)

def correct_mat():  

    cv.destroyWindow("fixed")      
    sel =  "[X 0 0] = " + str(v1.get())
    sel2 = "[0 Y 0] = " + str(v2.get())
    sel3 = "[0 0 x0] = " + str(v3.get())
    sel4 = "[0 0 y0] = " + str(v4.get())
    sel5 = "d5 = " + str(v5.get()/1000)

    newCameraMatrix[0][0] = v1.get()
    newCameraMatrix[1][1] = v2.get()
    newCameraMatrix[0][2] = v3.get()
    newCameraMatrix[1][2] = v4.get()
   

    

    l1.config(text = sel, font =("Courier", 10))  
    l2.config(text = sel2, font =("Courier", 10))
    l3.config(text = sel3, font =("Courier", 10))
    l4.config(text = sel4, font =("Courier", 10))
    l5.config(text = sel5, font =("Courier", 10))


    #dist[0,0] = d1
    #dist[0,1] = d2
    #dist[0,2] = d3
    #dist[0,3] = d4
    #dist[0,4] = d5

    fixed = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
    #fixed = cv.undistort(img, cameraMatrix, dist, None, newCameraMatrix)
    cv.imshow("fixed", fixed)
    cv.waitKey(5)
    
    print(newCameraMatrix)
    print(cameraMatrix)
    print("dist:", dist)

    
    #output = cv.vconcat([canny_img, img])
    
    #save = input("Save current itteration canny?: <Y/N>")
    save = False
    if save == Y:
        corrected_name = str(img_name + "-canny." + file_type) #use user input file to make edited name
        print("correctedname:", corrected_name)
        cv.imwrite(corrected_name, img)

#turn these on when tuning distortion
s1 = Scale( root, variable = v1, from_ = -400, to = 400, orient = HORIZONTAL)    
s2 = Scale( root, variable = v2, from_ = -400, to = 400, orient = HORIZONTAL) 
s3 = Scale( root, variable = v3, from_ = -200, to = 200, orient = HORIZONTAL) 
s4 = Scale( root, variable = v4, from_ = -200, to = 200, orient = HORIZONTAL) 
s5 = Scale( root, variable = v5, from_ = -200, to = 200, orient = HORIZONTAL) 

#turn these on for editing matrix
#s1 = Scale( root, variable = v1, from_ = 100, to = 500, orient = HORIZONTAL)    
#s2 = Scale( root, variable = v2, from_ = 100, to = 400, orient = HORIZONTAL) 
#s3 = Scale( root, variable = v3, from_ = 100, to = 300, orient = HORIZONTAL) 
#s4 = Scale( root, variable = v4, from_ = 100, to = 300, orient = HORIZONTAL) 
#s5 = Scale( root, variable = v5, from_ = -200, to = 200, orient = HORIZONTAL) 


l3 = Label(root, text = "Horizontal Scaler")
l4 = Label(root, text = "Horizontal Scaler")
l5 = Label(root, text = "Horizontal Scaler")
l6 = Label(root, text = "Horizontal Scaler")
l7 = Label(root, text = "Horizontal Scaler")

b1 = Button(root, text ="Display Horizontal", command = correct_dist, bg = "yellow")  

l1 = Label(root)
l2 = Label(root)
l3 = Label(root)
l4 = Label(root)
l5 = Label(root)

s1.pack(anchor = CENTER)
s2.pack(anchor = CENTER) 
s3.pack(anchor = CENTER) 
s4.pack(anchor = CENTER) 
s5.pack(anchor = CENTER)

l1.pack()
l2.pack()
l3.pack()
l4.pack()
l5.pack()


b1.pack(anchor = CENTER)


root.mainloop()