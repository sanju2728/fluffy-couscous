import sqlite3
conn= sqlite3.connect("employee.db")
cur = conn.cursor()
cur.execute("""
                create table if not exists emp(
                    ID int primary key, 
                    fname text, 
                    lname text
                );
                                    """)
conn.commit()

cur.execute("insert into emp values(1, 'Sanjana', 'Bhat')")

conn.commit()
v=cur.execute("select * from emp;")
print(v.fetchone())