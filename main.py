import cv2 as cv
import numpy as np
import os
from time import time
from windowcapture import WindowCapture
from vision import Vision
from hsvfilter import HsvFilter

class Icon:
    def __init__(self, img_paths, hsv_filter=None, threshold=0.7, max_results=10):
        self.img_paths = img_paths
        self.hsv_filter = hsv_filter
        self.threshold = threshold
        self.found = False
        self.rectangle = []
        self.max_results = max_results

    def find(self, screenshot):
        if not self.found:
            for img_path in self.img_paths:
                vision = Vision(img_path)
                self.rectangle = vision.find(screenshot, self.threshold, self.max_results)
                if len(self.rectangle):
                    self.found = True
                    break
        return self.rectangle

# initialize the WindowCapture class
wincap = WindowCapture('Toontown Offline')
# initialize the Vision class
vision = Vision('images//task_icon.jpg')
# initialize the trackbar window
vision.init_control_gui()

# ttc HSV filter
ttc_filter = HsvFilter(0,0,210,23,132,255,0,0,0,0)

# create instances of the Icon class
icon_toontask = Icon(['images//task_icon.jpg'])
icon_arrow = Icon(['images//arrow_left.jpg','images//arrow_right.jpg','images//arrow_up.jpg'],
    threshold=0.7)
icon_ttc_mainroad = Icon(['images//ttc_mainroad.jpg'],hsv_filter=ttc_filter, threshold=0.6, max_results=50)

loop_time = time()
while(True):

    # get an updated image of the game
    screenshot = wincap.get_screenshot()

    # pre-process the image
    processed_image = vision.apply_hsv_filter(screenshot)

    # apply edge filter
    edges_image = vision.apply_edge_filter(processed_image)

    # find ToonTask icon and the player arrow icon, combine them into a list
    # rectangle_tt = icon_toontask.find(screenshot)
    rectangle_arrow = icon_arrow.find(screenshot)
    # rectangles = np.concatenate((rectangle_tt, rectangle_arrow))
    # rectangles = icon_ttc_mainroad.find(screenshot)
    x = Vision.get_click_points(rectangle_arrow)
    print(x)

    # draw the detection results onto the original image
    output_image = Vision.draw_rectangles(screenshot, rectangle_arrow)

    # display the processed image
    cv.imshow('Processed', processed_image)
    cv.imshow('Edges', edges_image)
    cv.imshow('Matches', output_image)

    # debug the loop rate
    print('FPS {}'.format(1 / (time() - loop_time)))
    loop_time = time()

    # press 'q' with the output window focused to exit.
    # waits 1 ms every loop to process key presses
    if cv.waitKey(1) == ord('q'):
        cv.destroyAllWindows()
        break

print('Done.')