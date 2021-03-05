from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///posts.db'
db = SQLAlchemy(app)
class BlogPost(db.Model):

	__tablename__ = "BlogPost"
	id = db.Column(db.Integer, primary_key=True)
	title = db.Column(db.String(100), nullable=False)
	content = db.Column(db.Text, nullable=False)
	auther = db.Column(db.String(100), nullable=False, default="N/A")
	date_created = db.Column(db.DateTime, default=datetime.now())
	
	def __repr__(self):
		# return "<Task %r>" % self.sr
		return "Blog post " + str(self.id)
	
@app.route('/')
def index():
	return render_template('index.html')

@app.route('/posts', methods=["POST", "GET"])
def posts():
	if request.method == "POST":
		post_title = request.form['title']
		post_auther = request.form['auther']
		post_content = request.form['content']
		new_post = BlogPost(title=post_title, auther=post_auther, content=post_content)
		db.session.add(new_post)
		db.session.commit()
		return redirect('/posts')
	posts = BlogPost.query.order_by(BlogPost.date_created).all()
	return render_template('posts.html', posts=posts)
	
@app.route('/post/delete/<int:post_id>')
def post_delete(post_id):
	# delete_post = db.session.query.filter_by(id=post_id).all()
	delete_post = BlogPost.query.get(post_id)
	db.session.delete(delete_post)
	db.session.commit()
	return redirect('/posts')
	
@app.route('/post/update/<int:post_id>', methods=['GET', 'POST'])
def post_update(post_id):
	update_post = BlogPost.query.get(post_id)
	if request.method == 'POST':
		update_post.title = request.form['title']
		update_post.auther = request.form['auther']
		update_post.content = request.form['content']
		db.session.commit()
		return redirect('/posts')
	return render_template('update_posts.html', update_post=update_post)
	
   	
@app.route('/<string:shail>')
def student(shail):
	return "shail"
	# return f"<h3><center>Hey there, The web page that you are finding <h1><i><u>{shail}</u></i></h1> is not here.</center></h3>" 


if __name__ == '__main__':
	app.run(host='0.0.0.0', port=81, debug=True)
