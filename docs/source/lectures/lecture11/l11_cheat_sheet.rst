====================================================
Cheat Sheet
====================================================

A condensed reference for Lecture 11: ``EXPLAIN`` / ``EXPLAIN ANALYZE``
output, PostgreSQL cost constants, SARGABLE query design, compound
indexes, and join strategies.

----

EXPLAIN Commands
------------------

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Command**
     - **What it does**
   * - ``EXPLAIN query;``
     - Prints the planner's **estimates**. Does **not** execute the
       query.
   * - ``EXPLAIN ANALYZE query;``
     - **Executes** the query and prints estimates + actual time,
       rows, and loops.
   * - ``EXPLAIN (ANALYZE, BUFFERS) query;``
     - Adds ``Buffers: shared hit=N read=N`` -- use for IO diagnosis.
   * - ``EXPLAIN (ANALYZE, MEMORY) query;``
     - Adds ``Memory: used=... allocated=...`` for the **planner**.
   * - ``EXPLAIN (ANALYZE, SERIALIZE) query;``
     - Adds serialization time, output size, and format.
   * - ``BEGIN; EXPLAIN ANALYZE <mutation>; ROLLBACK;``
     - Diagnose a write query without persisting changes.

----

Reading a Plan Line
---------------------

.. code-block:: text

    Seq Scan on employees  (cost=0.00..20.50 rows=762 width=27) (actual time=0.111..0.344 rows=762 loops=1)
      Filter: (age > 30)
      Rows Removed by Filter: 238
    Planning Time: 0.128 ms
    Execution Time: 0.405 ms

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Field**
     - **Meaning**
   * - Operator (``Seq Scan``, ``Index Scan``, ``Hash Join``, ...)
     - The physical step being performed.
   * - ``cost=start..total``
     - Planner's **relative** cost estimate (start-up / total).
   * - ``rows=N`` (in ``cost=...``)
     - **Estimated** rows produced.
   * - ``width=N``
     - Estimated bytes per row.
   * - ``actual time=start..total``
     - **Measured** start-up / total milliseconds (only with
       ``ANALYZE``).
   * - ``actual rows=N loops=M``
     - Measured rows per loop × number of loops.
   * - ``Filter:``
     - Predicate applied in this step.
   * - ``Rows Removed by Filter:``
     - Rows examined but discarded. Large numbers here signal wasted
       work.
   * - ``Planning Time``
     - Time to generate the plan.
   * - ``Execution Time``
     - End-to-end execution.

**Rule of thumb**: ``Execution Time`` close to ``Planning Time`` for a
simple query means the planner was the bottleneck -- uncommon.

----

Common Operators in Plans
---------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Meaning**
   * - ``Seq Scan``
     - Read every row in a table (usually bad at scale if a filter
       is selective).
   * - ``Index Scan``
     - Use an index to find matching rows, then fetch them.
   * - ``Index Only Scan``
     - Use an index that covers all needed columns -- no heap fetch.
   * - ``Bitmap Index Scan`` + ``Bitmap Heap Scan``
     - Build a bitmap of matching row IDs, then fetch heap pages in
       order.
   * - ``Nested Loop``
     - For each outer row, scan the inner side.
   * - ``Merge Join``
     - Sort both sides, walk sorted streams to find matches
       (equality only).
   * - ``Hash Join``
     - Build hash table on inner, probe from outer (equality only).
   * - ``Sort``
     - Explicit sort step; expensive especially when it spills to
       disk.
   * - ``GroupAggregate`` / ``HashAggregate``
     - GROUP BY + aggregations (sorted vs hashed).
   * - ``Limit``
     - Cap output size -- usually the **last** step executed.
   * - ``Memoize``
     - Cache of per-key results inside a Nested Loop's inner side.

----

PostgreSQL Cost Constants
----------------------------

.. list-table::
   :widths: 30 15 55
   :header-rows: 1
   :class: compact-table

   * - **Parameter**
     - **Default**
     - **Meaning**
   * - ``seq_page_cost``
     - 1.0
     - Sequential disk-page fetch.
   * - ``random_page_cost``
     - 4.0
     - Non-sequential disk-page fetch. Lower on SSD-only systems to
       prefer index scans.
   * - ``cpu_tuple_cost``
     - 0.01
     - Cost of processing each row.
   * - ``cpu_index_tuple_cost``
     - 0.005
     - Cost of processing each index entry.
   * - ``cpu_operator_cost``
     - 0.0025
     - Cost of processing each operator/function.
   * - ``parallel_setup_cost``
     - 1000
     - Parallel worker launch cost.
   * - ``parallel_tuple_cost``
     - 0.1
     - Per-tuple handoff between parallel workers.

**Rule**: don't tune these without benchmarking a representative
workload.

----

Magic Numbers (Latency Intuition)
-----------------------------------

.. list-table::
   :widths: 55 45
   :header-rows: 1
   :class: compact-table

   * - **Operation**
     - **Approx. latency**
   * - L1 cache reference
     - 1 ns
   * - L2 cache reference
     - 4 ns
   * - RAM reference
     - 100 ns
   * - SSD random read
     - 16 µs
   * - Magnetic disk seek
     - 3 ms
   * - Read 1 MB sequentially from RAM
     - 4 µs
   * - Read 1 MB sequentially from SSD
     - 62 µs
   * - Read 1 MB sequentially from disk
     - 947 µs
   * - Round-trip in same datacenter
     - 500 µs

----

SARGABLE vs Non-SARGABLE
--------------------------

.. list-table::
   :widths: 45 55
   :header-rows: 1
   :class: compact-table

   * - **SARGABLE (index-friendly)**
     - **Non-SARGABLE (defeats index)**
   * - ``col = 5``, ``col > 10``, ``col != 0``
     - ``col + 1 > 10``
   * - ``col BETWEEN a AND b``
     - ``UPPER(col) = 'ADA'``, ``LOWER(col) = ...``
   * - ``col IN (1, 2, 3)``
     - ``col NOT IN (...)``
   * - ``col LIKE 'prefix%'``
     - ``col LIKE '%suffix'``, ``col LIKE '%middle%'``
   * - ``col >= CURRENT_DATE``
     - ``col::text = '...'`` (implicit cast)

Rescues for non-SARGABLE patterns:

- **Functional index**: ``CREATE INDEX ... ON t(UPPER(col));``
- **Trigram index**: ``CREATE INDEX ... USING gin(col gin_trgm_ops);``
  for ``%substring%`` patterns (requires ``pg_trgm`` extension).
- **Generated column**: store a normalized value alongside and index
  it.

----

Compound Index Design (ESR Rule)
----------------------------------

Order columns in a compound index as:

1. **Equality** columns first (``status = 'open'``).
2. **Sort** column next (``ORDER BY created_at``).
3. **Range** columns last (``amount > 1000``).

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Index on**
     - **Serves queries filtering on**
   * - ``(a)``
     - ``a``
   * - ``(a, b)``
     - ``a``, or ``a + b`` -- **not** ``b`` alone
   * - ``(a, b, c)``
     - ``a``, ``a+b``, or ``a+b+c`` -- **not** ``b`` alone, ``c``
       alone, or ``b+c``

**Leftmost-prefix rule**: only the left-anchored prefix of the index
is useful.

----

Index Trade-offs
------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Cost**
     - **Detail**
   * - Read latency
     - Usually decreases (for SARGABLE queries).
   * - Write latency
     - Increases -- every insert/update/delete maintains indexes.
   * - Disk / memory
     - Increases -- compound indexes cost more than single-column.
   * - Plan churn
     - More indexes = more candidate plans for the planner.

**Rule**: index only what real queries need. Remove unused indexes
aggressively.

----

Join Strategies
-----------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - **Strategy**
     - **How it works**
     - **Best when**
   * - Nested Loop
     - For each outer row, scan the inner.
     - One side is small or the inner is well-indexed (with Memoize).
   * - Merge Join
     - Sort both sides on the join key; walk them in parallel.
     - Data is already sorted, or hash would exceed ``work_mem``.
       Equality only.
   * - Hash Join
     - Build hash on inner, probe from outer.
     - Hash table fits in ``work_mem`` and tables are large.
       Equality only.

**Inequality joins**: only Nested Loop works.

----

Optimization Checklist
------------------------

1. Run ``EXPLAIN ANALYZE`` on the slow query.
2. Identify the **most expensive step** (cost or actual time).
3. Check if the query is **SARGABLE**; fix non-SARGABLE predicates.
4. Look for large ``Rows Removed by Filter`` -- push filters earlier.
5. Consider a targeted **index** (single or compound, following ESR).
6. Verify with ``EXPLAIN (ANALYZE, BUFFERS)`` that plan and IO
   improved.
7. Revisit **schema / join keys** if the query has string-equality
   joins where integer FK joins could work.
8. Only now consider ``work_mem`` / ``shared_buffers`` tuning, or new
   hardware.

----

Summary
---------

- **Examine query plans before optimizing**.
- Use appropriate **data types** and narrow columns.
- **Filter early** with ``WHERE``.
- Avoid unnecessary **sorting** / **grouping**.
- **Optimize join operations** -- pick join keys that use indexes
  well.
- **Limit result-set size** -- return only what you need.
- **Use indexes appropriately** -- SARGABLE, ESR, measure before and
  after.
