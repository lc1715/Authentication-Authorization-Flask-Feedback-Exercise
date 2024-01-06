from flask import Flask, render_template, redirect, session, flash
from models import db, connect_db, User, Feedback
from forms import RegisterForm, LoginForm, FeedbackForm
from flask_debugtoolbar import DebugToolbarExtension

app = Flask(__name__)

app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///feedback"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_ECHO"] = True
app.config["SECRET_KEY"] = "abc123"
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False

app.app_context().push()  

connect_db(app)

toolbar = DebugToolbarExtension(app)


@app.route('/')
def homepage():
    return redirect('/register')

@app.route('/username/<username>/feedback/add', methods=['GET', 'POST'])
def add_feedback(username):
    # Check that the user is logged in before she can add feedback
    if 'user_username' not in session:
        flash('Please register or login first!')
        return redirect('/register')
    
    ###GET request####
    form = FeedbackForm()

    user_obj = User.query.filter_by(username=username).first()

    ###POST request###
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        new_feedback = Feedback(title=title, content=content, username=user_obj.username)
        db.session.add(new_feedback)
        db.session.commit()
        return redirect(f'/username/{username}')
    
    return render_template('add_feedback.html', user_obj=user_obj, form=form)

@app.route('/feedback/<int:feedback_id>/update', methods=['GET', 'POST'])
def edit_feedback(feedback_id):
    ##Get request###########
    form = FeedbackForm()

    feedback = Feedback.query.get_or_404(feedback_id)

    if 'user_username' not in session:
        flash('Please register or login first!')
        return redirect('/register')
        # If there is no user logged in then he needs to log in first before he can view the update form

    ##POST request#####
    if form.validate_on_submit():

        feedback.title = form.title.data
        feedback.content = form.content.data
        
        if feedback.user.username == session['user_username']:
            db.session.commit()
            return redirect(f'/username/{feedback.user.username}')
        else: 
            flash("You don't have persmission to do that!")
        # If the owner of the feedback is the same user that is logged in, 
        # then we will allow him to update the feedback.
    return render_template('edit_feedback.html', form=form, feedback=feedback )

@app.route('/feedback/<int:feedback_id>/delete', methods=['POST'])
def delete_feedback(feedback_id):
    feedback = Feedback.query.get_or_404(feedback_id)

    if feedback.user.username == session['user_username']:
        db.session.delete(feedback)
        db.session.commit()
        return redirect(f"/username/{session['user_username']}")
    
    flash("You don't have permission to do that!")
    return redirect('/login')    


@app.route('/username/<username>', methods=['GET', 'POST'])
def users_info(username):
    # Check that the user is logged in and registered before she can view her info
    if 'user_username' not in session:
        flash('Please register or login first!')
        return redirect('/register')
    
    # user_obj = User.query.filter_by(username=username)
    user_obj = User.query.filter_by(username=username).first()

    if user_obj.feedbacks:
        feedbacks = user_obj.feedbacks  #[<Feedback 1>, <Feedback 2>] - a list of feedbacks objects
        return render_template('users_info.html', user_obj=user_obj, feedbacks=feedbacks)
    return render_template('users_info.html', user_obj=user_obj)
                           
@app.route('/users/<username>/delete')
def delete_user(username):
    # user = User.query.filter_by(username=username)
    user = User.query.filter_by(username=username).first()
    # raise

    if user.username == session['user_username']:
        db.session.delete(user)
        db.session.commit()
        session.pop('user_username')
        return redirect('/register')
    else: 
        flash("You don't have permission to do that!")
    return redirect('/register')



@app.route('/register', methods=['GET', 'POST'])
def register_user():
    ####GET Request####
    form = RegisterForm()

    ###### POST Requst ####
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        hashed_user_obj = User.register(username, password)  # {username:'LizTheCat', password:'hashed pwd'}
        new_user = User(username=hashed_user_obj[username], password=hashed_user_obj[password], email=email, first_name=first_name, last_name=last_name)

        db.session.add(new_user)
        db.session.commit()

        session['user_username'] = new_user.username

        flash('Welcome! Successfully created your account!')
        return redirect(f'/username/{username}')
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_user():
    ###GET request####
    form = LoginForm()

    ####POST request####
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        user_obj = User.authenticate(username=username, password=password) #{username:'LizTheCat', password:'hashed pwd', email:'liz24@gmail.com', first_name:"Elizabeth", last_name:'Lin'.}

        # if user_obj and session['user_username'] == user_obj.username:
        if user_obj:
            session['user_username'] = user_obj.username
            flash(f'Welcome back, {user_obj.username}')
            return redirect(f'/username/{user_obj.username}')
        else:
            form.username.errors = ['Invalid username/password']

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_user():
    session.pop('user_username')
    flash('You are logged out')
    return redirect('/login')