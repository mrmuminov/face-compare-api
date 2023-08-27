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


@app.route("/compare", methods=['POST'])
def compare():
    try:
        data = request.json  # Assuming JSON request
        passport_base64 = data.get('passport')
        face_base64 = data.get('face')

        def decode_base64(data):
            image_data = re.sub('^data:image/.+;base64,', '', data)
            return base64.b64decode(image_data)

        start_time = time.time()

        passport_bytes = decode_base64(passport_base64)
        face_bytes = decode_base64(face_base64)

        known_image = face_recognition.load_image_file(io.BytesIO(passport_bytes))
        unknown_image = face_recognition.load_image_file(io.BytesIO(face_bytes))

        biden_encoding = face_recognition.face_encodings(known_image)[0]
        unknown_encoding = face_recognition.face_encodings(unknown_image)[0]

        comparison_start_time = time.time()
        results = face_recognition.compare_faces([biden_encoding], unknown_encoding)
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
