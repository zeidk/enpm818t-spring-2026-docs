====================================================
Lecture
====================================================



From Conceptual to Logical
====================================================


.. dropdown:: Where We Are in the Design Lifecycle
   :class-container: sd-border-secondary
   :open:

   Three Levels of Data Modeling (Revisited)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 15 22 22 22 19
      :header-rows: 1
      :class: compact-table

      * -
        - Conceptual
        - Logical
        - Physical
      * - **Goal**
        - What data exists and how it relates
        - How data is structured in tables
        - How tables are stored on disk
      * - **Notation**
        - Chen/EER
        - Crow's Foot / Relational Schema
        - DDL (SQL), indexes, partitions
      * - **Audience**
        - Stakeholders, analysts
        - Developers, DBAs
        - DBAs, sysadmins
      * - **Contains**
        - Entities, attributes, relationships, ISA, categories
        - Tables, columns, PKs, FKs, constraints
        - Data types, indexes, storage engines
      * - **DBMS?**
        - No
        - No (still abstract)
        - Yes (PostgreSQL, MySQL, etc.)

   .. important::

      **Today**: We convert the conceptual model (L2) into a logical model using a systematic, step-by-step algorithm. The result is a set of **relational schemas** that can then be implemented in any relational DBMS.


.. dropdown:: Why Not Jump Straight to SQL?
   :class-container: sd-border-secondary

   Four Reasons for a Logical Layer
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   1. **Conceptual constructs have no direct SQL equivalent.** :math:`M{:}N` relationships, multivalued attributes, weak entities, ISA hierarchies, and categories must be *resolved* into tables and foreign keys.

   2. **Design validation before implementation.** Normalization operates on the logical model. It is easier to detect redundancy and anomalies in a schema than in SQL scripts.

   3. **DBMS independence.** The logical model uses abstract types (``INTEGER``, ``VARCHAR``), not vendor-specific syntax. The same logical model can target PostgreSQL, MySQL, Oracle, or SQL Server.

   4. **Communication with developers.** Stakeholders validated the conceptual model; developers work with the logical model.


.. dropdown:: Crow's Foot Notation: Quick Reference
   :class-container: sd-border-secondary

   Key Differences from Chen
   ~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 25 35 40
      :header-rows: 1
      :class: compact-table

      * - Concept
        - Chen (Conceptual)
        - Crow's Foot (Logical)
      * - Entity
        - Rectangle (name only)
        - Rectangle with columns listed
      * - Attributes
        - Ovals radiating outward
        - Rows inside the entity box
      * - Primary Key
        - Underlined oval
        - PK marker or bold/underline
      * - Foreign Key
        - Not shown explicitly
        - FK marker with reference arrow
      * - Relationship
        - Diamond with verb phrase
        - Line between entities (no diamond)
      * - Cardinality
        - Numbers (:math:`1`, :math:`N`, :math:`M`)
        - Fork (crow's foot) symbols
      * - Participation
        - Single/double line
        - Circle (optional) / Bar (mandatory)
      * - Weak Entity
        - Double rectangle + double diamond
        - Table with composite PK
      * - Multivalued Attr
        - Double-bordered oval
        - Separate table with FK

   .. card::
       :class-card: sd-border-info

       **Crow's Foot is closer to implementation**: Every entity is already a table. Every attribute is a column. Relationships are foreign keys. This is the standard in industry tools (ERwin, DbSchema, DataGrip, pgAdmin, DBeaver).


   Reading Crow's Foot Cardinality Symbols
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Each end of a relationship line has two components: the **inner symbol** (closest to the entity) specifies *maximum* cardinality, and the **outer symbol** (farther from the entity) specifies *minimum* participation.

   .. list-table::
      :widths: 15 15 40 30
      :header-rows: 1
      :class: compact-table

      * - Inner (max)
        - Outer (min)
        - Meaning
        - Chen Equivalent
      * - ``|`` (bar)
        - ``|`` (bar)
        - Exactly one (mandatory, single)
        - Total, :math:`1`
      * - ``|`` (bar)
        - ``○`` (circle)
        - Zero or one (optional, single)
        - Partial, :math:`1`
      * - ``<`` (crow's foot)
        - ``|`` (bar)
        - One or many (mandatory, multi)
        - Total, :math:`N`
      * - ``<`` (crow's foot)
        - ``○`` (circle)
        - Zero or many (optional, multi)
        - Partial, :math:`N`


   Reading a Crow's Foot Diagram
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. only:: html

      .. figure:: /_static/images/l3/example-erd-relational-light.png
         :alt: ERD to Relational mapping example
         :width: 90%
         :align: center
         :class: only-light

         **ERD to Relational mapping example**: Chen notation (top) mapped to Crow's Foot notation (bottom)

      .. figure:: /_static/images/l3/example-erd-relational-dark.png
         :alt: ERD to Relational mapping example
         :width: 90%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/example-erd-relational-light.png
         :alt: ERD to Relational mapping example
         :width: 90%
         :align: center

         **ERD to Relational mapping example**: Chen notation (left) mapped to Crow's Foot notation (right)



   Table Symbols
   ^^^^^^^^^^^^^^

   - **PK (Primary Key)**: Uniquely identifies each row. Cannot be ``NULL`` or duplicated. Example: ``dept_id`` in ``DEPARTMENT``.
   - **FK (Foreign Key)**: References a PK in another table, enforcing a link. Example: ``dept_id`` in ``PROFESSOR`` must match a valid ``dept_id`` in ``DEPARTMENT``.
   - **PK, FK**: A column that is both the table's PK and an FK to another table. Example: ``person_id`` in ``PROFESSOR`` is inherited from ``PERSON`` (ISA).
   - **UK (Unique Key)**: Must be unique across all rows but is not the chosen PK. Example: ``professor_id`` is a business identifier enforced with ``UNIQUE``. Also called an **Alternate Key (AK)**.

   Reading the Line
   ^^^^^^^^^^^^^^^^^

   - **Bar + bar** at ``DEPARTMENT``: exactly one (each professor belongs to one department)
   - **Crow's foot + bar** at ``PROFESSOR``: one or many (a department has one or more professors)
   - The FK (``dept_id``) lives on the crow's foot side (the "many" side)




Relational Database Fundamentals
====================================================


.. dropdown:: The Relational Model
   :class-container: sd-border-secondary
   :open:

   A **relational database** stores data in structured **tables** (also called *relations*), providing powerful ways to retrieve and manipulate data efficiently.

   .. list-table::
      :widths: 15 20 30 35
      :header-rows: 1
      :class: compact-table

      * - Formal Term
        - Informal Term
        - Definition
        - University Example
      * - Relation
        - Table
        - A named set of tuples with a fixed schema
        - ``STUDENT``, ``COURSE``
      * - Tuple
        - Row/Record
        - A single data instance in a relation
        - One specific student
      * - Attribute
        - Column/Field
        - A named property of a relation
        - ``first_name``, ``gpa``
      * - Domain
        - Data type + constraints
        - The set of allowable values for an attribute
        - ``gpa`` :math:`\in [0.0,\, 4.0]`
      * - Schema
        - Table definition
        - The structure: name + list of attributes and their domains
        - ``STUDENT`` (``person_id``, ``gpa``, ...)


   Four Benefits of the Relational Model
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   1. **Data integrity through constraints.** The database itself enforces rules: primary keys guarantee uniqueness, foreign keys prevent orphaned records, ``NOT NULL`` eliminates missing required values, and ``CHECK`` constraints restrict domains. Bad data is rejected *at the database level*, not left for application code to catch.

   2. **Support for complex queries via relational algebra and SQL.** Because relations are mathematical objects, operations like selection (:math:`\sigma`), projection (:math:`\pi`), and join (:math:`\bowtie`) are formally defined and composable (covered in L5). SQL translates these operations into a declarative language: you describe *what* you want, and the DBMS optimizes *how* to retrieve it.

   3. **Enforced relationships between entities via foreign keys.** A foreign key from ``COURSE``.``dept_id`` to ``DEPARTMENT``.``dept_id`` guarantees that every course references a department that actually exists. Without this, deleting a department could silently orphan hundreds of course records.

   4. **DBMS independence.** The logical model uses abstract concepts (tables, columns, keys, constraints) that are not tied to any vendor. The same logical schema can be implemented in PostgreSQL, MySQL, Oracle, or SQL Server.


.. dropdown:: Formal Definition of a Relation
   :class-container: sd-border-primary
   :open:

   .. card:: Formal Definition of a Relation
      :class-card: sd-bg-primary sd-bg-text-light

      Let :math:`D_1, D_2, \ldots, D_n` be **domains** (sets of allowable values). A **relation** :math:`R` on these domains is:

      .. math::

         R \subseteq D_1 \times D_2 \times \cdots \times D_n

      That is, :math:`R` is a **subset of the Cartesian product** of its attribute domains. Each element of :math:`R` is an :math:`n`-tuple :math:`(d_1, d_2, \ldots, d_n)` where :math:`d_i \in D_i`.

   Example: The PERSON Relation
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Domains** (simplified): :math:`D_1` = String (``person_id``), :math:`D_2` = String (``first_name``), :math:`D_3` = String (``middle_name``), :math:`D_4` = String (``last_name``), :math:`D_5` = Date (``date_of_birth``)
   - The **Cartesian product** :math:`D_1 \times D_2 \times \cdots \times D_5` contains every conceivable combination, including nonsensical ones like ``('P999', 'Zz', 'Qq', 'Xx', 1900-01-01)``
   - The relation :math:`R_{\text{PERSON}}` is a **set** containing only the valid tuples (actual people)

   The relation :math:`R_{\text{PERSON}}` is a **set** of tuples, and this set is a **subset** of the Cartesian product of the five domains.


.. dropdown:: Schema vs. Instance
   :class-container: sd-border-secondary

   Relation Schema (Intension)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A **relation schema** defines the *structure* of a relation: the relation name, its attribute names, and their domains. Formally:

   .. math::

      R(A_1\!: D_1,\; A_2\!: D_2,\; \ldots,\; A_n\!: D_n)

   where :math:`R` is the relation name, each :math:`A_i` is an **attribute name**, and each :math:`D_i` is the **domain** of :math:`A_i`.

   The schema is like a **class definition** in OOP: it specifies what fields exist and what types they have, but contains no data. It changes rarely (only via ``ALTER TABLE``).

   .. note::

      We dropped ``phone_numbers`` and ``email_addresses`` from the schema. As multivalued attributes, they cannot be represented as single atomic columns. They will be handled in their own tables during mapping (Step 6).


   Relation Instance (Extension)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A **relation instance** :math:`r(R)` is a specific **set of tuples** conforming to schema :math:`R` at a point in time. It changes with every ``INSERT``, ``UPDATE``, or ``DELETE``. The instance is like the **objects in memory** (OOP): the actual data that currently exists.

   .. list-table::
      :widths: 20 20 20 20 20
      :header-rows: 1
      :class: compact-table

      * - person_id
        - first_name
        - middle_name
        - last_name
        - date_of_birth
      * - P101
        - Alice
        - Maria
        - Smith
        - 1998-03-15
      * - P102
        - Bob
        - NULL
        - Jones
        - 1999-07-22

   *Instance at Week 1*

   .. list-table::
      :widths: 20 20 20 20 20
      :header-rows: 1
      :class: compact-table

      * - person_id
        - first_name
        - middle_name
        - last_name
        - date_of_birth
      * - P101
        - Alice
        - Maria
        - Smith
        - 1998-03-15
      * - P102
        - Bob
        - NULL
        - Jones
        - 1999-07-22
      * - P103
        - Carlos
        - John
        - Rivera
        - 1997-11-08

   *Instance at Week 3*

   - The **schema** did not change. It is still ``PERSON``.
   - The **instance** changed: Carlos was added (``INSERT``).
   - A third snapshot after Bob leaves (``DELETE``) would have different tuples than Week 1.


.. dropdown:: Degree and Cardinality
   :class-container: sd-border-secondary

   These two measures describe the **shape** of a relation:

   - **Degree** (arity): The number of attributes in the schema. It is a property of the *schema* and rarely changes.
   - **Cardinality**: The number of tuples in a particular instance. It is a property of the *instance* and changes constantly.

   For the ``PERSON`` table with 5 columns and 2 rows: degree :math:`= 5`, cardinality :math:`= 2`. Tomorrow, if Carlos is added, the cardinality becomes :math:`3`, but the degree stays :math:`5`.

.. dropdown:: Four Properties of Relations
   :class-container: sd-border-secondary

   Four Properties from Set Theory
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   1. **No duplicate tuples.** Every row is unique. Inserting :math:`(\text{P101},\, \text{Alice},\, \text{Maria},\, \text{Smith},\, \text{1998-03-15})` a second time is **not allowed** because a relation is a *set*, not a bag (multiset). This is guaranteed by the **primary key**: no two tuples share the same ``person_id``.

   2. **Tuples are unordered.** The rows for Alice and Diana can appear in any order; swapping them produces the *same* relation. If you need a specific order, you request it at query time (``ORDER BY``), not in the schema.

   3. **Attributes are unordered.** We reference columns by *name* (e.g., ``gpa``), not by position (e.g., "the 5th column"). Moving the ``last_name`` column before ``first_name`` does not change the relation.

   4. **Values are atomic.** Each cell holds exactly **one indivisible value**: this is why we store ``first_name``, ``middle_name``, and ``last_name`` as separate attributes rather than a single ``name`` field containing "Alice Maria Smith". No arrays, no comma-separated lists, no nested structures inside a cell. This is **First Normal Form (1NF)**, covered in detail in L4. This is exactly why ``phone_numbers`` had to be removed from the schema earlier.


   SQL Tables Are Not Pure Relations
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   The relational model as defined by Codd is a mathematical ideal. SQL, the language we use to interact with relational databases, is a **practical approximation** that deviates in several important ways:

   .. list-table::
      :widths: 15 40 45
      :header-rows: 1
      :class: compact-table

      * - Property
        - Relational Model (Theory)
        - SQL (Practice)
      * - Duplicate tuples
        - Forbidden: a relation is a *set*
        - Allowed by default; must explicitly add a ``PRIMARY KEY`` or ``UNIQUE`` constraint to prevent them
      * - Tuple ordering
        - No inherent order
        - Rows have a physical order on disk; query results are unordered unless ``ORDER BY`` is specified
      * - Attribute ordering
        - No inherent order; reference by name
        - Columns have a defined position; ``SELECT *`` returns them in creation order
      * - NULL values
        - Not part of Codd's original model (added later as a pragmatic extension)
        - Fully supported; any column is nullable unless constrained with ``NOT NULL``
      * - Atomic values
        - Required (1NF)
        - Most DBMSs support arrays, JSON, and composite types inside a single column

   .. card::
       :class-card: sd-border-info

       **Why does this matter?** Understanding the theoretical model helps you recognize *why* constraints exist. When you declare a ``PRIMARY KEY``, you are enforcing the "no duplicate tuples" property. When you add ``NOT NULL``, you are choosing to exclude ``NULL`` s that the theory did not originally anticipate. Every constraint you write in SQL is a deliberate step toward making your table behave more like a true relation.


   Connecting Theory to Practice
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. card::
       :class-card: sd-border-success sd-shadow-sm

       **What Relies on the Formal Foundation**

       - **Key constraints** (next topic): The concept of a "superkey" is defined as a subset of attributes whose values uniquely identify tuples in the set. Without the set-theoretic definition, "uniquely identifies" has no precise meaning.
       - **Normalization** (L4): Normal forms are defined in terms of functional dependencies between attributes. These dependencies only make sense when values are atomic and tuples are unique.
       - **Relational algebra** (L5): Every operator (:math:`\sigma`, :math:`\pi`, :math:`\bowtie`, :math:`\cup`, :math:`\cap`, :math:`-`) takes one or more relations as input and produces a relation as output. The closure property (relations in, relations out) depends on the formal definition.
       - **Query optimization**: The DBMS can reorder joins and push down selections precisely because tuple and attribute order are irrelevant in the relational model.


.. dropdown:: Key Taxonomy
   :class-container: sd-border-secondary

   Types of Keys in the Relational Model
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   In Lecture 2, we marked key attributes with underlined ovals. In the relational model, keys have a formal hierarchy:

   .. only:: html

      .. figure:: /_static/images/l3/keys-light.png
         :alt: Key hierarchy diagram
         :width: 70%
         :align: center
         :class: only-light

         **Key hierarchy**: Superkey :math:`\supset` Candidate Key :math:`\supset` Primary Key / Alternate Key

      .. figure:: /_static/images/l3/keys-dark.png
         :alt: Key hierarchy diagram
         :width: 70%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/keys-light.png
         :alt: Key hierarchy diagram
         :width: 70%
         :align: center

         **Key hierarchy**: Superkey :math:`\supset` Candidate Key :math:`\supset` Primary Key / Alternate Key

   .. list-table::
      :widths: 18 42 40
      :header-rows: 1
      :class: compact-table

      * - Key Type
        - Definition
        - University Example
      * - **Superkey**
        - Any set of attributes that uniquely identifies tuples
        - :math:`\{` ``person_id`` :math:`\}`, :math:`\{` ``person_id``, ``first_name`` :math:`\}`, :math:`\{` ``person_id``, ``date_of_birth`` :math:`\}`
      * - **Candidate Key**
        - A *minimal* superkey (remove any attribute :math:`\Rightarrow` loses uniqueness)
        - :math:`\{` ``person_id`` :math:`\}` is the only candidate key of ``PERSON``
      * - **Primary Key**
        - The candidate key chosen by the designer
        - ``person_id``
      * - **Alternate Key**
        - Candidate keys *not* chosen as PK (enforced with UNIQUE)
        - ``student_id`` in ``STUDENT`` (UNIQUE constraint)
      * - **Foreign Key**
        - References another table's PK
        - ``COURSE``.``dept_id`` :math:`\to` ``DEPARTMENT``.``dept_id``


   Orthogonal Key Properties
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~

   Keys can also be classified along two independent axes:

   .. list-table::
      :widths: 20 15 35 30
      :header-rows: 1
      :class: compact-table

      * - Axis
        - Options
        - Description
        - Example
      * - **Composition**
        - Simple
        - Single attribute
        - ``person_id``
      * -
        - Composite
        - Multiple attributes together
        - (``course_id``, ``section_no``)
      * - **Origin**
        - Natural
        - Has real-world meaning
        - ``email``, ``ssn``, ``isbn``
      * -
        - Surrogate
        - System-generated, no business meaning
        - ``SERIAL``, ``UUID``

   Any key (PK, CK, AK, FK) can be simple or composite, natural or surrogate:

   - ``PERSON``.``person_id``: PK, simple, surrogate (``SERIAL``)
   - ``STUDENT``.``student_id``: AK, simple, natural (business identifier, enforced with UNIQUE)
   - ``COURSE_SECTION``.(``course_id``, ``section_no``): PK, composite, natural
   - ``ENROLLMENT``.(``student_person_id``, ``course_id``, ``section_no``): PK, composite (all three components are also FKs)

   .. warning::

      **Surrogate vs. Natural**: Prefer surrogate PKs for stability (they never change). Use natural keys as alternate keys with ``UNIQUE`` constraints. **Exception**: junction tables, where composite natural keys (the FK pairs) are the correct PK.


.. dropdown:: Foreign Keys and Referential Integrity
   :class-container: sd-border-secondary

   A **foreign key** is an attribute (or set of attributes) in one table that references the **primary key** of another table. It establishes and enforces a link between two relations.

   - **Referential integrity constraint**: Every FK value must either match an existing PK value in the referenced table or be ``NULL`` (if the FK is nullable). Formally, for FK attribute :math:`F` in relation :math:`R_1` referencing PK :math:`K` in relation :math:`R_2`:

     .. math::

        \forall\, t \in R_1 :\; t[F] \in \pi_K(R_2) \;\cup\; \{\texttt{NULL}\}

   - A FK can reference any candidate key (PK or AK with ``UNIQUE``), though referencing the PK is standard practice
   - FKs can be part of the PK (e.g., in junction tables and weak entity tables)
   - **FK names need not match the referenced PK name.** They must share the same *domain* (data type), but the column names are independent. Descriptive FK names clarify the role of the relationship.

   .. list-table::
      :widths: 30 25 45
      :header-rows: 1
      :class: compact-table

      * - FK Column
        - References
        - Why the Name Differs
      * - ``STUDENT``.``advisor_person_id``
        - ``PROFESSOR`` (``person_id``)
        - Clarifies the *role* (advisor)
      * - ``COURSE_PREREQ``.``prereq_id``
        - ``COURSE`` (``course_id``)
        - Distinguishes from the other FK
      * - ``TA_ASSIGNMENT``.``grad_person_id``
        - ``GRAD_STUDENT`` (``person_id``)
        - Identifies which participant
      * - ``DEPARTMENT``.``chair_id``
        - ``PROFESSOR`` (``person_id``)
        - Names the :math:`1{:}1` relationship

   .. tip::

      **Naming convention**: A common pattern is ``role_referenced_pk``, e.g., ``advisor_person_id``. This is especially important when a table has **multiple FKs to the same table** (e.g., both ``successor_id`` and ``prereq_id`` reference ``COURSE``).


   FK Varieties and Cascade Behavior
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Simple FK**: Single column referencing a single-column PK (e.g., ``COURSE``.``dept_id`` :math:`\to` ``DEPARTMENT``.``dept_id``)
   - **Composite FK**: Multiple columns referencing a composite PK (e.g., ``ENROLLMENT``.(``course_id``, ``section_no``) :math:`\to` ``COURSE_SECTION``.(``course_id``, ``section_no``))
   - **Self-referencing FK**: FK that references the PK of the *same* table (e.g., ``COURSE_PREREQ``.``prereq_id`` :math:`\to` ``COURSE``.``course_id``)

   .. list-table::
      :widths: 25 30 45
      :header-rows: 1
      :class: compact-table

      * - Option (SQL)
        - Behavior
        - University Example
      * - ``ON DELETE CASCADE``
        - Delete children automatically
        - Deleting a course deletes its sections
      * - ``ON DELETE SET NULL``
        - Set FK to ``NULL``
        - Advisor leaves; student's advisor becomes ``NULL``
      * - ``ON DELETE RESTRICT``
        - Prevent parent deletion
        - Cannot delete a department with active courses
      * - ``ON UPDATE CASCADE``
        - Propagate PK changes to children
        - If ``dept_id`` changes, all referencing rows update

   .. card::
       :class-card: sd-border-info

       **The mapping algorithm (next section) converts conceptual relationships into FK constraints.** Every :math:`1{:}N` becomes a FK on the "many" side; every :math:`M{:}N` becomes a junction table with two FKs. Cascade behavior is chosen based on the semantics: weak entities typically use ``CASCADE``, optional relationships use ``SET NULL``, and critical references use ``RESTRICT``.


.. dropdown:: Relationship Types in the Relational Model
   :class-container: sd-border-secondary

   In L2 we modeled relationships with diamonds and cardinality labels. In the relational model, relationships are implemented through **foreign keys** and **junction tables**:

   .. list-table::
      :widths: 15 25 30 30
      :header-rows: 1
      :class: compact-table

      * - Type
        - Chen (L2)
        - Relational (L3)
        - Example
      * - One-to-One (:math:`1{:}1`)
        - Diamond with :math:`1` on each side
        - FK with ``UNIQUE`` on one side
        - ``PROFESSOR`` <-> ``DEPARTMENT`` (chairs)
      * - One-to-Many (:math:`1{:}N`)
        - Diamond with :math:`1` and :math:`N`
        - FK on the "many" side
        - ``DEPARTMENT`` -> ``COURSE``
      * - Many-to-Many (:math:`M{:}N`)
        - Diamond with :math:`M` and :math:`N`
        - Junction table with two FKs
        - ``STUDENT`` <-> ``COURSE_SECTION``

   .. important::

      **Key insight**: The relational model has **no native concept of relationships**. It only has tables and foreign keys. Every relationship must be "flattened" into this structure. This is precisely what the 7-step mapping algorithm does.


.. dropdown:: Table Design Best Practices
   :class-container: sd-border-secondary

   Principles of Good Table Design
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - **Atomicity**: Every column stores indivisible values. Store ``first_name`` and ``last_name`` separately, not a combined "name" field. No comma-separated lists. (This is also 1NF, covered in L4.)
   - **Avoid redundancy**: Each fact should be stored *once*. If a department name appears in 500 course rows, it should live in a ``DEPARTMENT`` table instead, referenced by FK.
   - **Meaningful names**: Use descriptive, consistent table and column names (e.g., ``enrollment_date``, not ``d1`` or ``date``).
   - **Choose keys wisely**: Prefer surrogate keys (auto-increment integers or UUIDs) over natural keys. Natural keys may change (e.g., email or SSN) or not be truly unique (e.g., names).
   - **Enforce constraints**: Use ``NOT NULL``, ``UNIQUE``, ``CHECK``, and ``FOREIGN KEY`` constraints to catch bad data at the database level, not just in application code.


   Three Common Table Design Pitfalls
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   1. **Unnecessary duplication.** Storing a customer's address in both the ``CUSTOMER`` and ``ORDER`` tables instead of linking via FK. Leads to update anomalies (change address in one place, forget the other), increased storage, and maintenance headaches. **Fix**: Normalize. Store shared data once, reference with FKs.

   2. **Poorly chosen keys.** Using a person's name as a PK (names are not unique, and they change). Using long composite natural keys when a simple surrogate would suffice. **Fix**: Use simple, non-changing, unique keys: auto-increment integers or UUIDs.

   3. **Improper or missing relationships.** Orders without a FK to customers lead to orphaned records. Missing ``ON DELETE`` behavior causes dangling references. :math:`M{:}N` relationships stored as comma-separated lists instead of junction tables. **Fix**: Clearly define :math:`1{:}1`, :math:`1{:}N`, :math:`M{:}N` and enforce with FKs and cascade rules.




The 7-Step Mapping Algorithm
====================================================


.. dropdown:: Algorithm Overview
   :class-container: sd-border-secondary
   :open:

   A systematic procedure to convert any EER diagram into relational schemas, based on Elmasri and Navathe.

   .. list-table::
      :widths: 8 15 77
      :header-rows: 1
      :class: compact-table

      * - Step
        - Input
        - Output
      * - 1
        - Strong entities
        - One table per entity; PK = key attribute(s); composite :math:`\to` flattened; derived :math:`\to` omit
      * - 2
        - Weak entities
        - Table with PK = owner PK + partial key; FK :math:`\to` owner with ``CASCADE``
      * - 3
        - Binary :math:`1{:}1`
        - FK on one side (prefer total participation side); ``UNIQUE`` on FK
      * - 4
        - Binary :math:`1{:}N`
        - FK on the "many" side pointing to the "one" side
      * - 5
        - Binary :math:`M{:}N`
        - New junction table; PK = composite of both FKs; relationship attrs become columns
      * - 6
        - Multivalued attrs
        - New table with FK :math:`\to` owner; PK = FK + attribute value
      * - 7
        - :math:`n`-ary rels
        - New table with FK to each participant; PK depends on cardinality

   .. note::

      ISA hierarchies and categories are sometimes listed as Steps 8 and 9 in extended treatments. We cover them separately after the core 7 steps.


.. dropdown:: Step 1: Strong Entity Types
   :class-container: sd-border-secondary

   Map Each Strong Entity to a Table
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: For each strong entity type :math:`E`, create a relation :math:`R` with all **simple attributes**. Choose one candidate key as the **primary key**.

   Handling Attribute Types
   ^^^^^^^^^^^^^^^^^^^^^^^^^

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Attribute Type
        - Mapping Rule
      * - Simple (atomic)
        - Direct column in :math:`R`
      * - Composite
        - Flatten: include only leaf sub-attributes. E.g., name :math:`\to` ``first_name``, ``middle_name``, ``last_name``
      * - Derived
        - Omit (compute at query time) or mark as generated/virtual column
      * - Multivalued
        - Do **not** include. Handled in Step 6
      * - Key
        - Mark as ``PRIMARY KEY`` (PK)


   University Example
   ^^^^^^^^^^^^^^^^^^^

   .. list-table::
      :widths: 15 85
      :header-rows: 1
      :class: compact-table

      * - Entity
        - Resulting Table
      * - ``PERSON``
        - ``PERSON`` (``person_id``, ``first_name``, ``middle_name``, ``last_name``, ``date_of_birth``, ``street``, ``city``, ``state``, ``zip``)
      * - ``DEPARTMENT``
        - ``DEPARTMENT`` (``dept_id``, ``dept_name``, ``building``, ``budget``)
      * - ``COURSE``
        - ``COURSE`` (``course_id``, ``title``, ``credits``, ``level``)
      * - ``ROOM``
        - ``ROOM`` (``room_id``, ``building``, ``room_number``, ``capacity``, ``room_type``)


   .. only:: html

      .. figure:: /_static/images/l3/strong-entity-light.png
         :alt: Mapping the Person entity
         :width: 90%
         :align: center
         :class: only-light

         **Mapping the PERSON entity**: Chen attributes are flattened into table columns. Composite attribute ``name`` becomes ``first_name``, ``middle_name``, ``last_name``. Multivalued attributes (phone_numbers, email_addresses) are deferred to Step 6.

      .. figure:: /_static/images/l3/strong-entity-dark.png
         :alt: Mapping the Person entity
         :width: 90%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/strong-entity-light.png
         :alt: Mapping the Person entity
         :width: 90%
         :align: center

         **Mapping the PERSON entity**: Chen attributes are flattened into table columns. Composite attribute ``name`` becomes ``first_name``, ``middle_name``, ``last_name``. Multivalued attributes (phone_numbers, email_addresses) are deferred to Step 6.


   Lookup Tables (The Enum Pattern)
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   Some strong entities exist solely to constrain a column to a **fixed set of valid values**. These are called **lookup tables** (also known as reference tables or code tables). They serve the same purpose as an enum in programming languages, but at the database level.

   **Why not just use a CHECK constraint?**

   - A ``CHECK`` constraint works for simple cases: ``CHECK (rank IN ('ASST','ASSOC','FULL','EMER'))``
   - But a lookup table is better when:

     - You need **metadata** per value (display name, sort order, description)
     - The valid set may **grow** over time (adding a row vs. altering the schema)
     - **Multiple tables** reference the same set of values
     - You want **FK enforcement** rather than a string-based check


   University Example: ACADEMIC_RANK
   """"""""""""""""""""""""""""""""""

   .. list-table::
      :widths: 25 40 35
      :header-rows: 1
      :class: compact-table

      * - rank_code
        - rank_name
        - rank_order
      * - ASST
        - Assistant Professor
        - 1
      * - ASSOC
        - Associate Professor
        - 2
      * - FULL
        - Full Professor
        - 3
      * - EMER
        - Professor Emeritus
        - 4

   - ``rank_code``: short mnemonic used as PK and referenced by FKs
   - ``rank_name``: human-readable display name (enforced ``UNIQUE``)
   - ``rank_order``: enables sorting by seniority without relying on alphabetical order


   How Lookup Tables Connect
   """""""""""""""""""""""""""

   .. only:: html

      .. figure:: /_static/images/l3/lookup-academic-rank-light.png
         :alt: Crow's Foot diagram showing Professor referencing Academic_Rank
         :width: 60%
         :align: center
         :class: only-light

         **Crow's Foot**: ``PROFESSOR`` references the ``ACADEMIC_RANK`` lookup table

      .. figure:: /_static/images/l3/lookup-academic-rank-dark.png
         :alt: Crow's Foot diagram showing Professor referencing Academic_Rank
         :width: 60%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/lookup-academic-rank-light.png
         :alt: Crow's Foot diagram showing Professor referencing Academic_Rank
         :width: 60%
         :align: center

         **Crow's Foot**: ``PROFESSOR`` references the ``ACADEMIC_RANK`` lookup table

   ``PROFESSOR``.``rank_code`` is a FK referencing ``ACADEMIC_RANK``.``rank_code``. This is a standard :math:`1{:}N` relationship: one rank applies to many professors, but each professor has exactly one rank.

   - Every ``rank_code`` value in ``PROFESSOR`` must exist in ``ACADEMIC_RANK``
   - Inserting a professor with ``rank_code`` = 'ADJUNCT' **fails** unless that code is first added to the lookup table
   - Multiple professors can share the same rank (no ``UNIQUE`` on the FK)


   Other Lookup Table Candidates
   """""""""""""""""""""""""""""""

   .. list-table::
      :widths: 25 25 50
      :header-rows: 1
      :class: compact-table

      * - Column
        - Current Approach
        - Lookup Table Alternative
      * - ``STUDENT``.``acad_standing``
        - ``CHECK`` constraint
        - ``ACADEMIC_STANDING`` (``standing_code``, ``standing_name``, ``description``)
      * - ``COURSE``.``level``
        - Free-text varchar
        - ``COURSE_LEVEL`` (``level_code``, ``level_name``, ``level_order``)
      * - ``INTL_STUDENT``.``visa_type``
        - Free-text varchar
        - ``VISA_TYPE`` (``visa_code``, ``visa_name``, ``max_duration``)
      * - ``ROOM``.``room_type``
        - Free-text varchar
        - ``ROOM_TYPE`` (``type_code``, ``type_name``, ``has_projector``)

   .. card::
       :class-card: sd-border-info

       **When to use a lookup table vs. a CHECK constraint**: If the set of values is small, stable, and needs no metadata, a ``CHECK`` constraint is sufficient. If you need display names, sort order, descriptions, or expect the set to grow, promote it to a lookup table. In our university model, we use a lookup table for ``ACADEMIC_RANK`` and ``CHECK`` constraints for the others, but either approach is valid.


.. dropdown:: Step 2: Weak Entity Types
   :class-container: sd-border-secondary

   Map Each Weak Entity to a Table
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: For each weak entity :math:`W` with owner entity :math:`E`:

   - Create table :math:`R_W` with all simple attributes of :math:`W`
   - Include the **PK of owner** :math:`E` as a foreign key
   - **PK of** :math:`R_W` = owner's PK + partial key (discriminator)


   University Example: COURSE_SECTION (owned by COURSE)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. only:: html

      .. figure:: /_static/images/l3/weak-entity-light.png
         :alt: Mapping weak entities from Chen to Crow's Foot
         :width: 100%
         :align: center
         :class: only-light

         **Mapping weak entities**: Chen (left) to Crow's Foot (right)

      .. figure:: /_static/images/l3/weak-entity-dark.png
         :alt: Mapping weak entities from Chen to Crow's Foot
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/weak-entity-light.png
         :alt: Mapping weak entities from Chen to Crow's Foot
         :width: 80%
         :align: center

         **Mapping weak entities**: Chen (left) to Crow's Foot (right)

   ``COURSE_SECTION`` (``course_id``, ``section_no``, ``semester``, ``year``, ``capacity``, ``schedule``)

   - ``course_id``: used both as PK *and* FK (referencing ``COURSE``.``course_id``)
   - ``section_no``: partial key (discriminator)
   - Together, (``course_id``, ``section_no``) uniquely identifies each section

   .. important::

      **Key point**: The identifying relationship (double diamond in Chen) does **not** produce a separate table. It is absorbed into the weak entity's table through the owner's PK.


.. dropdown:: Step 3: Binary :math:`1{:}1` Relationships
   :class-container: sd-border-secondary

   Map Binary :math:`1{:}1` Relationships
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: Three options depending on participation:

   .. list-table::
      :widths: 15 30 55
      :header-rows: 1
      :class: compact-table

      * - Option
        - When to Use
        - How
      * - **A:** FK on one side
        - One side total, other partial
        - FK on the **total** side (no ``NULL`` s). Add ``UNIQUE``
      * - **B:** Merge tables
        - Both sides total, few attrs
        - Combine into one table
      * - **C:** Cross-reference
        - Both sides partial
        - FK on either side (``UNIQUE``); ``NULL`` s unavoidable


   .. tab-set::

      .. tab-item:: Option A: FK on Total Side

         .. only:: html

            .. figure:: /_static/images/l3/1-1-A-light.png
               :alt: Option A for 1:1 mapping with FK on total participation side
               :width: 100%
               :align: center
               :class: only-light

               **Option A**: FK on the total participation side. Chen (top) to Crow's Foot (bottom).

            .. figure:: /_static/images/l3/1-1-A-dark.png
               :alt: Option A for 1:1 mapping with FK on total participation side
               :width: 100%
               :align: center
               :class: only-dark

         .. only:: latex

            .. figure:: /_static/images/l3/1-1-A-light.png
               :alt: Option A for 1:1 mapping with FK on total participation side
               :width: 80%
               :align: center

               **Option A**: FK on the total participation side. Chen (top) to Crow's Foot (bottom).

         ``PROFESSOR`` :math:`(0,1)` -- ``CHAIRS`` -- :math:`(1,1)` ``DEPARTMENT``. ``DEPARTMENT`` has **total** participation, so the FK goes there.

         - ``chair_id`` FK :math:`\to` ``PROFESSOR`` (``person_id``). ``NOT NULL``: every department *must* have a chair (total participation). ``UNIQUE``: no professor can chair two departments (enforces 1:1).
         - ``start_date`` migrates into ``DEPARTMENT`` alongside the FK. In Option A, relationship attributes always follow the FK to the total side.
         - Result: 3 department rows, **zero NULLs**. Compare with the alternative where the FK on the partial side produces 62% NULLs.

         .. dropdown:: Why place the FK on the total side? (Counterexample)
            :class-container: sd-border-warning

            **Bad choice: FK on the partial side (PROFESSOR)**

            Placing FK (``chairs_dept_id`` :math:`\to` ``DEPARTMENT``.``dept_id``) on ``PROFESSOR`` means most professors are **not** chairs, so the column is mostly ``NULL``.

            .. list-table::
               :widths: 10 10 10 12 12 15 15 16
               :header-rows: 1
               :class: compact-table

               * - person_id
                 - professor_id
                 - rank_code
                 - salary
                 - hire_date
                 - start_date
                 - chairs_dept_id
               * - 101
                 - P001
                 - FULL
                 - 95000
                 - 2015-08-15
                 - NULL
                 - NULL
               * - 102
                 - P002
                 - ASSOC
                 - 88000
                 - 2018-01-10
                 - NULL
                 - NULL
               * - 103
                 - P003
                 - ASSOC
                 - 92000
                 - 2016-06-01
                 - 2022-09-01
                 - CS
               * - 104
                 - P004
                 - ASST
                 - 87000
                 - 2019-08-20
                 - NULL
                 - NULL
               * - 105
                 - P005
                 - FULL
                 - 91000
                 - 2017-01-15
                 - 2023-07-01
                 - EE
               * - 106
                 - P006
                 - ASST
                 - 85000
                 - 2020-08-25
                 - NULL
                 - NULL
               * - 107
                 - P007
                 - EMER
                 - 99000
                 - 2014-01-10
                 - 2021-06-01
                 - ME
               * - 108
                 - P008
                 - ASST
                 - 86000
                 - 2021-08-15
                 - NULL
                 - NULL

            *PROFESSOR table with FK on the partial side (bad). Only 3 of 8 professors are chairs, so both start_date and chairs_dept_id are NULL for 62% of rows.*

            This wastes storage, complicates queries with ``NULL``-handling logic (``IS NULL``, ``COALESCE``), and makes the table harder to read.

            **Correct choice: FK on the total side (DEPARTMENT)**

            .. list-table::
               :widths: 10 25 20 20 15 10
               :header-rows: 1
               :class: compact-table

               * - dept_id
                 - dept_name
                 - building
                 - budget
                 - start_date
                 - chair_id
               * - CS
                 - Computer Science
                 - A.V. Williams
                 - 2,500,000
                 - 2022-09-01
                 - 103
               * - EE
                 - Electrical Engineering
                 - Kim Building
                 - 1,800,000
                 - 2023-07-01
                 - 105
               * - ME
                 - Mechanical Engineering
                 - Glenn L. Martin
                 - 2,100,000
                 - 2021-06-01
                 - 107

            *DEPARTMENT table with FK on the total side (correct). Every value is non-NULL and unique. Zero NULLs.*

         .. card::
             :class-card: sd-border-success

             **Rule**: In a :math:`1{:}1` relationship, always place the FK on the **total participation** side. If both sides are total, either side works (or merge the tables). If both sides are partial, ``NULL`` s are unavoidable; pick the side with fewer ``NULL`` s.


      .. tab-item:: Option B: Merge Tables

         .. only:: html

            .. figure:: /_static/images/l3/1-1-B-light.png
               :alt: Option B for 1:1 mapping by merging tables
               :width: 100%
               :align: center
               :class: only-light

               **Option B**: Merging two entities into one table. Chen (top) to Crow's Foot (bottom).

            .. figure:: /_static/images/l3/1-1-B-dark.png
               :alt: Option B for 1:1 mapping by merging tables
               :width: 100%
               :align: center
               :class: only-dark

         .. only:: latex

            .. figure:: /_static/images/l3/1-1-B-light.png
               :alt: Option B for 1:1 mapping by merging tables
               :width: 80%
               :align: center

               **Option B**: Merging two entities into one table. Chen (top) to Crow's Foot (bottom).

         *Note: This example uses an Employee/Passport use case (not our university model) to illustrate Option B clearly.*

         ``EMPLOYEE`` :math:`(1,1)` -- ``HAS`` -- :math:`(1,1)` ``PASSPORT``. Both sides have **total** participation and ``PASSPORT`` has only two attributes, so we merge both entities into a single table.

         - No FK needed: both entities share the same table
         - ``emp_id`` remains the sole PK
         - ``passport_no`` is demoted from PK to ``UNIQUE`` (alternate key)
         - ``expiry_date`` is absorbed as a regular column

         .. list-table::
            :widths: 12 15 15 15 18 15
            :header-rows: 1
            :class: compact-table

            * - emp_id
              - first_name
              - last_name
              - hire_date
              - passport_no
              - expiry_date
            * - 201
              - Alice
              - Smith
              - 2018-03-01
              - US1234567
              - 2028-06-15
            * - 202
              - Bob
              - Jones
              - 2019-07-10
              - US2345678
              - 2029-11-20
            * - 203
              - Carlos
              - Garcia
              - 2020-01-15
              - US3456789
              - 2030-04-10
            * - 204
              - Diana
              - Lee
              - 2021-09-01
              - US4567890
              - 2031-08-25

         *Merged EMPLOYEE table. UNIQUE on passport_no enforces* :math:`1{:}1` *cardinality.*


      .. tab-item:: Option C: Cross-Reference

         *Another non-university example.* Both sides have **partial** participation: not every employee has a parking spot, and not every spot is assigned.

         - ``NULL`` s are **unavoidable** regardless of which side holds the FK
         - The FK must be ``UNIQUE`` (:math:`1{:}1` cardinality) but **nullable** (partial participation)
         - **Strategy**: Place the FK on the side with fewer ``NULL`` s

         .. only:: html

            .. figure:: /_static/images/l3/1-1-C-light.png
               :alt: Option C for 1:1 mapping with both sides partial
               :width: 100%
               :align: center
               :class: only-light

               **FK on PARKING_SPOT or on EMPLOYEE?**

            .. figure:: /_static/images/l3/1-1-C-dark.png
               :alt: Option C for 1:1 mapping with both sides partial
               :width: 100%
               :align: center
               :class: only-dark

         .. only:: latex

            .. figure:: /_static/images/l3/1-1-C-light.png
               :alt: Option C for 1:1 mapping with both sides partial
               :width: 90%
               :align: center

               **FK on PARKING_SPOT or on EMPLOYEE?**

         Comparing the two placements: FK on ``EMPLOYEE`` produces :math:`4/8` ``NULL`` s (50%), while FK on ``PARKING_SPOT`` produces :math:`2/6` ``NULL`` s (33%).

         .. card::
             :class-card: sd-border-warning

             **Better choice**: FK on ``PARKING_SPOT`` (33% vs. 50% ``NULL`` s). With both sides partial, ``NULL`` s are unavoidable. Always pick the side with the **higher assignment ratio** to minimize them.


.. dropdown:: Step 4: Binary :math:`1{:}N` Relationships
   :class-container: sd-border-secondary

   Map Binary :math:`1{:}N` Relationships
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: Add the PK of the "one" side as a **FK on the "many" side**. Relationship attributes also go on the "many" side. Total participation :math:`\Rightarrow` ``NOT NULL``; partial :math:`\Rightarrow` nullable.

   University Example
   ^^^^^^^^^^^^^^^^^^^^

   ``PROFESSOR`` :math:`(1,1)` -- ``BELONGS_TO`` -- :math:`(1,N)` ``DEPARTMENT``. Each professor belongs to exactly one department; a department has one or more professors.

   - Place FK on the :math:`N`-side (``PROFESSOR``): ``dept_id`` references ``DEPARTMENT``.``dept_id``
   - ``dept_id`` is constrained ``NOT NULL`` because ``PROFESSOR`` has **total** participation
   - No ``UNIQUE`` constraint: multiple professors can reference the same department
   - Any relationship attributes would also migrate to ``PROFESSOR``

   .. only:: html

      .. figure:: /_static/images/l3/1-N-light.png
         :alt: Mapping 1:N relationships
         :width: 100%
         :align: center
         :class: only-light

         **Mapping :math:`1{:}N` relationships**: FK on the "many" side

      .. figure:: /_static/images/l3/1-N-dark.png
         :alt: Mapping 1:N relationships
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/1-N-light.png
         :alt: Mapping 1:N relationships
         :width: 60%
         :align: center

         **Mapping :math:`1{:}N` relationships**: FK on the "many" side


   .. dropdown:: Why not put the FK on the "one" side? (Counterexample)
      :class-container: sd-border-warning

      Storing professor references inside ``DEPARTMENT`` would require multiple values in one cell:

      .. list-table::
         :widths: 10 30 10 50
         :header-rows: 1
         :class: compact-table

         * - dept_id
           - dept_name
           - ...
           - professor_ids
         * - CS
           - Computer Science
           - ...
           - {101, 102, 107}
         * - EE
           - Electrical Engineering
           - ...
           - {103, 104, 108}
         * - ME
           - Mechanical Engineering
           - ...
           - {105, 106}

      *DEPARTMENT table with multi-valued FK (violates 1NF).*

      The ``professor_ids`` column stores a **set of values** in a single cell. This violates **First Normal Form (1NF)**: every attribute must hold exactly one atomic value. You also cannot enforce referential integrity, index efficiently, or join cleanly on a list inside a cell.

      **Correct approach**: Each professor row stores a single FK value.

      .. list-table::
         :widths: 15 15 15 15 15
         :header-rows: 1
         :class: compact-table

         * - person_id
           - professor_id
           - rank_code
           - ...
           - dept_id
         * - 201
           - P001
           - FULL
           - ...
           - CS
         * - 202
           - P002
           - ASSOC
           - ...
           - CS
         * - 203
           - P003
           - ASST
           - ...
           - EE
         * - 204
           - P004
           - ASST
           - ...
           - EE
         * - 205
           - P005
           - FULL
           - ...
           - ME
         * - 206
           - P006
           - ASSOC
           - ...
           - CS

      *PROFESSOR table: every row has a single, non-null dept_id. Atomic, 1NF compliant, indexable, joinable.*


.. dropdown:: Step 5: Binary :math:`M{:}N` Relationships
   :class-container: sd-border-secondary

   Map Binary :math:`M{:}N` Relationships
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: Create a **junction table** (also called a **bridge** or **associative** table) to represent the :math:`M{:}N` relationship.

   - Unlike :math:`1{:}1` or :math:`1{:}N`, there is **no way** to represent :math:`M{:}N` with a simple FK on either side
   - Each row in the junction table represents one pairing between the two entities

   Building the Junction Table
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - **Primary key**: The composite PK is formed by combining the PKs of both participating entities.
   - **Foreign keys**: Each component of the composite PK is also an FK referencing its source entity. These are inherently ``NOT NULL`` since they form the PK.
   - **Relationship attributes**: Any attributes that belong to the relationship (not to either entity alone) are moved into the junction table as additional columns.

   .. important::

      A relationship attribute like ``grade`` only has meaning when *both* entities are known. Asking "What is the grade?" makes no sense without specifying which student *and* which course section.


   Example: STUDENT -- ENROLLS_IN -- COURSE_SECTION
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A student enrolls in many course sections; a course section has many students.

   .. only:: html

      .. figure:: /_static/images/l3/M-N-student-light.png
         :alt: Mapping M:N relationships with a junction table
         :width: 100%
         :align: center
         :class: only-light

         **Mapping :math:`M{:}N` relationships with a junction table** (``ENROLLMENT``)

      .. figure:: /_static/images/l3/M-N-student-dark.png
         :alt: Mapping M:N relationships with a junction table
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/M-N-student-light.png
         :alt: Mapping M:N relationships with a junction table
         :width: 90%
         :align: center

         **Mapping :math:`M{:}N` relationships with a junction table** (``ENROLLMENT``)


   Example: COURSE Prerequisites (Recursive M:N)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A course can have many prerequisites; a course can be a prerequisite for many others. This is a **recursive** :math:`M{:}N` relationship on the same entity.

   .. only:: html

      .. figure:: /_static/images/l3/M-N-course-light.png
         :alt: Mapping recursive M:N with a junction table
         :width: 100%
         :align: center
         :class: only-light

         **Mapping recursive M:N** with a junction table (``COURSE_PREREQ``)

      .. figure:: /_static/images/l3/M-N-course-dark.png
         :alt: Mapping recursive M:N with a junction table
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/M-N-course-light.png
         :alt: Mapping recursive M:N with a junction table
         :width: 80%
         :align: center

         **Mapping recursive M:N** with a junction table (``COURSE_PREREQ``)

   - PK = (``successor_id``, ``prereq_id``)
   - Both FKs reference ``COURSE`` (``course_id``), but play different roles: ``successor_id`` is the course that requires the prerequisite; ``prereq_id`` is the course that must be completed first
   - Add ``CHECK`` (``successor_id`` :math:`\neq` ``prereq_id``) to prevent a course from being its own prerequisite

   .. warning::

      **Recursive** :math:`M{:}N` **:** The same table appears on both sides of the relationship. Use distinct column names (``successor_id`` vs. ``prereq_id``) to distinguish the two roles.


.. dropdown:: Step 6: Multivalued Attributes
   :class-container: sd-border-secondary

   Map Multivalued Attributes
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: For each multivalued attribute :math:`A` of entity :math:`E`: create a new table with PK = (FK to :math:`E` + attribute value). If composite+multivalued, include all leaf sub-attributes.

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Multivalued Attribute
        - Resulting Table
      * - ``phone_numbers`` (``PERSON``)
        - ``PERSON_PHONE`` (``person_id``, ``phone_number``). FK: ``person_id`` :math:`\to` ``PERSON``
      * - ``specializations`` (``PROFESSOR``)
        - ``PROF_SPECIALIZATION`` (``person_id``, ``specialization``). FK: ``person_id`` :math:`\to` ``PROFESSOR``
      * - ``previous_degrees`` (``STUDENT``)
        - ``STUDENT_DEGREE`` (``person_id``, ``degree_type``, ``institution``, ``year``). FK: ``person_id`` :math:`\to` ``STUDENT``; composite + multivalued

   .. only:: html

      .. figure:: /_static/images/l3/multivalued-attribute-light.png
         :alt: Mapping multivalued and composite-multivalued attributes
         :width: 100%
         :align: center
         :class: only-light

         **Mapping multivalued and composite-multivalued attributes**

      .. figure:: /_static/images/l3/multivalued-attribute-dark.png
         :alt: Mapping multivalued and composite-multivalued attributes
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/multivalued-attribute-light.png
         :alt: Mapping multivalued and composite-multivalued attributes
         :width: 90%
         :align: center

         **Mapping multivalued and composite-multivalued attributes**

   .. card::
       :class-card: sd-border-warning

       **Why not comma-separated strings?** Violates 1NF (atomicity). Cannot be efficiently queried, indexed, or constrained. Always use a separate table.


   .. dropdown:: Why year is not in the STUDENT_DEGREE PK (Deep Dive)
      :class-container: sd-border-info

      If the PK were (``person_id``, ``degree_type``, ``institution``, ``year``), the table would allow rows that should not exist: a student with two separate M.S. degrees from the same institution in different years, which is almost certainly a data entry error, not a legitimate record.

      **Correct PK**: (``person_id``, ``degree_type``, ``institution``). This enforces one degree of each type per institution per student. If a student's graduation year changes (e.g., delayed), use ``UPDATE``, not a second row.

      **Rule**: Only include attributes in the PK if different values represent genuinely **different real-world entities**. A change in ``year`` does not create a new degree; it corrects an existing one.


.. dropdown:: Step 7: :math:`n`-ary Relationships
   :class-container: sd-border-secondary

   Map :math:`n`-ary (Ternary+) Relationships
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Rule**: Create a new table with FKs to each participant. PK typically includes all FKs unless cardinality allows simplification.


   TA_ASSIGN (Ternary: GRAD_STUDENT, COURSE_SECTION, PROFESSOR)
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   ``TA_ASSIGNMENT`` (``course_id``, ``section_no``, ``grad_person_id``, ``professor_person_id``)

   - (``course_id``, ``section_no``) FK :math:`\to` ``COURSE_SECTION``
   - ``grad_person_id`` FK :math:`\to` ``GRAD_STUDENT`` (``person_id``), ``NOT NULL``
   - ``professor_person_id`` FK :math:`\to` ``PROFESSOR`` (``person_id``), ``NOT NULL``
   - PK = (``course_id``, ``section_no``)
   - Each section has exactly one TA and one supervising professor, so both are functionally determined by the section

   .. only:: html

      .. figure:: /_static/images/l3/n-ary-light.png
         :alt: Mapping the TA_ASSIGN ternary relationship
         :width: 100%
         :align: center
         :class: only-light

         **Mapping TA_ASSIGN** (Ternary: ``GRAD_STUDENT``, ``PROFESSOR``, ``COURSE_SECTION``)

      .. figure:: /_static/images/l3/n-ary-dark.png
         :alt: Mapping the TA_ASSIGN ternary relationship
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/n-ary-light.png
         :alt: Mapping the TA_ASSIGN ternary relationship
         :width: 90%
         :align: center

         **Mapping TA_ASSIGN** (Ternary: ``GRAD_STUDENT``, ``PROFESSOR``, ``COURSE_SECTION``)


   .. dropdown:: PK choice in :math:`n`-ary tables (Deep Dive)
      :class-container: sd-border-info

      Do not blindly include all FKs in the PK. Ask: "Can this participant appear more than once for the same combination of the other key columns?" If yes, include it in the PK. If no, leave it as a non-key ``NOT NULL`` FK.

      **What goes wrong if we add grad_person_id to the PK?** The PK becomes (``course_id``, ``section_no``, ``grad_person_id``), which would allow a section to have **two TAs** (two rows with different ``grad_person_id`` values). With PK = (``course_id``, ``section_no``) only, the table enforces that each section appears **at most once**, guaranteeing exactly one TA and one supervising professor.


.. dropdown:: Transformation Summary
   :class-container: sd-border-secondary

   Chen to Crow's Foot: What Disappears, What Appears
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 25 30 45
      :header-rows: 1
      :class: compact-table

      * - Chen Construct
        - Disappears
        - Replaced By (Crow's Foot)
      * - Entity rectangle
        - Stays (becomes table box)
        - Table with columns listed
      * - Attribute ovals
        - All ovals
        - Rows inside table box
      * - Relationship diamond
        - Diamond shape
        - FK column + line between tables
      * - Double diamond (identifying)
        - Diamond + double lines
        - Composite PK with FK component
      * - Double oval (multivalued)
        - Oval
        - Separate table with FK
      * - Dashed oval (derived)
        - Oval
        - Omitted (computed at query time)
      * - Cardinality numbers
        - Numbers on lines
        - Fork/bar/circle at line ends
      * - ISA triangle
        - Triangle
        - Shared PK as FK between tables
      * - Category circle
        - Circle
        - Discriminator + exclusive nullable FKs

   .. card::
       :class-card: sd-border-info

       **The Crow's Foot model is simpler**: no diamonds, no ovals, no triangles. Everything is a table, every relationship is a FK, and every constraint is expressed as PK/FK/``UNIQUE``/``NOT NULL``/``CHECK``. This is why it is the industry standard for implementation-ready logical models.




Mapping ISA and Categories
====================================================


.. dropdown:: Step 8: ISA Mapping Strategies
   :class-container: sd-border-secondary
   :open:

   Strategy Comparison
   ~~~~~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 18 22 25 35
      :header-rows: 1
      :class: compact-table

      * - Strategy
        - Tables Created
        - Best When
        - Trade-off
      * - **A: Separate Tables**
        - Superclass + one per subclass (shared PK)
        - Overlapping or partial; shared queries on superclass
        - Requires ``JOIN``; more tables
      * - **B: Subclass Only**
        - One per subclass (no superclass table); includes inherited attrs
        - Disjoint + total; few shared queries
        - Duplicates superclass cols; ``UNION ALL`` for shared queries
      * - **C: Single Table**
        - One table + type discriminator column
        - Few subclasses, few distinct attrs; fast reads
        - Many ``NULL`` s; cannot enforce subclass-specific ``NOT NULL``

   .. card::
       :class-card: sd-border-info

       **No universally "best" strategy.** Choice depends on specialization constraints (disjoint/overlapping, total/partial), number of subclass-specific attributes, and query patterns. The flowchart below is a **starting point**; practical considerations (shared queries, data volume, application needs) may override it.


   Choosing the Right ISA Strategy
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. only:: html

      .. figure:: /_static/images/l3/strategy-selection-light.png
         :alt: ISA strategy decision flowchart
         :width: 100%
         :align: center
         :class: only-light

         **ISA strategy decision flowchart**

      .. figure:: /_static/images/l3/strategy-selection-dark.png
         :alt: ISA strategy decision flowchart
         :width: 100%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/strategy-selection-light.png
         :alt: ISA strategy decision flowchart
         :width: 60%
         :align: center

         **ISA strategy decision flowchart**

   How to Read the Flowchart
   ^^^^^^^^^^^^^^^^^^^^^^^^^^

   - Start with the specialization constraints (disjoint/overlapping, total/partial)
   - Consider the number of subclass-specific attributes
   - Factor in **shared queries**: how often does your application query across all subclasses at once? (e.g., "list all people with last name Smith")
   - If shared queries are frequent, prefer **Strategy A** regardless of other constraints

   .. tip::

      **Key insight**: Strategy A is the safest default. Strategies B and C are performance optimizations for specific scenarios where shared queries are rare.


   .. tab-set::

      .. tab-item:: Strategy A: Separate Tables

         For superclass :math:`S` with subclasses :math:`C_1, C_2, \ldots`:

         - Table for :math:`S`: all superclass attributes + PK
         - Table for each :math:`C_i`: only subclass-specific attributes
         - PK of each :math:`C_i` = PK of :math:`S` (also FK :math:`\to` :math:`S`)
         - Full entity = ``JOIN`` Ci with S on shared PK

      .. tab-item:: Strategy B: Subclass Only

         For superclass :math:`S` with subclasses :math:`C_1, C_2, \ldots`:

         - No table for :math:`S`
         - Table for each :math:`C_i`: *all* superclass attributes + subclass-specific attributes
         - Each :math:`C_i` table has its own copy of the PK
         - Cross-subclass query = ``UNION ALL`` across all :math:`C_i` tables
         - Only valid for **disjoint + total** (otherwise rows are lost or duplicated)

      .. tab-item:: Strategy C: Single Table

         For superclass :math:`S` with subclasses :math:`C_1, C_2, \ldots`:

         - One table containing all attributes from :math:`S, C_1, C_2, \ldots`
         - Add a **type discriminator** column (e.g., ``person_type``)
         - Subclass-specific attributes are ``NULL`` for rows of other types
         - Cannot enforce subclass-specific ``NOT NULL`` at the database level


.. dropdown:: University: Both ISA Hierarchies Use Strategy A
   :class-container: sd-border-secondary

   .. list-table::
      :widths: 15 85
      :header-rows: 1
      :class: compact-table

      * - Table
        - Schema
      * - ``PERSON``
        - (``person_id``, ``first_name``, ``middle_name``, ``last_name``, ``date_of_birth``, ``street``, ``city``, ``state``, ``zip``)
      * - ``STUDENT``
        - (``person_id``, ``student_id``, ``admission_date``, ``gpa``, ``acad_standing``, ``advisor_person_id``): PK/FK :math:`\to` ``PERSON``
      * - ``PROFESSOR``
        - (``person_id``, ``professor_id``, ``rank_code``, ``hire_date``, ``salary``, ``dept_id``): PK/FK :math:`\to` ``PERSON``
      * - ``GRAD_STUDENT``
        - (``person_id``, ``thesis_topic``): PK/FK :math:`\to` ``STUDENT``
      * - ``INTL_STUDENT``
        - (``person_id``, ``visa_type``, ``country_of_origin``, ``passport_number``, ``visa_expiration_date``): PK/FK :math:`\to` ``STUDENT``


   ISA1: PERSON :math:`\to` STUDENT / PROFESSOR (disjoint, total)
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - The flowchart says: disjoint + total with many subclass attrs :math:`\Rightarrow` Strategy B
   - **But**: We need the ``PERSON`` table for shared queries ("list all people with last name Smith"), phone numbers (``PERSON_PHONE`` references ``PERSON``), and the address attributes that both students and professors share
   - Eliminating ``PERSON`` would force us to ``UNION ALL`` across ``STUDENT`` and ``PROFESSOR`` for every cross-role query
   - **Decision**: Strategy A. The shared-query benefit outweighs the extra ``JOIN`` s.


   ISA2: STUDENT :math:`\to` GRAD_STUDENT / INTL_STUDENT (overlapping, partial)
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - The flowchart says: overlapping or partial :math:`\Rightarrow` Strategy A
   - **Overlapping**: A student can be both a grad student and an international student (rows in both subtables)
   - **Partial**: Not every student is a grad student or an international student (no row in either subtable)
   - Only Strategy A handles both correctly: subclass tables are optional extensions, not replacements

   .. card::
       :class-card: sd-border-success

       **Takeaway**: Strategy A is the safest general-purpose choice. It works for *any* combination of disjoint/overlapping and total/partial. Strategies B and C are performance optimizations you consider when A creates too many ``JOIN`` s.


.. dropdown:: Step 9: Mapping Categories (Union Types)
   :class-container: sd-border-secondary

   How to Map a Category
   ~~~~~~~~~~~~~~~~~~~~~~~

   A **category** (union type) is a subclass whose instances come from **multiple unrelated superclass hierarchies**. From L2: ``VEHICLE_OWNER`` is a category of ``PERSON`` :math:`\cup` ``COMPANY`` :math:`\cup` ``BANK``.

   *Note: This example is outside the university model. A vehicle can be owned by a person, a company, or a bank (repossession).*


   Why Categories Are Different from ISA
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   - In ISA, subclasses share a **common superclass** with a single PK
   - In a category, the superclasses are **unrelated** with **incompatible PKs** (``ssn`` vs. ``tax_id`` vs. ``routing_no``)
   - We cannot reuse any superclass PK as the category's PK
   - Solution: a **surrogate PK** + a **discriminator** + **mutually exclusive nullable FKs**


   Mapping Rule
   ^^^^^^^^^^^^^^

   - Create a **surrogate PK** (``owner_id``)
   - Add a **type discriminator** column (``owner_type``)
   - Add one **nullable FK per superclass**, only one non-NULL per row
   - ``CHECK``: exactly one FK is populated
   - Add any category-specific attributes

   Resulting Schema: ``VEHICLE_OWNER`` (``owner_id``, ``owner_type``, ``person_ssn``, ``company_tax_id``, ``bank_routing_no``, ``ownership_date``)


   .. only:: html

      .. figure:: /_static/images/l3/category-light.png
         :alt: Mapping categories from Chen to Crow's Foot
         :width: 80%
         :align: center
         :class: only-light

         **Mapping categories**: Chen (left) to Crow's Foot (right)

      .. figure:: /_static/images/l3/category-dark.png
         :alt: Mapping categories from Chen to Crow's Foot
         :width: 80%
         :align: center
         :class: only-dark

   .. only:: latex

      .. figure:: /_static/images/l3/category-light.png
         :alt: Mapping categories from Chen to Crow's Foot
         :width: 80%
         :align: center

         **Mapping categories**: Chen (left) to Crow's Foot (right)


   Category Table: Sample Data
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   .. list-table::
      :widths: 10 12 18 18 18 15
      :header-rows: 1
      :class: compact-table

      * - owner_id
        - owner_type
        - person_ssn
        - company_tax_id
        - bank_routing_no
        - ownership_date
      * - 1
        - person
        - 111-22-3333
        - NULL
        - NULL
        - 2024-03-15
      * - 2
        - person
        - 444-55-6666
        - NULL
        - NULL
        - 2024-06-01
      * - 3
        - company
        - NULL
        - 52-1234567
        - NULL
        - 2025-01-10
      * - 4
        - bank
        - NULL
        - NULL
        - 021000021
        - 2025-09-22

   *Each row has exactly one non-NULL FK. The NULLs are expected: each row belongs to exactly one superclass. The CHECK constraint enforces this invariant at the database level.*

   .. card::
       :class-card: sd-border-info

       **Key difference from ISA**: In ISA, subclasses share a common superclass with a single PK. In a category, the superclasses are unrelated with incompatible PKs, so a surrogate PK is required.




Complete Mapping Result
====================================================


.. dropdown:: Full Table Inventory
   :class-container: sd-border-secondary
   :open:

   All Tables, Organized by Mapping Step
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 8 18 50 24
      :header-rows: 1
      :class: compact-table

      * - Step
        - Table
        - Key Columns
        - Origin
      * - 1
        - ``PERSON``
        - ``person_id``
        - Strong entity
      * - 1
        - ``ACADEMIC_RANK``
        - ``rank_code``
        - Strong (lookup)
      * - 1
        - ``DEPARTMENT``
        - ``dept_id``
        - Strong entity
      * - 1
        - ``COURSE``
        - ``course_id``, ``dept_id`` (Step 4)
        - Strong entity
      * - 1
        - ``ROOM``
        - ``room_id``
        - Strong entity
      * - 2
        - ``COURSE_SECTION``
        - ``course_id``, ``section_no``, ``professor_person_id`` (Step 4), ``room_id`` (Step 4)
        - Weak entity
      * - 5
        - ``ENROLLMENT``
        - ``student_person_id``, ``course_id``, ``section_no``
        - :math:`M{:}N` junction
      * - 5
        - ``COURSE_PREREQ``
        - ``successor_id``, ``prereq_id``
        - Recursive :math:`M{:}N`
      * - 6
        - ``PERSON_PHONE``
        - ``person_id``, ``phone_number``
        - MV attribute
      * - 6
        - ``PERSON_EMAIL``
        - ``person_id``, ``email_address``
        - MV attribute
      * - 6
        - ``PROF_SPECIALIZATION``
        - ``person_id``, ``specialization``
        - MV attribute
      * - 6
        - ``STUDENT_DEGREE``
        - ``person_id``, ``degree_type``, ``institution``, ``year``
        - MV (composite)
      * - 7
        - ``TA_ASSIGNMENT``
        - ``course_id``, ``section_no``, ``grad_person_id``, ``professor_person_id``
        - Ternary
      * - ISA
        - ``STUDENT``
        - ``person_id``, ``student_id``, ``advisor_person_id``
        - Subclass
      * - ISA
        - ``PROFESSOR``
        - ``person_id``, ``professor_id``, ``dept_id``, ``rank_code``
        - Subclass
      * - ISA
        - ``GRAD_STUDENT``
        - ``person_id``, ``thesis_topic``
        - Subclass
      * - ISA
        - ``INTL_STUDENT``
        - ``person_id``, ``visa_type``, ``country_of_origin``
        - Subclass


.. dropdown:: Validation Checklist
   :class-container: sd-border-secondary

   Verifying the Mapping
   ~~~~~~~~~~~~~~~~~~~~~~

   .. card::
       :class-card: sd-border-success

       **Use this as your rubric**

       - ☑ Every strong entity has a table with all simple/composite attributes
       - ☑ Every weak entity has a table whose PK includes the owner's PK
       - ☑ Every :math:`1{:}1` relationship captured by FK (with ``UNIQUE``) on appropriate side
       - ☑ Every :math:`1{:}N` relationship captured by FK on the "many" side
       - ☑ Every :math:`M{:}N` relationship has a junction table with composite PK
       - ☑ Every multivalued attribute has its own table with FK to owner
       - ☑ Every ternary relationship has its own table with FKs to all participants
       - ☑ ISA hierarchies mapped with consistent strategy and correct PK/FK sharing
       - ☑ Categories have discriminator column and mutually exclusive FKs
       - ☑ Derived attributes omitted (or marked as computed)
       - ☑ Total participation :math:`\Rightarrow` ``NOT NULL`` FK; partial :math:`\Rightarrow` nullable FK
       - ☑ Relationship attributes in correct table (junction for :math:`M{:}N`, entity for :math:`1{:}N`)




Wrap-Up and Next Steps
====================================================


Key Takeaways
--------------

1. A **relational database** stores data in tables; relationships are implemented through **foreign keys** and **junction tables**, not as first-class constructs.

2. **Primary keys** uniquely identify rows; **foreign keys** enforce referential integrity; **constraints** (``NOT NULL``, ``UNIQUE``, ``CHECK``, ``CASCADE``) catch bad data at the DB level.

3. The logical model bridges **what** (conceptual) and **how** (physical); it resolves conceptual constructs into tables, columns, and foreign keys.

4. The **7-step algorithm** provides a systematic procedure: strong entities :math:`\to` weak entities :math:`\to` :math:`1{:}1` :math:`\to` :math:`1{:}N` :math:`\to` :math:`M{:}N` :math:`\to` multivalued attributes :math:`\to` :math:`n`-ary relationships.

5. **ISA hierarchies** can be mapped three ways (separate tables, subclass-only, single table); choice depends on constraints and query patterns.

6. **Categories** use a discriminator column with mutually exclusive nullable FKs.

7. **Crow's Foot notation** is the industry standard for logical models: entities are table boxes with columns; relationships are lines with fork/bar/circle symbols.