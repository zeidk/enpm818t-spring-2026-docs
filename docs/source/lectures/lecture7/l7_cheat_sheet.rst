====================================================
Cheat Sheet
====================================================

A condensed, box-by-box reference covering all major topics from
Lecture 7: DML statements, ``RETURNING``, ``ON CONFLICT``, transaction
control, ACID and isolation levels, psycopg3 connection and query patterns,
connection pooling, and the repository pattern.

----

DML Quick Reference
--------------------

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - **Statement**
     - **Key rule**
   * - ``INSERT INTO t (cols) VALUES (...)``
     - Always include the column list; omit identity columns
   * - ``INSERT ... RETURNING col``
     - Capture generated PK in the same round trip; safer than ``MAX()``
   * - Multi-row ``INSERT``
     - One ``VALUES`` clause, multiple tuples; atomic; one round trip
   * - ``INSERT ... ON CONFLICT DO NOTHING``
     - Skip conflicting rows silently; idempotent seed scripts
   * - ``INSERT ... ON CONFLICT (col) DO UPDATE SET col = EXCLUDED.col``
     - Upsert; ``EXCLUDED`` refers to the incoming blocked row
   * - ``UPDATE t SET col = val WHERE condition``
     - **Always include WHERE**; run ``SELECT`` with same ``WHERE`` first
   * - ``UPDATE ... RETURNING``
     - Returns **new** values after update; confirms which rows changed
   * - ``DELETE FROM t WHERE condition``
     - **Always include WHERE**; run ``\d+ t`` first to check cascade scope
   * - ``DELETE ... RETURNING``
     - Returns values **before** deletion; use for audit trails

----

RETURNING on All Three DML Statements
--------------------------------------

.. list-table::
   :widths: 18 30 52
   :header-rows: 1
   :class: compact-table

   * - **Statement**
     - **Returns**
     - **Typical use**
   * - ``INSERT ... RETURNING``
     - Values just written (including generated PK)
     - Thread identity PK into ISA subtype inserts
   * - ``UPDATE ... RETURNING``
     - **New** values after the update
     - Confirm which rows changed and what they now contain
   * - ``DELETE ... RETURNING``
     - Values **before** deletion
     - Audit log; capture cascaded rows before parent delete

----

ON CONFLICT Patterns
---------------------

.. code-block:: sql

   -- Skip duplicates silently
   INSERT INTO department (dept_name)
   VALUES ('Physics')
   ON CONFLICT DO NOTHING;

   -- Upsert: insert or update
   INSERT INTO course (course_id, title, credits)
   VALUES ('ENPM818T', 'Databases', 3)
   ON CONFLICT (course_id) DO UPDATE
       SET title   = EXCLUDED.title,
           credits = EXCLUDED.credits;

``EXCLUDED`` is the alias for the incoming row that was blocked.
``ON CONFLICT (col)`` is required for ``DO UPDATE``; optional for ``DO NOTHING``.

----

Safe UPDATE / DELETE Workflow
-------------------------------

.. code-block:: sql

   -- Step 1: preview the target set
   SELECT person_id, gpa, academic_standing
   FROM student
   WHERE gpa < 2.0;

   -- Step 2: run UPDATE only after confirming the preview
   UPDATE student
   SET academic_standing = 'Probation'
   WHERE gpa < 2.0
   RETURNING person_id, gpa, academic_standing;

.. code-block:: text

   -- Before DELETE: inspect cascade scope in psql
   \d+ student

**Rule**: never run ``UPDATE`` or ``DELETE`` without ``WHERE``.
Always run the equivalent ``SELECT`` first.

----

ACID Properties
----------------

.. list-table::
   :widths: 16 22 30 32
   :header-rows: 1
   :class: compact-table

   * - **Property**
     - **What it means**
     - **Without it**
     - **PostgreSQL mechanism**
   * - Atomicity
     - All-or-nothing commit
     - Half-finished enrollment (capacity decremented, no row inserted)
     - ``ROLLBACK`` undoes all partial work
   * - Consistency
     - Every commit satisfies all constraints
     - GPA 5.0 stored; FK references missing row
     - ``CHECK``, ``FOREIGN KEY``, ``NOT NULL`` at commit
   * - Isolation
     - In-progress work invisible to others
     - Two sessions both read ``capacity = 1``; both enroll; capacity = -1
     - MVCC snapshots; ``FOR UPDATE`` row locks
   * - Durability
     - Committed data survives crashes
     - Power cut erases the last committed transaction
     - WAL flushed to disk before ``COMMIT`` returns

----

Transaction Control
--------------------

.. code-block:: sql

   -- Explicit transaction (happy path)
   BEGIN;
       UPDATE course_section SET capacity = capacity - 1
           WHERE course_id = 'ENPM818T' AND section_no = '0101';
       INSERT INTO enrollment (student_person_id, course_id, section_no)
           VALUES (1, 'ENPM818T', '0101');
   COMMIT;

   -- Rollback path
   BEGIN;
       -- ... statements ...
   ROLLBACK;   -- discards ALL work since BEGIN

   -- Partial rollback with SAVEPOINT
   BEGIN;
       INSERT INTO enrollment VALUES (1, 'ENPM818T', '0101');
       INSERT INTO enrollment VALUES (2, 'ENPM605',  '0101');
       SAVEPOINT after_two;
       INSERT INTO enrollment VALUES (3, 'ENPM702',  '0101');  -- may fail
       ROLLBACK TO SAVEPOINT after_two;   -- undo row 3 only; rows 1,2 kept
       INSERT INTO enrollment VALUES (4, 'ENPM702',  '0101');  -- replacement
   COMMIT;

----

Isolation Levels vs. Anomalies
--------------------------------

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

\*PostgreSQL ``REPEATABLE READ`` prevents phantoms; SQL standard only requires
``SERIALIZABLE`` to do so. PostgreSQL silently upgrades ``READ UNCOMMITTED``
to ``READ COMMITTED``.

**Default**: ``READ COMMITTED``.
**For GP2**: ``READ COMMITTED`` + ``SELECT ... FOR UPDATE`` covers most cases.

----

SELECT ... FOR UPDATE (Lost-Update Prevention)
-----------------------------------------------

.. code-block:: sql

   BEGIN;
   SELECT capacity FROM course_section
   WHERE course_id = 'ENPM818T' AND section_no = '0101'
   FOR UPDATE;                     -- row locked until COMMIT
   -- check capacity > 0 in application code
   UPDATE course_section SET capacity = capacity - 1
       WHERE course_id = 'ENPM818T' AND section_no = '0101';
   INSERT INTO enrollment (student_person_id, course_id, section_no)
       VALUES (1, 'ENPM818T', '0101');
   COMMIT;                         -- lock released

Session B's ``SELECT ... FOR UPDATE`` on the same row **blocks** until
Session A commits. Session B then reads the committed value -- preventing
the lost update.

----

psycopg3: Connection and Query Patterns
----------------------------------------

.. code-block:: python

   import psycopg, os
   from dotenv import load_dotenv
   from psycopg.rows import dict_row

   load_dotenv()
   conn_str = (
       f"host={os.getenv('DB_HOST','localhost')} "
       f"port={os.getenv('DB_PORT','5432')} "
       f"dbname={os.getenv('DB_NAME')} "
       f"user={os.getenv('DB_USER')} "
       f"password={os.getenv('DB_PASSWORD')}"
   )

   # Single query (dict rows)
   with psycopg.connect(conn_str) as conn:
       with conn.cursor(row_factory=dict_row) as cur:
           cur.execute("SELECT * FROM student WHERE person_id = %s", (1,))
           row = cur.fetchone()   # None if not found

   # Transaction
   with psycopg.connect(conn_str) as conn:
       with conn.transaction():
           conn.execute("UPDATE ...", (...,))
           conn.execute("INSERT ...", (...,))
           # COMMIT on clean exit; ROLLBACK on exception

**Never use f-strings for SQL values**. Always use ``%s`` placeholders.
Single-element tuple: ``(val,)`` not ``(val)``.

----

Tuple vs. Dict Cursor
-----------------------

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * -
     - **Tuple** (default)
     - **Dict** (``row_factory=dict_row``)
   * - Access
     - ``row[0]``, ``row[1]``
     - ``row['person_id']``
   * - Fragility
     - Breaks if columns reordered
     - Safe; name-based
   * - Readability
     - Low
     - High
   * - Speed
     - Slightly faster
     - Negligible difference
   * - **Use in GP2**
     - Avoid
     - **Use this everywhere**

----

Autocommit: psql vs. psycopg3
-------------------------------

.. list-table::
   :widths: 30 35 35
   :header-rows: 1
   :class: compact-table

   * -
     - **psql**
     - **psycopg3**
   * - Default mode
     - Autocommit
     - Transaction (no autocommit)
   * - ``INSERT`` visible?
     - Immediately
     - After ``conn.commit()`` or ``conn.transaction()``
   * - DDL support
     - Direct
     - Set ``conn.autocommit = True``

**Most common bug**: INSERT runs in psycopg3 but the row is invisible in
psql because the transaction was never committed. Fix: always use
``conn.transaction()`` for DML.

----

Connection Pool (DatabaseConfig)
----------------------------------

.. code-block:: python

   # config/database.py
   import psycopg_pool, os
   from dotenv import load_dotenv
   load_dotenv()

   class DatabaseConfig:
       _pool = None

       @classmethod
       def _conninfo(cls):
           return (
               f"host={os.getenv('DB_HOST','localhost')} "
               f"port={os.getenv('DB_PORT','5432')} "
               f"dbname={os.getenv('DB_NAME')} "
               f"user={os.getenv('DB_USER')} "
               f"password={os.getenv('DB_PASSWORD')}"
           )

       @classmethod
       def initialize(cls):
           cls._pool = psycopg_pool.ConnectionPool(
               conninfo=cls._conninfo(), min_size=2, max_size=10, open=True
           )

       @classmethod
       def get_connection(cls):
           if cls._pool is None:
               cls.initialize()
           return cls._pool.connection()

       @classmethod
       def close(cls):
           if cls._pool:
               cls._pool.close()

**Rule**: call ``initialize()`` once at startup in ``main.py``.
Never call ``psycopg.connect()`` directly in repository methods.

----

Repository Pattern: Five Layers
---------------------------------

.. list-table::
   :widths: 20 38 42
   :header-rows: 1
   :class: compact-table

   * - **Layer**
     - **Owns**
     - **Must NOT contain**
   * - ``config/``
     - Connection pool
     - SQL queries, business logic
   * - ``models/``
     - Dataclasses (pure data)
     - ``import psycopg``, DB calls
   * - ``repositories/``
     - All ``cur.execute()`` calls; one method = one query
     - Business logic (``if gpa < x``), ``input()``
   * - ``services/``
     - Business rules, ``conn.transaction()``
     - ``cur.execute()``, ``input()``
   * - ``cli/``
     - User I/O, menu loop
     - SQL strings, business logic

**Column renamed?** Edit one repository method. Nothing else changes.

----

StudentRepository Skeleton
---------------------------

.. code-block:: python

   # repositories/student_repo.py
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
                   return cur.fetchone()   # None if not found

       def find_all(self):
           with DatabaseConfig.get_connection() as conn:
               with conn.cursor(row_factory=dict_row) as cur:
                   cur.execute("SELECT * FROM student ORDER BY person_id")
                   return cur.fetchall()   # [] if no rows

----

EnrollmentService Skeleton
---------------------------

.. code-block:: python

   # services/enrollment_service.py
   from config.database import DatabaseConfig
   from psycopg.errors import UniqueViolation, ForeignKeyViolation

   class EnrollmentService:

       def enroll_student(self, person_id, course_id, section_no):
           try:
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
           except UniqueViolation:
               raise ValueError("Already enrolled")
           except ForeignKeyViolation:
               raise ValueError("Student or section not found")

----

Seven Most Common DML and Python Mistakes
------------------------------------------

.. list-table::
   :widths: 8 40 52
   :header-rows: 1
   :class: compact-table

   * - **#**
     - **Mistake**
     - **Fix**
   * - M1
     - ``UPDATE``/``DELETE`` without ``WHERE``
     - Run ``SELECT`` with same ``WHERE`` first; use ``RETURNING`` to verify
   * - M2
     - SQL injection via f-string: ``f"... = '{val}'"``
     - Parameterized: ``cur.execute(sql, (val,))``
   * - M3
     - Hardcoded credentials in source code
     - ``.env`` + ``os.getenv()``; add ``.env`` to ``.gitignore`` before first commit
   * - M4
     - ISA insert without ``RETURNING``
     - ``INSERT INTO person ... RETURNING person_id``; use returned value for subtype
   * - M5
     - ``psycopg.connect()`` per query
     - ``psycopg_pool.ConnectionPool``; initialize once in ``main.py``
   * - M6
     - No commit (INSERT invisible in psql)
     - Use ``conn.transaction()`` for DML; it auto-commits on exit
   * - M7
     - ``import psycopg2`` with psycopg3 installed
     - Use ``import psycopg``; they are separate packages
