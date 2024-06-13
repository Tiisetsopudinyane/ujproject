from flask import Flask,redirect,url_for,render_template,request,jsonify,session,flash
from user_validation import matchPassword,encryptdata
from user import (updatePassword,sharing,likes_update_table_row,increase_like_count,update_likes_delete,decrease_like_count,user_has_liked_post,loadCommentsandUser
                  ,loadComments,insert_comment,updateMedia,updateDescription,updateTitle,get_one_post,deletelikes,deletereplies,deletecomments,deleteshare
                  ,deletepost,get_post,retrieve_media,activeusers,loadPosts,insertUserIntodb,loginCredentials,selectAllfromUser_with_Id,emailExists
                  ,selectAllfromUser,insertBio,insertOccupation,insertContact,insertAddress,insertPostal,insertInterests,insertImage,insertPost,user_has_liked_post
                  ,decrease_like_count,increase_like_count,selectAllmessages,insertMessages,selectAllmessages,countPosts,loadPosts)
import base64
import io
from PIL import Image
import cv2
import os
from dotenv import load_dotenv
import datetime
import json
from flask_mail import Mail, Message
from flask_wtf.csrf import CSRFProtect
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, validators
from configparser import ConfigParser
import hashlib
import time
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import smtplib




app=Flask(__name__)

app.secret_key="session"

csrf = CSRFProtect(app)
load_dotenv()
# Load email configuration from config.cfg
config = ConfigParser()
config.read('config.cfg')

# Configure Flask-Mail
app.config['MAIL_SERVER'] = config['EMAIL']['MAIL_SERVER']
app.config['MAIL_PORT'] = config['EMAIL']['MAIL_PORT']
app.config['MAIL_USE_TLS'] = config.getboolean('EMAIL', 'MAIL_USE_TLS')
app.config['MAIL_USE_SSL'] = config.getboolean('EMAIL', 'MAIL_USE_SSL')

app.config['MAIL_USERNAME'] = os.environ.get('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.environ.get('MAIL_PASSWORD') 
mail = Mail(app)

comment_list=[]
comments={}
import socket
socket.getaddrinfo('127.0.0.1', 8000)
port = int(os.environ.get('FLASK_RUN_PORT', 8000))

@app.route("/",methods=["POST","GET"])

def homePage():
    
    return render_template("login.html")    
    

@app.route("/post")
def post():
    if 'user_id' not in session:
        return render_template("login.html")
    
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    profileimage = userdata['images']
    return render_template("post.html",user=userdata,profileimage=profileimage)

@app.route("/count")
def countPosts():
    cat_list=[]
    agric_count=countPosts("agriculture")
    health_count=countPosts("healthcare")
    teach_count=countPosts("technology")
    enrgy_count=countPosts("energy")
    edu_count=countPosts("education")
    manu_count=countPosts("manufacturing")
    finance_count=countPosts("finance")
    trans_count=countPosts("transport")
    envir_count=countPosts("environment")
    retail_count=countPosts("retail")
    
@app.route("/loadposts/<string:name>",methods=["GET"])
def loadposts(name):
    posts=loadPosts(name)
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    profileimage = userdata['images']
    media=[]
    if "message" not in posts:
        for item in posts:
            
            if "media" in item:
                images=item['media'][1:-1].split(', ')
                images=[s.strip('"') for s in images]
                media.append(images)
                for picture_list in media:
                    item['media']=picture_list
                    
        return render_template("postcontent.html",post=posts,user=userdata,profileimage=profileimage)
    else:
        print("message")
        return redirect(url_for("post"))


@app.route("/loadmessages")
def loadmessages():
    userId=session["user_id"]
    sender=selectAllmessages(userId)
    return render_template("inbox.html",sender=sender)
    



@app.route("/selectedUserProfile/<int:user_id>", methods=["POST","GET"])
def selectedUserProfile(user_id):
    user=selectAllfromUser_with_Id(user_id)
    userId=session["user_id"]
    senderdata=selectAllfromUser_with_Id(userId)
    
    senderId=senderdata['userId']
    if request.method=="POST":
        message=request.form.get('message')
        insertMessages(senderId, user_id, message)
        return redirect(url_for("post"))
    
    return render_template("selectedUserProfile.html",user=user)
   

@app.route("/login",methods=["POST","GET"])
def login():
    if request.method=="POST":
        email=request.form["email"]
        session["email"]=email
        password=request.form["password"]
        
        password=encryptdata(password.strip())
        
        user_credentials= loginCredentials(email,password)
        
        user=selectAllfromUser(email)
        media=[]
        if user_credentials:
            session["user_id"]=user['userId']
            return render_template("post.html",user=user,media=media)
             
    return render_template("login.html")





@app.route("/logout")
def logout():
        session.clear()
        return render_template("login.html")


@app.route("/autologout")
def autologout():
    session.clear()
    return render_template("index.html")


#route to the create account page

@app.route("/createAccount",methods=["POST",'GET'])

def createAccount():
        if request.method=='POST':
            firstName = request.form.get('firstName')

            lastName = request.form.get('lastName')

            dob = request.form.get('dob')

            gender = request.form.get('gender')

            email = request.form.get('email')

            occupation = request.form.get('occupation')

            bio=request.form.get('bio')

            contact = request.form.get('contact')

            address = request.form.get('address')

            postalCode = request.form.get('postalCode')

            password = request.form.get('password')

            confirmPassword = request.form.get('confirmPassword')
            finalPassword = matchPassword(password.strip(), confirmPassword.strip())
            
            #check if password dont match
            if not finalPassword:
                flash('Passwords do not match')
                return redirect(url_for('createAccount'))
            #check if user already has an account or not
            emailExistance=emailExists(email)
            if emailExistance:
                flash('Email already exists',"error")
                return redirect(url_for('createAccount'))
                
            password=encryptdata(password.strip())
            insertUserIntodb( firstName, lastName, dob, gender, email, occupation,bio, contact, address, postalCode, password)

            user=selectAllfromUser(email)
            if 'userId' in user:
                session["user_id"]=user['userId']
                return render_template("post.html",user=user)
        else:
            return render_template("createAccount.html")




@app.route('/createNewPost', methods=["POST", "GET"])
def createNewPost():
    if 'user_id' not in session:
        flash('User not logged in.')
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    if request.method == "POST":
        userId = session['user_id']
        title = request.form.get('title')
        description = request.form.get('description')
        media = request.files.getlist('media[]')
        file_list= create_upload_folder(media)
        insertPost(userId, title, description, file_list)
        return redirect(url_for('post'))  # Redirect to the post page after creating the post
    
    return render_template('add_post.html')


@app.route('/userprofileEdit',methods=["POST","GET"])

def userProfile():
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    user=selectUserInfo()
    userPosts=get_post(userId)
    if request.method=='POST':
        return render_template('post.html',user=user)
    else:
        media=[]
        
        if userPosts is not None:
            for item in userPosts:
            
                images=item['media'][1:-1].split(', ')
                images=[s.strip('"') for s in images]
                media.append(images)
                for picture_list in media:
                    item['media']=picture_list
    return render_template('userProfile.html',userPosts=userPosts,userdata=userdata,user=user)

@app.route('/updatePost/<int:postid>',methods=["POST","GET"])

def updatePost(postid):
    Post=get_one_post(postid)
    if request.method=='POST':
        media=[]
        for item in Post:
            images=item['media'][1:-1].split(', ')
            images=[s.strip('"') for s in images]
            media.append(images)
            for picture_list in media:
                item['media']=picture_list
        return render_template('editPost.html',Post=Post)


@app.route('/editOldPost/<int:postid>', methods=["POST", "GET"])
def editOldPost(postid):
    if 'user_id' not in session:
        flash('User not logged in.')
        return redirect(url_for('login'))  # Redirect to login page if user is not logged in

    if request.method == "POST":
        userId = session['user_id']
        title = request.form.get('title')
        description = request.form.get('description')
        media = request.files.getlist('media[]')
        
        file= create_upload_folder(media)
        if title:
            updateTitle(postid,title)
        if description:
            updateDescription(postid,description)
        if file:
            updateMedia(postid,file)

        flash('Post updated successfully.')
        return redirect(url_for('post'))  # Redirect to the post page after creating the post
    
    return render_template('add_post.html')


@app.route('/deletePost/<int:postid>',methods=["POST","GET"])

def deletePost(postid):
    userId=session["user_id"]
    userPosts=get_post(userId)
    if request.method=='POST':
        deletepost(userId,postid)
        deleteshare(postid)
        deletecomments(postid)
        deletereplies(postid)
        deletelikes(postid)
        return redirect(url_for('post'))
    return render_template('add_post.html',userPosts=userPosts,data=data,userdata=userdata,user=user)


@app.route('/comments_list/<int:postid>',methods=["GET"])
def comments_list(postid):
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    profileimage = userdata['images']
    if 'user_id' not in session:
        redirect('login')
    user=selectAllfromUser_with_Id(userId)
    postid=int(postid)
    
    # post=loadPosts()
    # media=[]
    # for item in post:
    #     images=item['media'][1:-1].split(', ')
    #     images=[s.strip('"') for s in images]
    #     media.append(images)
    #     for picture_list in media:
    #         item['media']=picture_list
    comment_list =loadCommentsandUser(postid)
    return jsonify(comment_list)


@app.route('/share/<int:postid>', methods=["GET"])
def share(postid):
    if 'user_id' not in session:
        
        return render_template("index.html")
    post_content=sharing(postid)
    userId=session["user_id"]
    userdata=selectAllfromUser_with_Id(userId)
    profileimage = userdata['images']

    return jsonify(post_content)
    




@app.route('/comments/<int:postid>', methods=["POST", "GET"])
def comments(postid):
    if "user_id" in session:
        userId = session["user_id"]
        if request.method == "POST":
            comment=request.form.get('comment')
            insert_comment(postid,userId,comment)
        comment_list = loadCommentsandUser(postid)
    post=loadPosts()
    userdata = selectAllfromUser_with_Id(userId)

    return redirect(url_for('post'))



  
  

@app.route('/like/<int:postid>/<string:name>', methods=["GET","POST"])
def like(postid,name):
    # posts=loadPosts(name)
    userId=session["user_id"]
    # userdata=selectAllfromUser_with_Id(userId)
    # profileimage = userdata['images']
    # media=[]
    

    if request.method=="POST":
        post_id=postid
        results=user_has_liked_post(userId, post_id)
        count=0
        if results:
            decrease_like_count(post_id)
            update_likes_delete(userId,post_id)
            count=count-count
        else:
            increase_like_count(post_id)
            likes_update_table_row(userId,post_id)
            count=count+count
    # return count, to check if is one,button must be blue,
    # if count is zero the button color must be white
    return redirect(url_for('loadposts',name=name))

    
@app.route('/updateUserInfo',methods=['POST'])

def updateUser():

    user_id=session['user_id']
    bio=request.form.get('bio')
    contact=request.form.get('contact')
    address=request.form.get('address')
    postal_code=request.form.get('postalCode')
    occupation=request.form.get('occupation')
    
    image=request.files['file']
    
    if bio:
        insertBio(user_id,bio)
        
    if contact:
        insertContact(user_id,contact)
    
    if occupation:
        insertOccupation(user_id,occupation)
    
    if address:
        insertAddress(user_id,address) 
        
    if postal_code:
        insertPostal(user_id,postal_code)
        
    if image.filename:
        image_=profile_image(image)
        insertImage(user_id,image_)
        post=loadPosts()
    return redirect(url_for('post'))
        
@app.route('/createPost')
def createPostPage():
    return render_template('add_post.html')

@app.route('/userinfo')
def selectUserInfo():

    if "email" in session:
        userEmail=session["email"]
        user=selectAllfromUser(userEmail)
        return user


def create_upload_folder(files):
    config={'base_dir':'static\\'}
    # Get base directory from config
    base_dir = config['base_dir']
   
    # Construct path for the uploads folder
    uploads_dir = os.path.join(base_dir, 'uploads')

    # Create the uploads folder if it doesn't exist
    if not os.path.exists(uploads_dir):
        os.makedirs(uploads_dir)
    # Construct path for the file within the uploads folder
    file_paths=[]
    for file_obj  in files:
        file_path = os.path.join(uploads_dir, file_obj.filename)
        file_obj.save(file_path)
        file_paths.append(file_path)
        
    return file_paths


def media_file(files):
    # Create the 'uploads' directory if it doesn't exist
    os.makedirs('static/uploads', exist_ok=True)
    file_paths = []
    for file in files:
        # Save each file to the 'uploads' directory
        file_path = os.path.join('static/uploads', file.filename)
        file.save(file_path)
        file_paths.append(file_path)
        
        # Check if the file was saved successfully
        if not os.path.exists(file_path):
            print(f"Error: File '{file.filename}' not found.")
            return None
    
    return file_paths
    

def profile_image(files):
    # Create the 'uploads' directory if it doesn't exist
    os.makedirs('static/uploads', exist_ok=True)
    
        # Save each file to the 'uploads' directory
    file_path = os.path.join('static/images', files.filename)
    files.save(file_path)
        
        # Check if the file was saved successfully
    if not os.path.exists(file_path):
        print(f"Error: File '{files.filename}' not found.")
        return None
    
    return file_path


class EmailForm(FlaskForm):
    email = StringField('Email', validators=[validators.DataRequired(), validators.Email()])
    submit = SubmitField('Send Reset Email')

# Flask-WTF form for password reset
class ResetPasswordForm(FlaskForm):
    password = PasswordField('New Password', validators=[validators.DataRequired(), validators.Length(min=8)])
    confirm_password = PasswordField('Confirm New Password', validators=[validators.DataRequired(), validators.EqualTo('password')])
    submit = SubmitField('Reset Password')

# Route to send reset email
@app.route('/reset_password_page', methods=['GET', 'POST'])
def reset_password_page():
        if request.method=="POST":
            email = request.form['email']
            user=selectAllfromUser(email)
            send_reset_email(user['email'])
            return render_template('login.html')

        return render_template('email.html')


# Function to send reset email
@app.route("/send_reset_email/<string:email>", methods=["POST",'GET'])
def send_reset_email(email):
    token = generate_token(email) 
    session['email']=email
    sender = app.config['MAIL_USERNAME']  # Replace with verified sender address if needed
    recipient = email
    try:
        message = Message(subject='Reset Your Password', sender=sender, recipients=[recipient])
        message.html ="""
    <div class="container">
        <h1>Password Reset</h1>
        <p>Hello,</p>
        <p>You requested a password reset. Click the button below to reset your password:</p>
        <a href=`http://127.0.0.1:8000/reset_password`>Reset Password</a>
        <p>If you did not request a password reset, please ignore this email.</p>
        <p>Thank you,</p>
        <p>The Team</p>
    </div>"""
        mail.send(message)
        return f"Reset email sent successfully to {email}"
    except Exception as e:
        print(f"Error sending email: {e}")
        return "Error sending reset email"    
    
# Dummy function to generate token
def generate_token(email):
    # Concatenate email and current timestamp
    data = email + str(time.time())
    
    # Hash the concatenated data using SHA256
    hashed_data = hashlib.sha256(data.encode()).hexdigest()
    
    # Return the hashed token
    return hashed_data

@app.route("/reset_password", methods=["POST","GET"])
def reset_password():
    if request.method=="POST":
        password = request.form.get('password')
        confirmPassword = request.form.get('confirmPassword')
        email=session["email"]
        finalPassword = matchPassword(password.strip(), confirmPassword.strip())
            
        #check if password dont match
        if not finalPassword:
            return flash('Passwords do not match')
        password=encryptdata(password.strip())
        updatePassword(email,password)
        return redirect(url_for('post'))
    return render_template('reset_password.html')





if __name__ =="__main__":

    app.run(debug=True, port=port)