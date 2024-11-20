from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from Crypto.Util.number import getPrime
from random import randint


app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///marks.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.secret_key = "your_secret_key"

db = SQLAlchemy(app)


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(50))
    role = db.Column(db.String(10))


class Marks(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    subject = db.Column(db.String(50))
    marks = db.Column(db.Integer)


class Paillier:
    def __init__(self, bit_length=10):
        p = getPrime(bit_length)
        q = getPrime(bit_length)

        self.n = p * q
        self.n_square = self.n * self.n
        self.g = self.n + 1

        self.lmbda = (p - 1) * (q - 1)
        self.mu = self.mod_inverse(self.lmbda, self.n)

    def mod_inverse(self, a, m):
        def egcd(a, b):
            if a == 0:
                return b, 0, 1
            else:
                g, x, y = egcd(b % a, a)
                return g, y - (b // a) * x, x

        g, x, _ = egcd(a, m)
        if g != 1:
            raise Exception("Modular inverse does not exist.")
        else:
            return x % m

    def encrypt(self, plaintext):
        r = randint(1, self.n - 1)

        c = (
            pow(self.g, plaintext, self.n_square) * pow(r, self.n, self.n_square)
        ) % self.n_square

        return c

    def decrypt(self, ciphertext):
        numerator = pow(ciphertext, self.lmbda, self.n_square) - 1
        plaintext = (numerator // self.n * self.mu) % self.n

        return plaintext


paillier = Paillier()


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        role = request.form["role"]
        new_user = User(username=username, password=password, role=role)
        db.session.add(new_user)
        db.session.commit()
        return redirect("/login")
    return render_template("signup.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return render_template("login.html", error="Invalid username or password")
    return render_template("login.html")


@app.route("/dashboard", methods=["GET", "POST"])
def dashboard():
    if "user_id" in session:
        user_id = session["user_id"]
        user = User.query.get(user_id)
        if user.role == "professor":
            students = User.query.filter_by(role="student").all()
            selected_student_id = request.args.get(
                "student"
            )  # Get the selected student ID from the query parameter
            selected_student = None
            if selected_student_id:
                selected_student = User.query.get(selected_student_id)
                selected_student.marks = Marks.query.filter_by(
                    user_id=selected_student_id
                ).all()
            return render_template(
                "professor_dashboard.html",
                students=students,
                selected_student=selected_student,
            )
        else:
            marks = Marks.query.filter_by(user_id=user_id).all()
            fin_marks = 0
            count = 0
            for mark in marks:
                decrypted_value = paillier.decrypt(mark.marks)
                fin_marks += decrypted_value
                count += 1
            percentage = (fin_marks / (count * 100)) * 100

            return render_template(
                "student_dashboard.html", marks=marks, percentage=percentage
            )
    else:
        return redirect("/login")


@app.route("/add_marks", methods=["GET", "POST"])
def add_marks():
    if "user_id" in session:
        if request.method == "POST":
            subject = request.form["subject"]
            vmarks = int(request.form["marks"])
            nmarks = paillier.encrypt(vmarks)
            user_id = request.form["student"]
            new_marks = Marks(user_id=user_id, subject=subject, marks=nmarks)
            db.session.add(new_marks)
            db.session.commit()
            return redirect("/dashboard")
        students = User.query.filter_by(role="student").all()
        return render_template("add_marks.html", students=students)
    else:
        return redirect("/login")


@app.route("/logout")
def logout():
    session.pop("user_id", None)
    return redirect("/")


if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True)