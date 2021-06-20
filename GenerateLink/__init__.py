from GenerateLink.process_image import run_link_generator, save_image_from_base64
import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generate URL Link Function Triggered!!')

    global image_binary
    
    image_name = "test.png"
    if req.method == "GET":
            
        image_name = req.params.get('image_name')
        if image_name == "null":
            return func.HttpResponse("Thanks for checking out the api. Send a valid image name to generate the url", status_code=200)
        
    else:
        req_body = req.get_json()
        image_binary = req_body.get('image_binary')["$content"]
    
        save_image_from_base64(image_binary)

        try:

            detected_url = run_link_generator()

            return func.HttpResponse(
                detected_url,
                status_code=200
            )
        
        except:
            return func.HttpResponse("Something went wrong!!!")