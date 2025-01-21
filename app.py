from flask import Flask , render_template,request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db  = SQLAlchemy(app)

class Todo(db.Model):
    S_No = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    desc = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.S_No} - {self.title}"

# Create the database tables
with app.app_context():
    db.create_all()

@app.route("/", methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo(title=title, desc=desc)
        db.session.add(todo)
        db.session.commit()

    allTodo = Todo.query.all()
    return render_template('index.html', allTodo=allTodo)
    
 
@app.route("/update/<int:S_No>", methods=['GET','POST'])
def update(S_No):
    if request.method=='POST':
        title=request.form['title']
        desc=request.form['desc']
        todo = Todo.query.filter_by(S_No=S_No).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")

    todo = Todo.query.filter_by(S_No=S_No).first()
    return render_template('update.html', todo=todo)

@app.route("/delete/<int:S_No>")
def delete(S_No):
    todo = Todo.query.filter_by(S_No=S_No).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")


#this snippet of code is used to call the website in debug mode
if __name__ == "__main__":
    app.run(debug=True, port=8000)