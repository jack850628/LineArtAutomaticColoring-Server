import traceback
import flaskr.Model.Coloring as coloring
import flaskr.Utility.ResponseTemplate as ResponseTemplate
from flaskr.Config import Config
from flask import Blueprint, Response, request
from flaskr.Model.JException import *

Coloring = Blueprint('Coloring', __name__)

def init_app(app):
    app.register_blueprint(Coloring, url_prefix='/api/coloring')

@Coloring.route('/doColoring', methods=['POST'])
def doColoring():
    try:
        userID = request.values['userID'].strip() if 'userID' in request.values else None
        image = request.values['image'].strip() if 'image' in request.values else None
        if userID is None:
            raise '缺少userID。'
        if image is None:
            raise '缺少圖片。'
        coloring.doColoring(userID, image)
        return ResponseTemplate.success('OK')
    except (
        Exception
    ) as e:
        print(traceback.format_exc())
        response = ResponseTemplate.fail(e.__str__())
        response.status_code = 490
        return response

@Coloring.route('/wait_image', methods=['GET'])
def waitImage():
    try:
        userID = request.values['userID'].strip() if 'userID' in request.values else None
        if userID is None:
            raise '缺少userID。'
        return Response(coloring.waitImage(userID), content_type='text/event-stream')
    except (
        Exception
    ) as e:
        print(traceback.format_exc())
        response = ResponseTemplate.fail(e.__str__())
        response.status_code = 490
        return response