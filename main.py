import json
from flask import Flask, request, jsonify, abort, make_response

from model.comment import Comment
from model.twit import Twit
from model.user import User

comments = []
twits = []

app = Flask(__name__)

class CustomJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Twit):
            return {"body": obj.body, "author": obj.author.username, "id_twit": obj.id_twit}
        elif isinstance(obj, Comment):
            return {"body": obj.body, "id_twit": obj.id_twit, "username": obj.username}
        elif isinstance(obj, list):
            return [self.default(item) for item in obj]
        return json.JSONEncoder.default(self, obj)

app.json_encoder = CustomJSONEncoder


@app.route("/twit", methods=["POST"]) #Создает твиты
def create_twit():
    id_twit = len(twits)
    '''{"body": "Hello world", "author": "@egoska"}'''
    twit_json = request.get_json()
    user = User(twit_json["author"])
    id_twit += 1
    twit = Twit(twit_json["body"], user, id_twit)
    twits.append(twit)
    return jsonify({"status": "success"})

@app.route("/twit", methods=["GET"]) #Показывает все твиты в случае если не выбран id твита
def read_twits():
    twits_data = [app.json_encoder().default(twit) for twit in twits]
    return jsonify({"twits": twits_data})

@app.route("/twit/<int:twit_id>", methods=["GET"]) #Показывает твиты по заданному id
def read_twit(twit_id):
    twit = next((t for t in twits if t.id_twit == twit_id), None)
    if twit is None:
        abort(404)
    return jsonify(app.json_encoder().default(twit))

@app.errorhandler(404) #Обрабатыввает ошибку 404
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@app.route("/twit/<int:twit_id>", methods=["PUT"]) #Изменяет твиты
def update_twit(twit_id):
    twit = next((t for t in twits if t.id_twit == twit_id), None)
    if twit is None:
        abort(404)
    if not request.json:
        abort(404)
    twit.body = request.json.get("body", twit.body)
    twit_data = app.json_encoder.default(app.json_encoder, twit)  # Сериализуйте объект twit
    return jsonify({"twit": twit_data})

@app.route("/twitd/<int:twit_id>", methods=["DELETE"]) #Удаляет твит
def delete_twit(twit_id):
    twit = next((t for t in twits if t.id_twit == twit_id), None)
    if twit is None:
        abort(404)
    twits.remove(twit)
    return jsonify({"result": "twit was successfully deleted"})

@app.route("/comm/<int:twit_id_comm>", methods=["POST"]) #Создает комментарий к твиту по id твита
def create_comm(twit_id_comm):
    '''{"body": "cool", "id_twit": 1, "username": "Igor"}'''
    twit = next((t for t in twits if t.id_twit == twit_id_comm), None)
    if twit is None:
        abort(404)
    comm_json = request.get_json()
    comm = Comment(comm_json["body"], comm_json["id_twit"], comm_json["username"])
    comments.append(comm)
    return jsonify({"status": "success"})

@app.route("/commd/<int:twit_id_comm>", methods=["DELETE"]) #Удаляет комментарий по его id
def delete_comm(twit_id_comm):
    comm = next((t for t in comments if t.id_twit == twit_id_comm), None)
    if comm is None:
        abort(404)
    comments.remove(comm)
    return jsonify({"status": "comment was successfully deleted"})

if __name__ == "__main__":
    app.run(debug=True)