# import required libraries
import cv2
from vidgear.gears import VideoGear

# enable enablePiCamera boolean flag to access PiGear API backend
stream = VideoGear(enablePiCamera=True).start()

# loop over
while True:
    # read frames from stream
    frame = stream.read()

    # check for frame if Nonetype
    if frame is None:
        break

    # {do something with the frame here}

    # Show output window
    cv2.imshow("Output Frame", frame)

    # check for 'q' key if pressed
    key = cv2.waitKey(1) & 0xFF
    if key == ord("q"):
        break

# close output window
cv2.destroyAllWindows()

# safely close video stream
stream.stop()
