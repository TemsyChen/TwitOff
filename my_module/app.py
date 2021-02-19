"""Main application and routing logic for TwitOff"""

from flask import Flask, render_template, request
from .models import DB, User
from .twitter import add_or_update_user
from .predict import predict_user
import logging


def create_app():

    """create and configure an instance of the Flask application"""

    app = Flask(__name__)

    #allows detailed error logs to exist on Heroku
    gunicorn_logger = logging.getLogger('gunicorn.error')
    app.logger.handlers = gunicorn_logger.handlers
    app.logger.setLevel(gunicorn_logger.level)

    app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///db.sqlite3'  #getenv("DATABASE_URI")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS']=False

    #initializes database
    DB.init_app(app)

    #decorator listens for specific endpoint visits
    #'GET' means this route gets an endpoint/URL
    @app.route("/", methods=['GET']) #http://127.0.0.1:5000/
    def root():
        DB.drop_all()
        DB.create_all()
        #insert_data()
        example_users = ['elonmusk', 'katyperry', 'rihanna', 'barackobama']
        for user in example_users:
            add_or_update_user(user)
        #renders base.html template and passes down title and users
        return render_template('hello.html', title="TwitOff", users=User.query.all())

    @app.route('/update')
    def update():
        # insert_example_users()
        return render_template('hello.html', title="TwitOff", users=Users.query.all())

    @app.route('/reset')
    def reset():
        DB.drop_all()
        DB.create_all()
        return render_template('hello.html', title="TwitOff")

    #This route 'POST's data to the server
    @app.route('/compare', methods=['POST'])
    def compare():
        user1 = request.form['selected_user_1'] #extracts the form data
        user2 = request.form['selected_user_2']
        tweet_text = request.values['tweet_text']

        if user1 == user2:
            message = "Cannot compare the same user to itself"

        else:
            prediction = predict_user(user1, user2, tweet_text)
            message = str(prediction) + " is more likely to have said " + str(tweet_text)

        return render_template('prediction.html', title="Predict Tweet Author", message=message)

    return app

app=create_app()

# if __name__ == "__main__":
#     app.run()
