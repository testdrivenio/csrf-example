from flask import Flask, Response, abort, redirect, render_template, request, url_for
from flask_login import (
    LoginManager,
    UserMixin,
    current_user,
    login_required,
    login_user,
    logout_user,
)
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)
app.config.update(
    DEBUG=True,
    SECRET_KEY="secret_sauce",
)

login_manager = LoginManager()
login_manager.init_app(app)

csrf = CSRFProtect()
csrf.init_app(app)


# database
users = [
    {
        "id": 1,
        "username": "test",
        "password": "test",
        "balance": 2000,
    },
    {
        "id": 2,
        "username": "hacker",
        "password": "hacker",
        "balance": 0,
    },
]


class User(UserMixin):
    ...


def get_user(user_id: int):
    for user in users:
        if int(user["id"]) == int(user_id):
            return user
    return None


@login_manager.user_loader
def user_loader(id: int):
    user = get_user(id)
    if user:
        user_model = User()
        user_model.id = user["id"]
        return user_model
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
                user_model = User()
                user_model.id = user["id"]
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
    user = get_user(current_user.id)

    if request.method == "POST":
        amount = int(request.form.get("amount"))
        account = int(request.form.get("account"))

        transfer_to = get_user(account)

        if amount <= user["balance"] and transfer_to:
            user["balance"] -= amount
            transfer_to["balance"] += amount

    return render_template(
        "accounts.html",
        balance=user["balance"],
        username=user["username"],
    )


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug=True)
