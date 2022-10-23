from datetime import datetime
from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.db'
db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.String(200), nullable=False)
    completed = db.Column(db.Integer, default=0)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<Task %r>' % self.id


@app.route("/", methods=["POST", "GET"])
def index():
    if request.method == "POST":
        taskcontent = request.form.get("newtask")
        newtask = Todo(content=taskcontent)
        
        try:
            db.session.add(newtask)
            db.session.commit()
            return redirect('/')

        except:
            return 'failure'


    else:
        tasks = Todo.query.order_by(Todo.date_created).all()
        return render_template("index.html", tasks=tasks)

@app.route("/delete/<int:id>")
def delete(id):
    tasktodelete = Todo.query.get_or_404(id)

    try:
        db.session.delete(tasktodelete)
        db.session.commit()
        return redirect('/')

    except:
        return 'failure'

@app.route("/update/<int:id>", methods=['POST', 'GET'])
def update(id):
    task = Todo.query.get_or_404(id)

    if request.method == "POST":

        task.content = request.form.get("content")
        
        try:
            db.session.commit()
            return redirect('/')

        except:
            return 'failure'
    
    else:
        return render_template('update.html', task=task)


if __name__ == '__main__':
    app.run(debug=True)

