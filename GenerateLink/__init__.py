from GenerateLink.process_image import run_link_generator
import logging
import json
import azure.functions as func


def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Generate URL Link Function Triggered!!')

    image_name = req.params.get('image_name')
    if not image_name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            image_name = req_body.get('image_name')

    if image_name == "null":
        return func.HttpResponse("Thanks for checking out the api. Send a valid image name to generate the url", status_code=200)

    else:

        detected_url = run_link_generator(image_name) 

        return func.HttpResponse(
             f"{detected_url}",
             status_code=200
        )
