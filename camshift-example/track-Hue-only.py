import numpy as np
import argparse
import cv2
import imutils

# initialize global variable
# - video frame
# - ROI points
# - flag to know if input mode is active
frame = None
roiPts = []
inputMode = False


# Selection of the object to track
def selectROI(event, x, y, flags, param):
    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode

    # if we are in ROI selection mode, the mouse was clicked,
    # and we do not already have four points, then update the
    # list of ROI points with the (x, y) location of the click
    # and draw the circle around the pint clicked
    if inputMode and event == cv2.EVENT_LBUTTONDOWN and len(roiPts) < 4:
        roiPts.append((x, y))
        cv2.circle(frame, (x, y), 4, (0, 255, 0), 2) # draw a green circle
        cv2.imshow("frame", frame)


def main():
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("-v", "--video",
                    help="path to the (optional) video file")
    args = vars(ap.parse_args())

    # grab the reference to the current frame, list of ROI
    # points and whether or not it is ROI selection mode
    global frame, roiPts, inputMode

    # if the video path was not supplied, grab the reference to the
    # camera
    if not args.get("video", False):
        camera = cv2.VideoCapture(0)

    # otherwise, load the video
    else:
        camera = cv2.VideoCapture(args["video"])

    # setup the mouse callback to grab the clicks to define ROI
    cv2.namedWindow("frame")
    cv2.setMouseCallback("frame", selectROI)

    # initialize the termination criteria for cam shift, indicating
    # a maximum of ten iterations or movement by a least one pixel
    # along with the bounding box of the ROI
    termination = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 1)
    roiBox = None

    # keep looping over the frames
    while True:
        # grab the current frame
        (grabbed, frame) = camera.read()

        # resize frame
        frame = imutils.resize(frame, width=800)
        # check to see if we have reached the end of the video
        if not grabbed:
            break

        # if the see if the ROI has been computed
        if roiBox is not None:
            # convert the current frame to the HSV color space
            # and perform mean shift
            hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

            # One dimension back-projection (Hue only)
            backProj = cv2.calcBackProject([hsv], [0], roiHist, [0, 179], 1)

            # Show back-projection image result
            # cv2.imshow("backProjection", backProj)

            # apply cam shift to the back projection, convert the
            # points to a bounding box, and then draw them
            (r, roiBox) = cv2.CamShift(backProj, roiBox, termination)
            pts = np.int0(cv2.boxPoints(r))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 2)

        # show the frame and record if the user presses a key
        cv2.imshow("frame", frame)
        key = cv2.waitKey(1) & 0xFF

        # handle if the 'i' key is pressed, then go into ROI
        # selection mode
        if key == ord("i") and len(roiPts) < 4:
            # indicate that we are in input mode and clone the
            # frame (to keep original since we later write on it.)
            inputMode = True
            orig = frame.copy()

            # keep looping until 4 reference ROI points have
            # been selected; press any key to exit ROI selction
            # mode once 4 points have been selected
            while len(roiPts) < 4:
                cv2.imshow("frame", frame)
                cv2.waitKey(0)

            # determine the top-left and bottom-right points
            # Top Left is the minimum if the sum, Bottom Right is the max
            # (this is true for a somewhat rectangular shape)
            roiPts = np.array(roiPts)
            s = roiPts.sum(axis=1)
            tl = roiPts[np.argmin(s)]
            br = roiPts[np.argmax(s)]

            # store bounding box
            roiBox = (tl[0], tl[1], br[0], br[1])  # grab the ROI for the bounding box and convert it

            # crop image and convert to the HSV color space (Hue-Saturation-Value)
            roi = orig[tl[1]:br[1], tl[0]:br[0]]
            roi = cv2.cvtColor(roi, cv2.COLOR_BGR2HSV)
            # optional blurring to smooth the histogram
            roi = cv2.GaussianBlur(roi, (21, 21), 0)

            # show histogram
            # cv2.imshow("histogram", roi)

            # compute a HSV histogram for the ROI
            # 1D histogram using only channel 0 (H-Hue)
            roiHist = cv2.calcHist([roi], [0], None, [6], [0, 180])

            # normalize histogram to 0-255 uint8 space
            roiHist = cv2.normalize(roiHist, roiHist, 0, 255, cv2.NORM_MINMAX)

        # if the 'q' key is pressed, stop the loop
        elif key == ord("q"):
            break

    # cleanup the camera and close any open windows
    camera.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
