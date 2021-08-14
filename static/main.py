import os
from flask import Flask, render_template, request, redirect, url_for
import sys
from math import ceil
from db import Database
from datetime import datetime
from PIL import Image

application = Flask(__name__)
size = (600, 600)

@application.route("/")
def main():
    return render_template("main.html")

@application.route("/collection")
def collection():
    return redirect(url_for("collection_page", id=1))

@application.route("/collection/<int:id>")
def collection_page(id):
    filelist = os.listdir('static/image/db/thumbnail')
    pagenum = ceil((len(filelist))/16)
    if id == pagenum:
        filelist = filelist[(id-1)*16:]
    else:
        filelist = filelist[(id-1)*16:id*16]
    length = len(filelist)
    return render_template("collection.html", id = id, filelist = filelist, pagenum=pagenum, length=length)

@application.route("/about")
def about():
    return render_template("about.html")

@application.route("/create_button")
def create_button():
    return render_template("create_button.html")

@application.route("/create", methods=['POST', 'GET'])
def create():
    if request.method == 'POST':
        result = request.form
        uploaded_file = request.files["file"]
        s = datetime.now().strftime('%Y%m%d%H%M%S')
        uploaded_file.save("static/image/db/%s.jpg" %s)

        im = Image.open("static/image/db/%s.jpg" %s)
        im.thumbnail(size)
        im.save('static/image/db/' + '/thumbnail/' + s + ".jpg")

        data = [result['title'], result['description']]
        db.saveID(s, data)
        return redirect(url_for("collection"))

@application.route("/update_button/<id>")
def update_button(id):
    title, content = db.getID(id)
    return render_template("update_button.html", id=id, title=title, content=content)

@application.route("/update", methods=['POST', 'GET'])
def update():
    if request.method == 'POST':
        result = request.form
        imageID = result['imageID']
        if request.files["file"].filename != '':
            uploaded_file = request.files["file"]
            uploaded_file.save("static/image/db/%s.jpg" %(imageID))
        data = [result['title'], result['description']]
        db.updateID(imageID, data)
        return redirect(url_for("collection"))

@application.route("/delete", methods=['POST', 'GET'])
def delete():
    if request.method == 'POST':
        result = request.form
        imageID = result['imageID']
        os.remove("static/image/db/%s.jpg"%(imageID))
        db.deleteID(imageID)
        return redirect(url_for("collection"))

@application.route("/image/<id>")
def image(id):
    title, content = db.getID(id)
    return render_template("image.html", id=id, title=title, content=content)

if __name__ == "__main__":
    db = Database()
    application.run(debug=True)