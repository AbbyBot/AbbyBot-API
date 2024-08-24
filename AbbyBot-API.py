from flask import Flask, jsonify, request
from flask_mysqldb import MySQL
from config import Config
from dotenv import load_dotenv

# Load dotenv variables
load_dotenv()

app = Flask(__name__)

# Datanbase settings
app.config.from_object(Config)

mysql = MySQL(app)

# English help quotes route
@app.route('/help/en', methods=['GET'])
def get_help_english():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM abbybot.help WHERE language_id = 1")
        rows = cur.fetchall()

        help_list = []
        for row in rows:
            help_list.append({
                'command_code': row[0],
                'command_description': row[1],
                'language_id': row[2]
            })

        return jsonify(help_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Spanish help quotes route
@app.route('/help/es', methods=['GET'])
def get_help_spanish():
    try:
        cur = mysql.connection.cursor()
        cur.execute("SELECT * FROM abbybot.help WHERE language_id = 2")
        rows = cur.fetchall()

        help_list = []
        for row in rows:
            help_list.append({
                'command_code': row[0],
                'command_description': row[1],
                'language_id': row[2]
            })

        return jsonify(help_list)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
