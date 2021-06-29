from flask import Flask, render_template, request, redirect
from werkzeug.utils import redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class todo(db.Model):
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    date_time = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        query = todo(title=title, description=description)
        db.session.add(query)
        db.session.commit()
    allquery = todo.query.all()
    return render_template('index.html', allquery = allquery)

@app.route("/about")
def about():
    return render_template('about.html')

@app.route("/update/<int:sno>", methods=["GET", "POST"])
def update(sno):
    if request.method == "POST":
        title = request.form['title']
        description = request.form['description']
        query = todo.query.filter_by(sno=sno).first()
        query.title = title
        query.description = description
        db.session.add(query)
        db.session.commit()
        return redirect("/")
    query = todo.query.filter_by(sno=sno).first()
    return render_template('update.html', allquery=query)

@app.route("/delete/<int:sno>")
def delete(sno):
    query = todo.query.filter_by(sno=sno).first()
    db.session.delete(query)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True , port=8000)