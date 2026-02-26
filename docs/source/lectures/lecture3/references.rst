References
==========


.. dropdown:: 🏛️ Lecture 3
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L3: Logical Data Modeling**

        Covers the relational model (relations, tuples, attributes, keys),
        Crow's Foot notation, the 7-step ER-to-Relational mapping algorithm
        (strong entities, weak entities, 1:1, 1:N, M:N relationships,
        multivalued attributes, n-ary relationships), ISA mapping strategies,
        category (union type) mapping, lookup tables, table design best
        practices, and a complete mapping of the university system.


.. dropdown:: 📚 Foundational Papers and Textbooks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📄 Codd (1970) -- The Relational Model
            :link: https://dl.acm.org/doi/10.1145/362384.362685
            :class-card: sd-border-secondary

            **E.F. Codd -- "A Relational Model of Data for Large Shared Data Banks"**

            The foundational 1970 paper introducing the relational model,
            relations as mathematical objects, and the formal basis for
            relational databases. Published in *Communications of the ACM*.

            +++

            - Defines relations, tuples, domains
            - Introduces normalization concepts
            - Foundation for all relational databases

        .. grid-item-card:: 📘 Elmasri and Navathe Ch. 5-9
            :class-card: sd-border-secondary

            **Elmasri, Navathe -- "Fundamentals of Database Systems" (7th Ed.)**

            Chapters 5-9 cover the relational model, relational algebra,
            ER-to-relational mapping, and normalization.

            +++

            - Chapter 5: The relational data model
            - Chapter 7: Relational database design using ER mapping
            - Chapter 9: Normalization

        .. grid-item-card:: 📗 Silberschatz, Korth and Sudarshan Ch. 2, 6-7
            :class-card: sd-border-secondary

            **Silberschatz et al. -- "Database System Concepts" (7th Ed.)**

            Alternative foundational textbook with strong coverage of the
            relational model, schema design, and normalization.

            +++

            - Chapter 2: Relational model
            - Chapter 6: ER-to-relational design
            - Chapter 7: Normalization

        .. grid-item-card:: 📄 Teorey et al. (1986)
            :link: https://dl.acm.org/doi/10.1145/5397.5399
            :class-card: sd-border-secondary

            **Teorey et al. -- "A Logical Design Methodology for ER Databases"**

            Classic paper on ER-to-relational mapping, including handling of
            specialization hierarchies and weak entities.


.. dropdown:: 🛠️ Logical Modeling Tools
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🖊️ DbSchema
            :link: https://dbschema.com
            :class-card: sd-border-secondary

            **DbSchema -- Visual Database Designer**

            Visual database design tool with native Crow's Foot notation,
            schema comparison, and DDL generation for multiple DBMSs.

            +++

            - Crow's Foot diagrams
            - Forward/reverse engineering
            - Multi-DBMS support

        .. grid-item-card:: 📐 DBeaver
            :link: https://dbeaver.io
            :class-card: sd-border-secondary

            **DBeaver -- Universal Database Tool**

            Free database tool with ER diagram generation from existing
            schemas. Supports PostgreSQL, MySQL, and many others.

            +++

            - Auto-generates Crow's Foot diagrams
            - Free Community Edition
            - Multi-DBMS support

        .. grid-item-card:: 💼 pgAdmin
            :link: https://www.pgadmin.org
            :class-card: sd-border-secondary

            **pgAdmin -- PostgreSQL Administration**

            The standard management tool for PostgreSQL with ERD support
            and DDL generation.

            +++

            - Native PostgreSQL support
            - ERD viewer
            - Free and open source

        .. grid-item-card:: 🖋️ PlantUML
            :link: https://plantuml.com/er-diagram
            :class-card: sd-border-secondary

            **PlantUML -- Text-Based Diagrams**

            Text-based diagramming tool that supports Crow's Foot ER
            diagrams. Integrates with VS Code, IntelliJ, and CI pipelines.

            +++

            - Text-based (version-controllable)
            - Crow's Foot entity diagrams
            - Integrates with documentation tools


.. dropdown:: 📖 Relational Model Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🎓 Stanford CS145
            :link: https://web.stanford.edu/class/cs145/
            :class-card: sd-border-secondary

            **Stanford CS145 -- Database Systems**

            Lecture notes and materials on the relational model and
            ER-to-relational mapping from Stanford's database course.

        .. grid-item-card:: 📘 PostgreSQL Documentation
            :link: https://www.postgresql.org/docs/current/ddl-constraints.html
            :class-card: sd-border-secondary

            **PostgreSQL -- DDL Constraints**

            Official PostgreSQL documentation on table constraints including
            PRIMARY KEY, FOREIGN KEY, UNIQUE, NOT NULL, and CHECK.

        .. grid-item-card:: 🌐 Vertabelo Blog
            :link: https://www.vertabelo.com/blog/crow-s-foot-notation/
            :class-card: sd-border-secondary

            **Vertabelo -- Crow's Foot Notation Guide**

            Comprehensive guide to reading and drawing Crow's Foot diagrams,
            including cardinality and participation symbols.

        .. grid-item-card:: 📚 GeeksforGeeks Mapping
            :link: https://www.geeksforgeeks.org/mapping-from-er-model-to-relational-model/
            :class-card: sd-border-secondary

            **GeeksforGeeks -- ER to Relational Mapping**

            Step-by-step tutorial covering the mapping algorithm with
            examples for each step.


.. dropdown:: 📹 Video Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🎥 Lucidchart Crow's Foot Tutorial
            :link: https://www.youtube.com/watch?v=QpdhBUYk7Kk
            :class-card: sd-border-secondary

            **Lucidchart -- ER Diagrams Tutorial**

            Video introduction to ER diagrams including Crow's Foot notation,
            cardinality symbols, and practical examples.

        .. grid-item-card:: 🎬 freeCodeCamp Database Course
            :link: https://www.youtube.com/watch?v=HXV3zeQKqGY
            :class-card: sd-border-secondary

            **freeCodeCamp -- Database Design Course**

            4-hour video course covering database design from conceptual
            modeling through implementation, including ER-to-relational mapping.

        .. grid-item-card:: 📺 Stanford CS145 Lectures
            :link: https://www.youtube.com/playlist?list=PL6hGtHedy2Z4EkgY76QOcueU8lAC4o6c3
            :class-card: sd-border-secondary

            **Stanford CS145 -- Introduction to Databases**

            Lecture videos covering the relational model, relational design,
            and normalization.

        .. grid-item-card:: 🎞️ Caleb Curry -- ER Mapping
            :link: https://www.youtube.com/watch?v=-CuY5ADwn24
            :class-card: sd-border-secondary

            **Caleb Curry -- ER to Relational Mapping**

            Clear walkthrough of the ER-to-relational mapping algorithm with
            practical database examples.


.. dropdown:: 🔗 Related Topics
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🧱 Normalization (L4)
            :link: https://www.postgresql.org/docs/current/ddl-constraints.html
            :class-card: sd-border-secondary

            **Normalization and Denormalization**

            Covered in the next lecture. Functional dependencies, normal
            forms (1NF through BCNF), decomposition algorithms, and
            denormalization trade-offs.

        .. grid-item-card:: 📐 Relational Algebra (L5)
            :class-card: sd-border-secondary

            **Relational Algebra**

            Mathematical foundation for SQL queries. Selection, projection,
            join, union, difference, and Cartesian product operations
            defined on relations.

        .. grid-item-card:: 📊 Physical Design
            :class-card: sd-border-secondary

            **Physical Database Design**

            Translating the logical model into DDL for a specific DBMS.
            Includes indexes, storage engines, data types, partitioning,
            and performance tuning.

        .. grid-item-card:: 🎯 SQL Implementation
            :link: https://www.postgresql.org/docs/current/sql-createtable.html
            :class-card: sd-border-secondary

            **PostgreSQL CREATE TABLE**

            Official documentation for creating tables with constraints
            in PostgreSQL, the DBMS used in this course.
