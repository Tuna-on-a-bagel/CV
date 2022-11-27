import pyrealsense2 as rs
import numpy as np


def initialize():
    # Configure depth and color streams
    pipeline = rs.pipeline()
    config = rs.config()
    #print("fig", config[0])
    # Get device product line for setting a supporting resolution
    pipeline_wrapper = rs.pipeline_wrapper(pipeline)
    pipeline_profile = config.resolve(pipeline_wrapper)
    device = pipeline_profile.get_device()
    device_product_line = str(device.get_info(rs.camera_info.product_line))

    #pipeline_profile.set_option(rs.option.exposure, 4)    # -p

    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    #config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgra8, 30) # -p
    #config.enable_stream(rs.stream.color, 640, 480, rs.format.yuyv, 30) # -p
    


   

    #pipeline = rs.pipeline()
    #config = rs.config()
    #profile = pipeline.start(config) # Start streaming
    #sensor_dep = profile.get_device().first_depth_sensor()
    #print("Trying to set Exposure")
    #exp = sensor_dep.get_option(rs.option.exposure)
    ##print "exposure = %d" % exp
    ##print "Setting exposure to new value"
    #exp = sensor_dep.set_option(rs.option.exposure, 25000)
    #exp = sensor_dep.get_option(rs.option.exposure)
    ##print "New exposure = %d" % exp
    #profile = pipeline.stop







    # From git, for c implementation but could be helpful # -p
    #rs2::pipeline pipe;
    #rs2::pipeline_profile selection = pipe.start();
    #rs2::device selected_device = selection.get_device();
    #auto depth_sensor = selected_device.first<rs2::depth_sensor>();
    #depth_sensor.set_option(RS2_OPTION_AUTO_EXPOSURE_MODE, 1.f); // Enable auto-exposure anti flicker mode
    
    



    
    # Start streaming
    profile = pipeline.start(config)


    sensor_dep = profile.get_device().first_depth_sensor() # -p
    exp = sensor_dep.get_option(rs.option.exposure)
    print( "exposure = %d" % exp)
    exp = sensor_dep.set_option(rs.option.exposure, 25000)

    exp = sensor_dep.get_option(rs.option.exposure)
    print( "exposure = %d" % exp)
    
    #auto = sensor_dep.get_option(rs.option.auto_exposure_mode)
    #print( "auto = %d" % auto)
    #########me###########3
    #s = pipeline.get_device()   #.query_sensors()[1]
    #s.set_option(rs.option.exposure, 4)
        
    

    return pipeline

def grab_frame(pipeline):
    frames = pipeline.wait_for_frames()
    depth_frame = frames.get_depth_frame()
    color_frame = frames.get_color_frame()

    depth_image = np.asanyarray(depth_frame.get_data())
    color_image = np.asanyarray(color_frame.get_data())
    if not depth_frame or not color_frame:
        return False, None, None
    return True, depth_image, color_image

def release(self):
    self.pipeline.stop()