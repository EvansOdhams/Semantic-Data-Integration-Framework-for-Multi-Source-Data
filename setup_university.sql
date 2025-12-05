-- Schema and sample data for the university domain (SQLite)

-- Drop tables if they already exist (for re-runs)
DROP TABLE IF EXISTS Enrollments;
DROP TABLE IF EXISTS Students;
DROP TABLE IF EXISTS Courses;

-- Create tables
CREATE TABLE Students (
    student_id    INTEGER PRIMARY KEY,
    first_name    TEXT,
    last_name     TEXT,
    date_of_birth TEXT,   -- ISO string 'YYYY-MM-DD'
    major         TEXT
);

CREATE TABLE Courses (
    course_id     INTEGER PRIMARY KEY,
    course_code   TEXT,
    course_title  TEXT,
    department    TEXT,
    credits       INTEGER
);

CREATE TABLE Enrollments (
    enrollment_id INTEGER PRIMARY KEY,
    student_id    INTEGER,
    course_id     INTEGER,
    semester      TEXT,
    year          INTEGER,
    grade         TEXT,
    FOREIGN KEY (student_id) REFERENCES Students(student_id),
    FOREIGN KEY (course_id)  REFERENCES Courses(course_id)
);

-- Sample data for Students
INSERT INTO Students (student_id, first_name, last_name, date_of_birth, major) VALUES
(1, 'Alice', 'Mensah', '2002-03-10', 'Computer Science'),
(2, 'Brian', 'Osei', '2001-11-22', 'Information Systems'),
(3, 'Cynthia', 'Boateng', '2000-07-05', 'Business Administration');

-- Sample data for Courses
INSERT INTO Courses (course_id, course_code, course_title, department, credits) VALUES
(101, 'CSC101', 'Introduction to Programming', 'Computer Science', 3),
(102, 'CSC202', 'Data Structures', 'Computer Science', 3),
(201, 'BUS110', 'Principles of Management', 'Business', 3);

-- Sample data for Enrollments
INSERT INTO Enrollments (enrollment_id, student_id, course_id, semester, year, grade) VALUES
(1, 1, 101, 'Spring', 2024, 'A'),
(2, 1, 201, 'Spring', 2024, 'B'),
(3, 2, 101, 'Spring', 2024, 'B'),
(4, 3, 201, 'Spring', 2024, 'A'),
(5, 2, 102, 'Fall', 2024, NULL);


