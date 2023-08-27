from flask import Flask, request
from random import randint
import face_recognition

app = Flask(__name__)


@app.route(rule="/", methods=['GET', 'POST'])
def main():
    return {
        "success": True,
        "message": "Server is working",
    }


@app.route(rule="/compare", methods=['POST'])
def compare():
    r = randint(a=0, b=10)
    passport_img_path = 'uploads/' + str(r) + '_passport.jpg'
    face_img_path = 'uploads/' + str(r) + '_face.jpg'
    passport = request.files['passport']
    face = request.files['face']
    passport.save(passport_img_path)
    face.save(face_img_path)
    known_image = face_recognition.load_image_file(passport_img_path)
    unknown_image = face_recognition.load_image_file(face_img_path)
    biden_encoding = face_recognition.face_encodings(known_image)[0]
    unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
    results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
    return {
        "success": results,
        "message": "It's same" if results else "Images saved",
    }
