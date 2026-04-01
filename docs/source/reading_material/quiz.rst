====================================================
Quiz
====================================================

This quiz covers the topics from the
:doc:`select_aggregates_subqueries` reading material: ``SELECT``
fundamentals (``WHERE``, ``ORDER BY``, ``LIMIT`` / ``OFFSET``), aggregate
functions (``COUNT``, ``SUM``, ``AVG``, ``MIN``, ``MAX``), ``GROUP BY``,
``HAVING``, and subqueries (non-correlated and correlated).

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-15)
================================

.. admonition:: Question 1
   :class: hint

   What is the correct logical evaluation order of SQL clauses?

   A. ``SELECT`` -> ``FROM`` -> ``WHERE`` -> ``GROUP BY`` -> ``HAVING`` -> ``ORDER BY``

   B. ``FROM`` -> ``WHERE`` -> ``GROUP BY`` -> ``HAVING`` -> ``SELECT`` -> ``ORDER BY``

   C. ``FROM`` -> ``SELECT`` -> ``WHERE`` -> ``GROUP BY`` -> ``HAVING`` -> ``ORDER BY``

   D. ``SELECT`` -> ``FROM`` -> ``GROUP BY`` -> ``WHERE`` -> ``HAVING`` -> ``ORDER BY``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``FROM`` -> ``WHERE`` -> ``GROUP BY`` -> ``HAVING`` -> ``SELECT`` -> ``ORDER BY``

   SQL evaluates ``FROM`` first to identify the source rows, then ``WHERE``
   filters individual rows, ``GROUP BY`` forms groups, ``HAVING`` filters
   groups, ``SELECT`` computes output columns, and ``ORDER BY`` sorts the
   final result. This is the logical order; the optimizer may execute
   steps differently for performance.


.. admonition:: Question 2
   :class: hint

   What happens if you use ``LIMIT`` and ``OFFSET`` without ``ORDER BY``?

   A. PostgreSQL raises a syntax error.

   B. The result is always sorted by primary key.

   C. The rows returned may be non-deterministic, causing pages to contain
      duplicates or miss rows.

   D. ``OFFSET`` is ignored.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The rows returned may be non-deterministic.

   Without ``ORDER BY``, PostgreSQL makes no guarantee about row order.
   Consecutive pages may overlap or skip rows depending on the physical
   storage order, which can change after ``VACUUM`` or concurrent writes.


.. admonition:: Question 3
   :class: hint

   What does ``COUNT(*)`` count?

   A. Only non-NULL values in the first column.

   B. All rows, including those with NULL values.

   C. Distinct rows only.

   D. Only rows where every column is non-NULL.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- All rows, including those with NULL values.

   ``COUNT(*)`` counts every row regardless of NULL values. Use
   ``COUNT(column)`` to count only non-NULL values in a specific column.


.. admonition:: Question 4
   :class: hint

   What is the difference between ``COUNT(column)`` and
   ``COUNT(DISTINCT column)``?

   A. No difference; they always return the same number.

   B. ``COUNT(column)`` counts all non-NULL values; ``COUNT(DISTINCT column)``
      counts unique non-NULL values.

   C. ``COUNT(DISTINCT column)`` includes NULL as a distinct value.

   D. ``COUNT(column)`` counts NULLs; ``COUNT(DISTINCT column)`` does not.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``COUNT(column)`` counts all non-NULL values;
   ``COUNT(DISTINCT column)`` counts unique non-NULL values.

   Both ignore NULLs, but ``DISTINCT`` eliminates duplicates before
   counting.


.. admonition:: Question 5
   :class: hint

   Which clause filters **groups** after aggregation?

   A. ``WHERE``

   B. ``GROUP BY``

   C. ``HAVING``

   D. ``ORDER BY``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``HAVING``

   ``HAVING`` is evaluated after ``GROUP BY`` and filters entire groups
   based on aggregate conditions. ``WHERE`` filters individual rows before
   grouping.


.. admonition:: Question 6
   :class: hint

   Given ``SELECT city, COUNT(*) FROM customers GROUP BY city``, what
   happens if you add ``WHERE COUNT(*) > 2`` instead of
   ``HAVING COUNT(*) > 2``?

   A. PostgreSQL returns the same result either way.

   B. PostgreSQL raises an error because aggregate functions cannot appear
      in ``WHERE``.

   C. ``WHERE`` silently ignores the aggregate.

   D. The query runs but returns zero rows.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- PostgreSQL raises an error.

   ``WHERE`` is evaluated before ``GROUP BY``, so aggregate functions are
   not yet computed and cannot be referenced. Use ``HAVING`` to filter on
   aggregates.


.. admonition:: Question 7
   :class: hint

   What does ``SUM(column)`` return if all values in the group are NULL?

   A. 0

   B. NULL

   C. An error

   D. An empty string

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- NULL

   All aggregate functions except ``COUNT`` return NULL when applied to an
   all-NULL input set. Use ``COALESCE(SUM(column), 0)`` to substitute 0.


.. admonition:: Question 8
   :class: hint

   In ``SELECT dept, AVG(salary) FROM employees GROUP BY dept``, which
   columns can appear in the ``SELECT`` list without being inside an
   aggregate function?

   A. Any column from the ``employees`` table.

   B. Only columns that appear in the ``GROUP BY`` clause.

   C. Only the primary key.

   D. No columns at all; only aggregates are allowed.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Only columns that appear in the ``GROUP BY`` clause.

   Every column in the ``SELECT`` list must either be in ``GROUP BY`` or
   wrapped in an aggregate function. PostgreSQL enforces this rule and
   raises an error otherwise. (PostgreSQL does allow non-grouped columns
   that are functionally dependent on the grouped columns, but the general
   rule is to include them in ``GROUP BY``.)


.. admonition:: Question 9
   :class: hint

   What is a non-correlated subquery?

   A. A subquery that references columns from the outer query.

   B. A subquery that runs once, independently of the outer query.

   C. A subquery that always returns exactly one row.

   D. A subquery in the ``FROM`` clause only.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A subquery that runs once, independently of the outer query.

   A non-correlated subquery does not reference any columns from the outer
   query. It is evaluated once and its result is used by the outer query.


.. admonition:: Question 10
   :class: hint

   What error occurs if a single-row subquery returns more than one row?

   A. The query returns the first row silently.

   B. ``ERROR: more than one row returned by a subquery used as an expression``

   C. The query returns NULL.

   D. PostgreSQL picks a random row.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``ERROR: more than one row returned by a subquery used as an expression``

   When a subquery is used with ``=``, ``<``, ``>``, etc., PostgreSQL
   expects exactly one row. Returning multiple rows is a runtime error.


.. admonition:: Question 11
   :class: hint

   Which operator should you use to compare a value against a set of rows
   returned by a subquery?

   A. ``= (subquery)``

   B. ``IN (subquery)``

   C. ``LIKE (subquery)``

   D. ``BETWEEN (subquery)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``IN (subquery)``

   ``IN`` checks whether a value matches any value in the subquery result
   set. ``= (subquery)`` only works for single-row subqueries.


.. admonition:: Question 12
   :class: hint

   What does ``> ANY (subquery)`` mean?

   A. Greater than every value returned by the subquery.

   B. Greater than at least one value returned by the subquery.

   C. Greater than the average of the subquery results.

   D. Greater than NULL.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Greater than at least one value returned by the subquery.

   ``> ANY`` is true if the comparison holds for at least one row in the
   subquery. ``> ALL`` requires the comparison to hold for every row.


.. admonition:: Question 13
   :class: hint

   How does a correlated subquery differ from a non-correlated subquery?

   A. A correlated subquery uses ``JOIN`` instead of ``WHERE``.

   B. A correlated subquery references columns from the outer query and is
      re-evaluated for each outer row.

   C. A correlated subquery always returns multiple rows.

   D. A correlated subquery cannot use aggregate functions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A correlated subquery references columns from the outer query
   and is re-evaluated for each outer row.

   This row-by-row execution makes correlated subqueries more expensive
   than non-correlated ones. Indexing the correlated column helps.


.. admonition:: Question 14
   :class: hint

   Why is ``NOT EXISTS`` generally preferred over ``NOT IN`` when the
   subquery column may contain NULLs?

   A. ``NOT EXISTS`` is always faster.

   B. ``NOT IN`` with NULLs in the subquery always returns an empty result
      set because ``x NOT IN (..., NULL, ...)`` is never true.

   C. ``NOT EXISTS`` can use ``HAVING`` but ``NOT IN`` cannot.

   D. There is no difference; they are interchangeable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``NOT IN`` with NULLs in the subquery always returns empty.

   ``x <> NULL`` evaluates to ``NULL`` (unknown), not ``TRUE``. Since
   ``NOT IN`` requires all comparisons to be true, a single NULL in the
   subquery result causes the entire ``NOT IN`` to fail. ``NOT EXISTS``
   uses boolean logic (exists or does not exist) and handles NULLs
   correctly.


.. admonition:: Question 15
   :class: hint

   A subquery in the ``FROM`` clause must have:

   A. A ``WHERE`` clause.

   B. An alias.

   C. A ``LIMIT`` clause.

   D. A correlated reference to the outer query.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- An alias.

   PostgreSQL requires every derived table (subquery in ``FROM``) to have
   an alias so the outer query can reference its columns:
   ``FROM (SELECT ...) AS alias_name``.


----


True / False (Questions 16-22)
==============================

.. admonition:: Question 16
   :class: hint

   True or False: ``WHERE`` and ``HAVING`` can be used interchangeably.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``WHERE`` filters individual rows before grouping. ``HAVING`` filters
   groups after aggregation. They operate at different stages of query
   evaluation and cannot be swapped.


.. admonition:: Question 17
   :class: hint

   True or False: ``AVG(column)`` includes NULL values in its calculation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``AVG`` ignores NULL values. It computes the sum of non-NULL values
   divided by the count of non-NULL values.


.. admonition:: Question 18
   :class: hint

   True or False: ``ORDER BY`` can reference column aliases defined in the
   ``SELECT`` list.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   In PostgreSQL, ``ORDER BY`` is evaluated after ``SELECT``, so it can
   use aliases: ``SELECT price * qty AS total ... ORDER BY total``.


.. admonition:: Question 19
   :class: hint

   True or False: A correlated subquery always runs slower than a
   non-correlated subquery.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   While correlated subqueries conceptually execute once per outer row, the
   PostgreSQL optimizer can sometimes flatten them into joins or use other
   strategies. With proper indexes, a correlated subquery can be fast.
   Performance depends on the specific query and data.


.. admonition:: Question 20
   :class: hint

   True or False: ``OFFSET`` is efficient on large tables because
   PostgreSQL skips directly to the requested position.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   PostgreSQL must scan and discard all rows before the offset. For large
   offsets, this is expensive. Keyset pagination (``WHERE id > last_seen``)
   is more efficient for deep pages.


.. admonition:: Question 21
   :class: hint

   True or False: ``GROUP BY customer_id`` and ``GROUP BY customer_id,
   customer_name`` always produce the same number of groups if
   ``customer_id`` is the primary key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Since ``customer_id`` is the primary key, ``customer_name`` is
   functionally dependent on it. Adding a functionally dependent column to
   ``GROUP BY`` does not change the number of groups. PostgreSQL recognizes
   this dependency.


.. admonition:: Question 22
   :class: hint

   True or False: ``SELECT DISTINCT`` and ``GROUP BY`` always produce
   identical results.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``SELECT DISTINCT`` removes duplicate rows from the output.
   ``GROUP BY`` forms groups and allows aggregate functions. Without
   aggregates, they may produce the same rows, but ``GROUP BY`` enables
   computations like ``COUNT`` and ``SUM`` that ``DISTINCT`` does not.


----


Essay Questions (Questions 23-25)
=================================

.. admonition:: Question 23
   :class: hint

   Explain in 2-4 sentences why you must use ``HAVING`` instead of
   ``WHERE`` to filter on an aggregate value like ``COUNT(*) > 5``. What
   happens if you try to put this condition in the ``WHERE`` clause?

.. dropdown:: Answer
   :class-container: sd-border-success

   ``WHERE`` is evaluated before ``GROUP BY``, so aggregate functions have
   not yet been computed and cannot be referenced. Placing ``COUNT(*) > 5``
   in ``WHERE`` causes PostgreSQL to raise an error: aggregate functions
   are not allowed in ``WHERE``. ``HAVING`` is evaluated after ``GROUP BY``
   and has access to the aggregated values, making it the correct place for
   group-level filters.


.. admonition:: Question 24
   :class: hint

   Compare non-correlated and correlated subqueries. Give one scenario
   where each type is the better choice, and explain why.

.. dropdown:: Answer
   :class-container: sd-border-success

   A **non-correlated subquery** is best when the inner query is
   independent -- for example, finding all orders placed by customers in a
   specific city: ``WHERE customer_id IN (SELECT customer_id FROM
   customers WHERE city = 'Berlin')``. The subquery runs once and its
   result is reused for every outer row.

   A **correlated subquery** is best when the condition depends on the
   current outer row -- for example, finding employees who earn above their
   department's average: ``WHERE salary > (SELECT AVG(salary) FROM
   employees WHERE department_id = e.department_id)``. The average must be
   recalculated for each department, which requires referencing the outer
   row's ``department_id``.


.. admonition:: Question 25
   :class: hint

   A junior developer writes the following query and says it "doesn't work
   right." Identify the bug and explain how to fix it.

   .. code-block:: sql

      SELECT c.customer_name, COUNT(o.order_id) AS num_orders
      FROM customers c
      LEFT JOIN orders o ON o.customer_id = c.customer_id
      WHERE COUNT(o.order_id) > 2
      GROUP BY c.customer_name;

.. dropdown:: Answer
   :class-container: sd-border-success

   The bug is that ``COUNT(o.order_id) > 2`` is in the ``WHERE`` clause,
   but ``WHERE`` is evaluated before ``GROUP BY``, so aggregate functions
   are not available. PostgreSQL raises an error. The fix is to move the
   aggregate filter to ``HAVING``:

   .. code-block:: sql

      SELECT c.customer_name, COUNT(o.order_id) AS num_orders
      FROM customers c
      LEFT JOIN orders o ON o.customer_id = c.customer_id
      GROUP BY c.customer_name
      HAVING COUNT(o.order_id) > 2;
