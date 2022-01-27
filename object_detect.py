from imutils.video import VideoStream
from imutils.video import FPS
import numpy as np
import imutils
import time
import cv2
import os

# initialize the video stream
print("[INFO] starting video stream...")
vs = VideoStream(src=1).start()
fps = FPS().start()

# loop over the frames from the video stream
while True:
    # grab the frame from the threaded video stream and resize it
    # to have a maximum width of 400 pixels
    frame = vs.read()
    frame = imutils.resize(frame, width=600)

    start = time.time()
    sum = 0
    N = 300
    for i in range(0, N):
        for j in range(0, N):
            sum += 1
    end = time.time()

    seconds = end - start

    frps = 1 / seconds


    cv2.putText(frame, str(round(frps,2)), (10,350), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255,255,255))

    # show the output frame
    cv2.imshow("Frame", frame)
    key = cv2.waitKey(1) & 0xFF

    fps.update()

    # if the `q` key was pressed, break from the loop
    if key == ord("q"):
        break


fps.stop()
print("[INFO] elasped time: {:.2f}".format(fps.elapsed()))
print("[INFO] approx. FPS: {:.2f}".format(fps.fps()))
# do a bit of cleanup
cv2.destroyAllWindows()
vs.stop()