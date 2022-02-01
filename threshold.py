import numpy as np
import cv2  

def threshold(image_path):    
    '''
        image_path: Path to image
    '''
    inp_img = cv2.imread(image_path)
    img = inp_img.reshape((-1,3))
    img = np.float32(img)
    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    k=4
    ret,label,center=cv2.kmeans(img,k,None,criteria,10,cv2.KMEANS_PP_CENTERS)
    center = np.uint8(center)
    result = center[label.flatten()]
    bright = np.amax(center)
    result = result.reshape((inp_img.shape))
    result[result==bright] = 255
    result = np.uint8(result)
    return result