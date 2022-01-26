import cv2
import numpy as np
from PIL import Image

def is_jpg(file_path):
    """
        file_path: path to file
    """
    name_array = file_path.split(".")
    if name_array[-1] == 'jpg' or name_array[-1] == 'jpeg':
        return True
    return False
    

def normalize(x):
    """
        x: Numpy array to normalize.
    """
    l2 = np.atleast_1d(np.linalg.norm(x, ord=2, axis=1)) # ord=2 -> L2 Normalization
    l2[l2 == 0] = 1 #every element with value 0 to 1
    return x / np.expand_dims(l2, 1)
 

def preprocess(file_path):
    """
        file_path: path to file
    """
    input_img = cv2.imread(file_path)  #reads image as numpy array
    pil_img = Image.fromarray(input_img) #converts numpy array to a Pillow image
    pil_img = pil_img.resize((64,64)) 
    pil_np = np.array(pil_img) 
    np_img = np.expand_dims(pil_np, axis=0) 
    img_to_pred = normalize(np_img) #L2 normalization
    return img_to_pred