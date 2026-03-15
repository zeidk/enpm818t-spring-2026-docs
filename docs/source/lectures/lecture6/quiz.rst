====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 6: From Logical to Physical.
Topics include PostgreSQL data types, integrity constraints (PRIMARY KEY,
FOREIGN KEY, NOT NULL, UNIQUE, CHECK, EXCLUDE), identity columns (SERIAL vs.
GENERATED ALWAYS AS IDENTITY), ISA and category patterns, deferrable
constraints, ALTER TABLE operations, and the DELETE / TRUNCATE / DROP
distinction.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-18)
================================

.. admonition:: Question 1
   :class: hint

   Which PostgreSQL data type should you always use for a GPA or monetary
   amount column?

   A. ``FLOAT``

   B. ``REAL``

   C. ``NUMERIC(p,s)``

   D. ``DOUBLE PRECISION``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``NUMERIC(p,s)``

   ``FLOAT``, ``REAL``, and ``DOUBLE PRECISION`` use binary floating-point
   storage and cannot represent most decimal fractions exactly. ``NUMERIC``
   stores exact decimal values, so ``3.9`` is stored and retrieved as exactly
   ``3.9``, making equality comparisons reliable.


.. admonition:: Question 2
   :class: hint

   What is the key difference between ``VARCHAR(n)`` and ``TEXT`` in
   PostgreSQL?

   A. ``TEXT`` has a lower storage overhead than ``VARCHAR(n)``.

   B. ``VARCHAR(n)`` enforces a maximum length; ``TEXT`` has no limit.
      Their internal storage and performance are identical in PostgreSQL.

   C. ``TEXT`` is only appropriate for columns with more than 255 characters.

   D. ``VARCHAR(n)`` is deprecated in PostgreSQL 15 and above.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``VARCHAR(n)`` enforces a maximum length; ``TEXT`` has no limit.
   Their internal storage and performance are identical in PostgreSQL.

   The only difference is the length check. Use ``TEXT`` as your default
   for variable-length strings. Reserve ``VARCHAR(n)`` for columns where
   the length limit is a real business rule (e.g., a two-character state code).


.. admonition:: Question 3
   :class: hint

   Which statement about ``GENERATED ALWAYS AS IDENTITY`` is correct?

   A. It is equivalent to ``SERIAL`` and can be used interchangeably.

   B. It allows explicit value inserts without any special syntax.

   C. It rejects explicit value inserts immediately; ``OVERRIDING SYSTEM VALUE`` is required to bypass it.

   D. It creates a separate sequence table visible in ``\d``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It rejects explicit value inserts immediately; ``OVERRIDING SYSTEM VALUE`` is required to bypass it.

   ``SERIAL`` wires the sequence as a ``DEFAULT``, so explicit values are
   silently accepted. ``GENERATED ALWAYS`` hands ownership to the engine:
   inserting a manual value without ``OVERRIDING SYSTEM VALUE`` raises an
   error immediately, preventing the silent sequence desynchronization bug
   that ``SERIAL`` allows.


.. admonition:: Question 4
   :class: hint

   After using ``OVERRIDING SYSTEM VALUE`` to restore three rows with IDs 1,
   2, and 3 into a table with ``GENERATED ALWAYS AS IDENTITY``, what must
   you do before the next auto-insert?

   A. Nothing; the sequence automatically advances to the highest existing ID.

   B. Drop and recreate the sequence.

   C. Call ``setval()`` to advance the sequence past the highest existing ID.

   D. Run ``ALTER TABLE ... RESTART WITH 4``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Call ``setval()`` to advance the sequence past the highest existing ID.

   ``OVERRIDING SYSTEM VALUE`` bypasses the sequence guard but does not
   advance the counter. The sequence remains at 1. The next auto-insert will
   call ``nextval()``, get 1, and collide with the restored row. The fix is:
   ``SELECT setval('table_col_seq', (SELECT MAX(col) FROM table));``


.. admonition:: Question 5
   :class: hint

   In the shared-PK ISA strategy, why is there no ``GENERATED ALWAYS AS IDENTITY``
   on the subtype table's primary key column?

   A. The subtype cannot have a primary key.

   B. The subtype PK must match the supertype PK value, which comes from the supertype insert, not from a new sequence.

   C. PostgreSQL does not allow identity columns on tables with foreign keys.

   D. The subtype inherits the sequence automatically from the supertype.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The subtype PK must match the supertype PK value, which comes from the supertype insert, not from a new sequence.

   The entire point of the shared-PK strategy is that both tables identify
   the same entity with the same value. The identity sequence lives on the
   supertype only. The application inserts the generated supertype ID into
   the subtype as its PK. Adding ``GENERATED ALWAYS`` to the subtype would
   create an independent counter, breaking the shared identity.


.. admonition:: Question 6
   :class: hint

   Which ``ON DELETE`` action removes child rows automatically when the
   parent row is deleted?

   A. ``SET NULL``

   B. ``RESTRICT``

   C. ``NO ACTION``

   D. ``CASCADE``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``CASCADE``

   ``CASCADE`` propagates the delete to all child rows automatically.
   ``SET NULL`` sets the FK column to ``NULL`` instead of removing the row.
   ``RESTRICT`` and ``NO ACTION`` both reject the parent delete when child
   rows exist (``RESTRICT`` fires immediately; ``NO ACTION`` fires at
   statement end).


.. admonition:: Question 7
   :class: hint

   What problem does ``DEFERRABLE INITIALLY DEFERRED`` solve for a circular
   FK dependency between ``department`` and ``professor``?

   A. It allows the FK to reference columns that are not primary keys.

   B. It moves the FK integrity check from statement end to transaction commit, allowing both rows to be inserted within a single transaction before the check fires.

   C. It disables the FK constraint entirely for the duration of the transaction.

   D. It creates a temporary table to hold intermediate values during the insert.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It moves the FK integrity check from statement end to transaction commit, allowing both rows to be inserted within a single transaction before the check fires.

   With immediate checking, no valid insert order exists when two tables
   reference each other. Deferring the check to ``COMMIT`` allows all rows to
   be written first; the FK is verified once at commit when both sides are
   in place.


.. admonition:: Question 8
   :class: hint

   A column declared ``gpa NUMERIC(3,2) CHECK (gpa >= 0.0)`` without ``NOT NULL``
   receives an insert with ``gpa = NULL``. What happens?

   A. The insert is rejected because ``NULL`` is not ``>= 0.0``.

   B. The insert is accepted because ``NULL >= 0.0`` evaluates to ``NULL``, not ``FALSE``, and the check passes.

   C. The insert is rejected because ``NUMERIC`` columns cannot store ``NULL``.

   D. The insert is accepted only if the column has a ``DEFAULT`` clause.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The insert is accepted because ``NULL >= 0.0`` evaluates to ``NULL``, not ``FALSE``, and the check passes.

   SQL uses three-valued logic (TRUE, FALSE, NULL). A ``CHECK`` constraint
   only rejects a row when the expression evaluates to definitively ``FALSE``.
   ``NULL`` is unknown, so the check does not fire. Always pair a ``CHECK``
   with ``NOT NULL`` unless ``NULL`` is a legitimate value.


.. admonition:: Question 9
   :class: hint

   Which of the following correctly explains why two ``NULL`` values can
   coexist in a column declared ``UNIQUE``?

   A. ``UNIQUE`` only applies to non-null values by design; ``NULL`` is not a value.

   B. In SQL the expression ``NULL = NULL`` evaluates to ``NULL``, not ``TRUE``, so two ``NULL`` are never considered equal by the uniqueness check.

   C. PostgreSQL treats ``NULL`` as 0 for uniqueness comparison purposes.

   D. ``UNIQUE`` constraints are not enforced until a row is queried.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- In SQL the expression ``NULL = NULL`` evaluates to ``NULL``, not ``TRUE``, so two ``NULL`` are never considered equal by the uniqueness check.

   SQL's three-valued logic means that two unknown values cannot be compared.
   The uniqueness check never fires when comparing two ``NULL`` values because
   the comparison result is ``NULL`` rather than ``TRUE``. PostgreSQL 15 introduced
   ``UNIQUE NULLS NOT DISTINCT`` for cases where at most one ``NULL`` should
   be allowed.


.. admonition:: Question 10
   :class: hint

   What does the ``EXCLUDE USING GIST`` constraint enforce that a standard
   ``UNIQUE`` constraint cannot?

   A. It enforces that no two rows have the same value in a column.

   B. It enforces that no two rows satisfy a specified binary operator pair simultaneously, such as same room and overlapping time range.

   C. It enforces that column values match a regular expression pattern.

   D. It enforces referential integrity across tables.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It enforces that no two rows satisfy a specified binary operator pair simultaneously, such as same room and overlapping time range.

   ``UNIQUE`` tests for equality only. ``EXCLUDE`` generalizes to any binary
   operator: it rejects a new row if any existing row satisfies all the
   specified operator conditions simultaneously. The overlap operator ``&&``
   on a range type is the classic use case for preventing double-booking.


.. admonition:: Question 11
   :class: hint

   Which ``ALTER TABLE`` operation triggers a full table rewrite in PostgreSQL?

   A. Adding a nullable column with no default.

   B. Renaming a column.

   C. Dropping a column.

   D. Adding a ``NOT NULL`` column with no default to a non-empty table.

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- Adding a ``NOT NULL`` column with no default to a non-empty table.

   PostgreSQL must scan and rewrite every row to verify the ``NOT NULL``
   requirement. Adding a nullable column (A) is instant -- only metadata
   changes. Renaming (B) and dropping (C) are also instant metadata
   operations. Since PostgreSQL 11, adding ``NOT NULL`` with a constant
   default is also instant.


.. admonition:: Question 12
   :class: hint

   What is the correct order for the four-step safe migration pattern when
   adding a ``NOT NULL`` column to a large live table?

   A. Add column with ``NOT NULL``, backfill, validate, add constraint.

   B. Add nullable column, backfill, add ``NOT VALID`` constraint, validate constraint.

   C. Add nullable column, validate constraint, backfill, add ``NOT NULL``.

   D. Backfill, add nullable column, add constraint, validate.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Add nullable column, backfill, add ``NOT VALID`` constraint, validate constraint.

   Step 1 (add nullable) acquires only a metadata lock. Step 2 (backfill)
   fills existing rows without a long-running lock. Step 3 (``NOT VALID``)
   adds the constraint without scanning existing rows; new writes are checked
   immediately. Step 4 (``VALIDATE``) scans existing rows with a weaker lock
   that allows concurrent reads.


.. admonition:: Question 13
   :class: hint

   Which of the following is TRUE about ``TRUNCATE`` compared to ``DELETE``
   without a ``WHERE`` clause?

   A. ``TRUNCATE`` fires row-level triggers; ``DELETE`` does not.

   B. ``TRUNCATE`` is faster on large tables and does not fire row-level triggers, but both are rollbackable in PostgreSQL.

   C. ``DELETE`` is faster because it uses a sequential scan; ``TRUNCATE`` rewrites the heap.

   D. ``TRUNCATE`` cannot be rolled back in any PostgreSQL version.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``TRUNCATE`` is faster on large tables and does not fire row-level triggers, but both are rollbackable in PostgreSQL.

   ``TRUNCATE`` deallocates the table's data pages in bulk, making it much
   faster than row-by-row ``DELETE`` on large tables. Unlike some other
   databases, PostgreSQL makes ``TRUNCATE`` transactional: it can be rolled
   back within a ``BEGIN`` / ``ROLLBACK`` block.


.. admonition:: Question 14
   :class: hint

   What does ``DROP TABLE student CASCADE`` do?

   A. Removes all rows from ``student`` but keeps the table structure.

   B. Removes the ``student`` table and all tables that have a FK referencing it.

   C. Removes the ``student`` table and all rows in tables that reference it, but keeps those tables intact.

   D. Removes the ``student`` table only if no other tables reference it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Removes the ``student`` table and all tables that have a FK referencing it.

   ``DROP ... CASCADE`` removes the table and all dependent objects,
   including FK constraints on other tables that reference ``student``.
   Depending on the schema, this can silently remove entire tables (like
   ``enrollment``) that happen to reference ``student``. Always run
   ``\d+ student`` before any ``DROP`` to inspect dependencies.


.. admonition:: Question 15
   :class: hint

   A named ``CHECK`` constraint ``chk_gpa`` is listed in an error message.
   An anonymous ``CHECK`` on the same column would appear as which of the
   following?

   A. ``check_constraint_violation``

   B. ``student_gpa_check`` (system-generated from table and column name)

   C. ``constraint_violation``

   D. ``unnamed_check``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``student_gpa_check`` (system-generated from table and column name)

   PostgreSQL generates constraint names from the table name, column name,
   and constraint type when no explicit name is given. The result is a
   readable but unpredictable name. Named constraints (``chk_gpa``) are
   immediately actionable in error messages and are the correct convention
   in production schemas.


.. admonition:: Question 16
   :class: hint

   Which constraint types support deferral in PostgreSQL?

   A. ``NOT NULL`` and ``CHECK`` only.

   B. ``FOREIGN KEY``, ``UNIQUE``, and ``PRIMARY KEY``.

   C. ``FOREIGN KEY`` only.

   D. All constraint types.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``FOREIGN KEY``, ``UNIQUE``, and ``PRIMARY KEY``.

   These three constraint types enforce structural relationships where a
   temporarily inconsistent state within a transaction is meaningful (e.g.,
   swapping key values). ``NOT NULL`` has no meaningful transient state
   (a value is either present or absent), and ``CHECK`` is a row-level
   expression with no cross-row dependency, so neither can be deferred.


.. admonition:: Question 17
   :class: hint

   What does ``TRUNCATE TABLE enrollment RESTART IDENTITY`` do compared to
   plain ``TRUNCATE TABLE enrollment``?

   A. It removes only the rows with the highest identity values.

   B. It removes all rows and resets the identity sequence to its initial start value.

   C. It removes all rows and drops the identity column.

   D. It is equivalent to ``DROP TABLE enrollment`` followed by a ``CREATE TABLE``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It removes all rows and resets the identity sequence to its initial start value.

   ``RESTART IDENTITY`` is useful when reloading a table from scratch (e.g.,
   at the start of a new semester). The next auto-insert will begin at the
   sequence's start value (typically 1 or the value specified in
   ``START WITH``). Without ``RESTART IDENTITY``, the sequence continues
   from where it left off even after truncation.


.. admonition:: Question 18
   :class: hint

   Which naming convention is correct for a foreign key constraint from the
   ``enrollment`` table to the ``student`` table?

   A. ``fk_student_enrollment``

   B. ``foreign_key_enrollment_student``

   C. ``fk_enrollment_student``

   D. ``enrollment_student_fk``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``fk_enrollment_student``

   The convention from the lecture is ``fk_child_parent``: the child table
   (``enrollment``) comes first, followed by the parent table (``student``).
   This convention immediately tells you the direction of the dependency from
   the constraint name alone.


----


True/False (Questions 19-28)
============================

.. admonition:: Question 19
   :class: hint

   **True or False:** In PostgreSQL, ``FLOAT`` and ``NUMERIC`` have identical
   storage precision.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``FLOAT`` uses binary floating-point representation, which cannot represent
   most decimal fractions exactly. ``NUMERIC`` stores exact decimal values.
   For GPA or monetary amounts, only ``NUMERIC`` is correct.


.. admonition:: Question 20
   :class: hint

   **True or False:** ``PRIMARY KEY`` is shorthand for ``NOT NULL UNIQUE``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A ``PRIMARY KEY`` constraint automatically enforces both ``NOT NULL`` and
   ``UNIQUE`` on the designated column(s). Declaring either ``NOT NULL`` or
   ``UNIQUE`` explicitly on a ``PRIMARY KEY`` column is redundant.


.. admonition:: Question 21
   :class: hint

   **True or False:** ``SERIAL`` and ``GENERATED ALWAYS AS IDENTITY`` behave
   identically when you insert a row without specifying the ID column.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Both auto-increment the sequence counter and assign the next value. The
   difference appears only when you attempt an explicit insert: ``SERIAL``
   silently accepts it; ``GENERATED ALWAYS`` rejects it immediately.


.. admonition:: Question 22
   :class: hint

   **True or False:** A ``CHECK`` constraint guarantees that a column cannot
   be ``NULL`` if the expression is written as ``CHECK (col > 0)``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``NULL > 0`` evaluates to ``NULL``, not ``FALSE``. The ``CHECK``
   constraint only fires when the expression is definitively ``FALSE``. A
   ``NULL`` value passes the check silently. A separate ``NOT NULL``
   constraint is required to block ``NULL`` values.


.. admonition:: Question 23
   :class: hint

   **True or False:** In the shared-PK ISA strategy, the subtype table
   creates its own identity sequence to generate subtype IDs independently.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The subtype PK receives its value from the supertype insert. The identity
   sequence lives on the supertype only. No sequence is created on the
   subtype; its PK column is declared ``INTEGER PRIMARY KEY`` (no
   ``GENERATED ALWAYS``).


.. admonition:: Question 24
   :class: hint

   **True or False:** ``TRUNCATE`` is always faster than ``DELETE`` on any
   table size.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``TRUNCATE`` is dramatically faster on large tables because it deallocates
   data pages in bulk. On a table with only a handful of rows, ``DELETE``
   and ``TRUNCATE`` have comparable performance. The advantage of
   ``TRUNCATE`` grows with table size.


.. admonition:: Question 25
   :class: hint

   **True or False:** ``DROP TABLE student`` will succeed even if
   ``enrollment`` has a foreign key referencing ``student``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   PostgreSQL rejects ``DROP TABLE`` when other tables hold FK constraints
   referencing the target table. ``DROP TABLE student CASCADE`` would
   succeed, but would also remove all dependent FK constraints (and
   potentially entire tables). Always check ``\d+ student`` before dropping.


.. admonition:: Question 26
   :class: hint

   **True or False:** Adding a nullable column with ``ALTER TABLE ... ADD COLUMN``
   triggers a full table rewrite in PostgreSQL.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Adding a nullable column is a metadata-only operation in PostgreSQL.
   Existing rows are not physically modified; the new column is treated as
   ``NULL`` for all existing rows without a table scan. The rewrite is only
   required for ``NOT NULL`` columns with no default on a non-empty table.


.. admonition:: Question 27
   :class: hint

   **True or False:** ``UNIQUE NULLS NOT DISTINCT`` allows multiple ``NULL``
   values in the column.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``UNIQUE NULLS NOT DISTINCT`` (PostgreSQL 15+) treats ``NULL`` as a
   comparable value for the purposes of the uniqueness check. At most one
   ``NULL`` is allowed. A second ``NULL`` insert is rejected just as a
   duplicate non-null value would be.


.. admonition:: Question 28
   :class: hint

   **True or False:** ``VALIDATE CONSTRAINT`` acquires an ``ACCESS EXCLUSIVE``
   lock, blocking all reads during validation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``VALIDATE CONSTRAINT`` acquires a ``SHARE UPDATE EXCLUSIVE`` lock, which
   allows concurrent reads. This is why the four-step migration pattern uses
   ``NOT VALID`` followed by a separate ``VALIDATE``: it avoids holding the
   stronger ``ACCESS EXCLUSIVE`` lock (which blocks reads) during the
   potentially slow full-table scan.


----


Essay Questions (Questions 29-32)
==================================

.. admonition:: Question 29
   :class: hint

   Explain the silent bypass bug that ``SERIAL`` introduces and describe
   exactly how ``GENERATED ALWAYS AS IDENTITY`` prevents it. Include
   the role of ``OVERRIDING SYSTEM VALUE`` and what you must do after using it.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``SERIAL`` wires the sequence as a column ``DEFAULT``. When you supply
     an explicit value, PostgreSQL uses your value and never calls the
     sequence, so the sequence counter stays frozen.
   - On the next auto-insert, ``nextval()`` returns a value that may already
     exist as an explicit ID, causing a duplicate key error on an otherwise
     legitimate insert. The bug is introduced silently and surfaces later.
   - ``GENERATED ALWAYS AS IDENTITY`` hands ownership to the engine.
     An explicit insert without ``OVERRIDING SYSTEM VALUE`` raises an
     immediate error, so the desynchronization can never happen accidentally.
   - After using ``OVERRIDING SYSTEM VALUE`` (e.g., during a restore), the
     sequence counter is not advanced. You must call
     ``setval('seq_name', (SELECT MAX(col) FROM table))`` to advance it past
     the highest existing ID, or the next auto-insert will collide.


.. admonition:: Question 30
   :class: hint

   Describe the shared-PK ISA strategy and explain why the subtype PK
   column must not have ``GENERATED ALWAYS AS IDENTITY``. Use the
   ``person`` and ``student`` tables as your example.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - In the shared-PK strategy, the subtype table's PK carries the same
     value as the supertype PK for the same entity. This ensures a subtype
     row cannot exist without a corresponding supertype row.
   - The identity sequence lives only on the supertype (``person.person_id``).
     The application inserts a person first, captures the generated ID, and
     uses that same ID when inserting the subtype (``student.person_id``).
   - Adding ``GENERATED ALWAYS AS IDENTITY`` to ``student.person_id`` would
     create an independent sequence starting at 1. The subtype ID would be
     generated independently of the supertype ID, breaking the shared
     identity relationship: the same entity would have different IDs in the
     two tables.
   - The ``ON DELETE CASCADE`` on the FK ensures that deleting a ``person``
     row automatically removes the ``student`` row, maintaining referential
     integrity without application-level cleanup.


.. admonition:: Question 31
   :class: hint

   Compare ``TRUNCATE``, ``DELETE`` (without ``WHERE``), and ``DROP TABLE``
   across four dimensions: what survives the operation, whether it fires
   row-level triggers, whether it is rollbackable, and what its relative
   speed is on a million-row table.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``DELETE`` removes rows one by one: the table structure, constraints,
     and indexes survive; row-level triggers fire for each deleted row; it
     is fully rollbackable; and it is slow on large tables because it
     writes a WAL entry per row.
   - ``TRUNCATE`` removes all rows by deallocating data pages: the table
     structure survives; row-level triggers do not fire; it is rollbackable
     in PostgreSQL (unlike some other databases); and it is very fast
     regardless of table size.
   - ``DROP TABLE`` removes everything: the table structure, data,
     constraints, and indexes are all gone; triggers do not fire; the
     operation is rollbackable within a transaction; and speed is fast.
   - The choice rule: ``DELETE`` when you need selective removal or trigger
     firing; ``TRUNCATE`` when you need to empty the entire table quickly
     before a reload; ``DROP`` only when the table definition itself is no
     longer needed.


.. admonition:: Question 32
   :class: hint

   Explain the four-step safe migration pattern for adding a ``NOT NULL``
   column to a large live table. Why is each step necessary, and what lock
   does each step acquire?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Step 1** (``ADD COLUMN`` nullable): acquires a brief ``ACCESS EXCLUSIVE``
     metadata lock; no rows are touched; all existing rows implicitly have
     ``NULL`` for the new column.
   - **Step 2** (backfill with ``UPDATE``): fills existing rows in batches;
     no DDL lock; runs as ordinary DML that can be chunked with ``LIMIT`` to
     avoid long-running transactions.
   - **Step 3** (``ADD CONSTRAINT ... NOT VALID``): acquires ``ACCESS EXCLUSIVE``
     briefly to add the constraint definition; existing rows are not scanned;
     new inserts and updates are checked immediately, so new data is valid
     even before the scan.
   - **Step 4** (``VALIDATE CONSTRAINT``): acquires ``SHARE UPDATE EXCLUSIVE``,
     which allows concurrent reads; scans all existing rows to verify the
     constraint; once complete, the constraint is marked valid (``convalidated = true``).
     The pattern avoids holding the stronger lock during the expensive scan.
