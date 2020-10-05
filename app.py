from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)

# Creating a DB Model for our data to populate
class BlogPost(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    author = db.Column(db.String(20), nullable=False, default='Anonymous')
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)

    def __repr__(self):
        return 'Blog Post ' + str(self.id)

"""
To build the db: 
# Switch to Python REPL
# >> from app import db
# >> db.create_all()    

To import the db model:
# Switch to Python REPL:
# >> from app import BlogPost

To see what's in a db model:
# >> BlogPost.query.all()

To add to a db:
# >> db.session.add(BlogPost(title='Blog Post 1', content='content 1', author='author'))
# >> db.session.commit()
"""

@app.route('/')
def index():
    return render_template('index.html') 

@app.route('/posts', methods=['GET', 'POST'])
def posts():
    if request.method == 'POST':
        post_title = request.form['title']
        post_content = request.form['content']
        post_author = request.form['author']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        all_posts = BlogPost.query.order_by(BlogPost.date_posted).all()
        return render_template('posts.html', posts=all_posts)

# Delete a post with a given ID and then redirect the user back to the posts page.
@app.route('/posts/delete/<int:id>')
def delete(id):
    post = BlogPost.query.get_or_404(id)
    db.session.delete(post)
    db.session.commit()
    return redirect('/posts')

@app.route('/posts/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    post = BlogPost.query.get_or_404(id)

    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('edit.html', post=post)

# This decorator demonstrates dynamic URL routing
@app.route('/home/<string:name>')
def hello(name):
    return f"Hello {name}! Are you lost?"

# This decorator restricts the HTTP request types that are allowed on our webpage
@app.route('/onlyget', methods=['GET'])
def get_req():
    return "You can only GET this webpage. POST methods will fail. Please don't try a POST method on this page!"


@app.route('/posts/new', methods=['GET', 'POST'])
def func_name():
    if request.method == 'POST':
        post.title = request.form['title']
        post.author = request.form['author']
        post.content = request.form['content']
        new_post = BlogPost(title=post_title, content=post_content, author=post_author)
        db.session.add(new_post)
        db.session.commit()
        return redirect('/posts')
    else:
        return render_template('new_post.html')

# Boiler plate
# Don't run debug mode in prod 
if __name__ == "__main__":
    app.run(debug=True)

