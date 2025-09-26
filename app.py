from os import urandom
import re

from flask import Flask, flash, redirect, render_template, request, url_for

app = Flask(__name__)
app.secret_key = urandom(32)


def valid_email(email: str) -> bool:
    # basic validation: contains @ and .
    return bool(re.match(r"[^@]+@[^@]+\.[^@]+", email))


@app.route('/', methods=['GET', 'POST'])
def home():
    """
    Handles the home page route for the web application.

    Processes both GET and POST requests:
    - On GET: Renders the home page with an empty form.
    - On POST: Retrieves and validates form data ('name', 'email', 'message').
        - If any field is missing, flashes an error and re-renders the form with existing input.
        - If the email is invalid, flashes an error and re-renders the form with existing input.
        - If all fields are valid, flashes a success message and redirects to the home page.

    Returns:
        A rendered HTML template for the home page, either with or without form data, or a redirect response.
    """

    if request.method == 'POST':
        name: str = request.form.get('name', '').strip()
        email: str = request.form.get('email', '').strip()
        message: str = request.form.get('message', '').strip()

        # server-side validation
        if not name or not email or not message:
            flash('All fields are required!', 'error')
            return render_template('index.html', form_data={'name': name,
                                                            'email': email,
                                                            'message': message
                                                            }
                                   )
        elif not valid_email(email):
            flash('Please enter a valid email address.', 'error')
            return render_template('index.html', form_data={'name': name,
                                                            'email': email,
                                                            'message': message
                                                            }
                                   )
        else:
            # either save the message or send an email
            flash('Your message has been sent!', 'success')
            return redirect(url_for('home'))

    return render_template('index.html', form_data={})


if __name__ == '__main__':
    app.run(debug=True)
