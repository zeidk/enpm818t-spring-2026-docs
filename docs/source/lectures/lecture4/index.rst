====================================================
L4-L5: Normalization & Denormalization
====================================================

Overview
--------

This lecture covers the theory and practice of database normalization and
denormalization. Starting from the problems caused by poorly designed tables
(insertion, deletion, and update anomalies), we develop the formal tools needed
to fix them: functional dependencies, Armstrong's axioms, and attribute closures.
These tools drive the normal form hierarchy (1NF, 2NF, 3NF, BCNF) and the
decomposition algorithms (3NF synthesis, BCNF decomposition) that produce
well-structured schemas. The lecture concludes with strategic denormalization:
when and how to intentionally reintroduce redundancy for read-heavy workloads.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Define functional dependencies and apply Armstrong's axioms to derive closures.
- Identify and explain insertion, deletion, and update anomalies.
- Distinguish between 1NF, 2NF, 3NF, and BCNF with practical examples.
- Decompose relations into higher normal forms while preserving lossless joins.
- Test decompositions for dependency preservation.
- Apply normalization algorithms to convert any relation to 3NF or BCNF.
- Justify strategic denormalization decisions with performance trade-offs.
- Design materialized views and redundant columns to optimize read-heavy workloads.

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

- In the next lecture (**L6: Physical Model**), we will cover:

  - Relational algebra operators: selection, projection, join, set operations.
  - SQL: SELECT, FROM, WHERE, GROUP BY, HAVING, ORDER BY.
  - Joins: INNER, LEFT, RIGHT, FULL, CROSS.

- Complete the normalization exercises from today.
- Read (optional): Elmasri & Navathe Ch. 6 to 8 *or* Silberschatz Ch. 3 to 6.