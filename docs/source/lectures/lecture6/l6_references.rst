References
==========


.. dropdown:: 🏛️ Lecture 6
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L6: From Logical to Physical: Implementing Your Database in PostgreSQL**

        Covers the full translation pipeline from a logical schema to a
        running PostgreSQL database: data type selection, the complete
        constraint toolkit (PRIMARY KEY, FOREIGN KEY, NOT NULL, UNIQUE,
        CHECK, EXCLUDE), identity columns (SERIAL vs. GENERATED ALWAYS AS
        IDENTITY), ISA and category patterns, deferrable constraints,
        ALTER TABLE and safe schema evolution, and the DELETE / TRUNCATE /
        DROP distinction with naming conventions and DDL best practices.

        **Before next class**: Complete the DDL exercises using your live
        ``university_db``. Optional reading: Elmasri & Navathe Ch. 3-4 or
        Silberschatz Ch. 4-5.


.. dropdown:: 📖 PostgreSQL Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 CREATE TABLE
            :link: https://www.postgresql.org/docs/current/sql-createtable.html
            :class-card: sd-border-secondary

            **PostgreSQL -- CREATE TABLE Reference**

            Complete reference for all ``CREATE TABLE`` options including
            column definitions, constraint types, ``GENERATED ALWAYS AS
            IDENTITY``, deferrable constraints, and ``EXCLUDE`` constraints.

            +++

            - PRIMARY KEY and UNIQUE syntax
            - FOREIGN KEY with ON DELETE / ON UPDATE actions
            - CHECK and EXCLUDE constraints
            - Identity column options

        .. grid-item-card:: 📘 ALTER TABLE
            :link: https://www.postgresql.org/docs/current/sql-altertable.html
            :class-card: sd-border-secondary

            **PostgreSQL -- ALTER TABLE Reference**

            Full syntax for schema evolution: adding and dropping columns
            and constraints, renaming, type changes, NOT VALID, and
            VALIDATE CONSTRAINT.

            +++

            - ADD COLUMN and DROP COLUMN
            - ADD CONSTRAINT ... NOT VALID
            - VALIDATE CONSTRAINT
            - RENAME COLUMN and RENAME CONSTRAINT

        .. grid-item-card:: 📘 Data Types
            :link: https://www.postgresql.org/docs/current/datatype.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Data Types**

            Comprehensive reference for all PostgreSQL data types including
            numeric, character, date/time, boolean, UUID, JSONB, arrays,
            range types, and more.

            +++

            - Numeric types (SMALLINT, INTEGER, BIGINT, NUMERIC, FLOAT)
            - Character types (VARCHAR, TEXT, CHAR)
            - Date/time types (DATE, TIMESTAMP, TIMESTAMPTZ)
            - Range types (used with EXCLUDE)

        .. grid-item-card:: 📘 Constraints
            :link: https://www.postgresql.org/docs/current/ddl-constraints.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Constraints**

            Narrative documentation for all constraint types: NOT NULL,
            UNIQUE, PRIMARY KEY, FOREIGN KEY, CHECK, and EXCLUDE. Includes
            the NULL and UNIQUE interaction and deferral mechanics.

            +++

            - NULL behavior with UNIQUE
            - NULLS NOT DISTINCT (PG 15+)
            - Deferrable constraints explained
            - EXCLUDE constraint examples

        .. grid-item-card:: 📘 DELETE
            :link: https://www.postgresql.org/docs/current/sql-delete.html
            :class-card: sd-border-secondary

            **PostgreSQL -- DELETE**

            Reference for the ``DELETE`` statement including ``WHERE``
            clause, RETURNING, and interaction with triggers and FK
            constraints.

            +++

            - WHERE clause filtering
            - Trigger interaction
            - RETURNING clause

        .. grid-item-card:: 📘 TRUNCATE
            :link: https://www.postgresql.org/docs/current/sql-truncate.html
            :class-card: sd-border-secondary

            **PostgreSQL -- TRUNCATE**

            Reference for ``TRUNCATE`` including RESTART IDENTITY, CASCADE,
            and its differences from DELETE.

            +++

            - RESTART IDENTITY behavior
            - CASCADE propagation
            - Trigger and transaction details

        .. grid-item-card:: 📘 DROP TABLE
            :link: https://www.postgresql.org/docs/current/sql-droptable.html
            :class-card: sd-border-secondary

            **PostgreSQL -- DROP TABLE**

            Reference for ``DROP TABLE`` including IF EXISTS and CASCADE.

            +++

            - IF EXISTS: safe drop
            - CASCADE: removes dependent objects
            - Differences from TRUNCATE

        .. grid-item-card:: 📘 Range Types
            :link: https://www.postgresql.org/docs/current/rangetypes.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Range Types and Operators**

            Documentation for range types (``TSRANGE``, ``DATERANGE``,
            ``INT4RANGE``) and the overlap operator ``&&``. Required
            background for ``EXCLUDE`` constraints on time ranges.

            +++

            - Built-in range types
            - Overlap operator &&
            - Range comparison operators

        .. grid-item-card:: 📘 GiST Indexes
            :link: https://www.postgresql.org/docs/current/gist.html
            :class-card: sd-border-secondary

            **PostgreSQL -- GiST Indexes**

            Generalized Search Tree index documentation. Required for
            ``EXCLUDE USING GIST`` constraints.

            +++

            - GiST index structure
            - Supported operator classes
            - btree_gist extension


.. dropdown:: 📚 Textbooks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📘 Elmasri and Navathe Ch. 3-4
            :class-card: sd-border-secondary

            **Elmasri, Navathe -- "Fundamentals of Database Systems" (7th Ed.)**

            Chapters 3-4 cover the relational model and SQL DDL including
            data types, constraints, and table creation.

            +++

            - Chapter 3: The Relational Model
            - Chapter 4: SQL: Data Definition and Constraints
            - CREATE TABLE, ALTER TABLE, data types

        .. grid-item-card:: 📗 Silberschatz, Korth and Sudarshan Ch. 4-5
            :class-card: sd-border-secondary

            **Silberschatz et al. -- "Database System Concepts" (7th Ed.)**

            Alternative textbook with strong coverage of SQL DDL, integrity
            constraints, and referential integrity actions.

            +++

            - Chapter 4: Intermediate SQL
            - Chapter 5: Advanced SQL
            - Constraints, assertions, and triggers


.. dropdown:: 🛠️ Online Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🔍 psql Meta-Commands
            :link: https://www.postgresql.org/docs/current/app-psql.html
            :class-card: sd-border-secondary

            **PostgreSQL -- psql Reference**

            Documentation for psql meta-commands including ``\d``, ``\d+``,
            ``\dt``, and ``\di``. Essential for inspecting table structure,
            constraints, and indexes during demos.

            +++

            - ``\d tablename``: show columns and constraints
            - ``\d+ tablename``: show FK references too
            - ``\dt``: list all tables

        .. grid-item-card:: 📖 Use The Index, Luke
            :link: https://use-the-index-luke.com
            :class-card: sd-border-secondary

            **Use The Index, Luke -- SQL Indexing and Tuning**

            Free online book covering SQL performance, indexing strategies,
            and query optimization. Useful context for understanding why
            physical type and constraint choices affect query performance.

            +++

            - Query performance analysis
            - Index types and when to use them
            - Cost-based optimizer concepts

        .. grid-item-card:: 🌐 pgpedia -- GENERATED ALWAYS
            :link: https://pgpedia.info/g/generated-always-as-identity.html
            :class-card: sd-border-secondary

            **pgpedia -- GENERATED ALWAYS AS IDENTITY**

            Concise reference entry for identity columns with examples and
            comparison to ``SERIAL``.

        .. grid-item-card:: 🌐 DataGrip Documentation
            :link: https://www.jetbrains.com/help/datagrip/
            :class-card: sd-border-secondary

            **JetBrains DataGrip Help**

            Official DataGrip documentation covering query consoles,
            database connections, schema explorer, and keyboard shortcuts
            used throughout the lecture demos.

            +++

            - Connecting to PostgreSQL
            - Running SQL statements (Ctrl+Enter, Ctrl+Shift+Enter)
            - Schema inspection tools


.. dropdown:: 🔗 Related Topics
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🧱 Logical Data Modeling (L3)
            :class-card: sd-border-secondary

            **ER-to-Relational Mapping**

            Covered in Lecture 3. The 7-step mapping algorithm, Crow's Foot
            notation, and the relational schemas that L6 translates into
            physical SQL. Understanding the logical schema is a prerequisite
            for choosing correct physical constraints.

        .. grid-item-card:: 🗂️ Normalization (L4-L5)
            :class-card: sd-border-secondary

            **Normalization and Denormalization**

            Covered in Lectures 4-5. A normalized logical schema is the
            correct input to physical modeling. Physical constraints enforce
            the business rules that normalization identified.

        .. grid-item-card:: 📊 DML and Transactions (L7)
            :class-card: sd-border-secondary

            **INSERT, UPDATE, DELETE, and Transactions**

            Covered in the next lecture. INSERT, UPDATE, and DELETE populate
            and modify the tables defined in L6. ACID properties, BEGIN /
            COMMIT / ROLLBACK, and savepoints. psycopg3 for Python-to-PostgreSQL
            connectivity.

        .. grid-item-card:: 🔍 DQL and Joins (L8)
            :class-card: sd-border-secondary

            **SELECT, Joins, and Aggregates**

            Covered in Lecture 8. Querying the ``university_db`` schema
            built in L6 with SELECT, all join types, GROUP BY, HAVING,
            and window functions.
