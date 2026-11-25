import sqlite3

conn = sqlite3.connect("campus.db")
cur = conn.cursor()

with open("database_setup.sql", "r") as f:
    script = f.read()

cur.executescript(script)
conn.commit()

print("---- High demand records ----")
for row in cur.execute("SELECT * FROM facility_usage WHERE demand_level = 'High'"):
    print(row)

print("\n---- Average students per facility ----")
for row in cur.execute("SELECT facility_id, AVG(students_count) FROM facility_usage GROUP BY facility_id ORDER BY AVG(students_count) DESC"):
    print(row)

print("\n---- Facilities with capacity above average (subquery) ----")
for row in cur.execute("SELECT facility_name FROM facility_master WHERE capacity > (SELECT AVG(capacity) FROM facility_master)"):
    print(row)

print("\n---- Department wise usage ----")
for row in cur.execute("SELECT department, COUNT(*), AVG(students_count) FROM facility_usage GROUP BY department ORDER BY COUNT(*) DESC"):
    print(row)

print("\n---- Join example: facility name with demand ----")
query = """
SELECT fm.facility_name, fu.day, fu.students_count, fu.demand_level
FROM facility_usage fu
JOIN facility_master fm ON fu.facility_id = fm.facility_id
"""
for row in cur.execute(query):
    print(row)

conn.close()
print("\ncampus.db created successfully")
