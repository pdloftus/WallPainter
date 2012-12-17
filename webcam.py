from cv import *

NamedWindow('camera')
capture = CaptureFromCAM(0)

while True:    
    image = QueryFrame(capture)
    ShowImage('camera', image)
    WaitKey(5)
