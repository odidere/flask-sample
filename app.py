from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin
from flask_restful import Api, Resource
from werkzeug.exceptions import HTTPException
from werkzeug.exceptions import default_exceptions
import settings

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.errorhandler(Exception)
def handle_error(e):
    code = 500
    if isinstance(e, HTTPException):
        code = e.code
    return jsonify(error=str(e)), code


for ex in default_exceptions:
    app.register_error_handler(ex, handle_error)

app.config['BUNDLE_ERRORS'] = settings.BUNDLE_ERRORS

api = Api(app)
api.prefix = '/'


class Message(Resource):

    @cross_origin()
    def get(self):
        query = request.args
        q = query["q"]
        if q == "Ping":
            return "OK"
        elif q == "Degree":
            return "Bachelor of Science in Computer Science, Master of Science in Mathematics and Computer Science"
        elif q == "Name":
            return "Oluwashina Samuel Aladejubelo"
        elif q == "Phone":
            return "+2347031096039"
        elif q == "Source":
            return "https://github.com/odidere/flask-sample.git"
        elif q == "Status":
            return "No. Working remotely"
        elif q == "Years":
            return "15"
        elif q == "Puzzle":
            return ""
        elif q == "Resume":
            return "https://docs.google.com/document/d/1cZN_UhG0e-gVY6I07bpDWCgjjwN-p9EzV_eV1GVFP8k/edit?usp=sharing"
        elif q == "Referrer":
            return "Turing.com"
        elif q == "Position":
            return "Senior Data Engineer"
        return request.args.get("")


api.add_resource(Message, "/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
