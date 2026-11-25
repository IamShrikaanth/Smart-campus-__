DROP TABLE IF EXISTS students;
DROP TABLE IF EXISTS facility_master;
DROP TABLE IF EXISTS facility_usage;
DROP TABLE IF EXISTS daily_usage;

CREATE TABLE students (
    student_id INTEGER PRIMARY KEY,
    student_name TEXT,
    department TEXT,
    year INTEGER
);

CREATE TABLE facility_master (
    facility_id INTEGER PRIMARY KEY,
    facility_name TEXT,
    capacity INTEGER,
    location TEXT,
    facility_type TEXT
);

CREATE TABLE facility_usage (
    usage_id INTEGER PRIMARY KEY,
    facility_id INTEGER,
    day TEXT,
    time_slot TEXT,
    department TEXT,
    students_count INTEGER,
    previous_usage INTEGER,
    demand_level TEXT,
    FOREIGN KEY (facility_id) REFERENCES facility_master(facility_id)
);

CREATE TABLE daily_usage (
    daily_id INTEGER PRIMARY KEY,
    facility_id INTEGER,
    day TEXT,
    total_students INTEGER,
    FOREIGN KEY (facility_id) REFERENCES facility_master(facility_id)
);

INSERT INTO students (student_id, student_name, department, year) VALUES
(1, 'Arjun Kumar', 'CSE', 2),
(2, 'Divya S', 'ECE', 3),
(3, 'Rahul M', 'MECH', 1),
(4, 'Priya R', 'IT', 4),
(5, 'Karthik V', 'CIVIL', 2),
(6, 'Sneha T', 'MBA', 1);

INSERT INTO facility_master (facility_id, facility_name, capacity, location, facility_type) VALUES
(1, 'Library', 400, 'Block A', 'Academic'),
(2, 'Computer Lab', 200, 'Block B', 'Academic'),
(3, 'Canteen', 500, 'Block C', 'Recreational'),
(4, 'Seminar Hall', 150, 'Block A', 'Academic'),
(5, 'Classroom', 80, 'Block D', 'Academic'),
(6, 'Wifi Zone', 600, 'Campus Wide', 'Utility');

INSERT INTO facility_usage (usage_id, facility_id, day, time_slot, department, students_count, previous_usage, demand_level) VALUES
(1, 1, 'Monday', '10 AM', 'CSE', 320, 290, 'High'),
(2, 2, 'Tuesday', '2 PM', 'ECE', 180, 120, 'Medium'),
(3, 3, 'Friday', '1 PM', 'MECH', 450, 410, 'High'),
(4, 4, 'Wednesday', '4 PM', 'IT', 80, 60, 'Low'),
(5, 1, 'Thursday', '11 AM', 'CIVIL', 150, 140, 'Medium'),
(6, 5, 'Saturday', '9 AM', 'MBA', 20, 15, 'Low');

INSERT INTO daily_usage (daily_id, facility_id, day, total_students) VALUES
(1, 1, 'Monday', 320),
(2, 2, 'Tuesday', 180),
(3, 3, 'Friday', 450),
(4, 4, 'Wednesday', 80),
(5, 1, 'Thursday', 150),
(6, 5, 'Saturday', 20);

SELECT * FROM facility_usage WHERE demand_level = 'High';

SELECT facility_id, AVG(students_count) AS avg_students
FROM facility_usage
GROUP BY facility_id
ORDER BY avg_students DESC;

SELECT fm.facility_name, fu.day, fu.students_count, fu.demand_level
FROM facility_usage fu
JOIN facility_master fm ON fu.facility_id = fm.facility_id
WHERE fu.demand_level = 'High';

SELECT fm.facility_name, COUNT(*) AS high_demand_count
FROM facility_usage fu
JOIN facility_master fm ON fu.facility_id = fm.facility_id
WHERE fu.demand_level = 'High'
GROUP BY fm.facility_name;

SELECT facility_name FROM facility_master
WHERE capacity > (SELECT AVG(capacity) FROM facility_master);

SELECT department, COUNT(*) AS total_visits, AVG(students_count) AS avg_students
FROM facility_usage
GROUP BY department
ORDER BY total_visits DESC;
