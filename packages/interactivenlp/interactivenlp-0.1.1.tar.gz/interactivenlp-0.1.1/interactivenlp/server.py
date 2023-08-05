from flask import Flask, jsonify, request
from flask_cors import CORS
from .types import InteractiveRssType, ModelConfigurationType


class Server:
    def __init__(self, config: ModelConfigurationType):
        self.app = Flask(__name__)
        self.config = config

        self.functions = config.functions



        CORS(self.app)

        @self.app.route('/')
        def index():
            return "Hello, World!"
        
        @self.app.route('/model/<name>', methods=['POST'])
        def model_route(name):
            target_function = next(
                filter(lambda function: function.name == name, self.functions), None)
            
            if target_function is None:
                return {
                    "success": False,
                    "message": "Function not found"
                }
            
            rss = request.get_json()
            rss_modeled = InteractiveRssType(
                "", rss['paragraphs'])
            
            res = target_function.function(rss_modeled)
            return jsonify([block.__dict__ for block in res])


        @self.app.route('/submit', methods=['POST'])
        def submit():
            return {
                "success": True
            }

    def run(self):
        self.app.run(debug=True)
