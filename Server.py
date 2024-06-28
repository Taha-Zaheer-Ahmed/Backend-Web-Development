from flask import Flask, render_template, request, redirect, url_for, session, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

mydb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="12345",
    database="library_database"
)

mycursor = mydb.cursor()

book_insertion_formula = "INSERT INTO books (isbn, title, author, publisher, year_of_publication, category, total_copies, available_copies) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
member_insertion_formula = "INSERT INTO members (member_id, first_name, last_name, date_of_birth, email, phone_number, address, password) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
staff_insertion_formula = "INSERT INTO staff (staff_id, first_name, last_name, position, email, phone_number, password) VALUES (%s, %s, %s, %s, %s, %s, %s)"

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/book_form')
def book_form():
    if 'staff_id' not in session:
        flash("Please log in first!")
        return redirect(url_for('staff_login'))
    return render_template('book_form.html')

@app.route('/member_form')
def member_form():
    return render_template('member_form.html')

@app.route('/staff_form')
def staff_form():
    return render_template('staff_form.html')

@app.route('/submit_book', methods=['POST'])
def submit_book():
    isbn = request.form['isbn']
    title = request.form['title']
    author = request.form['author']
    publisher = request.form['publisher']
    publication_year = request.form['publication_year']
    category = request.form['category']
    total_copies = request.form['total_copies']
    available_copies = request.form['available_copies']

    book_vals = (isbn, title, author, publisher, publication_year, category, total_copies, available_copies)
    mycursor.execute(book_insertion_formula, book_vals)
    mydb.commit()

    print("Book submitted successfully!")
    return "Book submitted successfully!"

@app.route('/submit_member', methods=['POST'])
def submit_member():
    member_id = request.form['member_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    date_of_birth = request.form['date_of_birth']
    email = request.form['email']
    phone_number = request.form['phone_number']
    address = request.form['address']
    password = request.form['password']

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    member_vals = (member_id, first_name, last_name, date_of_birth, email, phone_number, address, hashed_password)
    mycursor.execute(member_insertion_formula, member_vals)
    mydb.commit()

    print("Member submitted successfully!")
    return "Member submitted successfully!"

@app.route('/submit_staff', methods=['POST'])
def submit_staff():
    staff_id = request.form['staff_id']
    first_name = request.form['first_name']
    last_name = request.form['last_name']
    position = request.form['position']
    email = request.form['email']
    phone_number = request.form['phone_number']
    password = request.form['password']

    # Hash the password before storing it
    hashed_password = generate_password_hash(password)

    staff_vals = (staff_id, first_name, last_name, position, email, phone_number, hashed_password)
    mycursor.execute(staff_insertion_formula, staff_vals)
    mydb.commit()

    print("Staff submitted successfully!")
    return "Staff submitted successfully!"

@app.route('/staff_login', methods=['GET', 'POST'])
def staff_login():
    if request.method == 'POST':
        staff_id = request.form['staff_id']
        password = request.form['password']

        mycursor.execute("SELECT password FROM staff WHERE staff_id = %s", (staff_id,))
        staff = mycursor.fetchone()

        if staff and check_password_hash(staff[0], password):
            session['staff_id'] = staff_id
            return redirect(url_for('staff_dashboard'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('staff_login'))
    return render_template('staff_login.html')

@app.route('/member_login', methods=['GET', 'POST'])
def member_login():
    if request.method == 'POST':
        member_id = request.form['member_id']
        password = request.form['password']

        mycursor.execute("SELECT password FROM members WHERE member_id = %s", (member_id,))
        member = mycursor.fetchone()

        if member and check_password_hash(member[0], password):
            session['member_id'] = member_id
            return redirect(url_for('member_dashboard'))
        else:
            flash("Invalid credentials, please try again.")
            return redirect(url_for('member_login'))
    return render_template('member_login.html')

@app.route('/staff_dashboard')
def staff_dashboard():
    if 'staff_id' not in session:
        flash("Please log in first!")
        return redirect(url_for('staff_login'))
    return render_template('staff_dashboard.html')

@app.route('/member_dashboard')
def member_dashboard():
    if 'member_id' not in session:
        flash("Please log in first!")
        return redirect(url_for('member_login'))
    return render_template('member_dashboard.html')

@app.route('/return_book')
def return_book():
    if 'member_id' not in session:
        flash("Please log in first!")
        return redirect(url_for('member_login'))
    return "Return Book functionality to be implemented"

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
