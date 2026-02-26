====================================================
L3: Logical Data Modeling
====================================================

Overview
--------

This lecture introduces logical data modeling by converting conceptual ER
diagrams (from L2) into relational schemas using the 7-step ER-to-Relational
mapping algorithm. You will learn the core components of the relational model
(relations, tuples, attributes, keys), understand how to read and draw Crow's
Foot diagrams, and systematically map strong entities, weak entities, 1:1, 1:N,
and M:N relationships, multivalued attributes, n-ary relationships, ISA
hierarchies, and categories into tables and foreign keys. The session includes
a complete mapping of the university course management system introduced in L2.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Identify the core components of a relational database (relations, tuples, attributes, keys).
- Explain the role of primary keys, foreign keys, and referential integrity.
- Apply table design best practices and recognize common pitfalls.
- Apply the 7-step ER-to-Relational mapping algorithm to convert a Chen EER diagram into relational schemas.
- Map strong entities, weak entities, 1:1, 1:N, and M:N relationships to tables and foreign keys.
- Handle multivalued, composite, and derived attributes during mapping.
- Map ISA hierarchies and categories (union types) to relational schemas.
- Read and draw Crow's Foot notation as the standard logical-level representation.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   lecture
   quiz
   exercises
   glossary
   references

Next Steps
----------

- In the next lecture, we will cover **Normalization and Denormalization**:

  - Functional Dependencies and Armstrong's Axioms.
  - Normal Forms: 1NF -> 2NF -> 3NF -> BCNF.
  - Anomalies: insertion, deletion, and update anomalies.
  - Decomposition: lossless join and dependency preservation.
  - Denormalization: when and why to break the rules.

- Complete the mapping exercise from today.
- Begin thinking about how your project domain's conceptual model maps to tables.
- Read (optional): Elmasri & Navathe Ch. 9-11 *or* Silberschatz Ch. 7.
