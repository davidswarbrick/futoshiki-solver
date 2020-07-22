import cv2
import numpy as np
import matplotlib.pyplot as plt

# Square detector copied from C++ source code here: https://docs.opencv.org/master/db/d00/samples_2cpp_2squares_8cpp-example.html


def is_square(approx):
    max_cosine = 0
    for j in range(2, 5):
        a = approx[j % 4]
        b = approx[j - 2]
        c = approx[j - 1]
        v_1 = (a - c) / np.linalg.norm(a - c)
        v_2 = (b - c) / np.linalg.norm(b - c)
        cosine = np.dot(v_1[0], v_2[0])
        max_cosine = np.amax([cosine, max_cosine])
    return max_cosine < 0.3


def find_squares(img, N=11, thresh=50):
    low = cv2.pyrDown(img)
    smoothed = cv2.pyrUp(low)
    squares = []
    # Assuming black & white image (as we are detecting black squares on grey paper)
    for l in range(N):
        # l is the threshold level
        if l == 0:
            # Use Canny for zero level to catch squares with gradient shading
            # Upper threshold thresh, lower to 0 forces edges merging
            gray0 = cv2.Canny(smoothed, 0, thresh, 5)
            # dilate Canny output to remove potential holes between edge segments
            # squares.cpp uses an empty kernel so we attempt an empty numpy matrix as kernel
            gray = cv2.dilate(gray0, np.ones((3, 3), np.uint8))
        else:
            # gray = gray0[gray0 >= (l + 1) * 255 / N]
            t = (l + 1) * 255 / N
            print(l, ": Threshold pixel value: ", t)
            retval, gray = cv2.threshold(gray0, t, 255, cv2.THRESH_TOZERO)
        contours, hierarchy = cv2.findContours(
            gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE
        )
        squares_found = False
        for i in range(len(contours)):
            # Approximate contour with accuracy proportional to perimeter
            approx = cv2.approxPolyDP(
                contours[i], cv2.arcLength(contours[i], True) * 0.02, True
            )
            # square contours should have 4 vertices after approximation
            # relatively large area (to filter out noisy contours) and be convex
            if (
                len(approx) == 4
                and cv2.contourArea(approx) > 1000
                and cv2.isContourConvex(approx)
                and is_square(approx)
            ):
                squares_found = True
                squares.append(approx)
        if squares_found:
            plt.figure()
            plt.imshow(gray, "gray")

    return squares


imgs = []
for i in range(11):
    img = cv2.imread("img/{}.jpg".format(i), 0)
    imgs.append(img)

# p = cv2.imread("img/3712crop.jpg",0)
p = imgs[2]

plt.imshow(p, "gray")
N = 2
squares = find_squares(p)
plt.show()
