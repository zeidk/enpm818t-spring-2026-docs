====================================================
L7: DML, Transactions, and Python Integration
====================================================

Overview
--------

This lecture covers everything needed to populate and maintain a PostgreSQL
database from both SQL and Python. Starting from the ``university_db`` schema
built in L6, we write ``INSERT``, ``UPDATE``, and ``DELETE`` statements,
explore the full range of ``RETURNING`` and ``ON CONFLICT`` variants, and
then wrap multi-statement operations in explicit transactions. The ACID
properties, isolation levels, and the lost-update problem are examined with
live two-session demos. The second half of the lecture introduces
**psycopg3**: connecting from Python, parameterized queries, the
``conn.transaction()`` context manager, connection pooling, and the
five-layer repository pattern required for GP2.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Use ``SELECT`` at the level needed to verify DML results (full coverage in L8).
- Write correct ``INSERT``, ``UPDATE``, and ``DELETE`` statements, including multi-row, ``RETURNING``, and upsert variants.
- Explain the four ACID properties and describe what each one prevents.
- Control transactions with ``BEGIN``, ``COMMIT``, ``ROLLBACK``, and ``SAVEPOINT``.
- Connect to PostgreSQL from Python using **psycopg3** and execute parameterized queries safely.
- Structure a Python project using the repository pattern.
- Generate realistic seed data for the university schema using an LLM prompt.

Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   l7_lecture
   l7_exercises
   l7_quiz
   l7_references
   l7_cheat_sheet

Next Steps
----------

- In the next lecture (**L8: Joins, Subqueries, and Aggregates**), we will cover:

  - ``SELECT`` fundamentals: ``WHERE``, ``ORDER BY``, ``LIMIT``, ``OFFSET``.
  - Join types: ``INNER``, ``LEFT``, ``RIGHT``, ``FULL``, ``CROSS``, self-join.
  - Aggregates and grouping: ``GROUP BY``, ``HAVING``, ``COUNT``, ``SUM``, ``AVG``.
  - Subqueries: correlated and non-correlated; ``EXISTS``, ``IN``, scalar subqueries.

- Before next class: seed ``university_db`` (use the LLM prompt from the seeding
  slide), and complete the take-home exercises (Exercises 3 and 4 in the exercises page).
- Optional reading: Silberschatz Ch. 3 *or* Elmasri & Navathe Ch. 6.
