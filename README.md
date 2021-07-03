# URL-Retrieval-for-Microsoft-Teams

## Azure Developer League

The entire process starts by receiving the binary image in **POST requests**

Endpoint to test - https://santhosh-url-retrieval.azurewebsites.net/api/GenerateLink?image_name=null

If get the following message then the service is up and running - "**Thanks for checking out the api. Send a valid image name to generate the url**"

**process_image.py** - is where the text is extracted from the image and the links are retrieved