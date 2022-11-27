import cv2 as cv
import pyrealsense2 as rs
from realsense_depth import *
import simple_rs

#dc = DepthCamera()

p = simple_rs.initialize()

ret_val, depth_frame, color_frame = simple_rs.grab_frame(p)

#re_vat, depth_frame, color_frame = dc.get_frame()

cv.imshow("color", color_frame)
cv.waitKey()
cv.destroyAllWindows()

cv.imshow("d", depth_frame)
cv.waitKey()
cv.destroyAllWindows()

#dc.release()
#p.release()