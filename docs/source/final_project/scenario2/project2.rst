====================================================
Group Project 2: PostgreSQL + Python Integration
====================================================

Overview
--------

Implement your GP1 design in PostgreSQL, generate realistic synthetic data, write SQL queries supporting clinical and administrative operations, and build a Python command-line application with a menu-driven interface.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 3 weeks |
   **Weight**: 15 points (30% of final project) |
   **Team Size**: 4 students

**Builds on**: Your GP1 relational design


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Translate healthcare designs into physical PostgreSQL schemas
- Write DDL with tables, constraints, indexes, and triggers
- Generate and validate synthetic healthcare data
- Write clinical, financial, and operational SQL queries
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

   - **Database setup**: Extensions
   - **Custom types**: ENUMs for constrained healthcare values (appointment status, claim status, priority levels, etc.)
   - **All tables**: Complete with all columns from GP1
   - **Primary keys**: All defined correctly
   - **Foreign keys**: With ON DELETE/UPDATE rules
   - **Check constraints**: Business rules from your GP1 entity catalog
   - **NOT NULL constraints**: All mandatory fields
   - **UNIQUE constraints**: All candidate keys (MRN, NPI, etc.)
   - **Indexes**: Strategic indexes for clinical query patterns
   - **Triggers**: Automatic ``updated_at`` timestamps

   **Healthcare Identifier Constraints**:

   .. code-block:: sql

      -- MRN format: 10-digit zero-padded
      ALTER TABLE patient
      ADD CONSTRAINT chk_mrn_format
      CHECK (mrn ~ '^\d{10}$');

      -- NPI format: 10-digit
      ALTER TABLE provider
      ADD CONSTRAINT chk_npi_format
      CHECK (npi ~ '^\d{10}$');

      -- DEA required for controlled substance prescriptions
      ALTER TABLE prescription
      ADD CONSTRAINT chk_dea_for_controlled
      CHECK (
          controlled_substance_schedule IS NULL
          OR prescriber_dea_number IS NOT NULL
      );

   **File to create**: ``postgresql/schema.sql``

.. dropdown:: Task 1.2: Synthetic Data Generation (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Create ``data.sql`` with **synthetic data only** (NEVER real patient data!).

   **Minimum data volumes**:

   - 100+ patients across the network
   - 30+ providers (physicians, nurses, specialists)
   - 200+ appointments (various statuses and types)
   - 150+ prescriptions (including controlled substances)
   - 100+ lab orders with 200+ lab results
   - 30+ hospital admissions with discharge info
   - 50+ insurance claims (various lifecycle stages)
   - 30+ medications in formulary
   - 5 hospitals and 10+ clinic locations

   .. note::

      **Data Generation with LLMs**

      You may use an LLM (such as ChatGPT or Claude) to generate your INSERT statements. Provide your ``schema.sql`` to the LLM and ask it to generate realistic synthetic data that respects all constraints. See the :doc:`data_generation_guide` for a ready-to-use prompt.

   **Data Quality Checks** (run after loading):

   .. code-block:: text

      After loading data, verify:

      1. All FK references resolve (no orphan records)
      2. All CHECK constraints pass
      3. MRN, NPI, DEA formats are consistent
      4. Temporal data spans at least 6 months
      5. Controlled substance prescriptions have DEA numbers
      6. Lab results include reference ranges and abnormal flags

   **File to create**: ``postgresql/data.sql``


Part 2: Clinical SQL Queries
-----------------------------

**Objective**: Write 8+ queries demonstrating clinical, financial, and operational mastery.

.. dropdown:: Clinical Queries (3 minimum)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Patient Care Coordination**:

   *"For a patient arriving for an appointment, show demographics, active medications, and recent lab results."*

   **Medication Safety**:

   *"Find all patients with 5+ active prescriptions (polypharmacy risk) along with their prescribing providers."*

   **Quality Metrics**:

   *"Calculate 30-day readmission rates by diagnosis, identifying patients readmitted within 30 days of discharge."*

.. dropdown:: Financial Queries (2 minimum)
   :icon: gear
   :class-container: sd-border-primary

   **Claim Denials**:

   *"Show claim denial rates by insurance company and denial reason, with total denied amounts."*

   **Outstanding Balances**:

   *"Generate an aging report showing outstanding patient balances in 30/60/90/120+ day buckets."*

.. dropdown:: Operational Queries (3 minimum)
   :icon: gear
   :class-container: sd-border-primary

   **Provider Productivity**:

   *"Show appointment counts, no-show rates, and average patients per day by provider."*

   **Controlled Substances**:

   *"Report all Schedule II controlled substance prescriptions by provider, required for DEA reporting."*

   **Capacity Planning**:

   *"Show average length of stay and bed occupancy rates by hospital and admission type over the past 90 days."*

.. dropdown:: Query Documentation Format
   :icon: gear
   :class-container: sd-border-primary

   Use this format for **every query** in ``queries.sql``:

   .. code-block:: sql

      -- Query #X: [Title]
      -- Clinical/Financial/Operational Context: [Why this matters]
      -- Tables Used: [List all tables]
      -- Complexity Features: [JOINs, aggregates, subqueries used]

      [YOUR SQL QUERY]

      -- Expected Output: [Description of result columns]
      -- Sample Results: [First 3 rows with synthetic data]

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

      healthcare-management/
      ├── requirements.txt
      ├── .env.example
      ├── config/
      │   └── database.py          # Connection pooling
      ├── models/
      │   ├── patient.py           # Dataclasses
      │   └── [other models].py
      ├── repositories/
      │   ├── base_repository.py
      │   ├── patient_repo.py      # CRUD operations
      │   └── [other repos].py
      ├── services/
      │   ├── patient_service.py   # Business logic
      │   └── [other services].py
      └── cli/
          └── main.py              # Menu-driven interface

   **Layer Responsibilities**:

   - **config/**: Database connection pooling with psycopg2. Configuration loaded from environment variables.
   - **models/**: Python dataclasses representing each entity. Each dataclass mirrors a database table and includes a ``from_row()`` class method to convert query results into objects.
   - **repositories/**: CRUD operations and custom queries for each entity. Each repository handles its own SQL and returns model objects. Repositories do not contain business logic.
   - **services/**: Business logic combining multiple repositories. For example, a ``patient_service.get_patient_dashboard(id)`` method might call the patient repository, prescription repository, and lab repository to assemble a complete view.
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
                      dbname=os.getenv("DB_NAME", "healthcare_management"),
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
   - Custom query methods (e.g., ``find_active_prescriptions(patient_id)``)

   **Example**:

   .. code-block:: python

      class PatientRepository:
          def find_by_id(self, patient_id):
              with DatabaseConfig.get_connection() as conn:
                  with conn.cursor() as cur:
                      cur.execute(
                          "SELECT * FROM patient WHERE patient_id = %s",
                          (patient_id,)
                      )
                      row = cur.fetchone()
                      return Patient.from_row(row) if row else None

          def find_all(self, limit=20, offset=0):
              with DatabaseConfig.get_connection() as conn:
                  with conn.cursor() as cur:
                      cur.execute(
                          "SELECT * FROM patient ORDER BY patient_id "
                          "LIMIT %s OFFSET %s",
                          (limit, offset)
                      )
                      return [Patient.from_row(row) for row in cur.fetchall()]

.. dropdown:: Task 3.4: Menu-Driven CLI (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Build an interactive command-line interface that lets users explore the database through a menu system. The CLI should demonstrate your repository and service layer in action.

   **Minimum menu options (6 required)**:

   Clinical (2 minimum):

   - Look up patient by MRN
   - View active medications for a patient

   Financial (2 minimum):

   - Show claim denial analytics
   - Display accounts receivable aging report

   Operational (1 minimum):

   - Show provider productivity metrics

   Analytics (1 minimum):

   - Show system-wide performance dashboard

   **Example interaction**:

   .. code-block:: text

      === Healthcare Management System ===

      1. Look up patient by MRN
      2. View active medications
      3. Claim denial analytics
      4. Accounts receivable aging
      5. Provider productivity
      6. System dashboard
      7. Exit

      Select option: 1

      Enter MRN: 0000000042

      === Patient Record ===

      Name:       Jane Smith
      MRN:        0000000042
      DOB:        1985-03-15
      Provider:   Dr. Robert Chen (Cardiology)
      Insurance:  BlueCross PPO (Policy: BC-2024-1234)
      ...

   **File to create**: ``cli/main.py``


Part 4: Testing (Optional)
---------------------------

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
   - Constraint violations (e.g., duplicate MRN, invalid FK) raise appropriate exceptions

   **What to test in services**:

   - Business logic methods return correct results (e.g., ``get_polypharmacy_patients()`` returns patients sorted by prescription count)
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

   GP2_Healthcare_Team{X}/
   ├── postgresql/
   │   ├── schema.sql              # DDL with constraints, indexes, triggers
   │   ├── data.sql                # Generated synthetic data
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
   │   │   └── patient_service.py  # Business logic
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
      DB_NAME=healthcare_management
      DB_USER=postgres
      DB_PASSWORD=your_password_here

   **README.md**

   Setup and usage instructions. Include: prerequisites (Python 3, PostgreSQL), how to create the database and load the schema/data, how to configure ``.env``, how to install dependencies (``pip install -r requirements.txt``), how to run the application, and how to run tests (if applicable).

   **team_contributions.md**

   List each team member's name, the tasks they completed, hours contributed, and contribution percentage. Percentages must sum to 100%.


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP2_Healthcare_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP2_Healthcare_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **SQL Files**:

   - [ ] ``schema.sql`` creates all tables, constraints, indexes, triggers
   - [ ] ``schema.sql`` includes healthcare identifier constraints (MRN, NPI, DEA)
   - [ ] ``data.sql`` contains ONLY synthetic data (no real patient data!)
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
     - Complete DDL (1pt); proper constraints and indexes (1pt); healthcare identifier constraints with triggers and ENUMs (1pt)
   * - **Part 1: Synthetic Data**
     - 2
     - Meets volume requirements (1pt); realistic clinical patterns, constraint-clean, and verified (1pt)
   * - **Part 2: SQL Queries**
     - 5
     - 8+ queries across clinical/financial/operational (2pts); correct results (1.5pts); query documentation (1.5pts)
   * - **Part 3: Python Application**
     - 3
     - Clean layered architecture (1pt); repository pattern with CRUD (1pt); error handling and connection pooling (1pt)
   * - **Part 3: CLI Interface**
     - 2
     - 6+ working menu options (1pt); clear output formatting and input validation (1pt)
   * - **Total**
     - **15**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Using real patient data (NEVER; always use synthetic data)
   - Hardcoded credentials (use .env files, never commit passwords)
   - Missing healthcare identifier constraints (MRN uniqueness, DEA for controlled substances)
   - Clinical queries without context (each query needs clinical/business justification)
   - Forgetting triggers (``updated_at`` timestamps should be automatic)


Tips for Success
----------------

.. tip::

   - **Start with the schema**: Get your database working and data loaded before touching Python. A solid schema prevents headaches later.
   - **Test queries in psql first**: Write and debug SQL interactively before embedding in Python code.
   - **Think like a clinician**: For each query, ask "Why would a doctor or billing staff need this?"
   - **Layer your application**: Keep database logic in repositories, business logic in services, and user interaction in the CLI. This separation makes testing much easier.
   - **Use office hours**: Bring your schema for review. Ask about query optimization strategies.
