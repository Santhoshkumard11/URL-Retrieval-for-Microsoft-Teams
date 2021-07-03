import io
import logging
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
import io
import cv2
import numpy as np
import tempfile
from os import listdir

tempFilePath = tempfile.gettempdir()

# these environment variables are set in the Azure Function
subscription_key = os.environ.get("COGNITIVESERVICES_KEY")
endpoint = os.environ.get("COGNITIVESERVICES_URL")


logging.info("Computer vision service connected!!")

domain_ref_dict = ["http","https"]

def is_url(text: str):
    """ Check if the given string is a URL or contains an URL

    Args:
        text (str): recognized text from the image

    Returns:
        Bool : Return True if given string is a URL else False
    """
    
    return True if len(list(filter(lambda x: text.startswith(x), domain_ref_dict))) else False


def sanitize_urls(urls_list: list):
    """Remove unwanted space and strip the text string

    Args:
        urls_list (list): list of recognized text from Computer Vision

    Returns:
        json: json payload of sanitized URLs
    """
    
    result_url_list = []
    
    for url in urls_list:
        
        url = url.replace(" ","")
        
        result_url_list.append({"url":  url})

    return json.dumps(result_url_list)


def get_text_from_image(image_string: str):
    
    # since Azure Functions are readonly using a temp file process the image
    fp = tempfile.TemporaryFile()
    url_links = []

    # reconstruct the image from binary form
    img_data = base64.b64decode(image_string)
    fp.write(img_data)
    fp.seek(0)

    # create the computer vision client
    computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
    
    # Call API with image and raw response (allows you to get the operation location)
    read_response = computervision_client.read_in_stream(fp, raw=True)
    # Get the operation location (URL with ID as last appendage)
    read_operation_location = read_response.headers["Operation-Location"]
    # Take the ID off and use to get results
    operation_id = read_operation_location.split("/")[-1]
    
    fp.close()

    logging.info("Image sent to Computer Vision Services")

    # Call the "GET" API and wait for the retrieval of the results
    while True:
        read_result = computervision_client.get_read_result(operation_id)
        if read_result.status.lower () not in ['notstarted', 'running']:
            break
        print('Waiting for result...')
        time.sleep(10)


    # Get the text in the images
    if read_result.status == OperationStatusCodes.succeeded:
        for text_result in read_result.analyze_result.read_results:
            for line in text_result.lines:
                received_text = line.text.strip()
                if is_url(received_text):
                    url_links.append(received_text)

    computervision_client.close()

    return sanitize_urls(url_links)


def run_link_generator(image_binary: str):

    "Process the received text to get only the links"

    # TODO: identify the Linkedin and Twitter handles and find the profile links

    logging.info("Process Started!!")
    
    url_links = get_text_from_image(image_binary)

    logging.info("End of Processing!!")

    return url_links
