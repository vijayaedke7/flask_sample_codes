from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy


app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='mysql://root:password@localhost:3306/testdb'
db=SQLAlchemy(app)

class Example(db.Model):
    __tablename__='example'
    id = db.Column('id',db.Integer,primary_key=True)
    task = db.Column('task',db.String(200))
    status = db.Column('status',db.Boolean)

    def __init__(self,task,status):
    	self.task=task
    	self.status = status

@app.route('/')
def index():
	incompletetask = Example.query.filter_by(status=False).all()
	completetask = Example.query.filter_by(status=True).all()
	return render_template('home.html',incompletetask=incompletetask,completetask=completetask)

@app.route('/update/<id_>')
def update(id_):
	example = Example.query.filter_by(id=int(id_)).first()
	example.status=True
	db.session.commit()
	return redirect(url_for('index')) 

@app.route('/delete/<id_>')
def delete(id_):
	example = Example.query.filter_by(id=int(id_)).first() 		
	db.session.delete(example)
	db.session.commit()
	return redirect(url_for('index'))

@app.route('/add',methods=["POST"])
def add():
	example = Example(request.form['task_name'], status=False)
	db.session.add(example)
	db.session.commit()
	return redirect(url_for('index'))

if __name__=="__main__":
    app.run(debug=True)
