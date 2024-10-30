from flask import Blueprint, jsonify, request, send_from_directory
import os
import urllib.parse

photos_bp = Blueprint('photos', __name__)

IMAGE_FOLDER = os.path.join(os.getcwd(), 'AbbyBot-News')

@photos_bp.route('/photos', methods=['GET'])
def list_photos():
    try:
        photos = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
        photo_urls = [
            {
                "file_name": photo,
                "url": f"{request.host_url}photos/{urllib.parse.quote(photo)}"
            } for photo in photos
        ]
        return jsonify(photo_urls), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@photos_bp.route('/photos/<path:filename>', methods=['GET'])
def get_photo(filename):
    try:
        decoded_filename = urllib.parse.unquote(filename)
        return send_from_directory(IMAGE_FOLDER, decoded_filename)
    except Exception as e:
        return jsonify({"error": "File not found or an error occurred"}), 404

@photos_bp.route('/generate-photo-urls', methods=['POST'])
def generate_photo_urls():
    try:
        photos = [f for f in os.listdir(IMAGE_FOLDER) if os.path.isfile(os.path.join(IMAGE_FOLDER, f))]
        photo_urls = [
            {
                "file_name": photo,
                "url": f"{request.host_url}photos/{urllib.parse.quote(photo)}"
            } for photo in photos
        ]
        return jsonify({
            "generated_urls": photo_urls
        }), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
