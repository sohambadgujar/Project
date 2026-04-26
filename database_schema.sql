CREATE DATABASE IF NOT EXISTS smart_photo_studio;
USE smart_photo_studio;

-- 1. Users Table
CREATE TABLE IF NOT EXISTS users (
    user_id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(50) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('admin', 'staff') DEFAULT 'staff',
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 2. Customers Table
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT AUTO_INCREMENT PRIMARY KEY,
    first_name VARCHAR(50) NOT NULL,
    last_name VARCHAR(50) NOT NULL,
    email VARCHAR(100) UNIQUE,
    phone VARCHAR(15) NOT NULL,
    address TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- 3. Services Table
CREATE TABLE IF NOT EXISTS services (
    service_id INT AUTO_INCREMENT PRIMARY KEY,
    service_name VARCHAR(100) NOT NULL,
    base_price DECIMAL(10,2) NOT NULL
);

-- 4. Bookings Table
CREATE TABLE IF NOT EXISTS bookings (
    booking_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id INT NOT NULL,
    service_id INT NOT NULL,
    booking_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    shoot_date DATE NOT NULL,
    status ENUM('Pending', 'Confirmed', 'Completed', 'Cancelled') DEFAULT 'Pending',
    total_amount DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id) ON DELETE CASCADE,
    FOREIGN KEY (service_id) REFERENCES services(service_id)
);

-- 5. Payments Table
CREATE TABLE IF NOT EXISTS payments (
    payment_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    payment_method ENUM('Cash', 'Card', 'UPI', 'Bank Transfer') NOT NULL,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- 6. Deliveries Table
CREATE TABLE IF NOT EXISTS deliveries (
    delivery_id INT AUTO_INCREMENT PRIMARY KEY,
    booking_id INT NOT NULL UNIQUE,
    status ENUM('Editing', 'Printing', 'Ready', 'Delivered') DEFAULT 'Editing',
    notes TEXT,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES bookings(booking_id) ON DELETE CASCADE
);

-- ============== DUMMY DATA ==============

-- Insert Admin User (Password is 'admin123' using pbkdf2:sha256 hash or simple text if hashing is skipped)
-- Note: We will use plain text for simplicity in the basic version, let's just insert an initial user in app.py if missing, or use a pre-hashed string.
-- 'scrypt:32768:8:1$mN...' -> for 'admin123'
-- For college students, we can do raw checking or werkzeug hash. Werkzeug hash for 'admin123':
INSERT INTO users (username, password_hash, role) VALUES 
('admin', 'scrypt:32768:8:1$S73x98a2t9A8r6f5$5e72d2427f71424bfaeeb53fa7ca5d5c5f4fa631a0eefacbc65481d45be701f2ff235626880da0dc09ae2dc3e42f62770635fca315c2a106ca9ed70afbcc778a', 'admin');

-- Insert Sample Services
INSERT INTO services (service_name, base_price) VALUES 
('Wedding Photography', 50000.00),
('Pre-Wedding Shoot', 25000.00),
('Maternity Shoot', 15000.00),
('Passport Size Photos', 150.00),
('Corporate Event Coverage', 30000.00);

-- Insert Sample Customers
INSERT INTO customers (first_name, last_name, email, phone, address) VALUES 
('John', 'Doe', 'john@example.com', '9876543210', '123 Main St, Cityville'),
('Jane', 'Smith', 'jane@example.com', '9876543211', '456 Oak Avenue, Townsville');

-- Insert Sample Bookings
INSERT INTO bookings (customer_id, service_id, shoot_date, status, total_amount) VALUES 
(1, 1, '2024-12-15', 'Confirmed', 50000.00),
(2, 3, '2024-05-20', 'Completed', 15000.00);

-- Insert Sample Payments
INSERT INTO payments (booking_id, amount, payment_method) VALUES 
(1, 10000.00, 'UPI'),
(2, 15000.00, 'Card');

-- Insert Sample Deliveries
INSERT INTO deliveries (booking_id, status, notes) VALUES 
(2, 'Ready', 'Album printing complete, customer to pick up.');
