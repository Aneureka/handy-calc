import base64
import json

import requests
from flask import current_app
from latex2sympy_custom4.process_latex import process_sympy


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


def latex_equation(latex_text):
    res = calculate(latex_text)
    equation = latex_text + ' = ' + str('%.2f' % res)
    print('latex_equation:' + equation)
    return equation


def calculate(latex_text=None):
    sympy_expr = process_sympy(latex_text)

    res = sympy_expr.evalf()
    return res


if __name__ == '__main__':
    inputLatex = '\sum_{i = 1}^{10} i'
    latex_equation(inputLatex)
