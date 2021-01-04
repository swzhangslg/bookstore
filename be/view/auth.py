from flask import Blueprint
from flask import request
from flask import jsonify
import json
from be.model.user import Player

bp_auth = Blueprint("auth", __name__, url_prefix="/auth")


@bp_auth.route("/login", methods=["POST"])
def login():
    # data = request.get_data()
    # js = json.loads(data.decode("utf-8"))
    # user_id = js.get("user_id")
    # password = js.get("password")
    # terminal = js.get("terminal")
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    terminal = request.json.get("terminal", "")
    # print(user_id, password, terminal)
    u = Player()
    code, message, token = u.login(user_id=user_id, password=password, terminal=terminal)
    return jsonify({"message": message, "token": token}), code


@bp_auth.route("/logout", methods=["POST"])
def logout():
    user_id: str = request.json.get("user_id")
    token: str = request.headers.get("token")
    u = Player()
    code, message = u.logout(user_id=user_id, token=token)
    return jsonify({"message": message}), code


@bp_auth.route("/register", methods=["POST"])
def register():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = Player()
    code, message = u.register(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/unregister", methods=["POST"])
def unregister():
    user_id = request.json.get("user_id", "")
    password = request.json.get("password", "")
    u = Player()
    code, message = u.unregister(user_id=user_id, password=password)
    return jsonify({"message": message}), code


@bp_auth.route("/password", methods=["POST"])
def change_password():
    user_id = request.json.get("user_id", "")
    old_password = request.json.get("oldPassword", "")
    new_password = request.json.get("newPassword", "")
    u = Player()
    code, message = u.change_password(user_id=user_id, old_password=old_password, new_password=new_password)
    return jsonify({"message": message}), code
