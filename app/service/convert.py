import base64
import json

import requests
from flask import current_app
from latex2sympy_custom4.process_latex import process_sympy



def convert_image_to_latex(image_uri=None):
    if image_uri is None:
        # test mode
        file_path = '.tmp/test3.jpg'
        image_uri = base64.b64encode(open(file_path, 'rb').read()).decode()
        f = open('image_base64.txt', 'w')
        f.write(image_uri)
        f.close()
    image_uri = "data:image/jpg;base64," + image_uri
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
    if resp.status_code == 200:
        resp_data = json.loads(resp.text)
        if 'confidence' not in resp_data.keys() or resp_data['confidence'] < current_app.config['MATHPIX_CONFIDENCE_THRESHOLD']:
            return None
        if 'data' not in resp_data.keys():
            return None
        for item in resp_data['data']:
            t, v = item['type'], item['value']
            if t == 'latex':
                return v
    return None


def get_latex_equation(latex_text):
    try:
        res = _calculate(latex_text)
        equation = latex_text + ' = '
        if res == int(res):
            equation += str(int(res))
        else:
            equation += str('%.2f' % res)
        print('latex equation: %s' % equation)
        return equation
    except Exception:
        return None
    

def _calculate(latex_text=None):
    sympy_expr = process_sympy(latex_text)
    return sympy_expr.evalf()


if __name__ == '__main__':
    inputLatex = '\\frac{|5-1}{7 \\times 6}'
    get_latex_equation(inputLatex)
