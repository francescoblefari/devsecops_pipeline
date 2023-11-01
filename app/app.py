from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import text

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+mysqlconnector://root:root@localhost/logindemo'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)

@app.route("/")
def indec():
    return "ciao"

@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Invalid request data"}), 400

    username = data['username']
    password = data['password']

    # Execute a raw SQL query to check the username and password
    sql = f"SELECT * FROM user WHERE username = '{username}' AND password = '{password}'"

    conn = db.engine.connect()

    
    # Execute the vulnerable SQL query concatenating user-provided input.
    res = conn.execute(text(sql))
    names = [row[0] for row in res]
    print(names)

    if names:
        return jsonify({"message": "Login successful"})

    return jsonify({"message": "Login failed"}), 401

if __name__ == '__main__':
    app.run(debug=True)
