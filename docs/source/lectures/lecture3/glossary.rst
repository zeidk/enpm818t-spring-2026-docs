====================================================
Glossary
====================================================

:ref:`A <t3-glossary-a>` · :ref:`B <t3-glossary-b>` · :ref:`C <t3-glossary-c>` · :ref:`D <t3-glossary-d>` · :ref:`F <t3-glossary-f>` · :ref:`I <t3-glossary-i>` · :ref:`J <t3-glossary-j>` · :ref:`K <t3-glossary-k>` · :ref:`L <t3-glossary-l>` · :ref:`N <t3-glossary-n>` · :ref:`P <t3-glossary-p>` · :ref:`R <t3-glossary-r>` · :ref:`S <t3-glossary-s>` · :ref:`T <t3-glossary-t>` · :ref:`U <t3-glossary-u>`

----


.. _t3-glossary-a:

A
=

.. glossary::

   Alternate Key
      A candidate key that was *not* chosen as the primary key. Enforced
      with a ``UNIQUE`` constraint in SQL. Example: ``student_id`` in
      ``STUDENT`` when ``person_id`` is the PK.

   Atomic Value
      An indivisible value stored in a single cell of a relation. The
      relational model requires all attribute values to be atomic (First
      Normal Form). No arrays, comma-separated lists, or nested structures.

   Attribute (Relational)
      A named column of a relation. Each attribute has a domain (set of
      allowable values). Example: ``first_name``, ``gpa``, ``dept_id``.


.. _t3-glossary-b:

B
=

.. glossary::

   Bridge Table
      See :term:`Junction Table`.


.. _t3-glossary-c:

C
=

.. glossary::

   Candidate Key
      A minimal superkey: a set of one or more attributes that uniquely
      identifies each tuple, with no unnecessary attributes. One candidate
      key is chosen as the primary key; others become alternate keys.

   Cardinality (of a relation)
      The number of tuples (rows) in a particular relation instance at a
      point in time. Changes with every ``INSERT``, ``UPDATE``, or ``DELETE``.

   Cascade Behavior
      The action taken on child rows when a referenced parent PK is deleted
      or updated. Options include ``ON DELETE CASCADE`` (delete children),
      ``ON DELETE SET NULL`` (set FK to NULL), and ``ON DELETE RESTRICT``
      (prevent parent deletion).

   Category (Relational Mapping)
      A union type mapped to a table with a surrogate PK, a type
      discriminator column, and mutually exclusive nullable FKs to each
      superclass. Only one FK is non-NULL per row.

   Composite FK
      A foreign key consisting of multiple columns that together reference
      a composite primary key in another table. Example:
      ``ENROLLMENT``.(``course_id``, ``section_no``) referencing
      ``COURSE_SECTION``.(``course_id``, ``section_no``).

   Composite Key
      A primary key composed of two or more attributes that together
      uniquely identify a tuple. Common in junction tables and weak entity
      tables. Example: (``course_id``, ``section_no``) in
      ``COURSE_SECTION``.

   Cross-Reference
      A 1:1 mapping strategy (Option C) used when both sides have partial
      participation. The FK is placed on the side with fewer NULLs and
      constrained with ``UNIQUE``.

   Crow's Foot Notation
      The industry-standard notation for logical data models. Entities are
      drawn as rectangles with columns listed inside. Relationships are
      lines between tables with fork/bar/circle symbols at the ends to
      indicate cardinality and participation.


.. _t3-glossary-d:

D
=

.. glossary::

   Degree (of a relation)
      The number of attributes (columns) in a relation schema. A property
      of the schema that rarely changes.

   Discriminator (Category)
      A column in a category table that indicates which superclass a given
      row belongs to. Example: ``owner_type`` in ``VEHICLE_OWNER`` with
      values 'person', 'company', or 'bank'.

   Domain
      The set of allowable values for an attribute. Specified as a data type
      plus optional constraints. Example: ``gpa`` has domain [0.0, 4.0].


.. _t3-glossary-f:

F
=

.. glossary::

   First Normal Form (1NF)
      A relation is in 1NF if every attribute value is atomic (indivisible).
      No repeating groups, no arrays, no comma-separated lists. Covered in
      detail in L4.

   Foreign Key (FK)
      An attribute (or set of attributes) in one table that references the
      primary key of another table, enforcing referential integrity. Every
      FK value must match an existing PK value or be NULL (if nullable).

   Functional Dependency
      A constraint where the value of one set of attributes determines the
      value of another. Formally: X -> Y means that for any two tuples with
      the same X values, their Y values must also be the same. Foundational
      to normalization (L4).


.. _t3-glossary-i:

I
=

.. glossary::

   ISA Mapping
      The process of converting specialization/generalization hierarchies
      into relational tables. Three strategies exist: Strategy A (separate
      tables), Strategy B (subclass only), and Strategy C (single table).


.. _t3-glossary-j:

J
=

.. glossary::

   Junction Table
      A table created to represent an M:N relationship. Its primary key is
      the composite of both participating entities' PKs, and each component
      is also a foreign key. Also called a bridge table or associative table.
      Example: ``ENROLLMENT`` for the Student-Course_Section M:N relationship.


.. _t3-glossary-k:

K
=

.. glossary::

   Key Attribute
      An attribute that participates in a key (superkey, candidate key,
      primary key, or alternate key). Key attributes enforce uniqueness
      and are used to identify tuples.


.. _t3-glossary-l:

L
=

.. glossary::

   Logical Data Model
      The second stage of database design that translates the conceptual
      model into relational schemas (tables, columns, keys, constraints).
      DBMS-family specific (relational vs. NoSQL) but not tied to a
      particular product or version.

   Lookup Table
      A reference table that constrains a column to a fixed set of valid
      values while providing metadata (display name, sort order, description).
      Serves the same purpose as an enum at the database level. Example:
      ``ACADEMIC_RANK`` with columns ``rank_code``, ``rank_name``,
      ``rank_order``.


.. _t3-glossary-n:

N
=

.. glossary::

   Natural Key
      A key with real-world meaning. Examples: ``email``, ``ssn``, ``isbn``.
      Natural keys may change over time or not be truly unique, so surrogate
      keys are often preferred as PKs.

   N-tuple
      A single element of a relation: an ordered list of n values
      (d1, d2, ..., dn) where each di is drawn from domain Di. Informally
      called a row or record.


.. _t3-glossary-p:

P
=

.. glossary::

   Primary Key (PK)
      The candidate key chosen by the designer as the main identifier for
      a relation. Must be unique and non-null for every tuple. In Crow's
      Foot notation, marked with a PK label.

   Projection
      A relational algebra operation that selects a subset of columns from
      a relation. Covered in L5.


.. _t3-glossary-r:

R
=

.. glossary::

   Referential Integrity
      The constraint that every foreign key value must either match an
      existing primary key value in the referenced table or be NULL (if
      the FK is nullable). Enforced by the DBMS at the database level.

   Relation
      A named set of tuples with a fixed schema. Informally called a table.
      Formally, a subset of the Cartesian product of its attribute domains.

   Relation Instance (Extension)
      A specific set of tuples conforming to a relation schema at a point
      in time. Changes with every ``INSERT``, ``UPDATE``, or ``DELETE``.

   Relation Schema (Intension)
      The structure of a relation: its name, attribute names, and their
      domains. Analogous to a class definition in OOP. Changes rarely
      (only via ``ALTER TABLE``).


.. _t3-glossary-s:

S
=

.. glossary::

   Self-Referencing FK
      A foreign key that references the primary key of the *same* table.
      Used for recursive relationships. Example: ``COURSE_PREREQ`` where
      both ``successor_id`` and ``prereq_id`` reference ``COURSE``.

   Seven-Step Mapping Algorithm
      A systematic procedure to convert an EER diagram into relational
      schemas: (1) strong entities, (2) weak entities, (3) binary 1:1,
      (4) binary 1:N, (5) binary M:N, (6) multivalued attributes,
      (7) n-ary relationships. ISA and categories are sometimes added
      as Steps 8 and 9.

   Superkey
      Any set of one or more attributes that uniquely identifies each
      tuple in a relation. Need not be minimal (may contain unnecessary
      attributes). Every candidate key is a superkey, but not every
      superkey is a candidate key.

   Surrogate Key
      A system-generated key with no business meaning. Examples:
      auto-increment integers (``SERIAL``), UUIDs. Preferred as PKs
      for stability (they never change).


.. _t3-glossary-t:

T
=

.. glossary::

   Tuple
      A single row (record) in a relation. Formally, an n-tuple is an
      ordered list of values, one per attribute, drawn from the
      corresponding domains.


.. _t3-glossary-u:

U
=

.. glossary::

   Union Type
      See :term:`Category (Relational Mapping)`.
