====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 11: **Optimizing SQL
Queries**. Topics include ``EXPLAIN`` / ``EXPLAIN ANALYZE``, query
plans, cost constants, IO / memory / serialization diagnostics,
SARGABLE query patterns, compound-index design, and join strategies.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement
     is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-18)
================================


.. admonition:: Question 1
   :class: hint

   What is the main difference between ``EXPLAIN`` and
   ``EXPLAIN ANALYZE`` in PostgreSQL?

   A. ``EXPLAIN`` is for write queries; ``EXPLAIN ANALYZE`` is for
      read queries.

   B. ``EXPLAIN`` prints the planner's estimates; ``EXPLAIN ANALYZE``
      also executes the query and reports actual times.

   C. ``EXPLAIN`` requires a ``COMMIT``; ``EXPLAIN ANALYZE`` does not.

   D. ``EXPLAIN`` is deprecated in modern PostgreSQL.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``EXPLAIN`` prints estimates; ``EXPLAIN ANALYZE``
   actually runs the query and reports measured timings in addition
   to estimates.


.. admonition:: Question 2
   :class: hint

   In the line ``Seq Scan on employees (cost=0.00..22.50 rows=791
   width=39)``, what does ``22.50`` represent?

   A. The number of milliseconds the scan took.

   B. The number of rows returned.

   C. The planner's **total cost** estimate to complete the scan.

   D. The buffer page size in KB.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``cost=START..TOTAL``. ``0.00`` is the startup cost;
   ``22.50`` is the total cost to complete the operation.


.. admonition:: Question 3
   :class: hint

   Which of the following is a **SARGABLE** query predicate?

   A. ``WHERE UPPER(name) = 'ADA'``

   B. ``WHERE salary + 1000 > 50000``

   C. ``WHERE hire_date >= '2023-01-01'``

   D. ``WHERE name LIKE '%smith'``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A simple range predicate against an indexed column is
   SARGABLE. A, B, and D all transform the column side or use a
   leading wildcard, defeating the index.


.. admonition:: Question 4
   :class: hint

   In a compound index on ``(col1, col2, col3)``, which query can
   use the index?

   A. ``WHERE col2 = 5``

   B. ``WHERE col3 = 'x'``

   C. ``WHERE col1 = 5``

   D. ``WHERE col2 = 5 AND col3 = 'x'``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The leftmost-prefix rule. ``col1`` is the prefix and can
   use the index; the others cannot (without ``col1`` in the
   predicate).


.. admonition:: Question 5
   :class: hint

   Which join algorithm requires that both tables be sorted on the
   join key?

   A. Nested Loop Join

   B. Merge Join

   C. Hash Join

   D. Cross Join

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Merge Join sorts (or expects sorted input on) both sides
   and walks them in parallel.


.. admonition:: Question 6
   :class: hint

   ``EXPLAIN (ANALYZE, BUFFERS)`` reports ``Buffers: shared hit=42``.
   What does that tell you?

   A. 42 disk pages had to be read.

   B. 42 buffer pages were found in the in-memory cache, no disk
      read required.

   C. 42 rows were returned.

   D. 42 MB of memory was allocated by the planner.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``shared hit=N`` means ``N`` buffers were served from the
   ``shared_buffers`` cache without a disk read. ``shared read=N``
   would indicate disk reads.


.. admonition:: Question 7
   :class: hint

   Which PostgreSQL cost constant controls the planner's preference
   between sequential scans and index scans?

   A. ``cpu_tuple_cost``

   B. ``seq_page_cost``

   C. ``random_page_cost``

   D. ``parallel_setup_cost``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``random_page_cost`` is the cost of a
   non-sequentially-fetched page. Lowering it makes index scans
   relatively cheaper; raising it makes them relatively more
   expensive.


.. admonition:: Question 8
   :class: hint

   Why would you wrap ``EXPLAIN ANALYZE`` on an ``UPDATE`` in
   ``BEGIN; ... ROLLBACK;``?

   A. To avoid an authentication prompt.

   B. Because ``EXPLAIN ANALYZE`` actually executes the query; the
      rollback ensures the change is not persisted.

   C. To force the query planner to re-plan.

   D. To bypass the ACID constraints.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``EXPLAIN ANALYZE`` really runs the query. For mutating
   statements, a transaction + rollback lets you profile without
   changing state.


.. admonition:: Question 9
   :class: hint

   Which of these is **most likely** to cause a ``Merge Join`` instead
   of a ``Hash Join``?

   A. Both tables are tiny.

   B. One side is very small and the other is indexed on the join
      column.

   C. The expected hash table would not fit in ``work_mem``.

   D. The join is on an inequality condition.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- When the hash table is too large for ``work_mem``, the
   planner prefers Merge Join (sort + merge) over Hash Join. Option
   A favors Nested Loop; B favors Nested Loop + Index Scan; D rules
   out both Merge and Hash.


.. admonition:: Question 10
   :class: hint

   A query plan contains ``Rows Removed by Filter: 95000``. What does
   this imply?

   A. The filter removed 95000 rows before the scan.

   B. The scan examined 95000 rows that were discarded by the filter,
      suggesting a better index or an earlier filter might help.

   C. The database had to sort 95000 rows.

   D. The network dropped 95000 rows.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The scan touched those rows before discarding them. Large
   ``Rows Removed by Filter`` numbers often point to a missing index
   or a filter that could be pushed earlier.


.. admonition:: Question 11
   :class: hint

   Which PostgreSQL feature caches per-key results of an inner-loop
   lookup during a Nested Loop Join?

   A. ``WorkMem``

   B. ``Memoize``

   C. ``Materialize``

   D. ``BitmapHeapScan``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``Memoize`` is a local cache over a repeated inner-loop
   lookup. It is often what enables Nested Loop + Index Scan plans
   to outperform Hash / Merge Join on medium-sized inner tables.


.. admonition:: Question 12
   :class: hint

   Which guideline usually produces the most performance improvement
   per unit of effort?

   A. Buy more RAM.

   B. Upgrade to the latest PostgreSQL version.

   C. Examine query plans and fix the expensive steps.

   D. Rewrite the application in a faster language.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Query optimization is the cheapest, most broadly
   applicable, and most easily measurable performance lever.


.. admonition:: Question 13
   :class: hint

   Which is a correct ordering of steps when reading an advanced
   nested query plan in PostgreSQL?

   A. Top-down, outside-in (in the order lines appear).

   B. Bottom-up, inside-out (deepest indented step runs first).

   C. Alphabetical by operator name.

   D. By cost, highest first.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- PostgreSQL plans are nested trees. The deepest indented
   node runs first, with work bubbling upward.


.. admonition:: Question 14
   :class: hint

   A query joins two tables on a **string** (text) column with no
   index. You change the join to use a foreign-key integer column
   with an index. What is the most likely effect?

   A. The planner switches from Merge Join to Nested Loop + Index
      Scan, and execution time drops materially.

   B. Execution time gets slower because integers take more memory
      than short strings.

   C. No change -- the planner ignores which column you join on.

   D. The query becomes non-SARGABLE.

.. dropdown:: Answer
   :class-container: sd-border-success

   **A** -- This is the join-key-selection example from lecture.
   Indexed integer joins typically switch the plan to Nested Loop +
   Index Scan (often with Memoize) and drop execution time
   significantly.


.. admonition:: Question 15
   :class: hint

   Which of the following best describes the "Equality-Sort-Range"
   (ESR) rule for compound index design?

   A. Place range columns first, then sort, then equality.

   B. Place equality columns first, then the sort column, then the
      range columns.

   C. Place sort columns first, then range, then equality.

   D. Order is irrelevant for compound indexes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Equality first narrows the scan; a matching sort column
   next lets the index feed ``ORDER BY`` directly; range columns
   last, because a range predicate stops the usable portion of the
   index.


.. admonition:: Question 16
   :class: hint

   Which statement about indexes is **false**?

   A. Indexes speed up reads for SARGABLE queries.

   B. Indexes make writes slower because they must be maintained.

   C. Adding an index to every column is always a good idea.

   D. Compound indexes obey a leftmost-prefix rule.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Over-indexing slows writes and consumes memory/disk with
   little read benefit. Index only where a real query benefits.


.. admonition:: Question 17
   :class: hint

   ``EXPLAIN (ANALYZE, SERIALIZE)`` is most useful when:

   A. You suspect the planner is choosing the wrong join strategy.

   B. You want to measure how long it takes to serialize the query
      results for network transfer, and how large the output is.

   C. You want to diagnose transaction isolation.

   D. You want to see the GPU utilization.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The SERIALIZE flag reports serialization time, output
   size, and format -- useful when network transfer dominates query
   cost.


.. admonition:: Question 18
   :class: hint

   ``work_mem`` primarily controls:

   A. The size of the transaction log.

   B. The memory per sort / hash / aggregate operation before it
      spills to disk.

   C. The maximum number of connections.

   D. The WAL segment size.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``work_mem`` is the per-operation memory budget. When
   sorts or hash tables outgrow it, they spill to disk, raising IO
   cost.


----


True / False (Questions 19-28)
================================


.. admonition:: Question 19
   :class: hint

   **True or False:** ``EXPLAIN`` executes the query and reports
   actual timings.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Plain ``EXPLAIN`` only reports estimates.
   ``EXPLAIN ANALYZE`` executes the query.


.. admonition:: Question 20
   :class: hint

   **True or False:** Cost numbers in a query plan are in
   milliseconds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Cost numbers are a relative, unitless measure
   calibrated by the planner's cost constants. Actual milliseconds
   appear only in the ``actual time=...`` fields when you use
   ``EXPLAIN ANALYZE``.


.. admonition:: Question 21
   :class: hint

   **True or False:** A query with ``WHERE UPPER(name) = 'ADA'`` can
   use an ordinary B-tree index on ``name``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- The ``UPPER()`` call on the indexed column makes the
   predicate non-SARGABLE. A **functional index** on
   ``UPPER(name)`` would rescue it.


.. admonition:: Question 22
   :class: hint

   **True or False:** ``EXPLAIN ANALYZE`` on a ``DELETE`` actually
   deletes the rows, unless wrapped in a transaction that is rolled
   back.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- ``EXPLAIN ANALYZE`` runs the statement. Always use
   ``BEGIN; ... ROLLBACK;`` around mutating diagnostics.


.. admonition:: Question 23
   :class: hint

   **True or False:** A Nested Loop Join always outperforms a Hash
   Join.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Nested Loop is the best choice when one side is
   small or the inner side is indexed. For large unindexed joins,
   Hash Join (if memory allows) or Merge Join is usually better.


.. admonition:: Question 24
   :class: hint

   **True or False:** Hash joins can only be used for equality join
   conditions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- Hashing requires equality. Inequality or range join
   conditions force Nested Loop.


.. admonition:: Question 25
   :class: hint

   **True or False:** A compound index ``(a, b)`` can efficiently
   serve queries filtering only on ``b``.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- The leftmost-prefix rule says you must reference
   ``a`` in the predicate for the index to be used efficiently.


.. admonition:: Question 26
   :class: hint

   **True or False:** In PostgreSQL, a Common Table Expression (CTE)
   is always materialized into a temporary result set before being
   used.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Since PostgreSQL 12, non-recursive / non-mutable
   CTEs are **inlined** by default (equivalent to a subquery).
   You can force materialization with ``WITH ... AS MATERIALIZED``.


.. admonition:: Question 27
   :class: hint

   **True or False:** Adding an index always improves query
   performance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Indexes cost storage, memory, and write performance.
   They help read-heavy SARGABLE queries; they don't help
   non-SARGABLE queries and can slow down write-heavy workloads.


.. admonition:: Question 28
   :class: hint

   **True or False:** If a query's plan shows a large
   ``Rows Removed by Filter`` number, an index or an earlier filter
   may be able to reduce the work done.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- A large rows-removed count means the scan did
   substantial work discarding rows. Pushing the filter earlier, or
   indexing the filter column, typically helps.


----


Essay Questions (Questions 29-32)
=================================


.. admonition:: Question 29
   :class: hint

   Explain the difference between the **estimated** and **actual**
   row counts shown by ``EXPLAIN ANALYZE``, and why a large divergence
   between them is a problem worth investigating.

.. dropdown:: Answer
   :class-container: sd-border-success

   The estimated row count (``rows=...``) is what the planner
   predicted based on table statistics. The actual row count
   (``actual rows=...``) is what the query really produced.

   Large divergences (e.g., estimated 100, actual 100000) mean the
   planner is optimizing for the wrong workload: it may pick a
   Nested Loop where a Hash Join would have been better, or a Seq
   Scan where an Index Scan would have been better. The usual fix
   is to refresh statistics with ``ANALYZE`` (distinct from the
   ``EXPLAIN ANALYZE`` clause), or -- for pathological distributions
   -- to extend statistics with ``CREATE STATISTICS`` or change the
   data model.


.. admonition:: Question 30
   :class: hint

   Describe the three physical join strategies PostgreSQL may choose
   from, and for each, state one scenario in which it is the best
   choice.

.. dropdown:: Answer
   :class-container: sd-border-success

   - **Nested Loop Join**: for each row in the outer relation, probe
     the inner. Best when one side is very small or the inner side
     is well-indexed. A Memoize layer can accelerate repeated
     lookups.
   - **Merge Join**: sort both sides on the join key, then walk in
     parallel. Best when data does not fit in ``work_mem`` for a
     hash join, or when the data is already sorted (e.g., an
     index-order scan), so the sort cost is amortized.
   - **Hash Join**: build a hash table on the inner relation; probe
     with the outer. Best when the hash table fits in ``work_mem``
     and the tables are large enough that iteration would beat
     construction. Requires equality join conditions.


.. admonition:: Question 31
   :class: hint

   A teammate claims they can always speed up a query by adding an
   index on every column used in ``WHERE``. Critique this advice and
   propose a better heuristic.

.. dropdown:: Answer
   :class-container: sd-border-success

   Indexes have real costs: every ``INSERT`` / ``UPDATE`` / ``DELETE``
   must maintain every affected index, and every index consumes disk
   and memory. Over-indexing can dominate write latency and bloat
   storage, and many indexes never get used by the planner.

   Better heuristic: **measure first**, then index. Look at the slow
   query's plan, verify the predicate is **SARGABLE**, check whether
   a compound index matching the workload (following the ESR rule)
   would help. Add indexes deliberately, benchmark with
   ``EXPLAIN (ANALYZE, BUFFERS)`` before and after, and remove
   indexes that turn out to be unused (``pg_stat_user_indexes``).


.. admonition:: Question 32
   :class: hint

   Walk through the optimization journey on a query whose plan shows
   a ``Seq Scan on orders`` with ``cost=0.00..1000000.00`` and
   ``Rows Removed by Filter: 9000000``. What steps would you take, in
   order?

.. dropdown:: Answer
   :class-container: sd-border-success

   A reasonable sequence:

   1. **Read the plan** carefully -- confirm the Seq Scan is really
      the bottleneck (vs a downstream Sort / GroupAggregate).
   2. **Check the filter predicate** for SARGABILITY -- any
      ``UPPER()``, ``LOWER()``, arithmetic, or leading wildcards
      should be removed or rescued with functional indexes.
   3. **Consider a targeted index** on the filter column (or a
      compound index matching the observed filter + sort / group
      pattern, following ESR).
   4. **Check selectivity** -- if the filter is not selective enough
      (e.g., returns 80% of rows), an index won't help; consider
      partitioning, denormalization, or a different data model.
   5. **Re-run ``EXPLAIN (ANALYZE, BUFFERS)``** to confirm the Seq
      Scan is replaced by an Index Scan and that IO drops.
   6. **Verify write cost** did not increase materially; if it did,
      consider a partial index (``WHERE status = 'open'``) or a
      functional index that covers only the hot query.
