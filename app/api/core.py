from flask import request, render_template, current_app
import requests
import json

from . import api
from app.service.convert import convert_image_to_latex
from app.utils import convert_file_size_to_mb

@api.route('/ping', methods=['GET'])
def ping():
    return 'Link started!'


@api.route('/', methods=['GET'])
def index():
    return render_template('index.html', title=current_app.config['APP_NAME'], host=current_app.config['HOST'])

@api.route('/drawing-board', methods=['GET'])
def drawingboard():
    return render_template('drawing-board.html', title=current_app.config['APP_NAME'], host=current_app.config['HOST'])

@api.route('/convert', methods=['POST'])
def convert():
    if request.method == 'POST':
        image_uri = request.json.get('image_uri')
        if image_uri is None:
            return json.dumps({'code': -1, 'msg': 'Param of <image_uri> (image base64) required.'})
        data = convert_image_to_latex(image_uri)
        return json.dumps({'code': 0, 'data': data}) 


@api.route('/test', methods=['GET'])
def test():
    convert_image_to_latex()
    return 'Converted!'