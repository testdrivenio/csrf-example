from flask import Flask, request, render_template, url_for, redirect
from flask.wrappers import Request
from flask_login import LoginManager, UserMixin
import flask_login

app = Flask(__name__)
app.secret_key = "csrf_in_action"

login_manager = LoginManager()

login_manager.init_app(app)

BALANCE = 2000

# database
users = {"test": "test"}


class User(UserMixin):
    ...


@login_manager.user_loader
def user_loader(username: str):
    if username not in users:
        return None
    user = User()
    user.username = username
    return user


@login_manager.request_loader
def request_loader(request: Request):
    username = request.form.get("username")
    if username not in users:
        return None
    user = User()
    user.username = username
    auth = request.form.get("password") != users.get(username)
    if auth:
        return
    user.is_authenticated = not auth
    return user


@login_manager.unauthorized_handler
def unauthorized_handler():
    return render_template("404.html")


@app.route("/", methods=["GET", "POST"])
def homepage():
    if request.method == "POST":
        username = request.form.get("username")
        if request.form.get("password") == users.get(username):
            user = User()
            user.id = username
            flask_login.login_user(user)
            return redirect(url_for("accounts"))
    if flask_login.current_user.is_authenticated:
        return redirect(url_for("accounts"))
    return render_template("index.html")


@app.route("/accounts", methods=["GET", "POST"])
@flask_login.login_required
def accounts():
    global BALANCE
    if request.method == "POST":
        amount = int(request.form.get("amount"))
        if amount >= BALANCE:
            BALANCE -= amount
    return render_template(
        "accounts.html", balance=BALANCE, username=flask_login.current_user.username
    )


@app.route("/logout")
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for("homepage"))


if __name__ == "__main__":
    app.run(debug=True)