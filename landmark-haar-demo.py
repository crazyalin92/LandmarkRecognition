# -*- coding: utf-8 -*-
__author__ = 'zBritva'

import cv2
import numpy as np
from math import fabs
from lib import contour_processor

# camera
cap = cv2.VideoCapture(0)

# image data of leard (helipad, landmark)
cascade = cv2.CascadeClassifier('./train_data/train3/H-helipad-2/cascade.xml')
cp = contour_processor.ContourProcessor()
kernel = np.ones((3, 3), np.uint8)

if cascade.empty():
    print 'CASCADE IS EMPTY'
    exit(-1)

# print 'HAAR' if cascade.getFeatureType() == 0 else 'LBP'



while (True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # cv2.imshow('frame', frame)

    #
    try:
        # print 'frame'
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    except:
        print 'Get frame ERROR'
        continue
    # gray = (255-gray)
    #
    # gray = frame
    #

    # gray = cv2.medianBlur(gray, 3)

    # kernel = np.ones((3, 3), np.uint8)
    # opening = cv2.morphologyEx(gray, cv2.MORPH_OPEN, kernel, iterations=1)

    # # sure background area
    # gray = cv2.dilate(opening, kernel, iterations=1)

    # # convert to im = np.array(float_img * 255, dtype = np.uint8)
    # gray = np.array(gray * 255, dtype=np.uint8)

    # im2, contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


    # gray = (255-gray)

    # simple
    gray_tr = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    _, binary = cv2.threshold(gray_tr, 127, 255, cv2.THRESH_BINARY)

    # adaptive
    # binary = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
    #                              cv2.THRESH_BINARY, 11, 2)


    opening = cv2.morphologyEx(binary, cv2.MORPH_OPEN, kernel, iterations=1)
    bin_res = cv2.dilate(opening, kernel, iterations=1)

    binary_result = cv2.medianBlur(bin_res, 3)
    marks = cascade.detectMultiScale(binary_result, 3.8, 3)

    # filter detections

    # for (x, y, w, h) in marks:
    #     roi = gray[y:y+h, x:x+w]
    #
    #     roi = cv2.medianBlur(roi, 3)
    #
    #     _, roi_gray = cv2.threshold(roi, 70, 225, cv2.THRESH_BINARY_INV)
    #
    #     opening = cv2.morphologyEx(roi_gray, cv2.MORPH_OPEN, kernel, iterations=1)
    #     roi_gray = cv2.dilate(opening, kernel, iterations=1)

    #
    # cv2.imshow('rio', roi_gray)
    #
    #     break
    #
    #     print 'rio'
    #
    #     # sleep(15)
    #
    # sleep(15)

    # end filter of detection

    # TODO 1. дописать поиск каскадом хаара
    # TODO 2. внутри области детектирования, провести контурный анализ

    if False:

        for (x, y, w, h) in marks:
            # cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

            roi = frame[y:y+h, x:x+w]

            # debug
            # while(True):
            #     if cv2.waitKey(1) & 0xFF == ord('c'):
            #         break

            gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

            _, binary_roi = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)


            cv2.imshow('frame3', roi)
            cv2.imshow('frame4', binary_roi)

            im2, contours, hierarchy = cv2.findContours(binary_roi, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

            for contour in contours:
                contour = cv2.approxPolyDP(contour, 2, True)

                if len(contour) > 5 and fabs(cv2.arcLength(contour, True)) > 20:
                    # x, y, width, height = cv2.boundingRect(contour)
                    # roi = frame[y:y+height, x:x+width]
                    #shift contour
                    # contour = cp.shiftContour(contour, x, y)

                    rect = cv2.minAreaRect(contour)

                    box = cv2.boxPoints(rect)
                    box = np.int0(box)
                    # cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                    # cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                    h_mark_points = cp.getBoxROI(box)
                    result = cp.checkBoxROI(binary_roi, h_mark_points, True)

                    if result:
                        cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                    else:
                        for point in box:
                            point[0] += x
                            point[1] += y

                        cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

                        for point in h_mark_points:
                            point[0] += x
                            point[1] += y

                        cv2.circle(frame, (h_mark_points[0][0], h_mark_points[0][1]), 3, (255, 0, 0), 5)
                        cv2.circle(frame, (h_mark_points[1][0], h_mark_points[1][1]), 3, (0, 255, 0), 5)
                        cv2.circle(frame, (h_mark_points[2][0], h_mark_points[2][1]), 3, (0, 0, 255), 5)
                        cv2.circle(frame, (h_mark_points[3][0], h_mark_points[3][1]), 3, (255, 255, 0), 5)
                        cv2.circle(frame, (h_mark_points[4][0], h_mark_points[4][1]), 3, (255, 0, 255), 5)
                        cv2.circle(frame, (h_mark_points[5][0], h_mark_points[5][1]), 3, (0, 255, 255), 5)
                        cv2.circle(frame, (h_mark_points[6][0], h_mark_points[6][1]), 3, (255, 100, 255), 5)
                        cv2.circle(frame, (h_mark_points[7][0], h_mark_points[7][1]), 3, (100, 255, 255), 5)


        # ret,frameOut = cv2.threshold(gray,127,255,cv2.THRESH_BINARY)

        # gray_roi = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        #
        # _, binary_roi = cv2.threshold(gray_roi, 127, 255, cv2.THRESH_BINARY)

    if True:
        im2, contours, hierarchy = cv2.findContours(binary_result, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)

        for contour in contours:
            contour = cv2.approxPolyDP(contour, 2, True)

            if len(contour) > 5 and fabs(cv2.arcLength(contour, True)) > 20:
                # x, y, width, height = cv2.boundingRect(contour)
                # roi = frame[y:y+height, x:x+width]
                #shift contour
                # contour = cp.shiftContour(contour, x, y)

                rect = cv2.minAreaRect(contour)

                box = cv2.boxPoints(rect)
                box = np.int0(box)
                # cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)
                # cv2.drawContours(frame, [contour], -1, (0, 255, 0), 3)
                h_mark_points = cp.getBoxROI(box)
                result = cp.checkBoxROI(binary_result, h_mark_points, True)

                if result:
                    cv2.drawContours(frame, [box], 0, (0, 255, 0), 2)
                else:
                    cv2.drawContours(frame, [box], 0, (0, 0, 255), 2)

                    radius = 2

                    cv2.circle(frame, (h_mark_points[0][0], h_mark_points[0][1]), radius, (255, 0, 0), radius)
                    cv2.circle(frame, (h_mark_points[1][0], h_mark_points[1][1]), radius, (0, 255, 0), radius)
                    cv2.circle(frame, (h_mark_points[2][0], h_mark_points[2][1]), radius, (0, 0, 255), radius)
                    cv2.circle(frame, (h_mark_points[3][0], h_mark_points[3][1]), radius, (255, 255, 0), radius)
                    cv2.circle(frame, (h_mark_points[4][0], h_mark_points[4][1]), radius, (255, 0, 255), radius)
                    cv2.circle(frame, (h_mark_points[5][0], h_mark_points[5][1]), radius, (0, 255, 255), radius)
                    cv2.circle(frame, (h_mark_points[6][0], h_mark_points[6][1]), radius, (255, 100, 255), radius)
                    cv2.circle(frame, (h_mark_points[7][0], h_mark_points[7][1]), radius, (100, 255, 255), radius)



    frameOut = frame
    #
    cv2.imshow('frame1', frame)
    cv2.imshow('frame2', binary)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
