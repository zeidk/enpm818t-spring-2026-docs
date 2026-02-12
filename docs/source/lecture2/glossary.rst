====================================================
Glossary
====================================================

:ref:`A <t2-glossary-a>` · :ref:`B <t2-glossary-b>` · :ref:`C <t2-glossary-c>` · :ref:`D <t2-glossary-d>` · :ref:`E <t2-glossary-e>` · :ref:`G <t2-glossary-g>` · :ref:`I <t2-glossary-i>` · :ref:`K <t2-glossary-k>` · :ref:`L <t2-glossary-l>` · :ref:`M <t2-glossary-m>` · :ref:`O <t2-glossary-o>` · :ref:`P <t2-glossary-p>` · :ref:`R <t2-glossary-r>` · :ref:`S <t2-glossary-s>` · :ref:`T <t2-glossary-t>` · :ref:`U <t2-glossary-u>` · :ref:`W <t2-glossary-w>`

----


.. _t2-glossary-a:

A
=

.. glossary::

   Aggregation
      An EER modeling concept that treats a relationship (and its participating
      entities) as a higher-level entity that can itself participate in other
      relationships. Represented by a dashed rectangle around a relationship
      in Chen notation.

   Attribute
      A named property of an entity or relationship that maps each instance
      to a value from a defined domain. Examples: ``name``, ``gpa``,
      ``enrollment_date``.


.. _t2-glossary-b:

B
=

.. glossary::

   Binary Relationship
      A relationship that connects exactly two entity types. The most common
      type of relationship in ER diagrams. Example: ``STUDENT`` --
      ``ENROLLS_IN`` -- ``COURSE``.


.. _t2-glossary-c:

C
=

.. glossary::

   Candidate Key
      A minimal superkey — a set of one or more attributes that uniquely
      identifies each entity instance, with no unnecessary attributes.
      One candidate key is chosen as the primary key.

   Cardinality Ratio
      The maximum number of relationship instances in which an entity can
      participate. Expressed as 1:1 (one-to-one), 1:N (one-to-many), or
      M:N (many-to-many).

   Category (Union Type)
      An EER modeling concept representing a subclass with multiple possible
      superclasses. Unlike generalization (one superclass → many subclasses),
      a category is one subclass that can be an instance of any one of several
      superclasses. Represented with a ∪ symbol in Chen notation.

   Chasm Trap
      A common ER modeling error where a path between two entities passes
      through a partial participation, creating gaps in the derivable
      information.

   Chen Notation
      The original ER diagram notation introduced by Peter Chen in 1976.
      Uses rectangles for entities, ovals for attributes, diamonds for
      relationships, and lines for connections. The standard notation for
      conceptual modeling in academia.

   Completeness Constraint
      In specialization hierarchies, specifies whether every superclass instance
      must belong to a subclass (total) or may exist without belonging to any
      subclass (partial).

   Composite Attribute
      An attribute that can be subdivided into smaller sub-attributes, each with
      independent meaning. Example: ``address`` → {``street``, ``city``,
      ``state``, ``zip``}. Represented as an oval with connected sub-ovals
      in Chen notation.

   Composite Key
      A primary key composed of two or more attributes that together uniquely
      identify an entity instance. Common in junction tables and weak entities.

   Conceptual Data Model
      The first stage of database design that captures *what* data exists and
      *how* it relates, independent of any specific database technology.
      Expressed using ER diagrams in Chen notation.

   Constrained Domain
      An attribute whose values are restricted to a small, fixed set.
      Example: ``semester`` ∈ {Fall, Spring, Summer}. Can be enforced at
      the physical level using ``ENUM`` types or ``CHECK`` constraints.

   Crow's Foot Notation
      An alternative ER notation that represents entities as rectangles with
      attribute lists, and uses fork-shaped symbols for cardinality. More
      common in industry tools than Chen notation.


.. _t2-glossary-d:

D
=

.. glossary::

   Degree (of a relationship)
      The number of entity types participating in a relationship. Most relationships
      are binary (degree 2); ternary relationships (degree 3) are less common.

   Derived Attribute
      An attribute whose value can be calculated or derived from other attributes.
      Example: ``age`` derived from ``date_of_birth``. Represented as a dashed
      oval in Chen notation. Not stored in the database; computed on query.

   Discriminator
      See :term:`Partial Key`.

   Disjointness Constraint
      In specialization hierarchies, specifies whether an entity can belong to
      multiple subclasses simultaneously (overlapping) or only one (disjoint).


.. _t2-glossary-e:

E
=

.. glossary::

   EER Model
      **Enhanced Entity-Relationship Model** — an extension of the original
      ER model that adds specialization/generalization, aggregation, and
      categories (union types). Introduced in the 1980s to support more
      complex modeling scenarios.

   Entity
      A distinctly identifiable thing (person, place, object, event, or concept)
      in the real world about which data is stored. Represented as a rectangle
      in Chen notation. Example: ``STUDENT``, ``COURSE``, ``DEPARTMENT``.

   Entity Integrity
      The guarantee that every entity instance is distinguishable from all
      others, enforced through primary keys. One of the fundamental integrity
      constraints in relational databases.

   Entity Set
      The collection of all current instances of an entity type at a point in
      time. Example: The entity set for ``STUDENT`` contains all currently
      enrolled students.

   Entity Type
      The schema or structure that defines an entity — its name and attributes.
      Example: ``STUDENT`` is an entity type; Alice (student_id: S101) is an
      entity instance.

   ER Diagram
      **Entity-Relationship Diagram** — a graphical representation of entities,
      attributes, and relationships in a conceptual data model. Typically drawn
      using Chen notation or Crow's Foot notation.


.. _t2-glossary-g:

G
=

.. glossary::

   Generalization
      A bottom-up process of identifying common attributes across multiple entity
      types and creating a superclass to hold them. Example: ``STUDENT`` and
      ``PROFESSOR`` both have ``name`` and ``DOB``, so generalize to ``PERSON``.


.. _t2-glossary-i:

I
=

.. glossary::

   Identifying Relationship
      A relationship that connects a weak entity to its owner entity, allowing
      the weak entity to "borrow" part of its identity. Represented as a double
      diamond in Chen notation, with double lines connecting to the weak entity.

   ISA Relationship
      "Is-a" relationship used in specialization/generalization hierarchies to
      connect a subclass to its superclass. Represented as a triangle or circle
      in EER diagrams. Example: ``STUDENT`` ISA ``PERSON``.


.. _t2-glossary-k:

K
=

.. glossary::

   Key Attribute
      An attribute that uniquely identifies each instance of an entity. Represented
      with a solid underline in Chen notation. Example: ``student_id`` for
      ``STUDENT``.


.. _t2-glossary-l:

L
=

.. glossary::

   Logical Data Model
      The second stage of database design that translates the conceptual model
      into relational schemas (tables, columns, keys). DBMS-family specific but
      not yet tied to a particular product or version.

   Lookup Entity
      An entity created to represent a constrained domain when the values have
      their own attributes, change over time, or are referenced by multiple
      other entities. Example: ``ACADEMIC_RANK`` instead of a simple ``rank``
      attribute with a fixed set of values.


.. _t2-glossary-m:

M
=

.. glossary::

   (min, max) Notation
      A precise way to specify participation constraints by indicating the
      minimum and maximum number of times an entity can participate in a
      relationship. Example: (1,N) means "at least 1, up to N". Read locally:
      the label next to an entity describes that entity's participation.

   Multivalued Attribute
      An attribute that can hold multiple values for a single entity instance.
      Example: ``phone_numbers`` for ``STUDENT`` (a student may have 2 or 3
      phone numbers). Represented as a double oval in Chen notation. Becomes
      a separate table at the logical level.

   M:N Relationship
      **Many-to-Many** — a relationship where each entity on side A can be
      associated with many entities on side B, and vice versa. Example:
      ``STUDENT`` -- ``ENROLLS_IN`` -- ``COURSE_SECTION``. Cannot be implemented
      directly in relational databases; requires a junction table.


.. _t2-glossary-o:

O
=

.. glossary::

   Owner Entity
      See :term:`Strong Entity`. In the context of weak entities, the strong
      entity on which a weak entity depends for its identity. Example:
      ``COURSE`` is the owner entity for ``COURSE_SECTION``.


.. _t2-glossary-p:

P
=

.. glossary::

   Partial Key
      An attribute (or set of attributes) that partially identifies instances
      of a weak entity within the context of its owner entity. Represented
      with a dashed underline in Chen notation. Example: ``section_no`` for
      ``COURSE_SECTION`` — it only uniquely identifies a section when combined
      with ``course_id``.

   Partial Participation
      A participation constraint where not all instances of an entity must
      participate in a relationship. Represented as a single line in Chen
      notation. Example: Not all professors teach every semester.

   Participation Constraint
      Specifies the minimum number of relationship instances in which an entity
      must participate. Distinguishes between total (mandatory) and partial
      (optional) participation.

   Physical Data Model
      The third stage of database design that specifies how the logical model
      will be implemented in a specific DBMS. Includes indexes, storage engines,
      data types, partitioning, and performance tuning decisions.

   Primary Key
      The candidate key chosen as the main identifier for an entity. Must be
      unique and non-null for every instance. Represented with a solid underline
      in Chen notation.


.. _t2-glossary-r:

R
=

.. glossary::

   Recursive Relationship
      A relationship where an entity is related to itself. Roles must be labeled
      to distinguish the two participants. Example: ``COURSE`` --
      ``HAS_PREREQ`` -- ``COURSE`` with roles "prerequisite" and "successor".
      Also called a unary relationship.

   Relationship
      A meaningful association between two or more entities. Represented as a
      diamond in Chen notation. Example: ``PROFESSOR`` -- ``TEACHES`` --
      ``COURSE_SECTION``.

   Relationship Attribute
      An attribute that belongs to a relationship rather than to any participating
      entity. Example: ``grade`` on the ``ENROLLS_IN`` relationship — it doesn't
      belong to ``STUDENT`` alone or ``COURSE_SECTION`` alone, but to the
      specific pairing.

   Role Label
      A label used to distinguish the function of an entity in a relationship,
      especially important in recursive relationships. Example: In
      ``PROFESSOR`` -- ``SUPERVISES`` -- ``PROFESSOR``, roles might be
      "supervisor" and "supervisee".


.. _t2-glossary-s:

S
=

.. glossary::

   Simple Attribute
      An atomic attribute that cannot be meaningfully subdivided. Also called
      a single-valued attribute. Example: ``gpa``, ``student_id``.
      Represented as a regular oval in Chen notation.

   Specialization
      A top-down process of defining subtypes of an entity based on distinguishing
      characteristics. Example: ``PERSON`` specializes into ``STUDENT`` and
      ``PROFESSOR``. The inverse of generalization.

   Specialization Hierarchy
      A tree-like structure of ISA relationships connecting superclasses to
      subclasses. Can have multiple levels. Example: ``PERSON`` → ``STUDENT``
      → ``GRAD_STUDENT``.

   Strong Entity
      An entity that has its own primary key and exists independently.
      Represented as a single rectangle in Chen notation. Example: ``STUDENT``,
      ``PROFESSOR``, ``DEPARTMENT``.

   Superkey
      Any set of one or more attributes that uniquely identifies each entity
      instance. Need not be minimal (may contain unnecessary attributes).
      Example: {student_id, name, gpa} is a superkey for ``STUDENT``.


.. _t2-glossary-t:

T
=

.. glossary::

   Ternary Relationship
      A relationship involving exactly three entity types. Example:
      ``GRAD_STUDENT`` -- ``TA_ASSIGNMENT`` -- ``COURSE_SECTION`` --
      ``PROFESSOR``. Used when the association genuinely requires all three
      entities simultaneously and cannot be decomposed into binaries without
      losing information.

   Total Participation
      A participation constraint where every instance of an entity must
      participate in the relationship at least once. Represented as a double
      line in Chen notation. Example: Every ``COURSE_SECTION`` must be held
      in a ``ROOM``.


.. _t2-glossary-u:

U
=

.. glossary::

   Unary Relationship
      See :term:`Recursive Relationship`.


.. _t2-glossary-w:

W
=

.. glossary::

   Weak Entity
      An entity that cannot be uniquely identified by its own attributes alone
      and depends on a strong entity (the owner) for its identity. Uses a
      partial key plus the owner's key. Represented as a double rectangle in
      Chen notation. Example: ``COURSE_SECTION`` depends on ``COURSE``.
