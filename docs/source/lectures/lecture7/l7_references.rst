References
==========


.. dropdown:: 🏛️ Lecture 7
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L7: DML, Transactions, and Python Integration**

        Covers the full DML toolkit for populating and maintaining the
        university database: ``INSERT`` (single-row, multi-row, ``RETURNING``,
        ``ON CONFLICT`` upsert), ``UPDATE`` (safe workflow, ``UPDATE ... FROM``,
        ``RETURNING``), and ``DELETE`` (cascade behavior, ``RESTRICT`` handling,
        referential action summary). Transactions are covered from first
        principles through ACID properties, explicit ``BEGIN`` / ``COMMIT`` /
        ``ROLLBACK`` / ``SAVEPOINT``, isolation levels (dirty read,
        non-repeatable read, phantom read, write skew), and the
        ``SELECT ... FOR UPDATE`` lost-update prevention pattern. The Python
        integration section introduces psycopg3, parameterized queries, SQL
        injection defense, ``conn.transaction()``, connection pooling
        (``psycopg_pool.ConnectionPool``), and the five-layer repository
        pattern required for GP2.

        **Before next class**: seed ``university_db`` using the LLM prompt
        from the seeding slide and complete the take-home exercises
        (Exercises 3 and 4). Review today's five SELECT forms -- L8 builds
        directly on them.


.. dropdown:: 📖 PostgreSQL Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 INSERT
            :link: https://www.postgresql.org/docs/current/sql-insert.html
            :class-card: sd-border-secondary

            **PostgreSQL -- INSERT Reference**

            Complete reference for all ``INSERT`` options including column
            lists, ``VALUES``, ``INSERT ... SELECT``, ``ON CONFLICT``,
            and ``RETURNING``.

            +++

            - ``RETURNING`` clause
            - ``ON CONFLICT DO NOTHING`` and ``DO UPDATE``
            - ``EXCLUDED`` pseudo-table
            - ``OVERRIDING SYSTEM VALUE``

        .. grid-item-card:: 📘 UPDATE
            :link: https://www.postgresql.org/docs/current/sql-update.html
            :class-card: sd-border-secondary

            **PostgreSQL -- UPDATE Reference**

            Full syntax for ``UPDATE`` including ``SET``, ``WHERE``,
            ``FROM`` (PostgreSQL extension for join-based updates), and
            ``RETURNING``.

            +++

            - ``UPDATE ... FROM`` join syntax
            - ``RETURNING`` on UPDATE
            - Computed updates (``SET col = col + 1``)

        .. grid-item-card:: 📘 DELETE
            :link: https://www.postgresql.org/docs/current/sql-delete.html
            :class-card: sd-border-secondary

            **PostgreSQL -- DELETE Reference**

            Reference for ``DELETE`` including ``WHERE``, ``RETURNING``,
            and interaction with FK referential actions and triggers.

            +++

            - ``RETURNING`` on DELETE
            - Interaction with ``ON DELETE CASCADE``
            - ``USING`` clause for join-based deletes

        .. grid-item-card:: 📘 Transaction Isolation
            :link: https://www.postgresql.org/docs/current/transaction-iso.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Transaction Isolation**

            Narrative documentation for all four isolation levels, the
            anomalies each level prevents, and PostgreSQL-specific
            implementation notes (MVCC, ``REPEATABLE READ`` phantom
            prevention, ``SERIALIZABLE`` SSI).

            +++

            - Dirty read, non-repeatable read, phantom read
            - Write skew and ``SERIALIZABLE``
            - PostgreSQL MVCC mechanics

        .. grid-item-card:: 📘 BEGIN
            :link: https://www.postgresql.org/docs/current/sql-begin.html
            :class-card: sd-border-secondary

            **PostgreSQL -- BEGIN Reference**

            Reference for ``BEGIN`` including isolation level options and
            the relationship to autocommit mode.

            +++

            - ``BEGIN ISOLATION LEVEL``
            - Autocommit vs. explicit transactions

        .. grid-item-card:: 📘 SAVEPOINT
            :link: https://www.postgresql.org/docs/current/sql-savepoint.html
            :class-card: sd-border-secondary

            **PostgreSQL -- SAVEPOINT Reference**

            Reference for ``SAVEPOINT``, ``ROLLBACK TO SAVEPOINT``, and
            ``RELEASE SAVEPOINT``, with examples of partial transaction
            rollback.

            +++

            - Setting and rolling back to savepoints
            - Releasing savepoints
            - Nested savepoint behavior

        .. grid-item-card:: 📘 SELECT (FOR UPDATE)
            :link: https://www.postgresql.org/docs/current/sql-select.html#SQL-FOR-UPDATE-SHARE
            :class-card: sd-border-secondary

            **PostgreSQL -- SELECT FOR UPDATE / FOR SHARE**

            Documentation for row-level locking in ``SELECT`` statements.
            Essential for preventing lost updates in concurrent enrollment
            scenarios.

            +++

            - ``FOR UPDATE`` row locking
            - ``NOWAIT`` and ``SKIP LOCKED`` variants
            - Interaction with ``REPEATABLE READ``

        .. grid-item-card:: 📘 SET CONSTRAINTS
            :link: https://www.postgresql.org/docs/current/sql-set-constraints.html
            :class-card: sd-border-secondary

            **PostgreSQL -- SET CONSTRAINTS**

            Reference for per-transaction deferral of deferrable
            constraints using ``SET CONSTRAINTS name DEFERRED``.

            +++

            - Per-transaction opt-in for ``DEFERRABLE INITIALLY IMMEDIATE``
            - Interaction with ``COMMIT``


.. dropdown:: 🐍 psycopg3 Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🐍 psycopg3 Basic Usage
            :link: https://www.psycopg.org/psycopg3/docs/basic/usage.html
            :class-card: sd-border-secondary

            **psycopg3 -- Basic Usage**

            Getting started: connecting, executing queries, fetching
            results, and transactions with context managers.

            +++

            - ``psycopg.connect()`` and context managers
            - ``cur.execute()`` and fetch methods
            - ``conn.transaction()``

        .. grid-item-card:: 🐍 Passing Parameters
            :link: https://www.psycopg.org/psycopg3/docs/basic/params.html
            :class-card: sd-border-secondary

            **psycopg3 -- Passing Parameters to SQL Queries**

            The authoritative reference for parameterized queries in
            psycopg3: ``%s`` placeholders, named parameters, and why
            f-strings are dangerous.

            +++

            - ``%s`` positional parameters
            - ``%(name)s`` named parameters
            - ``cur.query`` for debugging
            - SQL injection explained

        .. grid-item-card:: 🐍 Row Factories
            :link: https://www.psycopg.org/psycopg3/docs/advanced/rows.html
            :class-card: sd-border-secondary

            **psycopg3 -- Row Factories**

            Documentation for ``dict_row``, ``namedtuple_row``, and
            custom row factories. Essential for the GP2 repository pattern.

            +++

            - ``row_factory=dict_row`` usage
            - ``namedtuple_row`` alternative
            - Custom row factory implementation

        .. grid-item-card:: 🐍 Connection Pool
            :link: https://www.psycopg.org/psycopg3/docs/advanced/pool.html
            :class-card: sd-border-secondary

            **psycopg3 -- Connection Pool**

            Documentation for ``psycopg_pool.ConnectionPool``: configuration,
            ``min_size`` / ``max_size``, ``pool.connection()`` context
            manager, and shutdown.

            +++

            - Pool configuration parameters
            - ``pool.connection()`` context manager
            - Async pool variant
            - Pool statistics and monitoring

        .. grid-item-card:: 🐍 Transactions
            :link: https://www.psycopg.org/psycopg3/docs/basic/transactions.html
            :class-card: sd-border-secondary

            **psycopg3 -- Transaction Management**

            How psycopg3 handles autocommit, explicit transactions, and
            the ``conn.transaction()`` context manager.

            +++

            - Autocommit vs. transaction mode
            - ``conn.transaction()`` mechanics
            - Nested transactions and savepoints

        .. grid-item-card:: 🐍 Errors Reference
            :link: https://www.psycopg.org/psycopg3/docs/api/errors.html
            :class-card: sd-border-secondary

            **psycopg3 -- Errors Module**

            Complete list of ``psycopg.errors`` exceptions mapped to
            PostgreSQL error codes. Use for catching specific constraint
            violations in the service layer.

            +++

            - ``UniqueViolation``
            - ``ForeignKeyViolation``
            - ``CheckViolation``
            - ``OperationalError``


.. dropdown:: 📚 Textbooks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 Silberschatz, Korth and Sudarshan Ch. 3
            :class-card: sd-border-secondary

            **Silberschatz et al. -- "Database System Concepts" (7th Ed.)**

            Chapter 3 covers SQL DML: ``INSERT``, ``UPDATE``, ``DELETE``,
            and ``SELECT`` fundamentals used as verification throughout L7.

            +++

            - Chapter 3: Introduction to SQL
            - INSERT, UPDATE, DELETE syntax and semantics
            - NULL handling in DML

        .. grid-item-card:: 📗 Silberschatz Ch. 17 -- Transactions
            :class-card: sd-border-secondary

            **Silberschatz et al. -- "Database System Concepts" (7th Ed.)**

            Chapter 17 covers transaction concepts, ACID properties, and
            serialization theory at a deeper level than the lecture.

            +++

            - ACID properties formal definitions
            - Serializability
            - Isolation levels and their trade-offs

        .. grid-item-card:: 📘 Elmasri and Navathe Ch. 20
            :class-card: sd-border-secondary

            **Elmasri, Navathe -- "Fundamentals of Database Systems" (7th Ed.)**

            Chapter 20 covers transaction processing concepts including
            concurrency control and the ACID properties.

            +++

            - Transaction states
            - Concurrency control techniques
            - Isolation and serialization


.. dropdown:: 🛠️ Online Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🔍 python-dotenv Documentation
            :link: https://saurabh-kumar.com/python-dotenv/
            :class-card: sd-border-secondary

            **python-dotenv**

            Documentation for loading ``.env`` files into ``os.environ``
            with ``load_dotenv()``. Essential for credential management in
            all GP2 Python code.

            +++

            - ``load_dotenv()`` usage
            - ``os.getenv()`` with defaults
            - Multiple environment files

        .. grid-item-card:: 🌐 OWASP SQL Injection
            :link: https://owasp.org/www-community/attacks/SQL_Injection
            :class-card: sd-border-secondary

            **OWASP -- SQL Injection**

            The authoritative reference for SQL injection attacks,
            prevention techniques, and real-world examples. Required
            background for understanding why parameterized queries are
            mandatory.

            +++

            - Attack vectors and examples
            - Defense techniques
            - Common misconceptions

        .. grid-item-card:: 🌐 Postgres MVCC Explained
            :link: https://www.postgresql.org/docs/current/mvcc-intro.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Introduction to MVCC**

            Explains how PostgreSQL's Multi-Version Concurrency Control
            works: row versioning, visibility rules, and the interaction
            with isolation levels.

            +++

            - How MVCC enables non-blocking reads
            - Snapshot timing (``READ COMMITTED`` vs ``REPEATABLE READ``)
            - Dead tuple accumulation and autovacuum

        .. grid-item-card:: 🌐 DataGrip Documentation
            :link: https://www.jetbrains.com/help/datagrip/
            :class-card: sd-border-secondary

            **JetBrains DataGrip Help**

            Official DataGrip documentation. For L7, pay particular
            attention to how to open multiple query consoles (needed for
            the two-session concurrency exercises).

            +++

            - Opening multiple consoles for concurrency demos
            - ``Ctrl+Enter`` vs. ``Ctrl+Shift+Enter``
            - Transaction indicator in the status bar


.. dropdown:: 🔗 Related Topics
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🧱 DDL and Schema (L6)
            :class-card: sd-border-secondary

            **From Logical to Physical**

            Covered in Lecture 6. The ``university_db`` schema that L7
            populates was built here: ``CREATE TABLE``, constraints,
            ``GENERATED ALWAYS AS IDENTITY``, ISA patterns, and
            deferrable foreign keys.

        .. grid-item-card:: 🔍 DQL: Joins and Aggregates (L8)
            :class-card: sd-border-secondary

            **SELECT, Joins, Subqueries, and Aggregates**

            Covered in the next lecture. The five SELECT forms introduced
            in L7 are the foundation for L8's full coverage: all join
            types, ``GROUP BY``, ``HAVING``, subqueries, and window
            functions. ``university_db`` must be seeded before L8.

        .. grid-item-card:: 🐍 SQLAlchemy ORM (L11)
            :class-card: sd-border-secondary

            **Production Operations and SQLAlchemy**

            Covered in Lecture 11. SQLAlchemy provides a higher-level ORM
            layer above raw psycopg3, adding session management, model
            classes, and migration support via Alembic.

        .. grid-item-card:: 🗂️ GP2 Project
            :class-card: sd-border-secondary

            **PostgreSQL + Python Integration**

            The GP2 group project requires the five-layer repository
            pattern from L7: a ``DatabaseConfig`` pool, model dataclasses,
            repository classes with parameterized queries, service classes
            with ``conn.transaction()``, and a CLI menu. Exercises 3 and 4
            from L7 are direct GP2 preparation.
