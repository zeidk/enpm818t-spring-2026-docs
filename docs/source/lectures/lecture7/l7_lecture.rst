====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Prerequisites
====================================================

Before writing any DML, complete these setup steps.


.. dropdown:: Four Steps Before Writing Any DML
   :class-container: sd-border-secondary
   :open:

   1. **Clone or pull the**
      `GitHub repository <https://github.com/zeidk/enpm818t-spring-2026-code>`__.

   2. **Database.** ``university_db`` must already exist from L6. If not,
      create it:

      .. code-block:: sql

         CREATE DATABASE university_db;

   3. **DataGrip console.** Verify the **database dropdown** shows
      ``university_db``. Every DML statement lands in whichever database
      that dropdown shows.

   4. **Schema.** Open ``demo_sql/sql_demo.sql`` and run the **Schema
      Setup** section at the top -- it drops and recreates all tables with
      seed data (up to line 250).


DML: INSERT, UPDATE, DELETE
====================================================

DDL built the schema. DML populates and modifies it.

Three questions to keep in mind as you work through this section:

- How do you insert a row and immediately get its generated primary key back?
- How do you update rows without accidentally overwriting the entire table?
- How does ``ON DELETE CASCADE`` from L6 play out in a real delete?

Every DML statement targets exactly one table and affects zero or more rows.
By default PostgreSQL runs each statement in its own implicit transaction
(*autocommit mode*). Section 2 covers explicit transactions.


.. dropdown:: SQL Sublanguages -- DML and TCL Focus
   :class-container: sd-border-secondary

   .. rubric:: What This Lecture Covers

   .. list-table::
      :widths: 28 12 28 32
      :header-rows: 1
      :class: compact-table

      * - **Sublanguage**
        - **Abbrev.**
        - **Purpose**
        - **Key Commands**
      * - Data Definition Language
        - DDL
        - Define and modify structure
        - ``CREATE``, ``ALTER``, ``DROP``
      * - **Data Manipulation Language**
        - **DML**
        - **Insert, update, delete rows**
        - ``INSERT``, ``UPDATE``, ``DELETE``
      * - Data Query Language
        - DQL
        - Retrieve rows
        - ``SELECT``
      * - Data Control Language
        - DCL
        - Manage permissions
        - ``GRANT``, ``REVOKE``
      * - **Transaction Control Language**
        - **TCL**
        - **Control transactions**
        - ``BEGIN``, ``COMMIT``, ``ROLLBACK``

   DML and TCL are the focus of this lecture (bold rows). DDL was covered
   in L6. DQL (``SELECT`` in depth) is covered in L8.


.. dropdown:: SELECT: What You Need Today
   :class-container: sd-border-secondary

   .. rubric:: Five Forms Used Throughout This Lecture

   ``SELECT`` is covered in full depth in L8. The five forms below are the
   only ones needed to follow today's demos and exercises.

   **Form 1: All rows, all columns**

   .. code-block:: sql

      SELECT * FROM student;
      SELECT * FROM department;

   The ``*`` wildcard returns every column and every row. Useful during
   development to inspect the full table state. Avoid ``*`` in production
   code: if a column is added later, the result set changes silently and
   can break application logic.

   **Form 2: Specific columns**

   .. code-block:: sql

      SELECT person_id, gpa, academic_standing
      FROM student;

   Only the named columns are returned. Reduces data transferred from the
   server and makes queries self-documenting.

   **Form 3: Filter with WHERE**

   .. code-block:: sql

      SELECT person_id, gpa
      FROM student
      WHERE gpa < 2.0;

      SELECT person_id, academic_standing
      FROM student
      WHERE academic_standing = 'Probation';

   ``WHERE`` filters rows before they are returned. The condition can use
   ``=``, ``<``, ``>``, ``<=``, ``>=``, ``<>`` (not equal), ``AND``,
   ``OR``, ``NOT``. String values must be enclosed in single quotes.
   This is the same ``WHERE`` used in ``UPDATE`` and ``DELETE``.

   **Form 4: Sort with ORDER BY**

   .. code-block:: sql

      SELECT person_id, gpa
      FROM student
      ORDER BY gpa DESC;

      SELECT person_id, gpa
      FROM student
      WHERE gpa < 2.0
      ORDER BY gpa ASC;

   ``ORDER BY col ASC`` sorts smallest to largest (default); ``DESC``
   sorts largest to smallest. Without ``ORDER BY``, PostgreSQL makes no
   guarantee about row order. ``ORDER BY`` is applied after ``WHERE``.
   Multiple columns are supported: ``ORDER BY dept_id ASC, gpa DESC``.

   **Form 5: Count rows**

   .. code-block:: sql

      SELECT COUNT(*) FROM enrollment
      WHERE course_id = 'ENPM818T';

   ``COUNT(*)`` counts every row that passes the ``WHERE`` filter. The
   ``*`` tells ``COUNT`` to count rows regardless of ``NULL`` values.
   ``COUNT(column)`` counts only rows where that column is non-``NULL``.
   Returns a single integer. Used to verify that inserts, updates, and
   deletes affected the expected number of rows.


.. dropdown:: INSERT
   :class-container: sd-border-secondary

   .. rubric:: Adding Rows to a Table

   ``INSERT`` adds one or more rows to a table. Always include the column
   list: omitting it couples your code to the physical column order, which
   can change silently during schema evolution.

   Key concepts:

   - **Single-row**: ``INSERT INTO t (cols) VALUES (...)``
   - **Multi-row**: one ``VALUES`` clause with multiple tuples -- one round
     trip, far faster than N individual inserts
   - ``INSERT ... RETURNING``: get generated values (PK, timestamps) back
     without a second query -- essential for ISA chains
   - ``INSERT ... ON CONFLICT``: upsert -- insert if new, do nothing or
     update if duplicate
   - Identity columns (``GENERATED ALWAYS AS IDENTITY``) must be omitted
     from the column list

   Resources:

   - `PostgreSQL documentation: INSERT <https://www.postgresql.org/docs/current/sql-insert.html>`__

   .. rubric:: Single-Row and Multi-Row INSERT

   .. code-block:: sql

      -- Single-row
      INSERT INTO department (dept_name)
      VALUES ('Computer Science');

      -- Multi-row: preferred for bulk data (4 rows, one round trip)
      INSERT INTO department (dept_name)
      VALUES ('Computer Science'),
             ('Mathematics'),
             ('Mechanical Engineering'),
             ('Electrical Engineering');

   All rows are inserted atomically: all succeed or all fail. Identity
   values are assigned by the engine's sequence, not by the order rows
   appear in ``VALUES``. Always include the column list.

   .. list-table::
      :widths: 20 50
      :header-rows: 1
      :class: compact-table

      * - ``dept_id``
        - ``dept_name``
      * - 1
        - Computer Science
      * - 2
        - Mathematics
      * - 3
        - Mechanical Engineering
      * - 4
        - Electrical Engineering

   .. rubric:: The Generated PK Problem

   When you insert a row whose primary key is generated by the engine, how
   do you get that value back to use in a subtype insert?

   .. code-block:: sql

      INSERT INTO person (first_name, last_name, date_of_birth)
      VALUES ('Alice', 'Johnson', '1998-04-12');
      /* person_id was generated by the engine -- what value did it assign? */

      /* Attempt 1: guess */
      INSERT INTO student (person_id, ...) VALUES (1, ...);
      /* Breaks silently if another session inserted a row at the same time */

      /* Attempt 2: SELECT MAX(person_id) */
      SELECT MAX(person_id) FROM person;
      /* Still NOT safe: another session may insert between your INSERT
         and your SELECT, returning the wrong ID */

   The engine assigns the identity value; your code never sees it directly.
   Guessing or using ``MAX()`` introduces a race condition under concurrent
   inserts.

   .. rubric:: The Solution: RETURNING

   ``RETURNING`` appended to any ``INSERT``, ``UPDATE``, or ``DELETE``
   causes the engine to return the specified columns from the rows it just
   wrote. The value is captured atomically: no other session can interfere
   between the write and the read.

   .. code-block:: sql

      INSERT INTO person (first_name, last_name, date_of_birth)
      VALUES ('Alice', 'Johnson', '1998-04-12')
      RETURNING person_id;
      /* Result set: person_id = 1 -- one row, one column, exact value */

      INSERT INTO student (person_id, student_id, admission_date,
                           academic_standing)
      VALUES (1, '117453210', '2024-08-26', 'Good Standing');

   ``RETURNING`` can list any column or expression:
   ``RETURNING person_id, created_at``. ``RETURNING *`` returns every
   column. The result is a normal result set; read it with ``fetchone()``
   in Python. Works on ``INSERT``, ``UPDATE``, and ``DELETE``.

   .. admonition:: Demo 1 -- INSERT with RETURNING for ISA Chain
      :class: note

      Insert Alice using ``RETURNING person_id``. Use the returned value
      to insert her ``student`` row. Then attempt
      ``INSERT INTO student`` with ``person_id = 99`` and observe the FK
      violation.

      .. code-block:: sql

         INSERT INTO person (first_name, last_name, date_of_birth)
         VALUES ('Alice', 'Johnson', '1998-04-12')
         RETURNING person_id;
         -- Returns person_id = 1

         INSERT INTO student (person_id, student_id, admission_date,
                              academic_standing)
         VALUES (1, '117453210', '2024-08-26', 'Good Standing');

         -- FK violation: person 99 does not exist
         INSERT INTO student (person_id, student_id, admission_date,
                              academic_standing)
         VALUES (99, '117453299', '2024-08-26', 'Good Standing');
         -- ERROR: insert or update on table "student" violates
         -- foreign key constraint "fk_student_person"

   .. rubric:: RETURNING on UPDATE and DELETE

   ``RETURNING`` on ``UPDATE`` returns the **new** values after the update
   was applied. ``RETURNING`` on ``DELETE`` returns the row values as they
   were **before** deletion. Neither is a preview: the write already
   happened.

   .. code-block:: sql

      -- UPDATE ... RETURNING: inspect what changed
      UPDATE student
      SET academic_standing = 'Probation'
      WHERE gpa < 2.0
      RETURNING person_id, gpa, academic_standing;
      /* Returns only the rows that were actually modified */

      -- DELETE ... RETURNING: capture before it disappears
      DELETE FROM enrollment
      WHERE student_person_id = 1
      RETURNING student_person_id, course_id, grade;
      /* Returns every deleted row; useful for audit trails */

   In Python: ``rows = cur.fetchall()`` after either statement.

   .. rubric:: ON CONFLICT: Handling Duplicates Gracefully

   ``ON CONFLICT`` tells PostgreSQL what to do when an ``INSERT`` would
   violate a ``UNIQUE`` or ``PRIMARY KEY`` constraint, instead of aborting
   with an error. Without it, any duplicate key aborts the statement and
   rolls back the current transaction block.

   .. code-block:: sql

      INSERT INTO department (dept_name)
      VALUES ('Computer Science');
      /* First run: OK */

      INSERT INTO department (dept_name)
      VALUES ('Computer Science');
      /* Second run:
         ERROR: duplicate key value violates unique constraint
         "department_dept_name_key" */

   ``ON CONFLICT`` makes operations idempotent: safe to run any number of
   times with the same result. The conflict target (``ON CONFLICT (col)``)
   names the ``UNIQUE`` or ``PRIMARY KEY`` column that triggers the
   alternative action.

   **DO NOTHING** -- suppress the error, skip the row:

   .. code-block:: sql

      INSERT INTO department (dept_name)
      VALUES ('Computer Science')
      ON CONFLICT DO NOTHING;
      /* Row already exists: skipped, no error
         Row does not exist: inserted normally */

   .. list-table::
      :widths: 30 40
      :header-rows: 1
      :class: compact-table

      * - Row exists?
        - Result
      * - Yes
        - Skip silently
      * - No
        - Insert normally

   **DO UPDATE (Upsert)** -- update the existing row with the incoming
   values:

   .. code-block:: sql

      INSERT INTO course (course_id, title, credits)
      VALUES ('ENPM818T', 'Databases', 3)
      ON CONFLICT (course_id) DO UPDATE
          SET title   = EXCLUDED.title,
              credits = EXCLUDED.credits;
      /* Row exists: title and credits updated
         Row does not exist: inserted normally */

   ``EXCLUDED`` is the table alias PostgreSQL gives to the incoming row
   that was blocked by the conflict. It lets you reference the values you
   tried to insert inside the ``SET`` clause. ``ON CONFLICT (course_id)``
   names the column whose uniqueness constraint triggers conflict detection.
   ``EXCLUDED`` is PostgreSQL-specific; the SQL-standard equivalent is
   ``MERGE`` (PostgreSQL 15+).

   .. admonition:: Demo 2 -- ON CONFLICT DO NOTHING
      :class: note

      Run the ``department`` insert once and confirm the row is inserted.
      Run it a second time without ``ON CONFLICT`` and observe the
      constraint violation error. Add ``ON CONFLICT DO NOTHING``, run
      again, and confirm zero rows inserted and no error.

      .. code-block:: sql

         INSERT INTO department (dept_name) VALUES ('Computer Science');
         -- First run: OK

         INSERT INTO department (dept_name) VALUES ('Computer Science');
         -- ERROR: duplicate key value violates unique constraint

         INSERT INTO department (dept_name)
         VALUES ('Computer Science')
         ON CONFLICT DO NOTHING;
         -- No error; SELECT COUNT(*) confirms same row count

   .. admonition:: Demo 3 -- ON CONFLICT DO UPDATE
      :class: note

      Insert the course row and confirm insertion. Run the same statement
      with a different title and verify with ``SELECT`` that the title was
      updated, not duplicated.

      .. code-block:: sql

         INSERT INTO course (course_id, title, credits)
         VALUES ('ENPM818T', 'Databases', 3)
         ON CONFLICT (course_id) DO UPDATE
             SET title   = EXCLUDED.title,
                 credits = EXCLUDED.credits;

         -- Run again with a changed title
         INSERT INTO course (course_id, title, credits)
         VALUES ('ENPM818T', 'Data Storage and Databases', 3)
         ON CONFLICT (course_id) DO UPDATE
             SET title   = EXCLUDED.title,
                 credits = EXCLUDED.credits;

         SELECT * FROM course WHERE course_id = 'ENPM818T';
         -- title is now 'Data Storage and Databases'

   .. rubric:: INSERT ... SELECT: Insert from a Query

   No ``VALUES`` clause -- the ``SELECT`` provides the rows. Column count
   and types from the ``SELECT`` must match the target column list exactly.

   .. code-block:: sql

      -- Seed a test table from production
      INSERT INTO student_archive
          (person_id, student_id, admission_date, academic_standing, gpa)
      SELECT person_id, student_id, admission_date, academic_standing, gpa
      FROM student
      WHERE academic_standing = 'Dismissed';

      -- Copy high-GPA students into an honors table
      INSERT INTO honors_student (person_id, student_id, gpa)
      SELECT person_id, student_id, gpa
      FROM student
      WHERE gpa >= 3.5;

   Useful for archiving, data migration, and seeding test tables from
   existing data. Can be combined with ``ON CONFLICT`` for idempotent
   bulk copies. ``RETURNING`` works here too.


.. dropdown:: UPDATE
   :class-container: sd-border-secondary

   .. rubric:: Modifying Existing Rows

   ``UPDATE`` modifies existing rows that match a condition. The most
   dangerous mistake in SQL is running ``UPDATE`` without a ``WHERE``
   clause: every row in the table is overwritten with no warning.

   Key concepts:

   - **Always include WHERE**: an ``UPDATE`` without ``WHERE`` modifies
     every row in the table
   - **Safe workflow**: run ``SELECT`` with the same ``WHERE`` first to
     confirm the target set, then ``UPDATE``
   - ``UPDATE ... RETURNING``: inspect exactly which rows changed and what
     the new values are
   - ``UPDATE ... FROM``: join another table in the ``SET`` or ``WHERE``
     clause (PostgreSQL extension)
   - Computed updates: ``SET credits = credits + 1`` -- the right side is
     evaluated per-row

   Resources:

   - `PostgreSQL documentation: UPDATE <https://www.postgresql.org/docs/current/sql-update.html>`__

   .. warning::

      ``UPDATE`` without ``WHERE`` modifies every row in the table. Always
      write the ``WHERE`` clause in your head before typing ``SET``.

      .. code-block:: sql

         /* DANGEROUS: overwrites every student */
         UPDATE student
         SET academic_standing = 'Probation';

   .. rubric:: Safe Workflow: SELECT First, Then UPDATE

   .. code-block:: sql

      -- Step 1: confirm the target set
      SELECT person_id, gpa, academic_standing
      FROM student
      WHERE gpa < 2.0;

      -- Step 2: update only after verifying
      UPDATE student
      SET academic_standing = 'Probation'
      WHERE gpa < 2.0
      RETURNING person_id, gpa, academic_standing;

   Run the ``SELECT`` with the same ``WHERE`` you plan to use in the
   ``UPDATE``. The result set shows exactly which rows will change.
   ``RETURNING`` confirms exactly which rows changed and what the new
   values are.

   .. list-table::
      :widths: 25 20 35
      :header-rows: 1
      :class: compact-table

      * - ``person_id``
        - ``gpa``
        - ``standing``
      * - 2
        - 1.85
        - Probation
      * - 5
        - 1.92
        - Probation

   .. rubric:: Bulk Updates with a WHERE Condition

   .. code-block:: sql

      -- Promote all associate professors hired before 2020 to Full Professor
      UPDATE professor
      SET rank_code = 'Full'
      WHERE rank_code = 'Associate'
        AND hire_date < '2020-01-01'
      RETURNING person_id, rank_code, hire_date;

   ``SET`` names the column to change and the new value. ``WHERE``
   restricts which rows are affected; rows that do not match are left
   untouched. This is a single statement: all matching rows are updated
   atomically.

   .. list-table::
      :widths: 18 20 22 20 20
      :header-rows: 1
      :class: compact-table

      * - ``person_id``
        - ``hire_date``
        - **rank before**
        - **rank after**
        - **updated?**
      * - 3
        - 2017-08-01
        - Associate
        - Full
        - Yes
      * - 7
        - 2019-01-15
        - Associate
        - Full
        - Yes
      * - 9
        - 2021-03-20
        - Associate
        - Associate
        - No (post-2020)

   .. rubric:: UPDATE ... FROM: Updating from Another Table

   Sometimes the new value you want to write comes from another table.
   ``UPDATE ... FROM`` is a PostgreSQL extension that lets you join a
   second table inside the update statement.

   .. code-block:: sql

      -- Assign each professor the dept_id from a mapping table
      UPDATE professor p
      SET dept_id = m.dept_id
      FROM dept_mapping m
      WHERE m.person_id = p.person_id
        AND p.dept_id IS NULL
      RETURNING p.person_id, p.dept_id AS new_dept;

   The joined table (``dept_mapping``) appears in ``FROM``; it is
   read-only. The join condition in ``WHERE`` is **required**; without it
   every row in ``professor`` is matched against every row in
   ``dept_mapping``. Rows with no match in ``dept_mapping`` are left
   unchanged (``dept_id`` stays ``NULL``).

   .. admonition:: Demo 4 -- Safe UPDATE Workflow
      :class: note

      Run the ``SELECT`` first and note the rows. Run the
      ``UPDATE ... RETURNING`` and confirm the output matches exactly.
      Then deliberately omit ``WHERE`` inside a ``BEGIN`` block, observe
      all rows change, and ``ROLLBACK``.

      .. code-block:: sql

         -- Step 1: preview the target set
         SELECT person_id, gpa, academic_standing
         FROM student
         WHERE gpa < 2.0;

         -- Step 2: update with RETURNING
         UPDATE student
         SET academic_standing = 'Probation'
         WHERE gpa < 2.0
         RETURNING person_id, gpa, academic_standing;

         -- Danger demo: full table overwrite (roll back immediately)
         BEGIN;
         UPDATE student SET academic_standing = 'Probation';
         -- Every row now shows Probation
         SELECT COUNT(*) FROM student
         WHERE academic_standing = 'Probation';
         ROLLBACK;
         -- Damage undone


.. dropdown:: DELETE
   :class-container: sd-border-secondary

   .. rubric:: Removing Rows and Cascade Behavior

   ``DELETE`` removes rows that match a condition. The ``ON DELETE``
   referential actions you defined in L6 determine what happens to
   dependent rows automatically. Always check the cascade scope with
   ``\d+`` before deleting a parent row.

   Key concepts:

   - ``DELETE FROM t WHERE condition``: safe; operates on a subset
   - ``DELETE FROM t`` (no ``WHERE``): removes every row; use ``TRUNCATE``
     for intentional full clears
   - ``DELETE ... RETURNING``: capture deleted rows before they disappear
   - ``ON DELETE CASCADE`` fires silently; always run ``\d+ tablename``
     to know what will disappear
   - ``ON DELETE RESTRICT``: the delete is blocked; remove dependents first

   Resources:

   - `PostgreSQL documentation: DELETE <https://www.postgresql.org/docs/current/sql-delete.html>`__

   .. rubric:: Syntax and CASCADE Behavior

   .. code-block:: sql

      -- Safe: always include WHERE
      DELETE FROM student WHERE person_id = 1;

      -- Capture deleted rows for audit
      DELETE FROM enrollment
      WHERE student_person_id = 1
      RETURNING student_person_id, course_id, grade;

      -- Cascade: one delete propagates down
      DELETE FROM person WHERE person_id = 1;
      /* Automatically removes:
           student row      (ON DELETE CASCADE)
           enrollment rows  (ON DELETE CASCADE)
           grad_student     (ON DELETE CASCADE) */

   ``RETURNING`` only returns the rows deleted from the target table, not
   cascaded rows. To audit cascades, ``DELETE ... RETURNING`` child tables
   explicitly before deleting the parent.

   .. list-table::
      :widths: 35 30 25
      :header-rows: 1
      :class: compact-table

      * - ``student_person_id``
        - ``course_id``
        - ``grade``
      * - 1
        - ENPM818T
        - A
      * - 1
        - ENPM605
        - B+

   .. admonition:: Demo 5 -- DELETE with CASCADE
      :class: note

      Insert Alice into ``person``, ``student``, and two ``enrollment``
      rows. Run ``DELETE FROM enrollment RETURNING`` to capture her rows
      first. Then delete her ``person`` row and confirm both ``student``
      and remaining ``enrollment`` rows are gone.

      .. code-block:: sql

         -- Insert test data
         INSERT INTO person (first_name, last_name, date_of_birth)
         VALUES ('Alice', 'Johnson', '1998-04-12')
         RETURNING person_id;  -- note the returned ID, e.g. 1

         INSERT INTO student (person_id, student_id, admission_date,
                              academic_standing)
         VALUES (1, '117453210', '2024-08-26', 'Good Standing');

         INSERT INTO enrollment (student_person_id, course_id, section_no)
         VALUES (1, 'ENPM818T', '0101'),
                (1, 'ENPM605',  '0101');

         -- Capture enrollment rows before cascade removes them
         DELETE FROM enrollment
         WHERE student_person_id = 1
         RETURNING student_person_id, course_id, grade;

         -- Delete the person row; CASCADE propagates automatically
         DELETE FROM person WHERE person_id = 1;

         -- Confirm cascade: both tables should be empty for person_id = 1
         SELECT * FROM student     WHERE person_id = 1;  -- 0 rows
         SELECT * FROM enrollment  WHERE student_person_id = 1;  -- 0 rows

   .. rubric:: ON DELETE RESTRICT

   When a FK column uses ``RESTRICT``, deleting a parent row that is still
   referenced is blocked immediately.

   .. code-block:: sql

      CREATE TABLE course (
          course_id CHAR(8)     PRIMARY KEY,
          title     VARCHAR(60) NOT NULL,
          credits   INT         NOT NULL
      );

      CREATE TABLE course_prereq (
          successor_id CHAR(8) NOT NULL,
          prereq_id    CHAR(8) NOT NULL,
          PRIMARY KEY (successor_id, prereq_id),
          CONSTRAINT fk_cp_successor
              FOREIGN KEY (successor_id)
                  REFERENCES course (course_id)
                  ON DELETE RESTRICT,
          CONSTRAINT fk_cp_prereq
              FOREIGN KEY (prereq_id)
                  REFERENCES course (course_id)
                  ON DELETE RESTRICT
      );

   ``course_prereq`` has two foreign keys, both pointing back to
   ``course`` -- one for the successor and one for the prerequisite. Both
   are declared ``ON DELETE RESTRICT``.

   .. code-block:: sql

      DELETE FROM course WHERE course_id = 'ENPM605';
      -- ERROR: update or delete on table "course" violates foreign key
      -- constraint "fk_cp_prereq" on table "course_prereq"
      -- DETAIL: Key (course_id)=(ENPM605) is still referenced from
      -- table "course_prereq".

   ``ENPM605`` is referenced in ``course_prereq`` on both sides: as a
   ``prereq_id`` (ENPM605 is required by ENPM818T) and as a
   ``successor_id`` (ENPM605 requires ENPM601). PostgreSQL checks before
   the delete executes -- the parent row is never touched.

   Read the FK name in the error. ``fk_cp_prereq`` tells you exactly which
   constraint and table are blocking. Run ``\d+`` on the parent table to
   list every table that references it.

   **Fix: remove dependents first.**

   .. code-block:: sql

      -- Step 1: remove every course_prereq row that mentions ENPM605
      DELETE FROM course_prereq
      WHERE prereq_id    = 'ENPM605'
         OR successor_id = 'ENPM605';

      -- Step 2: parent row is now unreferenced
      DELETE FROM course WHERE course_id = 'ENPM605';
      -- succeeds

   Both ``OR`` branches are required -- ``ENPM605`` appears in both FK
   columns. Order matters: attempt Step 2 before Step 1 and you get the
   same error again.

   .. rubric:: Referential Actions Summary

   .. list-table::
      :widths: 18 40 42
      :header-rows: 1
      :class: compact-table

      * - **FK action**
        - **Effect on child rows**
        - **Use when**
      * - ``RESTRICT``
        - Block the delete; you remove children manually
        - Default; safest -- no silent side effects
      * - ``CASCADE``
        - Automatically delete child rows
        - Child rows are meaningless without the parent (e.g., ``enrollment``
          when a ``student`` is deleted)
      * - ``SET NULL``
        - Set the child FK column to ``NULL``
        - Child row survives but loses its association (e.g., optional FK)
      * - ``SET DEFAULT``
        - Set the child FK column to its declared default
        - Rare; only valid if the default value is itself a valid FK target

   ``RESTRICT`` and ``NO ACTION`` are nearly identical; the difference is
   *when* the check fires -- ``RESTRICT`` checks immediately, ``NO ACTION``
   defers until end of statement. If no action is specified, PostgreSQL
   defaults to ``NO ACTION``. ``CASCADE`` is powerful but dangerous on
   wide schemas -- prefer ``RESTRICT`` during development.

   .. admonition:: Exercise 1
      :class: note

      Open DataGrip and connect to ``university_db``.

      1. Insert three new departments in a single ``INSERT`` statement.
         Confirm the identity values with ``SELECT``.
      2. Insert a new ``person`` and use ``RETURNING person_id`` to insert
         a matching ``student`` row immediately.
      3. Set ``academic_standing = 'Probation'`` for all students with
         ``gpa < 2.0``. Use the safe workflow: ``SELECT`` first, then
         ``UPDATE ... RETURNING``. Verify the ``RETURNING`` output matches
         the ``SELECT`` preview exactly.
      4. Delete the student you created. Check ``\d+ student`` first, then
         delete from ``person`` and confirm the cascade removed the
         ``student`` row automatically.

      For step 3, deliberately omit ``WHERE`` in a ``BEGIN`` block first,
      observe all rows change, then ``ROLLBACK``. For step 4, run
      ``\d+ student`` in psql before and after to confirm cascade behavior.


Transactions
====================================================

A transaction is a unit of work the database treats as a single
all-or-nothing operation.

Real-world operations often require **multiple statements** to complete:
enrolling a student means decrementing capacity *and* inserting an
enrollment row. Without transactions, a crash or error between statements
leaves the database in a **half-finished state**. Transactions group
statements so the database guarantees: either **all succeed** or **none
take effect**. They also control what concurrent sessions can see: one
session's in-progress work is **invisible** to others until committed.

Every DML statement you ran so far was already a transaction -- PostgreSQL
wraps each standalone statement in an implicit ``BEGIN``/``COMMIT``
(autocommit mode). Explicit transactions let you control where the boundary
falls.


.. dropdown:: ACID Properties
   :class-container: sd-border-secondary

   .. rubric:: Four Guarantees Every PostgreSQL Transaction Makes

   ACID is the set of four properties every PostgreSQL transaction
   guarantees. Each property addresses a different category of failure.
   A database that violates any one is not safe for financial, medical,
   or critical data.

   .. list-table::
      :widths: 16 22 32 30
      :header-rows: 1
      :class: compact-table

      * - **Property**
        - **What it means**
        - **Violation example**
        - **PostgreSQL mechanism**
      * - **Atomicity**
        - All statements commit together or none do
        - Seat decremented; insert fails; seat gone, student not enrolled
        - ``ROLLBACK`` undoes all partial work
      * - **Consistency**
        - Every committed state satisfies all constraints
        - GPA set to 5.0; FK references a non-existent course
        - ``CHECK``, ``FOREIGN KEY``, ``NOT NULL`` at commit
      * - **Isolation**
        - Transactions cannot see uncommitted changes
        - Two sessions read ``capacity = 1``, both enroll; capacity
          becomes -1
        - Read Committed default; ``FOR UPDATE`` for stricter control
      * - **Durability**
        - Committed data survives a crash
        - Power cut immediately after ``COMMIT`` returns
        - WAL flushed to disk before ``COMMIT`` returns


.. dropdown:: BEGIN, COMMIT, ROLLBACK, SAVEPOINT
   :class-container: sd-border-secondary

   .. rubric:: Controlling Transaction Boundaries

   PostgreSQL runs each statement in its own implicit transaction by default
   (autocommit mode). ``BEGIN`` opens an explicit block that spans multiple
   statements. ``SAVEPOINT`` marks a rollback point inside a transaction so
   you can undo part of the work without losing the rest.

   Key concepts:

   - ``BEGIN``: open a transaction block
   - ``COMMIT``: persist all changes; deferred constraints are checked here
   - ``ROLLBACK``: discard all changes since ``BEGIN``
   - ``SAVEPOINT name``: set a named rollback marker inside the transaction
   - ``ROLLBACK TO SAVEPOINT name``: undo work after the marker; transaction
     stays open
   - ``RELEASE SAVEPOINT name``: remove the marker; work is kept

   .. rubric:: COMMIT: The Happy Path

   .. code-block:: sql

      BEGIN;
      UPDATE course_section
      SET capacity = capacity - 1
      WHERE course_id  = 'ENPM818T'
        AND section_no = '0101';
      INSERT INTO enrollment (student_person_id, course_id, section_no)
      VALUES (1, 'ENPM818T', '0101');
      COMMIT;

   ``BEGIN`` opens the transaction block. Both statements execute but are
   not yet visible to other sessions. ``COMMIT`` makes both changes
   permanent and visible atomically. If the server crashes between
   ``BEGIN`` and ``COMMIT``, neither change is applied.

   .. list-table::
      :widths: 36 22 22
      :header-rows: 1
      :class: compact-table

      * - **Event**
        - ``capacity``
        - ``enrollment``
      * - Before ``BEGIN``
        - 30
        - 0 rows
      * - After ``UPDATE``
        - 29
        - 0 rows
      * - After ``INSERT``
        - 29
        - 1 row
      * - After ``COMMIT``
        - 29
        - 1 row

   .. rubric:: ROLLBACK: When Something Goes Wrong

   .. code-block:: sql

      BEGIN;
      UPDATE course_section
      SET capacity = capacity - 1
      WHERE course_id  = 'ENPM818T'
        AND section_no = '0101';
      INSERT INTO enrollment (student_person_id, course_id, section_no)
      VALUES (999, 'ENPM818T', '0101');
      /* FK violation: person 999 does not exist */
      ROLLBACK;   /* capacity restored to 30 */

   The ``UPDATE`` succeeded (capacity is 29 inside this transaction). The
   ``INSERT`` fails: person 999 does not exist. ``ROLLBACK`` discards
   **all** work since ``BEGIN`` -- including the successful ``UPDATE``.
   Capacity goes back to 30 as if nothing happened.

   .. list-table::
      :widths: 36 22 22
      :header-rows: 1
      :class: compact-table

      * - **Event**
        - ``capacity``
        - ``enrollment``
      * - Before ``BEGIN``
        - 30
        - 0 rows
      * - After ``UPDATE``
        - 29
        - 0 rows
      * - ``INSERT`` fails
        - 29
        - 0 rows
      * - After ``ROLLBACK``
        - 30
        - 0 rows

   .. warning::

      ``ROLLBACK`` is all-or-nothing. You cannot roll back just the failing
      statement and keep the rest. ``ROLLBACK`` discards everything. To undo
      only part of the work, use ``SAVEPOINT``.

   .. admonition:: Demo 6 -- COMMIT and ROLLBACK
      :class: note

      Run the successful block and confirm both rows are committed. Then
      run the failing variant (``person_id = 999``) and confirm capacity
      is restored after ``ROLLBACK``.

      .. code-block:: sql

         -- Happy path: both changes committed atomically
         BEGIN;
         UPDATE course_section
         SET capacity = capacity - 1
         WHERE course_id = 'ENPM818T' AND section_no = '0101';
         INSERT INTO enrollment (student_person_id, course_id, section_no)
         VALUES (1, 'ENPM818T', '0101');
         COMMIT;
         SELECT capacity FROM course_section
         WHERE course_id = 'ENPM818T' AND section_no = '0101';
         -- capacity = 29

         -- Rollback path: FK violation undoes the UPDATE too
         BEGIN;
         UPDATE course_section
         SET capacity = capacity - 1
         WHERE course_id = 'ENPM818T' AND section_no = '0101';
         INSERT INTO enrollment (student_person_id, course_id, section_no)
         VALUES (999, 'ENPM818T', '0101');
         -- ERROR: FK violation
         ROLLBACK;
         SELECT capacity FROM course_section
         WHERE course_id = 'ENPM818T' AND section_no = '0101';
         -- capacity restored to 30

   .. rubric:: SAVEPOINT: Partial Rollback Without Aborting

   .. code-block:: sql

      BEGIN;
      INSERT INTO enrollment VALUES (1, 'ENPM818T', '0101');
      INSERT INTO enrollment VALUES (2, 'ENPM605',  '0101');
      INSERT INTO enrollment VALUES (3, 'ENPM702',  '0101');

      SAVEPOINT after_three;

      INSERT INTO enrollment VALUES (3, 'ENPM702', '0101');
      /* FAIL: duplicate PK */

      ROLLBACK TO SAVEPOINT after_three;
      /* Rows 1, 2, 3 still here; failed insert gone */

      INSERT INTO enrollment VALUES (4, 'ENPM702', '0101');
      COMMIT;
      /* 4 rows committed; bad attempt left no trace */

   ``SAVEPOINT`` does not commit; it only marks a rollback point.
   ``ROLLBACK TO SAVEPOINT`` undoes everything *after* the marker --
   everything before is preserved. The transaction stays open; you can
   continue adding work. Ideal for batch inserts where one row may fail
   without aborting the entire batch.

   .. admonition:: Demo 7 -- SAVEPOINT: Partial Rollback
      :class: note

      Run the script exactly as shown. Observe the duplicate key error
      does not abort the transaction. After ``ROLLBACK TO SAVEPOINT``,
      insert the replacement row and commit. Confirm exactly 4 rows exist
      and the failed attempt left no trace.

      .. code-block:: sql

         BEGIN;
         INSERT INTO enrollment (student_person_id, course_id, section_no)
             VALUES (1, 'ENPM818T', '0101');
         INSERT INTO enrollment (student_person_id, course_id, section_no)
             VALUES (2, 'ENPM605',  '0101');
         INSERT INTO enrollment (student_person_id, course_id, section_no)
             VALUES (3, 'ENPM702',  '0101');

         SAVEPOINT after_three;

         INSERT INTO enrollment (student_person_id, course_id, section_no)
             VALUES (3, 'ENPM702', '0101');
         -- ERROR: duplicate key value violates unique constraint
         -- Transaction is still open -- NOT aborted

         ROLLBACK TO SAVEPOINT after_three;
         -- Rows 1, 2, 3 preserved; duplicate attempt gone

         INSERT INTO enrollment (student_person_id, course_id, section_no)
             VALUES (4, 'ENPM702', '0101');
         COMMIT;

         SELECT COUNT(*) FROM enrollment;  -- 4

   .. rubric:: Manual vs. Automated Rollback

   The ``SAVEPOINT`` demo was intentionally manual to expose the mechanism.
   In production code, rollback is never written by hand -- it is triggered
   automatically by the layer that owns the transaction.

   Three patterns exist for handling failures in practice:

   - **PL/pgSQL exception block** -- the database catches the error and
     rolls back to an implicit savepoint that PostgreSQL creates at the
     start of every ``EXCEPTION`` block; the calling session never sees
     the failure.
   - **Application-level try/catch** -- the application driver raises an
     exception on error; the application calls ``conn.rollback()`` and
     decides whether to retry, skip, or re-raise.
   - ``ON CONFLICT`` -- the cleanest option for uniqueness violations;
     the conflict is handled entirely at the SQL level with no exception
     handling or rollback needed at all.

   .. card::
      :class-card: sd-border-info

      **Rule of thumb**: if you find yourself writing
      ``ROLLBACK TO SAVEPOINT`` in application code, first ask whether
      ``ON CONFLICT`` or a proper ``EXCEPTION`` block would handle the
      same case more cleanly. Manual savepoints belong in migration
      scripts and one-off administrative work, not in application logic.


.. dropdown:: Isolation
   :class-container: sd-border-secondary

   .. rubric:: What Concurrent Transactions Can See

   Isolation controls what a transaction can see when other transactions
   run concurrently. Without it, two sessions can read and write the same
   row simultaneously and produce inconsistent results. PostgreSQL provides
   four isolation levels; the default is **Read Committed**.

   Resources:

   - `PostgreSQL documentation: Transaction Isolation <https://www.postgresql.org/docs/current/transaction-iso.html>`__

   .. rubric:: Anomaly 1: Dirty Read

   .. code-block:: sql

      -- CONNECTION 1 (Session A)
      BEGIN;
      UPDATE student SET gpa = 0.5 WHERE person_id = 1;
      -- NOT committed yet

      -- CONNECTION 2 (Session B) -- while A is still open
      SELECT gpa FROM student WHERE person_id = 1;
      -- Sees 0.5 even though A has not committed

      -- Back in CONNECTION 1
      ROLLBACK;
      -- gpa is back to 3.75, but B already used the wrong value

   A **dirty read** occurs when a transaction reads data written by another
   transaction that has not yet committed. **PostgreSQL prevents this
   entirely**: even at the lowest isolation level, PostgreSQL uses Read
   Committed, which never exposes uncommitted writes. This anomaly is
   mentioned because other databases (e.g., MySQL with Read Uncommitted)
   allow it.

   .. rubric:: Anomaly 2: Non-Repeatable Read (READ COMMITTED)

   .. code-block:: sql

      -- CONNECTION 1 (Session A)
      BEGIN;
      SELECT gpa FROM student WHERE person_id = 1;  -- Returns 3.75

      -- CONNECTION 2 (Session B)
      UPDATE student SET gpa = 2.0 WHERE person_id = 1;
      -- Session B commits and closes

      -- Back in CONNECTION 1 (Session A)
      SELECT gpa FROM student WHERE person_id = 1;  -- Returns 2.0 (!)
      COMMIT;

   A **non-repeatable read** occurs when a transaction reads the same row
   twice and gets two different values because another transaction committed
   a change in between. Under ``READ COMMITTED``, each ``SELECT`` takes a
   fresh snapshot of all committed data at the moment that statement
   executes -- so Session B's commit bleeds into A's second read.

   **Preventing it with REPEATABLE READ:**

   .. code-block:: sql

      -- CONNECTION 1 (Session A)
      BEGIN ISOLATION LEVEL REPEATABLE READ;
      SELECT gpa FROM student WHERE person_id = 1;  -- Returns 3.75

      -- CONNECTION 2 (Session B)
      UPDATE student SET gpa = 2.0 WHERE person_id = 1;
      -- Session B commits and closes

      -- Back in CONNECTION 1 (Session A)
      SELECT gpa FROM student WHERE person_id = 1;  -- Returns 3.75
      -- Snapshot frozen at BEGIN time; Session B's commit is invisible to A
      COMMIT;

   One snapshot is taken at ``BEGIN`` and held for the entire transaction.
   Session B's commit is durable and visible to any new connection, but A
   cannot see it until A commits and starts a new transaction.

   .. note::

      PostgreSQL never overwrites a row in place -- updates write a new row
      version and mark the old one dead. Under ``REPEATABLE READ``, the old
      version must stay alive for as long as Session A's transaction is open.
      Long-running ``REPEATABLE READ`` transactions therefore pin dead row
      versions in place, delaying cleanup and causing table bloat in busy
      databases.

   .. rubric:: Anomaly 3: Phantom Read

   .. code-block:: sql

      -- CONNECTION 1 (Session A)
      BEGIN;
      SELECT count(*) FROM student WHERE gpa > 3.5;  -- Returns 2

      -- CONNECTION 2 (Session B): inserts a new high-GPA student
      INSERT INTO person (first_name, last_name, date_of_birth)
      VALUES ('New', 'Student', '2001-01-01')
      RETURNING person_id;  -- e.g. 11
      INSERT INTO student VALUES (11, '117999999', '2025-08-25',
                                  'Good Standing', 3.90);

      -- Back in CONNECTION 1 (Session A)
      SELECT count(*) FROM student WHERE gpa > 3.5;  -- Returns 3 (!)
      COMMIT;

   A **phantom read** occurs when a query returns a different *set of rows*
   because another transaction inserted or deleted rows that match the
   filter. ``READ COMMITTED`` allows phantoms. ``REPEATABLE READ`` prevents
   them in PostgreSQL -- the snapshot is frozen at transaction start, so new
   inserts by other sessions are invisible.

   .. rubric:: Anomaly 4: Write Skew

   .. code-block:: sql

      -- Rule: at least 1 of 2 doctors must be on call at all times

      -- CONNECTION 1 (Session A)
      BEGIN ISOLATION LEVEL REPEATABLE READ;
      SELECT count(*) FROM on_call;  -- Returns 2: safe to remove one

      -- CONNECTION 2 (Session B)
      BEGIN ISOLATION LEVEL REPEATABLE READ;
      SELECT count(*) FROM on_call;  -- Also returns 2: safe to remove one
      COMMIT;

      -- CONNECTION 1 (Session A)
      DELETE FROM on_call WHERE doctor = 'A';
      COMMIT;

      -- CONNECTION 2 (Session B) -- still thinks count was 2
      DELETE FROM on_call WHERE doctor = 'B';
      COMMIT;
      -- Result: 0 doctors on call!

   **Write skew** occurs when two transactions each read the same data,
   make decisions based on it, and write to *different* rows -- the combined
   effect violates a constraint that neither transaction violated alone. Each
   transaction saw a valid snapshot and made a valid decision in isolation.
   Neither overwrote the other's row, so row-level locks do not help. Only
   ``SERIALIZABLE`` prevents this.

   Under ``SERIALIZABLE``, PostgreSQL detects that the two transactions read
   overlapping data and made conflicting decisions. It aborts one with a
   ``serialization_failure`` error and requires the application to retry.

   .. rubric:: Isolation Levels vs. Anomalies

   .. list-table::
      :widths: 28 18 18 18 18
      :header-rows: 1
      :class: compact-table

      * - **Anomaly**
        - **Read Uncommitted**
        - **Read Committed**
        - **Repeatable Read**
        - **Serializable**
      * - Dirty read
        - Yes
        - No
        - No
        - No
      * - Non-repeatable read
        - Yes
        - Yes
        - No
        - No
      * - Phantom read
        - Yes
        - Yes
        - No*
        - No
      * - Write skew
        - Yes
        - Yes
        - Yes
        - No

   \*PostgreSQL ``REPEATABLE READ`` prevents phantom reads; the SQL standard
   only requires ``SERIALIZABLE`` to do so. PostgreSQL does not implement
   ``READ UNCOMMITTED``; it falls back to ``READ COMMITTED``.

   **Higher isolation = fewer anomalies, but more aborted transactions.**
   For GP2, ``READ COMMITTED`` is sufficient for most queries. Use
   ``SELECT ... FOR UPDATE`` when two concurrent transactions might read
   then modify the same row. Reach for ``SERIALIZABLE`` only when explicit
   locks are not enough.

   .. rubric:: The Lost Update Problem and SELECT ... FOR UPDATE

   Session A reads ``capacity = 1`` and plans to enroll student 1. Before
   it inserts, Session B also reads ``capacity = 1`` and enrolls student 2.
   Both inserts succeed. The course now has two enrollments but capacity was
   1.

   ``SELECT ... FOR UPDATE`` locks the row when Session A reads it. Session
   B blocks on the same lock until Session A commits. Session B then reads
   ``capacity = 0`` and correctly declines to enroll.


   .. code-block:: sql

      BEGIN;
      SELECT capacity FROM course_section
      WHERE course_id = 'ENPM818T' AND section_no = '0101'
      FOR UPDATE;           /* Row locked until COMMIT */
      /* If capacity > 0: update + insert; else ROLLBACK */
      UPDATE course_section
      SET capacity = capacity - 1
      WHERE course_id = 'ENPM818T' AND section_no = '0101';
      INSERT INTO enrollment (student_person_id, course_id, section_no)
      VALUES (1, 'ENPM818T', '0101');
      COMMIT;

   .. admonition:: Exercise 2
      :class: note

      Complete both tasks in DataGrip. Use ``\d+ enrollment`` in psql to
      understand the FK chain before starting.

      1. **Atomic enrollment**: wrap a ``capacity`` decrement and an
         ``INSERT INTO enrollment`` in a single ``BEGIN``/``COMMIT`` block.
         Then force a failure (e.g., ``person_id = 999``) inside the
         transaction and confirm ``ROLLBACK`` restores capacity.

      2. **Savepoint batch**: write a ``BEGIN`` block that inserts five
         enrollment rows. Set a ``SAVEPOINT`` after the third. Make the
         fourth deliberately fail (duplicate PK). Roll back to the
         savepoint, insert a valid replacement, then ``COMMIT``. Confirm
         exactly five rows were committed.


psycopg3: Python Integration
====================================================

psycopg3 is the recommended PostgreSQL driver for Python. Released in 2021;
actively maintained; use it for all new projects. It supports synchronous and
async usage, binary protocol, and automatic type mapping. psycopg2 remains
functional but receives no new features; **GP2 uses psycopg3 throughout**.

**Installation** (always inside a virtual environment):

.. code-block:: bash

   pip install -r requirements.txt

The ``requirements.txt`` contains three packages: ``psycopg[binary]`` (the
core psycopg3 driver plus pre-compiled C extensions; no local C compiler
required), ``psycopg-pool`` (the psycopg3 connection pool; shipped
separately), and ``python-dotenv`` (reads a ``.env`` file into environment
variables so credentials never appear in source code).


.. dropdown:: Repository Pattern
   :class-container: sd-border-secondary

   .. rubric:: SQL Lives in Exactly One Place

   Without a repository, ``cur.execute()`` calls are scattered across the
   codebase; renaming one column means hunting through every file. With a
   repository, one class owns all SQL for one entity; one place to change
   when the schema evolves.

   **Five layers:**

   .. list-table::
      :widths: 20 35 45
      :header-rows: 1
      :class: compact-table

      * - **Layer**
        - **Owns**
        - **Rule**
      * - ``cli/``
        - User I/O, menus
        - No SQL; no business logic
      * - ``services/``
        - Business rules, transactions
        - No ``execute()`` calls
      * - ``repositories/``
        - All ``execute()`` calls
        - No business logic; no user I/O
      * - ``models/``
        - Dataclasses
        - Pure data; no DB calls
      * - ``config/``
        - Connection pool
        - No queries; no logic

   Each layer has exactly one responsibility and calls only the layer below
   it.

   Why layer the application? Without layers, SQL strings, business rules,
   and ``input()`` calls are mixed in one file. Renaming a column means
   hunting through every function. Adding a menu option risks breaking a
   query. Layering provides separation of concerns, changeability (a schema
   change touches only the repository), testability (test a repository
   without a menu), and team-friendliness (four students can work on four
   layers in parallel with minimal merge conflicts).

   .. rubric:: Project Structure

   .. code-block:: text

      university_app/
      |-- .env
      |-- requirements.txt
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
      |   `-- enrollment_service.py
      `-- cli/
          `-- menu.py

   - ``.env`` -- holds database credentials (``DB_HOST``, ``DB_PORT``,
     ``DB_NAME``, ``DB_USER``, ``DB_PASSWORD``); read by ``load_dotenv()``
     at startup; **never committed to Git**.
   - ``requirements.txt`` -- lists the three packages; teammates run
     ``pip install -r requirements.txt``.
   - ``main.py`` -- the entry point: calls ``DatabaseConfig.initialize()``
     to create the connection pool, calls ``menu.main()`` to start the CLI
     loop, and calls ``DatabaseConfig.close()`` on exit.

   .. important::

      Create this structure **at the start of GP2** before writing any
      code. Do not let the project grow organically into a single file.


.. dropdown:: .env and Credentials
   :class-container: sd-border-secondary

   .. rubric:: Keeping Credentials Out of Source Code

   .. code-block:: text

      # .env
      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=university_db
      DB_USER=postgres
      DB_PASSWORD=your_password_here

   .. code-block:: text

      # .gitignore
      .env
      __pycache__/
      *.pyc
      *.pyo
      .venv/
      venv/
      .vscode

   ``.env`` sits in the project root and holds every secret for that
   environment. ``load_dotenv()`` reads it into ``os.environ`` at startup;
   the rest of the code calls ``os.getenv()`` and never sees the raw
   values. Use a different ``.env`` per environment: one for development,
   one for production, one for testing.

   .. warning::

      **Add .env to .gitignore before the first commit.** Once a password
      is pushed to a public repository it must be considered compromised --
      even if you delete the commit later. Leaked database credentials are
      the most common cause of data breaches in student projects.


.. dropdown:: Connecting and Executing Queries
   :class-container: sd-border-secondary

   .. rubric:: Connections, Cursors, and Row Factories

   A psycopg3 **connection** is one physical connection to PostgreSQL. A
   **cursor** is the object through which queries are sent and results
   retrieved. Both are used as context managers so cleanup is guaranteed
   even when exceptions occur.

   Key concepts:

   - **Context managers**: ``with psycopg.connect(...) as conn`` closes on
     exit; ``with conn.cursor() as cur`` closes the cursor
   - **Row factories**: ``row_factory=dict_row`` returns rows as ``dict``
     instead of tuple -- prefer this in GP2
   - **Fetch methods**: ``fetchone()`` for one row, ``fetchall()`` for all,
     ``fetchmany(n)`` for batches
   - **autocommit**: set ``conn.autocommit = True`` for DDL statements
     (``CREATE TABLE``, ``DROP``)

   .. rubric:: Minimal Working Connection

   .. code-block:: python

      # standalone_connection_test.py
      # Verify connectivity -- add to .gitignore or delete after use
      # This script is NOT part of university_app
      import psycopg, os
      from dotenv import load_dotenv

      load_dotenv()

      conn_str = (
          f"host={os.getenv('DB_HOST', 'localhost')} "
          f"port={os.getenv('DB_PORT', '5432')} "
          f"dbname={os.getenv('DB_NAME')} "
          f"user={os.getenv('DB_USER')} "
          f"password={os.getenv('DB_PASSWORD')}"
      )

      with psycopg.connect(conn_str) as conn:
          with conn.cursor() as cur:
              cur.execute("SELECT version()")
              print(cur.fetchone()[0])

   ``import psycopg`` is the psycopg3 import; psycopg2 used
   ``import psycopg2`` -- these are different packages. ``load_dotenv()``
   injects ``.env`` values into ``os.environ``; credentials never appear
   in source code. The ``with`` block on ``conn`` closes the connection
   automatically, even if an exception is raised.

   .. admonition:: Demo 8 -- Minimal Connection Script
      :class: note

      Create ``.env`` and run the script. Confirm the version string
      prints. In a second terminal, run
      ``SELECT count(*) FROM pg_stat_activity`` in psql and confirm one
      new connection appeared.

      .. code-block:: python

         # Create .env with your credentials, then:
         python standalone_connection_test.py
         # PostgreSQL 18.x on x86_64-pc-linux-gnu, compiled by ...

   .. rubric:: Tuple Cursor (Default) vs. Dict Cursor (Preferred)

   By default, each row is a plain Python tuple -- columns are accessed by
   position (``row[0]``, ``row[1]``). This is fragile: if you reorder
   columns in the query, every index breaks silently.

   .. code-block:: python

      # repositories/student_repo.py -- tuple cursor (avoid in GP2)
      with DatabaseConfig.get_connection() as conn:
          with conn.cursor() as cur:
              cur.execute(
                  "SELECT person_id, first_name FROM person ORDER BY person_id"
              )
              for row in cur.fetchall():
                  print(row[0], row[1])  # fragile: index-based access

   With ``row_factory=dict_row``, each row is a ``dict`` keyed by column
   name. Column order in the query no longer matters. Self-documenting:
   ``row['person_id']`` is unambiguous; ``row[0]`` is not.

   .. code-block:: python

      # repositories/student_repo.py -- dict cursor (use this)
      from psycopg.rows import dict_row

      with DatabaseConfig.get_connection() as conn:
          with conn.cursor(row_factory=dict_row) as cur:
              cur.execute(
                  "SELECT person_id, first_name FROM person ORDER BY person_id"
              )
              for row in cur.fetchall():
                  print(row['person_id'], row['first_name'])  # robust

   .. list-table::
      :widths: 25 35 40
      :header-rows: 1
      :class: compact-table

      * -
        - **Tuple**
        - **Dict**
      * - Access
        - ``row[0]``
        - ``row['col']``
      * - Speed
        - Slightly faster
        - Negligible difference
      * - Fragility
        - Breaks on column reorder
        - Safe
      * - Readability
        - Low
        - High

   Use dict rows in GP2. Column name access makes repository methods
   self-documenting and survives query refactoring.


.. dropdown:: Parameterized Queries and SQL Injection
   :class-container: sd-border-secondary

   .. rubric:: The Only Safe Way to Pass Values

   SQL injection is the most common and most preventable web vulnerability.
   It happens when user input is concatenated directly into a SQL string.
   Parameterized queries are the complete defense: the driver always
   separates SQL text from values.

   Key concepts:

   - ``cur.execute(sql, params)``: the **only** safe way to pass values --
     never use f-strings or ``%`` formatting
   - Placeholder: ``%s`` for positional parameters, ``%(name)s`` for named
     parameters
   - The driver escapes all values; an attacker cannot inject SQL through a
     parameterized value
   - ``print(cur.query)`` shows the exact SQL bytes sent to the server --
     useful for debugging

   Resources:

   - `Passing parameters to SQL queries <https://www.psycopg.org/psycopg3/docs/basic/params.html>`__

   .. warning::

      **SQL Injection: Never Do This**

      .. code-block:: python

         # repositories/student_repo.py -- WRONG
         sid = input("Student ID: ")
         # Attacker types: ' OR '1'='1
         cur.execute(
             f"SELECT * FROM student WHERE student_id = '{sid}'"
         )
         # Becomes: WHERE student_id = '' OR '1'='1'
         # Returns ALL rows

   .. card::
      :class-card: sd-border-success

      **Parameterized: Always Safe**

      .. code-block:: python

         # repositories/student_repo.py -- correct
         sid = input("Student ID: ")
         cur.execute(
             "SELECT * FROM student WHERE student_id = %s",
             (sid,)   # always a tuple
         )
         # Returns 0 rows for the attack string

   The driver sends SQL and values separately; the database never
   interprets values as SQL. Works for any special character: ``%``,
   quotes, semicolons, backslashes. Use ``(sid,)`` not ``(sid)``: a
   single-element tuple requires the trailing comma. With the parameterized
   version, the malicious input ``' OR '1'='1`` is treated as a literal
   string value -- zero rows are returned.

   .. rubric:: Transactions in Python

   .. code-block:: python

      # services/enrollment_service.py
      with DatabaseConfig.get_connection() as conn:
          with conn.transaction():
              conn.execute(
                  "UPDATE course_section "
                  "SET capacity = capacity - 1 "
                  "WHERE course_id = %s AND section_no = %s",
                  ('ENPM818T', '0101')
              )
              conn.execute(
                  "INSERT INTO enrollment "
                  "(student_person_id, course_id, section_no) "
                  "VALUES (%s, %s, %s)",
                  (1, 'ENPM818T', '0101')
              )
              # COMMIT on clean exit; ROLLBACK on exception

   ``conn.transaction()`` issues ``BEGIN`` on entry and ``COMMIT`` on
   clean exit. Any exception inside the block triggers automatic
   ``ROLLBACK``; no manual ``conn.rollback()`` is needed. This pattern
   maps directly to the ``BEGIN``/``COMMIT`` blocks from Section 2.

   .. admonition:: Demo 9 -- Transactions in Python
      :class: note

      Run ``conn.transaction()`` with the enrollment example. Verify both
      rows are committed. Then pass ``person_id = 999`` and confirm the
      capacity is restored by the automatic rollback.

      .. code-block:: python

         # services/enrollment_service.py
         from config.database import DatabaseConfig

         def enroll_student(person_id, course_id, section_no):
             with DatabaseConfig.get_connection() as conn:
                 with conn.transaction():
                     conn.execute(
                         "UPDATE course_section "
                         "SET capacity = capacity - 1 "
                         "WHERE course_id = %s AND section_no = %s",
                         (course_id, section_no)
                     )
                     conn.execute(
                         "INSERT INTO enrollment "
                         "(student_person_id, course_id, section_no) "
                         "VALUES (%s, %s, %s)",
                         (person_id, course_id, section_no)
                     )

         # Happy path
         enroll_student(1, 'ENPM818T', '0101')

         # Rollback path: person 999 does not exist
         enroll_student(999, 'ENPM818T', '0101')
         # Exception raised; capacity auto-restored

   .. rubric:: Autocommit: psql vs. psycopg3

   .. warning::

      **Different defaults.** ``psql`` runs in **autocommit** mode by
      default: every statement is its own transaction and is committed
      immediately. **psycopg3** does **not** autocommit by default:
      statements are accumulated in an implicit transaction block. Nothing
      is visible to other sessions until you call ``conn.commit()`` or exit
      a ``conn.transaction()`` block.

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * -
        - **psql**
        - **psycopg3**
      * - Default mode
        - Autocommit
        - Transaction
      * - ``INSERT`` visible?
        - Immediately
        - After ``commit()``
      * - DDL support
        - Direct
        - Requires ``autocommit=True``

   This is the most common source of *"my INSERT worked in psql but nothing
   shows up from Python"* bugs. Always use ``conn.transaction()`` for DML
   or call ``conn.commit()`` explicitly.


.. dropdown:: Connection Pooling
   :class-container: sd-border-secondary

   .. rubric:: One Pool, Shared Across the Application

   Opening a PostgreSQL connection takes roughly 50 ms and spawns a
   dedicated backend process. Calling ``psycopg.connect()`` on every query
   is far too expensive in any real application. A pool keeps connections
   open and lends them to callers on demand.

   Key concepts:

   - ``psycopg_pool.ConnectionPool``: psycopg3's pool class; ``min_size``
     connections always open; up to ``max_size`` under load
   - ``pool.connection()``: context manager -- borrows one connection,
     returns it on exit
   - Initialize the pool **once at startup**, not once per request or per
     function call
   - GP2 guideline: ``min_size=2``, ``max_size=10`` is appropriate for a
     CLI application
   - ``pool.close()`` at shutdown releases all backend processes


   .. rubric:: DatabaseConfig: The Pool Wrapper

   .. code-block:: python

      # university_app/config/database.py
      import psycopg_pool, os
      from dotenv import load_dotenv
      load_dotenv()

      class DatabaseConfig:
          _pool = None

          @classmethod
          def _conninfo(cls):
              return (
                  f"host={os.getenv('DB_HOST', 'localhost')} "
                  f"port={os.getenv('DB_PORT', '5432')} "
                  f"dbname={os.getenv('DB_NAME')} "
                  f"user={os.getenv('DB_USER')} "
                  f"password={os.getenv('DB_PASSWORD')}"
              )

          @classmethod
          def initialize(cls):
              cls._pool = psycopg_pool.ConnectionPool(
                  conninfo=cls._conninfo(),
                  min_size=2,
                  max_size=10,
                  open=True
              )

          @classmethod
          def get_connection(cls):
              if cls._pool is None:
                  cls.initialize()
              return cls._pool.connection()

   ``_pool = None`` is a class-level variable; there is exactly one pool
   shared across the entire application. ``open=True`` opens ``min_size=2``
   connections immediately at construction time. ``get_connection()`` is a
   lazy guard: if ``initialize()`` was never called, it calls it
   automatically.

   .. rubric:: Using the Pool

   .. code-block:: python

      # university_app/main.py
      DatabaseConfig.initialize()

      # university_app/repositories/student_repo.py
      with DatabaseConfig.get_connection() as conn:
          with conn.cursor() as cur:
              cur.execute("SELECT ...")
              return cur.fetchall()

   ``initialize()`` is called once in ``main.py`` at startup -- never
   inside a repository method or per-request. Every repository method calls
   ``get_connection()``; none of them know or care which physical
   connection they receive. When the ``with`` block exits, the connection
   is returned to the pool and immediately available for the next caller.


.. dropdown:: Bulk Inserts from Python
   :class-container: sd-border-secondary

   .. rubric:: executemany and COPY

   Section 1 showed multi-row ``INSERT`` in SQL. When rows come from Python
   (CSV files, API responses, generated data), the driver provides two ways
   to send them efficiently.

   Key concepts:

   - ``cur.executemany(sql, params_seq)``: runs the same statement once per
     row; simple but sends N round trips
   - ``cur.copy("COPY t FROM STDIN")``: streams rows via PostgreSQL's
     binary ``COPY`` protocol; orders of magnitude faster for large batches
   - Use ``executemany()`` for tens of rows; use ``copy()`` for hundreds
     or more
   - Both respect transactions: wrap in ``conn.transaction()`` for
     atomicity

   .. rubric:: executemany(): Simple Batch Insert

   .. code-block:: python

      # standalone_seed.py -- run once to populate the database
      # not part of university_app
      departments = [
          ('Computer Science',),
          ('Mathematics',),
          ('Mechanical Engineering',),
          ('Electrical Engineering',),
      ]

      with conn.transaction():
          with conn.cursor() as cur:
              cur.executemany(
                  "INSERT INTO department (dept_name) VALUES (%s)",
                  departments
              )
              # 4 rows inserted atomically

   Each element in the list is a tuple of parameters for one execution.
   All inserts share the same ``conn.transaction()`` block: all succeed or
   all roll back. ``executemany()`` does not return results; use
   ``cur.rowcount`` after to verify the count.

   .. rubric:: copy(): High-Performance Bulk Load

   .. code-block:: python

      # standalone_seed.py (continued)
      with conn.cursor() as cur:
          with cur.copy(
              "COPY department (dept_name) FROM STDIN"
          ) as copy:
              for name in dept_names:
                  copy.write_row((name,))

   Streams rows directly via PostgreSQL's ``COPY`` protocol -- no per-row
   round trips. Ideal for seeding GP2 data. Cannot use ``RETURNING`` with
   ``COPY``; use ``INSERT ... SELECT`` or ``executemany()`` when you need
   returned values.


.. dropdown:: Implementing the Repository Layer
   :class-container: sd-border-secondary

   .. rubric:: One Method = One Query

   .. code-block:: python

      # university_app/repositories/student_repo.py
      from config.database import DatabaseConfig
      from psycopg.rows import dict_row

      class StudentRepository:

          def find_by_id(self, person_id: int):
              with DatabaseConfig.get_connection() as conn:
                  with conn.cursor(row_factory=dict_row) as cur:
                      cur.execute(
                          "SELECT * FROM student WHERE person_id = %s",
                          (person_id,)
                      )
                      return cur.fetchone()
                      # Returns None if the row does not exist

          def find_all(self):
              with DatabaseConfig.get_connection() as conn:
                  with conn.cursor(row_factory=dict_row) as cur:
                      cur.execute(
                          "SELECT * FROM student ORDER BY person_id"
                      )
                      return cur.fetchall()
                      # Returns [] if no rows match; never None

   Each method does exactly one thing: run one query and return the result.
   No business logic here; the service decides what to do with the data.
   The caller never sees SQL; it just calls ``find_by_id(1)``.

   .. rubric:: The Student Model

   .. code-block:: python

      # university_app/models/student.py
      from dataclasses import dataclass
      from datetime import date

      @dataclass
      class Student:
          person_id:         int
          student_id:        str
          admission_date:    date
          academic_standing: str
          gpa:               float | None = None

   A ``@dataclass`` generates ``__init__``, ``__repr__``, and ``__eq__``
   automatically from the field declarations. Field names match the
   database column names exactly; this makes ``Student(**row)`` trivial to
   write. ``gpa: float | None = None`` means the field is optional.
   Models contain **no database calls** -- they are pure data containers.


.. dropdown:: The Service Layer
   :class-container: sd-border-secondary

   .. rubric:: Business Logic and Transactions

   .. code-block:: python

      # university_app/services/enrollment_service.py
      from config.database import DatabaseConfig

      class EnrollmentService:

          def enroll_student(self, person_id, course_id, section_no):
              with DatabaseConfig.get_connection() as conn:
                  with conn.transaction():
                      with conn.cursor() as cur:
                          cur.execute(
                              "SELECT capacity FROM course_section "
                              "WHERE course_id = %s AND section_no = %s "
                              "FOR UPDATE",
                              (course_id, section_no)
                          )
                          row = cur.fetchone()
                          if row is None:
                              raise ValueError("Section not found")
                          if row[0] <= 0:
                              raise ValueError("Section is full")
                          cur.execute(
                              "UPDATE course_section "
                              "SET capacity = capacity - 1 "
                              "WHERE course_id = %s AND section_no = %s",
                              (course_id, section_no)
                          )
                          cur.execute(
                              "INSERT INTO enrollment "
                              "(student_person_id, course_id, section_no) "
                              "VALUES (%s, %s, %s)",
                              (person_id, course_id, section_no)
                          )

   ``conn.transaction()`` wraps the entire operation atomically.
   ``FOR UPDATE`` prevents the lost-update race condition. Business rules
   (capacity check, section existence) live here, not in the repository or
   CLI. Any exception automatically rolls back -- capacity is never
   decremented without a matching enrollment row.

   .. admonition:: Demo 10 -- EnrollmentService with FOR UPDATE
      :class: note

      Call ``enroll_student`` twice for the same section to exhaust
      capacity. On the third call confirm ``ValueError("Section is full")``
      is raised and no row was inserted. Verify capacity in psql.

      .. code-block:: python

         svc = EnrollmentService()
         svc.enroll_student(1, 'ENPM818T', '0101')  # capacity: 30 -> 29
         svc.enroll_student(2, 'ENPM818T', '0101')  # capacity: 29 -> 28
         # ... repeat until capacity = 0 ...
         svc.enroll_student(31, 'ENPM818T', '0101')
         # ValueError: Section is full
         # Verify in psql: capacity unchanged

   .. rubric:: Handling Database Errors in the Service Layer

   .. list-table::
      :widths: 35 45
      :header-rows: 1
      :class: compact-table

      * - **Python exception**
        - **PostgreSQL cause**
      * - ``UniqueViolation``
        - Duplicate PK or ``UNIQUE`` value
      * - ``ForeignKeyViolation``
        - Referenced row does not exist
      * - ``CheckViolation``
        - ``CHECK`` constraint failed
      * - ``NotNullViolation``
        - Required column is ``NULL``
      * - ``OperationalError``
        - Connection lost, server down

   All live in ``psycopg.errors``.

   .. code-block:: python

      # university_app/services/enrollment_service.py
      from psycopg.errors import UniqueViolation, ForeignKeyViolation

      def enroll_student(self, pid, cid, sec):
          try:
              with DatabaseConfig.get_connection() as conn:
                  with conn.transaction():
                      # ... INSERT enrollment ...
                      pass
          except UniqueViolation:
              raise ValueError("Already enrolled")
          except ForeignKeyViolation:
              raise ValueError("Student or section not found")

   Catch specific exceptions, not bare ``except Exception``. Translate
   database errors into domain errors (``ValueError``) for the CLI layer.
   The ``conn.transaction()`` block auto-rolls back before the exception
   reaches your ``except``.

   .. rubric:: The Full Call Stack: From Menu to Database and Back

   .. code-block:: python

      # university_app/cli/menu.py
      def main():
          svc = EnrollmentService()
          choice = input("Select option: ")
          if choice == "1":
              pid = int(input("Person ID: "))
              cid = input("Course ID: ")
              sec = input("Section: ")
              try:
                  svc.enroll_student(pid, cid, sec)
                  print("Enrolled successfully.")
              except ValueError as e:
                  print(f"Error: {e}")

      # services/enrollment_service.py
      #   -> opens conn.transaction()
      #   -> SELECT capacity ... FOR UPDATE
      #   -> checks capacity
      #   -> UPDATE course_section
      #   -> INSERT enrollment
      #   -> COMMIT on exit

      # repositories/student_repo.py
      #   find_by_id / find_all / create  (SQL strings live here)

   .. list-table::
      :widths: 18 82
      :header-rows: 1
      :class: compact-table

      * - **Layer**
        - **Responsibility**
      * - CLI
        - Read user input; call service; print result or error
      * - Service
        - Open transaction; enforce business rules
      * - Repository
        - Own SQL strings; return typed results
      * - Database
        - Execute statements; enforce constraints; commit

   The CLI never touches SQL. The service never reads from ``input()``.
   The repository never enforces business rules. If any of these cross,
   the design has a problem.

   .. admonition:: Exercise 3
      :class: note

      Complete before next class. Work in pairs; one person writes, the
      other reviews.

      1. **Connect**: create ``.env``, run the minimal connection script,
         and print the server version.
      2. **Safe query**: write ``find_student(student_id: str)`` using a
         parameterized query; return a dict row. Verify it returns ``None``
         for an unknown ID.
      3. **Injection check**: swap in an f-string query, pass
         ``' OR '1'='1``, observe the difference, then switch back to
         parameterized.
      4. **Repository**: implement ``find_by_id`` and ``create`` in
         ``StudentRepository``. ``create`` should insert into ``person``
         with ``RETURNING person_id``, then insert the ``student`` row
         inside ``conn.transaction()``.
      5. **CLI**: write a ``main()`` loop with two options: *1 -- Add
         student*, *2 -- Find student by ID*. All SQL stays in the
         repository; ``main()`` calls only service/repository methods.


.. dropdown:: Seeding the University Database
   :class-container: sd-border-secondary

   .. rubric:: Generating Realistic Seed Data with an LLM

   Use the following prompt template to generate ``INSERT`` statements for
   your GP2 database. Paste your actual DDL -- the LLM needs column names,
   types, and constraints.

   .. code-block:: text

      Given these CREATE TABLE statements: [paste your DDL here]

      Generate INSERT statements for:
        - 10 rows in 'department'
        - 20 rows in 'person' (DOB 1975-2005)
        - 20 rows in 'professor' (hire 2010-2024, rank_code in
          ('Assistant', 'Associate', 'Full'))
        - 20 rows in 'student' (admission 2022-2024, academic_standing in
          ('Good Standing', 'Probation', 'Suspended', 'Dismissed'))

      Rules:
        - Omit identity columns (person_id, dept_id)
        - Use RETURNING to thread person_id into professor/student inserts
        - All FK references must be valid
        - Wrap everything in BEGIN/COMMIT

   Specify ``CHECK`` vocabularies (``rank_code``, ``academic_standing``)
   explicitly. After you get the output: run it, paste any errors back, ask
   for a fix. Usually converges in two or three rounds. Validate with row
   counts after seeding.


Best Practices and Common Mistakes
====================================================

DML and Python mistakes are often silent: no error is raised but the data
is wrong, exposed, or missing.


.. dropdown:: Seven Common Mistakes
   :class-container: sd-border-secondary

   .. list-table::
      :widths: 5 40 55
      :header-rows: 1
      :class: compact-table

      * -
        - **Mistake**
        - **Fix**
      * - M1
        - ``UPDATE``/``DELETE`` without ``WHERE``
        - Run ``SELECT`` with the same ``WHERE`` first (UPDATE section)
      * - M2
        - String-concatenated SQL
        - Parameterized queries: ``cur.execute(sql, (val,))`` (Parameterized
          Queries section)
      * - M3
        - Hardcoded credentials
        - ``.env`` + ``os.getenv()`` + ``.gitignore`` (Connecting section)
      * - M4
        - ISA insert without ``RETURNING``
        - ``RETURNING person_id`` to thread PK into subtype (INSERT section)
      * - M5
        - New connection per query
        - ``psycopg_pool.ConnectionPool`` initialized once (Connection
          Pooling section)
      * - M6
        - Forgetting to commit
        - ``conn.transaction()`` auto-commits on exit (Autocommit slide)
      * - M7
        - ``import psycopg2`` with psycopg3 installed
        - Use ``import psycopg``; they are different packages

   All seven are silent: no error is raised, but the data is wrong,
   exposed, or missing. Use this table as a GP2 checklist before each
   submission.


Wrap-Up and Next Steps
====================================================


Key Takeaways
--------------

1. **Always include WHERE in UPDATE and DELETE.** An unguarded ``UPDATE``
   or ``DELETE`` modifies every row in the table silently. Run the
   equivalent ``SELECT`` first.

2. **Use RETURNING to thread generated keys.** ISA inserts require the
   exact ``person_id`` just created; ``RETURNING`` captures it atomically
   without a race condition.

3. **Wrap multi-statement operations in transactions.** ``BEGIN``/``COMMIT``
   guarantees that all steps succeed together or none take effect.

4. **Use SAVEPOINT for batch operations.** ``ROLLBACK TO SAVEPOINT`` undoes
   only the work after the marker; the transaction stays open.

5. **Parameterized queries are mandatory.** Never concatenate user input
   into SQL strings. Always use ``cur.execute(sql, (val,))``.

6. **Initialize the pool once at startup.** Never call
   ``psycopg.connect()`` directly inside repository methods or per-request.

7. **psycopg3 does not autocommit by default.** Use ``conn.transaction()``
   for DML; changes are invisible to other sessions until committed.


Quick Reference
---------------

.. seealso::

   :doc:`../../glossary/glossary` -- key terms from this lecture: DML
   statements, ACID properties, transaction isolation levels, ``RETURNING``,
   ``ON CONFLICT``, parameterized queries, connection pooling, and the
   repository pattern.
