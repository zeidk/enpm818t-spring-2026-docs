====================================================
Lecture
====================================================




Foundations & Motivation
====================================================


Why Conceptual Modeling?
-------------------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Four Reasons to Model Before You Build**

    - **Communication Bridge**: Shared language between business stakeholders, analysts, and developers. Non-technical people can read and validate an ER diagram.
    - **Requirements Discovery**: Exposes ambiguities, missing data, and conflicting assumptions early. Forces you to ask: "What *exactly* do we mean by this?"
    - **Error Prevention**: Fixing a design flaw in a diagram costs minutes; in production, it costs weeks. Avoids costly schema migrations and data loss.
    - **Technology Independence**: Model the world as it is, not as a specific DBMS constrains it. The same conceptual model can target PostgreSQL, MySQL, or MongoDB.

.. important::

   Conceptual models capture **what** data exists and **how** it relates, independent of technology.


Three Levels of Data Modeling
------------------------------

.. grid:: 1 1 3 3
    :gutter: 2

    .. grid-item-card:: 🎯 Conceptual
        :class-card: sd-border-primary

        **What & How**

        - Entities, attributes, relationships
        - Chen notation (rectangles, ovals, diamonds)
        - Technology-independent
        - Stakeholder-facing

    .. grid-item-card:: 📊 Logical
        :class-card: sd-border-info

        **Tables & Keys**

        - Relational schemas (tables, columns)
        - Primary keys, foreign keys
        - Normalization (1NF → BCNF)
        - DBMS-family specific (relational vs. NoSQL)

    .. grid-item-card:: ⚙️ Physical
        :class-card: sd-border-warning

        **Storage & Performance**

        - Indexes, partitions, data types
        - Storage engines, file layouts
        - Specific DBMS (PostgreSQL 16)
        - Performance tuning

.. note::

   **Today's Focus**: The **conceptual model** — capturing *what* data exists and *how* it relates, before making any technology decisions.


ER Notations
------------

An **ER notation** is a standardized set of graphical symbols and conventions used to visually represent entities, attributes, and relationships in an Entity-Relationship diagram.

Chen Notation (1976)
~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::

        **Symbols**

        - Rectangles = Entities
        - Ovals = Attributes
        - Diamonds = Relationships
        - Lines with labels = Cardinality

    .. grid-item::

        **Strengths**

        - Great for learning and communication
        - Explicit relationship semantics
        - Standard in academia
        - Clear visual distinction between concepts

Crow's Foot / IE Notation
~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::

        **Symbols**

        - Rectangles with columns = Entities
        - Attributes listed inside box
        - Lines with fork symbols
        - Min/max shown at line ends

    .. grid-item::

        **Strengths**

        - Used in industry tools (ERwin, Lucidchart)
        - More compact diagrams
        - Closer to logical model

Other Notations
~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - Notation
     - Description
   * - **UML Class Diagrams**
     - Object-oriented notation widely used in software engineering; represents entities as classes with attributes and methods in compartmentalized boxes
   * - **IDEF1X**
     - US federal standard (FIPS 184); extends Chen with exact cardinality symbols; common in government and defense
   * - **Bachman Notation**
     - One of the earliest (1969); uses arrows to show data flow direction between record types
   * - **Min-Max Notation**
     - Extension of Chen that replaces cardinality labels with precise numeric ranges on participation

.. card::
    :class-card: sd-border-primary

    **This Lecture's Focus**

    This lecture focuses on **Chen Notation**: the original ER notation ideal for conceptual modeling. Crow's Foot *can* be used at the conceptual level as well, but it blurs the line with logical design because attributes appear as columns inside entity boxes, pulling you toward implementation thinking prematurely.


ER Modeling Tools
-----------------

Not all diagramming tools support Chen notation. Many default to Crow's Foot. Here are tools that support or can be configured for Chen notation:

.. list-table::
   :widths: 20 15 20 45
   :header-rows: 1
   :class: compact-table

   * - Tool
     - Cost
     - Chen Support
     - Notes
   * - **draw.io** (`diagrams.net <https://app.diagrams.net>`_)
     - Free
     - Yes (built-in)
     - Browser-based; Entity Relation shape library has Chen symbols
   * - **ERDPlus** (`erdplus.com <https://erdplus.com>`_)
     - Free
     - Yes (native)
     - Designed for Chen notation; exports to relational schema
   * - **Lucidchart** (`lucidchart.com <https://www.lucidchart.com>`_)
     - Free (limited)
     - Yes (shape library)
     - Collaborative; requires importing Chen shapes
   * - **PlantUML** (`plantuml.com <https://plantuml.com/er-diagram>`_)
     - Free
     - Partial
     - Text-based; integrates with VS Code, IntelliJ, and CI pipelines
   * - **Mermaid** (`mermaid.js.org <https://mermaid.js.org>`_)
     - Free
     - Partial
     - Text-based; supports basic ER but limited Chen styling
   * - **TikZ (LaTeX)** (`tikz.dev <https://tikz.dev>`_)
     - Free
     - Full control
     - Used in this course; publication-quality diagrams
   * - **Microsoft Visio** (`microsoft.com <https://www.microsoft.com/en-us/microsoft-365/visio>`_)
     - Paid
     - Yes (template)
     - Chen template available; common in enterprise

.. tip::

   **Recommendation for this course**: Use **ERDPlus** for homework and practice. It natively supports Chen notation, enforces correct symbol usage, and can generate relational schemas from your diagrams. For text-based workflows, **PlantUML** and **Mermaid** integrate well with version control and documentation pipelines. For quick sketches, **draw.io** is excellent and requires no account.


Running Use Case
----------------

.. card::
    :class-card: sd-border-info sd-shadow-sm

    **Use Case: University Course Management System**

    A university needs a database to manage its academic operations. The system must track:

    - **Students** — personal information, enrollment dates, and academic standing
    - **Professors** — employment details, rank, and department affiliation
    - **Courses** — offered each semester with room assignments and capacity limits
    - **Departments** — which employ professors and offer courses
    - **Enrollments** — students taking courses, with grades assigned per course
    - **Prerequisites** — some courses require completion of other courses first
    - **Advisors** — each student is assigned a faculty advisor

    The university also has **graduate students** who serve as Teaching Assistants (TAs) for courses. Some professors are **Department Chairs**. Rooms are shared across departments and may host multiple courses at different times.

.. note::

   We will build the ER diagram for this system **step by step** throughout the lecture.




Entities, Attributes & Keys
====================================================


What Is an Entity?
------------------

Definitions from the Literature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary

    **From Foundational Papers and Textbooks**

    - **Chen (1976)**: "An entity is a 'thing' which can be distinctly identified. A specific person, company, or event is an example of an entity."
    - **Elmasri & Navathe**: "An entity is a thing in the real world with an independent existence. It may be an object with physical existence ... or ... conceptual existence."
    - **Silberschatz, Korth & Sudarshan**: "An entity is an object that exists and is distinguishable from other objects ... described by a set of attributes."

Synthesized Definition
~~~~~~~~~~~~~~~~~~~~~~~

An **entity** is a distinctly identifiable thing in the real world (physical or conceptual) about which we need to store data. It may be a **person** (a student), a **physical object** (a room), an **organization** (a department), an **event** (an enrollment), or an **abstract concept** (a course). Each entity has **instances** (Alice, Bob, and Charlie are instances of ``STUDENT``), and each instance is described by a set of **attributes**.

.. note::

   **Chen (1976) Insight**: Chen acknowledges that the boundary between entity and relationship is a modeling choice: "It is possible that some people may view something (e.g., marriage) as an entity while other people may view it as a relationship ... this is a decision which has to be made by the enterprise administrator."


Entity Type vs. Entity Set
---------------------------

Definitions from the Literature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary

    **Terminology Clarification**

    - **Chen (1976)**: Entities are "classified into different *entity sets* such as EMPLOYEE, PROJECT, and DEPARTMENT. There is a predicate associated with each entity set to test whether an entity belongs to it."
    - **Elmasri & Navathe**: An *entity type* defines a collection of entities that have the same attributes; an *entity set* is the current collection of instances of that type at a point in time.
    - **Silberschatz et al.**: "An *entity set* is a set of entities of the same type that share the same properties."

.. warning::

   **Terminology Note**: Chen uses **entity set** for the concept that Elmasri & Navathe split into **entity type** (the schema/structure) and **entity set** (the current instances). Silberschatz uses **entity set** closer to Chen's usage. Be aware of this when reading different textbooks.

Sample Entity Types and Instances
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 40 35
   :header-rows: 1
   :class: compact-table

   * - Entity Type
     - Attributes (Schema)
     - Sample Instances (Entity Set)
   * - ``STUDENT``
     - student_id, name, gpa, DOB
     - (S101, Alice, 3.8, 1999-03-15)
       (S102, Bob, 3.2, 2000-07-22)
   * - ``COURSE``
     - course_id, title, credits
     - (ENPM818T, Data Storage & DB, 3)
       (ENPM702, Intro Robot Programming, 3)
   * - ``DEPARTMENT``
     - dept_id, dept_name, budget
     - (CS, Computer Science, 2500000)
       (ME, Mechanical Engineering, 1800000)
   * - ``ROOM``
     - room_id, building, capacity
     - (EGR-1103, Kim Building, 40)
       (IRB-0324, IRB, 120)

.. tip::

   **OOP Analogy**: Entity type ≈ **class** (the blueprint); entity instance ≈ **object** (one student); entity set ≈ the collection of all currently instantiated objects of that class. Each instance must be **distinguishable** — this is the role of the key.


Strong vs. Weak Entities
-------------------------

Definitions from the Literature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary

    **From Elmasri & Navathe and Silberschatz et al.**

    - **Elmasri & Navathe**: Entity types that do not have key attributes of their own are called *weak entity types*; those that do are called *strong* (or *regular*) entity types.
    - **Silberschatz et al.**: "An entity that does not have a primary key is referred to as a *weak entity set*. The existence of a weak entity set depends on the existence of an *identifying entity set*."

.. only:: html

   .. figure:: /_static/images/l2/strong-vs-weak-entity-light.png
      :alt: Strong vs. weak entity comparison
      :width: 100%
      :align: center
      :class: only-light

      **Strong Entity** (left): Has its own primary key, exists independently. **Weak Entity** (right): Cannot be uniquely identified by its own attributes alone, existence-dependent on owner entity.

   .. figure:: /_static/images/l2/strong-vs-weak-entity-dark.png
      :alt: Strong vs. weak entity comparison
      :width: 100%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/strong-vs-weak-entity-light.png
      :alt: Strong vs. weak entity comparison
      :width: 100%
      :align: center

      **Strong Entity** (left): Has its own primary key, exists independently. **Weak Entity** (right): Cannot be uniquely identified by its own attributes alone, existence-dependent on owner entity.

Comparison
~~~~~~~~~~

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - Aspect
     - Strong Entity
     - Weak Entity
   * - **Primary Key**
     - Has its own primary key
     - No independent key; uses partial key + owner's key
   * - **Existence**
     - Exists independently
     - Existence-dependent on owner
   * - **Chen Symbol**
     - Single rectangle
     - Double rectangle
   * - **Examples**
     - ``STUDENT``, ``PROFESSOR``, ``DEPARTMENT``, ``COURSE``
     - ``COURSE_SECTION`` (depends on ``COURSE``)

.. card::
    :class-card: sd-border-info

    **Why is Course_Section weak?**

    Section "001" is not unique on its own: ENPM818T has a section 001, and ENPM702 also has a section 001. The ``section_no`` only identifies a section *within the context of a specific course*. Without knowing which ``COURSE`` it belongs to, we cannot distinguish one section from another. The full identity requires the owner's key: ``(course_id, section_no)``.


What Is an Attribute?
---------------------

Definitions from the Literature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary

    **From Chen, Elmasri & Navathe, and Silberschatz et al.**

    - **Chen (1976)**: "The information about an entity or a relationship is obtained by observation or measurement, and is expressed by a set of attribute-value pairs." An attribute is formally "a function which maps from an entity set or a relationship set into a value set."
    - **Elmasri & Navathe**: Each entity has particular *attributes*; the properties that describe it. An entity is represented in the database by a collection of attributes; a particular entity will have a *value* for each of its attributes.
    - **Silberschatz et al.**: "An entity is represented by a set of attributes, that is, descriptive properties possessed by all members of an entity set."

Synthesized Definition
~~~~~~~~~~~~~~~~~~~~~~~

An **attribute** is a named property of an entity (or relationship) that maps each instance to a value drawn from a defined **domain**, i.e., the set of permitted values (e.g., GPA ∈ [0.0, 4.0]; rank ∈ {Assistant, Associate, Full}).

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::

        **Key Points**

        - A **NULL** value means the attribute is unknown or not applicable for a particular instance
        - Attributes can be **single-valued** or **multivalued**
        - Some attributes are **stored** (recorded directly) while others are **derived** (computed)

    .. grid-item::

        **Entity or Attribute?**

        .. tip::

           If something has *its own attributes* and participates in independent relationships, it should be modeled as an entity. If it merely describes a property of another thing, it is likely an attribute.


Attribute Types
---------------

Chen notation distinguishes six types of attributes:

.. list-table::
   :widths: 20 40 15 25
   :header-rows: 1
   :class: compact-table

   * - Type
     - Description
     - Chen Symbol
     - Example
   * - **Simple (Atomic)**
     - Cannot be divided further
     - Single oval
     - first_name, gpa
   * - **Composite**
     - Subdivided into sub-attributes
     - Oval with sub-ovals
     - name → {first, middle, last}
   * - **Multivalued**
     - Multiple values per entity
     - Double oval
     - phone_numbers, emails
   * - **Derived**
     - Computed from other attributes
     - Dashed oval
     - age (from DOB)
   * - **Key**
     - Uniquely identifies an instance
     - Underlined oval
     - student_id
   * - **Composite + Multivalued**
     - Composite and can repeat
     - Double oval with sub-ovals
     - previous_degrees → {type, institution, year}

.. only:: html

   .. figure:: /_static/images/l2/attribute-types-diagram-light.png
      :alt: Chen notation attribute types diagram
      :width: 100%
      :align: center
      :class: only-light

      **Chen Notation Attribute Types**: Visual representation of all attribute types attached to a ``STUDENT`` entity

   .. figure:: /_static/images/l2/attribute-types-diagram-dark.png
      :alt: Chen notation attribute types diagram
      :width: 100%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/attribute-types-diagram-light.png
      :alt: Chen notation attribute types diagram
      :width: 100%
      :align: center

      **Chen Notation Attribute Types**: Visual representation of all attribute types attached to a ``STUDENT`` entity

.. card::
    :class-card: sd-border-warning

    **Stored vs. Derived**

    A stored attribute (``date_of_birth``) is recorded directly in the database. A derived attribute (``age``) is calculated from stored attributes and is *not* stored — it can always be recomputed. This distinction matters for data consistency: if you store ``age``, it becomes stale every birthday.


Why Is Course_Section a Weak Entity?
-------------------------------------

.. only:: html

   .. figure:: /_static/images/l2/course-section-weak-entity-light.png
      :alt: Course_Section as weak entity with relationships
      :width: 80%
      :align: center
      :class: only-light

      **Why Not an Attribute of Course?** Course_Section has its own attributes and participates in relationships

   .. figure:: /_static/images/l2/course-section-weak-entity-dark.png
      :alt: Course_Section as weak entity with relationships
      :width: 80%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/course-section-weak-entity-light.png
      :alt: Course_Section as weak entity with relationships
      :width: 80%
      :align: center

      **Why Not an Attribute of Course?** Course_Section has its own attributes and participates in relationships

**Three Reasons It Must Be an Entity:**

1. **It has its own attributes**: A section carries semester, capacity, and schedule. These describe the section, not the course. The same course can have sections with different capacities in different semesters.

2. **It participates in its own relationships**: A section is taught by a professor (``TEACHES``), enrolled in by students (``ENROLLS_IN``), and assigned to a room (``HELD_IN``). An attribute cannot participate in relationships—only an entity can.

3. **It is not uniquely identifiable on its own**: Section "001" exists in many courses. The full identity requires the owner's key: ``(course_id, section_no)``. This makes it **weak**, not strong.

.. tip::

   **The test**: If something has its own attributes *or* participates in its own relationships, it must be an entity. If it also cannot be uniquely identified without another entity's key, it is a **weak** entity.


Composite and Multivalued: A Closer Look
-----------------------------------------

Composite Attributes
~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::

        **Characteristics**

        - Can be referenced as a **whole** or by **individual parts**
        - Useful when sometimes you need the full value and sometimes just a component
        - **Design choice**: If you never need to query sub-parts independently, keep it simple (atomic)

    .. grid-item::

        **Examples**

        - name → {first, middle, last}
        - address → {street, city, state, zip}
        - DOB → {day, month, year}

Multivalued Attributes
~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::

        **Characteristics**

        - A single entity instance holds a **set** of values, not just one
        - The number of values can differ per instance
        - **Impact on design**: Multivalued attributes become *separate tables* in the logical model

    .. grid-item::

        **Examples**

        - phone_numbers (a student can have multiple)
        - email_addresses
        - specializations (a professor may have several)
        - previous_degrees (composite + multivalued)

.. warning::

   **Common Mistake**: Listing multiple phone numbers as separate attributes (``phone1``, ``phone2``, ``phone3``) is *not* the same as a multivalued attribute. This approach imposes a fixed upper limit and wastes space when a student has only one phone. Use a multivalued attribute instead.


Domain Constraints and Fixed Value Sets
----------------------------------------

Attributes with Constrained Domains
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some attributes can only take values from a small, fixed set. At the conceptual level, we specify this as a **domain constraint** (the permitted values are documented as part of the attribute's definition).

.. list-table::
   :widths: 25 45 30
   :header-rows: 1
   :class: compact-table

   * - Attribute
     - Domain (Permitted Values)
     - Entity
   * - rank
     - {Assistant, Associate, Full}
     - ``PROFESSOR``
   * - academic_standing
     - {Good Standing, Probation, Suspended, Dismissed}
     - ``STUDENT``
   * - semester
     - {Fall, Spring, Summer}
     - ``COURSE_SECTION``
   * - course_level
     - {Undergraduate, Graduate}
     - ``COURSE``
   * - room_type
     - {Lecture Hall, Lab, Seminar, Office}
     - ``ROOM``

Chen Notation Example
~~~~~~~~~~~~~~~~~~~~~~

.. only:: html

   .. figure:: /_static/images/l2/constrained-domain-attribute-light.png
      :alt: Constrained domain attribute in Chen notation
      :width: 60%
      :align: center
      :class: only-light

      **Constrained domain in Chen notation**: The attribute is drawn as a regular oval, with permitted values annotated

   .. figure:: /_static/images/l2/constrained-domain-attribute-dark.png
      :alt: Constrained domain attribute in Chen notation
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/constrained-domain-attribute-light.png
      :alt: Constrained domain attribute in Chen notation
      :width: 60%
      :align: center

      **Constrained domain in Chen notation**: The attribute is drawn as a regular oval, with permitted values annotated

Attribute vs. Lookup Entity
----------------------------

When to Promote a Constrained Attribute to a Lookup Entity
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Sometimes a fixed value set should be modeled as its own entity rather than a domain constraint on an attribute.

Keep as Attribute When...
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
    :class-card: sd-border-success

    - The value set is **small and stable** (rarely changes)
    - The values have **no attributes of their own**
    - Only **one entity** references these values
    - You only need the **value itself**, not metadata about it
    - **Examples**: semester {Fall, Spring, Summer}; boolean flags
    - At the conceptual level: documented in the **data dictionary**
    - At the physical level: enforced as schema constraints (``CHECK`` or ``ENUM``)

Promote to Entity When...
^^^^^^^^^^^^^^^^^^^^^^^^^^

.. card::
    :class-card: sd-border-warning

    - The values have **their own attributes** (code, label, description, effective_date)
    - The value set **changes over time** (new values added, old ones retired)
    - **Multiple entities** reference the same set
    - You need to **query or report** on the values independently
    - **Example**: ``ACADEMIC_RANK``

.. tip::

   **The Test**: If removing the value set would lose information beyond the label itself, promote it to an entity. If the value is just a label with nothing else to say about it, keep it as an attribute.

Example: Why Promote "rank" to a Lookup Entity?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. only:: html

   .. figure:: /_static/images/l2/academic-rank-lookup-entity-light.png
      :alt: Academic rank as a lookup entity
      :width: 60%
      :align: center
      :class: only-light

      **Promoting rank to a lookup entity**: ``ACADEMIC_RANK`` has its own attributes (description, min_years_experience, effective_date)

   .. figure:: /_static/images/l2/academic-rank-lookup-entity-dark.png
      :alt: Academic rank as a lookup entity
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/academic-rank-lookup-entity-light.png
      :alt: Academic rank as a lookup entity
      :width: 60%
      :align: center

      **Promoting rank to a lookup entity**: ``ACADEMIC_RANK`` has its own attributes (description, min_years_experience, effective_date)

**Rationale for Promotion:**

1. **Has its own attributes**: A rank is not just the string "Associate": it carries a description, minimum years of experience, and an effective date.

2. **Multiple entities reference it**: Both ``PROFESSOR`` and potentially ``JOB_POSTING`` or ``SALARY_SCALE`` need the same rank definitions.

3. **Changes over time**: The university might add "Distinguished," retire old ranks, or update eligibility thresholds. With an entity, you update one row. With a constrained attribute, you must alter the schema.

4. **Queried independently**: "How many ranks require >10 years of experience?" or "When was Associate last updated?" (these questions target the rank itself, not any professor).

.. note::

   **Implementation Preview**: At the physical level, constrained attributes become PostgreSQL ``ENUM`` types or ``CHECK`` constraints. Lookup entities become reference tables with foreign keys. Both are valid—the choice depends on how the data will be used and maintained.


What Is a Key?
--------------

Definitions from the Literature
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-secondary

    **From Chen, Elmasri & Navathe, and Silberschatz et al.**

    - **Chen (1976)**: Entities within an entity set are distinguishable from one another through their attributes. Chen uses underlined attributes in ER diagrams to denote identifiers, but does not formalize a hierarchy of key types (superkey, candidate key). That terminology originates from Codd's relational model and was later integrated into ER modeling by subsequent authors.
    - **Elmasri & Navathe**: "An attribute of an entity type for which each entity must have a unique value is called a *key attribute*. ... A key attribute may be composite."
    - **Silberschatz et al.**: "A *superkey* is a set of one or more attributes that, taken collectively, allow us to identify uniquely an entity in the entity set." A *candidate key* is a minimal superkey.

Synthesized Definition
~~~~~~~~~~~~~~~~~~~~~~~

A **key** is an attribute (or minimal combination of attributes) whose values **uniquely identify** each instance of an entity. No two students share the same ``student_id``: that is what makes it a key. Without keys, we cannot distinguish one entity instance from another.

.. note::

   **Why does this matter?** Keys enforce **entity integrity**, which is the guarantee that every instance is distinguishable. At the conceptual level we identify *what* makes each entity unique. Surrogate keys, auto-increment IDs, and UUIDs are logical/physical concerns addressed in Lecture 3.


Types of Keys
-------------

.. list-table::
   :widths: 25 50 25
   :header-rows: 1
   :class: compact-table

   * - Key Type
     - Definition
     - Example (``STUDENT``)
   * - **Superkey**
     - Any set of attributes that uniquely identifies every instance (need not be minimal)
     - {student_id, name, gpa}
   * - **Candidate Key**
     - A *minimal* superkey: removing any attribute breaks uniqueness
     - {student_id} or {ssn}
   * - **Primary Key**
     - The candidate key chosen as the main identifier; underlined in Chen notation
     - student_id
   * - **Composite Key**
     - A primary key made of multiple attributes
     - ``ENROLLMENT``: {student_id, section_id, semester}
   * - **Partial Key**
     - Discriminator for weak entities; combined with owner's key to form full identity
     - ``COURSE_SECTION``: section_no + owner's course_id

Superkey vs. Candidate Key
~~~~~~~~~~~~~~~~~~~~~~~~~~~

``STUDENT`` has attributes: student_id, ssn, name, gpa, email_addresses.

.. list-table::
   :widths: 40 20 40
   :header-rows: 1
   :class: compact-table

   * - Attribute Set
     - Unique?
     - Minimal?
   * - {student_id, name, gpa}
     - ✓ Yes → superkey
     - ✗ No: remove name and gpa, still unique
   * - {student_id, ssn}
     - ✓ Yes → superkey
     - ✗ No: either alone is sufficient
   * - {student_id}
     - ✓ Yes → superkey
     - ✓ Yes → **candidate key**
   * - {ssn}
     - ✓ Yes → superkey
     - ✓ Yes → **candidate key**
   * - {name}
     - ✗ No (not unique)
     - ---
   * - {gpa}
     - ✗ No (not unique)
     - ---

.. warning::

   **The relationship**: Every candidate key is a superkey, but most superkeys are *not* candidate keys because they contain unnecessary attributes. A candidate key is a superkey with **nothing extra**. Think of it as: superkey − redundant attributes = candidate key.


Keys in Chen Notation
----------------------

How Keys Appear in Chen Diagrams
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. only:: html

   .. figure:: /_static/images/l2/keys-in-chen-notation-light.png
      :alt: Keys in Chen notation
      :width: 90%
      :align: center
      :class: only-light

      **Strong entity** (top): Primary key with solid underline. **Weak entity** (bottom): Partial key with dashed underline, connected to owner via identifying relationship (double diamond + double lines)

   .. figure:: /_static/images/l2/keys-in-chen-notation-dark.png
      :alt: Keys in Chen notation
      :width: 90%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/keys-in-chen-notation-light.png
      :alt: Keys in Chen notation
      :width: 90%
      :align: center

      **Strong entity** (top): Primary key with solid underline. **Weak entity** (bottom): Partial key with dashed underline, connected to owner via identifying relationship (double diamond + double lines)

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - Symbol
     - Meaning
   * - Solid underline in oval
     - Primary key (strong entity)
   * - Dashed underline in oval
     - Partial key (weak entity)
   * - Double rectangle
     - Weak entity
   * - Double diamond + double lines
     - Identifying relationship
   * - Full key of weak entity
     - owner's key + partial key: ``(course_id, section_no)``

.. note::

   **Candidate keys not chosen** as primary key are not shown in Chen notation. The ER diagram only marks the *primary* key.




Relationships & Cardinality
====================================================


What Is a Relationship?
-----------------------

Relationship
~~~~~~~~~~~~

A **relationship** is a meaningful association between two or more entities. It captures the fact that entities are connected in the real world.

- A professor *belongs to* a department
- A student *enrolls in* a course section
- A department *offers* a course

In Chen Notation
~~~~~~~~~~~~~~~~

A relationship is drawn as a **diamond** connected by lines to the participating entities.

.. only:: html

   .. figure:: /_static/images/l2/basic-relationship-light.png
      :alt: Basic relationship in Chen notation
      :width: 70%
      :align: center
      :class: only-light

      **Binary relationship**: ``PROFESSOR`` -- ``BELONGS_TO`` -- ``DEPARTMENT``

   .. figure:: /_static/images/l2/basic-relationship-dark.png
      :alt: Basic relationship in Chen notation
      :width: 70%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/basic-relationship-light.png
      :alt: Basic relationship in Chen notation
      :width: 70%
      :align: center

      **Binary relationship**: ``PROFESSOR`` -- ``BELONGS_TO`` -- ``DEPARTMENT``

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item::

        **Key Elements**

        - Diamond contains the **verb or verb phrase**
        - Each line links an entity to the relationship
        - This is a **binary relationship** (two entities)

    .. grid-item::

        **Naming Convention**

        .. tip::

           Name relationships with a verb phrase that reads naturally: "Professor ``BELONGS_TO`` Department", "Student ``ENROLLS_IN`` Course_Section". Read the diagram left to right or top to bottom.


Relationship Degree
-------------------

The **degree** of a relationship is the number of entities involved.

.. grid:: 1 1 3 3
    :gutter: 2

    .. grid-item-card:: Binary (Degree 2)
        :class-card: sd-border-info

        - Most common type
        - Two entities participate
        - Example: ``PROFESSOR`` -- ``BELONGS_TO`` -- ``DEPARTMENT``

    .. grid-item-card:: Ternary (Degree 3)
        :class-card: sd-border-info

        - Three entities participate simultaneously
        - Cannot always be decomposed into binaries without losing information
        - Example: ``GRAD_STUDENT`` -- ``TA_ASSIGNMENT`` -- ``COURSE_SECTION`` -- ``PROFESSOR``

    .. grid-item-card:: Recursive (Unary)
        :class-card: sd-border-info

        - An entity is related **to itself**
        - Roles must be labeled to avoid ambiguity
        - Example: ``COURSE`` -- ``HAS_PREREQ`` -- ``COURSE``

.. note::

   **Practical Rule**: The vast majority of relationships in a typical ER diagram are binary. Ternary relationships are rare and should only be used when the association genuinely requires all three entities simultaneously.


Cardinality Ratios
------------------

What Is Cardinality?
~~~~~~~~~~~~~~~~~~~~

**Cardinality** specifies the *maximum* number of relationship instances an entity can participate in. It answers: "How many on each side?"

1:1 --- One-to-One
~~~~~~~~~~~~~~~~~~

Each entity on side A is associated with **at most one** entity on side B, and vice versa.

.. only:: html

   .. figure:: /_static/images/l2/cardinality-1-1-light.png
      :alt: One-to-one cardinality
      :width: 60%
      :align: center
      :class: only-light

      **1:1 Relationship**: ``DEPARTMENT`` -- ``CHAIRS`` -- ``PROFESSOR``

   .. figure:: /_static/images/l2/cardinality-1-1-dark.png
      :alt: One-to-one cardinality
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/cardinality-1-1-light.png
      :alt: One-to-one cardinality
      :width: 60%
      :align: center

      **1:1 Relationship**: ``DEPARTMENT`` -- ``CHAIRS`` -- ``PROFESSOR``

- Each department has **at most one** chair
- Each professor chairs **at most one** department
- **How to read the labels (Chen convention)**: The label next to an entity tells you the maximum number of instances *of that entity* that can participate per instance of the opposite entity. The **1** next to ``DEPARTMENT`` means "for each professor, at most one department"; the **1** next to ``PROFESSOR`` means "for each department, at most one professor"

.. card::
    :class-card: sd-border-warning

    **1:1 relationships are relatively rare.** If you find many of them in your model, consider whether the two entities should be merged into one.

1:N --- One-to-Many
~~~~~~~~~~~~~~~~~~~

Each entity on the "one" side can be associated with **many** entities on the "many" side, but each entity on the "many" side is associated with **at most one** on the other.

.. only:: html

   .. figure:: /_static/images/l2/cardinality-1-n-light.png
      :alt: One-to-many cardinality
      :width: 60%
      :align: center
      :class: only-light

      **1:N Relationship**: ``DEPARTMENT`` -- ``BELONGS_TO`` -- ``PROFESSOR``

   .. figure:: /_static/images/l2/cardinality-1-n-dark.png
      :alt: One-to-many cardinality
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/cardinality-1-n-light.png
      :alt: One-to-many cardinality
      :width: 60%
      :align: center

      **1:N Relationship**: ``DEPARTMENT`` -- ``BELONGS_TO`` -- ``PROFESSOR``

- One department has **many** professors who belong to it
- Each professor belongs to **exactly one** department
- The **N** next to ``PROFESSOR`` means "for each department, potentially many professors"

Other 1:N examples from our use case:

- ``COURSE`` (1) -- ``HAS_SECTION`` -- ``COURSE_SECTION`` (N)
- ``PROFESSOR`` (1) -- ``ADVISED_BY`` -- ``STUDENT`` (N)
- ``PROFESSOR`` (1) -- ``TEACHES`` -- ``COURSE_SECTION`` (N)
- ``DEPARTMENT`` (1) -- ``OFFERS`` -- ``COURSE`` (N)

.. tip::

   **1:N is the most common cardinality** in relational databases. It maps cleanly to a foreign key on the "many" side pointing to the "one" side (covered in Lecture 3).

M:N --- Many-to-Many
~~~~~~~~~~~~~~~~~~~~

Each entity on side A can be associated with **many** entities on side B, *and* vice versa.

.. only:: html

   .. figure:: /_static/images/l2/cardinality-m-n-light.png
      :alt: Many-to-many cardinality
      :width: 60%
      :align: center
      :class: only-light

      **M:N Relationship**: ``STUDENT`` -- ``ENROLLS_IN`` -- ``COURSE_SECTION``

   .. figure:: /_static/images/l2/cardinality-m-n-dark.png
      :alt: Many-to-many cardinality
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/cardinality-m-n-light.png
      :alt: Many-to-many cardinality
      :width: 60%
      :align: center

      **M:N Relationship**: ``STUDENT`` -- ``ENROLLS_IN`` -- ``COURSE_SECTION``

- A student enrolls in **many** course sections
- A course section has **many** students enrolled
- Neither side is limited to one — both carry "many" labels

.. warning::

   **Important**: M:N relationships *cannot* be implemented directly using a simple foreign key. At the logical level (Lecture 3), we will resolve every M:N relationship into a **junction table** (also called an associative entity or bridge table) that holds foreign keys to both sides.


Relationship Attributes
-----------------------

When Do Relationships Have Their Own Attributes?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some facts belong to the **association itself**, not to either participating entity.

.. only:: html

   .. figure:: /_static/images/l2/relationship-attributes-light.png
      :alt: Relationship with attributes
      :width: 70%
      :align: center
      :class: only-light

      **Relationship attributes**: ``grade`` and ``enroll_date`` belong to the ``ENROLLS_IN`` relationship

   .. figure:: /_static/images/l2/relationship-attributes-dark.png
      :alt: Relationship with attributes
      :width: 70%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/relationship-attributes-light.png
      :alt: Relationship with attributes
      :width: 70%
      :align: center

      **Relationship attributes**: ``grade`` and ``enroll_date`` belong to the ``ENROLLS_IN`` relationship

- ``grade`` does not belong to ``STUDENT`` alone (Alice has different grades in different courses) and does not belong to ``COURSE_SECTION`` alone (a section has different grades for different students). It belongs to the **specific pairing** of a student and a section.
- ``enroll_date`` records *when* a particular student enrolled in a particular section: again, it describes the association, not either entity.
- **Test**: Ask "Does this attribute make sense without knowing *both* entities?" If not, it belongs on the relationship.

.. note::

   **Cardinality Matters**: Relationship attributes are most common on **M:N** relationships. On a 1:N relationship, the attribute can usually be moved to the entity on the "many" side without ambiguity. On a 1:1 relationship, it can go on either side.


Total and Partial Participation
--------------------------------

What Are Participation Constraints?
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Cardinality tells us the *maximum* number of instances that can participate. **Participation constraints** tell us the *minimum*: must every instance participate, or is participation optional?

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - 
     - Total (Mandatory)
     - Partial (Optional)
   * - **Rule**
     - **Every** instance of the entity must participate in the relationship
     - **Some** instances may participate; others may not
   * - **Chen Symbol**
     - Double line (=)
     - Single line (---)
   * - **(min, max)**
     - min ≥ 1
     - min = 0
   * - **Implication**
     - Existence dependency
     - No existence dependency
   * - **At physical level**
     - ``NOT NULL`` foreign key or ``CHECK`` constraint
     - Nullable foreign key

.. card::
    :class-card: sd-border-info

    **Who decides?** Participation constraints are not technical decisions. They encode **business rules** that must be elicited from stakeholders. The same schema can have total or partial participation depending on the organization's policies.

Contrasting Participation Patterns
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

**Total on Both Sides: OFFERS**

.. only:: html

   .. figure:: /_static/images/l2/participation-total-both-light.png
      :alt: Total participation on both sides
      :width: 60%
      :align: center
      :class: only-light

      **Total on both sides**: ``DEPARTMENT`` -- ``OFFERS`` -- ``COURSE``

   .. figure:: /_static/images/l2/participation-total-both-dark.png
      :alt: Total participation on both sides
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/participation-total-both-light.png
      :alt: Total participation on both sides
      :width: 60%
      :align: center

      **Total on both sides**: ``DEPARTMENT`` -- ``OFFERS`` -- ``COURSE``

- Both sides have **double lines**: every department must offer ≥1 course, and every course must belong to a department.
- Neither entity can exist without participating.

**Mixed: HELD_IN**

.. only:: html

   .. figure:: /_static/images/l2/participation-mixed-light.png
      :alt: Mixed participation
      :width: 70%
      :align: center
      :class: only-light

      **Mixed participation**: ``COURSE_SECTION`` has total (must meet in a room), ``ROOM`` has partial (can exist unused)

   .. figure:: /_static/images/l2/participation-mixed-dark.png
      :alt: Mixed participation
      :width: 70%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/participation-mixed-light.png
      :alt: Mixed participation
      :width: 70%
      :align: center

      **Mixed participation**: ``COURSE_SECTION`` has total (must meet in a room), ``ROOM`` has partial (can exist unused)

- ``COURSE_SECTION`` has **total** participation (double line): every section must meet in a room.
- ``ROOM`` has **partial** participation (single line): a room can exist without hosting any section.

**Partial on Both Sides: HAS_PREREQ (Recursive)**

.. only:: html

   .. figure:: /_static/images/l2/participation-partial-both-light.png
      :alt: Partial participation on both sides (recursive)
      :width: 60%
      :align: center
      :class: only-light

      **Partial on both sides**: ``COURSE`` -- ``HAS_PREREQ`` -- ``COURSE`` (recursive)

   .. figure:: /_static/images/l2/participation-partial-both-dark.png
      :alt: Partial participation on both sides (recursive)
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/participation-partial-both-light.png
      :alt: Partial participation on both sides (recursive)
      :width: 60%
      :align: center

      **Partial on both sides**: ``COURSE`` -- ``HAS_PREREQ`` -- ``COURSE`` (recursive)

- Both sides have **single lines**: not every course has prerequisites, and not every course is a prerequisite for another.
- This is a **recursive (unary) relationship**: the same entity type participates twice.
- **Role labels** distinguish the two participants: "prerequisite" vs. "successor"


(min, max) Notation
-------------------

A More Precise Alternative
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Instead of just "total" or "partial," we can specify **exact numeric constraints** on each entity's participation.

.. only:: html

   .. figure:: /_static/images/l2/min-max-notation-light.png
      :alt: (min, max) notation
      :width: 60%
      :align: center
      :class: only-light

      **(min, max) notation**: ``PROFESSOR`` -- ``BELONGS_TO`` -- ``DEPARTMENT``

   .. figure:: /_static/images/l2/min-max-notation-dark.png
      :alt: (min, max) notation
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/min-max-notation-light.png
      :alt: (min, max) notation
      :width: 60%
      :align: center

      **(min, max) notation**: ``PROFESSOR`` -- ``BELONGS_TO`` -- ``DEPARTMENT``

- **(1,1)** on ``PROFESSOR``: every professor belongs to *at least 1* and *at most 1* department (mandatory, single-valued)
- **(1,N)** on ``DEPARTMENT``: every department has *at least 1* and *up to N* professors
- **min = 0** means partial participation; **min ≥ 1** means total participation
- **max = 1** means single-valued; **max = N** means multi-valued

.. list-table::
   :widths: 20 30 50
   :header-rows: 1
   :class: compact-table

   * - (min, max)
     - Participation
     - Meaning
   * - (0, 1)
     - Partial
     - Optional, at most one
   * - (0, N)
     - Partial
     - Optional, any number
   * - (1, 1)
     - Total
     - Mandatory, exactly one
   * - (1, N)
     - Total
     - Mandatory, one or more

.. warning::

   **Careful: Two conventions, opposite reading directions.** Chen cardinality ratios are read *across*: the label next to entity A tells you how many A's per B. But (min, max) notation is read *locally*: the label next to entity A tells you how many times A participates. The numbers sit in the same position but mean different things. We follow Elmasri & Navathe's convention for (min, max) throughout this course.

.. note::

   **Does N include 0?** In Chen's cardinality ratios (1:1, 1:N, M:N), the letters N and M mean "many" but do not specify whether zero is allowed. The same label 1:N appears on both ``BELONGS_TO`` (where every department *must* have at least one professor) and ``TEACHES`` (where a professor *may* teach zero sections). The cardinality ratio alone is ambiguous about the minimum. This is precisely why (min, max) notation exists: it makes both the minimum and maximum explicit.


Identifying Relationships
--------------------------

Identifying Relationships (Weak Entity Support)
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

An **identifying relationship** connects a weak entity to its owner entity. It is how the weak entity "borrows" part of its identity.

.. only:: html

   .. figure:: /_static/images/l2/identifying-relationship-light.png
      :alt: Identifying relationship
      :width: 70%
      :align: center
      :class: only-light

      **Identifying relationship**: ``COURSE`` -- ``HAS_SECTION`` -- ``COURSE_SECTION``

   .. figure:: /_static/images/l2/identifying-relationship-dark.png
      :alt: Identifying relationship
      :width: 70%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/identifying-relationship-light.png
      :alt: Identifying relationship
      :width: 70%
      :align: center

      **Identifying relationship**: ``COURSE`` -- ``HAS_SECTION`` -- ``COURSE_SECTION``

- The relationship diamond has **double borders**, matching the weak entity's double rectangle
- The weak entity always has **total participation** (double line): it cannot exist without its owner
- Cardinality is always **1:N** from owner to weak entity (one course has many sections)
- The weak entity's full identity combines the **owner's key** + the **partial key**: ``(course_id, section_no)``

.. tip::

   **Three Markers of a Weak Entity**: (1) Double rectangle for the entity, (2) Double diamond for its identifying relationship, (3) Double line (total participation) connecting them. If you see all three, you know it is a weak entity.




Advanced ER Concepts
====================================================


Specialization & Generalization
--------------------------------

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: Specialization
        :class-card: sd-border-primary

        - Defining **subtypes** from an existing entity based on distinguishing characteristics
        - Top-down process
        - Example: ``PERSON`` specializes into ``STUDENT`` and ``PROFESSOR``

    .. grid-item-card:: Generalization
        :class-card: sd-border-primary

        - Combining entities that share common attributes into a higher-level **superclass**
        - Bottom-up process
        - Example: ``STUDENT`` and ``PROFESSOR`` generalize to ``PERSON``

.. only:: html

   .. figure:: /_static/images/l2/specialization-generalization-light.png
      :alt: Specialization and generalization
      :width: 60%
      :align: center
      :class: only-light

      **ISA hierarchy**: ``PERSON`` specializes into ``STUDENT`` and ``PROFESSOR``

   .. figure:: /_static/images/l2/specialization-generalization-dark.png
      :alt: Specialization and generalization
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/specialization-generalization-light.png
      :alt: Specialization and generalization
      :width: 60%
      :align: center

      **ISA hierarchy**: ``PERSON`` specializes into ``STUDENT`` and ``PROFESSOR``

.. card::
    :class-card: sd-border-info

    **Attribute Inheritance**

    Subclasses inherit *all* superclass attributes plus their own specific ones. A ``STUDENT`` has all ``PERSON`` attributes *and* ``student_id``, ``gpa``, etc.

.. note::

   **Notation**: Specialization and generalization are part of the **Enhanced ER (EER) model**, an extension of Chen's original notation. The ISA symbol (circle or triangle) was not in Chen's 1976 paper but is now standard in most ER modeling textbooks and tools.


Specialization Constraints
---------------------------

Four Constraint Combinations
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. grid:: 1 2 2 2
    :gutter: 2

    .. grid-item-card:: Disjointness Constraint
        :class-card: sd-border-secondary

        **Disjoint (d)**

        An entity can be a member of *at most one* subclass

        - A person is either a student or a professor, not both

        **Overlapping (o)**

        An entity can be a member of *multiple* subclasses simultaneously

        - A person could be both a student and a professor

    .. grid-item-card:: Completeness Constraint
        :class-card: sd-border-secondary

        **Total Specialization**

        Every superclass entity *must* belong to at least one subclass (double line)

        - Every person must be either a student or professor

        **Partial Specialization**

        A superclass entity *may* exist without being in any subclass (single line)

        - A person could exist without being a student or professor

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - Combination
     - Meaning
   * - Disjoint + Total
     - Every entity is in exactly one subclass
   * - Disjoint + Partial
     - Entity is in at most one subclass (or none)
   * - Overlapping + Total
     - Every entity is in at least one subclass (possibly multiple)
   * - Overlapping + Partial
     - Entity may be in zero, one, or multiple subclasses


Specialization Hierarchy
-------------------------

.. only:: html

   .. figure:: /_static/images/l2/specialization-hierarchy-light.png
      :alt: Multi-level specialization hierarchy
      :width: 70%
      :align: center
      :class: only-light

      **Two-level specialization hierarchy**: ``PERSON`` → ``STUDENT``/``PROFESSOR`` → ``GRAD_STUDENT``

   .. figure:: /_static/images/l2/specialization-hierarchy-dark.png
      :alt: Multi-level specialization hierarchy
      :width: 70%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/specialization-hierarchy-light.png
      :alt: Multi-level specialization hierarchy
      :width: 70%
      :align: center

      **Two-level specialization hierarchy**: ``PERSON`` → ``STUDENT``/``PROFESSOR`` → ``GRAD_STUDENT``

- **Level 1** (double lines): ``PERSON`` specializes into ``STUDENT`` and ``PROFESSOR``. **Disjoint** means a person cannot be both simultaneously. **Total** means every person must be one or the other.
- **Level 2** (single lines): ``STUDENT`` specializes into ``GRAD_STUDENT``. **Overlapping** allows additional subclasses. **Partial** means not every student is a grad student.


Ternary Relationships
---------------------

Ternary (and Higher-Degree) Relationships
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When a relationship involves **three or more entities simultaneously**, it's ternary (or n-ary).

.. only:: html

   .. figure:: /_static/images/l2/ternary-relationship-light.png
      :alt: Ternary relationship
      :width: 60%
      :align: center
      :class: only-light

      **Ternary relationship**: ``TA_ASSIGNMENT`` involves ``GRAD_STUDENT``, ``PROFESSOR``, and ``COURSE_SECTION``

   .. figure:: /_static/images/l2/ternary-relationship-dark.png
      :alt: Ternary relationship
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/ternary-relationship-light.png
      :alt: Ternary relationship
      :width: 60%
      :align: center

      **Ternary relationship**: ``TA_ASSIGNMENT`` involves ``GRAD_STUDENT``, ``PROFESSOR``, and ``COURSE_SECTION``

- A ``GRAD_STUDENT`` serves as TA for a ``COURSE_SECTION`` under the supervision of a ``PROFESSOR``
- The assignment depends on **all three entities together**: it cannot be decomposed into binary relationships without losing information
- **Test**: Does knowing (Grad_Student, Course_Section) *and* (Course_Section, Professor) tell us everything? If not, it must remain ternary

.. note::

   **Alternative**: Instead of a ternary relationship, we could model this using **aggregation**: grouping a binary relationship (e.g., ``ENROLLS_IN``) into an abstract entity and relating it to a third entity.


Aggregation
-----------

Aggregation
~~~~~~~~~~~

Aggregation treats a **relationship (and its participating entities) as a higher-level entity** that can participate in other relationships.

- **Why?** In the basic ER model, relationships can only be between entities, not between relationships. Aggregation extends this by allowing a relationship to be treated as an entity.
- **Notation**: Draw a **dashed rectangle** around the relationship diamond and its connected entities to indicate the aggregation.

.. only:: html

   .. figure:: /_static/images/l2/aggregation-diagram-light.png
      :alt: Aggregation example
      :width: 80%
      :align: center
      :class: only-light

      **Aggregation**: The ``ENROLLS_IN`` relationship is treated as an entity that can relate to ``GRAD_STUDENT (TA)``

   .. figure:: /_static/images/l2/aggregation-diagram-dark.png
      :alt: Aggregation example
      :width: 80%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/aggregation-diagram-light.png
      :alt: Aggregation example
      :width: 80%
      :align: center

      **Aggregation**: The ``ENROLLS_IN`` relationship is treated as an entity that can relate to ``GRAD_STUDENT (TA)``

**Reading the Diagram:**

1. **Inside the box**: ``STUDENT`` and ``COURSE_SECTION`` are connected by the M:N relationship ``ENROLLS_IN``.
2. **The dashed box**: The entire relationship (entities + diamond) is grouped into a single abstract entity called an **aggregation**.
3. **Outside the box**: The aggregation participates in a new M:N relationship ``SUPPORTED_BY`` with ``GRAD_STUDENT (TA)``.

.. note::

   Aggregation is from the Extended ER model. It models **relationships about relationships**. If you encounter it in practice, it often signals that the relationship should be promoted to an entity instead.


Categories (Union Types)
-------------------------

Categories (Union Types)
~~~~~~~~~~~~~~~~~~~~~~~~

A **category** (or union type) is a subclass with **multiple possible superclasses**.

- Unlike specialization (one superclass → multiple subclasses), a category is one subclass that can be an instance of **any one of several different superclasses**.
- **Use Case**: If the university tracked ``ACCOUNT_HOLDER`` for billing, it could be a category of ``STUDENT`` and ``DEPARTMENT``.
- **Notation**: Draw a ∪ symbol in a circle connecting the category to its possible superclasses.

.. only:: html

   .. figure:: /_static/images/l2/category-union-type-light.png
      :alt: Category (union type)
      :width: 60%
      :align: center
      :class: only-light

      **Category**: ``ACCOUNT_HOLDER`` can be either a ``STUDENT`` or a ``DEPARTMENT``

   .. figure:: /_static/images/l2/category-union-type-dark.png
      :alt: Category (union type)
      :width: 60%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/l2/category-union-type-light.png
      :alt: Category (union type)
      :width: 60%
      :align: center

      **Category**: ``ACCOUNT_HOLDER`` can be either a ``STUDENT`` or a ``DEPARTMENT``

**Reading the Diagram:**

- **Top row (superclasses)**: ``STUDENT`` and ``DEPARTMENT`` are two independent entity types with no common superclass.
- **The ∪ circle**: Indicates a **union**. An ``ACCOUNT_HOLDER`` is either a ``STUDENT`` or a ``DEPARTMENT``.
- **Bottom (category)**: ``ACCOUNT_HOLDER`` has its own key (``account_id``) and attributes (``balance``).
- **Inheritance**: Each account holder inherits attributes from whichever superclass it belongs to.

.. card::
    :class-card: sd-border-info

    **Key difference from generalization**

    - **Generalization** = one superclass, multiple subclasses (top-down split)
    - **Category** = one subclass, multiple superclasses (bottom-up union)
    - In set theory: generalization is intersection; category is union




Full Use Case Walkthrough
====================================================


Complete Entity Inventory
--------------------------

All Entities in the University System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 15 20 45
   :header-rows: 1
   :class: compact-table

   * - Entity
     - Type
     - Key
     - Notable Attributes
   * - ``PERSON``
     - Strong (Superclass)
     - person_id
     - name, DOB, email, address, phone_numbers (MV)
   * - ``STUDENT``
     - Subclass of Person
     - student_id
     - enrollment_date, gpa, academic_standing
   * - ``PROFESSOR``
     - Subclass of Person
     - professor_id
     - rank, hire_date, salary, office, specializations (MV)
   * - ``GRAD_STUDENT``
     - Subclass of Student
     - (inherits)
     - thesis_topic
   * - ``DEPARTMENT``
     - Strong
     - dept_id
     - dept_name, building, budget
   * - ``COURSE``
     - Strong
     - course_id
     - title, credits, description, level
   * - ``COURSE_SECTION``
     - Weak (owner: Course)
     - section_no (partial)
     - semester, year, capacity, schedule
   * - ``ROOM``
     - Strong
     - room_id
     - building, room_number, capacity, type

.. note::

   **Check**: Are we missing any entities? Should ``SEMESTER`` be an entity or an attribute? Should ``ACADEMIC_RANK`` be promoted to a lookup entity?


Complete Relationship Inventory
--------------------------------

All Relationships in the University System
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 20 25 15 12 12 16
   :header-rows: 1
   :class: compact-table

   * - Relationship
     - Entities
     - Card.
     - Side A
     - Side B
     - Notes
   * - ``BELONGS_TO``
     - Prof → Dept
     - N:1
     - (1,1)
     - (1,N)
     - ---
   * - ``OFFERS``
     - Dept → Course
     - 1:N
     - (1,N)
     - (1,1)
     - ---
   * - ``CHAIRS``
     - Prof → Dept
     - 1:1
     - (0,1)
     - (1,1)
     - start_date
   * - ``TEACHES``
     - Prof → C. Section
     - 1:N
     - (0,N)
     - (1,1)
     - ---
   * - ``ENROLLS_IN``
     - Student → C. Section
     - M:N
     - (0,N)
     - (0,N)
     - grade, enroll_date
   * - ``ADVISED_BY``
     - Student → Prof
     - N:1
     - (1,1)
     - (0,N)
     - ---
   * - ``HAS_SECTION``
     - Course → C. Section
     - 1:N
     - (1,N)
     - (1,1)
     - identifying
   * - ``HELD_IN``
     - C. Section → Room
     - N:1
     - (1,1)
     - (0,N)
     - time_slot
   * - ``HAS_PREREQ``
     - Course → Course
     - M:N
     - (0,N)
     - (0,N)
     - recursive

.. note::

   **Reading the table**: Card. is written as Side A:Side B. The (min, max) is read locally: the label next to an entity tells you how many times *that entity* participates.


Design Decisions & Trade-offs
------------------------------

Five Key Design Trade-offs
~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. **Entity vs. Attribute**: Should "semester" be an entity or just an attribute of ``COURSE_SECTION``? If we need semester-level data (start/end dates, holidays), promote it to an entity.

2. **Entity vs. Relationship**: Is ``ENROLLMENT`` an entity or a relationship? If it has many attributes and participates in other relationships, promote it to an entity.

3. **Attribute vs. Lookup Entity**: Should ``rank`` remain a constrained attribute or become ``ACADEMIC_RANK``? Apply the promotion test.

4. **Weak vs. Strong Entity**: Could ``COURSE_SECTION`` have its own unique ID (CRN)? If so, it becomes a strong entity.

5. **Generalization Depth**: How many levels of hierarchy? Balance based on attribute overlap and distinct behaviors.

.. tip::

   **Key Principle**: There is no single correct answer. Every design choice should be justified by asking: *What question does this design answer? What would break if we chose differently?*




Wrap-Up & Practice
====================================================


Common Mistakes to Avoid
-------------------------

Five Common Modeling Errors
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - Mistake
     - Description
   * - **Fan Trap**
     - Two 1:N relationships fan out from the same entity, creating ambiguous paths. Example: ``DEPARTMENT`` ← ``PROFESSOR`` and ``DEPARTMENT`` → ``COURSE``: we cannot determine which professor teaches which course without an explicit ``TEACHES`` relationship.
   * - **Chasm Trap**
     - A path between two entities passes through a partial participation, creating gaps. Example: not all professors teach, so querying "which department offers which section through professors" has missing links for non-teaching professors.
   * - **Redundant Relationships**
     - Adding a direct relationship when it can be derived through existing paths. Example: direct ``STUDENT`` → ``DEPARTMENT`` when it can be derived through ``ENROLLS_IN`` → ``COURSE_SECTION`` → ``COURSE`` → ``OFFERS`` → ``DEPARTMENT``.
   * - **Attribute vs. Entity Confusion**
     - Modeling something as an attribute that should be an entity. Example: making ``department_name`` an attribute of ``PROFESSOR`` instead of creating a ``DEPARTMENT`` entity.
   * - **Missing Constraints**
     - Drawing entities and relationships without specifying cardinality and participation. The model is incomplete without these.


Quality Checklist
-----------------

Conceptual Model Quality Checklist
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. card::
    :class-card: sd-border-success

    **Use this as your rubric**

    - ☑ Every entity has a clearly defined primary key (or partial key for weak entities)
    - ☑ All attributes are classified: simple, composite, multivalued, derived
    - ☑ Every relationship has a cardinality ratio specified (1:1, 1:N, M:N)
    - ☑ Every relationship has participation constraints (total/partial or min, max)
    - ☑ Weak entities have identifying relationships with double-bordered notation
    - ☑ Recursive relationships have role labels on both sides
    - ☑ Specialization/generalization constraints specified: disjoint/overlapping, total/partial
    - ☑ No redundant relationships (can it be derived from existing paths?)
    - ☑ Relationship attributes are placed on the relationship, not on entities
    - ☑ All business rules from requirements are captured in the model
    - ☑ The model has been reviewed with stakeholders for accuracy


Key Takeaways
-------------

Six Key Takeaways
~~~~~~~~~~~~~~~~~

1. Conceptual models capture **what** data exists and **how** it relates, independent of technology

2. Chen notation uses distinct symbols: **rectangles** (entities), **ovals** (attributes), **diamonds** (relationships), **lines** (connections)

3. Entities can be **strong or weak**; attributes can be **simple, composite, multivalued, derived**

4. Relationships have **degree**, **cardinality ratios**, and **participation constraints**; (min, max) notation resolves ambiguities

5. Extended ER (EER) adds **specialization/generalization**, **aggregation**, and **categories**

6. Good models are **validated against business rules** and reviewed with stakeholders