====================================================
Exercises
====================================================

This page contains exercises for Lecture 7. These exercises are designed to
reinforce your understanding of DML statements (``INSERT``, ``UPDATE``,
``DELETE``), the ``RETURNING`` clause, ``ON CONFLICT`` upsert patterns,
explicit transactions (``BEGIN`` / ``COMMIT`` / ``ROLLBACK`` / ``SAVEPOINT``),
and Python integration via psycopg3.

All exercises use the ``university_db`` schema from the lecture demos.
Open ``demo_sql/sql_demo.sql`` in DataGrip and run the Schema Setup section
before starting. Exercises 3 and 4 require a working Python environment with
psycopg3 installed.


.. dropdown:: Exercise 1 -- DML Sequence Predictor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build intuition for ``RETURNING``, ``ON CONFLICT``, and referential
    action behavior by predicting the outcome of a precisely ordered
    sequence of DML statements before running them.


    **Specification**

    Run the following setup, then predict the outcome of each labelled
    statement **before** running it in DataGrip.

    .. code-block:: sql

       -- Setup
       CREATE TABLE department (
           dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
           dept_name VARCHAR(100) NOT NULL UNIQUE
       );

       CREATE TABLE person (
           person_id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
           first_name    VARCHAR(100) NOT NULL,
           last_name     VARCHAR(100) NOT NULL,
           date_of_birth DATE NOT NULL
       );

       CREATE TABLE student (
           person_id         INTEGER PRIMARY KEY,
           student_id        VARCHAR(20) NOT NULL UNIQUE,
           academic_standing VARCHAR(30) NOT NULL
               CONSTRAINT chk_standing CHECK (academic_standing IN
                   ('Good Standing', 'Probation', 'Suspended', 'Dismissed')),
           gpa               NUMERIC(3,2),
           CONSTRAINT fk_student_person
               FOREIGN KEY (person_id) REFERENCES person (person_id)
               ON DELETE CASCADE
       );

       CREATE TABLE enrollment (
           student_person_id INTEGER NOT NULL,
           course_id         VARCHAR(10) NOT NULL,
           section_no        VARCHAR(10) NOT NULL,
           grade             CHAR(2),
           PRIMARY KEY (student_person_id, course_id, section_no),
           CONSTRAINT fk_enr_student
               FOREIGN KEY (student_person_id) REFERENCES student (person_id)
               ON DELETE CASCADE
       );

       INSERT INTO department (dept_name)
           VALUES ('Computer Science'), ('Mathematics');

       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Alice', 'Johnson', '1998-04-12'),
                  ('Bob',   'Smith',   '1999-06-01');

       INSERT INTO student (person_id, student_id, academic_standing, gpa)
           VALUES (1, '117453210', 'Good Standing', 3.75),
                  (2, '117453211', 'Probation',     1.85);

    **Statements to predict:**

    .. code-block:: sql

       -- A
       INSERT INTO student (person_id, student_id, academic_standing)
           VALUES (99, '117453299', 'Good Standing');

       -- B
       INSERT INTO student (person_id, student_id, academic_standing, gpa)
           VALUES (1, '117453299', 'Good Standing', 5.00);

       -- C
       UPDATE student SET gpa = 2.10 WHERE person_id = 2
       RETURNING person_id, gpa, academic_standing;

       -- D
       UPDATE student SET academic_standing = 'Expelled';

       -- E
       INSERT INTO department (dept_name)
           VALUES ('Computer Science')
           ON CONFLICT DO NOTHING;

       -- F
       INSERT INTO department (dept_name)
           VALUES ('Computer Science')
           ON CONFLICT (dept_name) DO UPDATE
               SET dept_name = EXCLUDED.dept_name || ' (updated)';

       -- G
       DELETE FROM person WHERE person_id = 1;
       SELECT * FROM student WHERE person_id = 1;

       -- H
       INSERT INTO enrollment (student_person_id, course_id, section_no)
           VALUES (2, 'ENPM818T', '0101');
       DELETE FROM student WHERE person_id = 2;
       SELECT * FROM enrollment WHERE student_person_id = 2;

    **Tasks**

    1. For each statement A through H (treating each multi-line block as one
       unit), predict **SUCCEED** or **FAIL**. For each FAIL, name the
       constraint or rule that fires. For each SUCCEED, describe what the
       database state looks like after the statement.

    2. Statement D succeeds but produces a result you probably do not want.
       What happened, and how would you prevent it in a production workflow?

    3. Statement G succeeds. What does the ``SELECT`` return and why?

    4. In statement H, the ``DELETE`` succeeds even though an enrollment row
       references student 2. Explain the mechanism that allows this.

    .. tip::

       Run statements A through H in order. Some later statements depend on
       the state left by earlier ones. Wrap statement D in
       ``BEGIN`` / ``ROLLBACK`` so you can observe the damage without keeping
       it.


    **Deliverables**

    - Prediction table: statement, SUCCEED/FAIL, constraint name or state
      description for each
    - Explanation for statement D behavior and prevention
    - Explanation of the ``SELECT`` result after G
    - Explanation of the cascade mechanism in H


.. dropdown:: Exercise 2 -- Transaction Repair Workshop
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Diagnose why three multi-statement operations fail or produce wrong
    results, then fix each one using the appropriate transaction control
    tool (``BEGIN`` / ``COMMIT``, ``ROLLBACK``, ``SAVEPOINT``, or
    ``ON CONFLICT``).


    **Specification**

    Each scenario below contains a realistic mistake. Reproduce each
    problem in DataGrip, diagnose it, and write the corrected version.

    **Scenario A -- Half-committed enrollment**

    The following script is supposed to enroll student 1 in two courses
    atomically. If either insert fails, neither should be committed.

    .. code-block:: sql

       -- Broken version: two standalone statements
       UPDATE course_section SET capacity = capacity - 1
           WHERE course_id = 'ENPM818T' AND section_no = '0101';

       INSERT INTO enrollment (student_person_id, course_id, section_no)
           VALUES (1, 'ENPM818T', '0101');

       UPDATE course_section SET capacity = capacity - 1
           WHERE course_id = 'ENPM605' AND section_no = '0101';

       INSERT INTO enrollment (student_person_id, course_id, section_no)
           VALUES (999, 'ENPM605', '0101');  -- FK violation: person 999 doesn't exist

    Observe that after the FK error, the first ``UPDATE`` and ``INSERT``
    are already committed and cannot be rolled back.

    **Scenario B -- Batch seed with one bad row**

    You are seeding five person rows but the third one has a duplicate
    last name / date-of-birth combination that violates a ``UNIQUE``
    constraint. You want the other four rows to be inserted; only the
    bad one should be skipped.

    .. code-block:: sql

       -- Broken version: one error aborts everything
       BEGIN;
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Carol',  'Davis',   '2000-03-22');
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('David',  'Lee',     '2001-07-14');
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Alice',  'Johnson', '1998-04-12');  -- Duplicate (already exists)
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Eve',    'Brown',   '2002-11-03');
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Frank',  'Miller',  '1997-05-29');
       COMMIT;

    (Assumes Alice Johnson 1998-04-12 was already inserted in Exercise 1.)
    Observe that the duplicate error aborts the entire transaction; Carol,
    David, Eve, and Frank are not inserted.

    **Scenario C -- Forgotten commit in Python**

    The following Python function inserts a department and returns its
    generated ID, but callers never see the row in the database.

    .. code-block:: python

       import psycopg, os
       from dotenv import load_dotenv
       load_dotenv()

       def add_department(name: str) -> int:
           conn_str = (
               f"host={os.getenv('DB_HOST','localhost')} "
               f"port={os.getenv('DB_PORT','5432')} "
               f"dbname={os.getenv('DB_NAME')} "
               f"user={os.getenv('DB_USER')} "
               f"password={os.getenv('DB_PASSWORD')}"
           )
           conn = psycopg.connect(conn_str)
           cur = conn.cursor()
           cur.execute(
               "INSERT INTO department (dept_name) VALUES (%s) RETURNING dept_id",
               (name,)
           )
           row = cur.fetchone()
           conn.close()
           return row[0]

       dept_id = add_department('Physics')
       print(dept_id)   # prints an ID, but the row never appears in psql

    **Tasks**

    1. **Scenario A**: Rewrite the broken script so that all four statements
       (two updates + two inserts) are wrapped in a single
       ``BEGIN`` / ``COMMIT`` block. The entire block should roll back
       atomically when the FK violation fires.

    2. **Scenario B**: Rewrite the batch insert so that rows 1, 2, 4, and 5
       are inserted even if row 3 fails. Use ``SAVEPOINT`` after each
       successful insert so that a failure can be rolled back to the last
       good state. Confirm exactly four rows are committed.

       *Alternatively*: show how ``ON CONFLICT DO NOTHING`` could be used
       to achieve the same result in a single multi-row ``INSERT`` with no
       savepoint management required.

    3. **Scenario C**: Identify the bug and fix the function. Rewrite it
       to use ``with psycopg.connect(...) as conn`` and
       ``conn.transaction()`` so the commit is guaranteed even if an
       exception is raised.

    .. note::

       Scenario B has two valid fixes: the ``SAVEPOINT`` approach gives you
       per-row error handling and logging; the ``ON CONFLICT DO NOTHING``
       approach is simpler and correct when you do not need to know which
       rows were skipped. Implement at least one; implement both for full
       marks.


    **Deliverables**

    - Fixed SQL for Scenario A with explanation
    - Fixed SQL for Scenario B (SAVEPOINT version and/or ON CONFLICT version) with explanation
    - Fixed Python function for Scenario C with explanation of the original bug


.. dropdown:: Exercise 3 -- psycopg3 Repository Implementation
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build a working five-layer Python application for the university schema,
    implementing the repository pattern from the lecture. This exercise
    maps directly to the GP2 deliverables.


    **Specification**

    Create the ``university_app`` project structure shown in the lecture:

    .. code-block:: text

       university_app/
       |-- .env                        (credentials; gitignored)
       |-- .gitignore
       |-- requirements.txt            (psycopg[binary], psycopg-pool, python-dotenv)
       |-- main.py
       |-- config/
       |   `-- database.py
       |-- models/
       |   |-- person.py
       |   `-- student.py
       |-- repositories/
       |   |-- person_repo.py
       |   `-- student_repo.py
       |-- services/
       |   `-- student_service.py
       `-- cli/
           `-- menu.py

    **Tasks**

    1. **Config layer** -- Implement ``DatabaseConfig`` in
       ``config/database.py`` exactly as shown in the lecture, with
       ``_conninfo()``, ``initialize()``, ``get_connection()``, and
       ``close()`` methods. Verify by running:

       .. code-block:: python

          from config.database import DatabaseConfig
          DatabaseConfig.initialize()
          with DatabaseConfig.get_connection() as conn:
              with conn.cursor() as cur:
                  cur.execute("SELECT version()")
                  print(cur.fetchone()[0])
          DatabaseConfig.close()

    2. **Models layer** -- Implement ``@dataclass Person`` in
       ``models/person.py`` with fields ``person_id``, ``first_name``,
       ``last_name``, and ``date_of_birth``. Implement ``@dataclass Student``
       in ``models/student.py`` with fields ``person_id``, ``student_id``,
       ``academic_standing``, and ``gpa: float | None = None``. Field names
       must match database column names exactly.

    3. **Repository layer** -- Implement the following methods using
       ``dict_row`` and parameterized queries throughout:

       In ``PersonRepository``:

       - ``find_by_id(person_id: int) -> dict | None``
       - ``find_all() -> list[dict]``
       - ``create(first_name, last_name, date_of_birth) -> int``
         (returns the generated ``person_id`` via ``RETURNING``)
       - ``delete(person_id: int) -> bool``
         (returns ``True`` if a row was deleted)

       In ``StudentRepository``:

       - ``find_by_id(person_id: int) -> dict | None``
       - ``find_by_standing(standing: str) -> list[dict]``
       - ``update_standing(person_id: int, new_standing: str) -> bool``

    4. **Service layer** -- Implement ``StudentService`` in
       ``services/student_service.py`` with:

       - ``register_student(first_name, last_name, date_of_birth, student_id, gpa) -> int``:
         inserts into ``person`` (capturing the returned ``person_id``) and
         then inserts into ``student``, wrapped in ``conn.transaction()``.
         Raises ``ValueError`` for ``ForeignKeyViolation`` or
         ``UniqueViolation``.
       - ``place_on_probation(min_gpa: float) -> list[dict]``:
         updates ``academic_standing`` to ``'Probation'`` for all students
         with ``gpa < min_gpa`` and returns the affected rows via
         ``RETURNING``.

    5. **CLI layer** -- Implement a ``main()`` loop in ``cli/menu.py`` with
       at least these four options:

       - **1 -- Register student**: prompts for name, DOB, student ID, GPA;
         calls ``StudentService.register_student()``; prints the new
         person ID or an error message.
       - **2 -- Find student by ID**: prompts for person ID; prints all
         fields or "Not found".
       - **3 -- List students on probation**: calls
         ``StudentRepository.find_by_standing('Probation')``; prints a
         formatted table.
       - **4 -- Place on probation**: prompts for minimum GPA threshold;
         calls ``StudentService.place_on_probation()``; prints the count
         of affected students.
       - **0 -- Exit**: calls ``DatabaseConfig.close()`` and exits.

    .. important::

       **Layer rules** (violations result in deductions):

       - ``cli/`` must contain no ``cur.execute()`` calls.
       - ``services/`` must contain no ``input()`` calls.
       - ``repositories/`` must contain no business logic (no ``if gpa < x``).
       - ``models/`` must contain no ``import psycopg``.

    .. tip::

       Test each layer in isolation before wiring the CLI. Start with
       ``config/``, then ``models/``, then each repository method, then the
       service, and finally the CLI. Add a ``standalone_connection_test.py``
       script to verify connectivity before writing any layer code.


    **Deliverables**

    - Complete project directory with all five layers implemented
    - Each repository method tested with at least one success and one
      edge-case call (e.g., ``find_by_id`` with a non-existent ID)
    - ``register_student`` tested with a valid insert and a duplicate
      ``student_id`` (should raise ``ValueError``, not crash)
    - Working CLI that exercises all four menu options


.. dropdown:: Exercise 4 -- Isolation and Concurrency Lab
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Reproduce the lost-update anomaly with two concurrent DataGrip
    connections, then prevent it with ``SELECT ... FOR UPDATE``, and
    finally observe a phantom read under ``READ COMMITTED`` and prevent it
    with ``REPEATABLE READ``.


    **Specification**

    This exercise requires two simultaneous query consoles in DataGrip,
    both connected to ``university_db``. Label them **Session A** and
    **Session B** in your answer.

    **Part 1 -- Lost Update (READ COMMITTED)**

    Set up a ``course_section`` row with ``capacity = 2``:

    .. code-block:: sql

       INSERT INTO course_section (course_id, section_no, capacity)
           VALUES ('ENPM999', 'TEST', 2)
           ON CONFLICT DO NOTHING;

    Now reproduce the lost update by running the steps below in order,
    switching between sessions as indicated. Execute each step before
    moving to the next.

    .. list-table::
       :widths: 10 15 75
       :header-rows: 1
       :class: compact-table

       * - **Step**
         - **Session**
         - **SQL**
       * - 1
         - A
         - ``BEGIN;``
       * - 2
         - B
         - ``BEGIN;``
       * - 3
         - A
         - ``SELECT capacity FROM course_section WHERE course_id = 'ENPM999' AND section_no = 'TEST';``
       * - 4
         - B
         - ``SELECT capacity FROM course_section WHERE course_id = 'ENPM999' AND section_no = 'TEST';``
       * - 5
         - A
         - ``UPDATE course_section SET capacity = capacity - 1 WHERE course_id = 'ENPM999' AND section_no = 'TEST'; INSERT INTO enrollment (student_person_id, course_id, section_no) VALUES (1, 'ENPM999', 'TEST');``
       * - 6
         - A
         - ``COMMIT;``
       * - 7
         - B
         - ``UPDATE course_section SET capacity = capacity - 1 WHERE course_id = 'ENPM999' AND section_no = 'TEST'; INSERT INTO enrollment (student_person_id, course_id, section_no) VALUES (2, 'ENPM999', 'TEST');``
       * - 8
         - B
         - ``COMMIT;``

    After step 8, check the final ``capacity`` value. Record what you see.

    **Part 2 -- Preventing the Lost Update with FOR UPDATE**

    Reset the section capacity to 2 and clear the enrollment rows. Repeat
    the experiment, but this time Session A's read at Step 3 uses
    ``SELECT ... FOR UPDATE``. Observe when Session B blocks and what value
    it reads at Step 4 when it unblocks.

    **Part 3 -- Phantom Read**

    .. code-block:: sql

       -- Session A
       BEGIN;
       SELECT COUNT(*) FROM student WHERE gpa > 3.5;  -- note the count

       -- Session B (while A is still open)
       -- Insert a new high-GPA student via register_student() or directly
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Zara', 'Khan', '2001-09-15') RETURNING person_id;
       INSERT INTO student (person_id, student_id, academic_standing, gpa)
           VALUES (<returned_id>, '117999999', 'Good Standing', 3.90);
       -- Session B auto-commits (standalone statements)

       -- Session A (still in the same transaction)
       SELECT COUNT(*) FROM student WHERE gpa > 3.5;  -- compare to the first count
       COMMIT;

    Repeat the same experiment with Session A opening with
    ``BEGIN ISOLATION LEVEL REPEATABLE READ`` instead. Record both counts
    for each isolation level.

    **Tasks**

    1. **Part 1**: Record the final ``capacity`` value after both commits.
       Explain why the value is wrong, naming the anomaly.

    2. **Part 2**: Describe exactly what happens to Session B at Step 4
       when Session A holds a ``FOR UPDATE`` lock. What value does Session B
       read when it unblocks, and why is this correct?

    3. **Part 3**: Record the ``COUNT(*)`` results for both ``READ COMMITTED``
       and ``REPEATABLE READ``. Explain the difference in terms of snapshot
       timing.

    4. Write the ``BEGIN ... COMMIT`` block that Session A should use in a
       production enrollment system (incorporating ``FOR UPDATE``) to
       prevent the anomaly from Part 1.

    .. note::

       For Part 2, you may need to wait a few seconds after Session A issues
       ``SELECT ... FOR UPDATE`` before opening Session B. If Session B appears
       to hang indefinitely, that is the expected blocking behavior -- run
       ``COMMIT`` in Session A to unblock it.


    **Deliverables**

    - Part 1: final capacity value and anomaly explanation
    - Part 2: description of blocking behavior and corrected capacity value
    - Part 3: COUNT results table for both isolation levels with explanation
    - Part 4: corrected ``BEGIN ... COMMIT`` block with ``FOR UPDATE``
