====================================================
L6: From Logical to Physical
====================================================

Overview
--------

This lecture bridges the gap between a completed logical schema and a
running PostgreSQL database. Starting from the university ERD, we
translate every entity, relationship, and constraint into concrete
``CREATE TABLE`` statements. Along the way we choose the right data type
for every column, apply the full suite of integrity constraints
(``PRIMARY KEY``, ``FOREIGN KEY``, ``NOT NULL``, ``UNIQUE``, ``CHECK``,
``EXCLUDE``), implement ISA hierarchies and category patterns using the
shared-PK strategy, and evolve a live schema safely with ``ALTER TABLE``.
The lecture concludes with ``DELETE``, ``TRUNCATE``, and ``DROP``,
naming conventions, and the six most common DDL mistakes to avoid.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Map a logical schema to physical ``CREATE TABLE`` statements.
- Select appropriate PostgreSQL data types for every attribute.
- Write the full range of integrity constraints correctly, including the ``NULL`` traps.
- Recognize ISA hierarchies and categories as specific PRIMARY KEY and CHECK constraint patterns.
- Evolve a live schema safely with ``ALTER TABLE`` and distinguish ``DROP`` from ``TRUNCATE``.
- Apply PostgreSQL-specific DDL: ``GENERATED ALWAYS AS IDENTITY``, deferrable constraints, ``EXCLUDE``.

Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l6_lecture
   l6_exercises
   l6_quiz
   l6_references
   l6_cheat_sheet

Next Steps
----------

- In the next lecture (**L7: DML, Transactions, and Python**), we will cover:

  - ``INSERT``, ``UPDATE``, ``DELETE``: populating and modifying the university schema.
  - Transactions: ACID properties, ``BEGIN`` / ``COMMIT`` / ``ROLLBACK``, savepoints.
  - **psycopg3**: connecting to PostgreSQL from Python, parameterized queries, connection pooling.
  - Assignment: load the full university dataset from CSV using Python and verify with SQL.

- Complete the DDL exercises from today using your live ``university_db`` in DataGrip.
- Optional reading: Elmasri & Navathe Ch. 3-4 *or* Silberschatz Ch. 4-5.
