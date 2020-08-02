import flask
from flask import request, jsonify
from knn import Knn
import logging
from configure_logging import configure_logging
from flask_cors import CORS
configure_logging('public_api.py')

class PublicApi():
        def __init__(self):
                self.app = flask.Flask(__name__)
                CORS(self.app)
                self.app.config["DEBUG"] = True
                self.knn = Knn(7)                

        def start(self):
                @self.app.route('/api/predict', methods=['POST'])
                def api_id():    
                        logging.info(request.args)
                        if 'radiant_score' in request.args and 'dire_score' in request.args and 'duration' in request.args:
                                radiant_score = int(request.args['radiant_score'])
                                dire_score = int(request.args['dire_score'])
                                duration = int(request.args['duration'])
                                result = self.knn.predict([[radiant_score,dire_score,duration]])
                                logging.info(result[0])
                                text_result = ''
                                if result[0] == 1:
                                        text_result = 'Radiant wins!'
                                else:
                                        text_result = 'Dire wins!'
                                return str('{"result": \"'+text_result+'\"}')
                        else:
                                return "Missed a field"
                self.app.run(host='0.0.0.0', port=8080)
