#!/usr/bin/env python3
"""
Script to create test tables and sample data in DB2 database.
"""
import os
import sys
import ibm_db
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Build connection string
def get_connection_string():
    host = os.getenv("DB2_HOST", "localhost")
    port = os.getenv("DB2_PORT", "50000")
    database = os.getenv("DB2_DATABASE", "SAMPLE")
    username = os.getenv("DB2_USERNAME", "db2inst1")
    password = os.getenv("DB2_PASSWORD", "password")

    return f"DATABASE={database};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};"

def main():
    conn = None
    try:
        print("Connecting to DB2...")
        conn_str = get_connection_string()
        conn = ibm_db.connect(conn_str, "", "")
        if not conn:
            print("Failed to connect to DB2")
            sys.exit(1)

        print("✓ Connected to DB2\n")

        # Drop tables if they exist (ignore errors)
        print("Dropping existing test tables (if any)...")
        tables_to_drop = ['ORDERS', 'CUSTOMERS', 'PRODUCTS', 'EMPLOYEES']
        for table in tables_to_drop:
            try:
                ibm_db.exec_immediate(conn, f"DROP TABLE {table}")
                print(f"  - Dropped {table}")
            except:
                pass  # Table doesn't exist, ignore

        print("\nCreating tables...")

        # Create CUSTOMERS table
        print("  - Creating CUSTOMERS table...")
        ibm_db.exec_immediate(conn, """
            CREATE TABLE CUSTOMERS (
                CUSTOMER_ID INT NOT NULL PRIMARY KEY,
                FIRST_NAME VARCHAR(50) NOT NULL,
                LAST_NAME VARCHAR(50) NOT NULL,
                EMAIL VARCHAR(100),
                PHONE VARCHAR(20),
                CITY VARCHAR(50),
                STATE VARCHAR(2),
                CREATED_DATE DATE
            )
        """)

        # Create PRODUCTS table
        print("  - Creating PRODUCTS table...")
        ibm_db.exec_immediate(conn, """
            CREATE TABLE PRODUCTS (
                PRODUCT_ID INT NOT NULL PRIMARY KEY,
                PRODUCT_NAME VARCHAR(100) NOT NULL,
                CATEGORY VARCHAR(50),
                PRICE DECIMAL(10,2),
                STOCK_QUANTITY INT,
                DESCRIPTION VARCHAR(500)
            )
        """)

        # Create EMPLOYEES table
        print("  - Creating EMPLOYEES table...")
        ibm_db.exec_immediate(conn, """
            CREATE TABLE EMPLOYEES (
                EMPLOYEE_ID INT NOT NULL PRIMARY KEY,
                FIRST_NAME VARCHAR(50) NOT NULL,
                LAST_NAME VARCHAR(50) NOT NULL,
                DEPARTMENT VARCHAR(50),
                POSITION VARCHAR(50),
                SALARY DECIMAL(10,2),
                HIRE_DATE DATE,
                MANAGER_ID INT
            )
        """)

        # Create ORDERS table
        print("  - Creating ORDERS table...")
        ibm_db.exec_immediate(conn, """
            CREATE TABLE ORDERS (
                ORDER_ID INT NOT NULL PRIMARY KEY,
                CUSTOMER_ID INT NOT NULL,
                PRODUCT_ID INT NOT NULL,
                QUANTITY INT,
                ORDER_DATE DATE,
                TOTAL_AMOUNT DECIMAL(10,2),
                STATUS VARCHAR(20)
            )
        """)

        print("\n✓ Tables created successfully\n")

        print("Inserting sample data...")

        # Insert customers
        print("  - Inserting customers...")
        customers = [
            (1, 'John', 'Doe', 'john.doe@email.com', '555-0101', 'New York', 'NY', '2023-01-15'),
            (2, 'Jane', 'Smith', 'jane.smith@email.com', '555-0102', 'Los Angeles', 'CA', '2023-02-20'),
            (3, 'Bob', 'Johnson', 'bob.johnson@email.com', '555-0103', 'Chicago', 'IL', '2023-03-10'),
            (4, 'Alice', 'Williams', 'alice.w@email.com', '555-0104', 'Houston', 'TX', '2023-04-05'),
            (5, 'Charlie', 'Brown', 'charlie.b@email.com', '555-0105', 'Phoenix', 'AZ', '2023-05-12'),
        ]

        for customer in customers:
            ibm_db.exec_immediate(conn, f"""
                INSERT INTO CUSTOMERS VALUES ({customer[0]}, '{customer[1]}', '{customer[2]}',
                '{customer[3]}', '{customer[4]}', '{customer[5]}', '{customer[6]}', '{customer[7]}')
            """)

        # Insert products
        print("  - Inserting products...")
        products = [
            (1, 'Laptop Pro 15', 'Electronics', 1299.99, 25, 'High-performance laptop with 15-inch display'),
            (2, 'Wireless Mouse', 'Electronics', 29.99, 150, 'Ergonomic wireless mouse'),
            (3, 'Office Chair', 'Furniture', 249.99, 45, 'Comfortable ergonomic office chair'),
            (4, 'Standing Desk', 'Furniture', 499.99, 20, 'Adjustable height standing desk'),
            (5, 'USB-C Hub', 'Electronics', 49.99, 200, '7-in-1 USB-C hub with multiple ports'),
            (6, 'Notebook Set', 'Stationery', 15.99, 500, 'Set of 3 premium notebooks'),
            (7, 'Desk Lamp', 'Furniture', 39.99, 75, 'LED desk lamp with adjustable brightness'),
        ]

        for product in products:
            ibm_db.exec_immediate(conn, f"""
                INSERT INTO PRODUCTS VALUES ({product[0]}, '{product[1]}', '{product[2]}',
                {product[3]}, {product[4]}, '{product[5]}')
            """)

        # Insert employees
        print("  - Inserting employees...")
        employees = [
            (1, 'Michael', 'Scott', 'Sales', 'Regional Manager', 75000.00, '2020-01-15', None),
            (2, 'Jim', 'Halpert', 'Sales', 'Sales Representative', 55000.00, '2020-03-20', 1),
            (3, 'Pam', 'Beesly', 'Reception', 'Receptionist', 45000.00, '2020-02-10', 1),
            (4, 'Dwight', 'Schrute', 'Sales', 'Assistant Regional Manager', 60000.00, '2020-01-20', 1),
            (5, 'Angela', 'Martin', 'Accounting', 'Senior Accountant', 58000.00, '2020-04-01', None),
            (6, 'Oscar', 'Martinez', 'Accounting', 'Accountant', 52000.00, '2020-05-15', 5),
        ]

        for emp in employees:
            manager_clause = f"{emp[7]}" if emp[7] else "NULL"
            ibm_db.exec_immediate(conn, f"""
                INSERT INTO EMPLOYEES VALUES ({emp[0]}, '{emp[1]}', '{emp[2]}',
                '{emp[3]}', '{emp[4]}', {emp[5]}, '{emp[6]}', {manager_clause})
            """)

        # Insert orders
        print("  - Inserting orders...")
        orders = [
            (1, 1, 1, 1, '2024-01-15', 1299.99, 'Delivered'),
            (2, 1, 2, 2, '2024-01-15', 59.98, 'Delivered'),
            (3, 2, 3, 1, '2024-02-20', 249.99, 'Shipped'),
            (4, 3, 4, 1, '2024-03-10', 499.99, 'Processing'),
            (5, 4, 5, 3, '2024-03-25', 149.97, 'Delivered'),
            (6, 5, 6, 10, '2024-04-05', 159.90, 'Delivered'),
            (7, 2, 7, 2, '2024-04-10', 79.98, 'Shipped'),
            (8, 3, 1, 1, '2024-04-20', 1299.99, 'Processing'),
        ]

        for order in orders:
            ibm_db.exec_immediate(conn, f"""
                INSERT INTO ORDERS VALUES ({order[0]}, {order[1]}, {order[2]},
                {order[3]}, '{order[4]}', {order[5]}, '{order[6]}')
            """)

        print("\n✓ Sample data inserted successfully\n")

        # Verify tables and counts
        print("Verification:")
        tables = ['CUSTOMERS', 'PRODUCTS', 'EMPLOYEES', 'ORDERS']
        for table in tables:
            stmt = ibm_db.exec_immediate(conn, f"SELECT COUNT(*) FROM {table}")
            row = ibm_db.fetch_tuple(stmt)
            print(f"  - {table}: {row[0]} rows")

        print("\n✅ Database setup complete! You can now test the MCP server.")

    except Exception as e:
        print(f"\n❌ Error: {e}")
        sys.exit(1)
    finally:
        if conn:
            ibm_db.close(conn)

if __name__ == "__main__":
    main()
