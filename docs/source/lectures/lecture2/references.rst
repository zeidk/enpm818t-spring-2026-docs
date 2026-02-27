References
==========


.. dropdown:: 🏛️ Lecture 2
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T — L2: Conceptual Data Modeling**

        Covers the role of conceptual modeling in database design, Entity-Relationship
        diagrams using Chen notation, entities (strong vs. weak), attributes
        (simple, composite, multivalued, derived), keys (superkey, candidate key,
        primary key, partial key), relationships with cardinality and participation
        constraints, Extended ER concepts (specialization/generalization,
        categories), and a complete university system use case walkthrough.


.. dropdown:: 📚 Foundational Papers & Textbooks
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📄 Chen (1976) — The ER Model
            :link: https://dl.acm.org/doi/10.1145/320434.320440
            :class-card: sd-border-secondary

            **Peter Chen — "The Entity-Relationship Model"**

            The original 1976 paper introducing the Entity-Relationship model,
            Chen notation, and the foundational concepts of entities, attributes,
            and relationships. Published in *ACM Transactions on Database Systems*.

            +++

            - Defines entities, relationships, and attributes
            - Introduces Chen notation (rectangles, ovals, diamonds)
            - Foundational work in database design

        .. grid-item-card:: 📘 Elmasri & Navathe
            :class-card: sd-border-secondary

            **Elmasri, Navathe — "Fundamentals of Database Systems" (7th Ed.)**

            Comprehensive database textbook covering ER modeling (Chapters 3–4),
            relational model, normalization, and advanced topics. Industry
            standard for database courses.

            +++

            - Chapters 3–4: ER and EER modeling
            - Chapter 9: Relational design and normalization
            - Extensive coverage of Chen notation

        .. grid-item-card:: 📗 Silberschatz, Korth & Sudarshan
            :class-card: sd-border-secondary

            **Silberschatz et al. — "Database System Concepts" (7th Ed.)**

            Alternative foundational textbook with strong coverage of ER modeling
            (Chapter 2), relational algebra, and database implementation.

            +++

            - Chapter 2: ER model and EER extensions
            - Focuses on both Chen and UML notations
            - Strong theoretical foundations

        .. grid-item-card:: 📙 Ramakrishnan & Gehrke
            :class-card: sd-border-secondary

            **Ramakrishnan, Gehrke — "Database Management Systems" (3rd Ed.)**

            Practical approach to database design and implementation. Covers
            ER modeling with industry-focused examples.

            +++

            - Chapter 2: ER model
            - Emphasis on design patterns and best practices
            - Good coverage of weak entities and cardinality


.. dropdown:: 🛠️ ER Modeling Tools
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🖊️ ERDPlus
            :link: https://erdplus.com
            :class-card: sd-border-secondary

            **ERDPlus — Free Chen Notation Tool**

            Browser-based ER diagram tool designed specifically for Chen notation.
            Exports to relational schemas. Recommended for homework.

            +++

            - Native Chen notation support
            - Automatic schema generation
            - Free, no account required

        .. grid-item-card:: 📐 draw.io (diagrams.net)
            :link: https://app.diagrams.net
            :class-card: sd-border-secondary

            **draw.io — General Diagramming Tool**

            Browser-based diagramming with built-in Entity Relation shape library
            that includes Chen symbols.

            +++

            - Free and open source
            - Entity Relation shape library
            - Exports to PNG, SVG, PDF

        .. grid-item-card:: 💼 Lucidchart
            :link: https://www.lucidchart.com
            :class-card: sd-border-secondary

            **Lucidchart — Collaborative Diagramming**

            Cloud-based diagramming tool with Chen notation support via shape
            libraries. Free tier available.

            +++

            - Collaborative editing
            - Chen shape libraries available
            - Integration with Google Drive

        .. grid-item-card:: 🖋️ Microsoft Visio
            :link: https://www.microsoft.com/en-us/microsoft-365/visio
            :class-card: sd-border-secondary

            **Microsoft Visio**

            Professional diagramming tool with Chen notation templates. Common in
            enterprise environments.

            +++

            - Chen notation templates
            - Part of Microsoft 365
            - Industry-standard tool


.. dropdown:: 📖 ER Modeling Tutorials & Guides
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🎓 Stanford ER Tutorial
            :link: https://web.stanford.edu/class/cs145/
            :class-card: sd-border-secondary

            **Stanford CS145 — Database Systems**

            Lecture notes and materials on ER modeling from Stanford's database
            course. Includes practical examples and exercises.

        .. grid-item-card:: 📘 Visual Paradigm ER Guide
            :link: https://www.visual-paradigm.com/guide/data-modeling/what-is-entity-relationship-diagram/
            :class-card: sd-border-secondary

            **Visual Paradigm — ER Diagram Guide**

            Comprehensive guide covering ER concepts, notation types (Chen,
            Crow's Foot, UML), and practical examples.

        .. grid-item-card:: 🌐 TutorialsPoint ER Tutorial
            :link: https://www.tutorialspoint.com/dbms/er_model_basic_concepts.htm
            :class-card: sd-border-secondary

            **TutorialsPoint — ER Model Tutorial**

            Step-by-step tutorial covering entities, attributes, relationships,
            and extended ER concepts with examples.

        .. grid-item-card:: 📚 GeeksforGeeks ER Guide
            :link: https://www.geeksforgeeks.org/introduction-of-er-model/
            :class-card: sd-border-secondary

            **GeeksforGeeks — ER Model Introduction**

            Beginner-friendly introduction to ER modeling with clear explanations
            and diagrams.


.. dropdown:: 🔬 Extended ER (EER) Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📄 Teorey et al. (1986)
            :link: https://dl.acm.org/doi/10.1145/5397.5399
            :class-card: sd-border-secondary

            **Teorey et al. — "A Logical Design Methodology for ER Databases"**

            Classic paper on ER-to-relational mapping, including handling of
            specialization hierarchies and weak entities.

        .. grid-item-card:: 📘 Elmasri & Navathe Chapter 4
            :class-card: sd-border-secondary

            **Enhanced ER (EER) Model**

            Chapter 4 of Elmasri & Navathe covers specialization/generalization,
            aggregation, categories (union types), and constraint notation in
            detail.

        .. grid-item-card:: 🎓 MIT OpenCourseWare
            :link: https://ocw.mit.edu/courses/6-830-database-systems-fall-2010/
            :class-card: sd-border-secondary

            **MIT 6.830 — Database Systems**

            Lecture materials on conceptual modeling, ER diagrams, and relational
            design from MIT's database systems course.

        .. grid-item-card:: 📖 Database Design Book
            :class-card: sd-border-secondary

            **Connolly & Begg — "Database Systems: A Practical Approach"**

            Comprehensive coverage of conceptual, logical, and physical design
            with extensive ER modeling examples.


.. dropdown:: 🎯 Practice & Exercises
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🏋️ ER Diagram Practice
            :link: https://www.w3resource.com/sql-exercises/er-diagram-exercises/
            :class-card: sd-border-secondary

            **W3Resource — ER Diagram Exercises**

            Collection of ER modeling exercises with solutions covering various
            domains (library, hospital, university, etc.).

        .. grid-item-card:: 📝 Database Design Examples
            :link: https://www.vertabelo.com/blog/database-model-examples/
            :class-card: sd-border-secondary

            **Vertabelo — Database Model Examples**

            Real-world database design examples with complete ER diagrams for
            various industries and use cases.

        .. grid-item-card:: 🎓 Stanford Database Course
            :link: https://lagunita.stanford.edu/courses/DB/2014/SelfPaced/about
            :class-card: sd-border-secondary

            **Stanford Online — Databases: Relational Databases and SQL**

            Free online course covering database design, ER modeling, and SQL.
            Includes interactive exercises and quizzes.

        .. grid-item-card:: 🧮 ER Quiz Generator
            :link: https://www.proprofs.com/quiz-school/topic/entity-relationship-diagram
            :class-card: sd-border-secondary

            **ProProfs — ER Diagram Quizzes**

            Interactive quizzes testing your understanding of ER concepts,
            notation, and design principles.


.. dropdown:: 📹 Video Tutorials
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🎥 Lucidchart ER Tutorial
            :link: https://www.youtube.com/watch?v=QpdhBUYk7Kk
            :class-card: sd-border-secondary

            **Lucidchart — ER Diagrams Tutorial**

            Comprehensive video introduction to ER diagrams, covering entities,
            attributes, relationships, and cardinality with examples.

        .. grid-item-card:: 🎬 freeCodeCamp Database Course
            :link: https://www.youtube.com/watch?v=HXV3zeQKqGY
            :class-card: sd-border-secondary

            **freeCodeCamp — Database Design Course**

            4-hour video course covering database design from conceptual modeling
            through implementation. Includes extensive ER modeling coverage.

        .. grid-item-card:: 📺 Stanford CS145 Lectures
            :link: https://www.youtube.com/playlist?list=PL6hGtHedy2Z4EkgY76QOcueU8lAC4o6c3
            :class-card: sd-border-secondary

            **Stanford CS145 — Introduction to Databases**

            Lecture videos from Stanford's database course, including detailed
            coverage of ER modeling and relational design.

        .. grid-item-card:: 🎞️ SQL Tutorial ER Section
            :link: https://www.youtube.com/watch?v=-fQ-bRllhXc
            :class-card: sd-border-secondary

            **Programming with Mosh — Database Design**

            Tutorial covering ER modeling fundamentals with practical examples
            and design patterns.


.. dropdown:: 🔗 Related Topics
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 🧱 UML Class Diagrams
            :link: https://www.uml-diagrams.org/class-diagrams-overview.html
            :class-card: sd-border-secondary

            **UML Class Diagrams**

            Object-oriented alternative to ER diagrams. While this course uses
            Chen notation, UML is common in software engineering contexts.

        .. grid-item-card:: 📐 Crow's Foot Notation
            :link: https://www.vertabelo.com/blog/crow-s-foot-notation/
            :class-card: sd-border-secondary

            **Crow's Foot Notation Guide**

            Industry-standard alternative to Chen notation. Common in tools like
            ERwin and MySQL Workbench.

        .. grid-item-card:: 📊 IDEF1X Notation
            :link: https://www.idef.com/idef1x/
            :class-card: sd-border-secondary

            **IDEF1X — Federal Standard**

            US federal standard for ER modeling (FIPS 184). Common in government
            and defense contracting.

        .. grid-item-card:: 🎯 Normalization
            :link: https://www.postgresql.org/docs/current/ddl-constraints.html
            :class-card: sd-border-secondary

            **Database Normalization**

            Logical design topic covered in Lecture 3. Understanding conceptual
            modeling is essential before learning normalization.


.. dropdown:: 📝 Design Patterns & Best Practices
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: 📖 Database Design Patterns
            :link: https://www.vertabelo.com/blog/database-design-patterns/
            :class-card: sd-border-secondary

            **Vertabelo — Database Design Patterns**

            Collection of common design patterns for modeling typical scenarios
            (many-to-many, hierarchies, historical data, etc.).

        .. grid-item-card:: 🎯 ER Best Practices
            :link: https://database.guide/er-diagram-best-practices/
            :class-card: sd-border-secondary

            **Database.Guide — ER Diagram Best Practices**

            Guidelines for creating clear, maintainable ER diagrams including
            naming conventions, layout, and documentation.

        .. grid-item-card:: 🔍 Common ER Mistakes
            :link: https://www.vertabelo.com/blog/common-er-diagram-mistakes/
            :class-card: sd-border-secondary

            **Vertabelo — Common ER Diagram Mistakes**

            Guide to avoiding fan traps, chasm traps, redundant relationships,
            and other common modeling errors.

        .. grid-item-card:: 📚 Data Modeling Handbook
            :class-card: sd-border-secondary

            **Steve Hoberman — "Data Modeling Made Simple"**

            Practical guide to data modeling covering conceptual, logical, and
            physical design with industry examples and best practices.
