from flask import Flask, request, jsonify, render_template
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
def home():
    return render_template('index.html')



@app.route('/secure_login', methods=['POST'])
def secure_login():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Dati di richiesta non validi"}), 400

    username = data['username']
    password = data['password']

    # Utilizzo di una query parametrizzata per evitare SQL injection
    sql = text("SELECT * FROM user WHERE username = :username AND password = :password")

    conn = db.engine.connect()

    # Esecuzione della query utilizzando i parametri
    res = conn.execute(sql, {"username": username, "password": password})
    names = [row[0] for row in res]
    print(names)

    # Utilizzo di una query parametrizzata con SQLAlchemy
    # user = User.query.filter_by(username=username, password=password).first()

    if names:
        return jsonify({"message": "Accesso riuscito"})

    return jsonify({"message": "Accesso fallito"}), 401


@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()

    if not data or 'username' not in data or 'password' not in data:
        return jsonify({"message": "Dati di richiesta non validi"}), 400

    username = data['username']
    password = data['password']

    # Verifica se lo username è già in uso
    existing_user = User.query.filter_by(username=username).first()

    if existing_user:
        return jsonify({"message": "Lo username è già in uso"}), 400

    # Creazione di un nuovo utente da aggiungere al database
    new_user = User(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"message": "Registrazione riuscita"})


if __name__ == '__main__':
    app.run(debug=False)
