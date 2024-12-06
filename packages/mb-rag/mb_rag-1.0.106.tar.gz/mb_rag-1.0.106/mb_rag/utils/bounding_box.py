from PIL import Image
import google.generativeai as genai
import os
import cv2
import json

__all__ = ["google_model","generate_bounding_box"]

# genai.configure(api_key=os.environ.get("GOOGLE_API_KEY"))
# model = genai.GenerativeModel(model_name="gemini-1.5-pro-latest")

def google_model(model="gemini-1.5-pro-latest",api_key=None,**kwargs):
    """
    Function to get google genai model 
    Args:
        model (str): Model name
        api_key (str): API key. If None, it will be fetched from the environment variable GOOGLE_API_KEY
        **kwargs: Additional arguments
    Returns:
        model (GenerativeModel): GenerativeModel object
    """
    if api_key == None:
        api_key = os.environ.get("GOOGLE_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(model_name=model,**kwargs)

def generate_bounding_box(model,image_path: str,prompt: str= 'Return bounding boxes of container, for each only one return [ymin, xmin, ymax, xmax]'):
    """
    Function to generate bounding boxes
    Args:
        model (GenerativeModel): GenerativeModel object
        image_path (str): Image path
        prompt (str): Prompt
    Returns:
        res (str): Result
    """
    image = Image.open(image_path)
    res = model.generate_content([image,prompt])
    return res

def add_bounding_box(image_path: str,bounding_box: list,label: str,show: bool=False):
    """
    Function to add bounding box to image
    Args:
        image_path (str): Image path
        bounding_box (dict): Bounding box
        label (str): Label
    Returns:
        image (Image): Image with bounding box
    """
    img= cv2.imread(image_path)
    for key,value in bounding_box.items():
        cv2.rectangle(img, (value[1],value[0]), (value[3],value[2]), (0, 0, 255), 4)
        cv2.putText(img, key, (value[1],value[0]), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)
    if show:
        cv2.imshow("Image",img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    return img

