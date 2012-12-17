#!/usr/bin/env python
#import cv_bridge
import cv

class BlobFinder:

    def __init__(self):
        
        #Dictionary containing the threshold values that the sliders correspond
        #to, each is initially set to 128, the mid value.
        self.thresholds = {'low_red': 128, 'high_red': 128,\
                           'low_green': 128, 'high_green': 128,\
                           'low_blue': 128, 'high_blue': 128,\
                           'low_hue': 128, 'high_hue': 128,\
                           'low_sat': 128, 'high_sat': 128,\
                           'low_val': 128, 'high_val': 128}
        
        #Set up the windows containing the image from the kinect, the altered
        #image, and the threshold sliders.
        cv.NamedWindow('image')
        cv.MoveWindow('image',320,0)
        cv.NamedWindow('threshold')
        cv.MoveWindow('threshold',960,0)       
        cv.NamedWindow('hsv')
        cv.MoveWindow('hsv', 320, 450)
        
        self.make_slider_window()
        
        #self.bridge = cv_bridge.CvBridge()
        
        #self.capture = cv.CaptureFromCAM(0)
        #self.image = cv.QueryFrame(self.capture)
        
        self.image_orig = cv.LoadImageM('room1.jpg')
        self.image_color = cv.LoadImageM('room1.jpg')
        self.image = cv.LoadImageM('room1.jpg')
        
        self.size = cv.GetSize(self.image)
        self.hsv = cv.CreateImage(self.size, 8, 3)
        
        cv.SetMouseCallback('image', self.mouse_callback, True)
        
        self.RGBavgs = ()
        self.RGBvals = []
        
        self.HSVavgs = ()
        self.HSVvals = []
        
        self.new_color = (128,0,0)
        self.new_hsv = (0, 255, 255)
        self.hue = 0
        
    def mouse_callback(self, event, x, y, flags, param):
    
        if event == cv.CV_EVENT_LBUTTONDOWN:
            bgra = cv.Get2D(self.image, y, x)
#            hsv = cv.Get2D(self.hsv, y, x)
#            bgrhsv = bgra[:-1] + hsv[:-1]
            
            print "coords: (",x,",",y,")"
            print "bgra:", bgra
            
            blue = int(bgra[0])
            green = int(bgra[1])
            red = int(bgra[2])
            
#            hue = int(bgrhsv[3])
#            sat = int(bgrhsv[4])
#            val = int(bgrhsv[5])
            
            self.RGBvals.append((red,green,blue))
#            self.HSVvals.append((hue,sat,val))
            
            if len(self.RGBavgs) > 0:
                print self.RGBavgs
                print red, green, blue
                self.RGBavgs = ((self.RGBavgs[0] + red)/2, 
                                (self.RGBavgs[1] + green)/2,
                                (self.RGBavgs[2] + blue)/2)
                
#                self.HSVavgs = ((self.HSVavgs[0] + hue)/2, 
#                                (self.HSVavgs[1] + sat)/2,
#                                (self.HSVavgs[2] + val)/2)
            else:
                self.RGBavgs = (red, green, blue)
#                self.HSVavgs = (hue, sat, val)
                                
            print "RGBavgs:", self.RGBavgs
            print "RGBvals:", self.RGBvals
            
#            print "HSVavgs:", self.HSVavgs
#            print "HSVvals:", self.HSVvals
            
            rgbwindow = 50 # half the size of the window we want for thresholds
#            hsvwindow = 200            
            
            self.thresholds['low_red'] = self.RGBavgs[0] - rgbwindow
            self.thresholds['high_red'] = self.RGBavgs[0] + rgbwindow
            self.thresholds['low_green'] = self.RGBavgs[1] - rgbwindow
            self.thresholds['high_green'] = self.RGBavgs[1] + rgbwindow
            self.thresholds['low_blue'] = self.RGBavgs[2] - rgbwindow
            self.thresholds['high_blue'] = self.RGBavgs[2] + rgbwindow
#            self.thresholds['low_hue'] = self.HSVavgs[0] - hsvwindow
#            self.thresholds['high_hue'] = self.HSVavgs[0] + hsvwindow
#            self.thresholds['low_sat'] = self.HSVavgs[1] - hsvwindow
#            self.thresholds['high_sat'] = self.HSVavgs[1] + hsvwindow
#            self.thresholds['low_val'] = self.HSVavgs[2] - hsvwindow
#            self.thresholds['high_val'] = self.HSVavgs[2] + hsvwindow
            
            #Recreate the slider window
            cv.DestroyWindow('sliders')
            self.make_slider_window()
            
        
    def make_slider_window(self):
        #Create slider window
        cv.NamedWindow('sliders')
        cv.MoveWindow('sliders', 0, 0)
        
        #Create sliders
        cv.CreateTrackbar('low_red', 'sliders', self.thresholds['low_red'],\
                          255, self.change_low_red)
        cv.CreateTrackbar('high_red', 'sliders', self.thresholds['high_red'],\
                           255, self.change_high_red)
        cv.CreateTrackbar('low_green', 'sliders', self.thresholds['low_green'],\
                          255, self.change_low_green)
        cv.CreateTrackbar('high_green', 'sliders',
                          self.thresholds['high_green'], 255,
                          self.change_high_green)
        cv.CreateTrackbar('low_blue', 'sliders', self.thresholds['low_blue'],\
                          255, self.change_low_blue)
        cv.CreateTrackbar('high_blue', 'sliders', self.thresholds['high_blue'],\
                          255, self.change_high_blue)    
#        cv.CreateTrackbar('low_hue', 'sliders', self.thresholds['low_hue'],\
#                          255, self.change_low_hue)
#        cv.CreateTrackbar('high_hue', 'sliders', self.thresholds['high_hue'],\
#                          255, self.change_high_hue)
#        cv.CreateTrackbar('low_sat', 'sliders', self.thresholds['low_sat'],\
#                          255, self.change_low_sat)
#        cv.CreateTrackbar('high_sat', 'sliders', self.thresholds['high_sat'],\
#                          255, self.change_high_sat)
#        cv.CreateTrackbar('low_val', 'sliders', self.thresholds['low_val'],\
#                          255, self.change_low_val)
#        cv.CreateTrackbar('high_val', 'sliders', self.thresholds['high_val'],\
#                          255, self.change_high_val)
                          
    #Functions for changing the slider values  
    def change_low_red(self, new_threshold):
        self.thresholds['low_red'] = new_threshold
        
    def change_high_red(self, new_threshold):
        self.thresholds['high_red'] = new_threshold
        
    def change_low_green(self, new_threshold):
        self.thresholds['low_green'] = new_threshold
        
    def change_high_green(self, new_threshold):
        self.thresholds['high_green'] = new_threshold
        
    def change_low_blue(self, new_threshold):
        self.thresholds['low_blue'] = new_threshold
        
    def change_high_blue(self, new_threshold):
        self.thresholds['high_blue'] = new_threshold
        
#    def change_low_hue(self, new_threshold):
#        self.thresholds['low_hue'] = new_threshold
#        
#    def change_high_hue(self, new_threshold):
#        self.thresholds['high_hue'] = new_threshold
#        
#    def change_low_sat(self, new_threshold):
#        self.thresholds['low_sat'] = new_threshold
#        
#    def change_high_sat(self, new_threshold):
#        self.thresholds['high_sat'] = new_threshold
#        
#    def change_low_val(self, new_threshold):
#        self.thresholds['low_val'] = new_threshold
#        
#    def change_high_val(self, new_threshold):
#        self.thresholds['high_val'] = new_threshold
        
    def check_key_press(self, key_press):
        if key_press == 113: #113 = q
            print 'quitting'
            rospy.signal_shutdown( "Quit requested from keyboard" )
            
        if key_press == 115: #115 = s
            print 'saving'
            f = open("thresholds.txt","w")
            print >> f, "low_red = ", self.thresholds['low_red']
            print >> f, "high_red = ", self.thresholds['high_red']
            print >> f, "low_green = ", self.thresholds['low_green']
            print >> f, "high_green = ", self.thresholds['high_green']
            print >> f, "low_blue = ", self.thresholds['low_blue']
            print >> f, "high_blue = ", self.thresholds['high_blue']
            print >> f, "low_hue = ", self.thresholds['low_hue']
            print >> f, "high_hue = ", self.thresholds['high_hue']
            print >> f, "low_sat = ", self.thresholds['low_sat']
            print >> f, "high_sat = ", self.thresholds['high_sat']
            print >> f, "low_val = ", self.thresholds['low_val']
            print >> f, "high_val = ", self.thresholds['high_val']
            f.close()

        if key_press == 108: #108 = l
            print "loading thresholds.txt"
            f = open("thresholds.txt","r")
            L = f.readlines()
            
            #Put each of the saved threshold values into the dictionary
            for line in L:
                pieces = line.split() #gives ['name', '=', 'value']
                self.thresholds[pieces[0]] = int(pieces[2])                
            
            #Recreate the slider window
            cv.DestroyWindow('sliders')
            self.make_slider_window()
            
            self.RGBavgs = ((self.thresholds['high_red'] + 
                             self.thresholds['low_red'])/2,
                            (self.thresholds['high_green'] + 
                             self.thresholds['low_green'])/2,
                            (self.thresholds['high_blue'] + 
                             self.thresholds['low_blue'])/2)
                             
            print self.RGBavgs
#            self.HSVavgs = self.rgb_to_hsv(self.RGBavgs)
#            print self.HSVavgs
                             
            self.RGBvals = [(self.RGBavgs[0], self.RGBavgs[1], self.RGBavgs[2])]
#            self.HSVvals = [(self.HSVavgs[0], self.HSVavgs[1], self.HSVavgs[2])]            
           
        if key_press == 114: # 114 = r
            print "resetting RGBvals, RGBavgs"
            self.RGBavgs = ()
            self.RGBvals = []
#            self.HSVavgs = ()
#            self.HSVvals = []
            
        if key_press == 99: # 99 = c
            print "recoloring by rgb, rgb = ", self.new_color
            self.change_by_rgb()
            
        if key_press == 98: # 98 = b
            print "recoloring by hue, hue = ", self.hue
            self.change_by_hue()
        
        if key_press == 97: # a
            print "recoloring by hsv. hsv = ", self.new_hsv
            self.change_by_hsv()
            
        if key_press == 100: #101 = d
            self.hue = float(raw_input("enter new hue: "))
        
        if key_press == 101: #101 = e
             vals = raw_input("enter rgb vals separated by commas: ")
             print vals
             vals = vals.split(',')
             print vals

             self.new_color = (int(vals[0].strip()),
                               int(vals[1].strip()),
                               int(vals[2].strip()))
                               
             self.new_hsv = self.rgb_to_hsv(self.new_color)
             self.hue = self.new_hsv[0]
             print self.new_hsv
             print self.new_color
            
        if key_press == 111: # o
            cv.Copy(self.image_orig, self.image_color)
            
            
    def change_by_rgb(self):
        avgs = self.get_avgs(self.image_color)
        for x in range(self.threshold.width):
            for y in range(self.threshold.height):
                if cv.Get2D(self.threshold,y,x)[0] == 255:
                    val = cv.Get2D(self.image_color,y,x)
                    difs = (val[2] - avgs[0],
                            val[1] - avgs[1],
                            val[0] - avgs[2])
                    cv.Set2D(self.image_color,y,x, (self.new_color[2] + difs[2],
                                                    self.new_color[1] + difs[1],
                                                    self.new_color[0] + difs[0],
                                                    0))
        
    def change_by_hue(self):
        for x in range(self.threshold.width):
            for y in range(self.threshold.height):
                if cv.Get2D(self.threshold,y,x)[0] == 255:
                    val = cv.Get2D(self.hsv,y,x)
                    cv.Set2D(self.hsv,y,x, (self.hue, val[1], val[2]))
        cv.CvtColor(self.hsv, self.image_color, cv.CV_HSV2BGR)
        
    def change_by_hsv(self):
        avgs = self.get_avgs(self.hsv)
        
        for x in range(self.threshold.width):
            for y in range(self.threshold.height):
                if cv.Get2D(self.threshold,y,x)[0] == 255:
                    val = cv.Get2D(self.hsv,y,x)
                    difs = (val[0] - avgs[0],
                            val[1] - avgs[1],
                            val[2] - avgs[2])
                    cv.Set2D(self.hsv,y,x, (self.new_hsv[0] + difs[0], 
                                            self.new_hsv[1] + difs[1], 
                                            self.new_hsv[2] + difs[2]))
        cv.CvtColor(self.hsv, self.image_color, cv.CV_HSV2BGR)

    def get_avgs(self, image):
        c = 0
        s = (0,0,0)
        for x in range(image.width):
            for y in range(image.height):
                if cv.Get2D(self.threshold,y,x)[0] == 255:
                    vals = cv.Get2D(image,y,x)
                    s = (s[0] + vals[0], s[1] + vals[1], s[2] + vals[2])
                    c += 1
        s = (s[0]/c, s[1]/c, s[2]/c)
        print "returning averages: ", s
        return s
                    
    def rgb_to_hsv(self, rgb):
        r = rgb[0]/255.0
        g = rgb[1]/255.0
        b = rgb[2]/255.0
        
        RGBmin = min( r, g, b )
        RGBmax = max( r, g, b )
        
        v = RGBmax*255
        
        delta = RGBmax - RGBmin
        print delta
        
        if delta == 0:
            s = 0
            h = 0
            return (h,s,v)

        if( RGBmax != 0 ):
            s = delta / RGBmax
            s *= 0.0
            print s
    
        else:
            s = 0
            h = 0
            print "returning 0s"            
            return (h,s,v)
    
        if( r == RGBmax ):
            h = ( g - b ) / delta
            print "red",h
        elif( g == RGBmax ):
            h = 2 + ( b - r ) / delta
            print "green",h
        else:
            h = 4 + ( r - g ) / delta
            print "blue",h
        h *= 60.0
        if( h < 0 ):
            h += 360.0
        print "degrees",h
        h *= (180.0/360.0)
        print "Returning ",(h,s,v)
        
        return (h,s,v)                                                   

    def find_blob(self):       
        
        #Convert Incoming image
        #self.image = self.bridge.imgmsg_to_cv(data, "bgr8")
        
        #self.image = cv.QueryFrame(self.capture)
        
        cv.Copy(self.image_color, self.image)
        
        #These shenanigans are to get input from the keyboard, cv.WaitKey gives
        #back the ascii value of the key pressed in the low 8 bits, but the rest
        #of the higher bits can be anything apparently. 
        key_press_raw = cv.WaitKey(5) #gets a raw key press
        key_press = key_press_raw & 255 #sets all but the low 8 bits to 0

        
        self.check_key_press(key_press)
        
        
        #Create the thresholded image
        self.threshold = self.create_image()
        
        #Find blob regions, draw a rectangle around the largest and a circle at
        #its center.
        self.find_regions()
        
        #Display the images
        cv.ShowImage('image', self.image)
        
        cv.ShowImage('threshold', self.threshold)
        
        cv.ShowImage('hsv', self.hsv)
        
    def create_image(self):
        
        #Find the size of the image
        
        #Create images for each channel
        blue = cv.CreateImage(self.size, 8, 1) 
        red = cv.CreateImage(self.size, 8, 1)
        green = cv.CreateImage(self.size, 8, 1)
    
        hue = cv.CreateImage(self.size, 8, 1)
        sat = cv.CreateImage(self.size, 8, 1)
        val = cv.CreateImage(self.size, 8, 1)

        #Create an image to be returned and eventually displayed
        thresholds = cv.CreateImage(self.size, 8, 1)
        
        #Create images to save the thresholded images to
        red_threshed = cv.CreateImage(self.size, 8, 1)
        green_threshed = cv.CreateImage(self.size,8,1)
        blue_threshed = cv.CreateImage(self.size, 8, 1) 

        hue_threshed = cv.CreateImage(self.size, 8, 1)    
        sat_threshed = cv.CreateImage(self.size,8,1)
        val_threshed = cv.CreateImage(self.size, 8, 1)

        #Split the image up into channels, saving them in their respective image
        cv.Split(self.image, blue, green, red, None)
        cv.CvtColor(self.image, self.hsv, cv.CV_RGB2HSV)
        cv.Split(self.hsv, hue, sat, val, None)
        
        #Threshold the images based on the slider values
        cv.InRangeS(red, self.thresholds['low_red'],\
                    self.thresholds['high_red'], red_threshed)
        cv.InRangeS(green, self.thresholds['low_green'],\
                    self.thresholds['high_green'], green_threshed)
        cv.InRangeS(blue, self.thresholds['low_blue'],\
                    self.thresholds['high_blue'], blue_threshed)

        cv.InRangeS(hue, self.thresholds['low_hue'],\
                    self.thresholds['high_hue'], hue_threshed)
        cv.InRangeS(sat, self.thresholds['low_sat'],\
                    self.thresholds['high_sat'], sat_threshed)
        cv.InRangeS(val, self.thresholds['low_val'],\
                    self.thresholds['high_val'], val_threshed)
                    
        #Recombine all of the thresholded images into one image
        cv.Mul(red_threshed, green_threshed, thresholds)
        cv.Mul(thresholds, blue_threshed, thresholds)
        cv.Mul(thresholds, hue_threshed, thresholds)
        cv.Mul(thresholds, sat_threshed, thresholds)
        cv.Mul(thresholds, val_threshed, thresholds)
        
        #Erode and Dilate shave off and add edge pixels respectively
        cv.Erode(thresholds, thresholds, iterations = 1)
        cv.Dilate(thresholds, thresholds, iterations = 1)

        return thresholds

    def find_regions(self):
    
        #Create a copy image of thresholds then find contours on that image
        storage = cv.CreateMemStorage(0)
        storage1 = cv.CreateMemStorage(0)
        copy = cv.CreateImage(self.size, 8, 1)
        cv.Copy( self.threshold, copy )
        contours = cv.FindContours(copy, storage, cv.CV_RETR_EXTERNAL,\
                                   cv.CV_CHAIN_APPROX_SIMPLE)
                                   
        #Find the largest contour
        if len(contours)>0:
            biggest = contours
            biggestArea=cv.ContourArea(contours)
            while contours!=None:
                nextArea=cv.ContourArea(contours)
                if biggestArea < nextArea:
                    biggest = contours
                    biggestArea = nextArea
                contours=contours.h_next()

            #print biggest
#            after_biggest = biggest.h_next()
#            after_biggest = None
            
            #Get a bounding rectangle for the largest contour
            br =cv.BoundingRect(biggest,update=0) 
            
            #self.tree = cv.CreateContourTree(biggest, storage1, 0)
            
            #print self.contour_tree
            
            #Find the middle of it
            circle_x = br[0]+br[2]/2
            circle_y = br[1]+br[3]/2
            
            #Create a blob message and publish it.
#            blob = Blob( br[0], br[1], br[2], br[3], circle_x, circle_y)
#            self.publish(blob)   
            
            #Find the coordinates for each corner of the box
            box_tl = (br[0],br[1])
            box_tr = (br[0]+br[2],br[1])
            box_bl = (br[0],br[1]+br[3])
            box_br = (br[0]+br[2],br[1]+br[3])
            
            #Draw the box
            cv.PolyLine(self.image,[[box_tl, box_bl, box_br, box_tr]],\
                        1, cv.RGB(255, 0, 0))
                        
            #Draw the circle
            cv.Circle(self.image,(circle_x, circle_y), 10, cv.RGB(255, 0, 0),\
                      thickness=1, lineType=8, shift=0)
            
            #Draw the contours
            cv.DrawContours(self.image, biggest, cv.RGB(255,255,255),
                            cv.RGB(0, 255, 0), 1, thickness=2, lineType=8,
                            offset=(0, 0))    
                            
                            
if __name__ == "__main__":
    """Main function, sets up stuff the class needs to run and runs it"""
    
    #Initialize our node
    #rospy.init_node('blobFinder')
    
    #Create a BlobFinder
    bf = BlobFinder()
    while True:
        bf.find_blob()
    #Subscribe to the image_color topic
    #rospy.Subscriber('/camera/rgb/image_color', sm.Image, bf.find_blob)
    
    #Run until soemthing stops us
    #rospy.spin()
