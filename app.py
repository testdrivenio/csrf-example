from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
)

login_manager = LoginManager()
login_manager.init_app(app)


# database
users = [
    {
        "username": "test",
        "password": "test",
        "balance": 2000,
    }
]


class User(UserMixin):
    def __init__(self, username):
        self.id = username
        self.username = username


def get_user(username: str):
    for user in users:
        if user["username"] == username:
            return user
    return None


@login_manager.user_loader
def user_loader(username: str):
    user = get_user(username)
    if user:
        return User(username=user["username"])
    return None


@app.errorhandler(401)
def unauthorized(error):
    return Response("Not authorized"), 401


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        for user in users:
            if user["username"] == username and user["password"] == password:
                user_model = User(username=user["username"])
                login_user(user_model)
                return redirect(url_for("accounts"))
            else:
                return abort(401)

    if current_user.is_authenticated:
        return redirect(url_for("accounts"))

    return render_template("index.html")


@app.route("/accounts", methods=["GET", "POST"])
@login_required
def accounts():
    user = get_user(current_user.username)

    if request.method == "POST":
        amount = int(request.form.get("amount"))
        if amount <= user["balance"]:
            user["balance"] -= amount

    return render_template(
        "accounts.html",
        balance=user["balance"],
        username=current_user.username,
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug=True)
