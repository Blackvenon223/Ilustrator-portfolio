from flask import render_template, flash, redirect, url_for, request
from app import app,db
from app.models import Artist
from app.forms import LoginForm
from flask_login import login_user, logout_user, current_user, login_required
import os

@app.route('/')
@app.route('/index')
def index():
    return render_template('base.html')
    

@app.route('/info')
def show_info():
	return render_template('info.html',name=Artist.name,phone_number=Artist.phone_number,email=Artist.email,description=Artist.description)
	
	
	
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS	
	
	
@login_required
@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
	args = {"method": "GET"}
	if request.method == "POST":
		file = request.files["file"]
		if bool(file.filename):
			file_bytes = file.read(app.config['MAX_FILE_SIZE'])
			args["file_size_error"] = len(file_bytes) == app.config['MAX_FILE_SIZE']
		args["method"] = "POST"
		file.save(os.path.join(app.config['UPLOAD_FOLDER']))
	return  render_template('upload.html')
	
@app.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		artist = Artist.query.filter_by(username=form.username.data).first()
		if artist is None or not artist.check_password(form.password.data):
			flash('Invalid username or password')
			return redirect(url_for('login'))
		login_user(artist, remember=form.remember_me.data)
		next_page = request.args.get('next')
		if not next_page or url_parse(next_page).netloc != '':
			next_page = url_for('index')
		return redirect(next_page)
	return render_template('login.html', form=form)
	


