from flask import Flask, render_template, request, redirect, url_for, session, flash
from flask_pymongo import PyMongo

app = Flask(__name)
app.secret_key = 'fe67ef52c93dec89e8d2a178a92817cc'
app.config['MONGO_URI'] = "mongodb+srv://codec:aqzGn6zKTgT4wm3R@cluster0.khegw2d.mongodb.net/?retryWrites=true&w=majority/parenting_and_family_advice"
mongo = PyMongo(app)

@app.route('/')
def landing():
    return render_template('index.html')

@app.route("/login", methods=["GET", "POST"])
def login():
    if 'user' in session:
        return redirect("/home")  

    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password"]

        user = mongo.db.user_collection.find_one({'email': email})

        if user:
            if user['password'] == password:
                session['user'] = user  
                flash('Login successful. Welcome, {}!'.format(email), 'success')
                return redirect(url_for('home'))  
            else:
                flash('Invalid email/password. Please enter the correct email/password.', 'error')
        else:
            flash('User not registered. Please register first.', 'error')

    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        phone = request.form['phone']
        parent_type = request.form['parent_type']
        message = request.form['message']

        if mongo.db.user_collection.find_one({'email': email}):
            flash('Email already exists. Please choose another.', 'error')
        else:
            user = {
                'name': name,
                'email': email,
                'password': password,
                'phone': phone,
                'parent_type': parent_type,
                'message': message
            }
            mongo.db.user_collection.insert_one(user)
            flash('Registration successful. You can now log in.', 'success')
            return redirect(url_for('login'))

    return render_template('register.html')

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect("/")

if __name__ == '__main__':
    app.run(debug=True)
