import random
import csv

random.seed(11)

facility_capacity = {
    "Library": 400,
    "Computer Lab": 200,
    "Canteen": 500,
    "Seminar Hall": 150,
    "Classroom": 80,
    "Wifi Zone": 600
}

facilities = list(facility_capacity.keys())
days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday"]
time_slots = ["9 AM", "10 AM", "11 AM", "12 PM", "1 PM", "2 PM", "3 PM", "4 PM", "5 PM"]
departments = ["CSE", "ECE", "MECH", "CIVIL", "IT", "MBA"]

rows = []
row_id = 1

for i in range(650):
    facility = random.choice(facilities)
    cap = facility_capacity[facility]
    day = random.choice(days)
    time = random.choice(time_slots)
    dept = random.choice(departments)

    if time in ["10 AM", "1 PM", "2 PM"]:
        base = random.randint(int(cap * 0.5), cap)
    else:
        base = random.randint(10, int(cap * 0.6))

    students = base
    if students > cap:
        students = cap

    prev_usage = students - random.randint(-30, 40)
    if prev_usage < 0:
        prev_usage = random.randint(5, 20)

    occ = (students / cap) * 100

    if occ >= 70:
        demand = "High"
    elif occ >= 40:
        demand = "Medium"
    else:
        demand = "Low"

    flip = random.random()
    if flip < 0.06:
        options = ["Low", "Medium", "High"]
        options.remove(demand)
        demand = random.choice(options)

    rows.append([row_id, facility, day, time, dept, students, prev_usage, cap, demand])
    row_id += 1

with open("facility_usage.csv", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Record_ID", "Facility", "Day", "Time", "Department", "Students", "Previous_Usage", "Capacity", "Demand_Level"])
    writer.writerows(rows)

print("facility_usage.csv created with", len(rows), "rows")
