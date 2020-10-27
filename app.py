from flask import Flask,render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] ='sqlite:///posts.db'
db=SQLAlchemy(app)


class Blogpost(db.Model):
    id=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(100),nullable=False)
    content=db.Column(db.Text,nullable=False)
    author=db.Column(db.String(50),nullable=False,default="N/A")
    posted=db.Column(db.DateTime,nullable=False,default=datetime.now)

    def __repr__(self):
        return "Blog post" + str(self.id)

all_posts=[
    {
        'title':'post1',
        'content':'this is the content of post1', 
        "author":'Aron'       
    },
    {
        'title':'post2',
        'content':'this is the content of post2',     
    }
]


@app.route('/')
def index():
    return render_template('./index.html')

@app.route('/posts',methods=['GET','POST'])
def posts():
    if request.method=='POST':
        post_title=request.form['title']
        post_content=request.form['content']
        post_author=request.form['author']
        new_post=Blogpost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('./posts')
    else:
        all_posts=Blogpost.query.order_by(Blogpost.posted).all()
        return render_template ('./posts.html',posts=all_posts)


@app.route('/posts/delete/<int:id>')
def delete(id):
    post=Blogpost.query.get(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>',methods=['GET','POST'])
def edit(id):
    post=Blogpost.query.get(id)

    if request.method=="POST":      
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html',post=post) 

 
@app.route('/posts/new',methods=['GET','POST'])
def newpost():
    if request.method=="POST":        
        post.title=request.form['title']
        post.author=request.form['author']
        post.content=request.form['content']
        new_post=Blogpost(title=post_title,content=post_content,author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('New.html')


@app.route('/onlyget',methods=['GET'])
def get_req():
    return "get request"


if __name__ == "__main__": 
    app.run(debug=True)

