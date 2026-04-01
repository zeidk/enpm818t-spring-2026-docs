====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 8: JOINs, Query Execution,
and Indexing. Topics include Cartesian products, relational algebra, all
join types (``INNER``, ``LEFT``, ``RIGHT``, ``FULL``, ``CROSS``, self-join,
semi/anti), ``ON`` vs ``WHERE`` semantics, physical join strategies
(nested loop, hash, merge), ``EXPLAIN`` output, Big O notation for join
algorithms, disk and memory architecture, and B+ tree indexing.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-18)
================================

.. admonition:: Question 1
   :class: hint

   What is the result size of ``R CROSS JOIN S`` if ``R`` has 100 rows and
   ``S`` has 50 rows?

   A. 150

   B. 50

   C. 5,000

   D. 100

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- 5,000

   A ``CROSS JOIN`` produces the Cartesian product: every row in ``R`` is
   paired with every row in ``S``, yielding ``100 x 50 = 5,000`` rows.


.. admonition:: Question 2
   :class: hint

   Which join type preserves all rows from the left table, filling in
   ``NULL`` for unmatched right-side columns?

   A. ``INNER JOIN``

   B. ``RIGHT JOIN``

   C. ``LEFT JOIN``

   D. ``CROSS JOIN``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``LEFT JOIN``

   A ``LEFT JOIN`` (or ``LEFT OUTER JOIN``) returns all rows from the left
   table. For left rows with no match on the right, the right-side columns
   are filled with ``NULL``.


.. admonition:: Question 3
   :class: hint

   Given a ``LEFT JOIN``, what is the effect of placing a filter on the
   right table in the ``WHERE`` clause instead of the ``ON`` clause?

   A. No difference -- both produce the same result.

   B. The query becomes syntactically invalid.

   C. It effectively converts the ``LEFT JOIN`` into an ``INNER JOIN``
      because ``NULL``-extended rows are eliminated.

   D. It causes PostgreSQL to use a different join algorithm.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It effectively converts the ``LEFT JOIN`` into an ``INNER JOIN``.

   When a filter on the right table is in the ``WHERE`` clause, rows where
   the right side is ``NULL`` (unmatched) fail the ``WHERE`` condition and
   are eliminated. This is functionally equivalent to an ``INNER JOIN``.


.. admonition:: Question 4
   :class: hint

   Which SQL pattern is the preferred way to find all customers who have
   **no** orders?

   A. ``SELECT * FROM customers c INNER JOIN orders o ON c.customer_id = o.customer_id WHERE o.order_id IS NULL``

   B. ``SELECT * FROM customers c WHERE NOT EXISTS (SELECT 1 FROM orders o WHERE o.customer_id = c.customer_id)``

   C. ``SELECT * FROM customers c CROSS JOIN orders o WHERE o.order_id IS NULL``

   D. ``SELECT * FROM customers c WHERE customer_id NOT IN (NULL)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``NOT EXISTS``

   ``NOT EXISTS`` is the standard anti-join pattern. It correctly handles
   ``NULL`` values and is the recommended approach. Option A would return
   zero rows since an ``INNER JOIN`` never produces ``NULL`` on the right.
   Option D is broken because ``NOT IN`` with a ``NULL`` value always
   returns empty.


.. admonition:: Question 5
   :class: hint

   Why should ``NATURAL JOIN`` be avoided in production code?

   A. It is not supported by PostgreSQL.

   B. It always produces a Cartesian product.

   C. It silently joins on all columns with matching names, so schema
      changes can change query semantics without warning.

   D. It is significantly slower than explicit ``JOIN ... ON``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- It silently joins on all columns with matching names.

   If a new column with the same name is added to either table, the join
   condition changes without any error or warning. This makes ``NATURAL
   JOIN`` brittle and dangerous in production systems.


.. admonition:: Question 6
   :class: hint

   What does ``LATERAL`` allow in a ``JOIN`` that a regular subquery does
   not?

   A. It allows the right-hand subquery to reference columns from the
      left-hand table.

   B. It forces a merge join strategy.

   C. It enables ``CROSS JOIN`` behavior.

   D. It disables ``NULL`` propagation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- It allows the right-hand subquery to reference columns from the
   left-hand table.

   ``LATERAL`` evaluates the subquery once per left-side row, allowing it
   to use values from the current left row in its ``WHERE`` clause.


.. admonition:: Question 7
   :class: hint

   Which physical join strategy is best suited for joining a small table
   (20 rows) to a very large table (100M rows) when there is an index on
   the large table's join column?

   A. Hash join

   B. Merge join

   C. Nested loop join

   D. Cross join

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Nested loop join

   With a small outer side and an indexed inner side, nested loop performs
   20 index lookups into the large table -- far cheaper than building a
   hash table or sorting 100M rows.


.. admonition:: Question 8
   :class: hint

   What is the approximate Big O cost of a hash join on two tables of size
   ``n`` and ``m``?

   A. ``O(n * m)``

   B. ``O(n + m)``

   C. ``O(n log n)``

   D. ``O(n^2)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``O(n + m)``

   A hash join builds a hash table from one input (``O(n)``) and probes it
   with the other (``O(m)``), giving ``O(n + m)`` total, assuming the hash
   table fits in memory.


.. admonition:: Question 9
   :class: hint

   In PostgreSQL, what is the default page size for heap storage?

   A. 4 KB

   B. 8 KB

   C. 16 KB

   D. 64 KB

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 8 KB

   PostgreSQL's standard page size is 8 KB. All I/O is page-oriented.


.. admonition:: Question 10
   :class: hint

   Which PostgreSQL configuration parameter controls the memory available
   for sorts and hash tables within a single query node?

   A. ``shared_buffers``

   B. ``effective_cache_size``

   C. ``work_mem``

   D. ``maintenance_work_mem``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``work_mem``

   Each sort or hash node in a query plan can use up to ``work_mem`` bytes.
   A single query with multiple nodes may use multiple chunks of
   ``work_mem``.


.. admonition:: Question 11
   :class: hint

   Which index type is the default when running ``CREATE INDEX`` in
   PostgreSQL?

   A. Hash

   B. GiST

   C. GIN

   D. B-tree

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- B-tree

   Unless another type is specified, ``CREATE INDEX`` creates a B-tree
   index. B-tree indexes support equality and range lookups and are the
   most common index type.


.. admonition:: Question 12
   :class: hint

   Does a hash join require a hash index on the join column?

   A. Yes -- hash joins can only use hash indexes.

   B. No -- hash joins build an in-memory hash table at runtime,
      independent of any on-disk index.

   C. Only if ``work_mem`` is insufficient.

   D. Only for ``FULL OUTER JOIN``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- No

   Hash joins build their own hash table at query execution time. The
   presence or absence of a hash index on disk has no bearing on whether
   PostgreSQL can use a hash join strategy.


.. admonition:: Question 13
   :class: hint

   What property of B+ trees keeps lookup cost predictable?

   A. Keys are stored in random order.

   B. All leaf nodes are at the same depth.

   C. Internal nodes store row data.

   D. The tree is rebuilt after every insert.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- All leaf nodes are at the same depth.

   This balanced property guarantees that any lookup traverses the same
   number of levels, giving predictable ``O(log n)`` performance.


.. admonition:: Question 14
   :class: hint

   In the relational algebra, a join is semantically equivalent to:

   A. A projection followed by a selection.

   B. A Cartesian product followed by a selection (filter).

   C. A union followed by a difference.

   D. An intersection followed by a projection.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A Cartesian product followed by a selection.

   ``R BOWTIE_{cond} S = sigma_{cond}(R x S)``. The join filters the
   Cartesian product to keep only matching pairs.


.. admonition:: Question 15
   :class: hint

   When is a sequential scan likely to be **faster** than an index scan?

   A. When the query returns very few rows.

   B. When the table has a unique index on the filter column.

   C. When the query needs a large fraction of the table's rows.

   D. Sequential scans are never faster than index scans.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- When the query needs a large fraction of the table's rows.

   Index scans incur random I/O per row. When most rows will be returned
   anyway, a single sequential pass through the heap is cheaper.


.. admonition:: Question 16
   :class: hint

   What does ``EXPLAIN (ANALYZE, BUFFERS)`` show that plain ``EXPLAIN``
   does not?

   A. The SQL query text.

   B. Actual execution times, actual row counts, and buffer hit/read
      statistics.

   C. The table's DDL.

   D. Index definitions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Actual execution times, actual row counts, and buffer
   statistics.

   ``ANALYZE`` runs the query and reports actual (not estimated) values.
   ``BUFFERS`` adds information about shared buffer hits and disk reads.


.. admonition:: Question 17
   :class: hint

   Which of the following is true about ``COUNT(*)`` vs
   ``COUNT(column_name)`` after a ``LEFT JOIN``?

   A. They always return the same number.

   B. ``COUNT(*)`` counts all rows including ``NULL``-extended ones;
      ``COUNT(column_name)`` counts only non-``NULL`` values in that column.

   C. ``COUNT(column_name)`` counts ``NULL`` values as well.

   D. ``COUNT(*)`` excludes ``NULL``-extended rows.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``COUNT(*)`` counts all rows; ``COUNT(column_name)`` skips
   ``NULL`` values.

   After a ``LEFT JOIN``, unmatched right-side columns are ``NULL``.
   ``COUNT(*)`` includes those rows, but ``COUNT(o.order_id)`` does not.


.. admonition:: Question 18
   :class: hint

   PostgreSQL automatically creates an index on which of the following?

   A. Foreign key columns on the referencing (child) table.

   B. Primary key columns.

   C. All ``NOT NULL`` columns.

   D. Columns used in ``WHERE`` clauses.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Primary key columns.

   PostgreSQL automatically creates a unique B-tree index for primary keys.
   Foreign key columns on the referencing side are **not** automatically
   indexed -- you must create those indexes yourself.


----


True / False (Questions 19-26)
==============================

.. admonition:: Question 19
   :class: hint

   True or False: ``INNER JOIN`` and ``CROSS JOIN`` produce the same
   result when the ``ON`` clause is always true (e.g., ``ON true``).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``INNER JOIN ... ON true`` produces the Cartesian product, which is the
   same as ``CROSS JOIN``.


.. admonition:: Question 20
   :class: hint

   True or False: A ``RIGHT JOIN`` can always be rewritten as a
   ``LEFT JOIN`` by swapping the table order.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   ``A RIGHT JOIN B ON cond`` is equivalent to ``B LEFT JOIN A ON cond``.


.. admonition:: Question 21
   :class: hint

   True or False: ``NOT IN (subquery)`` and ``NOT EXISTS (subquery)``
   always return the same results.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   If the subquery returns any ``NULL`` values, ``NOT IN`` returns no rows
   (because ``x NOT IN (..., NULL, ...)`` is never true). ``NOT EXISTS``
   handles ``NULL`` correctly.


.. admonition:: Question 22
   :class: hint

   True or False: A merge join requires both inputs to be sorted on the
   join key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Merge join processes two sorted streams in parallel. If the inputs are
   not already sorted, PostgreSQL adds explicit sort nodes to the plan.


.. admonition:: Question 23
   :class: hint

   True or False: Setting ``work_mem`` too high on a busy server is safe
   because PostgreSQL manages memory automatically.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Each sort/hash node in every concurrent query can allocate up to
   ``work_mem``. On a busy server with many sessions, this can cause
   excessive total memory consumption and memory pressure.


.. admonition:: Question 24
   :class: hint

   True or False: A ``FULL OUTER JOIN`` will never return fewer rows than
   a ``LEFT JOIN`` on the same tables with the same condition.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A ``FULL OUTER JOIN`` includes all rows from both sides (matched and
   unmatched). A ``LEFT JOIN`` only preserves unmatched rows from the left,
   so ``FULL OUTER`` always returns at least as many rows.


.. admonition:: Question 25
   :class: hint

   True or False: The ``USING (column)`` syntax can be used when the join
   columns have different names in the two tables.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``USING (column)`` requires that the column has the **same name** in
   both tables. If names differ, use ``ON a.col1 = b.col2``.


.. admonition:: Question 26
   :class: hint

   True or False: An ``INNER JOIN`` can be freely reordered by the query
   planner without changing the result.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Inner joins are commutative and associative, so PostgreSQL can reorder
   them freely to find the cheapest execution plan. Outer joins, however,
   cannot always be reordered.


----


Essay Questions (Questions 27-30)
=================================

.. admonition:: Question 27
   :class: hint

   Explain in 2-4 sentences why placing a filter on the right table in the
   ``WHERE`` clause of a ``LEFT JOIN`` effectively converts it into an
   ``INNER JOIN``.

.. dropdown:: Answer
   :class-container: sd-border-success

   A ``LEFT JOIN`` produces ``NULL`` for all right-side columns when there
   is no match. A ``WHERE`` clause that tests a right-side column (e.g.,
   ``WHERE o.total > 100``) evaluates to ``NULL`` (which is not true) for
   those unmatched rows, causing them to be filtered out. The result is
   that only rows with actual matches survive, which is the same behavior
   as an ``INNER JOIN``.


.. admonition:: Question 28
   :class: hint

   Compare and contrast hash join and merge join. Under what circumstances
   would PostgreSQL prefer one over the other?

.. dropdown:: Answer
   :class-container: sd-border-success

   A **hash join** builds an in-memory hash table from one input and probes
   it with the other; it is ``O(n + m)`` and excellent for unsorted equality
   joins when there is enough ``work_mem``. A **merge join** walks two
   sorted streams in parallel; it is ``O(n + m)`` when inputs are pre-sorted,
   but requires ``O(n log n + m log m)`` if sorting is needed first.
   PostgreSQL prefers hash join when inputs are unsorted and memory is
   sufficient, and merge join when both inputs are already sorted (e.g.,
   by an index) or when the sort can be reused for an ``ORDER BY``.


.. admonition:: Question 29
   :class: hint

   Why does PostgreSQL not automatically create indexes on foreign key
   columns, and what problems can this cause for join performance?

.. dropdown:: Answer
   :class-container: sd-border-success

   PostgreSQL treats index creation as a deliberate decision by the DBA
   because every index adds write overhead and storage cost. However,
   unindexed foreign key columns can cause severe performance issues: joins
   on those columns may require full sequential scans of the referencing
   table, and ``DELETE`` or ``UPDATE`` on the referenced table must check
   all referencing rows (which without an index requires a sequential scan).
   It is a best practice to manually create indexes on foreign key columns,
   especially on large tables.


.. admonition:: Question 30
   :class: hint

   A colleague tells you: "Sequential scans are always bad; we should add
   indexes everywhere." In 2-4 sentences, explain why this advice is
   oversimplified.

.. dropdown:: Answer
   :class-container: sd-border-success

   Sequential scans are actually the optimal choice when a query needs a
   large fraction of a table's rows, because they read pages in order and
   avoid the random I/O overhead of index lookups. Adding indexes
   everywhere increases storage requirements and slows down every
   ``INSERT``, ``UPDATE``, and ``DELETE`` because each index must be
   maintained. The PostgreSQL planner already chooses between sequential and
   index scans based on cost estimates. The correct approach is to design
   indexes around actual workload patterns and verify with
   ``EXPLAIN (ANALYZE, BUFFERS)``.
