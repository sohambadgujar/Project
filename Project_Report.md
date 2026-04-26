# Full Project Report
## Smart Photo Studio Management System

**Academic Project Report on Software Development Life Cycle (SDLC) based Database Application**

---

### 1. Title
**Smart Photo Studio Management System**

### 2. Abstract
The "Smart Photo Studio Management System" is a robust, full-stack web application tailored for modern photo studios. It addresses the challenges of manual record-keeping by digitizing customer management, service bookings, financial tracking, and deliverable status updates. The platform is designed using a Relational Database Management System (RDBMS) on MySQL, wrapped in a responsive web interface driven by Python (Flask) and HTML/CSS (Bootstrap), adhering strictly to Software Development Life Cycle (SDLC) guidelines.

### 3. Introduction
Traditionally, photo studios rely on manual ledgers and chaotic spreadsheets to manage shoots, payments, and client data. The Smart Photo Studio Management System was designed to centralize this workflow. By providing tools such as an admin dashboard, dynamic customer directories, centralized booking lists, and real-time status trackers, studio administration becomes seamless, allowing photographers to focus purely on creativity. 

---

### 4. Software Requirement Specification (SRS)

**4.1 Purpose**
To create a web-based management tool capable of replacing manual operations in a photo studio environment.

**4.2 Functional Requirements**
- **Authentication**: System must secure data via Admin/Staff logins.
- **Dashboard**: System must summarize total bookings, customer base, and revenue.
- **Customer Management**: Ability to Create, Read, Update, and Delete client data (CRUD).
- **Booking Manager**: Functionality to schedule photography services mapping to explicit customers.
- **Payment & Tracking**: Trace payment methods and update completion status from "Editing" to "Delivered".

**4.3 Non-Functional Requirements**
- **Performance**: Near instantaneous retrieval of client lists.
- **Security**: Data isolation using parameterized database queries.
- **Scalability**: Designed efficiently in 3NF to avoid data duplication as studios grow.
- **Tech Stack**:
  - Frontend: HTML5, Bootstrap 5 CSS
  - Backend: Python 3, Flask
  - Database: MySQL

---

### 5. System Design

#### 5.1 Entity-Relationship (ER) Diagram (Explanation)
In our conceptual model, the following Entities exist:
1.  **Users**: Staff operating the system.
2.  **Customers**: Clients availing services.
3.  **Services**: Master catalog of studio offerings.
4.  **Bookings**: The central tie connecting Customers to Services.
5.  **Payments**: Financial tracking linked to a booking.
6.  **Deliveries**: Physical/Digital album tracking.

**Relationships**:
- A **Customer** can have *One or Many* **Bookings** (1:N).
- A **Booking** assigns exactly *One* **Service** along with *One* **Customer** (N:1 mapping to both).
- A **Booking** can have *One or Many* partial **Payments** (1:N).
- A **Booking** has exactly *One* **Delivery** ticket (1:1).

#### 5.2 Relational Model & Schema Mapping
Based on the ER rules above, the following tables were generated with Primary Keys (PK) and Foreign Keys (FK):

- `users (user_id PK, username, password_hash, role)`
- `customers (customer_id PK, first_name, last_name, email, phone, address)`
- `services (service_id PK, service_name, base_price)`
- `bookings (booking_id PK, customer_id FK, service_id FK, booking_date, shoot_date, status, total_amount)`
- `payments (payment_id PK, booking_id FK, amount, payment_date, method)`
- `deliveries (delivery_id PK, booking_id FK, status, notes)`

#### 5.3 Normalization
The database satisfies rules up to the **Third Normal Form (3NF)**:
- **1NF (First Normal Form)**: All attributes hold atomic values. For example, `first_name` and `last_name` are separated. There are no repeating groups.
- **2NF (Second Normal Form)**: Our tables use Single Column Surrogate Primary keys like `booking_id` or `customer_id`. As there are no composite primary keys, there are perfectly zero partial dependencies.
- **3NF (Third Normal Form)**: There are no transitive dependencies. E.g., The customer's address is found in `customers`, not duplicated inside `bookings`. Bookings purely rely on the `customer_id` relation.

---

### 6. Implementation

The application employs the **MVC (Model-View-Controller)** pattern.
- **Model**: Handled purely via `.sql` schema definitions and PyMySQL establishing connection rules via Python code.
- **View**: Implemented cleanly using Jinja2 HTML templates inside the `/templates` directory styled with Bootstrap 5.
- **Controller**: `app.py` acts as the director, capturing POST requests representing forms, routing to proper SQL functions, and pushing Flash messages upon success. 

**Core Code Highlights**:
- Use of PyMySQL parameterized arrays `execute("INSERT INTO customers ... VALUES (%s)", (val,))` guaranteeing prevention of SQL Injections attacks.
- Passwords (if connected via Werkzeug) can dynamically be hashed ensuring data privacy.

---

### 7. Testing

#### Test Scenario 1: Authentication
- **Input**: User puts `admin` and `wrongpassword`.
- **Expected Output**: Rejection and flash message "Invalid Username or Password!".
- **Result**: Passed. Redirects back to login.

#### Test Scenario 2: Create Customer
- **Input**: Navigate to Customer page, click "Add Customer", fill form with valid Name and Contact, click Save.
- **Expected Output**: Entry inserts into MySQL DB `customers` table. Webpage refreshes to show the new Name in the latest row.
- **Validation check**: Backend `NOT NULL` prevents crashes by making HTML fields `required`. 
- **Result**: Passed.

#### Test Scenario 3: Relational Integrity (Foreign Keys)
- **Action**: Delete a Customer whom already has past Bookings attached to them.
- **Expected Output**: Because `ON DELETE CASCADE` is set on the foreign key, all their respective bookings should logically vanish to avoid orphaned data errors.
- **Result**: Passed. Database executes cascade properly.

---

### 8. Conclusion
The Smart Photo Studio Management System successfully addresses the challenges of tracking photography jobs. By deeply applying the Software Development Life Cycle (from SRS to System design, to Implementation and Testing), we generated a stable platform. Normalization to 3NF ensures structural integrity of MySQL data, and utilizing Python alongside straightforward HTML resulted in an accessible yet immensely powerful application ready for launch.
