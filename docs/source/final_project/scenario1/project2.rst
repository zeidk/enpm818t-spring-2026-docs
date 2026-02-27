====================================================
Group Project 2: PostgreSQL + Python Integration
====================================================

Overview
--------

Implement your GP1 design in PostgreSQL, generate realistic sample data, write SQL queries supporting traffic operations, and build a Python command-line application with a menu-driven interface.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 3 weeks |
   **Weight**: 15 points (30% of final project) |
   **Team Size**: 4 students

**Builds on**: Your GP1 relational design


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Translate conceptual designs into physical PostgreSQL schemas
- Write DDL with tables, constraints, indexes, and triggers
- Generate and validate sample data respecting all constraints
- Write multi-table JOINs, aggregate queries, subqueries, and geospatial queries
- Integrate PostgreSQL with Python using psycopg2
- Design repository and service layer architecture
- Build a menu-driven CLI application


Part 1: Physical Database Implementation
-----------------------------------------

**Objective**: Transform your GP1 design into a working PostgreSQL database with realistic data.

.. dropdown:: Task 1.1: Schema Implementation (3 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Create ``schema.sql`` with:

   - **Database setup**: Extensions (PostGIS for geospatial)
   - **Custom types**: ENUMs for constrained values
   - **All tables**: Complete with all columns from GP1
   - **Primary keys**: All defined correctly
   - **Foreign keys**: With ON DELETE/UPDATE rules
   - **Check constraints**: Business rules from your GP1 entity catalog
   - **NOT NULL constraints**: All mandatory fields
   - **UNIQUE constraints**: All candidate keys
   - **Indexes**: Strategic indexes for query performance
   - **Triggers**: Automatic ``updated_at`` timestamps

   **PostGIS Integration**:

   .. code-block:: sql

      CREATE EXTENSION IF NOT EXISTS postgis;

      ALTER TABLE intersection
      ADD COLUMN location GEOGRAPHY(POINT, 4326);

      CREATE INDEX idx_intersection_location
      ON intersection USING GIST (location);

   **File to create**: ``postgresql/schema.sql``

.. dropdown:: Task 1.2: Sample Data Generation (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Generate realistic sample data that fits your schema. We provide a :doc:`Data Generation Guide <data_generation_guide>` containing a ready-to-use prompt. The workflow is:

   1. Export your schema definition with ``pg_dump`` or ``\d+`` commands
   2. Paste the provided prompt and your schema into an LLM (e.g., Claude, ChatGPT)
   3. Review the generated INSERT statements for correctness
   4. Save as ``data.sql`` and load into your database
   5. Fix any constraint violations and verify data quality

   **Minimum Data Volumes**:

   - 50+ intersections in a realistic city grid
   - 100+ traffic signals across intersections
   - 150+ sensors (multiple per intersection)
   - 50+ road segments connecting intersections
   - 100+ maintenance records (various dates)
   - 10+ maintenance crews
   - 75+ incidents (last 90 days)
   - 20+ emergency routes
   - 10+ emergency facilities
   - 5+ weather stations
   - 10+ parking facilities
   - 5+ traffic control zones

   **Data Quality Checks** (run after loading):

   .. code-block:: text

      After loading data, verify:

      1. All FK references resolve (no orphan records)
      2. All CHECK constraints pass
      3. Geographic coordinates form a realistic grid
      4. Temporal data spans at least 90 days
      5. Every intersection has at least one signal
      6. Every zone contains multiple intersections

   **File to create**: ``postgresql/data.sql``


Part 2: SQL Queries
--------------------

**Objective**: Write 8+ queries demonstrating your ability to extract meaningful information from the database.

.. dropdown:: Query Categories (5 points total)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Write at least **8 queries** covering all of the following categories:

   **Multi-Table JOINs (3 queries minimum)**

   Combine 3 or more tables to answer business questions.

   Examples:

   - *"Which intersections have the most incidents, and what sensors are installed there?"*
   - *"List all maintenance tasks with crew details and intersection information."*
   - *"Find signals at intersections that have had critical incidents in the last 30 days."*

   **Aggregate Functions (2 queries minimum)**

   Use COUNT, SUM, AVG, MIN, MAX with GROUP BY and HAVING.

   Examples:

   - *"Calculate average incident resolution time by severity level."*
   - *"Count sensors per intersection and find intersections with fewer than 2 sensors."*

   **Subqueries (1 query minimum)**

   Use subqueries in WHERE, FROM, or SELECT clauses to solve multi-step problems.

   Examples:

   - *"Find intersections with more incidents than the citywide average."*
   - *"List crews that have never been assigned to a critical-priority maintenance task."*

   **PostGIS Geospatial (2 queries minimum)**

   Use PostGIS functions for location-based analysis.

   Examples:

   - *"Find all sensors within 500 meters of a given incident location."*
   - *"List the 5 nearest emergency facilities to a specific intersection."*

.. dropdown:: Query Documentation Format
   :icon: gear
   :class-container: sd-border-primary

   Use this format for **every query** in ``queries.sql``:

   .. code-block:: sql

      -- Query #X: [Title]
      -- Business Question: [Problem being solved]
      -- Complexity Features: [JOINs, aggregates, subqueries, geospatial]
      -- Tables Used: [List all tables]

      [YOUR SQL QUERY]

      -- Expected Output: [Description of result columns]
      -- Sample Results: [First 3 rows with representative data]

   **File to create**: ``postgresql/queries.sql``


Part 3: Python CLI Application
-------------------------------

**Objective**: Build a layered Python application with a menu-driven command-line interface that connects to your PostgreSQL database.

.. dropdown:: Task 3.1: Application Architecture (3 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Organize your code in layers:

   .. code-block:: text

      traffic-management/
      ├── requirements.txt
      ├── .env.example
      ├── config/
      │   └── database.py          # Connection pooling
      ├── models/
      │   ├── intersection.py      # Dataclasses
      │   └── [other models].py
      ├── repositories/
      │   ├── base_repository.py
      │   ├── intersection_repo.py # CRUD operations
      │   └── [other repos].py
      ├── services/
      │   └── traffic_service.py   # Business logic
      ├── cli/
      │   └── main.py              # Menu-driven interface
      └── tests/

   **Layer Responsibilities**:

   - **config/**: Database connection pooling with psycopg2. Configuration loaded from environment variables.
   - **models/**: Python dataclasses representing each entity. Each dataclass mirrors a database table and includes a ``from_row()`` class method to convert query results into objects.
   - **repositories/**: CRUD operations and custom queries for each entity. Each repository handles its own SQL and returns model objects. Repositories do not contain business logic.
   - **services/**: Business logic combining multiple repositories. For example, a ``traffic_service.get_intersection_dashboard(id)`` method might call the intersection repository, incident repository, and sensor repository to assemble a complete view.
   - **cli/**: Menu-driven interface that calls service methods and formats output for the terminal. The CLI contains no SQL and no direct database access.

.. dropdown:: Task 3.2: Connection Management
   :icon: gear
   :class-container: sd-border-primary

   Implement connection pooling with psycopg2. Your connection management should handle four concerns:

   **Pool size**: Use ``psycopg2.pool.SimpleConnectionPool`` with ``minconn=2`` and ``maxconn=10``. The pool pre-creates 2 connections at startup and can grow up to 10 under load. This avoids the overhead of creating a new connection for every query.

   **Context manager for automatic cleanup**: Wrap pool access in a context manager so that connections are always returned to the pool, even if an exception occurs. This prevents connection leaks where a borrowed connection is never returned.

   **Error handling for connection failures**: Catch ``psycopg2.OperationalError`` when creating the pool or borrowing connections. Print a clear error message (e.g., "Cannot connect to database. Check your .env settings.") instead of crashing with a raw stack trace.

   **Configuration from environment variables**: Read database host, port, name, user, and password from environment variables (using ``os.getenv()`` with sensible defaults). Provide a ``.env.example`` file so teammates can set up their own environment without sharing credentials in version control.

   **Example implementation**:

   .. code-block:: python

      from psycopg2 import pool, OperationalError
      from contextlib import contextmanager
      import os

      class DatabaseConfig:
          _pool = None

          @classmethod
          def initialize(cls):
              """Create the connection pool. Call once at application startup."""
              try:
                  cls._pool = pool.SimpleConnectionPool(
                      minconn=2,
                      maxconn=10,
                      host=os.getenv("DB_HOST", "localhost"),
                      port=os.getenv("DB_PORT", "5432"),
                      dbname=os.getenv("DB_NAME", "traffic_management"),
                      user=os.getenv("DB_USER", "postgres"),
                      password=os.getenv("DB_PASSWORD", "")
                  )
              except OperationalError as e:
                  print(f"Error: Cannot connect to database. Check .env settings.")
                  print(f"Details: {e}")
                  raise SystemExit(1)

          @classmethod
          @contextmanager
          def get_connection(cls):
              """
              Borrow a connection from the pool.

              Usage:
                  with DatabaseConfig.get_connection() as conn:
                      with conn.cursor() as cur:
                          cur.execute("SELECT ...")

              The connection is automatically returned to the pool
              when the with-block exits, even if an exception occurs.
              """
              if cls._pool is None:
                  cls.initialize()
              conn = cls._pool.getconn()
              try:
                  yield conn
                  conn.commit()
              except Exception:
                  conn.rollback()
                  raise
              finally:
                  cls._pool.putconn(conn)

          @classmethod
          def close_all(cls):
              """Close all connections. Call at application shutdown."""
              if cls._pool is not None:
                  cls._pool.closeall()

.. dropdown:: Task 3.3: Repository Pattern
   :icon: gear
   :class-container: sd-border-primary

   Each major entity needs a repository with:

   - ``find_by_id(id)`` -- Single record lookup
   - ``find_all(limit, offset)`` -- Paginated list
   - ``create(entity)`` -- Insert new record
   - ``update(entity)`` -- Update existing
   - ``delete(id)`` -- Remove record
   - Custom query methods (e.g., ``find_by_zone(zone_id)``)

   **Example**:

   .. code-block:: python

      class IntersectionRepository:
          def find_by_id(self, intersection_id):
              with DatabaseConfig.get_connection() as conn:
                  with conn.cursor() as cur:
                      cur.execute(
                          "SELECT * FROM intersection WHERE intersection_id = %s",
                          (intersection_id,)
                      )
                      row = cur.fetchone()
                      return Intersection.from_row(row) if row else None

          def find_all(self, limit=20, offset=0):
              with DatabaseConfig.get_connection() as conn:
                  with conn.cursor() as cur:
                      cur.execute(
                          "SELECT * FROM intersection ORDER BY intersection_id "
                          "LIMIT %s OFFSET %s",
                          (limit, offset)
                      )
                      return [Intersection.from_row(row) for row in cur.fetchall()]

.. dropdown:: Task 3.4: Menu-Driven CLI (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Build an interactive command-line interface that lets users explore the database through a menu system. The CLI should demonstrate your repository and service layer in action.

   **Minimum menu options (6 required)**:

   Basic CRUD (2 minimum):

   - Look up an intersection by ID
   - List intersections with pagination

   Complex queries (2 minimum):

   - Show high-incident intersections (multi-table JOIN)
   - Display incident counts by severity (aggregation)

   Geospatial (1 minimum):

   - Find nearby intersections given coordinates and radius

   Analytics (1 minimum):

   - Show system-wide performance metrics

   **Example interaction**:

   .. code-block:: text

      === Traffic Management System ===

      1. Look up intersection by ID
      2. List all intersections (paginated)
      3. Show high-incident intersections
      4. Incident counts by severity
      5. Nearby intersections (geospatial)
      6. System performance metrics
      7. Exit

      Select option: 3

      === High-Incident Intersections (Last 90 Days) ===

      Rank  Intersection            Zone        Incidents  Sensors
      ----  ----------------------  ----------  ---------  -------
      1     Main St & 1st Ave       Downtown    12         4
      2     Oak Blvd & Highway 9    Industrial   9         3
      3     School Rd & Park Ave    School Zone  7         2
      ...

   **File to create**: ``cli/main.py``


Part 4: Testing (Optional)
--------------------------

.. note::

   Testing is **optional** for GP2. If you include tests, they will be considered favorably during grading but are not required. This section is provided for teams that want to practice writing automated tests.

.. dropdown:: Test Suite
   :icon: gear
   :class-container: sd-border-primary

   Write tests using ``pytest`` that verify the behavior of your repositories and services. You are testing that your Python code correctly interacts with the database and returns the expected results.

   **What to test in repositories**:

   - ``find_by_id()`` returns the correct entity for a known ID
   - ``find_by_id()`` returns ``None`` for a non-existent ID
   - ``find_all()`` returns a list respecting ``limit`` and ``offset``
   - ``create()`` inserts a record that can then be retrieved
   - ``update()`` modifies a record and the changes persist
   - ``delete()`` removes a record so it can no longer be found
   - Constraint violations (e.g., duplicate PK, invalid FK) raise appropriate exceptions

   **What to test in services**:

   - Business logic methods return correct results (e.g., ``get_high_incident_intersections()`` returns intersections sorted by incident count)
   - Methods that combine multiple repositories produce the expected combined output
   - Edge cases: empty results, boundary values

   **Running tests**:

   Install the testing packages (if not already in your ``requirements.txt``):

   .. code-block:: bash

      pip install pytest pytest-cov

   Then, from the **project root directory** (the folder containing ``src/`` and ``tests/``), run:

   .. code-block:: bash

      pytest tests/ --cov=src --cov-report=html

   This generates an HTML coverage report in ``htmlcov/`` so you can see which lines are tested (i.e., at least half of the lines in your ``repositories/`` and ``services/`` code are executed by your test suite).

   **Files to create**: ``tests/test_repositories.py`` and ``tests/test_services.py``

   We provide starter versions of both files with test structure, fixtures, and commented-out test cases matching the application architecture described above. Download them here:

   - :download:`test_repositories.py <test_repositories.py>`
   - :download:`test_services.py <test_services.py>`

   Uncomment and adapt the tests to match your actual class names, method signatures, and data.


Folder Structure
----------------

.. code-block:: text

   GP2_Traffic_Team{X}/
   ├── postgresql/
   │   ├── schema.sql              # DDL with constraints, indexes, triggers
   │   ├── data.sql                # Generated sample data
   │   └── queries.sql             # 8+ documented queries
   ├── src/
   │   ├── config/
   │   │   └── database.py         # Connection pooling
   │   ├── models/
   │   │   └── [entity].py         # Dataclasses
   │   ├── repositories/
   │   │   ├── base_repository.py
   │   │   └── [entity]_repo.py    # CRUD + custom queries
   │   ├── services/
   │   │   └── traffic_service.py  # Business logic
   │   └── cli/
   │       └── main.py             # Menu-driven interface
   ├── tests/                      # Optional
   │   ├── test_repositories.py
   │   └── test_services.py
   ├── requirements.txt
   ├── .env.example
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **requirements.txt**

   List all Python packages needed to run your application. At minimum this includes ``psycopg2-binary`` and ``python-dotenv``. Include ``pytest`` and ``pytest-cov`` if you are writing tests.

   **.env.example**

   A template showing the environment variables your application needs, with placeholder values. Teammates and graders copy this to ``.env`` and fill in their own database credentials.

   .. warning::

      **Never commit your real ``.env`` file to Git.** It contains your database password. Add ``.env`` to your ``.gitignore`` file to prevent accidentally pushing credentials to GitHub. Only ``.env.example`` (with placeholder values) should be in version control.

   .. code-block:: text

      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=traffic_management
      DB_USER=postgres
      DB_PASSWORD=your_password_here

   **README.md**

   Setup and usage instructions. Include: prerequisites (Python 3, PostgreSQL with PostGIS), how to create the database and load the schema/data, how to configure ``.env``, how to install dependencies (``pip install -r requirements.txt``), how to run the application, and how to run tests (if applicable).

   **team_contributions.md**

   List each team member's name, the tasks they completed, hours contributed, and contribution percentage. Percentages must sum to 100%.


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP2_Traffic_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP2_Traffic_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **SQL Files**:

   - [ ] ``schema.sql`` creates all tables, constraints, indexes, triggers
   - [ ] ``schema.sql`` includes PostGIS extension and geography columns
   - [ ] ``data.sql`` meets minimum volume requirements and loads without constraint violations
   - [ ] ``queries.sql`` contains 8+ queries with documentation headers

   **Python Application**:

   - [ ] Application runs from command line without errors
   - [ ] Connection pooling implemented with context manager
   - [ ] Repository pattern with CRUD for major entities
   - [ ] Service layer with business logic
   - [ ] 6+ menu options working in CLI

   **Documentation**:

   - [ ] README.md with setup and usage instructions
   - [ ] .env.example with placeholder values
   - [ ] requirements.txt with all dependencies
   - [ ] team_contributions.md


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 10 55
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Schema**
     - 3
     - Complete DDL (1pt); proper constraints and indexes (1pt); PostGIS integration with triggers and ENUMs (1pt)
   * - **Part 1: Sample Data**
     - 2
     - Meets volume requirements (1pt); realistic patterns, constraint-clean, and verified (1pt)
   * - **Part 2: SQL Queries**
     - 5
     - 8+ queries covering all categories (2pts); correct results (1.5pts); query documentation (1.5pts)
   * - **Part 3: Python Application**
     - 3
     - Clean layered architecture (1pt); repository pattern with CRUD (1pt); error handling and connection pooling (1pt)
   * - **Part 3: CLI Interface**
     - 2
     - 6+ working menu options (1pt); clear output formatting and input validation (1pt)
   * - **Total**
     - **15**
     -


Tips for Success
----------------

.. tip::

   - **Start with the schema**: Get your database working and data loaded before touching Python. A solid schema prevents headaches later.
   - **Test queries in psql first**: Write and debug SQL interactively before embedding in Python code.
   - **Layer your application**: Keep database logic in repositories, business logic in services, and user interaction in the CLI. This separation makes testing much easier.
   - **Use office hours**: Bring your schema for review. Ask about query optimization strategies.
