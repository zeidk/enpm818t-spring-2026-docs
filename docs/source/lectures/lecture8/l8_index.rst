====================================================
L8: JOINs, Query Execution, and Indexing
====================================================

Overview
--------

This lecture covers SQL JOINs in depth -- from the conceptual foundations in
Cartesian products and relational algebra through every practical join type
available in PostgreSQL. Starting from the sample ``customers`` / ``orders``
schema, we work through ``INNER JOIN``, ``LEFT JOIN``, ``RIGHT JOIN``,
``FULL OUTER JOIN``, ``CROSS JOIN``, self-joins, semi-joins (``EXISTS``),
anti-joins (``NOT EXISTS``), and the PostgreSQL-specific ``LATERAL`` join.
The second half of the lecture explores **how** PostgreSQL actually executes
joins: logical vs. physical join strategies (nested loop, hash join, merge
join), reading ``EXPLAIN`` output, Big O analysis of join algorithms, disk
and memory storage architecture (heap pages, ``shared_buffers``,
``work_mem``), and B+ tree indexing for join-heavy workloads.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the idea behind a database join and connect it to the Cartesian product and relational algebra.
- Choose the right join type (``INNER``, ``LEFT``, ``RIGHT``, ``FULL``, ``CROSS``, self-join, semi/anti) for a given task.
- Distinguish ``ON`` vs ``WHERE`` behavior for inner and outer joins.
- Use ``EXISTS`` / ``NOT EXISTS`` for semi-join and anti-join patterns.
- Explain the difference between logical joins and physical join strategies.
- Predict approximate join performance using Big O notation.
- Read basic PostgreSQL ``EXPLAIN`` output and interpret join nodes.
- Design indexes (especially B+ tree and composite) that support join-heavy queries.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l8_lecture
   l8_exercises
   l8_quiz
   l8_references
   l8_cheat_sheet

Next Steps
----------

- In the next lecture (**L9**), we will cover:

  - Subqueries: correlated and non-correlated; ``EXISTS``, ``IN``, scalar subqueries.
  - Aggregates and grouping: ``GROUP BY``, ``HAVING``, ``COUNT``, ``SUM``, ``AVG``.
  - Window functions: ``ROW_NUMBER``, ``RANK``, ``DENSE_RANK``, cumulative sums.
  - Advanced grouping: ``GROUPING SETS``, ``CUBE``, ``ROLLUP``.

- Before next class: complete the take-home exercises (Exercises 3 and 4 on
  the exercises page) and experiment with ``EXPLAIN (ANALYZE, BUFFERS)`` on
  your own queries.
- Optional reading: Silberschatz Ch. 12--13 *or* Elmasri & Navathe Ch. 8.
