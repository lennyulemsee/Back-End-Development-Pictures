from . import app
import os
import json
from flask import jsonify, request, make_response, abort, url_for, Response # noqa; F401

SITE_ROOT = os.path.realpath(os.path.dirname(__file__))
json_url = os.path.join(SITE_ROOT, "data", "pictures.json")
data: list = json.load(open(json_url))

######################################################################
# RETURN HEALTH OF THE APP
######################################################################


@app.route("/health")
def health():
    return jsonify(dict(status="OK")), 200

######################################################################
# COUNT THE NUMBER OF PICTURES
######################################################################


@app.route("/count")
def count():
    """return length of data"""
    if data:
        return jsonify(length=len(data)), 200

    return {"message": "Internal server error"}, 500


######################################################################
# GET ALL PICTURES
######################################################################
@app.route("/picture", methods=["GET"])
def get_pictures():
    if data:
        return jsonify(data), 200
    return {"message": "Not found"}, 404



######################################################################
# GET A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["GET"])
def get_picture_by_id(id):
    if data:
        for picture in data:
            if picture["id"] == id:
                return jsonify(picture), 200
        return {"message": "Not found"}, 404
    return {"message": "Something went wrong"}, 500


######################################################################
# CREATE A PICTURE
######################################################################
@app.route("/picture", methods=["POST"])
def create_picture():
    new_pic = request.json
    print(new_pic)
    if data:
        for pic in data:
            if new_pic.get("id") == pic["id"]:
                return {"Message": f"picture with id {pic['id']} already present"}, 302
        data.append(new_pic)
        return new_pic, 201
    return {"message": "Something went wrong"}, 500


######################################################################
# UPDATE A PICTURE
######################################################################


@app.route("/picture/<int:id>", methods=["PUT"])
def update_picture(id):
    new_pic = request.json
    if data:
        i = 0
        for pic in data:
            if pic["id"] == id:
                data[i] = new_pic
                return {"message": "No content"}, 204
            i += 1
        return {"message": "Picture not found"}, 404
    return {"message": "Server error"}



######################################################################
# DELETE A PICTURE
######################################################################
@app.route("/picture/<int:id>", methods=["DELETE"])
def delete_picture(id):
    if data:
        for pic in data:
            if pic["id"] == id:
                data.remove(pic)
                return Response(status=204)
        return {"message": "Picture not found"}, 404
    return {"message": "Something went wrong"}, 500