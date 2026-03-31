====================================================
Exercises
====================================================

This page contains exercises for Lecture 6. These exercises are designed to
reinforce your understanding of PostgreSQL data types, integrity constraints,
ISA hierarchies, deferrable foreign keys, schema evolution with ``ALTER TABLE``,
and the DELETE / TRUNCATE / DROP distinction.

All exercises use the ``university_db`` schema you built during the lecture
demos. Open ``lecture6_schema.sql`` in DataGrip before starting.


.. dropdown:: Exercise 1 -- Type Auditor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build intuition for data type selection by auditing a poorly typed
    schema, identifying every mistake, and rewriting the ``CREATE TABLE``
    statement with correct types and constraints.


    **Specification**

    A new team member wrote the following table for a university grant
    tracking system:

    .. code-block:: sql

       CREATE TABLE grant_proposal (
           proposal_id  SERIAL,
           title        VARCHAR(255),
           pi_email     TEXT,
           amount       FLOAT,
           gpa_req      FLOAT,
           start_date   VARCHAR(20),
           end_date     VARCHAR(20),
           is_funded    VARCHAR(5),
           department   TEXT
       );

    Additional business rules:

    - Each proposal has a unique, system-generated ID.
    - Title, PI email, amount, start date, and end date are mandatory.
    - The PI email must be unique across all proposals.
    - Funding amounts are always exact to two decimal places and must be
      positive.
    - The minimum GPA requirement, if specified, must be between 0.00 and
      4.00.
    - ``is_funded`` is a true/false flag; it is mandatory and defaults to
      ``FALSE``.
    - A proposal's end date must be after its start date (this is a
      table-level constraint).
    - The department column references a ``dept_id`` in the ``department``
      table.

    **Tasks**

    1. List every type or constraint mistake in the original table.
       For each mistake, state what is wrong and what the correct choice is.

    2. Rewrite ``grant_proposal`` as a correct ``CREATE TABLE`` statement
       that enforces all business rules listed above. Follow the naming
       conventions from the lecture (``pk_``, ``fk_``, ``uq_``, ``chk_``
       prefixes).

    3. The team member wants to add a ``submitted_at`` column that records
       the exact date and time (including time zone) when the proposal was
       submitted. Write the ``ALTER TABLE`` statement to add it safely as a
       nullable column, then write a second ``ALTER TABLE`` to set its
       default to ``CURRENT_TIMESTAMP``.

    .. tip::

       There are at least seven distinct mistakes in the original table.
       Check every column for type, nullability, and naming issues before
       moving on to the rewrite.


    **Deliverables**

    - Numbered list of mistakes with explanations (at least seven)
    - Corrected ``CREATE TABLE`` statement with all constraints named
    - Two ``ALTER TABLE`` statements for the ``submitted_at`` column


.. dropdown:: Exercise 2 -- Constraint Detective
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Predict the outcome of a sequence of SQL statements, explain the
    constraint mechanics behind each result, and then fix a broken schema
    to make all statements succeed.


    **Specification**

    Run the following sequence in your live ``university_db``. Predict
    whether each statement will succeed or fail **before** running it,
    and identify which constraint fires in each failure.

    .. code-block:: sql

       -- Setup
       CREATE TABLE person (
           person_id     INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
           first_name    VARCHAR(100) NOT NULL,
           last_name     VARCHAR(100) NOT NULL,
           email         VARCHAR(200) UNIQUE,
           date_of_birth DATE         NOT NULL
       );

       CREATE TABLE student (
           person_id  INTEGER PRIMARY KEY,
           student_id VARCHAR(20) NOT NULL UNIQUE,
           gpa        NUMERIC(3,2) NOT NULL
               CONSTRAINT chk_gpa CHECK (gpa BETWEEN 0.00 AND 4.00),
           CONSTRAINT fk_student_person
               FOREIGN KEY (person_id)
                   REFERENCES person (person_id)
                   ON DELETE CASCADE
       );

       -- Statements to predict
       -- A
       INSERT INTO person (first_name, last_name, date_of_birth)
           VALUES ('Alice', 'Johnson', '1998-04-12');

       -- B
       INSERT INTO student (person_id, student_id, gpa)
           VALUES (99, '117453210', 3.5);

       -- C
       INSERT INTO student (person_id, student_id, gpa)
           VALUES (1, '117453210', 4.5);

       -- D
       INSERT INTO person (first_name, last_name, email, date_of_birth)
           VALUES ('Bob', 'Smith', NULL, '1999-06-01');

       -- E
       INSERT INTO person (first_name, last_name, email, date_of_birth)
           VALUES ('Carol', 'Davis', NULL, '2000-03-22');

       -- F
       INSERT INTO student (person_id, student_id, gpa)
           VALUES (1, '117453211', NULL);

       -- G
       DELETE FROM person WHERE person_id = 1;
       SELECT * FROM student WHERE person_id = 1;

    **Tasks**

    1. For each statement A through G, predict: **SUCCEED** or **FAIL**.
       For each FAIL, name the constraint that fires.

    2. Statement E inserts a ``NULL`` email and succeeds even though
       ``email`` is declared ``UNIQUE``. Explain why.

    3. After running G (which should succeed), what does the ``SELECT``
       return and why?

    4. Suppose the business rule changes: now at most **one** person may
       have a ``NULL`` email (representing an anonymous placeholder
       account). Write the single DDL change needed to enforce this rule
       without recreating the table.

    .. note::

       Run the statements exactly as written, in order. Some later
       statements depend on the state left by earlier ones.


    **Deliverables**

    - Prediction table (statement, SUCCEED/FAIL, constraint name for failures)
    - Explanation of statement E behavior
    - Explanation of the SELECT result after G
    - DDL statement for the modified email uniqueness rule


.. dropdown:: Exercise 3 -- ISA Hierarchy Builder
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Design and implement a three-level ISA hierarchy from scratch, verify
    the shared-PK relationships with live inserts, and then evolve the
    schema safely by adding a new subtype.


    **Specification**

    A robotics lab tracks all personnel with the following hierarchy:

    - Every **person** has a unique person ID (auto-generated), a first
      name, a last name, and a mandatory email address (unique across all
      persons).
    - Every **researcher** is a person and additionally has a research
      area (mandatory text) and an ORCID identifier (optional, but unique
      when present, exactly 19 characters: ``0000-0000-0000-0000`` format).
    - Every **graduate_researcher** is a researcher and additionally has
      a thesis title (mandatory) and an expected graduation year
      (mandatory integer, must be between 2020 and 2040).

    **Tasks**

    1. Write the ``CREATE TABLE`` statements for all three tables in the
       correct creation order. Use ``GENERATED ALWAYS AS IDENTITY`` for the
       supertype PK. Name all constraints.

    2. Insert the following data in the correct order:

       - Person: ``first_name='Maya'``, ``last_name='Patel'``, ``email='mpatel@umd.edu'``
       - Person: ``first_name='Leo'``, ``last_name='Nguyen'``, ``email='lnguyen@umd.edu'``
       - Maya is a researcher with ``research_area='Autonomous Navigation'``, ``orcid='0000-0002-1825-0097'``
       - Leo is a researcher with ``research_area='Computer Vision'``, no ORCID
       - Maya is a graduate researcher with ``thesis_title='LiDAR Odometry for Urban Environments'``, ``grad_year=2027``

    3. Attempt the following and explain the outcome of each:

       a. Insert a ``graduate_researcher`` row with ``person_id=99``.
       b. Insert a second ``graduate_researcher`` row for Maya.
       c. Delete Maya from ``person`` and then run
          ``SELECT * FROM graduate_researcher``.

    4. The lab now needs a new subtype: **postdoc_researcher**, which is a
       researcher with a mandatory ``start_date`` (DATE) and an optional
       ``end_date`` (DATE, must be after ``start_date`` if provided). Write
       the ``CREATE TABLE`` statement. Leo is a postdoc starting
       ``2025-09-01``. Write the insert sequence.

    .. important::

       Part 3c demonstrates a two-hop cascade: deleting from ``person``
       cascades to ``researcher``, which cascades to ``graduate_researcher``.
       Verify that all three rows disappear with a single ``DELETE``.


    **Deliverables**

    - ``CREATE TABLE`` statements for all three original tables
    - Insert sequence for Tasks 2 data (person inserts first, then researcher, then graduate_researcher)
    - Outcome and explanation for each of 3a, 3b, and 3c
    - ``CREATE TABLE`` for ``postdoc_researcher`` and insert sequence for Leo


.. dropdown:: Exercise 4 -- Schema Migration Challenge
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Apply the full range of ``ALTER TABLE`` operations to evolve a live
    schema through four requirements changes, choosing the safest migration
    path for each and explaining why each approach avoids data loss or
    downtime.


    **Specification**

    Start with this simplified ``course_section`` table and three rows of
    sample data:

    .. code-block:: sql

       CREATE TABLE course_section (
           section_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
           course_id  VARCHAR(10) NOT NULL,
           section_no VARCHAR(10) NOT NULL,
           capacity   INTEGER
       );

       INSERT INTO course_section (course_id, section_no, capacity)
           VALUES ('ENPM818T', '0101', 30),
                  ('ENPM605',  '0101', 25),
                  ('ENPM702',  '0101', 40);

    You will now apply four independent requirements changes to this table.
    For each change, write the SQL and briefly explain why you chose that
    approach over alternatives.

    **Requirement R1 -- Capacity is now mandatory**

    ``capacity`` must always be present and must be between 1 and 500.
    The table already has three rows, all with non-null capacities.
    Add ``NOT NULL`` and a ``CHECK`` constraint using the safe migration
    pattern (do not recreate the table). Confirm the constraint is marked
    valid after Step 4.

    **Requirement R2 -- Add a meeting room column**

    Add a ``meeting_room VARCHAR(20)`` column. The business rule says a
    room may be unknown at the time of section creation, so ``NULL`` is
    allowed. However, when a room is assigned, it must follow the pattern
    ``BLDG-NNN`` (building code, a hyphen, and a three-digit room number).
    Write the ``ALTER TABLE`` to add the column with an appropriate
    ``CHECK`` constraint. Use ``~`` (PostgreSQL regex match) in the
    constraint expression.

    **Requirement R3 -- Rename and retype the section identifier**

    The registrar's office requires renaming ``section_no`` to
    ``section_code`` and changing its type from ``VARCHAR(10)`` to
    ``CHAR(4)`` (all section codes are exactly four characters). Write
    the two ``ALTER TABLE`` statements needed. Explain whether either
    operation triggers a table rewrite.

    **Requirement R4 -- Detect and repair a naming mistake**

    You realize ``section_id`` uses an unnamed system-generated PK
    constraint (``course_section_pkey``). The course naming convention
    requires ``pk_course_section``. Without dropping and recreating the
    table, rename the constraint. Research and write the single
    ``ALTER TABLE`` statement that renames an existing constraint.

    .. tip::

       For R2, PostgreSQL regex: ``meeting_room ~ '^[A-Z]+-[0-9]{3}$'``
       matches ``IRB-112`` but not ``irb112`` or ``IRB-12``. Test your
       constraint by inserting both valid and invalid room codes.

    .. tip::

       For R4, look at ``ALTER TABLE ... RENAME CONSTRAINT``.


    **Deliverables**

    - Complete SQL for each of R1 through R4
    - Brief explanation for each (2-3 sentences: why this approach, what alternatives exist)
    - ``SELECT conname, convalidated FROM pg_constraint WHERE conrelid = 'course_section'::regclass`` output after all four changes
