import io

import cv2
import numpy as np

from chromahacker.spline import spline_from # hey this line is a palindrome
from chromahacker.process_image import url_to_image

def palettize(url, output, *args):
    np_array = url_to_image(url)

    img = cv2.cvtColor(np_array, cv2.COLOR_RGB2GRAY)

    fn = spline_from(*args)

    display = np.rint(fn(img)).astype(np.uint8)
    cv2.imshow('image', display)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    cv2.imwrite('wallpaper.' + output, display)
