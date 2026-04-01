====================================================
Cheat Sheet
====================================================

A condensed, box-by-box reference covering all major topics from
Lecture 8: SQL join types, ``ON`` vs ``WHERE`` semantics, physical join
strategies, Big O costs, ``EXPLAIN`` usage, disk/memory architecture,
and index design for joins.

----

Join Type Quick Reference
--------------------------

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - **Join Type**
     - **Key Rule**
   * - ``CROSS JOIN``
     - Every row paired with every row; result size = ``|R| x |S|``
   * - ``INNER JOIN``
     - Only matching rows survive; unmatched rows from either side disappear
   * - ``LEFT JOIN``
     - All left rows preserved; unmatched right columns become ``NULL``
   * - ``RIGHT JOIN``
     - All right rows preserved; usually rewrite as ``LEFT JOIN`` by swapping tables
   * - ``FULL OUTER JOIN``
     - All rows from both sides; unmatched sides filled with ``NULL``
   * - Self-join
     - Same table aliased twice; essential for hierarchies (``manager_id -> employee_id``)
   * - ``EXISTS`` (semi join)
     - Returns left rows that have at least one match; no duplicates
   * - ``NOT EXISTS`` (anti join)
     - Returns left rows with zero matches; prefer over ``NOT IN`` with NULLs
   * - ``LATERAL``
     - Right-side subquery can reference left-side columns; per-row evaluation

----

ON vs WHERE
-----------

.. list-table::
   :widths: 25 37 38
   :header-rows: 1
   :class: compact-table

   * - **Context**
     - **Filter in ON**
     - **Filter in WHERE**
   * - ``INNER JOIN``
     - Usually equivalent
     - Usually equivalent (prefer ``WHERE`` for clarity)
   * - ``LEFT JOIN``
     - Preserves all left rows; non-matching right rows become ``NULL``
     - Eliminates ``NULL``-extended rows; behaves like ``INNER JOIN``

**Rule of thumb**: join logic in ``ON``, result filters in ``WHERE``.

----

Preferred Join Syntax
---------------------

.. code-block:: sql

   -- Good: explicit JOIN ... ON
   SELECT c.customer_name, o.order_id
   FROM customers c
   JOIN orders o
     ON o.customer_id = c.customer_id
   WHERE o.total > 100;

   -- Avoid: old comma-join style
   SELECT c.customer_name, o.order_id
   FROM customers c, orders o
   WHERE c.customer_id = o.customer_id
     AND o.total > 100;

----

Semi-Join and Anti-Join Patterns
---------------------------------

.. code-block:: sql

   -- Semi join: customers WITH orders
   SELECT c.*
   FROM customers c
   WHERE EXISTS (
     SELECT 1 FROM orders o
     WHERE o.customer_id = c.customer_id
   );

   -- Anti join: customers WITHOUT orders
   SELECT c.*
   FROM customers c
   WHERE NOT EXISTS (
     SELECT 1 FROM orders o
     WHERE o.customer_id = c.customer_id
   );

   -- Alternative anti join using LEFT JOIN
   SELECT c.*
   FROM customers c
   LEFT JOIN orders o
     ON o.customer_id = c.customer_id
   WHERE o.order_id IS NULL;

----

Physical Join Strategies
------------------------

.. list-table::
   :widths: 20 25 55
   :header-rows: 1
   :class: compact-table

   * - **Strategy**
     - **Big O**
     - **When PostgreSQL chooses it**
   * - Nested loop
     - ``O(n * m)``
     - Small outer side + indexed inner; non-equality predicates
   * - Hash join
     - ``O(n + m)``
     - Equality join, unsorted input, sufficient ``work_mem``
   * - Merge join
     - ``O(n + m)`` pre-sorted; ``O(n log n + m log m)`` otherwise
     - Both inputs sorted or sort reusable for ``ORDER BY``

Hash join does **not** require a hash index.

----

EXPLAIN Quick Reference
-----------------------

.. code-block:: sql

   EXPLAIN (ANALYZE, BUFFERS)
   SELECT c.customer_name, o.order_id
   FROM customers c
   JOIN orders o ON o.customer_id = c.customer_id;

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **What to check**
     - **Why**
   * - Join node type
     - Confirms which physical strategy was used
   * - Estimated vs actual rows
     - Large mismatch signals bad statistics
   * - Buffers (shared hit/read)
     - Reveals whether data came from cache or disk
   * - Execution time
     - Actual wall-clock time per node

----

Big O for Database Operations
------------------------------

.. list-table::
   :widths: 25 35 40
   :header-rows: 1
   :class: compact-table

   * - **Complexity**
     - **Intuition**
     - **Database Example**
   * - ``O(1)``
     - Constant work
     - Ideal hash bucket lookup
   * - ``O(log n)``
     - Halve search space each step
     - B-tree index navigation
   * - ``O(n)``
     - Touch everything once
     - Sequential scan
   * - ``O(n log n)``
     - Sort plus process
     - Sort before merge join
   * - ``O(n^2)``
     - Pairwise combinations
     - Naive nested loop (no index)

----

Disk and Memory Architecture
------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Concept**
     - **Key Point**
   * - Heap table
     - Unsorted storage of row data in 8 KB pages
   * - Index file
     - Separate structure pointing to heap page locations
   * - ``shared_buffers``
     - Page cache; reduces disk reads for frequently accessed pages
   * - ``work_mem``
     - Per-node memory for sorts and hash tables; each node gets its own allocation
   * - Temp files
     - Created when ``work_mem`` is exhausted; significantly slower than in-memory

A sequential scan is not a moral failure -- if the query needs most of the
table, it is often the cheapest option.

----

Index Types in PostgreSQL
--------------------------

.. list-table::
   :widths: 15 40 45
   :header-rows: 1
   :class: compact-table

   * - **Type**
     - **Best For**
     - **Join Relevance**
   * - B-tree
     - Equality, range, ordering
     - Most common; default ``CREATE INDEX``
   * - Hash
     - Equality only
     - Niche; not needed for hash joins
   * - GiST
     - Geometric / range-like search
     - Specialized joins
   * - GIN
     - Arrays, ``jsonb``, full text
     - Membership / search
   * - BRIN
     - Huge naturally-ordered tables
     - Coarse filtering

----

Index Design Checklist for Joins
---------------------------------

.. code-block:: text

   1. Index foreign key columns on the referencing (child) table
      -- PostgreSQL does NOT auto-index FK columns
   2. Match data types and collations across join columns
      -- implicit casts block index usage
   3. Use composite indexes for join + filter patterns
      -- e.g., (customer_id, order_date)
   4. Consider INCLUDE for covering index patterns
      -- e.g., INCLUDE (total) to avoid heap lookup
   5. Do NOT duplicate the PK index
      -- it already exists
   6. Avoid functions/casts on join keys
      -- breaks index eligibility

----

B+ Tree Rules
--------------

- Keys stay sorted in each node.
- Insert into the appropriate leaf; split on overflow.
- Push separator key upward on split.
- All leaves at the same depth (predictable ``O(log n)`` lookups).
- Leaves are linked for efficient range scans.

----

PostgreSQL Tuning Checklist
----------------------------

.. code-block:: text

   1. EXPLAIN (ANALYZE, BUFFERS)  -- measure, don't guess
   2. ANALYZE                     -- keep statistics fresh
   3. VACUUM / autovacuum         -- control bloat
   4. work_mem                    -- tune carefully per workload
   5. CREATE STATISTICS           -- for correlated columns

**Tuning without measurement is just storytelling.**
