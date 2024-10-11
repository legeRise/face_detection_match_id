from flask import Flask, request, jsonify
import face_recognition
import os

app = Flask(__name__)

@app.route('/compare_faces', methods=['POST'])
def compare_faces():
    # Check if the post request has the images
    if 'image1' not in request.files or 'image2' not in request.files:
        return jsonify({"error": "Please provide both images."}), 400

    image1_file = request.files['image1']
    image2_file = request.files['image2']

    # Load images
    image1 = face_recognition.load_image_file(image1_file)
    image2 = face_recognition.load_image_file(image2_file)

    # Get face encodings (features)
    encoding1 = face_recognition.face_encodings(image1)
    encoding2 = face_recognition.face_encodings(image2)

    # Check if faces were found
    if len(encoding1) == 0 or len(encoding2) == 0:
        return jsonify({"error": "No faces found in one of the images."}), 400

    # Compare faces
    results = face_recognition.compare_faces([encoding1[0]], encoding2[0])
    
    return jsonify({"match": results[0]})

if __name__ == '__main__':
    app.run(host='0.0.0.0',debug=True)
