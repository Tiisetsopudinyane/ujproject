import sqlite3
from flask import Flask,jsonify
import json
import asyncio
# Connect to SQLite database (creates if not exists)




def insertUserIntodb(first_name, last_name, date_of_birth, gender, email, occupation,bio, contact_details, home_address, postal_code, password):
    query="""INSERT INTO User (first_name, last_name, date_of_birth, gender, email, occupation,bio, contact_details, home_address, postal_code, password)VALUES (?,?,?,?,?,?,?,?,?,?,?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [ first_name, last_name, date_of_birth, gender, email, occupation,bio, contact_details, home_address, postal_code, password])
        conn.commit()        
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()



def loginCredentials(email, password):
    query="""SELECT * from User WHERE email=? and password=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (email,password))
        credentials=cursor.fetchone()
        if credentials:
            return True
        else:
            return False
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def updatePassword(email,password):
    query="""UPDATE User SET password=? where email=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(password,email))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

        
def emailExists(email):
    query="""SELECT email from User WHERE email=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(email,))
        user = cursor.fetchone()
        if user:
            return True
        else:
            return False 
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def selectAllfromUser(email):
    query="""SELECT * from User WHERE email=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(email,))
        user = cursor.fetchone()
        
        if user:
            column=[column[0] for column in cursor.description]
            user_dict=dict(zip(column,user))
            user=user_dict
            return user
        else:
            return {'message':'email dont exist'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
def selectAllmessages(senderId, receiverId):
    query="""SELECT * from Messages WHERE senderId=? AND receiverId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(senderId, receiverId))
        Messages = cursor.fetchall()
        
        if Messages:
            column=[column[0] for column in cursor.description]
            messages_dict=dict(zip(column,Messages))
            messages=massages_dict
            return messages
        else:
            return {'message':'no messages found'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
        
def selectAllfromUser_with_Id(id):
    query="""SELECT * from User WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(id,))
        user = cursor.fetchone()
        
        if user:
            column=[column[0] for column in cursor.description]
            user_dict=dict(zip(column,user))
            user=user_dict
            return user
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

        
def insertBio(user_id,bio):
    query="""UPDATE User SET bio=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(bio,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        

def insertOccupation(user_id,occupation):
    query="""UPDATE User SET occupation=? where userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(occupation,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()


def insertContact(user_id,contact):
    query="""UPDATE User SET contact_details=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(contact,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def insertAddress(user_id,address):
    query="""UPDATE User SET home_address=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(address,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
        
def insertPostal(user_id,postal_code):
    query="""UPDATE User SET postal_code=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(postal_code,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
        
def insertInterests(user_id,interests):
    query="""UPDATE User SET interests=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(interests,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def insertImage(user_id,image):
    query="""UPDATE User SET images=? WHERE userId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(image,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
def insertPostimage(user_id,image):
    query="""UPDATE Post SET images=? WHERE user_Id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(image,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def insertPostvideo(user_id,video):
    query="""UPDATE Post SET video=? WHERE user_Id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(video,user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def insertPost(userId, title, description,media):
    user=selectAllfromUser_with_Id(userId)
    author=user['first_name']+' '+user['last_name']
    query = """INSERT INTO Post (user_id, author, title, description, media) VALUES (?, ?, ?, ?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (userId, author, title, description, json.dumps(media)))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()


def updateTitle(post_id,title):
    query="""UPDATE Post SET title=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(title,post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def updateDescription(post_id,description):
    query="""UPDATE Post SET description=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(description,post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def updateMedia(post_id,media):
    query="""UPDATE Post SET media=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(media,post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()

def updateOldPost(postId, userId, title, description,media):
    query = """UPDATE Post SET user_id=?, title=?, description=?, media=? WHERE postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (userId, title, description, json.dumps(media), postId))
        conn.commit()
        print("message i am here")
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
    
    
def get_post(userId):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Post WHERE user_id = ?"
    cursor.execute(query, (userId,))
    posts = cursor.fetchall()
    if posts:
            column=[column[0] for column in cursor.description]
            post_list = []
            for post in posts:
                post_dict=dict(zip(column,post))
                post_list.append(post_dict)
    
            return post_list
    conn.close()


def get_one_post(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    query = "SELECT * FROM Post WHERE postId = ?"
    cursor.execute(query, (post_id,))
    posts = cursor.fetchone()
    if posts:
            column=[column[0] for column in cursor.description]
            post_list = []
            post_dict=dict(zip(column,posts))
            post_list.append(post_dict)
    
            return post_list
    conn.close()



def deletepost(userId,post_id):
    query = """DELETE FROM Post WHERE user_id=? AND postId=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (userId, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()

def deleteshare(post_id):
    query = """DELETE FROM Shares WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()

def deletecomments(post_id):
    query = """DELETE FROM Comment WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
def deletereplies(post_id):
    query = """DELETE FROM replies WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
def deletelikes(post_id):
    query = """DELETE FROM Likes WHERE post_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id,))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        

def retrieve_media(post_id):
    post = get_post(post_id)
    if post:  
        media = post[6]  
        midea = json.loads(media)
        return media
    else:
        return None
    
    
    
def loadPosts(name):
    query="SELECT * ,COUNT(*) as total FROM Post where title=? ORDER BY post_date DESC, post_time DESC"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,[name,])
        posts = cursor.fetchall()
        
        if posts:
            columns = [column[0] for column in cursor.description]
            posts_list = []
            for post in posts:
                post_dict = dict(zip(columns, post))
                posts_list.append(post_dict)
            return posts_list
        else:
            return {'message': 'No posts found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()


def load_Posts(offset=0, limit=10):
    query="SELECT * FROM Post ORDER BY post_date DESC, post_time DESC LIMIT ? OFFSET ?"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(limit, offset))
        posts = cursor.fetchall()
        print("posts",posts)
        if posts:
            columns = [column[0] for column in cursor.description]
            posts_list = []
            for post in posts:
                post_dict = dict(zip(columns, post))
                posts_list.append(post_dict)
            return posts_list
        else:
            return {'message': 'No posts found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()




def countPosts():
    query="SELECT title,COUNT(title) as total FROM Post GROUP BY title"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,)
        posts = cursor.fetchall()
        
        columns = [column[0] for column in cursor.description]
        post_list = []
        for post in posts:
                
            post_dict = dict(zip(columns, post))
            post_list.append(post_dict)
                
        return post_list 
        
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()


def loadComments(postid):
    query = "SELECT * FROM Comment WHERE post_id=? ORDER BY post_date DESC, post_time DESC"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (postid,))
        comments = cursor.fetchall()
        
        if comments:
            
            columns = [column[0] for column in cursor.description]
            comment_list = []
            for comment in comments:
                
                comment_dict = dict(zip(columns, comment))
                comment_list.append(comment_dict)
                
            return json.dumps(comment_list)  # Return JSON data
        else:
            return json.dumps({'message': 'No comments found'})  # Return JSON data
    except sqlite3.Error as e:
        print('Error:', e)
        return json.dumps({'message': 'An error occurred while loading comments'})  # Return JSON data
    finally:
        conn.close()



def loadUsersIdViwComments(userId):
    query = "SELECT * FROM User WHERE userId=?"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (userId,))
        userIds = cursor.fetchall()
        
        if userIds:
            
            columns = [column[0] for column in cursor.description]
            userId_list = []
            for userId in userIds:
                
                userId_dict = dict(zip(columns, userId))
                UserId_list.append(UserId_dict)
                
            return json.dumps(UserId_list)  # Return JSON data
        else:
            return json.dumps({'message': 'No User Id found'})  # Return JSON data
    except sqlite3.Error as e:
        print('Error:', e)
        return json.dumps({'message': 'An error occurred while loading user'})  # Return JSON data
    finally:
        conn.close()
        
 


def loadCommentsandUser(postid):
    query = """
    SELECT 
        u.first_name, 
        u.last_name, 
        c.post_id,
        c.text,
        c.post_date,
        c.post_time
    FROM Comment c
    INNER JOIN User u ON c.user_id = u.userId
    WHERE c.post_id=?
    """
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    try:
        cursor.execute(query, (postid,))
        comments = cursor.fetchall()
        if comments:
            # Get column names
            column_names = [description[0] for description in cursor.description]
            
            comment_list = []
            for comment in comments:
                # Create a dictionary with column names as keys
                comment_dict = {column_names[i]: comment[i] for i in range(len(column_names))}
                comment_list.append(comment_dict)
                
            return json.dumps(comment_list)  # Return JSON data
        else:
            return json.dumps({'message': 'No comments found'})  # Return JSON data
    except sqlite3.Error as e:
        print('Error:', e)
        return json.dumps({'message': 'An error occurred while loading comments'})  # Return JSON data
    finally:
        conn.close()
        

        

def activeusers():
    query = "SELECT COUNT(active) AS countActive FROM User_session WHERE active=TRUE"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        countActive = cursor.fetchone()[0]  # Fetch one row and extract the count
        return {'message': 'Success', 'countActive': countActive}
    except sqlite3.OperationalError as e:
        return {'message': 'Database error: {}'.format(e)}
    except sqlite3.Error as e:
        return {'message': 'An error occurred: {}'.format(e)}
    finally:
        conn.close()


def count_likes():
    query = "SELECT SUM(likes) AS totalLikes FROM Posts"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        total_likes = cursor.fetchone()[0]  # Fetch one row and extract the total likes
        return total_likes
    except sqlite3.Error as e:
        print('An error occurred:', e)
        return None
    finally:
        conn.close()
        
def count_comments():
    query = "SELECT COUNT(*) AS totalComments FROM Comments"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query)
        total_comments = cursor.fetchone()[0]  # Fetch one row and extract the total comments
        return total_comments
    except sqlite3.Error as e:
        print('An error occurred:', e)
        return None
    finally:
        conn.close()


def user_has_liked_post(user_id, post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM likes WHERE user_id = ? AND post_id = ?", (user_id, post_id))
    like_count = cursor.fetchone()[0] 
    
    conn.close()
    
    # If like_count is greater than 0, it means the user has liked the post
    return like_count > 0

def decrease_like_count(post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Post SET likes = likes - 1 WHERE postId = ?", (post_id,))
    
    conn.commit()
    
    conn.close()


def update_likes_delete(userId,post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Likes  WHERE user_id = ? AND post_id=?", (userId,post_id))
    
    conn.commit()
    
    conn.close()

def likes_update_table_row(userId,post_id):
    query = """INSERT INTO Likes (post_id, user_id) VALUES (?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id, userId))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
    
    
def increase_like_count(post_id):
    # Connect to the SQLite database
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE Post SET likes = likes + 1 WHERE postId = ?", (post_id,))
    
    conn.commit()
    
    conn.close()
 

def insert_comment(post_id, user_id, comment):
    query = """INSERT INTO Comment (post_id, user_id, text) VALUES (?, ?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id, user_id, comment))
        conn.commit()
        increase_comment_count(post_id)
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
 
def increase_comment_count(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        # Fetch the current comment count for the post
        cursor.execute("SELECT comments FROM Post WHERE postId=?", (post_id,))
        current_count = cursor.fetchone()[0]

        # Increment the comment count by one
        new_count = current_count + 1

        # Update the comment count in the Post table
        cursor.execute("UPDATE Post SET comments=? WHERE postId=?", (new_count, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
        
        
        
def insert_share(post_id, user_id):
    query = """INSERT INTO Shares (post_id, user_id) VALUES (?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (post_id, user_id))
        conn.commit()
        increment_share_count(post_id)
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()

def share_count(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        # Fetch the current comment count for the post
        cursor.execute("SELECT count(share) FROM Post WHERE postId=?", (post_id,))
        current_count = cursor.fetchone()
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
    
    
def delete_profile_picture(userId):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE User SET images = NULL WHERE userId = ?", (userId,))    
    conn.commit()
    conn.close()
    
 
def increment_share_count(post_id):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        # Fetch the current comment count for the post
        cursor.execute("SELECT shares FROM Post WHERE postId=?", (post_id,))
        current_count = cursor.fetchone()[0]

        # Increment the comment count by one
        new_count = current_count + 1

        # Update the comment count in the Post table
        cursor.execute("UPDATE Post SET shares=? WHERE postId=?", (new_count, post_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
 
 
    
def update_comment(comment_id, comment, user_id):
    query = """UPDATE Comment SET text=? WHERE comment_id=? AND user_id=?"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, (comment, comment_id, user_id))
        conn.commit()
    except sqlite3.Error as e:
        print('Error: ', e)
    finally:
        conn.close()
    

def sharing(postid):
    query="SELECT author,title,description,media FROM Post WHERE postid=? ORDER BY post_date DESC, post_time DESC"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(postid,))
        posts = cursor.fetchall()
        
        if posts:
            columns = [column[0] for column in cursor.description]
            posts_list = []
            for post in posts:
                post_dict = dict(zip(columns, post))
                posts_list.append(post_dict)
            return posts_list
        else:
            return {'message': 'No posts found'}
    except sqlite3.Error as e:
        print('Error:', e)
        return {'message': 'An error occurred while loading posts'}
    finally:
        conn.close()

def insertreplyMessages(sender_id, user_id, reply, replyTo):
    query="""INSERT INTO Reply (senderId, receiverId, reply,replyTo) VALUES (?, ?, ?,?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [ senderId, receiverId, reply,replyTo])
        conn.commit()        
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()



def insertMessages(senderId, receiverId, message):
    query="""INSERT INTO Messages (senderId, receiverId, message) VALUES (?, ?, ?)"""
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [ senderId, receiverId, message])
        conn.commit()        
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()


def messagesFromSender(senderId, receiverId):
    query="SELECT User.first_name, User.last_name, Messages.message, Messages.timestamp FROM Messages INNER JOIN User ON Messages.senderId = User.userId WHERE senderId=? and receiverId=?"
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query,(senderId, receiverId))
        Messages = cursor.fetchall()
        
        if messages:
            columns = [column[0] for column in cursor.description]
            messages_list = []
            for message in messages:
                message_dict = dict(zip(columns, message))
                messages_list.append(message_dict)
            return messages_list
        else:
            return {'message':'no messages found'}
    except sqlite3.Error as e:
        print('Error: ',e)
    finally:
        conn.close()
        
        
def selectAllmessages(userId):
    query = """
    SELECT DISTINCT 
        M1.messageId AS message_id,
        Sender.userId AS sender_id, 
        Sender.first_name AS sender_first_name, 
        Sender.last_name AS sender_last_name, 
        Receiver.userId AS receiver_id,
        Receiver.first_name AS receiver_first_name, 
        Receiver.last_name AS receiver_last_name, 
        M1.message, 
        M1.timestamp AS message_timestamp,
        M2.message AS reply_message, 
        M2.timestamp AS reply_timestamp
    FROM 
        Messages AS M1
    INNER JOIN 
        User AS Sender ON M1.senderId = Sender.userId 
    INNER JOIN 
        User AS Receiver ON M1.receiverId = Receiver.userId 
    LEFT JOIN 
        Messages AS M2 ON M1.messageId = M2.replyTo
    WHERE 
        Receiver.userId = ? 
    ORDER BY 
        M1.timestamp DESC;
    """
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    try:
        cursor.execute(query, [userId])
        rows = cursor.fetchall()
        if rows:
            columns = [column[0] for column in cursor.description]
            messages_list = []
            for row in rows:
                row_dict = dict(zip(columns, row))
                messages_list.append(row_dict)
                print(messages_list)
            return messages_list
        else:
            return {'message': 'No messages found.'}
    except sqlite3.Error as e:
        print('Error:', e)
    finally:
        conn.close()


def update_campaign(subject, overview, funding_goal, duration, description):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('''
        INSERT INTO Campaigns (subject, overview, funding_goal, duration, description)
        VALUES (?, ?, ?, ?, ?)
    ''', (subject, overview, funding_goal, duration, description))
    conn.commit()
    conn.close()
    
    
def select_all_campaigns():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM Campaigns')
    campaigns = cursor.fetchall()
    conn.close()
    return campaigns



def get_column_names():
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()
    cursor.execute("PRAGMA table_info(Post)")
    columns = cursor.fetchall()
    conn.close()
    # Extract column names from the result of PRAGMA table_info
    return [column[1] for column in columns]


def get_suggestions(query):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    columns = get_column_names()
    columns = [column for column in columns if column != 'media']
    # Create the SQL query dynamically
    sql_query = " UNION ".join([f"SELECT {column}, '{column}' as column_name FROM Post WHERE {column} LIKE ?" for column in columns])
    parameters = ['%' + query + '%'] * len(columns)
    
    cursor.execute(sql_query, parameters)
    results = cursor.fetchall()
    conn.close()

    # Remove duplicates and extract results
    unique_results = {(result[0], result[1]) for result in results}
    return list(unique_results)


def get_full_post_content(search,offset=0, limit=10):
    conn = sqlite3.connect('blog.db')
    cursor = conn.cursor()

    sql_query = f"SELECT * FROM Post WHERE title = ? ORDER BY post_date DESC, post_time DESC LIMIT ? OFFSET ?"
    cursor.execute(sql_query,(search,limit, offset))
    post_content = cursor.fetchall()
    if post_content:
            columns = [column[0] for column in cursor.description]
            post_list = []
            for row in post_content:
                row_dict = dict(zip(columns, row))
                post_list.append(row_dict)
                print(post_list)
            return post_list
    conn.close()
    print(post_content)
    return post_content



