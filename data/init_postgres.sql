CREATE TABLE employees (
    id SERIAL PRIMARY KEY,
    name TEXT,
    department_id INTEGER,
    salary REAL
);

CREATE TABLE departments (
    id SERIAL PRIMARY KEY,
    name TEXT
);

-- Sample Data
INSERT INTO departments (name) VALUES ('Sales'), ('Marketing'), ('Engineering');

INSERT INTO employees (name, department_id, salary) VALUES ('Alice', 1, 60000);
INSERT INTO employees (name, department_id, salary) VALUES ('Bob', 2, 75000);
INSERT INTO employees (name, department_id, salary) VALUES ('Charlie', 1, 55000);
INSERT INTO employees (name, department_id, salary) VALUES ('David', 3, 80000);
INSERT INTO employees (name, department_id, salary) VALUES ('Eve', 2, 70000);
