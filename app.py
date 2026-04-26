from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.security import generate_password_hash, check_password_hash
from db_config import get_db_connection

app = Flask(__name__)
app.secret_key = 'smart_photo_studio_secret_key'  # Needed for session and flash messages

# ==========================================
# AUTHENTICATION ROUTES
# ==========================================

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        conn = get_db_connection()
        if not conn:
            flash("Database connection error. Ensure MySQL is running.", "danger")
            return render_template('login.html')

        with conn.cursor() as cursor:
            cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
            user = cursor.fetchone()
            
            # Simple check for simple student projects:
            if user and check_password_hash(user['password_hash'], password):
                session['loggedin'] = True
                session['user_id'] = user['user_id']
                session['username'] = user['username']
                session['role'] = user['role']
                return redirect(url_for('dashboard'))
            else:
                flash("Invalid Username or Password!", "danger")
        conn.close()
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash("You have been logged out.", "success")
    return redirect(url_for('login'))

# ==========================================
# DASHBOARD ROUTE
# ==========================================

@app.route('/dashboard')
def dashboard():
    if 'loggedin' not in session:
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT COUNT(*) as total FROM customers")
        customers_cnt = cursor.fetchone()['total']
        
        cursor.execute("SELECT COUNT(*) as total FROM bookings")
        bookings_cnt = cursor.fetchone()['total']
        
        cursor.execute("SELECT SUM(amount) as total FROM payments")
        res = cursor.fetchone()
        revenue = res['total'] if res['total'] else 0
        
    conn.close()
    return render_template('dashboard.html', 
                           customers_cnt=customers_cnt, 
                           bookings_cnt=bookings_cnt, 
                           revenue=revenue)

# ==========================================
# CUSTOMERS ROUTES
# ==========================================

@app.route('/customers')
def customers():
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("SELECT * FROM customers ORDER BY created_at DESC")
        customers_data = cursor.fetchall()
    conn.close()
    return render_template('customers.html', customers=customers_data)

@app.route('/add_customer', methods=['POST'])
def add_customer():
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        fname = request.form['first_name']
        lname = request.form['last_name']
        email = request.form['email']
        phone = request.form['phone']
        address = request.form['address']
        
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO customers (first_name, last_name, email, phone, address)
                              VALUES (%s, %s, %s, %s, %s)''', (fname, lname, email, phone, address))
            conn.commit()
        conn.close()
        flash("Customer Added Successfully", "success")
        return redirect(url_for('customers'))

@app.route('/delete_customer/<int:id>', methods=['GET', 'POST'])
def delete_customer(id):
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM customers WHERE customer_id = %s", (id,))
        conn.commit()
    conn.close()
    flash("Customer Deleted Successfully", "success")
    return redirect(url_for('customers'))

# ==========================================
# BOOKINGS ROUTES
# ==========================================

@app.route('/bookings')
def bookings():
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute('''
            SELECT b.booking_id, c.first_name, c.last_name, s.service_name, b.shoot_date, b.status, b.total_amount 
            FROM bookings b
            JOIN customers c ON b.customer_id = c.customer_id
            JOIN services s ON b.service_id = s.service_id
            ORDER BY b.booking_date DESC
        ''')
        bookings_data = cursor.fetchall()
        
        cursor.execute("SELECT * FROM customers")
        customers_data = cursor.fetchall()
        
        cursor.execute("SELECT * FROM services")
        services_data = cursor.fetchall()
    conn.close()
    
    return render_template('bookings.html', 
                           bookings=bookings_data, 
                           customers=customers_data, 
                           services=services_data)

@app.route('/add_booking', methods=['POST'])
def add_booking():
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    if request.method == 'POST':
        customer_id = request.form['customer_id']
        service_id = request.form['service_id']
        shoot_date = request.form['shoot_date']
        total_amount = request.form['total_amount']
        
        conn = get_db_connection()
        with conn.cursor() as cursor:
            cursor.execute('''INSERT INTO bookings (customer_id, service_id, shoot_date, status, total_amount)
                              VALUES (%s, %s, %s, 'Pending', %s)''', 
                           (customer_id, service_id, shoot_date, total_amount))
            conn.commit()
        conn.close()
        flash("Booking Added Successfully", "success")
        return redirect(url_for('bookings'))

@app.route('/delete_booking/<int:id>', methods=['GET'])
def delete_booking(id):
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("DELETE FROM bookings WHERE booking_id = %s", (id,))
        conn.commit()
    conn.close()
    flash("Booking Deleted Successfully", "success")
    return redirect(url_for('bookings'))

@app.route('/update_booking_status/<int:id>', methods=['POST'])
def update_booking_status(id):
    if 'loggedin' not in session: return redirect(url_for('login'))
    
    new_status = request.form['status']
    conn = get_db_connection()
    with conn.cursor() as cursor:
        cursor.execute("UPDATE bookings SET status = %s WHERE booking_id = %s", (new_status, id))
        conn.commit()
    conn.close()
    flash("Status Updated", "success")
    return redirect(url_for('bookings'))

# ==========================================
# MAIN APPLICATION RUN
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
