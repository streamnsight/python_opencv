import imutils
import cv2
import argparse


ap = argparse.ArgumentParser()
ap.add_argument("-v", "--video",
                help="path to the (optional) video file")
args = vars(ap.parse_args())

# Alternate haar cascade models
# haarcascade_frontalface_default.xml
# haarcascade_frontalface_alt2.xml

face_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.1.0/share/OpenCV/haarcascades/haarcascade_frontalface_alt.xml')
# profile_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.1.0/share/OpenCV/haarcascades/haarcascade_profileface.xml')
# eye_cascade = cv2.CascadeClassifier('/usr/local/Cellar/opencv3/3.1.0/share/OpenCV/haarcascades/haarcascade_eye.xml')


# if a video path was not supplied, grab the reference
# to the webcam

if not args.get("video", False):
    camera = cv2.VideoCapture(0)

# otherwise, grab a reference to the video file
else:
    camera = cv2.VideoCapture(args["video"])

# loop through frames
while True:
    # grab the current frame
    (grabbed, frame) = camera.read()

    # if we are viewing a video and we did not grab a frame,
    # then we have reached the end of the video
    if args.get("video") and not grabbed:
        break

    # resize the frame, blur it, and convert it grayscale
    frame = imutils.resize(frame, width=600)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # flip the video for profile detection
    # gray_flipped = cv2.flip(gray,1)

    # apply Haar Cascade model to the image
    # scale should be more than 1. The closer to 1 the more faces will be detected but more potential errors and slower
    # minNeighbors helps discriminate by distance between faces detected
    # minSize defines the smallest size to detect
    # outputs a list of rectangles detected
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30,30))

    # detect profiles: the model only detects left profiles so we use the flipped image to detect right profiles
    # profilesR = profile_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))
    # profilesL = profile_cascade.detectMultiScale(gray_flipped, scaleFactor=1.3, minNeighbors=5, minSize=(30, 30))

    for (x, y, w, h) in faces:
        # draw the rectangle around the face
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

        # detect the eyes
        # roi_gray = gray[y:y + h, x:x + w]
        # roi_color = frame[y:y + h, x:x + w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    '''
    # do the same for profiles
    for (x, y, w, h) in profilesR:
        # print("in faces")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # roi_gray = gray[y:y + h, x:x + w]
        # roi_color = frame[y:y + h, x:x + w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)

    for (x, y, w, h) in profilesL:
        # print("in faces")
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)
        # roi_gray = gray[y:y + h, x:x + w]
        # roi_color = frame[y:y + h, x:x + w]
        # eyes = eye_cascade.detectMultiScale(roi_gray)
        # for (ex, ey, ew, eh) in eyes:
        #    cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (0, 255, 0), 2)
    '''

    # show the frame with the drawn rectangle(s)
    cv2.imshow("Frame", frame)

    # check for keypressed
    key = cv2.waitKey(1) & 0xFF

    # if the 'q' key is pressed, stop the loop
    if key == ord("q"):
        break

# cleanup the camera and close any open windows
camera.release()
cv2.destroyAllWindows()
