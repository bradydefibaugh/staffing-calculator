from flask import Flask, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
from calculator import calculate_staff, calculate_cost

app = Flask(__name__)
app.secret_key = 'replace_with_a_secret_key'

# Initialize LoginManager
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

# Simple in-memory user store. In production, use a database and hashed passwords.
users = {
    'admin': {'password': 'password'}
}

class User(UserMixin):
    def __init__(self, id):
        self.id = id

@login_manager.user_loader
def load_user(user_id):
    if user_id in users:
        return User(user_id)
    return None

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        # Check credentials
        if username in users and users[username]['password'] == password:
            user = User(username)
            login_user(user)
            return redirect(url_for('calculator'))
        return 'Invalid credentials', 401
    # Simple HTML login form
    return '''
        <form method="post">
            <input type="text" name="username" placeholder="Username" />
            <input type="password" name="password" placeholder="Password" />
            <input type="submit" value="Login" />
        </form>
    '''

@app.route('/calculator', methods=['GET', 'POST'])
@login_required
def calculator():
    if request.method == 'POST':
        # Retrieve form values and convert to float
        required_hours = float(request.form.get('required_hours', 0))
        hours_per_employee = float(request.form.get('hours_per_employee', 1))
        hourly_rate = float(request.form.get('hourly_rate', 0))
        # Calculate staffing and cost using existing functions
        num_staff = calculate_staff(required_hours, hours_per_employee)
        total_cost = calculate_cost(num_staff, hourly_rate, hours_per_employee)
        return f'Staff needed: {num_staff}<br>Total cost: ${total_cost:.2f}'
    # HTML form for calculator input
    return '''
        <form method="post">
            <input type="number" step="any" name="required_hours" placeholder="Required hours" />
            <input type="number" step="any" name="hours_per_employee" placeholder="Hours per employee" />
            <input type="number" step="any" name="hourly_rate" placeholder="Hourly rate" />
            <input type="submit" value="Calculate" />
        </form>
    '''

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))

if __name__ == '__main__':
    # Run the app in debug mode for development
    app.run(debug=True)
