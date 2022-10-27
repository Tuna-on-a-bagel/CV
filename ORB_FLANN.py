from pickle import NONE
import numpy as np
import cv2 as cv
from matplotlib import pyplot as plt
import time
import numpy as np
import simple_CSI


#some setup:
video_capture = cv.VideoCapture(simple_CSI.gstreamer_pipeline(flip_method=0), cv.CAP_GSTREAMER)

cameraMatrix = np.array([[470.0, 0.0, 206.0], [0.0, 193.0, 156.0], [0.0, 0.0, 1.0]])
distortionCoeffs = np.array([[-0.141, 0.012, 0.0, 0.006, 0.018]])

counter = 0
timer = 300

#ORB stuff:
max_features = 400  #max number of features, will stop if this value is hit
scale_factor = 1.2  #default = 1.2
nlevels = 8        #default = 8, num of pyramid levels
first_level = 0     #default = 0, the pyramid level at which input image is  located, previous layers will be filled with upscaled source image
edge_threshold = 31 #default = 31, should nearly match patchsize
patch_size = 31    #default = 31, should nearly match edge threshold
score_type = 'HARRIS_SCORE' #default value = 0 (HARRIS_SCORE), optional value =  FAST_SCORE which will be faster but less stable points
fast_threshold = 20 #default = 20

orb_1 = cv.ORB_create(nfeatures=max_features, 
                    scaleFactor=scale_factor, 
                    nlevels=nlevels, 
                    edgeThreshold=edge_threshold, 
                    firstLevel=first_level, 
                    patchSize=patch_size,
                    fastThreshold=fast_threshold)

#flann stuff:
FLANN_INDEX_LSH = 6
index_params = dict(algorithm=FLANN_INDEX_LSH, table_number =6, key_size=12, multi_probe_level=1)
search_params = dict(checks=50)


def get_ORB(frame, ORB_ID, drawMarker, distortionFix=None):

    #convert to gray, saves cost
    frame = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

    #distortion:
    if distortionFix:
        frame = cv.undistort(frame, distortionFix[0], distortionFix[1], None, distortionFix[0])

    #Compute
    keyp, des = ORB_ID.detectAndCompute(frame, None) #this is faster than orb.detect(), orb.compute()
     
    #Draw the orb markers (only for visualizing, does not affect algorithm)
    if drawMarker == True:
        frame = cv.drawKeypoints(frame, keyp, None, color=(255, 0, 0), flags=0)
    
    return frame, keyp, des

    

  
def get_FLANN(keypA, desA, keypB, desB, flan_ID):

    good_matches = []

    #only run flann if minimum num keypt for orientation reached
    if len(keypA) > 6 and len(keypB) > 6:
        matches = flan_ID.knnMatch(desA, desB, k=2)
        #print(matches[0][0])
        #make sure we have enough matches, then build list of best matches
        try:
            for m, n in matches:
                match = True       #Debuggin
                if m.distance < 0.5 * n.distance:
                       
                    if m.distance * n.distance <= 5:
                        good_matches.insert(0, m)
                        #print("best match")
                    else:
                        good_matches.append(m)  #build list of best matches
                        
            #q1 = np.float32([keypA[m.queryIdx].pt for m in good_matches])
            #q2 = np.float32([keypB[m.trainIdx].pt for m in good_matches])

            matched_keyp = [keypA[m.queryIdx] for m in good_matches]
            return good_matches, matches, matched_keyp 

        except ValueError:
            match = False          #Debuggin
            print("match list insufficient")
            return None, matches, None
            pass

        

def compute_ORB_FLANN(runTime, imshow, cameraMatrix, distortionCoeffs):
    
    flann = cv.FlannBasedMatcher(indexParams=index_params, searchParams=search_params)
    curTime = 0
    new_frame_time = 0
    prev_frame_time = 0
    frame_count = 0
    avg_count = 0
    avg_fps = 0
   
    if video_capture.isOpened():
        
        ###THIS WARM UP SECTION IS IMPORTANT FOR ORB FOR SOME REASON####
        while True:
            
            ret_val, frameA = video_capture.read()
            frameA, keypA, desA = get_ORB(frame=frameA, ORB_ID=orb_1, drawMarker=False, distortionFix=[cameraMatrix, distortionCoeffs])
            print("in warm up mode -- ", " len(keypA):", len(keypA))
            curTime += 1
            if curTime >= 30:
                curTime=0
                #break warm up, set up intial frames for flann
                frameB, keypB, desB = frameA, keypA, desA   #set previous frame + data
                ret_val, frameA = video_capture.read()      #grab new frame
                frameA, keypA, desA = get_ORB(frame=frameA, ORB_ID=orb_1, drawMarker=False, distortionFix=[cameraMatrix, distortionCoeffs]) #compute latest frame ORB
                break

        ###MAIN LOOP WITH FLANN####
        while True:

            good_matches, matches, matched_keyp = get_FLANN(keypA, desA, keypB, desB, flan_ID=flann)

            if imshow == True:
                marked = cv.drawKeypoints(frameA, keypA, None, color=(20,20,180), flags=0)
                if matched_keyp:
                    matched_marked = cv.drawKeypoints(marked, matched_keyp[:10], None, color=(0,255,0), flags=0)
                    cv.imshow("matched", matched_marked)
                    cv.waitKey(1)

            frameB, keypB, desB = frameA, keypA, desA   #set previous frame + data
            ret_val, frameA = video_capture.read()      #grab new frame
            frameA, keypA, desA = get_ORB(frame=frameA, ORB_ID=orb_1, drawMarker=False, distortionFix=[cameraMatrix, distortionCoeffs]) #compute latest frame ORB

            curTime += 1
            frame_count += 1
            new_frame_time = time.time()
            fps2 = 1/(new_frame_time - prev_frame_time)
            fps2 = int(fps2)
            avg_count += fps2
            if frame_count >= 8:
                avg_fps = avg_count/frame_count
                avg_fps = int(avg_fps)
                frame_count = 0 
                avg_count = 0
            prev_frame_time = new_frame_time
            match = False
            if good_matches:
                match = True
            print("FPS: ", avg_fps, " #matches:", len(matches), "good_match:",  match)

            if curTime >= runTime:
                
                break

        video_capture.release()
        cv.destroyAllWindows()
    else:
        print("cant open video stream")


compute_ORB_FLANN(runTime=300, imshow=True, cameraMatrix=cameraMatrix, distortionCoeffs=distortionCoeffs)
#ret, img = video_capture.read()
#cv.imshow("img", img)
#cv.waitKey(2000)
#cv.destroyAllWindows()
#kp, des = get_ORB(orb_1, img, drawMarker=False)
#print("kp:", kp)
video_capture.release()
cv.destroyAllWindows()


#keyp2 = orb.detect(img2, None)
#keyp2, descriptor2 = orb.compute(img2, keyp2)

#while True:
#    result2, img2 = video_capture.read()
#    if img1 != img2:                    #wait to make sure frame is different
#        break


