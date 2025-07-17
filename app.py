#importing necessary modules
from flask import Flask, render_template, request, redirect ,url_for,session
from flask_sqlalchemy import SQLAlchemy
from datetime import date , timedelta
from werkzeug.security import generate_password_hash, check_password_hash

#important configurations
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///haris.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(minutes=1)
app.config['SECRET_KEY'] = '123456'
db = SQLAlchemy(app)

#Making The todo app
#defining class for app table
class Todo(db.Model):
    sno = db.Column(db.Integer,primary_key = True)
    title = db.Column(db.String(200),nullable = False)
    desc = db.Column(db.String(5000),nullable = False)
    date = db.Column(db.Date, default = date.today)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

#Making user Table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20) , nullable=False, unique=True)
    password = db.Column(db.String(200) , nullable=False)


#functional aspect of app
@app.route('/' , methods = ['GET','POST'])
def home():
    if 'user_id' not in session:
        return redirect('/signup')

    if request.method == 'POST':
        title = request.form.get("title")
        desc = request.form.get("desc")

        new_todo = Todo(title=title, desc=desc )
        db.session.add(new_todo)
        db.session.commit()

    all_todos = Todo.query.all()
    return render_template('index.html' , allTodo = all_todos)

#signup route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        hashed_pass = generate_password_hash(password)
        user = User(username=username , password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        return redirect('/login')
    return render_template('signup.html')

#login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password, password):
            session.permanent = True
            session['user_id'] = user.id
            return redirect('/')
        return 'Invalid Credentials'
    return render_template('login.html')

# Logout
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/login')

#Defining Delete Action
@app.route("/delete/<int:sno>" )
def delete(sno):
    if 'user_id' not in session:
        return redirect('/login')
    todo = Todo.query.get_or_404(sno)
    db.session.delete(todo)
    db.session.commit()
    return redirect ('/')


if __name__ == "__main__":
    app.run(debug=True)