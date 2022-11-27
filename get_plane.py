import numpy as np
import cv2 as cv



#Must define a fucntion to get points from realsense





def getOrthoNormVec(A, B, C):
    
    #Plane vector 1
    vecAB = [(A[0] - B[0]), (A[1] - B[1]), (A[2] - B[2])]
    #Plane vector 2
    vecBC = [(B[0] - C[0]), (B[1] - C[1]), (B[2] - C[2])]

    #calculate plane normal vector components
    a, b, c = np.cross(vecAB, vecBC)
    mag = np.sqrt(a**2 + b**2 + c**2)

    #create unit vector
    norm = [a/mag, b/mag, c/mag]

    return norm

def correct(imageVec, surfaceNorm):

    #calculate magnitude of vector on image plane
    imgMag = np.sqrt(imageVec[0]**2 + imageVec[1]**2 + imageVec[2]**2)
    #magnitude of surface plane ortho norm is always 1
    surfMag = 1

    #calculate angle between image vec and surface norm
    theta = np.arccos((np.dot(imageVec, surfaceNorm))/imgMag)

    #calculate corrected length (based on law of sines)
    corrected = imgMag/np.sin(theta)

    return corrected
    

