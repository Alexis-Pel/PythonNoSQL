import os
from flask import Flask
from flask import request
from flask import make_response
from pymongo import MongoClient

app = Flask(__name__)
host = os.environ["HOST"]
username = os.environ["DB_USER"]
password = os.environ["DB_PASS"]
cluster = os.environ["CLUSTER"]
database_name = os.environ["DB"]
collection_name = os.environ["COLLECTION"]

client = MongoClient(f"mongodb+srv://{username}:{password}@{cluster}/{database_name}?retryWrites=true&w=majority")
db = client[database_name]
collection = db[collection_name]


@app.route("/")
def main():
    """
    Fonction affichant un titre
    :return: string : Accueil
    """
    return make_response('<h1>Accueil</h1>', 200)


@app.route("/users", methods=["GET"])
def users():
    """
        Fonction permettant d'afficher une liste de users
        :return: user_list
        """
    user_list = []
    for i in collection.find():
        user_list.append(i)
    return make_response(str(user_list), 200)


@app.route("/users", methods=["POST"])
def post():
    """
        Fonction permettant de créer un user
            :return: string : Utilisateur ajouté
        """
    try:
        name_arg = request.args['name']
        if not name_arg.isalnum() or name_arg.isdigit():
            return make_response("Prénom Incorrect", 400)
    except:
        return make_response("Prénom Incorrect", 400)
    try:
        last_name_arg = request.args['last_name']
        if not last_name_arg.isalnum() or last_name_arg.isdigit():
            return make_response("Nom Incorrect", 400)
    except:
        return make_response("Nom Incorrect", 400)
    try:
        id_arg = int(request.args['id'])
        if id_arg == "":
            return make_response("Id Incorrect", 400)
    except:
        return make_response("Id Incorrect", 400)

    result = collection.find_one({'_id': id_arg})
    if result is None:
        collection.insert_one({'_id': id_arg, 'last_name': last_name_arg, 'name': name_arg})
        return make_response("Utilisateur ajouté", 200)
    else:
        return make_response("Utilisateur déja existant", 409)


@app.route("/users", methods=["PATCH"])
def patch():
    """
        Fonction permettant de modifier
        :return: string : Utilisateur modifié
        :exception: string: Id Introuvable, Id Incorrect
        """
    try:
        name_arg = request.args['name']
        if not name_arg.isalnum() or name_arg.isdigit():
            return make_response("Prénom Incorrect", 400)
    except:
        name_arg = None
    try:
        last_name_arg = request.args['last_name']
        if not last_name_arg.isalnum() or last_name_arg.isdigit():
            return make_response("Nom Incorrect", 400)
    except:
        last_name_arg = None
    try:
        id_arg = int(request.args['id'])
    except:
        return make_response("Id Incorrect", 400)

    try:
        if name_arg is None:
            name = collection.find_one({'_id': id_arg})['name']
        else:
            name = name_arg

        if last_name_arg is None:
            last_name = collection.find_one({'_id': id_arg})['last_name']
        else:
            last_name = last_name_arg
    except:
        return make_response("Utilisateur Introuvable", 404)

    collection.update_one({'_id': id_arg}, {'$set': {'name': name, 'last_name': last_name}})
    return make_response("Utilisateur Modifié", 200)


@app.route("/users", methods=["DELETE"])
def delete():
    """
        Fonction permettant de supprimer un user
        :return: string : Utilisateur Supprimé
        :exception: string : Utilisateur Introuvable
        """
    try:
        id_arg = int(request.args['id'])
    except:
        return "Id Incorrect"
    try:
        collection.delete_one({'_id':id_arg})
        return make_response("Utilisateur Supprimé", 200)
    except:
        return make_response("Utilisateur Introuvable", 404)


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )
