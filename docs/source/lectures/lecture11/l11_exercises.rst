====================================================
Exercises
====================================================

This page contains exercises for Lecture 11. These exercises are
designed to reinforce your understanding of query plans, ``EXPLAIN``
and ``EXPLAIN ANALYZE``, SARGABLE query design, compound-index design,
and join strategies.

All exercises use the ``enpm818t`` sample database from the
:doc:`PostgreSQL Setup Guide <l11_postgres_setup>` unless stated
otherwise.


.. dropdown:: Exercise 1 -- Read a Basic Query Plan
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice reading the fields of a basic ``EXPLAIN ANALYZE`` output.

    **Task**

    Run the following query and answer the questions:

    .. code-block:: sql

       EXPLAIN ANALYZE
       SELECT * FROM employees WHERE age > 30;

    1. Is this using a ``Seq Scan`` or an ``Index Scan``? Why?
    2. How many rows did the planner **estimate** would match? How
       many **actually** did?
    3. How many rows were examined but removed by the filter?
    4. What is the total (end-to-end) **Execution Time**?

    .. dropdown:: Solution
       :class-container: sd-border-success

       Results will vary slightly, but a typical plan looks like:

       .. code-block:: text

          Seq Scan on employees  (cost=0.00..22.50 rows=791 width=39) (actual time=0.053..0.404 rows=791 loops=1)
            Filter: (age > 30)
            Rows Removed by Filter: 209
          Planning Time: 0.146 ms
          Execution Time: 0.506 ms

       1. **Seq Scan** -- there is no index on ``age``, and even if
          there were, the planner might still prefer a sequential
          scan when a large fraction of rows match.
       2. Estimated **791**, actual **791** (for this data). In
          general ``rows=ESTIMATE`` and ``actual rows=MEASURED``.
       3. **209** rows were removed by the filter (out of 1000 total).
       4. **Execution Time ≈ 0.5 ms** in the example.


.. dropdown:: Exercise 2 -- Estimate vs Reality
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Understand the difference between planner estimates and measured
    execution.

    **Task**

    Run both commands and compare:

    .. code-block:: sql

       EXPLAIN
       SELECT * FROM employees WHERE age > 30;

       EXPLAIN ANALYZE
       SELECT * FROM employees WHERE age > 30;

    1. Which output includes ``actual time=...``?
    2. Which output has ``Rows Removed by Filter``?
    3. Why would you ever use ``EXPLAIN`` (without ``ANALYZE``)?

    .. dropdown:: Solution
       :class-container: sd-border-success

       1. Only ``EXPLAIN ANALYZE`` -- plain ``EXPLAIN`` does not
          execute the query.
       2. Only ``EXPLAIN ANALYZE`` -- the rows-removed count requires
          actual execution.
       3. Use plain ``EXPLAIN`` when the query would be expensive or
          destructive to run, or when you just want the planner's
          estimate for comparison. For any diagnostic where you want
          real times, prefer ``EXPLAIN ANALYZE``. For mutating queries,
          wrap it in ``BEGIN; ... ROLLBACK;``.


.. dropdown:: Exercise 3 -- SARGABLE vs Non-SARGABLE
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Identify query patterns that defeat indexes.

    **Task**

    For each of the following, state whether it is **SARGABLE** and
    why (assume an index exists on the relevant column):

    1. ``WHERE age > 30``
    2. ``WHERE age + 1 > 31``
    3. ``WHERE UPPER(name) = 'ADA'``
    4. ``WHERE name LIKE 'Ada%'``
    5. ``WHERE name LIKE '%ada'``
    6. ``WHERE salary BETWEEN 50000 AND 80000``
    7. ``WHERE id NOT IN (1, 2, 3)``
    8. ``WHERE hire_date >= '2020-01-01'``

    .. dropdown:: Solution
       :class-container: sd-border-success

       1. **SARGABLE** -- simple comparison.
       2. **Non-SARGABLE** -- arithmetic on the column side forces
          row-by-row evaluation. Rewrite as ``age > 30``.
       3. **Non-SARGABLE** -- ``UPPER(name)`` transforms the column.
          Rescue: create a **functional index** on ``UPPER(name)``, or
          store the data in a canonical case.
       4. **SARGABLE** -- left-anchored ``LIKE`` works with B-tree
          prefix matching.
       5. **Non-SARGABLE** -- leading wildcard defeats B-tree prefix
          matching. A trigram index (``pg_trgm``) or reversed-string
          index can rescue it.
       6. **SARGABLE** -- ``BETWEEN`` is a range predicate.
       7. Usually **non-SARGABLE** -- negation forces scanning the
          whole range.
       8. **SARGABLE** -- simple range comparison.


.. dropdown:: Exercise 4 -- Compound Index Design
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Design a compound index for a frequent query shape and apply the
    leftmost-prefix rule.

    **Frequent query shape**

    .. code-block:: sql

       SELECT name, salary
       FROM employees
       WHERE department_id = 1
         AND hire_date > '2022-01-01'
       ORDER BY hire_date DESC;

    **Questions**

    1. What compound index would you create?
    2. What is the recommended field order, and why?
    3. Would the same index also help
       ``WHERE hire_date > '2022-01-01'`` alone? Why or why not?
    4. What changes in the plan once you add the index?

    .. dropdown:: Solution
       :class-container: sd-border-success

       **Recommended starting point:**

       .. code-block:: sql

          CREATE INDEX idx_employees_dept_hire
            ON employees(department_id, hire_date DESC);

       **Rationale:**

       - **Equality column first** (``department_id``): narrows the
         range as much as possible.
       - **Range / sort column second** (``hire_date DESC``): the
         index can deliver rows already in the required order, so the
         planner can skip the ``Sort`` step.
       - This follows the **Equality-Sort-Range (ESR)** guideline.

       **Single-column usefulness**: the same index **does not** help
       a query filtering on ``hire_date`` alone, because of the
       **leftmost-prefix rule**. Queries on ``department_id`` alone
       *do* use the index.

       **Plan change**: expect the ``Seq Scan`` to be replaced by an
       ``Index Scan`` (or ``Index Only Scan`` if only indexed columns
       are selected) and the explicit ``Sort`` step to disappear.


.. dropdown:: Exercise 5 -- Reproduce the Join-Key Speedup
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Reproduce the 3x speedup from the lecture by changing the join key
    from a string column to a foreign-key integer.

    **Task**

    Run both versions of the query and compare:

    .. code-block:: sql

       -- Version A: join on department name (text)
       EXPLAIN ANALYZE
       SELECT departments.name, COUNT(*), AVG(employees.salary)
       FROM departments
       JOIN employees ON departments.name = employees.department
       WHERE employees.hire_date > '2020-01-01'
       GROUP BY departments.name
       HAVING COUNT(*) > 10
       ORDER BY AVG(employees.salary) DESC
       LIMIT 5;

       -- Version B: join on department_id (int, indexed PK)
       EXPLAIN ANALYZE
       SELECT departments.name, COUNT(*), AVG(employees.salary)
       FROM departments
       JOIN employees ON departments.id = employees.department_id
       WHERE employees.hire_date > '2020-01-01'
       GROUP BY departments.name
       HAVING COUNT(*) > 10
       ORDER BY AVG(employees.salary) DESC
       LIMIT 5;

    1. What join strategies did the planner pick for each?
    2. Which version has fewer ``Sort`` steps?
    3. Do you see a ``Memoize`` step in Version B? What does it do?
    4. Compare the ``Execution Time`` of each.

    .. dropdown:: Solution
       :class-container: sd-border-success

       - **Version A** typically uses a **Merge Join** with two
         explicit sorts (one on each side). String comparison +
         unindexed column → expensive prep.
       - **Version B** typically uses a **Nested Loop** with an
         **Index Scan** on ``departments_pkey`` and a **Memoize**
         over the index lookup. ``Memoize`` caches the per-key result
         so repeated probes hit the cache instead of re-scanning --
         expect **hits** ≫ **misses**.
       - Version B has **no** explicit sort on the join side, since
         the index walks keys in order.
       - Execution Time typically drops **2-3x** on this sample
         dataset. The lesson is that a small modeling change (use
         the FK integer, not the denormalized text) can deliver a
         larger performance win than most query tweaks.


.. dropdown:: Exercise 6 -- BUFFERS and Cold vs Warm Cache
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Interpret ``shared hit=N`` vs ``shared read=N`` in
    ``EXPLAIN (ANALYZE, BUFFERS)`` output.

    **Task**

    1. Restart the PostgreSQL container to drop its caches:

       .. code-block:: bash

          docker restart postgres

    2. Run the query **immediately** (cold cache):

       .. code-block:: sql

          EXPLAIN (ANALYZE, BUFFERS)
          SELECT * FROM employees WHERE hire_date > '2020-01-01';

    3. Run the **same query again** (warm cache).

    4. Compare the ``Buffers:`` line in each run.

    .. dropdown:: Solution
       :class-container: sd-border-success

       On the **cold** run you will see ``Buffers: shared read=N``
       (data had to come from disk). On the **warm** run you will
       see ``Buffers: shared hit=N`` (data came from the in-process
       buffer cache).

       **Implication**: a query that is fast warm but slow cold is a
       prime candidate for:

       - More memory (``shared_buffers``) so the working set stays
         hot;
       - A tighter index so fewer pages need to be fetched;
       - A schema change that reduces the number of pages touched.


.. dropdown:: Exercise 7 -- Unwind a Complex Plan
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Read an inside-out plan and identify the most expensive step.

    **Task**

    Run the complex lecture query with ``EXPLAIN ANALYZE`` (Version A
    from Exercise 5). Then:

    1. List the steps from **innermost** (first executed) to
       **outermost** (last executed).
    2. Identify the step with the **highest total cost**.
    3. Identify the step with the **highest actual time** (not
       necessarily the same!).
    4. Propose one change to the schema or query that would reduce
       the work at that step.

    .. dropdown:: Solution
       :class-container: sd-border-success

       Typical execution order (innermost first):

       1. ``Seq Scan on employees`` with ``hire_date`` filter.
       2. ``Sort`` the employees side by ``employees.department``.
       3. ``Seq Scan on departments``.
       4. ``Sort`` the departments side by ``departments.name``.
       5. ``Merge Join`` on the two sorted streams.
       6. ``GroupAggregate`` with ``HAVING``.
       7. ``Sort`` by ``avg(salary) DESC``.
       8. ``Limit 5``.

       The two **Sort** steps that prepare for the Merge Join usually
       carry most of the cost. The Merge Join itself is cheap *given*
       sorted input; the sorts pay the price.

       **Fix**: switch the join to use ``department_id`` (indexed
       integer), which lets the planner use a Nested Loop + Index
       Scan + Memoize and eliminates both explicit sort steps
       (see Exercise 5).


.. dropdown:: Exercise 8 -- Match the Join Strategy to the Workload
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Pick the right physical join strategy for a given workload.

    **Scenarios**

    For each, predict whether the planner is likely to choose
    **Nested Loop**, **Merge Join**, or **Hash Join**. Justify.

    1. Two small tables (10 rows × 20 rows) joined on equality.
    2. A 100-row ``departments`` table joined to a 10M-row
       ``employees`` table on a **foreign-key integer** with an index
       on the FK.
    3. Two 50M-row tables joined on an equality condition; neither
       has a useful index; ``work_mem`` is 8 MB.
    4. Two tables joined on an **inequality** (``a.x < b.y``) condition.

    .. dropdown:: Solution
       :class-container: sd-border-success

       1. **Nested Loop** -- with tiny tables, the constant overhead
          of building a hash table or sorting is not worth it.
       2. **Nested Loop + Index Scan** (often with Memoize) -- the
          100-row side scans; each row probes the indexed inner
          relation in ~log(n) time.
       3. **Merge Join** -- the hash table won't fit in 8 MB of
          ``work_mem``, so the planner sorts both sides and merges.
          (If ``work_mem`` were much larger, a Hash Join might win.)
       4. **Nested Loop** -- neither Merge Join nor Hash Join can
          handle non-equality conditions. Only Nested Loop is viable.


.. dropdown:: Exercise 9 -- Safe EXPLAIN on Mutating Queries (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice wrapping diagnostic ``EXPLAIN ANALYZE`` on write queries
    so your database state does not change.

    **Task**

    1. Capture employee 7's current salary with:

       .. code-block:: sql

          SELECT id, name, salary FROM employees WHERE id = 7;

    2. Run the following block, substituting ``ROLLBACK`` where
       appropriate:

       .. code-block:: sql

          BEGIN;
          EXPLAIN ANALYZE
          UPDATE employees SET salary = salary + 1000 WHERE id = 7;
          ROLLBACK;

    3. Re-check employee 7's salary. Is it the original value?

    4. What would have happened if you had used ``COMMIT`` instead of
       ``ROLLBACK``?

    .. dropdown:: Solution
       :class-container: sd-border-success

       - After ``ROLLBACK``, the salary is unchanged -- diagnosis
         leaves no trace.
       - With ``COMMIT``, the update would have been persisted and
         the salary would be 1000 higher.

       **Rule**: any ``EXPLAIN ANALYZE`` on an ``INSERT`` / ``UPDATE``
       / ``DELETE`` should be wrapped in ``BEGIN; ... ROLLBACK;`` by
       default, unless you explicitly want the mutation applied.
