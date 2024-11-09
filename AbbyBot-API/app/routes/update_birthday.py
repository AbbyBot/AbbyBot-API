from flask import Blueprint, jsonify, request
from ..utils.birthday_utils import get_current_birthday, update_user_birthday
from datetime import datetime

update_birthday_bd = Blueprint('update_abbybot', __name__)


@update_birthday_bd.route('/update-birthday', methods=['POST'])
def update_birthday():

    user_id = request.json.get('user_id')
    birthday = request.json.get('birthday_date')


    if not user_id or not birthday:
        return jsonify({"error": "Missing user_id or birthday_date", "status_code": 400}), 400


    try:
        birthday_date = datetime.strptime(birthday, '%Y-%m-%d').date()
    except ValueError:
        return jsonify({"error": "Invalid birthday format. Use YYYY-MM-DD.", "status_code": 400}), 400


    today = datetime.today().date()
    if birthday_date > today:
        return jsonify({"error": "Birthday cannot be in the future.", "status_code": 400}), 400
    elif birthday_date.year < 1900:
        return jsonify({"error": "Birthday is too old. Please enter a valid date after 1900.", "status_code": 400}), 400


    current_birthday = get_current_birthday(user_id)

    # Check if the user exists
    if current_birthday is None:
        return jsonify({"error": "No user found with the provided user_id", "status_code": 404}), 404


    if current_birthday == birthday_date:
        return jsonify({"info": "The birthday is already set to this value. No update needed.", "status_code": 200}), 200


    rows_affected = update_user_birthday(user_id, birthday_date)

    if rows_affected > 0:
        return jsonify({"success": f"Birthday updated for user {user_id}", "status_code": 200}), 200
    else:
        return jsonify({"error": "Failed to update the birthday for user {user_id}", "status_code": 500}), 500