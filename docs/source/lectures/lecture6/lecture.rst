====================================================
Lecture
====================================================



From Logical to Physical
====================================================


.. dropdown:: The Logical-to-Physical Gap
   :class-container: sd-border-secondary
   

   .. rubric:: What the Logical Schema Leaves Open

   The logical schema says *what* exists. SQL tells the database *how* to
   enforce it. Moving from logical to physical requires four additional
   decisions that the ERD does not make:

   1. **Exact data type** for every column -- ``INTEGER`` or ``NUMERIC``,
      ``VARCHAR(n)`` or ``TEXT``, ``SERIAL`` or ``GENERATED ALWAYS AS IDENTITY``.

   2. **Which constraints live in the database** versus in application code --
      every rule enforced by the schema cannot be violated by any client.

   3. **Creation order** -- parents must exist before children can reference
      them; circular FK dependencies require deferrable constraints.

   4. **PostgreSQL-specific features** that improve correctness -- identity
      columns, ``EXCLUDE`` constraints, ``NULLS NOT DISTINCT``.

   .. card::
       :class-card: sd-border-info

       **Analogy**: The logical schema is an architect's floor plan. The
       physical model is the construction specification: exact materials,
       load limits, and sequencing for every phase of the build.


.. dropdown:: SQL Sublanguages
   :class-container: sd-border-secondary

   .. rubric:: The Five SQL Sublanguages

   SQL is the ISO/IEC standard language for relational databases, organized
   into a family of sublanguages each targeting a different operation
   category. The current standard is SQL:2023.

   .. list-table::
      :widths: 22 10 20 28
      :header-rows: 1
      :class: compact-table

      * - **Sublanguage**
        - **Abbrev.**
        - **Purpose**
        - **Key Commands**
      * - Data Definition Language
        - DDL
        - Define and modify structure
        - ``CREATE``, ``ALTER``, ``DROP``, ``TRUNCATE``
      * - Data Manipulation Language
        - DML
        - Insert, update, delete rows
        - ``INSERT``, ``UPDATE``, ``DELETE``
      * - Data Query Language
        - DQL
        - Retrieve rows
        - ``SELECT``
      * - Data Control Language
        - DCL
        - Manage permissions
        - ``GRANT``, ``REVOKE``
      * - Transaction Control Language
        - TCL
        - Control transactions
        - ``BEGIN``, ``COMMIT``, ``ROLLBACK``

   .. card::
       :class-card: sd-border-info

       **Scope**: DDL is the focus of this lecture. DML and TCL are covered
       in L7. DQL (joins, aggregates) in L8. DCL in the administration module.


.. dropdown:: SQL Style Best Practices
   :class-container: sd-border-secondary

   .. rubric:: Writing Readable, Maintainable DDL

   .. code-block:: sql

      CREATE TABLE enrollment (
          student_id  INTEGER     NOT NULL,
          course_id   VARCHAR(10) NOT NULL,
          grade       CHAR(1),
          CONSTRAINT pk_enrollment
              PRIMARY KEY (student_id, course_id),
          CONSTRAINT fk_enroll_student
              FOREIGN KEY (student_id)
                  REFERENCES student(person_id)
                  ON DELETE CASCADE,
          CONSTRAINT chk_grade
              CHECK (grade IN ('A','B','C','D','F'))
      );

   Key conventions:

   - **Uppercase keywords**: ``CREATE``, ``NOT NULL``, ``REFERENCES``.
   - **Lowercase identifiers**: ``snake_case`` for tables and columns.
   - **One column per line**: easier to read and diff.
   - **Align types vertically**: structure is obvious at a glance.
   - **Named constraints**: ``pk_``, ``fk_``, ``chk_`` prefixes appear in error messages.
   - **Indent continuations**: ``REFERENCES`` indented under its constraint clause.


.. dropdown:: Setting Up in DataGrip
   :class-container: sd-border-secondary

   .. rubric:: Four Steps Before Writing Any DDL

   1. **Create the database.** Right-click the server in Database Explorer,
      choose **New > Database**, name it ``university_db``. Or run:

      .. code-block:: sql

         CREATE DATABASE university_db;

   2. **Point the console.** Open a Query Console and verify the database
      dropdown shows ``university_db``. Every DDL statement lands in
      whichever database that dropdown shows.

   3. **Select the schema.** Expand ``university_db`` in the explorer.
      If you see *"No schemas selected"*, click the three dots and check
      **public**.

   4. **Run the script.** Open ``lecture6_schema.sql`` via **File > Open**.
      Use ``Ctrl+Enter`` for the current statement or ``Ctrl+Shift+Enter``
      for the full file.

   .. tip::

      Always confirm the database dropdown before running any DDL.
      Running a ``DROP TABLE`` against the wrong database is a common and
      expensive mistake.



PostgreSQL Data Types
====================================================


.. dropdown:: Choosing the Right Type
   :class-container: sd-border-secondary
   

   .. rubric:: Type Selection Reference

   .. list-table::
      :widths: 18 22 40
      :header-rows: 1
      :class: compact-table

      * - **Type**
        - **University example**
        - **Rule of thumb**
      * - ``SMALLINT``
        - flags, small codes
        - 2-byte; avoid unless storage is critical
      * - ``INTEGER``
        - ``credits``, ``capacity``
        - Default choice for whole numbers
      * - ``BIGINT``
        - row counts, IDs at scale
        - Use when overflow is realistic
      * - ``NUMERIC(p,s)``
        - ``gpa``, ``budget``
        - Always for money and GPA; never ``FLOAT``
      * - ``VARCHAR(n)``
        - ``first_name``, ``email``
        - Only when the length limit is a real business rule
      * - ``TEXT``
        - ``description``
        - Unbounded; identical performance to ``VARCHAR`` in PostgreSQL
      * - ``CHAR(n)``
        - ``state``, ``zip``
        - Fixed-length; pads with spaces; use sparingly
      * - ``DATE``
        - ``hire_date``, ``date_of_birth``
        - Calendar date only; no time component
      * - ``TIMESTAMPTZ``
        - event logs
        - Always prefer over ``TIMESTAMP``; stores time zone offset
      * - ``BOOLEAN``
        - ``is_active``
        - ``TRUE`` / ``FALSE`` / ``NULL``: three-valued logic
      * - ``UUID``
        - distributed PKs
        - 128-bit; ``gen_random_uuid()`` requires no extension in PG 13+

   Full reference: `PostgreSQL data types <https://www.postgresql.org/docs/current/datatype.html>`__


.. dropdown:: Why Never FLOAT for GPA or Money
   :class-container: sd-border-secondary
   

   .. rubric:: Binary Floating-Point Cannot Represent Most Decimal Fractions Exactly

   Binary floating-point cannot represent most decimal fractions exactly.
   The value ``3.9`` stored as ``FLOAT`` becomes ``3.8999999...`` internally,
   so an equality comparison like ``WHERE gpa = 3.9`` may return zero rows
   even though the row exists.

   .. list-table::
      :widths: 25 35 35
      :header-rows: 1
      :class: compact-table

      * - **Value entered**
        - ``FLOAT`` stores
        - ``NUMERIC`` stores
      * - ``3.9``
        - ``3.8999999...``
        - ``3.9``
      * - ``0.1 + 0.2``
        - ``0.30000000000000004``
        - ``0.3``

   .. warning::

      Use ``NUMERIC(p,s)`` for any column where precision matters: GPA,
      tuition, budget. ``FLOAT`` is appropriate only for scientific
      measurements where approximate representation is acceptable.

   .. admonition:: Demo 1 -- FLOAT vs. NUMERIC for GPA
      :class: note

      Run both table examples and compare query results. Observe that
      ``SELECT gpa = 3.9 AS exact_match`` returns ``false`` for the FLOAT
      table and ``true`` for the NUMERIC table.

      .. code-block:: sql

         -- Step 1a: FLOAT (wrong choice)
         CREATE TABLE grade_wrong (
             student_id INTEGER,
             gpa        FLOAT
         );
         INSERT INTO grade_wrong VALUES (1, 3.9);

         -- May return 0 rows due to floating-point imprecision
         SELECT * FROM grade_wrong WHERE gpa = 3.9;

         -- See the stored value and why the comparison fails
         SELECT gpa, gpa = 3.9 AS exact_match FROM grade_wrong;

         DROP TABLE grade_wrong;

         -- Step 1b: NUMERIC (correct choice)
         CREATE TABLE grade_correct (
             student_id INTEGER,
             gpa        NUMERIC(3,2)
         );
         INSERT INTO grade_correct VALUES (1, 3.9);

         -- Returns the row; exact decimal storage guarantees the match
         SELECT * FROM grade_correct WHERE gpa = 3.9;

         -- Stored value is exact; comparison returns true
         SELECT gpa, gpa = 3.9 AS exact_match FROM grade_correct;

         DROP TABLE grade_correct;


.. dropdown:: Text Types: VARCHAR, TEXT, and CHAR
   :class-container: sd-border-secondary

   .. rubric:: Three String Types, Three Different Use Cases

   .. list-table::
      :widths: 15 20 45
      :header-rows: 1
      :class: compact-table

      * - **Type**
        - **Storage**
        - **When to use**
      * - ``VARCHAR(n)``
        - Up to n characters
        - Only when n is a real business rule (e.g., ``CHAR(2)`` for US state codes)
      * - ``TEXT``
        - Unlimited
        - Default for all variable-length strings; same performance as ``VARCHAR`` in PostgreSQL
      * - ``CHAR(n)``
        - Exactly n characters (padded)
        - Fixed-width codes only: ``state CHAR(2)``, ``zip CHAR(5)``

   .. card::
       :class-card: sd-border-info

       **Common mistake**: Using ``VARCHAR(255)`` out of habit. In PostgreSQL,
       ``TEXT`` and ``VARCHAR`` have identical internal storage and performance.
       Use ``TEXT`` unless the length limit encodes a genuine business rule.



Constraints
====================================================


.. dropdown:: PRIMARY KEY
   :class-container: sd-border-secondary
   

   .. rubric:: Declaring Primary Keys: Simple and Composite

   A ``PRIMARY KEY`` constraint combines ``NOT NULL`` and ``UNIQUE``
   automatically. It may be declared at the column level (single-attribute
   PKs) or at the table level (required for composite PKs and for named
   constraints).

   .. admonition:: Demo 2 -- PRIMARY KEY: Simple and Composite
      :class: note

      Create all three tables and insert valid rows. Then attempt a duplicate
      insert on each and compare the error messages: the unnamed constraint
      produces ``"department_pkey"``; the named constraint produces
      ``"pk_course"``.

      .. code-block:: sql

         -- Step 2a: simple PK, column-level (unnamed)
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );

         -- Step 2b: simple PK, table-level (named)
         CREATE TABLE course (
             course_id VARCHAR(10)  NOT NULL,
             title     VARCHAR(150) NOT NULL,
             CONSTRAINT pk_course PRIMARY KEY (course_id)
         );

         -- Step 2c: composite PK, table-level (named)
         CREATE TABLE enrollment (
             student_id INTEGER     NOT NULL,
             course_id  VARCHAR(10) NOT NULL,
             semester   CHAR(6)     NOT NULL,
             grade      CHAR(1),
             CONSTRAINT pk_enrollment
                 PRIMARY KEY (student_id, course_id, semester)
         );

         -- Inspect constraint names in psql:
         -- \d department  -> "department_pkey" (system-generated)
         -- \d course      -> "pk_course" (named)
         -- \d enrollment  -> "pk_enrollment" (named)

         -- Step 2d: insert valid rows
         INSERT INTO enrollment (student_id, course_id, semester)
             VALUES (42, 'ENPM818T', '202601');
         INSERT INTO enrollment (student_id, course_id, semester)
             VALUES (42, 'ENPM605',  '202601');

         -- Step 2e: attempt duplicate triple; observe error naming pk_enrollment
         INSERT INTO enrollment (student_id, course_id, semester)
             VALUES (42, 'ENPM818T', '202601');
         -- ERROR: duplicate key value violates unique constraint "pk_enrollment"

         DROP TABLE enrollment;
         DROP TABLE course;
         DROP TABLE department;


   .. admonition:: Demo 3 -- Named vs. Unnamed PRIMARY KEY Constraints
      :class: note

      Compare the error messages from an unnamed vs. a named PK constraint.
      Observe that the named constraint (``pk_course``) produces immediately
      actionable error messages while the system-generated name
      (``department_pkey``) is harder to interpret.

      .. code-block:: sql

         -- Step 3a: unnamed PK (system generates the name)
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );

         INSERT INTO department OVERRIDING SYSTEM VALUE
             VALUES (1, 'Engineering');
         -- Error message says "department_pkey" (not descriptive)
         INSERT INTO department OVERRIDING SYSTEM VALUE
             VALUES (1, 'Mathematics');
         -- ERROR: duplicate key value violates unique constraint "department_pkey"

         -- Step 3b: named PK (your prefix appears in the error)
         CREATE TABLE course (
             course_id VARCHAR(10)  NOT NULL,
             title     VARCHAR(150) NOT NULL,
             CONSTRAINT pk_course PRIMARY KEY (course_id)
         );

         INSERT INTO course VALUES ('ENPM818T', 'Databases');
         -- Error message says "pk_course" (immediately actionable)
         INSERT INTO course VALUES ('ENPM818T', 'Databases');
         -- ERROR: duplicate key value violates unique constraint "pk_course"

         -- Inspect in psql:
         -- \d department  -> "department_pkey PRIMARY KEY"
         -- \d course      -> "pk_course PRIMARY KEY"

         DROP TABLE course;
         DROP TABLE department;


.. dropdown:: SERIAL vs. GENERATED ALWAYS AS IDENTITY
   :class-container: sd-border-secondary
   

   .. rubric:: Auto-Incrementing Primary Keys: The Old Way and the Right Way

   ``SERIAL`` wires the sequence as a ``DEFAULT``: bypassing it with an
   explicit value is silent and undetected. ``GENERATED ALWAYS AS IDENTITY``
   hands ownership to the engine: inserting a manual value raises an
   immediate error.

   .. list-table::
      :widths: 40 30 30
      :header-rows: 1
      :class: compact-table

      * - **Property**
        - ``SERIAL``
        - ``GENERATED ALWAYS``
      * - SQL standard
        - No
        - Yes (SQL:2003)
      * - Explicit bypass
        - Silent (no error)
        - Immediate error
      * - Visible in ``\d``
        - No
        - Yes
      * - Customizable inline
        - No
        - Yes

   .. admonition:: Demo 4 -- SERIAL Silent Bypass
      :class: note

      Run the three inserts exactly as shown. Observe that Steps 1 and 2
      succeed silently even though the sequence is bypassed. Run
      ``SELECT last_value FROM department_dept_id_seq`` after Step 2 to
      confirm the counter is still 1. Run Step 3 and observe the duplicate
      key error. Note that the bug was introduced two steps earlier with no
      warning.

      .. code-block:: sql

         CREATE TABLE department (
             dept_id   SERIAL PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );

         -- Step 1: explicit insert; sequence counter never advances
         INSERT INTO department (dept_id, dept_name)
             VALUES (1, 'Computer Science');

         -- Step 2: explicit insert; sequence counter still frozen at 1
         INSERT INTO department (dept_id, dept_name)
             VALUES (2, 'Mathematics');

         -- Counter is still 1 despite two rows existing
         SELECT last_value FROM department_dept_id_seq;

         -- Step 3: auto insert; nextval() returns 1 and collides with row 1
         INSERT INTO department (dept_name)
             VALUES ('Physics');
         -- ERROR: duplicate key value violates unique constraint "department_pkey"
         -- DETAIL: Key (dept_id)=(1) already exists.

         DROP TABLE department;


   .. admonition:: Demo 5 -- GENERATED ALWAYS AS IDENTITY: The Safe Alternative
      :class: note

      Attempt the explicit bypass insert and observe the immediate error.
      Run ``OVERRIDING SYSTEM VALUE`` and confirm it succeeds. Run
      ``SELECT last_value FROM department_dept_id_seq`` and confirm the
      counter is still 1 despite the row existing. Drop and recreate with
      ``START WITH 1000`` and run ``\d department`` to confirm the custom
      sequence start.

      .. code-block:: sql

         CREATE TABLE department (
             dept_id   INTEGER
                 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );

         -- Bypass attempt: rejected immediately
         INSERT INTO department (dept_id, dept_name)
             VALUES (1, 'Computer Science');
         -- ERROR: cannot insert into column "dept_id"
         -- DETAIL: Column "dept_id" is an identity column defined as GENERATED ALWAYS

         -- Legal override: succeeds but does not advance the sequence
         INSERT INTO department (dept_id, dept_name)
             OVERRIDING SYSTEM VALUE
             VALUES (1, 'Computer Science');

         -- Counter is still 1 despite the row existing
         SELECT last_value FROM department_dept_id_seq;

         DROP TABLE department;

         -- Customized sequence: starts at 1000
         CREATE TABLE department (
             dept_id   INTEGER
                 GENERATED ALWAYS AS IDENTITY
                     (START WITH 1000 INCREMENT BY 1)
                 PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );

         INSERT INTO department (dept_name) VALUES ('Computer Science');
         INSERT INTO department (dept_name) VALUES ('Mathematics');

         -- Observe: dept_id values are 1000 and 1001
         SELECT * FROM department;

         DROP TABLE department;


.. dropdown:: ISA as a Shared-PK Pattern
   :class-container: sd-border-secondary
   

   .. rubric:: Implementing ISA Hierarchies in SQL

   In the shared-PK strategy, each subtype table uses the same primary key
   value as its supertype row. The subtype PK is simultaneously a FK
   referencing the supertype, so a subtype row cannot exist without a
   matching supertype row. The identity sequence lives on the supertype only.

   Key rules:

   - ``student.person_id`` has the type ``INTEGER PRIMARY KEY`` with no ``GENERATED ALWAYS``; the value comes from the supertype insert.
   - ``ON DELETE CASCADE`` removes the student row automatically when the person row is deleted.
   - The hierarchy can be arbitrarily deep: ``grad_student`` is a subtype of ``student``, which is a subtype of ``person``.
   - No new sequence is created on the subtype; only one identity column exists per entity hierarchy.

   .. admonition:: Think Prompt
      :class: hint

      ``student.person_id`` uses ``INTEGER PRIMARY KEY`` with no
      ``GENERATED ALWAYS``. Why? What would happen if you added
      ``GENERATED ALWAYS AS IDENTITY`` to it?

   .. dropdown:: Answer
      :class-container: sd-border-success

      The subtype PK must carry the same value as the supertype PK; that is
      the entire point of the shared-PK strategy. The identity sequence lives
      on ``person.person_id``; ``student.person_id`` receives that value via
      the application insert. Adding ``GENERATED ALWAYS AS IDENTITY`` to
      ``student.person_id`` would create an independent sequence starting at 1.
      The value inserted into ``student`` would then be determined by this new
      sequence rather than by the ``person`` row being linked, which immediately
      breaks the shared-PK relationship: the two tables would assign different
      IDs to the same entity.

   .. admonition:: Demo 6 -- ISA Shared-PK Pattern
      :class: note

      Create both tables and insert Alice and Bob into ``person``. Insert the
      matching ``student`` rows using the generated ``person_id`` values.
      Attempt to insert ``person_id = 99`` into ``student`` and observe the FK
      violation. Then delete Alice from ``person`` and run
      ``SELECT * FROM student`` to confirm her student row was removed
      automatically by ``ON DELETE CASCADE``.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER
                 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );

         CREATE TABLE student (
             person_id  INTEGER PRIMARY KEY,
             student_id VARCHAR(20) NOT NULL UNIQUE,
             CONSTRAINT fk_student_person
                 FOREIGN KEY (person_id)
                     REFERENCES person (person_id)
                     ON DELETE CASCADE
         );

         -- Insert supertypes; identity is generated here only
         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');

         -- Insert subtypes using the generated person_id values
         INSERT INTO student (person_id, student_id) VALUES (1, '117453210');
         INSERT INTO student (person_id, student_id) VALUES (2, '117453211');

         -- Observe: both rows exist in both tables
         SELECT * FROM person;
         SELECT * FROM student;

         -- Attempt to insert a student with no matching person row
         INSERT INTO student (person_id, student_id) VALUES (99, '117453299');
         -- ERROR: insert or update on table "student" violates foreign key
         -- constraint "fk_student_person"

         -- Delete Alice from person; CASCADE removes her student row too
         DELETE FROM person WHERE person_id = 1;

         SELECT * FROM person;   -- Alice gone
         SELECT * FROM student;  -- Alice's student row gone automatically

         DROP TABLE student;
         DROP TABLE person;


.. dropdown:: FOREIGN KEY: Syntax and Options
   :class-container: sd-border-secondary
   

   .. rubric:: Referential Integrity Between Tables

   A ``FOREIGN KEY`` constraint enforces that the child column's value must
   match a value present in the parent table's ``PRIMARY KEY`` or ``UNIQUE``
   column. Any insert or update that would leave the child referencing a
   non-existent parent row is rejected immediately.

   ``ON DELETE`` / ``ON UPDATE`` actions:

   .. list-table::
      :widths: 25 35 30
      :header-rows: 1
      :class: compact-table

      * - **Action**
        - **Effect on child rows**
        - **Use when...**
      * - ``NO ACTION`` (default)
        - Parent change blocked at statement end; deferrable
        - General-purpose default
      * - ``RESTRICT``
        - Parent change blocked immediately; never deferrable
        - Orphaning is always a mistake
      * - ``CASCADE``
        - Child rows deleted or updated to match
        - Child has no meaning without the parent
      * - ``SET NULL``
        - FK column set to ``NULL``
        - Child survives independently; column must be nullable
      * - ``SET DEFAULT``
        - FK column reset to its default
        - Sentinel/fallback parent row always exists

   .. admonition:: Demo 7 -- NO ACTION vs. RESTRICT
      :class: note

      Create both professor variants. With ``RESTRICT``, observe that the
      error fires before the statement completes. With ``NO ACTION``, the
      error fires at end of statement. With ``NO ACTION DEFERRABLE``,
      observe that deleting both child and parent inside the same transaction
      satisfies the FK at ``COMMIT`` with no error.

      .. code-block:: sql

         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );
         INSERT INTO department (dept_name) VALUES ('Computer Science');

         -- Variant A: RESTRICT -- error fires immediately
         CREATE TABLE professor_restrict (
             person_id INTEGER PRIMARY KEY,
             dept_id   INTEGER,
             CONSTRAINT fk_prof_restrict
                 FOREIGN KEY (dept_id)
                     REFERENCES department (dept_id)
                     ON DELETE RESTRICT
         );
         INSERT INTO professor_restrict VALUES (1, 1);

         BEGIN;
             DELETE FROM department WHERE dept_id = 1;
             -- ERROR fires before statement completes
         ROLLBACK;

         -- Variant B: NO ACTION -- error fires at end of statement
         CREATE TABLE professor_no_action (
             person_id INTEGER PRIMARY KEY,
             dept_id   INTEGER,
             CONSTRAINT fk_prof_no_action
                 FOREIGN KEY (dept_id)
                     REFERENCES department (dept_id)
                     ON DELETE NO ACTION
         );
         INSERT INTO professor_no_action VALUES (1, 1);

         BEGIN;
             DELETE FROM department WHERE dept_id = 1;
             -- ERROR: same violation, fires at end of statement
         ROLLBACK;

         -- Variant C: NO ACTION DEFERRABLE -- check deferred to COMMIT
         CREATE TABLE professor_deferred (
             person_id INTEGER PRIMARY KEY,
             dept_id   INTEGER,
             CONSTRAINT fk_prof_deferred
                 FOREIGN KEY (dept_id)
                     REFERENCES department (dept_id)
                     ON DELETE NO ACTION
                     DEFERRABLE INITIALLY DEFERRED
         );
         INSERT INTO professor_deferred VALUES (1, 1);

         -- Deleting both child and parent inside one transaction satisfies
         -- the FK at COMMIT; no error
         BEGIN;
             DELETE FROM professor_deferred WHERE dept_id = 1;
             DELETE FROM department WHERE dept_id = 1;
         COMMIT;

         SELECT * FROM professor_deferred;
         SELECT * FROM department;

         DROP TABLE professor_deferred;
         DROP TABLE professor_no_action;
         DROP TABLE professor_restrict;
         DROP TABLE department;


   .. admonition:: Demo 8 -- ON DELETE CASCADE
      :class: note

      Insert Alice and Bob into ``person``, their ``student`` rows, and
      three enrollment rows. Delete Alice from ``student`` and confirm that
      her two enrollment rows disappear automatically via ``CASCADE``.
      Bob's enrollment row remains untouched.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         CREATE TABLE student (
             person_id  INTEGER PRIMARY KEY,
             student_id VARCHAR(20) NOT NULL UNIQUE,
             CONSTRAINT fk_student_person
                 FOREIGN KEY (person_id)
                     REFERENCES person (person_id)
                     ON DELETE CASCADE
         );
         CREATE TABLE enrollment (
             person_id  INTEGER     NOT NULL,
             course_id  VARCHAR(20) NOT NULL,
             section_no VARCHAR(20) NOT NULL,
             grade      VARCHAR(2),
             CONSTRAINT fk_enr_student
                 FOREIGN KEY (person_id)
                     REFERENCES student (person_id)
                     ON DELETE CASCADE
         );

         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');
         INSERT INTO student VALUES (1, '117453210');
         INSERT INTO student VALUES (2, '117453211');
         INSERT INTO enrollment VALUES (1, 'CS301', '101',  'A');
         INSERT INTO enrollment VALUES (1, 'CS401', 'A01',  'B+');
         INSERT INTO enrollment VALUES (2, 'CS301', 'R002', 'A-');

         -- Three enrollment rows exist
         SELECT * FROM enrollment;

         -- Delete student 1 (Alice); CASCADE removes her enrollment rows
         DELETE FROM student WHERE person_id = 1;

         -- Only Bob's enrollment row remains
         SELECT * FROM enrollment;

         DROP TABLE enrollment;
         DROP TABLE student;
         DROP TABLE person;


   .. admonition:: Demo 9 -- ON DELETE SET NULL
      :class: note

      Insert Alice and Bob as professors in Computer Science and Carol in
      Mathematics. Delete the CS department and confirm Alice and Bob
      survive with ``dept_id = NULL``. Then attempt to add ``NOT NULL``
      to ``dept_id`` and observe that it fails because the column already
      contains null values, demonstrating why ``SET NULL`` requires a
      nullable column.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );
         CREATE TABLE professor (
             person_id INTEGER PRIMARY KEY
                 REFERENCES person (person_id) ON DELETE CASCADE,
             dept_id   INTEGER,
             CONSTRAINT fk_prof_dept
                 FOREIGN KEY (dept_id)
                     REFERENCES department (dept_id)
                     ON DELETE SET NULL
         );

         INSERT INTO department (dept_name) VALUES ('Computer Science'); -- dept_id = 1
         INSERT INTO department (dept_name) VALUES ('Mathematics');      -- dept_id = 2
         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');
         INSERT INTO person (first_name, last_name) VALUES ('Carol', 'Davis');
         INSERT INTO professor VALUES (1, 1);
         INSERT INTO professor VALUES (2, 1);
         INSERT INTO professor VALUES (3, 2);

         -- Alice and Bob assigned to dept 1
         SELECT p.first_name, pr.dept_id
         FROM professor pr JOIN person p ON pr.person_id = p.person_id;

         -- Delete CS department; Alice and Bob survive with dept_id = NULL
         DELETE FROM department WHERE dept_id = 1;

         -- Alice and Bob unassigned; Carol unchanged
         SELECT p.first_name, pr.dept_id
         FROM professor pr JOIN person p ON pr.person_id = p.person_id;

         -- Demonstrate why SET NULL requires a nullable column
         ALTER TABLE professor ALTER COLUMN dept_id SET NOT NULL;
         -- ERROR: column "dept_id" of relation "professor" contains null values

         DROP TABLE professor;
         DROP TABLE department;
         DROP TABLE person;


   .. admonition:: Demo 10 -- ON DELETE SET DEFAULT
      :class: note

      Insert professors assigned to CS (dept 1). Delete CS and confirm that
      Alice and Bob fall back to dept 0 (Unassigned). Then delete the
      Unassigned sentinel and attempt the same delete again to observe that
      ``SET DEFAULT`` fails when the default value does not exist as a valid
      FK target.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );

         -- Sentinel row: dept_id = 0 (Unassigned)
         INSERT INTO department OVERRIDING SYSTEM VALUE
             VALUES (0, 'Unassigned');
         INSERT INTO department (dept_name) VALUES ('Computer Science');  -- 1
         INSERT INTO department (dept_name) VALUES ('Mathematics');       -- 2

         CREATE TABLE professor (
             person_id INTEGER PRIMARY KEY
                 REFERENCES person (person_id) ON DELETE CASCADE,
             dept_id   INTEGER DEFAULT 0,
             CONSTRAINT fk_prof_dept
                 FOREIGN KEY (dept_id)
                     REFERENCES department (dept_id)
                     ON DELETE SET DEFAULT
         );

         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');
         INSERT INTO person (first_name, last_name) VALUES ('Carol', 'Davis');
         INSERT INTO professor VALUES (1, 1);
         INSERT INTO professor VALUES (2, 1);
         INSERT INTO professor VALUES (3, 2);

         -- Alice and Bob in dept 1
         SELECT p.first_name, pr.dept_id
         FROM professor pr JOIN person p ON pr.person_id = p.person_id;

         -- Delete CS; Alice and Bob fall back to dept_id = 0 (Unassigned)
         DELETE FROM department WHERE dept_id = 1;

         -- Alice and Bob now in dept 0; Carol unchanged
         SELECT p.first_name, pr.dept_id
         FROM professor pr JOIN person p ON pr.person_id = p.person_id;

         -- Delete the Unassigned sentinel and try again
         DELETE FROM department WHERE dept_id = 0;
         INSERT INTO professor VALUES (1, 2);
         DELETE FROM department WHERE dept_id = 2;
         -- ERROR: Key (dept_id)=(0) is not present in table "department"

         DROP TABLE professor;
         DROP TABLE department;
         DROP TABLE person;


.. dropdown:: Deferrable Foreign Keys
   :class-container: sd-border-secondary
   

   .. rubric:: Resolving Circular FK Dependencies

   When two tables reference each other (e.g., ``department.chair_id``
   references ``professor``, and ``professor.dept_id`` references
   ``department``), no valid insert order exists with immediate FK checking.
   The solution is ``DEFERRABLE INITIALLY DEFERRED``: move the FK check from
   statement end to transaction commit.

   Two deferral modes:

   - **Mode 1** (``DEFERRABLE INITIALLY DEFERRED``): FK is always deferred to ``COMMIT``; use for circular dependencies.
   - **Mode 2** (``DEFERRABLE INITIALLY IMMEDIATE``): FK fires at statement end by default; a specific transaction can opt in via ``SET CONSTRAINTS fk_name DEFERRED``.

   Only structural constraints support deferral: ``FOREIGN KEY``, ``UNIQUE``,
   and ``PRIMARY KEY``. ``NOT NULL`` and ``CHECK`` cannot be deferred.

   .. admonition:: Demo 11 -- Deferrable Foreign Keys: The Solution
      :class: note

      Run the ``BEGIN``/``COMMIT`` block as shown and confirm it succeeds.
      Then run each of the three statements as standalone statements outside
      a transaction and observe that the second fails immediately because
      ``chair_id`` references a professor that does not exist yet. Finally
      recreate ``department`` with ``NOT DEFERRABLE`` and confirm that even
      inside ``BEGIN``/``COMMIT`` the FK violation fires immediately on the
      ``UPDATE``.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');

         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL UNIQUE,
             chair_id  INTEGER UNIQUE,
             CONSTRAINT fk_dept_chair
                 FOREIGN KEY (chair_id)
                     REFERENCES professor (person_id)
                     ON DELETE SET NULL
                     DEFERRABLE INITIALLY DEFERRED
         );

         CREATE TABLE professor (
             person_id INTEGER PRIMARY KEY
                 REFERENCES person (person_id) ON DELETE CASCADE,
             dept_id   INTEGER NOT NULL,
             hire_date DATE    NOT NULL,
             rank_code VARCHAR(20) NOT NULL,
             CONSTRAINT fk_prof_dept
                 FOREIGN KEY (dept_id)
                     REFERENCES department (dept_id)
                     ON DELETE RESTRICT
         );

         -- Step 11a: three-step pattern inside a transaction
         -- FK check is deferred to COMMIT; temporary inconsistency is tolerated
         BEGIN;
             INSERT INTO department (dept_name) VALUES ('Computer Science');
             INSERT INTO professor (person_id, dept_id, hire_date, rank_code)
                 VALUES (1, 1, CURRENT_DATE, 'Associate');
             UPDATE department
                 SET chair_id = 1
                 WHERE dept_name = 'Computer Science';
         COMMIT;
         -- Observe: succeeds

         -- Step 11b: same inserts without BEGIN/COMMIT; fails immediately
         UPDATE department SET chair_id = 1 WHERE dept_name = 'Computer Science';
         -- ERROR if professor row did not exist yet

         DROP TABLE professor;
         DROP TABLE department;
         DROP TABLE person;


   .. admonition:: Demo 12 -- Deferrable FK Syntax: Mode 1 vs. Mode 2
      :class: note

      Create ``department`` with Mode 1 (``DEFERRABLE INITIALLY DEFERRED``).
      Run the circular insert inside ``BEGIN``/``COMMIT`` and confirm it
      succeeds without any ``SET CONSTRAINTS`` call. Drop and recreate with
      Mode 2 (``DEFERRABLE INITIALLY IMMEDIATE``). Run the same block without
      ``SET CONSTRAINTS`` and observe the immediate error. Then add
      ``SET CONSTRAINTS fk_dept_chair DEFERRED`` at the top of the
      transaction and confirm it succeeds.

      .. code-block:: sql

         -- Mode 1: DEFERRABLE INITIALLY DEFERRED
         -- Check postponed to COMMIT automatically for every transaction
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL UNIQUE,
             chair_id  INTEGER UNIQUE,
             CONSTRAINT fk_dept_chair
                 FOREIGN KEY (chair_id)
                     REFERENCES professor (person_id)
                     ON DELETE SET NULL
                     DEFERRABLE INITIALLY DEFERRED
         );

         -- No SET CONSTRAINTS needed; deferral is automatic
         BEGIN;
             INSERT INTO department (dept_name) VALUES ('Computer Science');
             INSERT INTO professor (person_id, dept_id, hire_date, rank_code)
                 VALUES (1, 1, CURRENT_DATE, 'Associate');
             UPDATE department SET chair_id = 1 WHERE dept_name = 'Computer Science';
         COMMIT;
         -- Observe: succeeds with no extra syntax

         DROP TABLE professor;
         DROP TABLE department;

         -- Mode 2: DEFERRABLE INITIALLY IMMEDIATE
         -- Immediate by default; transactions must opt in explicitly
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL UNIQUE,
             chair_id  INTEGER UNIQUE,
             CONSTRAINT fk_dept_chair
                 FOREIGN KEY (chair_id)
                     REFERENCES professor (person_id)
                     ON DELETE SET NULL
                     DEFERRABLE INITIALLY IMMEDIATE
         );

         -- Without SET CONSTRAINTS: error fires immediately
         BEGIN;
             INSERT INTO department (dept_name) VALUES ('Computer Science');
             INSERT INTO professor (person_id, dept_id, hire_date, rank_code)
                 VALUES (1, 1, CURRENT_DATE, 'Associate');
             UPDATE department SET chair_id = 1 WHERE dept_name = 'Computer Science';
             -- ERROR: fk_dept_chair violation fires immediately
         ROLLBACK;

         -- With SET CONSTRAINTS: transaction opts in; succeeds
         BEGIN;
             SET CONSTRAINTS fk_dept_chair DEFERRED;
             INSERT INTO department (dept_name) VALUES ('Computer Science');
             INSERT INTO professor (person_id, dept_id, hire_date, rank_code)
                 VALUES (1, 1, CURRENT_DATE, 'Associate');
             UPDATE department SET chair_id = 1 WHERE dept_name = 'Computer Science';
         COMMIT;

         DROP TABLE professor;
         DROP TABLE department;
         DROP TABLE person;


.. dropdown:: NOT NULL and UNIQUE
   :class-container: sd-border-secondary
   

   .. rubric:: Two Independent Questions for Every Column

   For every column, ask two independent questions before writing the
   ``CREATE TABLE`` statement:

   1. **Can a row legally exist without a value in this column?** If no, add ``NOT NULL``.
   2. **Can two rows ever share the same value?** If no, add ``UNIQUE``.

   ``PRIMARY KEY`` answers both questions simultaneously: it is shorthand
   for ``NOT NULL`` plus ``UNIQUE``.

   .. warning::

      ``NOT NULL`` and ``CHECK`` are **not** redundant. A column declared
      ``CHECK (gpa >= 0.0)`` without ``NOT NULL`` will silently accept
      ``NULL`` values because ``NULL`` is not ``< 0.0`` in SQL's three-valued
      logic. Always pair a ``CHECK`` constraint with ``NOT NULL`` unless
      ``NULL`` is a legitimate value.

   .. admonition:: Demo 13 -- UNIQUE and the NULL Trap
      :class: note

      Run all four inserts and confirm the fourth fails with a duplicate key
      error on ``plate``. Run ``SELECT * FROM vehicle`` and confirm rows 1
      and 2 coexist despite both having ``plate = NULL``. Then run
      ``SELECT plate, plate = plate AS self_equal FROM vehicle WHERE vehicle_id = 1``
      and observe that a value compared to itself returns ``NULL`` when the
      value is ``NULL``. Finally attempt to add ``NOT NULL`` to ``plate``
      with ``ALTER TABLE`` and confirm that both ``NULL`` rows block the
      operation.

      .. code-block:: sql

         CREATE TABLE vehicle (
             vehicle_id INTEGER
                 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             make       VARCHAR(50) NOT NULL,
             model      VARCHAR(50) NOT NULL,
             plate      VARCHAR(10) UNIQUE
         );

         INSERT INTO vehicle (make, model)
             VALUES ('Toyota', 'Camry');             -- OK
         INSERT INTO vehicle (make, model)
             VALUES ('Honda',  'Civic');             -- OK
         INSERT INTO vehicle (make, model, plate)
             VALUES ('Ford', 'F-150', 'ABC-1234');  -- OK
         INSERT INTO vehicle (make, model, plate)
             VALUES ('BMW',  'X5',    'ABC-1234');  -- FAIL
         -- ERROR: duplicate key value violates unique constraint "vehicle_plate_key"

         -- Rows 1 and 2 coexist despite both having plate = NULL
         SELECT * FROM vehicle;

         -- NULL compared to itself returns NULL, not TRUE
         SELECT plate, plate = plate AS self_equal
         FROM vehicle WHERE vehicle_id = 1;

         -- Adding NOT NULL fails because two NULL rows already exist
         ALTER TABLE vehicle ALTER COLUMN plate SET NOT NULL;
         -- ERROR: column "plate" of relation "vehicle" contains null values

         DROP TABLE vehicle;


   .. admonition:: Demo 14 -- UNIQUE NULLS NOT DISTINCT
      :class: note

      Run all four inserts with ``NULLS NOT DISTINCT`` and confirm the fourth
      fails. Run ``SELECT * FROM device`` and confirm three rows exist: two
      with distinct serial numbers and one with ``NULL``. Drop and recreate
      with plain ``UNIQUE`` instead of ``NULLS NOT DISTINCT`` and run the
      same four inserts; confirm all four now succeed, demonstrating that
      standard ``UNIQUE`` treats every ``NULL`` as distinct.

      .. code-block:: sql

         -- Step 14a: NULLS NOT DISTINCT -- at most one NULL allowed
         CREATE TABLE device (
             device_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             model     VARCHAR(50) NOT NULL,
             serial_no VARCHAR(30) UNIQUE NULLS NOT DISTINCT
         );

         INSERT INTO device (model, serial_no) VALUES ('RoboArm X1', 'SN-00142'); -- OK
         INSERT INTO device (model, serial_no) VALUES ('RoboArm X1', 'SN-00143'); -- OK
         INSERT INTO device (model)            VALUES ('RoboArm X1');              -- OK
         INSERT INTO device (model)            VALUES ('RoboArm X1');              -- FAIL
         -- ERROR: duplicate key value violates unique constraint "device_serial_no_key"

         -- Three rows exist; only one NULL is present
         SELECT * FROM device;

         DROP TABLE device;

         -- Step 14b: plain UNIQUE -- multiple NULLs allowed
         CREATE TABLE device (
             device_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             model     VARCHAR(50) NOT NULL,
             serial_no VARCHAR(30) UNIQUE
         );

         INSERT INTO device (model, serial_no) VALUES ('RoboArm X1', 'SN-00142'); -- OK
         INSERT INTO device (model, serial_no) VALUES ('RoboArm X1', 'SN-00143'); -- OK
         INSERT INTO device (model)            VALUES ('RoboArm X1');              -- OK
         INSERT INTO device (model)            VALUES ('RoboArm X1');              -- OK

         -- Four rows exist; two NULLs coexist
         SELECT * FROM device;

         DROP TABLE device;


.. dropdown:: CHECK Constraints
   :class-container: sd-border-secondary
   

   .. rubric:: Row-Level Business Rule Enforcement

   A ``CHECK`` constraint evaluates a Boolean expression for every inserted
   or updated row. If the expression evaluates to ``FALSE``, the operation
   is rejected. If it evaluates to ``NULL`` (because an operand is ``NULL``),
   the row is **accepted** -- which is the ``NULL`` trap.

   .. admonition:: Think Prompt
      :class: hint

      You add ``gpa NUMERIC(3,2) CHECK (gpa >= 0.0)`` without ``NOT NULL``.
      A client inserts a row with ``gpa = NULL``. Is the row accepted?

   .. dropdown:: Answer
      :class-container: sd-border-success

      Yes, the row is accepted. ``NULL >= 0.0`` evaluates to ``NULL``, not
      ``FALSE``. The ``CHECK`` constraint only rejects rows where the
      expression is definitively ``FALSE``. ``NULL`` means "unknown", so the
      check passes silently. The fix is to add ``NOT NULL`` alongside the
      ``CHECK``.

   .. admonition:: Demo 15 -- CHECK Constraints
      :class: note

      **Step 15a**: Insert the valid contract row and confirm it succeeds.
      Attempt the two invalid rows (end before start; equal dates) and
      observe the ``chk_dates`` error. Then drop ``NOT NULL`` from
      ``end_date`` and insert a row with ``end_date = NULL``; confirm it
      is accepted because ``CHECK`` evaluates to ``UNKNOWN``, not ``FALSE``.

      **Step 15b**: Insert a student with a valid standing and confirm it
      succeeds. Attempt ``'Expelled'`` and observe the ``chk_standing``
      error. Attempt ``NULL`` and observe the ``NOT NULL`` error, confirming
      that ``NOT NULL`` and ``CHECK`` are independent guards.

      .. code-block:: sql

         -- Step 15a: date range check
         CREATE TABLE contract (
             id         INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             start_date DATE NOT NULL,
             end_date   DATE NOT NULL,
             CONSTRAINT chk_dates CHECK (start_date < end_date)
         );

         INSERT INTO contract (start_date, end_date)
             VALUES ('2026-01-01', '2026-12-31');  -- OK
         INSERT INTO contract (start_date, end_date)
             VALUES ('2026-06-01', '2026-01-01');  -- FAIL: end before start
         -- ERROR: new row for relation "contract" violates check constraint "chk_dates"

         INSERT INTO contract (start_date, end_date)
             VALUES ('2026-03-01', '2026-03-01');  -- FAIL: equal dates
         -- ERROR: new row for relation "contract" violates check constraint "chk_dates"

         -- NULL trap: drop NOT NULL to expose it
         ALTER TABLE contract ALTER COLUMN end_date DROP NOT NULL;
         INSERT INTO contract (start_date, end_date)
             VALUES ('2026-01-01', NULL);           -- OK: CHECK returns UNKNOWN
         SELECT * FROM contract;

         DROP TABLE contract;

         -- Step 15b: IN-list vocabulary check
         CREATE TABLE person (
             person_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY
         );
         CREATE TABLE student (
             person_id         INTEGER PRIMARY KEY
                 REFERENCES person (person_id) ON DELETE CASCADE,
             academic_standing VARCHAR(30) NOT NULL,
             CONSTRAINT chk_standing
                 CHECK (academic_standing IN (
                     'Good Standing', 'Probation',
                     'Suspended',     'Dismissed'))
         );

         INSERT INTO person DEFAULT VALUES;  -- person_id = 1
         INSERT INTO person DEFAULT VALUES;  -- person_id = 2

         INSERT INTO student VALUES (1, 'Good Standing');  -- OK
         INSERT INTO student VALUES (2, 'Expelled');
         -- ERROR: new row violates check constraint "chk_standing"

         INSERT INTO student VALUES (2, NULL);
         -- ERROR: null value in column "academic_standing" violates not-null constraint


.. dropdown:: Category Pattern
   :class-container: sd-border-secondary

   .. rubric:: Implementing Categories (Union Types) in SQL

   A category (union type) represents an entity that can be associated with
   one of several disjoint supertype tables. The exclusive-arc pattern uses
   one nullable FK per supertype and a ``CHECK`` constraint that asserts
   exactly one of them is non-null at any given time.

   .. admonition:: Demo 16 -- Categories: Exclusive-Arc CHECK Pattern
      :class: note

      Insert the three valid rows (one per supertype) and confirm all succeed.
      Attempt the two-FK row and observe the error; confirm the arc sum
      evaluates to ``1 + 1 + 0 = 2``. Attempt the all-null row and observe
      the error; confirm the arc sum evaluates to ``0 + 0 + 0 = 0``. Then
      run the arc-sum ``SELECT`` on the valid rows to see the sum equal to 1
      for each.

      .. code-block:: sql

         CREATE TABLE veh_person (
             ssn       VARCHAR(11) PRIMARY KEY,
             full_name VARCHAR(100) NOT NULL
         );
         CREATE TABLE company (
             tax_id       VARCHAR(10) PRIMARY KEY,
             company_name VARCHAR(100) NOT NULL
         );
         CREATE TABLE bank (
             routing_no VARCHAR(9) PRIMARY KEY,
             bank_name  VARCHAR(100) NOT NULL
         );

         CREATE TABLE vehicle_owner (
             owner_id        INTEGER
                 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             owner_type      VARCHAR(10) NOT NULL,
             person_ssn      VARCHAR(11),
             company_tax_id  VARCHAR(10),
             bank_routing_no VARCHAR(9),
             ownership_date  DATE NOT NULL,
             CONSTRAINT fk_owner_person
                 FOREIGN KEY (person_ssn)
                     REFERENCES veh_person (ssn) ON DELETE CASCADE,
             CONSTRAINT fk_owner_company
                 FOREIGN KEY (company_tax_id)
                     REFERENCES company (tax_id) ON DELETE CASCADE,
             CONSTRAINT fk_owner_bank
                 FOREIGN KEY (bank_routing_no)
                     REFERENCES bank (routing_no) ON DELETE CASCADE,
             CONSTRAINT chk_exclusive_arc
                 CHECK (
                     (person_ssn      IS NOT NULL)::INT +
                     (company_tax_id  IS NOT NULL)::INT +
                     (bank_routing_no IS NOT NULL)::INT = 1)
         );

         INSERT INTO veh_person VALUES ('123-45-6789', 'Alice Johnson');
         INSERT INTO company    VALUES ('TX-9876543',  'Acme Corp');
         INSERT INTO bank       VALUES ('021000021',   'First National Bank');

         -- Valid rows: exactly one FK non-null per row
         INSERT INTO vehicle_owner (owner_type, person_ssn, ownership_date)
             VALUES ('person',  '123-45-6789', CURRENT_DATE);  -- OK: arc sum = 1
         INSERT INTO vehicle_owner (owner_type, company_tax_id, ownership_date)
             VALUES ('company', 'TX-9876543',  CURRENT_DATE);  -- OK: arc sum = 1
         INSERT INTO vehicle_owner (owner_type, bank_routing_no, ownership_date)
             VALUES ('bank',    '021000021',   CURRENT_DATE);  -- OK: arc sum = 1

         -- Verify arc sum is 1 for all valid rows
         SELECT owner_id,
                owner_type,
                (person_ssn      IS NOT NULL)::INT +
                (company_tax_id  IS NOT NULL)::INT +
                (bank_routing_no IS NOT NULL)::INT AS arc_sum
         FROM vehicle_owner;

         -- Two FKs non-null: arc sum = 2; rejected
         INSERT INTO vehicle_owner (owner_type, person_ssn, company_tax_id, ownership_date)
             VALUES ('person', '123-45-6789', 'TX-9876543', CURRENT_DATE);
         -- ERROR: violates check constraint "chk_exclusive_arc"

         -- All FKs null: arc sum = 0; rejected
         INSERT INTO vehicle_owner (owner_type, ownership_date)
             VALUES ('unknown', CURRENT_DATE);
         -- ERROR: violates check constraint "chk_exclusive_arc"

         DROP TABLE vehicle_owner;
         DROP TABLE bank;
         DROP TABLE company;
         DROP TABLE veh_person;


.. dropdown:: EXCLUDE Constraints
   :class-container: sd-border-secondary

   .. rubric:: Preventing Overlapping Ranges

   ``EXCLUDE`` is a PostgreSQL-specific constraint that generalizes ``UNIQUE``
   from equality to any binary operator. Where ``UNIQUE`` rejects two rows
   whose values are *equal*, ``EXCLUDE`` rejects two rows whose values satisfy
   a given operator pair simultaneously.

   Why ``UNIQUE`` is not enough:

   .. code-block:: sql

      -- UNIQUE only rejects identical ranges; overlapping ranges pass silently
      CONSTRAINT uq_room_range UNIQUE (room, seat_range)
      INSERT INTO exam_schedule VALUES ('EGR 1202', '[1,50)');   -- OK
      INSERT INTO exam_schedule VALUES ('EGR 1202', '[40,80)');  -- OK -- but overlaps!

   .. admonition:: Demo 17 -- EXCLUDE Constraint with GIST and Range Overlap
      :class: note

      Run all four inserts and confirm the second fails with an exclusion
      constraint violation. Insert ``'[50,80)'`` for ``EGR 1202`` and confirm
      it succeeds: ``[1,50)`` excludes seat 50 so there is no overlap. Insert
      ``'[1,50)'`` for ``EGR 1104`` and confirm it succeeds: the room
      condition fails so the constraint does not fire. Run the final two
      ``SELECT`` statements to confirm that ``&&`` returns ``TRUE`` (the
      ranges overlap) while ``=`` returns ``FALSE`` (the ranges are not equal
      -- which is why ``UNIQUE`` cannot catch the overlap).

      .. code-block:: sql

         -- btree_gist is required to use = with GIST on non-range types
         CREATE EXTENSION IF NOT EXISTS btree_gist;

         CREATE TABLE exam_schedule (
             exam_id    INTEGER
                 GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             room       VARCHAR(20) NOT NULL,
             seat_range INT4RANGE   NOT NULL,
             CONSTRAINT no_seat_overlap
                 EXCLUDE USING GIST (
                     room       WITH =,
                     seat_range WITH &&
                 )
         );

         INSERT INTO exam_schedule (room, seat_range)
             VALUES ('EGR 1202', '[1,50)');   -- OK: first row, no conflict
         INSERT INTO exam_schedule (room, seat_range)
             VALUES ('EGR 1202', '[40,80)');  -- FAIL: overlaps [1,50) at seats 40-49
         -- ERROR: conflicting key value violates exclusion constraint "no_seat_overlap"

         INSERT INTO exam_schedule (room, seat_range)
             VALUES ('EGR 1202', '[51,100)'); -- OK: no shared seat with [1,50)
         INSERT INTO exam_schedule (room, seat_range)
             VALUES ('EGR 1104', '[1,50)');   -- OK: different room

         SELECT * FROM exam_schedule;

         -- [50,80) is adjacent to [1,50) but does not overlap; succeeds
         INSERT INTO exam_schedule (room, seat_range)
             VALUES ('EGR 1202', '[50,80)');  -- OK: [1,50) excludes seat 50

         SELECT * FROM exam_schedule ORDER BY room, seat_range;

         -- Demonstrate that UNIQUE would not catch the overlap:
         SELECT '[1,50)'::INT4RANGE && '[40,80)'::INT4RANGE AS overlaps; -- TRUE
         SELECT '[1,50)'::INT4RANGE =  '[40,80)'::INT4RANGE AS equal;    -- FALSE

         DROP TABLE exam_schedule;



Building the University Schema
====================================================


.. dropdown:: Creation Order: Parents Before Children
   :class-container: sd-border-secondary
   

   .. rubric:: Every FK Must Reference a Table That Already Exists

   The university schema has a fixed creation order determined by FK
   dependencies:

   .. list-table::
      :widths: 15 85
      :header-rows: 1
      :class: compact-table

      * - **Wave**
        - **Tables**
      * - 1 (no deps)
        - ``person``, ``academic_rank``
      * - 2
        - ``department``, ``student``, ``course``
      * - 3
        - ``professor``, ``course_section``, ``grad_student``, ``person_email``, ``person_phone``, ``prof_specialization``
      * - 4 (junction)
        - ``enrollment``, ``ta_assignment``, ``course_prereq``, ``student_degree``

   The circular reference between ``department`` (``chair_id`` references
   ``professor``) and ``professor`` (``dept_id`` references ``department``)
   requires ``DEFERRABLE INITIALLY DEFERRED`` on ``fk_dept_chair``. Create
   ``department`` first with ``chair_id`` nullable, then create ``professor``,
   then wire the chair FK via ``ALTER TABLE``.

   .. card::
       :class-card: sd-border-info

       **Rule**: If you cannot draw a linear dependency graph from the tables,
       you need at least one deferrable constraint to resolve the cycle.


.. dropdown:: Building and Verifying the Full Schema
   :class-container: sd-border-secondary

   .. admonition:: Demo 18 -- Verifying the Schema with Catalog Views
      :class: note

      Run ``\d+ student`` in psql and locate the *Referenced by* section;
      note every table that holds a FK pointing at ``student``. Run the
      four catalog queries shown and compare their output against the psql
      meta-command results. Cross-reference ``table_constraints`` with
      ``referential_constraints`` to confirm the ``ON DELETE`` action for
      each FK. Run the ``pg_sequences`` query and verify that exactly one
      sequence exists per identity column in the schema.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         CREATE TABLE student (
             person_id         INTEGER PRIMARY KEY,
             student_id        VARCHAR(20) NOT NULL UNIQUE,
             admission_date    DATE        NOT NULL,
             gpa               NUMERIC(3,2),
             academic_standing VARCHAR(30) NOT NULL,
             CONSTRAINT chk_gpa
                 CHECK (gpa >= 0.0 AND gpa <= 4.0),
             CONSTRAINT chk_standing
                 CHECK (academic_standing IN (
                     'Good Standing', 'Probation',
                     'Suspended', 'Dismissed')),
             CONSTRAINT fk_student_person
                 FOREIGN KEY (person_id)
                     REFERENCES person (person_id)
                     ON DELETE CASCADE
         );
         CREATE TABLE grad_student (
             person_id    INTEGER PRIMARY KEY,
             thesis_topic VARCHAR(200),
             CONSTRAINT fk_grad_student
                 FOREIGN KEY (person_id)
                     REFERENCES student (person_id)
                     ON DELETE CASCADE
         );

         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');
         INSERT INTO person (first_name, last_name) VALUES ('Carol', 'Davis');
         INSERT INTO student VALUES (1, '117453210', '2024-08-26', 3.75, 'Good Standing');
         INSERT INTO student VALUES (2, '117453211', '2024-08-26', 2.10, 'Probation');
         INSERT INTO student VALUES (3, '117453212', '2023-08-28', 3.90, 'Good Standing');
         INSERT INTO grad_student VALUES (3, 'Autonomous Vehicle Perception');

         -- List all constraints on the student table with their types
         SELECT constraint_name, constraint_type
         FROM information_schema.table_constraints
         WHERE table_name   = 'student'
           AND table_schema = 'public'
         ORDER BY constraint_type, constraint_name;

         -- List all FK delete and update actions for the entire schema
         SELECT tc.table_name,
                tc.constraint_name,
                rc.delete_rule,
                rc.update_rule
         FROM information_schema.table_constraints tc
         JOIN information_schema.referential_constraints rc
             ON tc.constraint_name = rc.constraint_name
         WHERE tc.table_schema = 'public'
         ORDER BY tc.table_name, tc.constraint_name;

         -- Check current sequence values for all sequences in public schema
         SELECT sequencename, last_value, increment_by, start_value
         FROM pg_sequences
         WHERE schemaname = 'public'
         ORDER BY sequencename;

         -- List every table with a FK pointing at student
         SELECT tc.table_name AS child_table,
                tc.constraint_name,
                rc.delete_rule
         FROM information_schema.table_constraints      tc
         JOIN information_schema.referential_constraints rc
             ON tc.constraint_name = rc.constraint_name
         WHERE tc.constraint_type = 'FOREIGN KEY'
           AND tc.table_schema    = 'public'
           AND rc.unique_constraint_name IN (
               SELECT constraint_name
               FROM information_schema.table_constraints
               WHERE table_name = 'student' AND table_schema = 'public'
           )
         ORDER BY child_table;

         DROP TABLE grad_student;
         DROP TABLE student;
         DROP TABLE person;


.. dropdown:: Verifying the Schema: psql Meta-Commands
   :class-container: sd-border-secondary

   .. rubric:: psql: The Command-Line Client

   **psql** is the PostgreSQL interactive client that unlocks meta-commands
   prefixed with ``\``. Meta-commands are processed by the client and never
   sent to the server; they do not end with a semicolon.

   Connecting:

   .. code-block:: bash

      psql -d university_db
      psql -U postgres -d university_db
      psql -h localhost -p 5432 -U postgres -d university_db

   .. list-table::
      :widths: 28 50
      :header-rows: 1
      :class: compact-table

      * - **Meta-command**
        - **What it shows**
      * - ``\d tablename``
        - Columns, types, constraints
      * - ``\d+ tablename``
        - Same plus FK *Referenced by* section and storage parameters
      * - ``\dt``
        - All tables in the current schema
      * - ``\di``
        - All indexes
      * - ``\dn``
        - All schemas in the database
      * - ``\l``
        - All databases on the server

   .. tip::

      Always run ``\d+ tablename`` before any ``DROP`` or
      ``TRUNCATE CASCADE`` to inspect what references the table.



ALTER TABLE and Schema Evolution
====================================================


.. dropdown:: Common ALTER TABLE Operations
   :class-container: sd-border-secondary
   

   .. rubric:: Evolving a Live Schema Safely

   Not all ``ALTER TABLE`` operations are equal. Some complete in milliseconds
   on any table size; others hold an exclusive lock and rewrite every row.

   .. list-table::
      :widths: 45 25 30
      :header-rows: 1
      :class: compact-table

      * - **Operation**
        - **Table rewrite?**
        - **Cost**
      * - ``ADD COLUMN`` nullable
        - No
        - Instant
      * - ``ADD COLUMN NOT NULL`` + constant default (PG 11+)
        - No
        - Instant
      * - ``ADD COLUMN NOT NULL`` no default
        - Yes
        - Expensive
      * - ``ALTER COLUMN TYPE`` compatible
        - No
        - Instant
      * - ``ALTER COLUMN TYPE`` incompatible
        - Yes
        - Expensive
      * - ``RENAME COLUMN``
        - No
        - Instant
      * - ``DROP COLUMN``
        - No
        - Instant
      * - ``ADD CONSTRAINT CHECK``
        - No
        - Validates all rows
      * - ``DROP CONSTRAINT``
        - No
        - Instant

   .. admonition:: Demo 19 -- Common ALTER TABLE Operations
      :class: note

      Add a nullable ``description TEXT`` column to your live ``course``
      table and confirm it is instant. Then try
      ``ADD COLUMN is_archived BOOLEAN NOT NULL`` with no default and observe
      the error. Add it again with ``DEFAULT FALSE`` and confirm it succeeds
      instantly.

      .. code-block:: sql

         CREATE TABLE person (
             person_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name  VARCHAR(50) NOT NULL,
             middle_name VARCHAR(50),
             last_name   VARCHAR(50) NOT NULL,
             state       CHAR(2)
         );
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );
         CREATE TABLE course (
             course_id VARCHAR(10)  PRIMARY KEY,
             dept_id   INTEGER      NOT NULL REFERENCES department (dept_id),
             title     VARCHAR(150) NOT NULL,
             credits   INTEGER      NOT NULL
         );
         CREATE TABLE course_section (
             course_id  VARCHAR(10) NOT NULL REFERENCES course (course_id),
             section_no VARCHAR(10) NOT NULL,
             schedule   VARCHAR(100),
             CONSTRAINT pk_course_section PRIMARY KEY (course_id, section_no)
         );
         CREATE TABLE professor (
             person_id INTEGER PRIMARY KEY REFERENCES person (person_id),
             dept_id   INTEGER NOT NULL REFERENCES department (dept_id),
             hire_date DATE    NOT NULL,
             salary    NUMERIC(12,2)
         );

         INSERT INTO department (dept_name) VALUES ('Computer Science');
         INSERT INTO person (first_name, middle_name, last_name, state)
             VALUES ('Alice', 'M', 'Johnson', 'MD');
         INSERT INTO course VALUES ('ENPM818T', 1, 'Data Storage and Databases', 3);
         INSERT INTO course_section VALUES ('ENPM818T', '0101', 'MWF 10:00');
         INSERT INTO professor VALUES (1, 1, '2020-08-01', 95000.00);

         -- Add a nullable column: instant, no table rewrite
         ALTER TABLE course ADD COLUMN description TEXT;
         SELECT course_id, description FROM course;

         -- ADD COLUMN NOT NULL with no default: fails
         ALTER TABLE course ADD COLUMN is_archived BOOLEAN NOT NULL;
         -- ERROR: column "is_archived" of relation "course" contains null values

         -- ADD COLUMN NOT NULL with DEFAULT: instant in PG 11+
         ALTER TABLE course ADD COLUMN is_archived BOOLEAN NOT NULL DEFAULT FALSE;
         SELECT course_id, is_archived FROM course;

         -- Set a default on an existing column
         ALTER TABLE course ALTER COLUMN credits SET DEFAULT 3;

         -- Change a column type (compatible)
         ALTER TABLE person ALTER COLUMN state TYPE CHAR(3);

         -- Add a named CHECK constraint
         ALTER TABLE professor
             ADD CONSTRAINT chk_hire_date
                 CHECK (hire_date >= '1900-01-01');

         -- Confirm constraint exists
         SELECT constraint_name, constraint_type
         FROM information_schema.table_constraints
         WHERE table_name = 'professor' AND table_schema = 'public';

         -- Drop a named constraint
         ALTER TABLE professor DROP CONSTRAINT chk_hire_date;

         -- Rename a column: instant, no table rewrite
         ALTER TABLE course_section RENAME COLUMN schedule TO meeting_pattern;

         -- Confirm the rename
         SELECT column_name FROM information_schema.columns
         WHERE table_name = 'course_section' AND table_schema = 'public';

         -- Drop a column
         ALTER TABLE person DROP COLUMN middle_name;

         DROP TABLE professor;
         DROP TABLE course_section;
         DROP TABLE course;
         DROP TABLE department;
         DROP TABLE person;


.. dropdown:: Safe Migration Pattern for Large Tables
   :class-container: sd-border-secondary

   .. rubric:: Adding a NOT NULL Column Without Downtime

   Adding a ``NOT NULL`` column directly to a large table acquires an
   ``ACCESS EXCLUSIVE`` lock and rewrites every row. The four-step pattern
   avoids this:

   - Step 1 acquires only a brief metadata lock; no rows are touched.
   - Step 2 can be run in batches with ``LIMIT`` to avoid long-running transactions.
   - ``NOT VALID`` adds the constraint without scanning existing rows; new inserts and updates are checked immediately.
   - ``VALIDATE CONSTRAINT`` acquires ``SHARE UPDATE EXCLUSIVE``, so concurrent reads are not blocked.

   .. admonition:: Demo 20 -- Safe Migration Pattern for Large Tables
      :class: note

      Run the four steps in order and confirm each succeeds. After Step 3,
      insert a new row with ``office_number = NULL`` and observe that it is
      rejected immediately even though existing rows have not been validated
      yet. After Step 4, confirm the constraint is now marked valid by running
      ``SELECT conname, convalidated FROM pg_constraint WHERE conrelid = 'professor'::regclass``.
      Then attempt the single-step ``ADD COLUMN office_number VARCHAR(10) NOT NULL``
      without a default and confirm it fails, demonstrating why the four-step
      pattern is needed.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );
         CREATE TABLE professor (
             person_id INTEGER PRIMARY KEY REFERENCES person (person_id),
             dept_id   INTEGER NOT NULL REFERENCES department (dept_id),
             hire_date DATE    NOT NULL
         );

         INSERT INTO department (dept_name) VALUES ('Computer Science');
         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');
         INSERT INTO professor VALUES (1, 1, '2020-08-01');
         INSERT INTO professor VALUES (2, 1, '2018-01-15');

         -- Demonstrate why the naive approach fails
         ALTER TABLE professor ADD COLUMN office_number VARCHAR(10) NOT NULL;
         -- ERROR: column "office_number" of relation "professor" contains null values

         -- Step 1: add nullable; instant on any table size
         ALTER TABLE professor ADD COLUMN office_number VARCHAR(10);
         SELECT person_id, office_number FROM professor;

         -- Step 2: backfill existing rows
         UPDATE professor
             SET office_number = 'TBD'
             WHERE office_number IS NULL;
         SELECT person_id, office_number FROM professor;

         -- Step 3: add constraint as NOT VALID
         -- Skips scanning existing rows; new writes are checked immediately
         ALTER TABLE professor
             ADD CONSTRAINT nn_office_number
                 CHECK (office_number IS NOT NULL)
                 NOT VALID;

         SELECT conname, convalidated
         FROM pg_constraint
         WHERE conrelid = 'professor'::regclass;

         -- New inserts are checked immediately even before validation
         INSERT INTO professor (person_id, dept_id, hire_date, office_number)
             VALUES (1, 1, CURRENT_DATE, NULL);
         -- ERROR: new row violates check constraint "nn_office_number"

         -- Step 4: validate with a weaker lock
         -- Reads continue during this scan
         ALTER TABLE professor VALIDATE CONSTRAINT nn_office_number;

         -- Confirm constraint is now marked valid
         SELECT conname, convalidated
         FROM pg_constraint
         WHERE conrelid = 'professor'::regclass;

         DROP TABLE professor;
         DROP TABLE department;
         DROP TABLE person;



DELETE, TRUNCATE, and DROP
====================================================


.. dropdown:: Choosing the Right Removal Command
   :class-container: sd-border-secondary
   

   .. rubric:: Three Commands, Three Different Scopes

   .. list-table::
      :widths: 28 18 18 18
      :header-rows: 1
      :class: compact-table

      * - **Operation**
        - **Rows**
        - **Structure**
        - **Seq reset**
      * - ``DELETE`` filtered
        - Some gone
        - Kept
        - No
      * - ``TRUNCATE``
        - All gone
        - Kept
        - No
      * - ``TRUNCATE RESTART``
        - All gone
        - Kept
        - Yes
      * - ``DROP``
        - All gone
        - Removed
        - N/A

   .. list-table::
      :widths: 28 24 24 24
      :header-rows: 1
      :class: compact-table

      * - **Property**
        - ``DELETE``
        - ``TRUNCATE``
        - ``DROP``
      * - Triggers fired
        - Yes
        - No
        - No
      * - Rollbackable
        - Yes
        - Yes
        - Yes
      * - Speed (large table)
        - Slow
        - Fast
        - Fast
      * - ``WHERE`` clause
        - Yes
        - No
        - No

   .. admonition:: Think Prompt
      :class: hint

      You need to reload ``enrollment`` from a CSV file at the start of each
      semester. Which command do you use and why? What is the risk of
      ``TRUNCATE CASCADE`` in this context?

   .. dropdown:: Answer
      :class-container: sd-border-success

      ``TRUNCATE TABLE enrollment RESTART IDENTITY`` is the right choice.
      It removes all rows instantly, resets the identity sequence so IDs
      start cleanly, and leaves the table structure and constraints intact
      for the reload. ``DELETE`` would work but is far slower on a large
      table because it fires row-level triggers and generates write-ahead
      log entries for each row individually. ``DROP`` is wrong because it
      destroys the table definition. As for ``TRUNCATE CASCADE``: if any
      other table holds a FK referencing ``enrollment``, ``CASCADE`` will
      silently truncate those tables too. Always run ``\d+ enrollment``
      first to check what references it before using ``CASCADE``.

   .. admonition:: Demo 21 -- DELETE, TRUNCATE, and DROP
      :class: note

      Insert five rows into ``enrollment``. Delete two with ``WHERE`` and
      confirm three remain. Run ``TRUNCATE`` and confirm zero rows but the
      table still exists. Run ``TRUNCATE RESTART IDENTITY``, then
      ``DROP TABLE enrollment`` and confirm it is gone. Finally run
      ``DROP TABLE IF EXISTS enrollment`` and confirm it produces no error
      even though the table no longer exists.

      .. code-block:: sql

         CREATE TABLE person (
             person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             first_name VARCHAR(50) NOT NULL,
             last_name  VARCHAR(50) NOT NULL
         );
         CREATE TABLE student (
             person_id  INTEGER PRIMARY KEY
                 REFERENCES person (person_id) ON DELETE CASCADE,
             student_id VARCHAR(20) NOT NULL UNIQUE
         );
         CREATE TABLE department (
             dept_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
             dept_name VARCHAR(100) NOT NULL
         );
         CREATE TABLE course (
             course_id VARCHAR(10) PRIMARY KEY,
             dept_id   INTEGER     NOT NULL REFERENCES department (dept_id),
             title     VARCHAR(150) NOT NULL
         );
         CREATE TABLE course_section (
             course_id  VARCHAR(10) NOT NULL REFERENCES course (course_id),
             section_no VARCHAR(10) NOT NULL,
             CONSTRAINT pk_course_section PRIMARY KEY (course_id, section_no)
         );
         CREATE TABLE enrollment (
             student_person_id INTEGER     NOT NULL
                 REFERENCES student (person_id) ON DELETE CASCADE,
             course_id         VARCHAR(10) NOT NULL,
             section_no        VARCHAR(10) NOT NULL,
             grade             VARCHAR(3),
             CONSTRAINT pk_enrollment
                 PRIMARY KEY (student_person_id, course_id, section_no),
             CONSTRAINT fk_enroll_section
                 FOREIGN KEY (course_id, section_no)
                     REFERENCES course_section (course_id, section_no)
                     ON DELETE CASCADE
         );

         INSERT INTO department (dept_name) VALUES ('Computer Science');
         INSERT INTO course VALUES ('ENPM818T', 1, 'Databases');
         INSERT INTO course VALUES ('ENPM605',  1, 'Python for Robotics');
         INSERT INTO course VALUES ('ENPM702',  1, 'Robot Programming');
         INSERT INTO course_section VALUES ('ENPM818T', '0101');
         INSERT INTO course_section VALUES ('ENPM605',  '0101');
         INSERT INTO course_section VALUES ('ENPM702',  '0101');

         INSERT INTO person (first_name, last_name) VALUES ('Alice', 'Johnson');
         INSERT INTO person (first_name, last_name) VALUES ('Bob',   'Smith');
         INSERT INTO person (first_name, last_name) VALUES ('Carol', 'Davis');
         INSERT INTO person (first_name, last_name) VALUES ('David', 'Lee');
         INSERT INTO person (first_name, last_name) VALUES ('Eve',   'Brown');
         INSERT INTO student VALUES (1, '117453210');
         INSERT INTO student VALUES (2, '117453211');
         INSERT INTO student VALUES (3, '117453212');
         INSERT INTO student VALUES (4, '117453213');
         INSERT INTO student VALUES (5, '117453214');

         INSERT INTO enrollment VALUES (1, 'ENPM818T', '0101', 'A');
         INSERT INTO enrollment VALUES (2, 'ENPM818T', '0101', 'B+');
         INSERT INTO enrollment VALUES (3, 'ENPM605',  '0101', 'A-');
         INSERT INTO enrollment VALUES (4, 'ENPM702',  '0101', 'B');
         INSERT INTO enrollment VALUES (5, 'ENPM818T', '0101', 'A');

         -- Confirm five rows
         SELECT * FROM enrollment;

         -- DELETE: remove specific rows
         DELETE FROM enrollment
             WHERE student_person_id IN (1, 2);
         SELECT * FROM enrollment;  -- three rows remain

         -- TRUNCATE: remove all rows, keep structure
         TRUNCATE TABLE enrollment;
         SELECT * FROM enrollment;
         SELECT COUNT(*) FROM enrollment;

         -- TRUNCATE RESTART IDENTITY: reset the sequence too
         INSERT INTO enrollment VALUES (3, 'ENPM605', '0101', 'A-');
         TRUNCATE TABLE enrollment RESTART IDENTITY;

         -- DROP: remove table entirely
         DROP TABLE enrollment;
         SELECT * FROM enrollment;
         -- ERROR: relation "enrollment" does not exist

         -- Safe drop: no error if already absent
         DROP TABLE IF EXISTS enrollment;

         -- Clean up remaining tables
         DROP TABLE course_section;
         DROP TABLE course;
         DROP TABLE student;
         DROP TABLE department;
         DROP TABLE person;



Best Practices and Mistakes to Avoid
====================================================


.. dropdown:: The Six Most Common DDL Mistakes
   :class-container: sd-border-secondary
   

   .. rubric:: Mistakes That Cost the Most to Fix Later

   DDL mistakes are uniquely costly: unlike application bugs, a wrong
   constraint or type choice requires migrating existing data to fix.

   **M1: Forgetting NOT NULL on mandatory columns**

   .. code-block:: sql

      title VARCHAR(150)          -- nullable by default (wrong)
      title VARCHAR(150) NOT NULL -- correct

   **M2: FLOAT for money or GPA**

   .. code-block:: sql

      gpa FLOAT        -- binary rounding errors
      gpa NUMERIC(3,2) -- exact decimal

   **M3: CHECK without NOT NULL**

   .. code-block:: sql

      gpa NUMERIC(3,2) CHECK (gpa >= 0.0)           -- NULL passes silently
      gpa NUMERIC(3,2) NOT NULL CHECK (gpa >= 0.0)  -- correct

   **M4: Anonymous constraints**

   .. code-block:: sql

      email VARCHAR(100) UNIQUE                    -- error says "person_email_key"
      CONSTRAINT uq_person_email UNIQUE (email)    -- error says "uq_person_email"

   **M5: VARCHAR(255) out of habit**

   .. code-block:: sql

      name  VARCHAR(255) -- arbitrary; use TEXT
      state CHAR(2)      -- genuine business rule

   **M6: Dropping without checking dependencies**

   .. code-block:: sql

      DROP TABLE student;          -- fails: enrollment references student
      DROP TABLE student CASCADE;  -- works but silently destroys enrollment

   Always run ``\d+ student`` before any ``DROP`` to inspect what references it.


.. dropdown:: Naming Conventions
   :class-container: sd-border-secondary

   .. rubric:: Consistent Naming Pays Off at Debug Time

   .. list-table::
      :widths: 25 30 30
      :header-rows: 1
      :class: compact-table

      * - **Element**
        - **Convention**
        - **Example**
      * - Tables
        - Singular ``snake_case``
        - ``course_prereq``
      * - Columns
        - ``snake_case``
        - ``first_name``
      * - Primary keys
        - ``table_id``
        - ``dept_id``
      * - Foreign keys
        - Same name as referenced PK
        - ``dept_id`` in ``professor``
      * - PK constraints
        - ``pk_table``
        - ``pk_enrollment``
      * - FK constraints
        - ``fk_child_parent``
        - ``fk_prof_dept``
      * - UQ constraints
        - ``uq_table_col``
        - ``uq_person_email``
      * - CHK constraints
        - ``chk_table_col``
        - ``chk_gpa``

   Consistent naming pays off when reading error messages, running audits
   against ``information_schema``, and onboarding new team members.
   The prefix tells you the constraint type before you open the schema.



Wrap-Up and Next Steps
====================================================


Key Takeaways
--------------

1. **The logical schema says what exists; SQL says how to enforce it.** Every
   data type, constraint, and creation order decision is a deliberate act of
   physical modeling.

2. **Use GENERATED ALWAYS AS IDENTITY, not SERIAL.** ``SERIAL`` silently
   allows manual value insertion; ``GENERATED ALWAYS`` rejects it immediately.

3. **Pair CHECK with NOT NULL.** A ``CHECK`` constraint alone does not block
   ``NULL``; three-valued logic lets ``NULL`` pass silently.

4. **ISA hierarchies use the shared-PK strategy.** The subtype PK receives
   its value from the supertype insert; no second sequence is created.

5. **Deferrable FKs resolve circular dependencies.** Move the FK check from
   statement end to transaction commit with ``DEFERRABLE INITIALLY DEFERRED``.

6. **ALTER TABLE safely with the four-step pattern.** Adding ``NOT NULL``
   to a large table without downtime requires: add nullable, backfill,
   add ``NOT VALID`` constraint, then ``VALIDATE CONSTRAINT``.

7. **Know what DROP and TRUNCATE CASCADE do.** Both cascade silently to
   dependent tables. Always inspect ``\d+ tablename`` before running either.


Quick Reference
---------------

.. seealso::

   :doc:`../../glossary/glossary` -- a condensed, alphabetical reference covering all key
   DDL terms from this lecture: data types, constraint types, identity
   columns, deferrable constraints, ISA patterns, ALTER TABLE operations,
   and the DELETE / TRUNCATE / DROP comparison.
