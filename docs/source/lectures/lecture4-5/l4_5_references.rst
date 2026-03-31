References
==========


.. dropdown:: 🏛️ Lecture 4-5
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L4-L5: Normalization & Denormalization**

        Covers functional dependencies, Armstrong's axioms, attribute
        closures, canonical covers, normal forms (1NF, 2NF, 3NF, BCNF),
        decomposition algorithms (3NF synthesis, BCNF decomposition),
        lossless join and dependency preservation, denormalization
        techniques (materialized views, redundant columns, summary
        tables), and OLTP vs. OLAP schema design.

        **Before next class**: Complete the normalization exercises from
        today. Optional reading: Elmasri & Navathe Ch. 6-8 or
        Silberschatz Ch. 3-6.


.. dropdown:: 📚 Foundational Papers and Textbooks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📄 Codd (1970) -- The Relational Model
            :link: https://dl.acm.org/doi/10.1145/362384.362685
            :class-card: sd-border-secondary

            **E.F. Codd -- "A Relational Model of Data for Large Shared Data Banks"**

            The foundational 1970 paper introducing the relational model
            and the first concepts of normalization. Published in
            *Communications of the ACM*.

            +++

            - Defines relations, tuples, domains
            - Introduces normalization concepts
            - Foundation for all relational databases

        .. grid-item-card:: 📄 Codd (1971) -- Further Normalization
            :link: https://dl.acm.org/doi/10.5555/1734714.1734720
            :class-card: sd-border-secondary

            **E.F. Codd -- "Further Normalization of the Data Base Relational Model"**

            Defines Second and Third Normal Forms and introduces the
            concept of transitive dependencies. Published in *Data Base
            Systems* (Courant Computer Science Symposia, 1971).

            +++

            - Defines 2NF and 3NF
            - Introduces transitive dependencies
            - Formalizes decomposition goals

        .. grid-item-card:: 📄 Armstrong (1974) -- Dependency Structures
            :class-card: sd-border-secondary

            **William W. Armstrong -- "Dependency Structures of Data Base Relationships"**

            Introduces the axiom system (reflexivity, augmentation,
            transitivity) for reasoning about functional dependencies.
            Proven sound and complete.

            +++

            - Armstrong's axioms
            - Sound and complete inference
            - Foundation for normalization algorithms

        .. grid-item-card:: 📄 Codd (1974) -- BCNF
            :class-card: sd-border-secondary

            **E.F. Codd -- "Recent Investigations into Relational Data Base Systems"**

            Introduces Boyce-Codd Normal Form (BCNF), refining
            3NF to eliminate the prime-attribute exception.

            +++

            - Defines BCNF
            - Stricter than 3NF
            - Eliminates all FD-based anomalies

        .. grid-item-card:: 📘 Elmasri and Navathe Ch. 10-11
            :class-card: sd-border-secondary

            **Elmasri, Navathe -- "Fundamentals of Database Systems" (7th Ed.)**

            Chapters 10-11 cover functional dependencies, normal forms
            (1NF through BCNF), and decomposition algorithms. Chapters
            6-8 (optional pre-reading for L6) cover relational algebra
            and SQL.

            +++

            - Chapter 10: Functional dependencies and normalization
            - Chapter 11: Relational database design algorithms
            - Chapters 6-8: Relational algebra and SQL (optional, before L6)

        .. grid-item-card:: 📗 Silberschatz, Korth and Sudarshan Ch. 7-8
            :class-card: sd-border-secondary

            **Silberschatz et al. -- "Database System Concepts" (7th Ed.)**

            Alternative textbook with strong coverage of normalization
            theory, decomposition algorithms, and BCNF vs. 3NF
            trade-offs. Chapters 3-6 (optional pre-reading for L6)
            cover relational algebra, SQL, and advanced SQL.

            +++

            - Chapter 7: Relational database design
            - Chapter 8: Application design and development
            - Chapters 3-6: Relational model and SQL (optional, before L6)


.. dropdown:: 🛠️ Online Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📖 Use The Index, Luke
            :link: https://use-the-index-luke.com
            :class-card: sd-border-secondary

            **Use The Index, Luke -- SQL Indexing and Tuning**

            Free online book covering SQL performance, indexing
            strategies, and query optimization. Relevant to understanding
            when denormalization is (or is not) needed.

            +++

            - Query performance analysis
            - Indexing strategies
            - Alternatives to denormalization

        .. grid-item-card:: 🎓 Stanford CS145
            :link: https://web.stanford.edu/class/cs145/
            :class-card: sd-border-secondary

            **Stanford CS145 -- Database Systems**

            Lecture notes on functional dependencies, normalization,
            and decomposition algorithms.

        .. grid-item-card:: 📘 PostgreSQL Documentation
            :link: https://www.postgresql.org/docs/current/sql-createtable.html
            :class-card: sd-border-secondary

            **PostgreSQL -- CREATE TABLE & Constraints**

            Official PostgreSQL documentation on table constraints
            including PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, and
            CHECK. Relevant to implementing normalized schemas.

        .. grid-item-card:: 🌐 Normalization Tutorial
            :link: https://www.geeksforgeeks.org/normal-forms-in-dbms/
            :class-card: sd-border-secondary

            **GeeksforGeeks -- Normal Forms in DBMS**

            Step-by-step tutorial covering 1NF through BCNF with
            examples and decomposition walkthroughs.


.. dropdown:: 📹 Video Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📺 Stanford CS145 Lectures
            :link: https://www.youtube.com/playlist?list=PL6hGtHedy2Z4EkgY76QOcueU8lAC4o6c3
            :class-card: sd-border-secondary

            **Stanford CS145 -- Introduction to Databases**

            Lecture videos covering functional dependencies,
            normalization, and decomposition algorithms.

        .. grid-item-card:: 🎬 freeCodeCamp Database Course
            :link: https://www.youtube.com/watch?v=HXV3zeQKqGY
            :class-card: sd-border-secondary

            **freeCodeCamp -- Database Design Course**

            4-hour video course covering database design including
            normalization theory and practical decomposition.

        .. grid-item-card:: 🎥 Caleb Curry -- Normalization
            :link: https://www.youtube.com/watch?v=GFQaEYEc8_8
            :class-card: sd-border-secondary

            **Caleb Curry -- Database Normalization**

            Clear walkthrough of normal forms with practical
            database examples and step-by-step decomposition.


.. dropdown:: 🔗 Related Topics
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📐 Logical Data Modeling (L3)
            :class-card: sd-border-secondary

            **ER-to-Relational Mapping**

            Covered in the previous lecture. The 7-step mapping
            algorithm, Crow's Foot notation, and the relational
            schemas that normalization operates on.

        .. grid-item-card:: 🧱 Relational Algebra & SQL (L6)
            :class-card: sd-border-secondary

            **SQL and Query Optimization**

            Covered in the next lecture. Relational algebra operators
            (selection, projection, join, set operations), SQL syntax
            (SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY), all join
            types (INNER, LEFT, RIGHT, FULL, CROSS), and execution plans.
            Understanding normalized schemas is a prerequisite for writing
            correct and efficient SQL.

        .. grid-item-card:: 📊 OLAP & Data Warehousing
            :class-card: sd-border-secondary

            **Star and Snowflake Schemas**

            Denormalized schema patterns used in analytical workloads.
            Star schemas use a central fact table surrounded by
            dimension tables. Covered in more depth in later lectures.

        .. grid-item-card:: ⚡ Query Optimization & Indexing
            :class-card: sd-border-secondary

            **Performance Tuning**

            Indexing strategies, EXPLAIN ANALYZE, and query rewriting
            as alternatives to denormalization. Covered in Week 12.