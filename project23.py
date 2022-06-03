rom flask import Flask, render_template, request, redirect, jsonify, g
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, Boolean, Column, Integer, Date, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime


#connect to db
DB_URL = 'postgres+psycopg2://@localhost:5432/pet_hotel'

#setting config for sqlalchemy and postgres
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False 
db = SQLAlchemy(app)

print('databse up')
class Owner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    number_of_pets = db.Column(db.String(200), nullable=False)
    def __repr__(self):
        return '<Task %r' % self


class Pets(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    owner_id = db.Column(ForeignKey('Owner.id'))
    # owner_id = db.Column(db.Int, nullable=False)
    name = db.Column(db.String(50), nullable=False)
    breed = db.Column(db.String(50), nullable=False)
    color = db.Column(db.String(20), nullable=False)
    checked_in  = db.Column(db.Boolean , nullable=False, default=False)
    date_checked = db.Column(db.DateTime, default=datetime.utcnow)
    def __init__(self, id, owner_id, name, breed, color, checked_in, date_checked): 
        self.checked_in = checked_in 



@app.route('/pets', methods=['POST', 'GET'])
def pets():
    print('databse up')
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Pets(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/')

    else:
        tasks = Pets.query.order_by(Pets.date_checked).all()
        print(tasks)
        return redirect('/')


@app.route('/pets/delete/<int:id>')
def delete_one(id):
    task_to_delete = Pets.query.get_or_404(id)

    try:
        db.session.delete_one(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'no delete my friend, its mine!'



@app.route('/owner', methods=['POST', 'GET'])
def index_two():
    print('databse up')
    if request.method == 'POST':
        task_content = request.form['content']
        new_task = Owner(content=task_content)

        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return redirect('/')

    else:
        tasks = Owner.query.order_by(Owner.name).all()
        print(tasks)
        return redirect('/')

@app.route('/owner/delete/<int:id>')
def delete_two(id):
    task_to_delete = Owner.query.get_or_404(id)

    try:
        db.session.delete_two(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'no delete my friend, its mine!'

# @app.route('/update/<int:id>', methods=['GET', 'POST'])
# def update(id):
#     task = Todo.query.get_or_404(id)

#     if request.method == 'POST':
#         task.content = request.form['content']

#         try:
#             db.session.commit()
#             return redirect('/')
#         except:
#             return 'No! the Updator is angry'
#     else:
#         return render_template('update.html', task=task)


if __name__ == "__main__":
    app.run(debug=True)
