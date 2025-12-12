"""
Flask application with hashed passwords and in-memory user store.

This module defines a simple web interface that wraps the staffing
calculator functions behind a login screen. Passwords are hashed
using Werkzeug's `generate_password_hash` and validated with
`check_password_hash`, following best practices for password storage.
Use this as a starting point for a more robust authentication
implementation. See the Flask‐Login documentation for extending
user management and session handling【537517364647614†L145-L183】.
"""

from flask import Flask, render_template_string, redirect, url_for, request, flash
from flask_login import (
    LoginManager,
    login_user,
    login_required,
    logout_user,
    UserMixin,
)
from werkzeug.security import generate_password_hash, check_password_hash
import os

from calculator import calculate_staff, calculate_cost


app = Flask(__name__)
# It's good practice to load the secret key from an environment variable so
# that it isn’t hard‑coded. A default is provided for development.
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "super-secret-key")


# Set up the login manager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# In-memory user store with hashed password. In a real application, use a
# database and hashed passwords stored per user. See the Flask-Login docs for
# details【537517364647614†L145-L183】.
users = {
    "admin": generate_password_hash("password"),
}


class User(UserMixin):
    """Minimal user class for Flask‑Login."""

    def __init__(self, username: str) -> None:
        self.id = username


@login_manager.user_loader
def load_user(user_id: str):
    """Return a User object if the ID exists in our user store."""
    if user_id in users:
        return User(user_id)
    return None


# Templates defined as raw strings for simplicity. You can move these to
# separate HTML files and render them with render_template.
LOGIN_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Login</title>
</head>
<body>
    <h2>Login</h2>
    <form method="post">
        <label for="username">Username:</label><br>
        <input type="text" id="username" name="username" required><br>
        <label for="password">Password:</label><br>
        <input type="password" id="password" name="password" required><br>
        <button type="submit">Login</button>
    </form>
    {% with messages = get_flashed_messages(category_filter=['error']) %}
      {% if messages %}
        <ul>
        {% for message in messages %}
          <li style="color: red;">{{ message }}</li>
        {% endfor %}
        </ul>
      {% endif %}
    {% endwith %}
</body>
</html>
"""

CALCULATOR_TEMPLATE = """
<!doctype html>
<html lang="en">
<head>
    <meta charset="utf-8">
    <title>Staffing Calculator</title>
</head>
<body>
    <h2>Staffing Calculator</h2>
    <form method="post">
        <label for="required_hours">Required hours:</label><br>
        <input type="number" id="required_hours" name="required_hours" step="any" required><br>
        <label for="hours_per_employee">Hours per employee:</label><br>
        <input type="number" id="hours_per_employee" name="hours_per_employee" step="any" required><br>
        <label for="hourly_rate">Hourly rate:</label><br>
        <input type="number" id="hourly_rate" name="hourly_rate" step="0.01" required><br>
        <button type="submit">Calculate</button>
    </form>
    {% if result %}
    <p>Staff needed: {{ result.staff_needed }}</p>
    <p>Total cost: ${{ '%.2f'|format(result.total_cost) }}</p>
    {% endif %}
    <p><a href="{{ url_for('logout') }}">Logout</a></p>
</body>
</html>
"""


@app.route("/login", methods=["GET", "POST"])
def login():
    """Handle user login and authenticate against the hashed password."""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        hashed = users.get(username)
        # Use check_password_hash to compare the submitted password to the stored hash.
        if hashed and check_password_hash(hashed, password):
            user = User(username)
            login_user(user)
            return redirect(url_for("calculator"))
        flash("Invalid username or password", "error")
    return render_template_string(LOGIN_TEMPLATE)


@app.route("/logout")
@login_required
def logout():
    """Log out the current user and redirect to login."""
    logout_user()
    return redirect(url_for("login"))


@app.route("/calculator", methods=["GET", "POST"])
@login_required
def calculator():
    """Render and handle the staffing calculator form."""
    result = None
    if request.method == "POST":
        try:
            required_hours = float(request.form.get("required_hours"))
            hours_per_employee = float(request.form.get("hours_per_employee"))
            hourly_rate = float(request.form.get("hourly_rate"))
        except (TypeError, ValueError):
            flash("Please enter valid numbers", "error")
        else:
            staff_needed = calculate_staff(required_hours, hours_per_employee)
            total_cost = calculate_cost(staff_needed, hours_per_employee, hourly_rate)
            result = {
                "staff_needed": staff_needed,
                "total_cost": total_cost,
            }
    return render_template_string(CALCULATOR_TEMPLATE, result=result)


if __name__ == "__main__":
    # Debug mode is great for development but should be disabled in production.
    app.run(debug=True)