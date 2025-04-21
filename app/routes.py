from flask import Blueprint, render_template

main = Blueprint('main', __name__)

@main.route('/')
def index():
    return render_template('index.html')

@main.route('/upload')
def upload():
    return render_template('upload.html')

@main.route('/visualize')
def visualize():
    return render_template('visualize.html')

@main.route('/share')
def share():
    return render_template('share.html')

# ADD THESE TWO TEMPORARY ROUTES
@main.route('/login')
def login():
    return "<h1>Login Page Coming Soon</h1>"

@main.route('/register')
def register():
    return "<h1>Register Page Coming Soon</h1>"
