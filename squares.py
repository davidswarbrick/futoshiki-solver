import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools
import collections
from copy import deepcopy

# Square detector copied from C++ source code here: https://docs.opencv.org/master/db/d00/samples_2cpp_2squares_8cpp-example.html


class Square:
    def __init__(self, corners):
        # unpack corner array into a single 2D numpy array for ease of use.
        self.corners = np.array([x[0] for x in corners])

    def __repr__(self):
        return str(self.area)

    @property
    def reconstructed(self):
        return np.array([[x] for x in self.corners])

    @property
    def area(self):
        return cv2.contourArea(self.corners)

    def draw_square(self, img):
        return cv2.polylines(img, self.reconstructed, True, (255, 0, 0), 5)


class SquareList(collections.UserList):
    @property
    def all_corners(self):
        # Corners are stored as [ [[x0 y0]] [[x1 y1]] ...]
        # so we do two chain.from_iterable steps to unpack them.
        # ToDo: Would be better to do this in Square constructor
        a = list(itertools.chain.from_iterable(s.corners for s in self.data))

        return a

    def sort_by_area(self):
        self.data.sort(key=lambda x: x.area)

    def remove_close_squares(self):
        """ToDo: implement a function to remove all nearby squares
        (caused by edge detector getting things wrong)."""
        # Construct a list of the first corner of each square, check on these points.
        first_corners = list(
            itertools.chain.from_iterable(s.corners[0] for s in self.data)
        )

        return first_corners

    def draw_all(self, img):
        # ToDo: check if deepcopy needed/is it possible to draw without changing image
        p = deepcopy(img)
        for s in self.data:
            p = s.draw_square(p)
        return p


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


def find_squares(img, thresh=50, ratio=2.5):
    low = cv2.pyrDown(img)
    smoothed = cv2.pyrUp(low)
    sl = SquareList()
    # Assuming black & white image (as we are detecting black squares on grey paper)

    gray = cv2.Canny(smoothed, thresh, ratio * thresh)
    contours, hierarchy = cv2.findContours(gray, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
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
            # found a square
            sl.append(Square(approx))
    # if squares_found:
    #    plt.figure()
    #    plt.imshow(gray, "gray")

    return sl


imgs = []
for i in range(11):
    img = cv2.imread("img/{}.jpg".format(i), 0)
    imgs.append(img)

# p = cv2.imread("img/3712crop.jpg",0)
p = imgs[2]
sl = find_squares(p)


all_corners = sl.all_corners
clear_img = np.zeros(p.shape)

for c in all_corners:
    clear_img[c[1], c[0]] = 255


plt.figure(0)
plt.imshow(clear_img, "gray")
plt.figure(1)
plt.subplot(121)
plt.imshow(p, "gray")
p = sl.draw_all(p)
plt.subplot(122)
plt.imshow(p)
print("Found {} squares".format(len(sl)))
plt.show()
