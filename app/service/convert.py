import sys
import base64
import requests
import json
from flask import current_app


def convert_image_to_latex(image_uri=None):
    if image_uri is None:
        # test mode
        file_path = '.tmp/test3.jpg'
        image_uri = "data:image/jpg;base64," + base64.b64encode(open(file_path, 'rb').read()).decode()
    resp = requests.post(
        url=current_app.config['MATHPIX_API'],
        data=json.dumps({
          'src': image_uri,
          'formats': ['text', 'data'],
          'data_options': {
            'include_latex': True,
            'include_asciimath': True
          } 
        }),
        headers={
            'app_id': current_app.config['MATHPIX_APP_ID'],
            'app_key': current_app.config['MATHPIX_APP_KEY'],
            'Content-type': 'application/json'
        }
    )
    print(json.dumps(json.loads(resp.text), indent=4, sort_keys=True))
    return resp.text
