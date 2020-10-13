"""
    File name: Main.py
    Author: Ryan Fischback
    Date created: 5/13/2019
    Date last modified: 6/12/2019
"""
import imutils
import cv2
from imutils.video import VideoStream
from newObject import *
from CentroidTracker import *
from schedule import default_scheduler, time
import datetime
import requests
import argparse

ap = argparse.ArgumentParser()

ap.add_argument("-a", nargs='+', type=int, default=(0, 45, 0), help="Lower Color Range (HSV)")
ap.add_argument("-b", nargs='+', type=int, default=(16, 255, 255), help="Upper Color Range (HSV)")
ap.add_argument("-c", type=int, default=0, help="Camera option. 0 or 1 should work (default=0)")
ap.add_argument("-d", type=str, help="IP Address of the Arduino Webserver")
ap.add_argument("-e", type=int, help="Minimum area for object to be identified", default=100)
ap.add_argument("-f", type=int, default=60, help="Time in between checking 60 seconds default")
ap.add_argument("-g", type=int, default=15, help="Number of Objects in a minute that is considered too many")
ap.add_argument("-z", type=int, default=1000, help="Contour Area that is TOO high to be one object")

args = vars(ap.parse_args())

width = 0  # variable for width
height = 0  # variable for height
camera = VideoStream(src=args["c"]).start()  # start the camera
time.sleep(2)
tracked_objects = {}  # stored objs
ct = CentroidTracker(maxDisappeared=1, maxDistance=50)  # creating the CT ... update method
objCnt = 0  # temp cnt
totalObjCnt = 0  # total objs
watch1_start = datetime.time(23, 59, 59)
watch1_end = datetime.time(5, 59, 59)
watch2_start = datetime.time(6, 00)
watch2_end = datetime.time(11, 59, 59)
watch3_start = datetime.time(12, 00)
watch3_end = datetime.time(17, 59, 59)
watch4_start = datetime.time(18, 00)
watch4_end = datetime.time(23, 59, 58)


def write_to_log(filename, output):
    now = datetime.datetime.now()
    if is_time_between(watch1_start, watch1_end):
        try:
            f = open("Logs/" + filename, "a")
            f.write(str(output) + ",\t" + now.strftime("%m/%d/%Y") + ",\t" + now.strftime("%H:%M:%S") + ",\t" + "watch1\n")
            f.close()
        except FileNotFoundError:
            print("File was not found. Is LOGS inside of the same directory as Main.exe?")
    elif is_time_between(watch2_start, watch2_end):
        try:
            f = open("Logs/" + filename, "a")
            f.write(str(output) + ",\t" + now.strftime("%m/%d/%Y") + ",\t" + now.strftime("%H:%M:%S") + ",\t" + "watch2\n")
            f.close()
        except FileNotFoundError:
            print("File was not found. Is LOGS inside of the same directory as Main.exe?")
    elif is_time_between(watch3_start, watch3_end):
        try:
            f = open("Logs/" + filename, "a")
            f.write(str(output) + ",\t" + now.strftime("%m/%d/%Y") + ",\t" + now.strftime("%H:%M:%S") + ",\t" + "watch3\n")
            f.close()
        except FileNotFoundError:
            print("File was not found. Is LOGS inside of the same directory as Main.exe?")
    elif is_time_between(watch4_start, watch4_end):
        try:
            f = open("Logs/" + filename, "a")
            f.write(str(output) + ",\t" + now.strftime("%m/%d/%Y") + ",\t" + now.strftime("%H:%M:%S") + ",\t" + "watch4\n")
            f.close()
        except FileNotFoundError:
            print("File was not found. Is LOGS inside of the same directory as Main.exe?")


def exit_program_write(filename, output):
    now = datetime.datetime.now()
    try:
        f = open("Logs/" + filename, "a")
        f.write(str(output) + ",\t" + now.strftime("%m/%d/%Y") + ",\t" + now.strftime("%H:%M:%S") + ",\t" + "Final runtime count\n")
        f.close()
    except FileNotFoundError:
        print("File not found in Logs/filename. Couldn't write")


def is_time_between(begin_time, end_time, check_time=None):
    # If check time is not given, default to current time
    check_time = check_time or datetime.datetime.now().time()
    if begin_time < end_time:
        return check_time >= begin_time and check_time <= end_time
    else: # crosses midnight
        return check_time >= begin_time or check_time <= end_time


def crosses(y, middleLine):
    """
    crosses mid line
    :param y:
    :param middleLine:
    :return:
    """
    absDis = abs(y - middleLine)
    if absDis <= 25:  # if the distance from cY (center object Y value) is really close to middleLine then count it
        return 1
    else:
        return 0


def check():
    if objCnt < args["g"]:
        print("Safe", objCnt)
        try:
            url = "http://"+args["d"]+"/?off"  # ex: http://10.100.134.200/?off is what this will turn into
            requests.get(url, allow_redirects=False)  # requests the URL. &requires internet
            write_to_log("Log.txt", objCnt)
        except:
            write_to_log("Log.txt", objCnt)
    else:
        print("Too many", objCnt)
        try:
            url = "http://"+args["d"]+"/?on"
            requests.get(url, allow_redirects=False)
            write_to_log("Log.txt", objCnt)
        except:
            write_to_log("Log.txt", objCnt)


def reset_cnt():
    global objCnt
    objCnt = 0
    return objCnt


default_scheduler.every(args["f"]).seconds.do(check)
default_scheduler.every(args["f"]).seconds.do(reset_cnt)
print("Starting...")

while True:
    frame = camera.read()  # read camera

    if frame is None:
        print('fail with camera. Is it being used? src # correct?')
        break

    frame = imutils.resize(frame, width=400)  # resize frame
    height = np.size(frame, 0)  # calculates the height of frame
    width = np.size(frame, 1)  # calculates the width of frame
    blurred = cv2.GaussianBlur(frame, (21, 21), 0)  # blurring image before hsv applied (less noise)
    hsv = cv2.cvtColor(blurred, cv2.COLOR_BGR2HSV)  # creating hsv from blurred frame and converting the bgr to hsv

    mask = cv2.inRange(hsv, np.array(args["a"]), np.array(args["b"]))  # mask is setting hsv in range of the lower and upper HSV values
    mask = cv2.dilate(mask, None, iterations=2)  # dilate is opposite of erosion "thickens" image
    mask = cv2.erode(mask, None, iterations=2)  # erode "thins" image. erosion followed by dilation to remove white noises
    res = cv2.bitwise_and(frame, frame, mask=mask)  # this makes the color filter show that color in the res frame

    contours = cv2.findContours(mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)  # find contours of mask
    contours = imutils.grab_contours(contours)  # get them

    middleLine = (height // 2)  # calculate the middleLine
    cv2.line(frame, (0, middleLine), (width, middleLine), (100, 200, 100), 2)  # // = int division | draw the line
    rects = []  # empty rects
    areas = []

    if len(contours) > 0:  # don't pass in empty contour!!!
        for c in contours:  # loop through them
            if cv2.contourArea(c) < args["e"]:  # not big enough to be considered an object
                continue  # go next
            (x, y, w, h) = cv2.boundingRect(c)  # create rect for the object
            endX = x + w
            endY = y + h
            startX = x
            startY = y
            rects.append((startX, startY, endX, endY))  # append all of these objects rects to be compared in update
            if cv2.contourArea(c) not in areas and cv2.contourArea(c) >= args["z"]:
                areas.append(cv2.contourArea(c))

        objects = ct.update(rects)  # update compares centroids using eucludian distance formula and registers/deregisters

        for (objectID, centroid) in objects.items():
            obj = tracked_objects.get(objectID, None)  # if it exists then cool.. check if its been counted

            if obj is None:
                obj = newObject(objectID, centroid)
            else:

                obj.centroids.append(centroid)  # append the objects centroid in the centroids list
                if not obj.counted:
                    if crosses(centroid[1], middleLine):
                        objCnt += 1
                        totalObjCnt += 1
                        obj.counted = True
                        for i in areas:
                            write_to_log("Big.txt", i)
                            areas.remove(i)  # might be redundant

            tracked_objects[objectID] = obj
            text = "ID {}".format(objectID)
            cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 0, 255), -1)

    res = imutils.resize(res, width=400)  # resize mask frame
    cv2.imshow("Computers POV", res)  # show res frame
    cv2.putText(frame, "Current: {}".format(objCnt), (10, 30),  # object counter on top left
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.putText(frame, ("Total: {}".format(totalObjCnt)), (10, 270),  # object counter on bottom left
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    cv2.imshow("Unfiltered Frame", frame)  # shows frame
    if cv2.waitKey(1) == ord("b"):  # press b to exit
        break

    default_scheduler.run_pending()

print("Exiting...")
exit_program_write("Exitcount.txt", totalObjCnt)
camera.stop()
cv2.destroyAllWindows()
