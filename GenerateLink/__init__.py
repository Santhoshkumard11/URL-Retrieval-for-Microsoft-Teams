from GenerateLink.process_image import run_link_generator
import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generate URL Link Function Triggered!!')

    global image_binary
    
    # set the image name to default for testing
    image_name = "test1.png"
    if req.method == "GET":
            
        image_name = req.params.get('image_name')
        if image_name == "null":
            return func.HttpResponse("Thanks for checking out the api. Send a valid image name to generate the url", status_code=200)
        
    else:
        # get the binary image from the request body
        req_body = req.get_json()
        image_binary = req_body.get('image_binary')["$content"]

        try:
            # start the process calling the link generator
            detected_url = run_link_generator(image_binary)

            return func.HttpResponse(
                detected_url,
                status_code=200
            )
        
        except Exception as e:
            logging.exception(e)
            return func.HttpResponse("Something went wrong!!!")
