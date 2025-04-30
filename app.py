# Importing the modules
# Render_template renders HTML, request handles form data
# Redirect and url_for direct users to a route in the website navigation
from flask import Flask, render_template, request, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Create a new Flask app
app = Flask(__name__)

# Configure SQLite database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///todos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Define Game Model class
# Define the columns (attributes) for the class
class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    leftOffAt = db.Column(db.String(300), )
    completed = db.Column(db.Boolean, default=False)
    completionDate = db.Column(db.DateTime, default=datetime.utcnow)
    reviewInt = db.Column(db.Float, nullable=True)
    reviewText = db.Column(db.String(500), nullable=True)
    # Add the repr method
    # This is a special Python method that returns
    # a string representing the object
    def __repr__(self):
        return f'<Todo id={self.id} title={self.title} leftOffAt={self.leftOffAt} completed={self.completed} completionDate={self.completionDate} reviewInt={self.reviewInt} reviewText={self.reviewText} >'

# Create the database and table to hold the "log data"
with app.app_context():
    db.create_all()

# Create a home route that displays the To Do list
@app.route('/')
def index():
    games = Game.query.order_by(Game.title.desc()).all()
    return render_template('index.html', games=games)

# Create a route for adding a new To Do to the database
@app.route('/add', methods=['POST'])
def add():
    title = request.form.get('title')
    leftOffAt= request.form.get('leftOffAt')
    completed= True if request.form.get('completed') == 'on' else False
    raw_completionDate = request.form.get('completionDate')
    reviewInt = request.form.get('reviewInt')
    reviewText = request.form.get('reviewText')

    if raw_completionDate:
        try:
            completionDate = datetime.strptime(raw_completionDate, '%Y-%m-%d')
        except ValueError:
            completionDate = datetime.utcnow()
    else:
        completionDate = None

    new_game = Game(
        title=title,
        leftOffAt=leftOffAt,
        completed=completed,
        completionDate=completionDate,
        reviewInt=float(reviewInt) if reviewInt else None,
        reviewText=reviewText)
    
    db.session.add(new_game)
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to mark a To Do item as done
@app.route('/toggle/<int:game_id>')
def toggle(game_id):
    game = Game.query.get_or_404(game_id)
    game.completed = not game.completed
    db.session.commit()
    return redirect(url_for('index'))

# Create a route to delete a To Do item
@app.route('/delete/<int:game_id>')
def delete(game_id):
    game = Game.query.get_or_404(game_id)
    db.session.delete(game)
    db.session.commit()
    return redirect(url_for('index'))

# Start the Flask app in debug mode
# Flask provides a debugger & shows the stack trace if an error occurs
# Debug mode also reloads the page if you change the
# code so you don't need to restart the server.
if __name__ == '__main__':
    app.run(debug=True)