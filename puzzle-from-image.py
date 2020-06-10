import numpy as np
import matplotlib.pyplot as plt
import cv2

imgs = []
for i in range(11):
    img = cv2.imread("img/{}.jpg".format(i), 0)
    imgs.append(img)

# Harris corner detection
# plt.imshow(cv2.cornerHarris(img5, blockSize=5, ksize=3, k=0), "gray")
# Image pyramids
# lower_reso = cv2.pyrDown(img)


def canny_edges(img, thresh=200, ratio=2.5):
    return cv2.Canny(img, thresh, ratio * thresh)


def houghlines_and_plot(img):
    plt.figure()
    plt.subplot(121)
    edges = canny_edges(img)
    plt.imshow(edges, "gray")
    plt.subplot(122)
    rho_thresh = 3
    theta_thresh = np.pi / 180
    houghthresh = 300
    lines = cv2.HoughLines(edges, rho_thresh, theta_thresh, houghthresh)
    imgcopy = img.copy()
    for row in lines:
        # print(row)
        [rho, theta] = row[0]
        # print(rho, theta)
        a = np.cos(theta)
        b = np.sin(theta)
        x0 = a * rho
        y0 = b * rho
        x1 = int(x0 + 1000 * (-b))
        y1 = int(y0 + 1000 * (a))
        x2 = int(x0 - 1000 * (-b))
        y2 = int(y0 - 1000 * (a))
        cv2.line(imgcopy, (x1, y1), (x2, y2), (0, 0, 255), 2)
    plt.imshow(imgcopy, "gray")


def contour_and_plot(img):
    plt.figure()
    plt.subplot(121)
    plt.imshow(img, "gray")
    plt.subplot(122)
    edges = canny_edges(img)
    # ret, thresh = cv2.threshold(img, 127, 255, 0)
    contours, hierarchy = cv2.findContours(
        edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    drawncont = cv2.drawContours(img, contours, -1, (0, 128, 0), 1)
    plt.imshow(drawncont, "gray")


# houghlines_and_plot(imgs[0])

for j in range(3):
    contour_and_plot(imgs[j])


# https://opencv-python-tutroals.readthedocs.io/en/latest/py_tutorials/py_feature2d/py_feature_homography/py_feature_homography.html#feature-homography


plt.show()
