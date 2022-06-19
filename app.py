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
        if q == "Degree":
            return "Bachelor of Science in Computer Science, Master of Science in Mathematics and Computer Science"
        if q == "Name":
            return "Oluwashina Samuel Aladejubelo"
        if q == "Phone":
            return "+2347031096039"
        if q == "Email Address":
            return "Shinasamuel@gmail.com"
        if q == "Source":
            return "https://github.com/odidere/flask-sample.git"
        if q == "Status":
            return "No. Working remotely"
        if q == "Years":
            return "15"
        if q == "Puzzle":
            return ""
        if q == "Resume":
            return "https://docs.google.com/document/d/1cZN_UhG0e-gVY6I07bpDWCgjjwN-p9EzV_eV1GVFP8k/edit?usp=sharing"
        if q == "Referrer":
            return "Turing.com"
        if q == "Position":
            return "Senior Data Engineer"
        if q == "Puzzle":
            return self.solve_puzzle(query.get("d", None))
        return ""

    def parse_matrix(self, puzzle):
        puzzle_mat = []
        print(type(puzzle), puzzle)
        puzzle = str(puzzle.strip()).split("\n")
        print(puzzle)
        for pos, line in enumerate(puzzle):
            if pos == 0 or pos == 1:
                continue
            else:
                puzzle_mat.append(list(line[1:]))
        return puzzle_mat

    def parse_str(self, puzzle_mat):
        newline = '\n'
        temp = ' ABCD' + newline
        for pos, row in enumerate(puzzle_mat):
            t = temp[pos + 1] + ''.join([r for r in row]) + newline
            temp += t
        return temp

    def solve_puzzle(self, puzzle):
        puzzle_mat = self.parse_matrix(puzzle)
        puzzle_mat = Message.level_1(puzzle_mat)
        puzzle_mat_2 = Message.level_2(puzzle_mat)
        puzzle_mat_2 = Message.level_2(puzzle_mat_2)
        puzzle = self.parse_str(puzzle_mat_2)
        return puzzle


@staticmethod
def level_1(mat_1):
    mat_2 = [['-' for i in range(len(mat_1))] for j in range(len(mat_1[0]))]
    for pos_i, i in enumerate(mat_1):
        for pos_j, j in enumerate(mat_1[pos_i]):
            if pos_i == pos_j:
                mat_2[pos_i][pos_j] = '='
            else:
                if mat_1[pos_i][pos_j] == '>':
                    mat_2[pos_i][pos_j] = '>'
                    mat_2[pos_j][pos_i] = '<'
                elif mat_1[pos_i][pos_j] == '<':
                    mat_2[pos_i][pos_j] = '<'
                    mat_2[pos_j][pos_i] = '>'
    return mat_2


@staticmethod
def level_2(self, mat_1):
    mat_2 = [[mat_1[i][j] for i in range(len(mat_1))]
             for j in range(len(mat_1[0]))]
    for pos_i, i in enumerate(mat_1):
        for pos_j, j in enumerate(mat_1[pos_i]):
            if not (pos_i == pos_j) and mat_1[pos_i][pos_j] == '-':
                for k in range(4):
                    if pos_j != k and pos_i != k:
                        # print(pos_i, k, pos_j, k)
                        if mat_1[pos_i][k] == mat_1[k][
                                pos_j] and mat_1[k][pos_j] != '-':
                            # print('---', pos_i, k, pos_j, k)
                            mat_2[pos_i][
                                pos_j] = '>' if mat_1[k][pos_j] == '<' else '<'
    return mat_2


api.add_resource(Message, "/")

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
