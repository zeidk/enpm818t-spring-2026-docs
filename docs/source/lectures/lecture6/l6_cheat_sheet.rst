====================================================
Cheat Sheet
====================================================

A condensed, box-by-box reference covering all major topics from
Lecture 6: data types, constraints, identity columns, ISA / category
patterns, deferrable constraints, ALTER TABLE, and the DELETE /
TRUNCATE / DROP comparison.

----

Data Types
----------

.. list-table::
   :widths: 18 20 42
   :header-rows: 1
   :class: compact-table

   * - **Type**
     - **Use for**
     - **Key rule**
   * - ``INTEGER``
     - counts, IDs, credits
     - Default whole-number choice
   * - ``BIGINT``
     - large IDs, row counts
     - Only when overflow is realistic
   * - ``NUMERIC(p,s)``
     - GPA, money, exact decimals
     - **Never** use ``FLOAT`` for these
   * - ``FLOAT``
     - scientific measurements
     - Binary rounding error; never for GPA or money
   * - ``VARCHAR(n)``
     - strings with a real length limit
     - Use only when n is a business rule
   * - ``TEXT``
     - all other variable-length strings
     - Identical performance to ``VARCHAR`` in PostgreSQL
   * - ``CHAR(n)``
     - fixed-width codes
     - ``state CHAR(2)``, ``zip CHAR(5)``
   * - ``DATE``
     - calendar dates
     - No time component; use for ``hire_date``, ``date_of_birth``
   * - ``TIMESTAMPTZ``
     - timestamps with time zone
     - Always prefer over ``TIMESTAMP``
   * - ``BOOLEAN``
     - true/false flags
     - Three-valued: ``TRUE``, ``FALSE``, ``NULL``
   * - ``UUID``
     - distributed PKs
     - ``gen_random_uuid()`` built-in since PG 13

----

Constraint Quick Reference
--------------------------

.. list-table::
   :widths: 20 25 35
   :header-rows: 1
   :class: compact-table

   * - **Constraint**
     - **Purpose**
     - **Critical detail**
   * - ``PRIMARY KEY``
     - Unique row identifier
     - Implies ``NOT NULL + UNIQUE``; one per table
   * - ``FOREIGN KEY``
     - Referential integrity
     - Parent must exist before child; name with ``fk_child_parent``
   * - ``NOT NULL``
     - Mandatory column value
     - Default is nullable; always explicit opt-in
   * - ``UNIQUE``
     - Distinct non-null values
     - Multiple ``NULL``s allowed (``NULL`` is never equal to ``NULL``)
   * - ``UNIQUE NULLS NOT DISTINCT``
     - Distinct including at most one ``NULL``
     - PostgreSQL 15+; use when ``NULL`` is a singleton state
   * - ``CHECK``
     - Row-level Boolean expression
     - ``NULL`` passes silently; always pair with ``NOT NULL``
   * - ``EXCLUDE USING GIST``
     - No two rows satisfy operator pair
     - Generalises ``UNIQUE`` to overlap; requires ``btree_gist``

----

SERIAL vs. GENERATED ALWAYS AS IDENTITY
-----------------------------------------

.. list-table::
   :widths: 42 29 29
   :header-rows: 1
   :class: compact-table

   * - **Property**
     - ``SERIAL``
     - ``GENERATED ALWAYS``
   * - SQL standard
     - No
     - Yes (SQL:2003)
   * - Explicit value bypass
     - Silent (no error)
     - Immediate error
   * - Visible in ``\d``
     - No
     - Yes
   * - Customizable inline
     - No
     - Yes (``START WITH``, ``INCREMENT BY``)
   * - Recommendation
     - Legacy; avoid in new schemas
     - **Preferred for all new schemas**

After restoring rows with ``OVERRIDING SYSTEM VALUE``, always call:

.. code-block:: sql

   SELECT setval('table_col_seq', (SELECT MAX(col) FROM table));

----

ON DELETE / ON UPDATE Actions
------------------------------

.. list-table::
   :widths: 20 35 30
   :header-rows: 1
   :class: compact-table

   * - **Action**
     - **Effect on child rows**
     - **Use when...**
   * - ``NO ACTION`` (default)
     - Parent change blocked at statement end; deferrable
     - General-purpose default; compatible with ``DEFERRABLE``
   * - ``RESTRICT``
     - Parent change blocked immediately; never deferrable
     - Orphaning is always a mistake and no deferral is needed
   * - ``CASCADE``
     - Child rows deleted or updated to match
     - Child has no meaning without the parent
   * - ``SET NULL``
     - FK column set to ``NULL``
     - Child survives independently; FK column must be nullable
   * - ``SET DEFAULT``
     - FK column reset to declared default
     - Sentinel/fallback parent row always exists

----

ISA Shared-PK Pattern
---------------------

.. code-block:: sql

   -- Supertype: identity sequence lives here only
   CREATE TABLE person (
       person_id  INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       first_name VARCHAR(50) NOT NULL,
       last_name  VARCHAR(50) NOT NULL
   );

   -- Subtype: PK = FK; no GENERATED ALWAYS
   CREATE TABLE student (
       person_id  INTEGER PRIMARY KEY,
       student_id VARCHAR(20) NOT NULL UNIQUE,
       CONSTRAINT fk_student_person
           FOREIGN KEY (person_id)
               REFERENCES person (person_id)
               ON DELETE CASCADE
   );

**Rules**: one identity sequence per entity hierarchy; subtype PK declared
``INTEGER PRIMARY KEY`` only (no ``GENERATED ALWAYS``); ``ON DELETE CASCADE``
ensures subtype rows are removed automatically.

----

Category Exclusive-Arc Pattern
--------------------------------

.. code-block:: sql

   CREATE TABLE vehicle_owner (
       owner_id       INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
       person_ssn     VARCHAR(11),
       company_tax_id VARCHAR(10),
       bank_routing   VARCHAR(9),
       CONSTRAINT chk_exclusive_arc CHECK (
           (person_ssn     IS NOT NULL)::INT +
           (company_tax_id IS NOT NULL)::INT +
           (bank_routing   IS NOT NULL)::INT = 1
       )
   );

**Rule**: cast each ``IS NOT NULL`` to ``INT`` (0 or 1) and assert the sum
equals exactly 1. Exactly one FK must be non-null; zero or two or more are
rejected.

----

Deferrable Constraints
-----------------------

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Mode**
     - Mode 1
     - Mode 2
     - Default (non-deferrable)
   * - Declaration
     - ``DEFERRABLE INITIALLY DEFERRED``
     - ``DEFERRABLE INITIALLY IMMEDIATE``
     - ``NOT DEFERRABLE``
   * - Check timing
     - ``COMMIT``
     - Statement end (by default)
     - Statement end
   * - Always deferred?
     - Yes
     - No
     - No
   * - Per-transaction opt-in?
     - N/A
     - ``SET CONSTRAINTS name DEFERRED``
     - Not possible
   * - Use for
     - Circular FK dependencies
     - Deferral is the exception
     - All other FKs

**Deferrable constraint types**: ``FOREIGN KEY``, ``UNIQUE``, ``PRIMARY KEY``.
``NOT NULL`` and ``CHECK`` **cannot** be deferred.

----

Creation Order (University Schema)
------------------------------------

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

The ``department`` / ``professor`` circular FK requires
``DEFERRABLE INITIALLY DEFERRED`` on ``fk_dept_chair``.

----

ALTER TABLE Operations
-----------------------

.. list-table::
   :widths: 45 20 30
   :header-rows: 1
   :class: compact-table

   * - **Operation**
     - **Table rewrite?**
     - **Cost**
   * - ``ADD COLUMN`` nullable
     - No
     - Instant (metadata only)
   * - ``ADD COLUMN NOT NULL`` + constant default (PG 11+)
     - No
     - Instant
   * - ``ADD COLUMN NOT NULL`` no default
     - Yes
     - Expensive (full scan)
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
     - Validates all existing rows
   * - ``DROP CONSTRAINT``
     - No
     - Instant
   * - ``RENAME CONSTRAINT``
     - No
     - Instant

----

Safe Migration Pattern (4 Steps)
----------------------------------

.. code-block:: sql

   -- Step 1: add nullable (instant, metadata lock only)
   ALTER TABLE professor ADD COLUMN office_number VARCHAR(10);

   -- Step 2: backfill existing rows (batch with LIMIT in production)
   UPDATE professor SET office_number = 'TBD' WHERE office_number IS NULL;

   -- Step 3: add constraint NOT VALID (no existing-row scan; new writes checked immediately)
   ALTER TABLE professor
       ADD CONSTRAINT nn_office_number
           CHECK (office_number IS NOT NULL)
           NOT VALID;

   -- Step 4: validate with weaker lock (reads continue during scan)
   ALTER TABLE professor VALIDATE CONSTRAINT nn_office_number;

   -- Verify
   SELECT conname, convalidated FROM pg_constraint
   WHERE conrelid = 'professor'::regclass;

----

DELETE vs. TRUNCATE vs. DROP
------------------------------

.. list-table::
   :widths: 28 24 24 24
   :header-rows: 1
   :class: compact-table

   * - **Property**
     - ``DELETE``
     - ``TRUNCATE``
     - ``DROP``
   * - What survives
     - Structure + some rows
     - Structure (all rows gone)
     - Nothing
   * - ``WHERE`` clause
     - Yes
     - No
     - No
   * - Row-level triggers
     - Yes
     - No
     - No
   * - Rollbackable
     - Yes
     - Yes (PostgreSQL)
     - Yes (in a transaction)
   * - Speed (large table)
     - Slow (WAL per row)
     - Fast (bulk dealloc)
     - Fast
   * - Sequence reset
     - No
     - ``RESTART IDENTITY``
     - N/A

**Before any DROP or TRUNCATE CASCADE**: run ``\d+ tablename`` to inspect
what references the table.

----

Schema Verification Quick Reference
--------------------------------------

.. list-table::
   :widths: 30 30 40
   :header-rows: 1
   :class: compact-table

   * - **Goal**
     - **psql command**
     - **Catalog query**
   * - List columns and constraints
     - ``\d tablename``
     - ``SELECT * FROM information_schema.columns WHERE table_name = '...'``
   * - Show FK references (incoming and outgoing)
     - ``\d+ tablename``
     - ``SELECT * FROM information_schema.referential_constraints``
   * - List all constraints with types
     - ``\d tablename``
     - ``SELECT constraint_name, constraint_type FROM information_schema.table_constraints WHERE table_name = '...'``
   * - Check FK delete/update actions
     - ``\d+ tablename``
     - ``SELECT constraint_name, delete_rule, update_rule FROM information_schema.referential_constraints``
   * - Inspect sequence values
     - ``\d tablename``
     - ``SELECT sequencename, last_value FROM pg_sequences WHERE schemaname = 'public'``
   * - Verify constraint validation status
     - N/A
     - ``SELECT conname, convalidated FROM pg_constraint WHERE conrelid = 'tablename'::regclass``

----

Naming Conventions
-------------------

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
   * - Primary key column
     - ``table_id``
     - ``dept_id``
   * - FK column
     - Same name as referenced PK
     - ``dept_id`` in ``professor``
   * - PK constraint
     - ``pk_table``
     - ``pk_enrollment``
   * - FK constraint
     - ``fk_child_parent``
     - ``fk_prof_dept``
   * - UNIQUE constraint
     - ``uq_table_col``
     - ``uq_person_email``
   * - CHECK constraint
     - ``chk_table_col``
     - ``chk_gpa``
   * - EXCLUDE constraint
     - ``excl_table_desc``
     - ``excl_room_overlap``

----

The Six Most Common DDL Mistakes
----------------------------------

.. list-table::
   :widths: 10 30 30 30
   :header-rows: 1
   :class: compact-table

   * - **#**
     - **Mistake**
     - **Wrong**
     - **Correct**
   * - M1
     - Missing ``NOT NULL`` on mandatory column
     - ``title VARCHAR(150)``
     - ``title VARCHAR(150) NOT NULL``
   * - M2
     - ``FLOAT`` for GPA or money
     - ``gpa FLOAT``
     - ``gpa NUMERIC(3,2)``
   * - M3
     - ``CHECK`` without ``NOT NULL``
     - ``gpa NUMERIC(3,2) CHECK (gpa >= 0)``
     - ``gpa NUMERIC(3,2) NOT NULL CHECK (gpa >= 0)``
   * - M4
     - Anonymous constraints
     - ``email VARCHAR(100) UNIQUE``
     - ``CONSTRAINT uq_person_email UNIQUE (email)``
   * - M5
     - ``VARCHAR(255)`` out of habit
     - ``name VARCHAR(255)``
     - ``name TEXT``
   * - M6
     - ``DROP`` without checking dependencies
     - ``DROP TABLE student CASCADE``
     - ``\d+ student`` first, then targeted drop
