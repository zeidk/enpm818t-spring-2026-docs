====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 7: DML, Transactions, and
Python Integration. Topics include ``INSERT`` (single-row, multi-row,
``RETURNING``, ``ON CONFLICT``), ``UPDATE`` and ``DELETE`` (safe workflow,
referential actions), ACID properties, transaction control (``BEGIN``,
``COMMIT``, ``ROLLBACK``, ``SAVEPOINT``), isolation levels and anomalies,
and psycopg3 (parameterized queries, ``conn.transaction()``, connection
pooling, the repository pattern).

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

   Which clause must be appended to an ``INSERT`` statement to retrieve the
   generated primary key value in the same round trip?

   A. ``OUTPUT``

   B. ``RETURNING``

   C. ``SELECT LAST_INSERT_ID()``

   D. ``FETCH GENERATED``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``RETURNING``

   ``RETURNING`` causes PostgreSQL to emit the specified columns from the
   rows just written as a result set. It is the correct and safe way to
   capture a generated identity value without a separate ``SELECT MAX()``
   call, which would be vulnerable to race conditions under concurrent
   inserts.


.. admonition:: Question 2
   :class: hint

   What is the primary risk of omitting the column list from an
   ``INSERT INTO t VALUES (...)`` statement?

   A. PostgreSQL raises a syntax error if the column list is absent.

   B. The statement inserts a duplicate row.

   C. If columns are later added or reordered with ``ALTER TABLE``, values
      may be assigned to the wrong columns silently.

   D. The identity column receives an incorrect value.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- If columns are later added or reordered with ``ALTER TABLE``,
   values may be assigned to the wrong columns silently.

   Omitting the column list couples the statement to the physical column
   order at the time of writing. A future schema change (new column, renamed
   column) can silently mismap values without raising an error. Always
   include the column list.


.. admonition:: Question 3
   :class: hint

   What does ``ON CONFLICT DO NOTHING`` do when the incoming row violates
   a ``UNIQUE`` constraint?

   A. It raises an error and rolls back the statement.

   B. It silently skips the offending row; the existing row is left untouched.

   C. It deletes the existing row and inserts the new one.

   D. It merges the new row's values into the existing row.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It silently skips the offending row; the existing row is left
   untouched.

   ``DO NOTHING`` suppresses the constraint violation error and leaves the
   existing row completely unchanged. It is the correct choice for
   idempotent seed scripts and data loaders where duplicates are expected
   and should be ignored rather than cause failures.


.. admonition:: Question 4
   :class: hint

   In ``ON CONFLICT (course_id) DO UPDATE SET title = EXCLUDED.title``,
   what does ``EXCLUDED`` refer to?

   A. The existing row already in the table.

   B. The incoming row that was blocked by the conflict.

   C. A temporary table created by PostgreSQL for the upsert operation.

   D. The constraint that triggered the conflict.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The incoming row that was blocked by the conflict.

   When a conflict fires, PostgreSQL holds two versions of the row: the
   existing row in the table and the incoming row that was blocked.
   ``EXCLUDED`` is the alias PostgreSQL assigns to that incoming row, making
   its values available inside the ``SET`` clause. Without ``EXCLUDED``
   there would be no way to reference the values you tried to insert.


.. admonition:: Question 5
   :class: hint

   What happens if you run ``UPDATE student SET gpa = 4.0`` with no
   ``WHERE`` clause?

   A. PostgreSQL raises an error because ``UPDATE`` requires a ``WHERE`` clause.

   B. Only the most recently inserted row is updated.

   C. Every row in the ``student`` table has its ``gpa`` set to 4.0.

   D. The statement is silently ignored.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Every row in the ``student`` table has its ``gpa`` set to 4.0.

   PostgreSQL updates every row that matches the (absent) filter, which is
   all rows. No error is raised. This is the most dangerous mistake in DML.
   Always run a ``SELECT`` with the intended ``WHERE`` first to confirm the
   target set before executing the ``UPDATE``.


.. admonition:: Question 6
   :class: hint

   What does ``RETURNING`` return when used with ``DELETE``?

   A. The rows as they will look after a planned re-insert.

   B. The row values as they existed **before** deletion.

   C. The number of rows deleted.

   D. The primary keys of the deleted rows only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The row values as they existed **before** deletion.

   ``RETURNING`` on ``DELETE`` captures the deleted rows' data before they
   are removed. This is useful for building audit logs or capturing cascaded
   deletes that would otherwise be invisible. Contrast with ``RETURNING`` on
   ``UPDATE``, which returns the **new** values after the update.


.. admonition:: Question 7
   :class: hint

   Which ACID property guarantees that a ``COMMIT``-confirmed transaction
   survives an immediate server power failure?

   A. Atomicity

   B. Consistency

   C. Isolation

   D. Durability

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- Durability

   Durability means that committed data survives crashes. PostgreSQL
   implements this by flushing the Write-Ahead Log (WAL) to disk before
   ``COMMIT`` returns. On recovery after a crash, PostgreSQL replays the
   WAL to restore all committed transactions.


.. admonition:: Question 8
   :class: hint

   Which ACID property is violated when two sessions both read
   ``capacity = 1``, both decide to enroll, and the final capacity becomes
   ``-1``?

   A. Atomicity

   B. Consistency

   C. Isolation

   D. Durability

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Isolation

   Isolation ensures that in-progress transactions cannot see each other's
   uncommitted work. When both sessions read the same stale value and act on
   it concurrently, the lack of isolation allows their effects to combine in
   a way that violates the capacity constraint. ``SELECT ... FOR UPDATE``
   restores isolation by serializing access to the row.


.. admonition:: Question 9
   :class: hint

   What is the effect of ``ROLLBACK`` on a transaction that includes one
   successful ``UPDATE`` followed by a failing ``INSERT``?

   A. Only the failing ``INSERT`` is rolled back; the ``UPDATE`` is kept.

   B. Both the ``UPDATE`` and the ``INSERT`` attempt are rolled back.

   C. The ``UPDATE`` is committed automatically before the ``INSERT`` fails.

   D. PostgreSQL raises an error because partial rollback is not supported.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Both the ``UPDATE`` and the ``INSERT`` attempt are rolled back.

   ``ROLLBACK`` discards all work since ``BEGIN``, not just the failing
   statement. This is the atomicity guarantee: the transaction is
   all-or-nothing. To undo only part of a transaction, you must use
   ``SAVEPOINT`` / ``ROLLBACK TO SAVEPOINT``.


.. admonition:: Question 10
   :class: hint

   After ``ROLLBACK TO SAVEPOINT sp1``, which of the following is true?

   A. The entire transaction is aborted and all work is lost.

   B. Work done before ``SAVEPOINT sp1`` is preserved; work done after is
      discarded; the transaction remains open.

   C. Work done after ``SAVEPOINT sp1`` is committed; work before is
      discarded.

   D. The savepoint is automatically released and cannot be used again.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Work done before ``SAVEPOINT sp1`` is preserved; work done after
   is discarded; the transaction remains open.

   ``ROLLBACK TO SAVEPOINT`` undoes only the work that occurred after the
   marker was set, leaving everything before it intact. The transaction
   stays open so you can continue inserting or correcting the failed
   operation. This is the correct tool for batch operations where one row
   may fail without aborting the entire batch.


.. admonition:: Question 11
   :class: hint

   A non-repeatable read occurs when:

   A. A transaction reads data written by another transaction that has not
      yet committed.

   B. A transaction reads the same row twice and gets different values
      because another committed transaction changed it in between.

   C. A transaction's aggregate query returns a different row count because
      another transaction inserted matching rows in between.

   D. Two transactions write to different rows but violate a cross-row
      constraint.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A transaction reads the same row twice and gets different values
   because another committed transaction changed it in between.

   Under ``READ COMMITTED``, each ``SELECT`` takes a fresh snapshot of all
   committed data at the moment that statement executes. A second read of
   the same row therefore can return a different value if another session
   committed a change in between. ``REPEATABLE READ`` prevents this by
   freezing the snapshot at ``BEGIN`` for the entire transaction.


.. admonition:: Question 12
   :class: hint

   Which isolation level does PostgreSQL use by default?

   A. ``READ UNCOMMITTED``

   B. ``READ COMMITTED``

   C. ``REPEATABLE READ``

   D. ``SERIALIZABLE``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``READ COMMITTED``

   ``READ COMMITTED`` is the PostgreSQL default. Each statement sees a
   fresh snapshot of all committed data. It prevents dirty reads but allows
   non-repeatable reads and phantom reads. PostgreSQL does not implement
   ``READ UNCOMMITTED``; a request for that level is silently upgraded to
   ``READ COMMITTED``.


.. admonition:: Question 13
   :class: hint

   What is the difference between ``RESTRICT`` and ``NO ACTION`` as
   referential actions on a foreign key?

   A. ``RESTRICT`` removes child rows; ``NO ACTION`` sets them to ``NULL``.

   B. Both block the parent delete, but ``RESTRICT`` checks immediately
      (before other constraints in the statement), while ``NO ACTION``
      checks at the end of the statement and is compatible with
      ``DEFERRABLE``.

   C. ``NO ACTION`` is the same as ``CASCADE``; ``RESTRICT`` is the
      default.

   D. ``RESTRICT`` is not a valid PostgreSQL referential action.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Both block the parent delete, but ``RESTRICT`` checks
   immediately (before other constraints in the statement), while
   ``NO ACTION`` checks at the end of the statement and is compatible
   with ``DEFERRABLE``.

   The difference matters in transactions where the referencing child rows
   are deleted in the same statement as the parent: ``NO ACTION`` defers
   long enough for those deletes to take effect; ``RESTRICT`` fires before
   they can. For most use cases ``NO ACTION`` (the default) is the
   correct choice.


.. admonition:: Question 14
   :class: hint

   Why is using an f-string to build a SQL query with user input dangerous?

   A. f-strings produce Python bytes objects rather than strings, which
      psycopg3 cannot send.

   B. User input can include SQL syntax that changes the query's logic,
      potentially returning all rows or executing destructive commands.

   C. f-strings are slower than ``%s`` parameterization by a factor of 10.

   D. psycopg3 does not support f-strings in ``cur.execute()`` calls.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- User input can include SQL syntax that changes the query's
   logic, potentially returning all rows or executing destructive commands.

   SQL injection allows an attacker to inject SQL syntax (e.g.,
   ``' OR '1'='1``) into a query string, bypassing intended filters or
   accessing all rows. Parameterized queries (``cur.execute(sql, (val,))``)
   send SQL text and values separately so the driver always escapes values
   and the database never interprets them as SQL.


.. admonition:: Question 15
   :class: hint

   What does ``conn.transaction()`` do in psycopg3?

   A. It opens a connection to the database.

   B. It issues ``BEGIN`` on entry and ``COMMIT`` on clean exit; any
      exception triggers an automatic ``ROLLBACK``.

   C. It creates a savepoint at the current position in the transaction.

   D. It sets the isolation level to ``SERIALIZABLE``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It issues ``BEGIN`` on entry and ``COMMIT`` on clean exit; any
   exception triggers an automatic ``ROLLBACK``.

   ``conn.transaction()`` is a context manager that maps exactly to a
   ``BEGIN`` / ``COMMIT`` block. If any statement inside the ``with`` block
   raises an exception, psycopg3 automatically issues ``ROLLBACK`` before
   the exception propagates. This means you never need to write manual
   ``conn.rollback()`` calls in production service code.


.. admonition:: Question 16
   :class: hint

   A developer inserts a row in psycopg3 without using ``conn.transaction()``
   or calling ``conn.commit()``, then checks the row in ``psql`` and finds
   it missing. What is the most likely cause?

   A. The row was inserted into the wrong database.

   B. psycopg3 does not commit automatically; the insert is in an open
      implicit transaction that has not been committed.

   C. psql caches query results; the row will appear after the cache is
      cleared.

   D. The ``INSERT`` statement contained a syntax error that was silently
      ignored.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- psycopg3 does not commit automatically; the insert is in an
   open implicit transaction that has not been committed.

   Unlike ``psql`` (which runs in autocommit mode by default), psycopg3
   wraps all statements in an implicit transaction block. Nothing is visible
   to other sessions until you call ``conn.commit()`` or use
   ``conn.transaction()``. This is the single most common source of
   *"my INSERT worked but I can't see it"* bugs.


.. admonition:: Question 17
   :class: hint

   What is the primary reason to use a connection pool instead of calling
   ``psycopg.connect()`` on every query?

   A. ``psycopg.connect()`` is deprecated and will be removed in a future
      version.

   B. Opening a new PostgreSQL connection takes roughly 50 ms and spawns a
      dedicated backend process; a pool pays this cost once and reuses
      connections across all calls.

   C. Connection pools automatically retry failed queries.

   D. psycopg3 requires a pool to use the ``dict_row`` row factory.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Opening a new PostgreSQL connection takes roughly 50 ms and
   spawns a dedicated backend process; a pool pays this cost once and
   reuses connections across all calls.

   Each ``psycopg.connect()`` call creates a new OS process on the
   PostgreSQL server. Calling it per query adds ~50 ms of latency to every
   operation and can exhaust the server's ``max_connections`` limit. A
   pool opens ``min_size`` connections at startup and lends them on demand;
   each subsequent borrow is essentially free.


.. admonition:: Question 18
   :class: hint

   In the five-layer repository pattern, which layer is responsible for
   opening ``conn.transaction()`` and enforcing business rules like
   checking capacity before enrollment?

   A. ``cli/``

   B. ``models/``

   C. ``repositories/``

   D. ``services/``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``services/``

   The service layer owns business rules and transaction boundaries. It
   calls repository methods to read and write data, wraps multi-step
   operations in ``conn.transaction()``, and translates database exceptions
   into domain errors (``ValueError``) for the CLI. The repository layer
   owns SQL strings; the CLI layer owns user I/O; neither crosses into the
   service's responsibility.


----


True/False (Questions 19-28)
============================

.. admonition:: Question 19
   :class: hint

   **True or False:** ``RETURNING`` on an ``UPDATE`` statement returns the
   column values as they were **before** the update.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``RETURNING`` on ``UPDATE`` returns the **new** values after the update
   was applied. To see the original values, you would need to capture them
   with a ``SELECT`` before the update. Contrast this with ``RETURNING`` on
   ``DELETE``, which does return the values as they were before deletion.


.. admonition:: Question 20
   :class: hint

   **True or False:** A multi-row ``INSERT`` with multiple tuples in a
   single ``VALUES`` clause is always atomic: all rows are inserted or none
   are.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A single ``INSERT`` statement is wrapped in an implicit transaction by
   PostgreSQL's autocommit mode. If any row violates a constraint, the
   entire statement is rolled back -- no partial inserts. To insert some
   rows while skipping conflicting ones, use ``ON CONFLICT DO NOTHING``.


.. admonition:: Question 21
   :class: hint

   **True or False:** ``ROLLBACK TO SAVEPOINT`` aborts the entire
   transaction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``ROLLBACK TO SAVEPOINT`` only undoes the work performed after the named
   savepoint was set. The transaction remains open, and work done before
   the savepoint is preserved. The entire transaction is only discarded by
   a bare ``ROLLBACK`` (with no savepoint name).


.. admonition:: Question 22
   :class: hint

   **True or False:** PostgreSQL prevents dirty reads at all isolation
   levels, including ``READ UNCOMMITTED``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   PostgreSQL does not implement ``READ UNCOMMITTED`` as defined by the SQL
   standard. A connection that requests ``READ UNCOMMITTED`` is silently
   upgraded to ``READ COMMITTED``, which never exposes uncommitted writes.
   Dirty reads are therefore impossible in PostgreSQL regardless of the
   isolation level set.


.. admonition:: Question 23
   :class: hint

   **True or False:** ``SELECT ... FOR UPDATE`` commits the current
   transaction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``FOR UPDATE`` acquires a row-level lock on the selected rows but does
   not commit anything. The transaction remains open; the lock is held until
   the transaction is committed or rolled back. Other sessions attempting to
   lock the same rows will block until the lock is released.


.. admonition:: Question 24
   :class: hint

   **True or False:** In psycopg3, ``cur.execute(sql, (val,))`` and
   ``cur.execute(f"... WHERE col = '{val}'"`` are functionally equivalent.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   They are fundamentally different. The parameterized form sends SQL and
   the value separately; the driver escapes the value so it can never be
   interpreted as SQL. The f-string form embeds the raw value directly into
   the SQL string, creating a SQL injection vulnerability. They differ in
   security, not just style.


.. admonition:: Question 25
   :class: hint

   **True or False:** A repository method that calls ``cur.execute()`` twice
   in a single method body violates the one-method-one-query rule.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** (with nuance)

   The one-method-one-query rule states that repository methods should run
   exactly one query and return the result. A method that runs two queries
   usually contains either business logic (which belongs in the service
   layer) or a multi-step operation (which also belongs in the service
   layer, where ``conn.transaction()`` can wrap both queries atomically).


.. admonition:: Question 26
   :class: hint

   **True or False:** ``REPEATABLE READ`` in PostgreSQL also prevents
   phantom reads, which the SQL standard only requires ``SERIALIZABLE``
   to prevent.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   PostgreSQL's implementation of ``REPEATABLE READ`` uses a full
   transaction-level snapshot (frozen at ``BEGIN``), which means new rows
   inserted by other sessions are invisible for the duration of the
   transaction. This eliminates phantom reads, which the SQL standard only
   mandates ``SERIALIZABLE`` to handle. PostgreSQL's ``REPEATABLE READ``
   is therefore stronger than the standard requires.


.. admonition:: Question 27
   :class: hint

   **True or False:** The ``.env`` file containing database credentials
   should be committed to the project's Git repository so that teammates
   can use the same credentials.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``.env`` file must be added to ``.gitignore`` **before** the first
   commit. Credentials pushed to a public (or even private) repository must
   be considered compromised immediately. The correct pattern is to commit
   an ``.env.example`` file with placeholder values and let each team member
   create their own ``.env`` with real credentials locally.


.. admonition:: Question 28
   :class: hint

   **True or False:** In psycopg3, using ``row_factory=dict_row`` returns
   rows as Python dictionaries keyed by column name.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Passing ``row_factory=dict_row`` to ``conn.cursor()`` changes the default
   tuple-based row representation to a dictionary where each key is the
   column name from the query. This makes repository code self-documenting
   (``row['person_id']`` vs. ``row[0]``) and resilient to column reordering
   in the SQL query.


----


Essay Questions (Questions 29-32)
==================================

.. admonition:: Question 29
   :class: hint

   Explain why ``SELECT MAX(person_id) FROM person`` is not a safe way to
   retrieve a generated primary key after an ``INSERT``, and describe the
   correct alternative. Include the specific failure mode.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``SELECT MAX()`` introduces a race condition: between your ``INSERT``
     and your ``SELECT``, another session may insert a row with a higher
     ``person_id``. Your ``MAX()`` then returns the other session's ID, not
     yours, causing the subsequent subtype insert (e.g., ``student``) to
     reference the wrong person.
   - Even in a single-session environment, the pattern is fragile and
     semantically wrong: ``MAX()`` is a query about the table's current
     state, not about the specific row you just wrote.
   - The correct alternative is ``INSERT ... RETURNING person_id``. The
     engine returns the generated value atomically in the same operation
     that wrote the row; no other session can interfere between the write
     and the read.
   - In Python, read the returned value with ``cur.fetchone()`` immediately
     after the execute call.


.. admonition:: Question 30
   :class: hint

   Describe the lost-update problem in the context of course enrollment
   and explain precisely why ``SELECT ... FOR UPDATE`` prevents it. Include
   what happens to Session B when Session A holds the lock.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The lost update occurs when two sessions both read ``capacity = 1``,
     both decide there is a seat available, both decrement capacity and
     insert an enrollment row, and the final capacity is ``-1``. Each
     session acted on a stale snapshot; neither was wrong individually,
     but their combined effect violates the business rule.
   - ``SELECT ... FOR UPDATE`` acquires a row-level lock on the
     ``course_section`` row when Session A reads it. Session B's
     ``SELECT ... FOR UPDATE`` on the same row blocks until Session A
     commits or rolls back.
   - When Session A commits, Session B unblocks and reads the committed
     value -- which is now ``capacity = 0`` (or whatever Session A left).
     Session B sees zero seats and correctly declines to enroll.
   - The key insight is that ``FOR UPDATE`` forces Session B to wait until
     Session A is finished rather than racing ahead with a stale value.


.. admonition:: Question 31
   :class: hint

   Compare the ACID properties Atomicity and Isolation. For each, give a
   concrete example of what goes wrong without it, and identify which
   PostgreSQL mechanism enforces it.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Atomicity** ensures that a group of statements all commit together
     or none take effect. Without it: an enrollment transaction that
     decrements capacity and inserts a row could crash between the two
     statements, leaving capacity reduced but no enrollment row -- a
     half-finished state. PostgreSQL enforces atomicity via
     ``ROLLBACK``, which discards all partial work.
   - **Isolation** ensures that a transaction's in-progress work is
     invisible to other sessions until committed. Without it: the
     lost-update problem -- two sessions both read ``capacity = 1`` and
     both enroll, pushing capacity to ``-1``. PostgreSQL enforces isolation
     via MVCC (each session sees a consistent snapshot) and row-level locks
     (``SELECT ... FOR UPDATE``) for stricter serialization.
   - The key distinction: atomicity is about a single transaction's
     all-or-nothing guarantee; isolation is about how concurrent
     transactions interact with each other.


.. admonition:: Question 32
   :class: hint

   Explain the five-layer repository pattern: name each layer, describe
   its single responsibility, and give the one rule it must not violate.
   Then explain what benefit this design provides when a database column
   is renamed.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - ``config/``: manages the connection pool; no queries or business
     logic.
   - ``models/``: pure data containers (dataclasses); no database calls or
     ``import psycopg``.
   - ``repositories/``: owns all ``cur.execute()`` calls; no business logic
     and no ``input()``. One method = one query.
   - ``services/``: owns business rules, transaction boundaries, and
     domain error translation; no direct ``execute()`` calls and no
     ``input()``.
   - ``cli/``: handles user I/O; no SQL strings and no business logic.
   - **Column rename benefit**: because all SQL strings live exclusively in
     the repository layer, renaming a column requires editing exactly one
     method in one file. The service, CLI, and models are unaffected.
     Without this separation, a column rename would require searching every
     file in the codebase for embedded SQL strings.
