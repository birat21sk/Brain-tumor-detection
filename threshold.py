import numpy as np
import cv2  

def image_segmentation(image_path):    
    '''
    Parameters:
        image_path: Path to image
    '''
    inp_img = cv2.imread(image_path)
    img = inp_img.reshape((-1,3))
    img = np.float32(img)
    k=4 # Number of centroids
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    '''
        TERM_CRITERIA_EPS - stop the algorithm iteration if specified accuracy, epsilon, is reached.
        TERM_CRITERIA_MAX_ITER - stop the algorithm after the specified number of iterations, max_iter.
        TERM_CRITERIA_EPS + cv.TERM_CRITERIA_MAX_ITER - stop the iteration when any of the above condition is met.
    '''
    attempts = 10 # Flag to specify the number of times the algorithm is executed using different initial labellings.
    # K-Means with KMeans++ initial center
    ret,label,center=cv2.kmeans(img,k,bestLabels=None,criteria=criteria,attempts=attempts,flags=cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    bright = np.amax(center)
    result = result.reshape((inp_img.shape))
    result[result==bright] = 255
    result = np.uint8(result)
    return result