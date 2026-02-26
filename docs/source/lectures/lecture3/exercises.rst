====================================================
Exercises
====================================================

This page contains exercises for Lecture 3. These exercises are designed to reinforce your understanding of logical data modeling, the relational model, and the ER-to-Relational mapping algorithm.


.. dropdown:: 🎯 Exercise 1 -- Relational Model Fundamentals
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice identifying and applying the core concepts of the relational model: relations, tuples, attributes, domains, keys, and properties.

    ----

    **Specification**

    Complete Parts A-C using the ``COURSE`` entity from the university system.

    **Part A: Relation Schema and Instance**

    1. Write the **relation schema** for ``COURSE`` using formal notation: R(A1: D1, A2: D2, ..., An: Dn). Include at least 4 attributes with their domains.
    2. Write a **relation instance** with at least 4 tuples (rows).
    3. State the **degree** and **cardinality** of your instance.
    4. If a new course is added next semester, which of these three values changes? Explain.

    .. note::

       **Formal notation example**: ``STUDENT`` (``person_id``: int, ``student_id``: varchar, ``gpa``: numeric, ``admission_date``: date)

    **Part B: Key Identification**

    For your ``COURSE`` relation:

    1. List at least two **superkeys** (they need not be minimal).
    2. Identify all **candidate keys** and justify minimality for each.
    3. Choose a **primary key** and justify your choice.
    4. Identify any **alternate keys**.

    .. tip::

       **Minimality test**: For each candidate key, try removing one attribute at a time. If the remaining attributes still uniquely identify every tuple, the original was not minimal.

    **Part C: Properties of Relations**

    For each of the four properties of relations (no duplicate tuples, tuples unordered, attributes unordered, atomic values), provide one specific example of how your ``COURSE`` table satisfies or could violate each property:

    1. What constraint prevents duplicate tuples?
    2. Show two orderings of the same relation instance that represent the same relation.
    3. Explain why referencing a column by name (``credits``) is preferred over referencing by position ("the 4th column").
    4. Give one example of a non-atomic value that could appear in a ``COURSE`` column and explain how to fix it.

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Part A**: Schema notation, instance table, degree, cardinality, and explanation
    - **Part B**: Superkeys, candidate keys, PK choice with justification, alternate keys
    - **Part C**: One example per property (4 total)


.. dropdown:: 🔗 Exercise 2 -- Mapping Strong and Weak Entities (Steps 1-2)
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice applying Steps 1 and 2 of the mapping algorithm: mapping strong entities and weak entities to relational tables.

    ----

    **Specification**

    Map the following entities from the university conceptual model to relational schemas.

    **Part A: Strong Entity Mapping (Step 1)**

    For each of the following entities, produce a relational schema showing all columns, PK, and any constraints:

    1. ``ROOM`` (room_id, building, room_number, capacity, room_type)
    2. ``DEPARTMENT`` (dept_id, dept_name, building, budget)

    For each table:

    - Identify the **primary key**
    - Specify which attributes should be ``NOT NULL``
    - Identify any columns that should have a ``UNIQUE`` constraint
    - Identify any columns that should have a ``CHECK`` constraint (e.g., capacity > 0)

    **Part B: Weak Entity Mapping (Step 2)**

    Map ``COURSE_SECTION`` (weak entity, owner: ``COURSE``):

    1. Write the full schema including the owner's PK as part of the composite PK
    2. Specify the FK relationship to ``COURSE``
    3. Explain why the identifying relationship (``HAS_SECTION``) does **not** produce a separate table
    4. What ``ON DELETE`` behavior should the FK use? Justify your choice.

    .. warning::

       **Common Mistake**: Forgetting that the owner's PK is both part of the weak entity's PK *and* an FK to the owner table. It serves a dual role.

    **Part C: Lookup Table Design**

    Design a lookup table for ``ROOM_TYPE``:

    1. Choose appropriate columns (code, display name, and at least one metadata column)
    2. Write sample data (at least 3 rows)
    3. Show how ``ROOM`` would reference this lookup table via FK
    4. Compare the lookup table approach with a ``CHECK`` constraint approach: when would you prefer each?

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Part A**: Relational schemas for ``ROOM`` and ``DEPARTMENT`` with all constraints
    - **Part B**: ``COURSE_SECTION`` schema with FK, PK explanation, and cascade justification
    - **Part C**: ``ROOM_TYPE`` lookup table design with sample data and comparison


.. dropdown:: 🔀 Exercise 3 -- Mapping Relationships (Steps 3-5)
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice applying Steps 3-5 of the mapping algorithm: mapping 1:1, 1:N, and M:N relationships to relational schemas.

    ----

    **Specification**

    For each of the following relationships, produce the mapping result showing all columns, PKs, FKs, and constraints.

    **Part A: 1:1 Relationship (Step 3)**

    ``PROFESSOR`` (0,1) -- ``CHAIRS`` -- (1,1) ``DEPARTMENT``

    1. Identify the **total** and **partial** participation sides.
    2. Decide where to place the FK. Justify your decision.
    3. Write the updated schema for the table that receives the FK.
    4. Specify the constraints on the FK column: ``NOT NULL``? ``UNIQUE``? Why?
    5. Where does the relationship attribute ``start_date`` go?
    6. **Counterexample**: Show what the table would look like if you placed the FK on the wrong side (partial participation side) with 8 sample rows. Count the NULLs and explain why this is worse.

    .. tip::

       **Rule**: In a 1:1 relationship, the FK goes on the **total participation side** to avoid NULLs. The FK is constrained ``NOT NULL`` (total) and ``UNIQUE`` (1:1).

    **Part B: 1:N Relationship (Step 4)**

    Map **two** of the following 1:N relationships:

    1. ``DEPARTMENT`` (1,N) -- ``OFFERS`` -- (1,1) ``COURSE``
    2. ``PROFESSOR`` (0,N) -- ``TEACHES`` -- (1,1) ``COURSE_SECTION``
    3. ``PROFESSOR`` (0,N) -- ``ADVISED_BY`` -- (1,1) ``STUDENT``

    For each:

    - Identify the "one" and "many" sides
    - Place the FK on the correct side
    - Determine ``NOT NULL`` vs. nullable based on participation
    - Name the FK column descriptively (especially for ``ADVISED_BY``, where the FK references ``PROFESSOR`` but the column should clarify the role)

    **Part C: M:N Relationship (Step 5)**

    Map the ``ENROLLS_IN`` relationship:

    ``STUDENT`` (0,N) -- ``ENROLLS_IN`` -- (0,N) ``COURSE_SECTION``

    1. Design the ``ENROLLMENT`` junction table with all columns
    2. Specify the composite PK
    3. Specify both FK constraints
    4. Include the relationship attributes (``grade``, ``enroll_date``)
    5. Write 5 sample rows showing students enrolled in different sections

    .. note::

       **Why a junction table?** Placing an FK on either ``STUDENT`` or ``COURSE_SECTION`` would require multiple values in a single cell. The junction table resolves this by creating one row per (student, section) pairing.

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Part A**: 1:1 mapping with FK placement justification and counterexample
    - **Part B**: Two 1:N mappings with FK, constraints, and descriptive naming
    - **Part C**: ``ENROLLMENT`` junction table with composite PK, FKs, attributes, and sample data


.. dropdown:: 🏗️ Exercise 4 -- Complete Mapping
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Integrate all mapping steps by performing a complete ER-to-Relational mapping for a new domain.

    ----

    **Specification**

    A small veterinary clinic needs a database. Here are the business rules:

    **Entities**

    - ``PET``: pet_id (PK), name, species, breed, date_of_birth, weight. Each pet has **one owner** (total participation).
    - ``OWNER``: owner_id (PK), first_name, last_name, phone_numbers (multivalued), email.
    - ``VET``: vet_id (PK), first_name, last_name, license_number (unique), hire_date, specializations (multivalued).
    - ``VISIT``: Weak entity owned by ``PET``. Partial key: visit_date. Attributes: diagnosis, treatment, notes.
    - ``SPECIES`` (lookup): species_code (PK), species_name (unique), avg_lifespan.

    **Relationships**

    - ``OWNS``: Owner (1,N) -- Pet (1,1). One owner has one or more pets; each pet has exactly one owner.
    - ``HAS_VISIT``: Pet (1,N) -- Visit (1,1). Identifying relationship.
    - ``TREATED_BY``: Visit (1,1) -- Vet (0,N). Each visit is treated by one vet; a vet treats many visits (some vets may have zero visits if newly hired).
    - ``PRESCRIBED_MED``: Visit (0,N) -- Medication (0,N). M:N relationship. Attributes: dosage, frequency, duration.
    - ``MEDICATION``: med_id (PK), med_name, manufacturer, unit_cost.

    **ISA Hierarchy**

    - ``PET`` specializes into ``DOG`` (training_level, is_neutered) and ``CAT`` (is_indoor, is_declawed). Disjoint, partial (not every pet is a dog or cat; could be a bird, reptile, etc.).

    **Tasks**

    Apply the 7-step mapping algorithm:

    1. **Step 1**: Map all strong entities (``OWNER``, ``PET``, ``VET``, ``MEDICATION``, ``SPECIES``). Include lookup table design for ``SPECIES``.
    2. **Step 2**: Map the weak entity ``VISIT``.
    3. **Step 3**: No 1:1 relationships in this model (skip).
    4. **Step 4**: Map 1:N relationships (``OWNS``, ``TREATED_BY``).
    5. **Step 5**: Map M:N relationship (``PRESCRIBED_MED``).
    6. **Step 6**: Map multivalued attributes (``phone_numbers``, ``specializations``).
    7. **Step 7**: No n-ary relationships (skip).
    8. **ISA**: Map the PET -> DOG / CAT hierarchy. Choose a strategy and justify.

    **Requirements for Each Table**

    .. list-table::
       :widths: 30 70
       :header-rows: 1

       * - Component
         - Requirements
       * - **Schema**
         - List all columns with PK, FK, UK markers
       * - **Constraints**
         - ``NOT NULL``, ``UNIQUE``, ``CHECK`` where appropriate
       * - **FK Behavior**
         - Specify ``ON DELETE`` action for each FK with justification
       * - **Sample Data**
         - At least 3 rows per table (5 for junction tables)

    **Quality Checklist**

    Before submitting, verify:

    - ☑ Every strong entity has a table with all simple/composite attributes
    - ☑ ``VISIT`` has a composite PK including ``PET``'s PK
    - ☑ 1:N FKs are on the "many" side with correct nullability
    - ☑ ``PRESCRIBED_MED`` junction table has composite PK of both FKs
    - ☑ Multivalued attributes have their own tables
    - ☑ ISA strategy is justified and correctly implemented
    - ☑ Lookup table for ``SPECIES`` is designed with metadata columns

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Complete set of relational schemas** for all tables (at least 12 tables total)
    - **Sample data** for each table
    - **Design decisions document** (1 page) explaining:

      - Why you chose your ISA strategy for PET -> DOG / CAT
      - How you handled the ``SPECIES`` lookup table vs. a ``CHECK`` constraint
      - Your ``ON DELETE`` choices for at least 3 FK relationships

    - **Crow's Foot diagram** (optional, extra credit): Draw the complete logical model using Crow's Foot notation in a tool of your choice (PlantUML, draw.io, DBeaver, etc.)

    .. important::

       This exercise is the most comprehensive and should take 60-90 minutes. It is designed to prepare you for your first homework assignment, which will involve mapping your project domain's conceptual model to a full relational schema.
