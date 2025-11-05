#!/usr/bin/env python3
"""
Script to view test data in DB2 database.
"""
import os
import ibm_db
from dotenv import load_dotenv

load_dotenv()

def get_connection_string():
    host = os.getenv("DB2_HOST", "localhost")
    port = os.getenv("DB2_PORT", "50000")
    database = os.getenv("DB2_DATABASE", "TESTDB")
    username = os.getenv("DB2_USERNAME", "db2inst1")
    password = os.getenv("DB2_PASSWORD", "password")
    return f"DATABASE={database};HOSTNAME={host};PORT={port};PROTOCOL=TCPIP;UID={username};PWD={password};"

def main():
    conn = ibm_db.connect(get_connection_string(), "", "")

    # Query customers
    print("=" * 70)
    print("CUSTOMERS")
    print("=" * 70)
    stmt = ibm_db.exec_immediate(conn, "SELECT * FROM CUSTOMERS ORDER BY CUSTOMER_ID")
    row = ibm_db.fetch_assoc(stmt)
    while row:
        print(f"{row['CUSTOMER_ID']:3d} | {row['FIRST_NAME']:10s} {row['LAST_NAME']:10s} | {row['EMAIL']:25s} | {row['CITY']:15s}, {row['STATE']}")
        row = ibm_db.fetch_assoc(stmt)

    # Query products
    print("\n" + "=" * 70)
    print("PRODUCTS")
    print("=" * 70)
    stmt = ibm_db.exec_immediate(conn, "SELECT * FROM PRODUCTS ORDER BY PRODUCT_ID")
    row = ibm_db.fetch_assoc(stmt)
    while row:
        price = float(row['PRICE']) if row['PRICE'] else 0.0
        print(f"{row['PRODUCT_ID']:3d} | {row['PRODUCT_NAME']:20s} | ${price:8.2f} | Stock: {row['STOCK_QUANTITY']:3d}")
        row = ibm_db.fetch_assoc(stmt)

    # Query employees
    print("\n" + "=" * 70)
    print("EMPLOYEES")
    print("=" * 70)
    stmt = ibm_db.exec_immediate(conn, "SELECT * FROM EMPLOYEES ORDER BY EMPLOYEE_ID")
    row = ibm_db.fetch_assoc(stmt)
    while row:
        salary = float(row['SALARY']) if row['SALARY'] else 0.0
        manager = f"(Manager: {row['MANAGER_ID']})" if row['MANAGER_ID'] else "(No Manager)"
        print(f"{row['EMPLOYEE_ID']:3d} | {row['FIRST_NAME']:10s} {row['LAST_NAME']:10s} | {row['DEPARTMENT']:12s} | ${salary:10.2f} {manager}")
        row = ibm_db.fetch_assoc(stmt)

    # Query orders
    print("\n" + "=" * 70)
    print("ORDERS")
    print("=" * 70)
    stmt = ibm_db.exec_immediate(conn, "SELECT * FROM ORDERS ORDER BY ORDER_ID")
    row = ibm_db.fetch_assoc(stmt)
    while row:
        total = float(row['TOTAL_AMOUNT']) if row['TOTAL_AMOUNT'] else 0.0
        print(f"Order #{row['ORDER_ID']:3d} | Customer: {row['CUSTOMER_ID']} | Product: {row['PRODUCT_ID']} | ${total:8.2f} | {row['STATUS']:12s}")
        row = ibm_db.fetch_assoc(stmt)

    print("\n" + "=" * 70)
    ibm_db.close(conn)

if __name__ == "__main__":
    main()
