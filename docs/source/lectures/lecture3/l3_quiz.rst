====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 3: Logical Data Modeling,
including the relational model, Crow's Foot notation, keys, foreign keys,
referential integrity, and the 7-step ER-to-Relational mapping algorithm.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is the primary purpose of the logical data model?

   A. To specify storage indexes and partitioning strategies.

   B. To capture what data exists and how it relates, independent of technology.

   C. To translate the conceptual model into tables, columns, and foreign keys that can be implemented in any relational DBMS.

   D. To write SQL queries for data retrieval.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- To translate the conceptual model into tables, columns, and foreign keys that can be implemented in any relational DBMS.

   The logical model resolves conceptual constructs (M:N relationships, multivalued attributes, ISA hierarchies) into tables and foreign keys while remaining DBMS-independent.


.. admonition:: Question 2
   :class: hint

   In the relational model, what is a **relation**?

   A. A connection between two tables via a foreign key.

   B. A named set of tuples with a fixed schema; formally a subset of the Cartesian product of its attribute domains.

   C. A diamond shape connecting two entities in an ER diagram.

   D. A SQL ``JOIN`` statement.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A named set of tuples with a fixed schema.

   A relation is a mathematical object: a subset of the Cartesian product of its attribute domains. Informally, it is a table.


.. admonition:: Question 3
   :class: hint

   Which of the following is NOT a property of a relation in the pure relational model?

   A. No duplicate tuples.

   B. Tuples are unordered.

   C. Attributes are ordered by their creation sequence.

   D. All values are atomic.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Attributes are ordered by their creation sequence.

   In the pure relational model, attributes are unordered; we reference them by name, not position. SQL tables do have a column order, but this is a practical deviation from theory.


.. admonition:: Question 4
   :class: hint

   What distinguishes a **candidate key** from a **superkey**?

   A. A candidate key can contain NULL values.

   B. A candidate key is a minimal superkey; removing any attribute breaks uniqueness.

   C. A superkey must be a single attribute.

   D. There is no difference; the terms are interchangeable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A candidate key is a minimal superkey; removing any attribute breaks uniqueness.

   Every candidate key is a superkey, but superkeys may contain unnecessary attributes. A candidate key has nothing extra.


.. admonition:: Question 5
   :class: hint

   In Crow's Foot notation, what does a **crow's foot symbol** (fork) at the end of a line next to an entity indicate?

   A. Exactly one instance of that entity participates.

   B. Zero instances participate.

   C. Many instances of that entity can participate (the "many" side).

   D. The entity is a weak entity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Many instances of that entity can participate (the "many" side).

   The crow's foot (fork) symbol indicates maximum cardinality of "many". The inner symbol gives the maximum; the outer symbol gives the minimum.


.. admonition:: Question 6
   :class: hint

   In Step 1 of the mapping algorithm, how are **multivalued attributes** handled?

   A. They are included as array columns in the entity's table.

   B. They are stored as comma-separated values in a single column.

   C. They are NOT included in the entity's table; they are deferred to Step 6.

   D. They are converted to CHECK constraints.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- They are NOT included in the entity's table; they are deferred to Step 6.

   Multivalued attributes violate 1NF if placed in the entity's table. They get their own tables in Step 6 with PK = FK + attribute value.


.. admonition:: Question 7
   :class: hint

   In Step 2 (weak entities), what forms the primary key of the weak entity's table?

   A. Only the partial key (discriminator).

   B. A system-generated surrogate key.

   C. The owner entity's PK combined with the partial key (discriminator).

   D. The foreign key to the owner entity only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The owner entity's PK combined with the partial key (discriminator).

   The weak entity borrows part of its identity from the owner. For example, ``COURSE_SECTION`` has PK = (``course_id``, ``section_no``).


.. admonition:: Question 8
   :class: hint

   When mapping a 1:1 relationship (Step 3), where should the FK be placed to minimize NULLs?

   A. On the side with partial participation.

   B. On the side with total participation.

   C. On either side; it does not matter.

   D. In a separate junction table.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- On the side with total participation.

   Total participation means every instance must participate, so the FK is never NULL. Placing it on the partial side would produce NULLs for non-participating instances.


.. admonition:: Question 9
   :class: hint

   In Step 4 (1:N relationships), where is the FK placed?

   A. On the "one" side.

   B. On the "many" side.

   C. In a junction table.

   D. On whichever side has total participation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- On the "many" side.

   Each row on the "many" side references one row on the "one" side. Placing the FK on the "one" side would require multiple values per cell, violating 1NF.


.. admonition:: Question 10
   :class: hint

   Why does an M:N relationship require a junction table (Step 5)?

   A. Because M:N is too complex for SQL to handle natively.

   B. Because placing an FK on either side would require multiple values in a single cell, violating 1NF.

   C. Because junction tables improve query performance.

   D. Because all relationships require junction tables.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Because placing an FK on either side would require multiple values in a single cell, violating 1NF.

   In an M:N, each entity on one side relates to many on the other. A single FK column cannot hold multiple values atomically.


.. admonition:: Question 11
   :class: hint

   In the ``ENROLLMENT`` junction table, the PK is (``student_person_id``, ``course_id``, ``section_no``). Where does the ``grade`` attribute belong?

   A. In the ``STUDENT`` table.

   B. In the ``COURSE_SECTION`` table.

   C. In the ``ENROLLMENT`` junction table, because it describes the specific pairing.

   D. In a separate ``GRADE`` table.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- In the ``ENROLLMENT`` junction table, because it describes the specific pairing.

   ``grade`` only has meaning when both the student and the course section are known. It belongs to the association, not to either entity alone.


.. admonition:: Question 12
   :class: hint

   What is a **lookup table** (reference table)?

   A. A table that stores temporary query results.

   B. A strong entity that constrains a column to a fixed set of valid values while providing metadata like display names and sort order.

   C. A junction table for M:N relationships.

   D. A table that stores foreign key references only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A strong entity that constrains a column to a fixed set of valid values while providing metadata.

   Lookup tables like ``ACADEMIC_RANK`` provide display names, sort order, and other metadata that a simple ``CHECK`` constraint cannot store.


.. admonition:: Question 13
   :class: hint

   When mapping a ternary relationship (Step 7), how should you determine the PK of the new table?

   A. Always include all three FKs in the PK.

   B. Never include any FKs in the PK; use a surrogate key.

   C. Ask whether each participant can appear more than once for the same combination of the other key columns; include only those that can.

   D. Use the PK of the largest participating entity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Ask whether each participant can appear more than once for the same combination of the other key columns.

   For ``TA_ASSIGNMENT``, each section has exactly one TA, so ``grad_person_id`` is not in the PK. Blindly including all FKs would allow multiple TAs per section.


.. admonition:: Question 14
   :class: hint

   In ISA mapping, which strategy is the safest general-purpose choice?

   A. Strategy B (subclass-only tables).

   B. Strategy C (single table with discriminator).

   C. Strategy A (separate superclass + subclass tables with shared PK).

   D. It depends entirely on the number of attributes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Strategy A (separate superclass + subclass tables with shared PK).

   Strategy A works for any combination of constraints (disjoint/overlapping, total/partial) and supports shared queries on the superclass without ``UNION ALL``.


.. admonition:: Question 15
   :class: hint

   How is a **category (union type)** mapped differently from an ISA hierarchy?

   A. Categories use the superclass PK directly.

   B. Categories require a surrogate PK, a discriminator column, and mutually exclusive nullable FKs because the superclasses have incompatible PKs.

   C. Categories are always mapped using Strategy B.

   D. Categories do not use foreign keys.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Categories require a surrogate PK, a discriminator column, and mutually exclusive nullable FKs.

   Unlike ISA where subclasses share a common superclass PK, category superclasses have incompatible PKs (``ssn`` vs. ``tax_id`` vs. ``routing_no``), so a surrogate key is required.


.. admonition:: Question 16
   :class: hint

   What does ``ON DELETE CASCADE`` mean for a foreign key constraint?

   A. Prevent the parent row from being deleted.

   B. Set the FK column to NULL when the parent is deleted.

   C. Automatically delete child rows when the referenced parent row is deleted.

   D. Log the deletion for audit purposes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Automatically delete child rows when the referenced parent row is deleted.

   ``CASCADE`` propagates the deletion from parent to children. This is appropriate for weak entities (deleting a course deletes its sections) but dangerous for other relationships.


.. admonition:: Question 17
   :class: hint

   Which of the following correctly describes the **degree** and **cardinality** of a relation?

   A. Degree is the number of rows; cardinality is the number of columns.

   B. Degree is the number of columns (attributes); cardinality is the number of rows (tuples).

   C. Both refer to the number of relationships a table participates in.

   D. Degree is the number of foreign keys; cardinality is the number of primary keys.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Degree is the number of columns (attributes); cardinality is the number of rows (tuples).

   Degree is a property of the schema (rarely changes); cardinality is a property of the instance (changes with every DML operation).


.. admonition:: Question 18
   :class: hint

   In Crow's Foot notation, what does a **circle** at the outer position of a line end indicate?

   A. Mandatory participation (total).

   B. Optional participation (partial); the entity may have zero instances in the relationship.

   C. The entity is a weak entity.

   D. The relationship has attributes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Optional participation (partial); the entity may have zero instances in the relationship.

   The outer symbol indicates minimum participation. A circle means min = 0 (optional); a bar means min = 1 (mandatory).


.. admonition:: Question 19
   :class: hint

   Why do FK column names not need to match the referenced PK column name?

   A. Because FKs and PKs use different data types.

   B. Because they must share the same domain (data type), but descriptive FK names clarify the role of the relationship, especially when multiple FKs reference the same table.

   C. Because SQL does not allow matching column names across tables.

   D. Because FKs are always auto-generated by the DBMS.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Descriptive FK names clarify the role of the relationship.

   ``advisor_person_id`` is more informative than just ``person_id`` when ``STUDENT`` references ``PROFESSOR``. This is especially important when multiple FKs reference the same table.


.. admonition:: Question 20
   :class: hint

   What is the key difference between how the relational model and SQL handle duplicate rows?

   A. The relational model allows duplicates; SQL does not.

   B. Both forbid duplicates by default.

   C. The relational model forbids duplicates (a relation is a set); SQL allows them by default and requires explicit PRIMARY KEY or UNIQUE constraints to prevent them.

   D. SQL forbids duplicates; the relational model is ambiguous.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The relational model forbids duplicates; SQL allows them by default.

   A relation is a set (no duplicates by definition). SQL tables are bags by default; you must add ``PRIMARY KEY`` or ``UNIQUE`` constraints to enforce uniqueness.


----


True or False
=============

.. admonition:: Question 21
   :class: hint

   **True or False:** In the relational model, the order of tuples (rows) in a relation matters.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Tuples are unordered in the relational model. {Alice, Bob} and {Bob, Alice} represent the same relation. If you need a specific order, use ``ORDER BY`` at query time.


.. admonition:: Question 22
   :class: hint

   **True or False:** A foreign key value must always match an existing primary key value in the referenced table or be NULL (if the FK is nullable).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   This is the referential integrity constraint. Every FK value must either match an existing PK value in the referenced table or be NULL (if the FK column is nullable).


.. admonition:: Question 23
   :class: hint

   **True or False:** Derived attributes (like ``age`` computed from ``date_of_birth``) are included as regular columns during Step 1 of the mapping algorithm.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Derived attributes are omitted during mapping. They are computed at query time (e.g., ``age`` = ``CURRENT_DATE`` - ``date_of_birth``). Storing them would create stale data.


.. admonition:: Question 24
   :class: hint

   **True or False:** In a 1:N relationship, placing the FK on the "one" side would require storing multiple values in a single cell, violating First Normal Form.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A department can have many professors. If we stored ``professor_ids`` in ``DEPARTMENT``, the column would need to hold a set of values, which violates atomicity (1NF).


.. admonition:: Question 25
   :class: hint

   **True or False:** A junction table's primary key is always the composite of the PKs from both participating entities.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The junction table's PK is the composite of the two FK columns, ensuring each pairing is unique. Example: ``ENROLLMENT`` PK = (``student_person_id``, ``course_id``, ``section_no``).


.. admonition:: Question 26
   :class: hint

   **True or False:** In a 1:1 relationship where both sides have partial participation, NULLs in the FK column are unavoidable regardless of which side holds the FK.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   With both sides partial, not every instance on either side participates. Whichever side holds the FK will have NULL for non-participating instances. The strategy is to pick the side with fewer NULLs.


.. admonition:: Question 27
   :class: hint

   **True or False:** Strategy A for ISA mapping works for any combination of disjoint/overlapping and total/partial constraints.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Strategy A creates a superclass table plus one subclass table per subclass, connected by shared PK. This handles overlapping (a row in multiple subclass tables), partial (no row in any subclass table), and disjoint/total combinations.


.. admonition:: Question 28
   :class: hint

   **True or False:** A lookup table serves the same purpose as a ``CHECK`` constraint but provides additional metadata like display names and sort order.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A ``CHECK`` constraint validates values but cannot store metadata. A lookup table can store display names (``rank_name``), sort order (``rank_order``), descriptions, and other attributes per value.


.. admonition:: Question 29
   :class: hint

   **True or False:** In a category (union type) mapping, all FK columns in the category table must be non-NULL for every row.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Exactly **one** FK is non-NULL per row, and the rest are NULL. Each row belongs to exactly one superclass. A ``CHECK`` constraint enforces this invariant.


.. admonition:: Question 30
   :class: hint

   **True or False:** The identifying relationship for a weak entity produces its own separate table during mapping.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The identifying relationship is absorbed into the weak entity's table. The owner's PK becomes part of the weak entity's composite PK. No separate relationship table is created.


.. admonition:: Question 31
   :class: hint

   **True or False:** A composite foreign key references a composite primary key, and all component columns must match together.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A composite FK like ``ENROLLMENT``.(``course_id``, ``section_no``) references ``COURSE_SECTION``.(``course_id``, ``section_no``). Both columns must match an existing row together.


.. admonition:: Question 32
   :class: hint

   **True or False:** Every superkey is a candidate key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Every candidate key is a superkey, but not every superkey is a candidate key. A superkey may contain unnecessary attributes. A candidate key is a *minimal* superkey.


.. admonition:: Question 33
   :class: hint

   **True or False:** In Crow's Foot notation, a bar symbol (|) at the inner position means "at most one" (maximum cardinality of 1).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The inner symbol (closest to the entity) indicates maximum cardinality. A bar means maximum of 1 (single-valued). A crow's foot means maximum of many.


.. admonition:: Question 34
   :class: hint

   **True or False:** Relationship attributes on an M:N relationship are placed in the junction table, not in either participating entity's table.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Relationship attributes like ``grade`` on ``ENROLLS_IN`` belong to the pairing, not to either entity alone. They are placed in the junction table that represents the M:N relationship.


.. admonition:: Question 35
   :class: hint

   **True or False:** ``ON DELETE RESTRICT`` prevents the deletion of a parent row if any child rows reference it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``RESTRICT`` prevents the delete operation entirely if any child rows exist. The parent row cannot be removed until all referencing child rows are deleted or updated first.


----


Essay Questions
===============

.. admonition:: Question 36
   :class: hint

   Explain the difference between a **relation schema (intension)** and a **relation instance (extension)**. Use the ``PERSON`` table as an example and provide an OOP analogy.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A **relation schema (intension)** defines the *structure*: the relation name, its attribute names, and their domains. Example: ``PERSON`` (``person_id``: int, ``first_name``: varchar, ``last_name``: varchar, ``date_of_birth``: date). It is like a **class definition** in OOP.
   - A **relation instance (extension)** is the *data*: the specific set of tuples conforming to the schema at a point in time. Example: {(P101, Alice, Smith, 1998-03-15), (P102, Bob, Jones, 1999-07-22)}. It is like the **objects in memory** in OOP.
   - The schema changes rarely (only via ``ALTER TABLE``); the instance changes with every ``INSERT``, ``UPDATE``, or ``DELETE``.
   - Adding a student (Carlos) changes the instance but not the schema.


.. admonition:: Question 37
   :class: hint

   A university has a 1:1 relationship ``CHAIRS`` between ``PROFESSOR`` and ``DEPARTMENT``. ``PROFESSOR`` has partial participation and ``DEPARTMENT`` has total participation. Explain where the FK should be placed and why, including the constraints that should be applied to the FK column.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The FK should be placed on **DEPARTMENT** (the total participation side), not on ``PROFESSOR``.
   - ``DEPARTMENT`` has total participation: every department **must** have a chair. This means the FK column (``chair_id``) is never NULL.
   - The FK should be constrained with ``NOT NULL`` (total participation) and ``UNIQUE`` (1:1 cardinality, so no professor can chair two departments).
   - If the FK were placed on ``PROFESSOR`` instead, most professors are not chairs, so the column would be mostly NULL (wasted storage, complicated queries).
   - The relationship attribute ``start_date`` migrates to ``DEPARTMENT`` alongside the FK.


.. admonition:: Question 38
   :class: hint

   Compare and contrast the three ISA mapping strategies (A, B, C). For each, describe when it is most appropriate and what trade-offs it introduces. Which strategy did we use for the university model and why?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Strategy A (Separate Tables)**: Create superclass table + one table per subclass. Subclass PK = superclass PK (also FK). Best for overlapping or partial hierarchies, and when shared queries on the superclass are common. Trade-off: requires ``JOIN`` to get full entity data.
   - **Strategy B (Subclass Only)**: No superclass table; each subclass table includes all inherited attributes. Best for disjoint + total hierarchies with few shared queries. Trade-off: duplicates superclass columns; requires ``UNION ALL`` for cross-subclass queries.
   - **Strategy C (Single Table)**: One table with a type discriminator column and all attributes from all subclasses. Best when there are few subclasses with few distinct attributes and fast reads are needed. Trade-off: many NULL columns for subclass-specific attributes; cannot enforce subclass-specific ``NOT NULL`` constraints.
   - **University model**: We used **Strategy A** for both ISA hierarchies. For PERSON -> STUDENT/PROFESSOR (disjoint, total): the flowchart suggests Strategy B, but we need ``PERSON`` for shared queries, phone numbers, and emails. For STUDENT -> GRAD_STUDENT/INTL_STUDENT (overlapping, partial): only Strategy A handles both correctly.
