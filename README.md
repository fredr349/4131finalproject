# 4131finalproject
1. Project Type: Plan A
2. Group Members Name: Nathen Slater and Thomas Fredrickson
3. Link to live Application:
4. Link to Github Code Repository: https://github.com/fredr349/4131finalproject
5. List of Technologies/API's Used: Ipstack-api, bootstrap, flask, flask_sqlalchemy, WTForms
6. Detailed Description of the project:
You must provide a README that describes to the TAs how they should access and use your application.  This will aid them in grading.

This code is partially an extension of Corey Schafer's Flask tutorial on YouTube. His tutorial covered the basics of building a site, and was helpful in learning how the login stuff worked. We extended the tutorial quite a bit. We added the feature of saving a post as a draft, and then being able to post from the drafts section. We also implemented the ability to "Like" and "Unlike" a post, which required creating a table that incorporates a many-to-many relationship.

When starting the program create a user login by pressing the “register” button. You cannot duplicated a current user’s username or email, if you do you will get an error.  After successful registration you will be redirected to a login page.  On this login page you may check the “remember me” button to always stay login. Once logged in you may create,view, like any posts. While creating a post you may save it as a draft, to post at a later time. Any posts that you created, you may delete or update.  Every post has a timestamp saved to the database, a location, created by the api Ipstack, and your unique username along with a title and content you created. At any given time you may update your profile picture along with you username and email.  Yet the same criteria follow no duplication of username or email. The profile picture is defaulted to doge dog, but can be changed and will be sized down to save space once saved. Only a png and jpg files can be used to create a new profile picture.  



7. List of Controllers and their short description: (No more than 50 words for each controller)

@app.route('/') & @app.route("/home")
Goes to main page

@app.route("/drafts")
This route looks at drafts

@app.route("/drafts", methods=['GET','POST'])
This route handled draft updates or posts

@app.route('/about')
Goes to about page

@app.route('/register', methods=['GET','POST'])
Handles registration

@app.route("/login", methods=['GET', 'POST'])
Logs in

@app.route("/logout")
Logs out

@app.route("/account",  methods=['GET', 'POST'])
Views the account settings and profile picture change option

@app.route("/post/new", methods=['GET', 'POST'])
Create a new post

@app.route("/post/<int:post_id>", methods=['GET', 'POST'])
View this post

@app.route("/drafts/<int:draft_id>", methods=['GET', 'POST'])
View this draft, only by whom created the draft

@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
Update any given post, only by whom created the post

@app.route("/draft/<int:draft_id>/update_draft", methods=['GET', 'POST'])
Update any given draft, only by whom created the draft and lets you post it

@app.route("/post/<int:post_id>/delete", methods=['POST'])
Delete any given post, only by whom created the post

@app.route("/draft/<int:draft_id>/delete_draft", methods=['POST'])
Delete a draft, only by whom created the draft

@app.route("/draft/<int:draft_id>/post_draft", methods=['POST','GET'])
Handles conversion of draft to post

@app.route("/like_post_home/<int:post_id>", methods=['POST','GET'])
Handles liking posts on home page

@app.route("/like_post_view/<int:post_id>", methods=['POST','GET'])
Handles liking posts on individual post page



8. List of Views and their short description: (No more than 50 words for each view)
About.html
This is a simple about page.

Account.html
This views your account and offers options to change profile picture

Create_post.html
Create your posts here, or save to drafts.

Draft.html
View of a single draft

Drafts.html
View the collection of all your drafts

Home.html
Home page with all posts

Layout.html
Contains universal top bar and sidebars

Login.html
Login into account here

Post.html
View individual posts

Register.html
Register an account on this page. Has form validation

Update_draft.html
This is the page for updating a draft


9. List of Tables, their Structure and short description:
class User(db.Model, UserMixin):
The user database is the main database. It consists of a unique username, unique email, image_file, password (hashed),  foregin key of posts, and a foregin key of drafts. The user database has the use of “UserMixin” which helps with @app.login requests.

class Post(db.Model):
The post database has a one to many relationship to the user database.  The post database consists of titles, date posted, the content, city posted in, state posted in, the foreign key for number of likes, and the unique user id that links it to the user database.

class Draft(db.Model):
The draft database has a one to many relationship to the user database. It follows suit to the post database but only having a title, content, and the unique user id that links it to the user database.

class PostLikes(db.Model):
The postlikes database has a many to many relationship to the post database. It contains a unique user id that links it to the user and another foreign key that links it to the post database.  Postlikes has an integer counter that keeps the number of likes and by whom to each post.


10. References/Resources: List all the references, resources or the online templates that were used for the project.
https://blog.miguelgrinberg.com/post/the-flask-mega-tutorial-part-i-hello-world

https://ipstack.com/documentation

https://www.youtube.com/watch?v=Z1RJmh_OqeA

https://github.com/CoreyMSchafer

https://github.com/greyli/todoism

https://www.sqlalchemy.org/

https://getbootstrap.com/docs/4.0/components/modal/

https://runestone.academy/runestone/books/published/webfundamentals/index.html
