====================================================
L11: Optimizing SQL Queries
====================================================

Overview
--------

This lecture focuses on **optimizing SQL queries** in PostgreSQL. Your
database is the keystone of an application's architecture, so extracting
performance from it pays dividends everywhere else. We zero in on
**query optimization** specifically -- the easiest, least expensive,
and most broadly applicable performance lever.

The arc: **read the query plan first**, learn to decode basic plans
(``Seq Scan``, costs, rows, filters, planning/execution time), then
unwind advanced plans inside-out (sorts, merge joins, group aggregates,
limit). We cover how small query changes materially shift the plan
(``JOIN`` key selection, Memoize), how to debug plans that use CTEs or
views, and how to read **IO** with ``EXPLAIN (ANALYZE, BUFFERS)``,
**memory** with ``(ANALYZE, MEMORY)``, and **serialization** with
``(ANALYZE, SERIALIZE)``. Finally we cover **when to add indexes**
(SARGABLE vs non-SARGABLE queries, compound-index design, index
drawbacks) and **join strategies** (nested loop, merge, hash) with
guidance on when each wins.

A short interlude revisits **transactions** and ACID, since every
``EXPLAIN ANALYZE`` on a write query should be wrapped in
``BEGIN; ... ROLLBACK;`` to avoid mutating the database while
diagnosing.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain why **query optimization** is usually the first performance
  lever to pull (before hardware or schema redesign).
- Generate query plans with ``EXPLAIN`` and ``EXPLAIN ANALYZE``, and
  understand the difference (estimates vs measured execution).
- Read a basic plan: ``Seq Scan``, ``cost=start..total``, ``rows``,
  ``width``, ``Filter``, ``Rows Removed by Filter``, ``Planning Time``,
  ``Execution Time``.
- Unwind a complex plan **bottom-up and inside-out**, identifying the
  most expensive step.
- Interpret PostgreSQL's cost constants (``seq_page_cost``,
  ``random_page_cost``, ``cpu_tuple_cost``, ``cpu_index_tuple_cost``,
  ``cpu_operator_cost``, ``parallel_setup_cost``,
  ``parallel_tuple_cost``) and what they reveal about the planner's
  assumptions.
- Use ``EXPLAIN (ANALYZE, BUFFERS)`` to identify queries that would
  benefit from more memory, better indexes, or a better plan -- and
  distinguish buffer **hits** from disk **reads**.
- Use ``EXPLAIN (ANALYZE, MEMORY)`` and ``EXPLAIN (ANALYZE, SERIALIZE)``
  to diagnose memory usage and output serialization costs.
- Recognize **SARGABLE** query patterns (``=``, ``>``, ``<``,
  ``BETWEEN``, ``IN``, left-anchored ``LIKE``) and **non-SARGABLE**
  anti-patterns (implicit casts, arithmetic on indexed columns,
  leading-wildcard ``LIKE``, function calls in ``WHERE``, negation
  operators).
- Design **compound indexes** that match real query patterns (leftmost
  prefix rule) and weigh the trade-off against write amplification and
  index size.
- Explain the three physical join strategies (**nested loop**,
  **merge join**, **hash join**) and predict which PostgreSQL will
  choose based on table size, ``work_mem``, indexes, selectivity, and
  join condition type.
- Wrap read-only diagnostics on mutating queries in
  ``BEGIN; [queries]; ROLLBACK;`` so that ``EXPLAIN ANALYZE`` does not
  leave state behind.


.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l11_lecture
   l11_postgres_setup
   l11_exercises
   l11_quiz
   l11_references
   l11_cheat_sheet


Next Steps
----------

- Before next class: complete the take-home exercises and run
  ``EXPLAIN ANALYZE`` on the sample database from the setup guide.
  Try to reproduce the query-plan changes discussed in lecture by
  adjusting join keys, adding indexes, and tweaking ``work_mem``.
- Optional reading: the PostgreSQL docs on `Using EXPLAIN
  <https://www.postgresql.org/docs/current/using-explain.html>`_
  and `Planner Cost Constants
  <https://www.postgresql.org/docs/current/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS>`_.
