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
    for file in os.listdir("users"):
        with open(os.path.join("users", file), 'r') as f:
            user = f.readlines()
            last_name = user[0][0:-1]
            name = user[1]
            title = file.title()
            title = title.split('.')
            title = title[0]
            user_list.append({"id": title, "last_name": last_name, "name": name})
    return make_response(str(list(reversed(user_list))), 200)


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
        if not id_arg == "":
            return make_response("Id Incorrect", 400)
    except:
        return make_response("Id Incorrect", 400)

    try:
        open(os.path.join("users", f'{id_arg}.txt'))
        return make_response("Utilisateur déja existant", 409)
    except:
        with open(os.path.join("users", f'{id_arg}.txt'), 'w') as f:
            f.write(last_name_arg + '\n' + name_arg)
        return make_response("Utilisateur ajouté", 200)


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
        with open(os.path.join("users", f'{str(id_arg)}.txt'), 'r') as f:
            user = f.readlines()
            last_name_used = user[0][0:-1]
            name_used = user[1]
            if name_arg is None:
                name = name_used
            else:
                name = name_arg

            if last_name_arg is None:
                last_name = last_name_used
            else:
                last_name = last_name_arg
    except:
        return make_response("Utilisateur Introuvable", 404)

    with open(os.path.join("users", f'{str(id_arg)}.txt'), 'w') as f:
        f.write(f"{last_name}\n{name}")
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
        os.remove(os.path.join("users", f'{id_arg}.txt'))
        return make_response("Utilisateur Supprimé", 200)
    except:
        return make_response("Utilisateur Introuvable", 404)


if __name__ == '__main__':
    app.run(
        host=host,
        port=8001,
        debug=True
    )