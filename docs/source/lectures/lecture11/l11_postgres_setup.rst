====================================================
PostgreSQL Setup Guide
====================================================

This guide walks you through installing PostgreSQL, connecting with
``psql``, and loading a sample ``employees`` / ``departments`` database
that matches the queries used throughout the lecture. Two installation
options are provided: **Docker** (recommended for this course) and
**native installation**.

.. note::

   If you already have PostgreSQL installed and running from an earlier
   lecture (L6 / L7 / L8), you can reuse it -- just run the sample-data
   section against it.


Option A: Docker (Recommended)
====================================================

Docker provides the fastest, cleanest setup. No system-level packages
are installed, and you can remove everything with a single command.


Prerequisites
----------------------------------------------------

- Docker Desktop installed and running.

  - **macOS / Windows**: download from https://www.docker.com/products/docker-desktop/
  - **Linux**: install Docker Engine via your package manager.

- Verify Docker is working:

  .. code-block:: bash

     docker --version
     # Docker version 27.x.x or later


Pull and Start PostgreSQL
----------------------------------------------------

.. code-block:: bash

   # Pull the official PostgreSQL image
   docker pull postgres:17

   # Start a PostgreSQL container
   docker run -d \
     --name postgres \
     -e POSTGRES_USER=enpm \
     -e POSTGRES_PASSWORD=enpm818t \
     -e POSTGRES_DB=enpm818t \
     -p 5432:5432 \
     -v pg_data:/var/lib/postgresql/data \
     postgres:17

This command:

- Runs PostgreSQL 17 in the background (``-d``).
- Creates a user ``enpm`` with password ``enpm818t`` and a database
  ``enpm818t``.
- Maps port ``5432`` on your machine into the container.
- Persists data in a Docker volume (``pg_data``) so data survives
  container restarts.


Connect with ``psql``
----------------------------------------------------

.. code-block:: bash

   # If you have psql installed locally:
   psql "postgresql://enpm:enpm818t@localhost:5432/enpm818t"

   # Otherwise, run it inside the container:
   docker exec -it postgres psql -U enpm -d enpm818t

You should see a prompt like:

.. code-block:: text

   psql (17.x)
   Type "help" for help.

   enpm818t=>

Sanity check:

.. code-block:: sql

   SELECT version();


Stop and Restart
----------------------------------------------------

.. code-block:: bash

   # Stop the container
   docker stop postgres

   # Start it again (data is preserved)
   docker start postgres

   # Remove the container entirely
   docker rm -f postgres

   # Remove the data volume too (destroys all data)
   docker volume rm pg_data


Option B: Native Installation
====================================================


macOS (Homebrew)
----------------------------------------------------

.. code-block:: bash

   brew install postgresql@17
   brew services start postgresql@17
   psql postgres


Ubuntu / Debian
----------------------------------------------------

.. code-block:: bash

   sudo apt-get update
   sudo apt-get install -y postgresql postgresql-contrib

   sudo systemctl start postgresql
   sudo systemctl enable postgresql

   sudo -u postgres psql


Windows
----------------------------------------------------

1. Download the installer from https://www.postgresql.org/download/windows/.
2. Run the installer and follow the prompts.
3. Open **SQL Shell (psql)** from the Start menu.


Loading the Sample Database
====================================================

The sample schema mirrors the lecture's ``employees`` / ``departments``
examples. Copy and paste the following into ``psql``.


Create the Schema
----------------------------------------------------

.. code-block:: sql

   DROP TABLE IF EXISTS employees;
   DROP TABLE IF EXISTS departments;

   CREATE TABLE departments (
     id   SERIAL PRIMARY KEY,
     name TEXT NOT NULL UNIQUE
   );

   CREATE TABLE employees (
     id              SERIAL PRIMARY KEY,
     name            TEXT NOT NULL,
     age             INT  NOT NULL,
     salary          NUMERIC(10, 2) NOT NULL,
     department      TEXT,            -- legacy string join column
     department_id   INT REFERENCES departments(id),
     hire_date       DATE NOT NULL
   );

Two join columns are intentionally present:

- ``employees.department`` (TEXT) -- mirrors the lecture's slow
  string-equality join.
- ``employees.department_id`` (INT, FK) -- mirrors the fast
  integer-on-indexed-PK join after the data-modeling improvement.

This lets you reproduce the **3x speedup** shown in lecture.


Populate ``departments``
----------------------------------------------------

.. code-block:: sql

   INSERT INTO departments (name) VALUES
     ('Engineering'),
     ('Sales'),
     ('Marketing'),
     ('HR'),
     ('Finance');


Populate ``employees`` (1000 Synthetic Rows)
----------------------------------------------------

.. code-block:: sql

   -- Insert 1000 synthetic employees
   INSERT INTO employees (name, age, salary, department, department_id, hire_date)
   SELECT
     'Employee ' || g                                 AS name,
     20 + (g % 45)                                    AS age,                -- 20..64
     40000 + (g * 137) % 120000                       AS salary,             -- spread
     (ARRAY['Engineering','Sales','Marketing','HR','Finance'])[1 + (g % 5)]  AS department,
     1 + (g % 5)                                      AS department_id,
     DATE '2015-01-01' + ((g * 7) % 4000)             AS hire_date           -- spread over ~11 yrs
   FROM generate_series(1, 1000) AS g;


Verify the Data
----------------------------------------------------

.. code-block:: sql

   SELECT COUNT(*) FROM employees;       -- 1000
   SELECT COUNT(*) FROM departments;     -- 5

   -- Age distribution
   SELECT MIN(age), MAX(age), AVG(age)::INT FROM employees;

   -- One employee
   SELECT * FROM employees WHERE id = 7;


Useful Indexes for the Lecture Queries
----------------------------------------------------

These match the indexes referenced in the lecture and exercises. Add
them **one at a time** and re-run ``EXPLAIN ANALYZE`` to see the plan
change.

.. code-block:: sql

   -- Index on hire_date to accelerate the WHERE filter
   CREATE INDEX idx_employees_hire_date ON employees(hire_date);

   -- Compound index on department_id + hire_date to support common
   -- filter + join combinations
   CREATE INDEX idx_employees_dept_hire ON employees(department_id, hire_date);

   -- Before adding an index, drop it with:
   -- DROP INDEX idx_employees_hire_date;


Try the Lecture Queries
====================================================

Each of these reproduces something from the lecture. Run them with
``EXPLAIN ANALYZE`` to see the plan.


Basic ``Seq Scan`` with Filter
----------------------------------------------------

.. code-block:: sql

   EXPLAIN ANALYZE
   SELECT * FROM employees WHERE age > 30;


Slow String-Join Plan
----------------------------------------------------

.. code-block:: sql

   EXPLAIN ANALYZE
   SELECT departments.name,
          COUNT(employees.id)     AS total_employees,
          AVG(employees.salary)   AS average_salary
   FROM departments
   JOIN employees ON departments.name = employees.department
   WHERE employees.hire_date > '2020-01-01'
   GROUP BY departments.name
   HAVING COUNT(employees.id) > 10
   ORDER BY average_salary DESC
   LIMIT 5;


Faster FK-Join Plan
----------------------------------------------------

.. code-block:: sql

   EXPLAIN ANALYZE
   SELECT departments.name,
          COUNT(employees.id)     AS total_employees,
          AVG(employees.salary)   AS average_salary
   FROM departments
   JOIN employees ON departments.id = employees.department_id
   WHERE employees.hire_date > '2020-01-01'
   GROUP BY departments.name
   HAVING COUNT(employees.id) > 10
   ORDER BY average_salary DESC
   LIMIT 5;

Compare the **Planning Time** and **Execution Time** lines between the
two versions.


Advanced Analysis Variants
----------------------------------------------------

.. code-block:: sql

   EXPLAIN (ANALYZE, BUFFERS)    SELECT * FROM employees WHERE age > 30;
   EXPLAIN (ANALYZE, MEMORY)     SELECT * FROM employees WHERE age > 30;
   EXPLAIN (ANALYZE, SERIALIZE)  SELECT * FROM employees WHERE age > 30;


Diagnosing a Mutating Query Safely
----------------------------------------------------

.. code-block:: sql

   BEGIN;
   EXPLAIN ANALYZE
   UPDATE employees SET salary = salary + 1000 WHERE id = 7;
   ROLLBACK;

After the ``ROLLBACK``, the salary is unchanged; you still get the
plan and measurements.


Cleanup
====================================================

Wipe the sample tables:

.. code-block:: sql

   DROP TABLE IF EXISTS employees;
   DROP TABLE IF EXISTS departments;

Or, if using Docker, tear down the whole instance:

.. code-block:: bash

   docker rm -f postgres
   docker volume rm pg_data


Further Reading
====================================================

- `PostgreSQL -- Using EXPLAIN
  <https://www.postgresql.org/docs/current/using-explain.html>`_
- `PostgreSQL -- Planner Cost Constants
  <https://www.postgresql.org/docs/current/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS>`_
- `PostgreSQL -- Resource Consumption
  <https://www.postgresql.org/docs/current/runtime-config-resource.html>`_
  (``work_mem``, ``shared_buffers``, ``maintenance_work_mem``)
- `PostgreSQL -- Indexes
  <https://www.postgresql.org/docs/current/indexes.html>`_
