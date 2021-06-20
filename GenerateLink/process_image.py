from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time
import json
import base64

subscription_key = os.environ.get("COGNITIVESERVICES_KEY")
endpoint = os.environ.get("COGNITIVESERVICES_URL")

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

domain_ref_dict = ["http","https"]

def is_url(text: str):
    
    return True if len(list(filter(lambda x: text.startswith(x), domain_ref_dict))) else False


def sanitize_urls(urls_list: list):
    
    result_url_list = []
    
    for url in urls_list:
        
        url = url.replace(" ","")
        
        result_url_list.append({"url":  url})

    return json.dumps(result_url_list)


def save_image_from_base64(base64_string: str):
    img_data = base64.b64decode(base64_string)
    filename = os.path.join ("GenerateLink/images","ocr_image.jpg")
    with open(filename, 'wb') as f:
        f.write(img_data)

def get_text_from_image(image_name: str):
    
    url_links = []

    # Get image path
    read_image_path = os.path.join ("GenerateLink/images", image_name)
    # Open the image
    read_image = open(read_image_path, "rb")

    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(read_image, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print ('Waiting for result...')
        time.sleep(10)


    # Get the text in the images
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                received_text = line.text.strip()
                if is_url(received_text):
                    url_links.append(received_text)

    computervision_client.close()

    os.remove(read_image_path)

    print("End of Processing!!")

    return sanitize_urls(url_links)


def run_link_generator():

    "Process the received text to get only the links"

    # TODO: identify the Linkedin and Twitter handles and find the profile links

    print("Process Started!!")
    
    url_links = get_text_from_image("ocr_image.jpg")

    return url_links