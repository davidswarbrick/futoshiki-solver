import cv2
import numpy as np
import matplotlib.pyplot as plt

# Square detector copied from C++ source code here: https://docs.opencv.org/master/db/d00/samples_2cpp_2squares_8cpp-example.html


class Square:
    def __init__(self, corners):
        self.corners = corners

    @property
    def area(self):
        return cv2.contourArea(self.corners)


def is_square(approx):
    """
    Check the 4 points in the approximate contour form a rectangle
    This is completed checking the cosine of each corner angle
    """
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


def draw_square(img, square):
    return cv2.polylines(img, square, True, (255, 0, 0), 5)


def find_squares(img, thresh=50, ratio=2.5):
    low = cv2.pyrDown(img)
    smoothed = cv2.pyrUp(low)
    squares = []
    # Assuming black & white image (as we are detecting black squares on grey paper)

    gray = cv2.Canny(smoothed, thresh, ratio * thresh)
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    squares_found = False
    for i in range(len(contours)):
        # Approximate contour with accuracy proportional to perimeter
        approx = cv2.approxPolyDP(
            contours[i], cv2.arcLength(contours[i], True) * 0.03, True
        )
        # square contours should have 4 vertices after approximation
        # relatively large area (to filter out noisy contours) and be convex
        if (
            len(approx) == 4
            # and cv2.contourArea(approx) > 1000
            and cv2.isContourConvex(approx)
            and is_square(approx)
        ):
            squares_found = True
            squares.append(Square(approx))
    # if squares_found:
    #    plt.figure()
    #    plt.imshow(gray, "gray")

    return squares


imgs = []
for i in range(11):
    img = cv2.imread("img/{}.jpg".format(i), 0)
    imgs.append(img)

# p = cv2.imread("img/3712crop.jpg",0)
p = imgs[2]
squares = find_squares(p)

plt.figure(1)
plt.subplot(121)
plt.imshow(p, "gray")
for s in squares:
    p = draw_square(p, s.corners)
plt.subplot(122)
plt.imshow(p)
print("Found {} squares".format(len(squares)))
plt.show()
