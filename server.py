""" Investable Server """

from flask import Flask, render_template, flash
# from flask_debugtoolbar import DebugToolbarExtension
import jinja2


app = Flask(__name__)

# jinja debugger
app.jinja_env.undefined = jinja2.StrictUndefined
app.jinja_env.auto_reload = True


@app.route('/')
def homepage():
    """ Brings user to the homepage. """
    return render_template('index.html')


@app.route('/login')
def login():
    """ Brings user to the login page. """
    return render_template('login.html')


@app.route('/register', methods=['GET'])
def register():
    """ Brings user to the registration page. """
    return render_template('registration.html')


# @app.route('/register', methods=['POST'])
# def add_user_registration():
#     """ Processes a new user registration. """

#     if username exists:
#         flash('Sorry, that email has already been registered. Login instead?')
#         return redirect('/register')

#     else create a new user:
#         flash('You have successfully created an account. Please login to continue.')
#         return redirect('/')

@app.route('/account')
def account_details():
    """ Shows a user's account details. """

    return render_template('account.html')


if __name__ == "__main__":
    app.debug = True

    # Use the DebugToolbar
    # DebugToolbarExtension(app)

    app.run(host="0.0.0.0", port=4000)
