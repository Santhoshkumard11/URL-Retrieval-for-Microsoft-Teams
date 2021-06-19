from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time


subscription_key = ""
endpoint = ""


computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

domain_ref_dict = ["http","https"]

def is_url(text: str):
    
    return True if len(list(filter(lambda x: text.startswith(x), domain_ref_dict))) else False


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
    
    print("End of Processing!!")

    return url_links


def run_link_generator(image_name: str):

    "Process the received text to get only the links"

    print("Process Started!!")

    return get_text_from_image(image_name)