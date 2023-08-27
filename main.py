import base64
import io
import re
import time

import face_recognition
from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route("/", methods=['GET'])
def main():
    return jsonify({
        "success": True,
        "message": "Server is working",
    })


def decode_base64(data):
    image_data = re.sub('^data:image/.+;base64,', '', data)
    return base64.b64decode(image_data)


@app.route("/compare", methods=['POST'])
def compare():
    try:
        data = request.json  # Assuming JSON request
        passport_base64 = data.get('passport')
        face_base64 = data.get('face')

        start_time = time.time()

        passport_bytes = decode_base64(passport_base64)
        face_bytes = decode_base64(face_base64)

        passport_image = face_recognition.load_image_file(io.BytesIO(passport_bytes))
        face_image = face_recognition.load_image_file(io.BytesIO(face_bytes))

        passport_encoding = face_recognition.face_encodings(passport_image)[0]
        face_encoding = face_recognition.face_encodings(face_image)[0]

        comparison_start_time = time.time()
        results = face_recognition.compare_faces([passport_encoding], face_encoding)
        comparison_time = time.time() - comparison_start_time

        return jsonify({
            "success": True,
            "match": bool(results[0]),
            "message": "It's the same person" if results[0] else "It's not the same person",
            "image_save_time": comparison_start_time - start_time,
            "comparison_time": comparison_time,
        })

    except Exception as e:
        return jsonify({
            "success": False,
            "message": str(e),
        })


if __name__ == "__main__":
    app.run()
