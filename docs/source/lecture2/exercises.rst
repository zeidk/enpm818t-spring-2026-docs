====================================================
Exercises
====================================================

This page contains exercises for Lecture 2. These exercises are designed to reinforce your understanding of conceptual data modeling using Entity-Relationship diagrams in Chen notation.


.. dropdown:: 🎯 Exercise 1 – Entity, Attribute & Key Identification
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice identifying and classifying entities, attributes, and keys for a given domain. Develop your ability to distinguish between strong and weak entities and to choose appropriate primary keys.

    ----

    **Specification**

    Complete Parts A–C on paper for the following entities from the university system: ``DEPARTMENT``, ``COURSE``, and ``ROOM``.

    **Part A: Entity Classification**

    For each of your three entities:

    1. Determine whether it is **strong** or **weak**. Justify your answer using the definitions from the lecture.
    2. For any weak entity you identify, specify the **owner (identifying) entity**.

    .. note::

       Review the definitions: A **strong entity** has its own primary key and exists independently. A **weak entity** cannot be uniquely identified by its own attributes alone and depends on an owner entity for its identity.

    **Part B: Attributes**

    For each entity:

    1. List at least **4 attributes** that describe the entity.
    2. Classify each attribute as one of the following:

       - **Simple** (atomic, cannot be divided)
       - **Composite** (subdivided into sub-attributes)
       - **Multivalued** (can have multiple values per entity)
       - **Derived** (computed from other attributes)
       - **Constrained domain** (limited to a fixed set of values)

    3. Determine if any attribute should be promoted to a **lookup entity**. Justify your decision using the promotion test from the lecture.

    .. tip::

       **The Promotion Test**: If removing the value set would lose information beyond the label itself (e.g., descriptions, effective dates, eligibility criteria), promote it to an entity. If the value is just a label, keep it as an attribute.

    **Part C: Keys**

    For each entity:

    1. Identify at least one **candidate key** (a minimal set of attributes that uniquely identifies each instance).
    2. Select a **primary key** from your candidate keys. Justify your choice.
    3. For any weak entity, state the **partial key** (discriminator) and describe how the full composite key is formed by combining it with the owner's key.
    4. Draw **one** of your three entities with all its attributes in **Chen notation**. Use the correct oval styles:

       - Solid underline for **primary keys**
       - Dashed underline for **partial keys**
       - Double oval for **multivalued attributes**
       - Dashed oval for **derived attributes**
       - Regular oval for **simple attributes**
       - Composite attributes shown with sub-ovals

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Part A**: Entity classification for ``DEPARTMENT``, ``COURSE``, and ``ROOM`` with justifications
    - **Part B**: Attribute lists and classifications for all three entities, including any promotion decisions
    - **Part C**: Keys for all three entities, with a Chen notation diagram for one entity
    - **Diagram Requirements**: Hand-drawn or digital (use ERDPlus, draw.io, or similar). Must show the entity rectangle, all attributes as ovals, and proper notation (underlines, double borders, dashes).


.. dropdown:: 🔗 Exercise 2 – Modeling New Relationships
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice modeling binary and recursive relationships with correct cardinality ratios, participation constraints, and relationship attributes.

    ----

    **Specification**

    The university has these additional business rules not yet in our model. Using **Chen notation** (pen and paper or ERDPlus), draw **two** of the following three relationships:

    **Option 1: Recursive Relationship**

    ``PROFESSOR`` --- ``SUPERVISES`` --- ``PROFESSOR``

    Some professors supervise junior faculty members.

    Requirements:

    - Determine the **cardinality ratio** (1:1, 1:N, or M:N)
    - Specify **(min, max) constraints** on both sides
    - Use **double lines** for total participation, **single lines** for partial participation
    - Label the **roles** (e.g., "supervisor" and "supervisee") to disambiguate the recursive relationship

    .. note::

       **Roles are required** for recursive relationships because the same entity type appears twice. Without roles, the diagram is ambiguous about which instance plays which function.

    **Option 2: Relationship with Attributes**

    ``STUDENT`` --- ``WORKS_IN`` --- ``DEPARTMENT``

    Students can hold part-time jobs in departments (e.g., lab assistant, grader, office assistant).

    Requirements:

    - Determine the **cardinality ratio** (1:1, 1:N, or M:N)
    - Specify **(min, max) constraints** on both sides
    - Include **relationship attributes**: ``start_date``, ``hours_per_week``, ``hourly_rate``
    - Draw these attributes as ovals connected to the relationship diamond

    .. tip::

       **Test for relationship attributes**: Does this attribute make sense without knowing *both* entities? If ``hours_per_week`` doesn't make sense without knowing both the specific student and the specific department, it belongs on the relationship.

    **Option 3: Asymmetric Participation**

    ``ROOM`` --- ``MAINTAINED_BY`` --- ``DEPARTMENT``

    Each room is maintained by one department, but not every department maintains rooms (some departments may be purely academic with no physical spaces).

    Requirements:

    - Determine the **cardinality ratio** (1:1, 1:N, or M:N)
    - Specify **(min, max) constraints** on both sides
    - Carefully determine participation on **both sides**: Is it total or partial?
    - Justify your participation constraints based on the business rules

    ----

    **For Each Relationship You Draw**

    1. Label the **cardinality ratio** (1:1, 1:N, or M:N) on both sides
    2. Specify **(min, max) constraints** on both sides
    3. Use **double lines** for total participation, **single lines** for partial
    4. Include any **relationship attributes** attached to the diamond
    5. For recursive relationships, add **role labels**

    .. warning::

       **Justify your constraints**: For each (min, max) you assign, write **one sentence** explaining the business rule behind it. There is no single correct answer; different assumptions lead to different models. Your justification matters more than the specific numbers you choose.

    ----

    **Deliverables**

    Submit the following via Canvas:

    - Chen notation diagrams for **two** of the three relationships
    - For each diagram: justifications (1 sentence each) for your cardinality and participation choices
    - **Diagram Requirements**: Hand-drawn or digital. Must show entities as rectangles, relationship as diamond, proper line notation (single vs. double), cardinality labels, and (min, max) constraints on both sides.


.. dropdown:: 🏗️ Exercise 3 – Specialization Hierarchy
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice modeling specialization/generalization hierarchies with correct constraint notation (disjoint/overlapping, total/partial).

    ----

    **Specification**

    Model the ``PERSON`` → ``STUDENT`` / ``PROFESSOR`` specialization hierarchy from the university system using Chen/EER notation.

    **Part A: Top-Level Specialization**

    1. Draw the ``PERSON`` entity as the superclass with these attributes:

       - ``person_id`` (primary key)
       - ``name`` (composite: first, middle, last)
       - ``DOB``
       - ``email``
       - ``phone_numbers`` (multivalued)

    2. Draw the ISA relationship (triangle or circle) connecting ``PERSON`` to its two subclasses: ``STUDENT`` and ``PROFESSOR``

    3. Specify the constraints:

       - **Disjoint or Overlapping?** Can a person be both a student and a professor simultaneously in this university system? Justify your decision.
       - **Total or Partial?** Must every person in the database be either a student or a professor, or can there be "generic" persons (e.g., staff, alumni)? Justify your decision.

    4. Add subclass-specific attributes:

       - ``STUDENT``: ``student_id``, ``enrollment_date``, ``gpa``, ``academic_standing``
       - ``PROFESSOR``: ``professor_id``, ``rank``, ``hire_date``, ``salary``, ``office``

    .. note::

       **Attribute Inheritance**: Subclasses inherit *all* superclass attributes. A ``STUDENT`` has ``person_id``, ``name``, ``DOB``, ``email``, ``phone_numbers`` *plus* ``student_id``, ``enrollment_date``, ``gpa``, and ``academic_standing``.

    **Part B: Second-Level Specialization**

    Add the ``GRAD_STUDENT`` specialization of ``STUDENT``:

    1. Draw the ISA relationship connecting ``STUDENT`` to ``GRAD_STUDENT``
    2. Specify the constraints:

       - **Disjoint or Overlapping?** Could a student belong to multiple subclasses if we added others later (e.g., ``INTERNATIONAL_STUDENT``, ``HONORS_STUDENT``)? Justify your decision.
       - **Total or Partial?** Must every student be a grad student, or can undergraduate students exist without belonging to any subclass? Justify your decision.

    3. Add subclass-specific attributes:

       - ``GRAD_STUDENT``: ``thesis_topic``, ``advisor_id`` (could also be a relationship)

    ----

    **Deliverables**

    Submit the following via Canvas:

    - Complete specialization hierarchy diagram showing both levels
    - For each ISA relationship, clearly mark:

      - **Disjoint (d) or Overlapping (o)**
      - **Total (double line) or Partial (single line)**

    - **Written justifications** (2–3 sentences each) for all four constraint decisions (two per ISA relationship)
    - **Diagram Requirements**: Hand-drawn or digital. Must show rectangles for entities, ISA triangle/circle, proper line notation (single vs. double), constraint labels (d/o, total/partial), and all attributes with correct oval styles.


.. dropdown:: 📊 Exercise 4 – Complete ER Diagram
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Integrate all concepts from the lecture by drawing a complete ER diagram for a simplified version of the university system.

    ----

    **Specification**

    Build a complete ER diagram that includes:

    **Required Entities (8 minimum)**

    1. ``PERSON`` (superclass)
    2. ``STUDENT`` (subclass of Person)
    3. ``PROFESSOR`` (subclass of Person)
    4. ``DEPARTMENT``
    5. ``COURSE``
    6. ``COURSE_SECTION`` (weak entity, owner: Course)
    7. ``ROOM``
    8. Choose one additional entity: ``GRAD_STUDENT`` (subclass of Student) *or* ``ACADEMIC_RANK`` (lookup entity)

    **Required Relationships (6 minimum)**

    1. ``BELONGS_TO``: Professor → Department
    2. ``OFFERS``: Department → Course
    3. ``ENROLLS_IN``: Student → Course_Section (with attributes: ``grade``, ``enroll_date``)
    4. ``HAS_SECTION``: Course → Course_Section (identifying relationship)
    5. ``HELD_IN``: Course_Section → Room (with attribute: ``time_slot``)
    6. Choose one additional relationship from Exercise 2 or create your own

    **Requirements for Each Component**

    .. list-table::
       :widths: 30 70
       :header-rows: 1

       * - Component
         - Requirements
       * - **Entities**
         - - Mark strong (single rectangle) vs. weak (double rectangle)
           - Include at least 3 attributes for each entity
           - Classify at least one multivalued and one derived attribute
           - Underline primary keys (solid) or partial keys (dashed)
       * - **Relationships**
         - - Label cardinality ratio (1:1, 1:N, M:N) on both sides
           - Specify (min, max) on both sides
           - Use double lines for total participation
           - Include relationship attributes where appropriate
           - Double diamond for identifying relationships
       * - **Specialization**
         - - Include the Person → Student/Professor hierarchy
           - Mark disjoint/overlapping and total/partial constraints
           - Show attribute inheritance (you can annotate this with a note)

    **Quality Checklist**

    Before submitting, verify your diagram against the quality checklist from the lecture:

    - ☑ Every entity has a primary key or partial key
    - ☑ All attributes are classified by type
    - ☑ Every relationship has cardinality on both sides
    - ☑ Every relationship has (min, max) on both sides
    - ☑ Weak entities have identifying relationships
    - ☑ Specialization constraints are marked
    - ☑ No obvious redundant relationships

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Complete ER diagram** (hand-drawn or digital using ERDPlus, draw.io, Lucidchart, etc.)
    - **Design decisions document** (1 page) explaining:

      - Why you chose disjoint vs. overlapping for the Person specialization
      - Why you chose total vs. partial for the Person specialization
      - Justification for at least 3 participation constraints (why total vs. partial)
      - Any entity vs. attribute promotion decisions you made

    - **Legend** (if using digital tools): Include a small legend showing what each symbol means
    - **Diagram Requirements**: Professional quality (neat, readable, properly labeled). Use a tool for digital submissions. Hand-drawn must be scanned clearly.

    .. important::

       This exercise is the most comprehensive and should take 45–60 minutes. It's designed to prepare you for your first homework assignment (HW1), which will involve designing a complete ER diagram for your project domain.
