import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Check if the webcam is opened correctly
if not cap.isOpened():
    raise IOError("Cannot open webcam")

while True:
    width,height = 640,480 #default is 640*480
    upscaling = width>640 or height>480
    downscaling = width<640 or height<480

    ret, frame = cap.read()
    
    if (width,height) != (640,480):
        if downscaling: frame = cv2.resize(frame, dsize=(width,height), interpolation=cv2.INTER_AREA)
        #falls beide aufgerufen werden lieber gutes upscaling als letztes nutzen.
        if upscaling: frame = cv2.resize(frame, dsize=(width,height), interpolation=cv2.INTER_CUBIC)
    
    def transform(frame):
        #INSERT INTERISTING FEED-MANIPULATION!
        #frame = np.concatenate((frame,frame),axis=1)
        #frame = np.concatenate((frame,frame),axis=0)
        return frame
    frame = transform(frame)
    
    cv2.imshow('Input', frame)

    c = cv2.waitKey(1) #ms between frames
    if c == 27: #Esc
        break

cap.release()
cv2.destroyAllWindows()