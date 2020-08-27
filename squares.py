import cv2
import numpy as np
import matplotlib.pyplot as plt
import itertools
import collections
from copy import deepcopy

# Square detector copied from C++ source code here:
# https://docs.opencv.org/master/db/d00/samples_2cpp_2squares_8cpp-example.html


class Square:
    def __init__(self, corners):
        # unpack corner array into a single 2D numpy array for ease of use.
        self.corners = np.array([x[0] for x in corners])
        self.in_grid = False
        self.value = None
        self.possible_values = [1, 2, 3, 4, 5]

    def __repr__(self):
        return str(self.area)

    @property
    def area(self):
        return cv2.contourArea(self.corners)

    @property
    def average_side_length(self):
        return np.sqrt(self.area)

    @property
    def centre(self):
        return np.array(
            [np.mean(self.corners[:, 0]).round(), np.mean(self.corners[:, 1]).round(),]
        )

    @staticmethod
    def relative_area_increase(sq1, sq2):
        big = max(sq1.area, sq2.area)
        small = min(sq1.area, sq2.area)
        return big / small

    @staticmethod
    def are_duplicates(sq1, sq2):
        """Check two squares are similar by their centre location and area change.
        """
        dist = np.linalg.norm(sq1.centre - sq2.centre)
        return dist < 10 and (Square.relative_area_increase(sq1, sq2)) < 2

    @staticmethod
    def points_form_a_square(approx):
        """Check the 4 points in the approximate contour form a rectangle
        This is completed by checking the cosine of each corner angle
        """
        max_cosine = 0
        side_length_approx_same = False
        for j in range(2, 5):
            a = approx[j % 4]
            b = approx[j - 2]
            c = approx[j - 1]
            length_1 = np.linalg.norm(a - c)
            length_2 = np.linalg.norm(b - c)
            v_1 = (a - c) / length_1
            v_2 = (b - c) / length_2
            cosine = np.dot(v_1[0], v_2[0])
            max_cosine = np.amax([cosine, max_cosine])
            side_length_approx_same = (
                abs(length_2 - length_1) / min(length_1, length_2) < 0.5
            )
        return max_cosine < 0.3 and side_length_approx_same

    def draw_square(self, img):
        return cv2.polylines(img, [self.corners], True, (255, 0, 0), 5)


class SquareList(collections.UserList):
    @property
    def all_corners(self):
        return list(itertools.chain.from_iterable(s.corners for s in self.data))

    @property
    def all_areas(self):
        return [x.area for x in self.data]

    def sort_by_area(self, reverse=False):
        self.data.sort(key=lambda x: x.area, reverse=reverse)

    def sort_by_dist(self, centre, reverse=False):
        return sorted(
            self.data, key=lambda x: np.linalg.norm(x.centre - centre), reverse=reverse
        )

    def remove_duplicate_squares(self):
        """A function to remove duplicate nearby squares
        (caused by edge detector getting things wrong)."""
        # Sort from smallest to largest so we keep the inside of edge-detected squares.
        self.sort_by_area(reverse=False)
        duplicate_indices = []
        for index in range(len(self.data)):
            try:
                sq = self.data[index]
                rest_of_list = self.data[index + 1 :]
            except IndexError:
                pass
            for i, smaller_square in enumerate(rest_of_list):
                if Square.are_duplicates(sq, smaller_square):
                    duplicate_indices.append(i + index + 1)
        duplicate_indices = list(set(duplicate_indices))
        for index in sorted(duplicate_indices, reverse=True):
            del self.data[index]

    def remove_squares_mismatched_neighbours(self, num_neighbours=3):
        non_puzzle_square_indices = []
        for index, square in enumerate(self.data):
            closest_squares = self.sort_by_dist(square.centre)[1 : 1 + num_neighbours]
            neighbours = np.full((num_neighbours, 2), np.inf)
            for i, neighbour in enumerate(closest_squares):
                diff = neighbour.centre - square.centre
                dist = np.linalg.norm(diff)
                ang = np.rad2deg(np.arctan2(diff[1], diff[0])) + 22 // 45  # degrees
                if (
                    ang not in neighbours[:, 1]
                    and dist > square.average_side_length * 1.2
                    # and dist < square.average_side_length * 3.5
                ):
                    neighbours[i, :] = [dist, ang]
                else:
                    non_puzzle_square_indices.append(index)
                    break

        non_puzzle_square_indices = list(set(non_puzzle_square_indices))
        for index in sorted(non_puzzle_square_indices, reverse=True):
            del self.data[index]

    def draw_all(self, img):
        # ToDo: check if deepcopy needed/is it possible to draw without changing image
        p = deepcopy(img)
        for s in self.data:
            p = s.draw_square(p)
        return p


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
            and cv2.isContourConvex(approx)
            and cv2.contourArea(approx) > 100
            and Square.points_form_a_square(approx)
        ):
            # found a square
            sl.append(Square(approx))

    return sl


imgs = []
for i in range(11):
    img = cv2.imread("img/{}.jpg".format(i), 0)
    imgs.append(img)
    sl = find_squares(img)
    sl.remove_duplicate_squares()
    sl.remove_squares_mismatched_neighbours()
    all_corners = sl.all_corners
    clear_img = np.zeros(img.shape)
    for c in all_corners:
        clear_img[c[1], c[0]] = 255
    plt.figure(1)
    plt.subplot(3, 4, i + 1)
    # plt.imshow(p, "gray")
    # plt.imshow(clear_img, "gray")
    p = sl.draw_all(img)
    # plt.subplot("121")
    plt.imshow(p)
    print("Found {} squares".format(len(sl)))
plt.show()
