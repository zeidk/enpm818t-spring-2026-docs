====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


SQL Joins in PostgreSQL
====================================================

Semantics, execution, and performance. This lecture covers:

- Practical query writing
- Correctness first, then speed
- PostgreSQL-specific examples

Today's arc is: **what joins mean**, **how to write them safely**, and
**how PostgreSQL actually executes them**. If you can reason about joins,
you can reason about a very large chunk of real SQL.


Prerequisites
----------------------------------------------------

Before working through the examples, make sure you are comfortable with:

- Basic ``SELECT``, ``FROM``, ``WHERE``
- Primary key / foreign key concepts
- Comfort with ``NULL``
- Basic idea of indexes
- Some PostgreSQL familiarity (the syntax is standard-ish, but we will use
  PostgreSQL-friendly examples)


Why Joins Matter
----------------------------------------------------

- Most useful queries span multiple tables.
- Reports are mostly joins + aggregates.
- APIs often assemble joined views of data.
- Slow joins are a common bottleneck.
- Wrong joins give **wrong answers**.


Running Example Schema
----------------------------------------------------

We will reuse this schema throughout the lecture. Later, for self-joins, a
small ``employees`` example is introduced separately.


.. dropdown:: Sample Data -- customers
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 20 30 20
      :header-rows: 1
      :class: compact-table

      * - ``customer_id``
        - ``customer_name``
        - ``city``
      * - 1
        - Ada
        - Berlin
      * - 2
        - Bruno
        - Lisbon
      * - 3
        - Chandra
        - Delhi
      * - 4
        - Diana
        - Oslo


.. dropdown:: Sample Data -- orders
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 15 20 25 15
      :header-rows: 1
      :class: compact-table

      * - ``order_id``
        - ``customer_id``
        - ``order_date``
        - ``total``
      * - 101
        - 1
        - 2026-03-01
        - 120
      * - 102
        - 1
        - 2026-03-05
        - 75
      * - 103
        - 3
        - 2026-03-07
        - 200


Database JOINs
====================================================

Start with the simplest idea:

- Combine rows
- Keep some combinations
- Discard others
- A join is fundamentally about **matching**

.. admonition:: Key Insight
   :class: tip

   A join combines rows from two relations according to a predicate.


Cartesian Product
----------------------------------------------------

- ``R x S`` pairs every row in ``R`` with every row in ``S``.
- Result size is ``|R| x |S|``.
- Usually too large to want directly, but it is the conceptual foundation
  of joins.
- A join can be thought of as a **filtered product**.


.. dropdown:: Cartesian Product Example
   :class-container: sd-border-secondary

   **Table A**

   .. list-table::
      :widths: 50
      :header-rows: 1
      :class: compact-table

      * - ``id``
      * - 1
      * - 2

   **Table B**

   .. list-table::
      :widths: 50
      :header-rows: 1
      :class: compact-table

      * - ``code``
      * - X
      * - Y
      * - Z

   **A x B** = ``(1, X)``, ``(1, Y)``, ``(1, Z)``, ``(2, X)``, ``(2, Y)``, ``(2, Z)``

   Count before querying: ``2 x 3 = 6``. This habit is surprisingly useful
   when debugging joins.


.. dropdown:: Cartesian Product in SQL
   :class-container: sd-border-secondary

   .. code-block:: sql

      SELECT c.customer_name, o.order_id
      FROM customers c
      CROSS JOIN orders o;

   ``4 customers x 3 orders = 12 rows`` -- every customer appears with every
   order. This is almost never what we want for customer-order queries, but it
   is exactly what we want for some generation tasks.


.. dropdown:: Accidental Cartesian Products
   :class-container: sd-border-secondary

   - Missing join predicate = row explosion.
   - Old comma syntax makes mistakes easier.
   - Result counts can become enormous.
   - **Prefer explicit** ``JOIN ... ON``.

   .. code-block:: sql

      -- risky style
      SELECT *
      FROM customers c, orders o;

   What happens if someone forgets the
   ``WHERE c.customer_id = o.customer_id`` condition?


Relational Algebra
----------------------------------------------------

SQL is the practical language; relational algebra is the semantic model. It
describes meaning independent of execution. PostgreSQL optimizes from
declarative intent.


.. dropdown:: Core Relational Operators
   :class-container: sd-border-secondary

   .. list-table::
      :widths: 15 30 30
      :header-rows: 1
      :class: compact-table

      * - **Symbol**
        - **Operation**
        - **SQL Equivalent**
      * - :math:`\sigma`
        - Selection (filter rows)
        - ``WHERE``
      * - :math:`\pi`
        - Projection (choose columns)
        - ``SELECT``
      * - :math:`\times`
        - Product (all combinations)
        - ``CROSS JOIN``
      * - :math:`\bowtie`
        - Join (matching combinations)
        - ``JOIN ... ON``


.. dropdown:: Join in Relational Algebra
   :class-container: sd-border-secondary

   .. math::

      \text{Customers} \bowtie_{\text{Customers.customer_id} = \text{Orders.customer_id}} \text{Orders}

   Equivalent idea:

   .. math::

      \sigma_{\text{Customers.customer_id} = \text{Orders.customer_id}}(\text{Customers} \times \text{Orders})

   Join = product + filter. PostgreSQL does **not** usually materialize the
   full product first; this is about semantics, not implementation.


.. dropdown:: Relational Algebra to SQL
   :class-container: sd-border-secondary

   .. code-block:: sql

      SELECT c.customer_name, o.order_id
      FROM customers c
      JOIN orders o
        ON c.customer_id = o.customer_id;

   SQL says **what**. PostgreSQL decides **how**.


What Is a JOIN?
====================================================

A join combines rows from two relations. A predicate determines which pairs
qualify. Most everyday joins are equality joins, but non-equality joins
(theta joins) also exist.

- **Equi-join**: ``a.id = b.id``
- **Non-equi / theta join**: ranges, inequalities, intervals

We focus on the equality case because that is the bread-and-butter case in
PostgreSQL workloads.


Preferred SQL Join Syntax
----------------------------------------------------

.. code-block:: sql

   FROM customers c
   JOIN orders o
     ON o.customer_id = c.customer_id

- Put relationship logic in ``ON``.
- Put result filters in ``WHERE``.
- Use aliases.
- Avoid old comma joins in new code.

Readable SQL is more maintainable SQL, and maintainable SQL tends to be more
correct SQL.


INNER JOIN: ON vs WHERE
====================================================

.. dropdown:: Style A vs Style B
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Style A: filter in WHERE
      FROM customers c
      JOIN orders o
        ON c.customer_id = o.customer_id
      WHERE o.total > 100;

   .. code-block:: sql

      -- Style B: filter in ON
      FROM customers c
      JOIN orders o
        ON c.customer_id = o.customer_id
       AND o.total > 100;

   For **inner joins**, these are usually equivalent. Still: keep join logic in
   ``ON``, filters in ``WHERE``. The advice is mostly about clarity -- it pays
   off once outer joins enter the picture.


OUTER JOIN: ON vs WHERE
====================================================

.. warning::

   With outer joins, ``ON`` and ``WHERE`` are **not** equivalent.

.. dropdown:: The Difference Demonstrated
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Query 1: filter in ON (preserves unmatched left rows)
      SELECT c.customer_name, o.order_id
      FROM customers c
      LEFT JOIN orders o
        ON c.customer_id = o.customer_id
       AND o.total > 100;

   .. code-block:: sql

      -- Query 2: filter in WHERE (removes NULL-extended rows)
      SELECT c.customer_name, o.order_id
      FROM customers c
      LEFT JOIN orders o
        ON c.customer_id = o.customer_id
      WHERE o.total > 100;

   The second query filters away ``NULL``-extended rows, so it behaves like
   an inner join. Which customers disappear in the second query?


Join Types
====================================================


CROSS JOIN
----------------------------------------------------

.. dropdown:: CROSS JOIN
   :class-container: sd-border-secondary

   Returns every row combination. Useful when all combinations are desired.
   Not a mistake when deliberate.

   .. code-block:: sql

      SELECT s.size, c.color
      FROM sizes s
      CROSS JOIN colors c;

   Good for grids, parameter sets, calendars. ``CROSS JOIN`` is not wrong;
   **accidental** ``CROSS JOIN`` is wrong.


INNER JOIN
----------------------------------------------------

.. dropdown:: INNER JOIN
   :class-container: sd-border-secondary
   :open:

   Keep only matching rows. Unmatched rows from either side disappear. This
   is the most common join in application code.

   .. code-block:: sql

      SELECT c.customer_name, o.order_id, o.total
      FROM customers c
      JOIN orders o
        ON o.customer_id = c.customer_id;

   With our sample data:

   - Ada appears twice (orders 101, 102)
   - Chandra once (order 103)
   - Bruno and Diana do **not** appear

   .. rubric:: Result Table

   .. list-table::
      :widths: 25 20 15
      :header-rows: 1
      :class: compact-table

      * - ``customer_name``
        - ``order_id``
        - ``total``
      * - Ada
        - 101
        - 120
      * - Ada
        - 102
        - 75
      * - Chandra
        - 103
        - 200


.. dropdown:: INNER JOIN Across Multiple Tables
   :class-container: sd-border-secondary

   .. code-block:: sql

      SELECT c.customer_name, p.product_name, oi.qty
      FROM customers c
      JOIN orders o       ON o.customer_id = c.customer_id
      JOIN order_items oi ON oi.order_id = o.order_id
      JOIN products p     ON p.product_id = oi.product_id;

   Joins compose. One-to-many relationships multiply rows. Row counts can
   grow quickly.


LEFT OUTER JOIN
----------------------------------------------------

.. dropdown:: LEFT OUTER JOIN
   :class-container: sd-border-secondary
   :open:

   Keep all rows from the left table. Add matching rows from the right table.
   Missing right-side values become ``NULL``.

   .. code-block:: sql

      SELECT c.customer_name, o.order_id
      FROM customers c
      LEFT JOIN orders o
        ON o.customer_id = c.customer_id;

   This is the workhorse for "show me all parents, even if there are no
   children." Great for customer dashboards, optional metadata, and reporting.

   .. rubric:: Result Table

   .. list-table::
      :widths: 30 20
      :header-rows: 1
      :class: compact-table

      * - ``customer_name``
        - ``order_id``
      * - Ada
        - 101
      * - Ada
        - 102
      * - Bruno
        - ``NULL``
      * - Chandra
        - 103
      * - Diana
        - ``NULL``

   Bruno and Diana appear with ``NULL`` order IDs because they have no orders.


.. dropdown:: Business Domain Example (from LaTeX)
   :class-container: sd-border-secondary

   Using a richer schema with 5 customers and 5 orders:

   **CUSTOMERS Table**

   .. list-table::
      :widths: 15 20 20 30
      :header-rows: 1
      :class: compact-table

      * - ``customer_id``
        - ``first_name``
        - ``last_name``
        - ``email``
      * - 1
        - John
        - Doe
        - john.d@email.com
      * - 2
        - Jane
        - Smith
        - jane.s@email.com
      * - 3
        - Bob
        - Johnson
        - bob.j@email.com
      * - 4
        - Alice
        - Brown
        - alice.b@email.com
      * - 5
        - Charlie
        - Wilson
        - charlie.w@email.com

   **ORDERS Table**

   .. list-table::
      :widths: 15 20 25 20
      :header-rows: 1
      :class: compact-table

      * - ``order_id``
        - ``customer_id``
        - ``order_date``
        - ``total_amount``
      * - 101
        - 1
        - 2024-01-15
        - 150.00
      * - 102
        - 2
        - 2024-01-16
        - 89.99
      * - 103
        - 1
        - 2024-01-20
        - 75.50
      * - 104
        - 3
        - 2024-01-22
        - 230.00
      * - 105
        - 2
        - 2024-01-25
        - 45.00

   .. rubric:: LEFT JOIN Result

   .. list-table::
      :widths: 12 14 14 22 10 16 14
      :header-rows: 1
      :class: compact-table

      * - ``customer_id``
        - ``first_name``
        - ``last_name``
        - ``email``
        - ``order_id``
        - ``order_date``
        - ``total_amount``
      * - 1
        - John
        - Doe
        - john.d@email.com
        - 101
        - 2024-01-15
        - 150.00
      * - 1
        - John
        - Doe
        - john.d@email.com
        - 103
        - 2024-01-20
        - 75.50
      * - 2
        - Jane
        - Smith
        - jane.s@email.com
        - 102
        - 2024-01-16
        - 89.99
      * - 2
        - Jane
        - Smith
        - jane.s@email.com
        - 105
        - 2024-01-25
        - 45.00
      * - 3
        - Bob
        - Johnson
        - bob.j@email.com
        - 104
        - 2024-01-22
        - 230.00
      * - 4
        - Alice
        - Brown
        - alice.b@email.com
        - ``NULL``
        - ``NULL``
        - ``NULL``
      * - 5
        - Charlie
        - Wilson
        - charlie.w@email.com
        - ``NULL``
        - ``NULL``
        - ``NULL``

   Alice and Charlie have no orders, so their order columns are ``NULL``.


RIGHT OUTER JOIN
----------------------------------------------------

.. dropdown:: RIGHT OUTER JOIN
   :class-container: sd-border-secondary

   Keep all rows from the right table. Same idea as ``LEFT JOIN``, with sides
   swapped. Usually rewritten as ``LEFT JOIN``.

   .. code-block:: sql

      SELECT *
      FROM a
      RIGHT JOIN b
        ON a.id = b.id;

   Equivalent style:

   .. code-block:: sql

      SELECT *
      FROM b
      LEFT JOIN a
        ON a.id = b.id;

   ``LEFT JOIN`` is generally recommended over ``RIGHT JOIN``. Nothing wrong
   with ``RIGHT JOIN``; it is just usually harder to read in longer queries,
   and ``LEFT JOIN`` is the de facto standard.


FULL OUTER JOIN
----------------------------------------------------

.. dropdown:: FULL OUTER JOIN
   :class-container: sd-border-secondary

   Keep matching rows, unmatched left rows, and unmatched right rows.

   .. code-block:: sql

      SELECT COALESCE(a.id, b.id) AS id,
             a.val AS left_val,
             b.val AS right_val
      FROM a
      FULL OUTER JOIN b
        ON a.id = b.id;

   Great for reconciliation and comparison tasks: what exists only in system
   A or only in system B?

   .. rubric:: Business Domain Result (CUSTOMERS FULL JOIN ORDERS)

   .. list-table::
      :widths: 12 14 14 22 10 16 14
      :header-rows: 1
      :class: compact-table

      * - ``customer_id``
        - ``first_name``
        - ``last_name``
        - ``email``
        - ``order_id``
        - ``order_date``
        - ``total_amount``
      * - 1
        - John
        - Doe
        - john.d@email.com
        - 101
        - 2024-01-15
        - 150.00
      * - 1
        - John
        - Doe
        - john.d@email.com
        - 103
        - 2024-01-20
        - 75.50
      * - 2
        - Jane
        - Smith
        - jane.s@email.com
        - 102
        - 2024-01-16
        - 89.99
      * - 2
        - Jane
        - Smith
        - jane.s@email.com
        - 105
        - 2024-01-25
        - 45.00
      * - 3
        - Bob
        - Johnson
        - bob.j@email.com
        - 104
        - 2024-01-22
        - 230.00
      * - 4
        - Alice
        - Brown
        - alice.b@email.com
        - ``NULL``
        - ``NULL``
        - ``NULL``
      * - 5
        - Charlie
        - Wilson
        - charlie.w@email.com
        - ``NULL``
        - ``NULL``
        - ``NULL``


NULLs After Outer Joins
----------------------------------------------------

.. dropdown:: NULLs and Aggregates After Outer Joins
   :class-container: sd-border-secondary
   :open:

   Outer joins introduce ``NULL`` s. Be careful with aggregation:

   - ``COUNT(*)`` counts rows (including ``NULL``-extended ones).
   - ``COUNT(o.order_id)`` counts only matches.
   - ``NULL = NULL`` is **not true**.

   .. code-block:: sql

      SELECT c.customer_name,
             COUNT(*)          AS joined_rows,
             COUNT(o.order_id) AS matched_orders
      FROM customers c
      LEFT JOIN orders o
        ON o.customer_id = c.customer_id
      GROUP BY c.customer_name;

   PostgreSQL-specific tip: if you want NULL-safe equality semantics, use
   ``IS NOT DISTINCT FROM``.


Other Joins
====================================================


SELF JOIN
----------------------------------------------------

.. dropdown:: Self Join
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      SELECT e.employee_name,
             m.employee_name AS manager_name
      FROM employees e
      LEFT JOIN employees m
        ON e.manager_id = m.employee_id;

   Same table, two roles. Useful for hierarchies. Alias names are essential.
   This uses a self-referencing foreign key:
   ``manager_id -> employees.employee_id``.


USING and NATURAL
----------------------------------------------------

.. dropdown:: USING and NATURAL JOIN
   :class-container: sd-border-secondary

   .. code-block:: sql

      SELECT *
      FROM customers c
      JOIN orders o USING (customer_id);

   - ``USING`` is concise when column names match.
   - The shared join column appears only once in output.
   - **Avoid** ``NATURAL JOIN`` in production code: it silently depends on
     all same-named columns, so schema changes can change query meaning.


SEMI and ANTI Joins
----------------------------------------------------

.. dropdown:: Semi Join (EXISTS)
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Semi join: customers with orders
      SELECT c.*
      FROM customers c
      WHERE EXISTS (
        SELECT 1
        FROM orders o
        WHERE o.customer_id = c.customer_id
      );

   Often clearer than ``JOIN + DISTINCT``. PostgreSQL may internally produce
   semi-join plan nodes even though SQL syntax uses ``EXISTS``.


.. dropdown:: Anti Join (NOT EXISTS)
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Anti join: customers without orders
      SELECT c.*
      FROM customers c
      WHERE NOT EXISTS (
        SELECT 1
        FROM orders o
        WHERE o.customer_id = c.customer_id
      );

   Prefer ``NOT EXISTS`` over ``NOT IN`` when NULLs may be involved.


LATERAL Join (PostgreSQL)
----------------------------------------------------

.. dropdown:: LATERAL Join
   :class-container: sd-border-secondary

   .. code-block:: sql

      SELECT c.customer_name, x.order_id, x.order_date
      FROM customers c
      LEFT JOIN LATERAL (
        SELECT o.order_id, o.order_date
        FROM orders o
        WHERE o.customer_id = c.customer_id
        ORDER BY o.order_date DESC
        LIMIT 1
      ) x ON true;

   Evaluate the subquery per left-side row. Excellent for "latest row per
   parent." ``LATERAL`` lets the right-hand side depend on the current
   left-hand row.


Logical Join vs Physical Join
====================================================

- **Logical join** answers: **which rows**
- **Physical join** answers: **how computed**

"Hash join" is not equivalent to "inner join" or vice versa.
INNER joins can often be reordered more freely than outer joins.


Nested Loop Join
----------------------------------------------------

.. dropdown:: Nested Loop Join
   :class-container: sd-border-secondary
   :open:

   - Very simple idea: for each row on the left, look for matches on the right.
   - Great when outer side is small.
   - Excellent with an index on the inner join key.
   - Can be very expensive without one.
   - Very flexible: works for many predicates, not just equality.


Hash Join
----------------------------------------------------

.. dropdown:: Hash Join
   :class-container: sd-border-secondary
   :open:

   - Strong choice for large equality joins.
   - No sorted input required.
   - Often very fast.
   - Sensitive to memory limits.
   - Important: a **hash join does not require a hash index**.


Merge Join
----------------------------------------------------

.. dropdown:: Merge Join
   :class-container: sd-border-secondary
   :open:

   - Good when both sides are already sorted, or when sorting is still
     affordable.
   - Strong option for large datasets.
   - This is the "merge two sorted lists" idea from algorithms.
   - In PostgreSQL, merge join typically shines when the join keys are sortable
     and useful ordering already exists.


Reading EXPLAIN
====================================================

.. dropdown:: Using EXPLAIN (ANALYZE, BUFFERS)
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      EXPLAIN (ANALYZE, BUFFERS)
      SELECT c.customer_name, o.order_id
      FROM customers c
      JOIN orders o
        ON o.customer_id = c.customer_id;

   Example plan shape:

   .. code-block:: text

      Hash Join
        Hash Cond: (o.customer_id = c.customer_id)
        -> Seq Scan on orders o
        -> Hash
             -> Seq Scan on customers c

   - Look for the join node.
   - Compare estimated rows vs actual rows.
   - Check buffers and timing.

   Bad estimates often cause bad join choices.


Big O Notation
====================================================

Big O describes growth as input grows. It is not exact runtime -- constants
still matter. In databases, I/O often dominates.


.. dropdown:: Common Big O Complexities
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 20 35 45
      :header-rows: 1
      :class: compact-table

      * - **Complexity**
        - **Intuition**
        - **Database example**
      * - ``O(1)``
        - constant work
        - ideal hash bucket lookup
      * - ``O(log n)``
        - reduce search space each step
        - B-tree navigation
      * - ``O(n)``
        - touch everything once
        - sequential scan
      * - ``O(n log n)``
        - sort plus process
        - sort before merge join
      * - ``O(n^2)``
        - pairwise combinations
        - naive nested loops

   ``n log n`` is usually survivable; ``n^2`` is where sadness begins.


.. dropdown:: Join Algorithms and Big O
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 25 35 40
      :header-rows: 1
      :class: compact-table

      * - **Join strategy**
        - **Rough cost model**
        - **Best-case intuition**
      * - Nested loop
        - ``O(n * m)``
        - small outer + indexed inner
      * - Hash join
        - ``O(n + m)``
        - equality join, enough memory
      * - Merge join
        - ``O(n log n + m log m)``
        - or ``O(n + m)`` if pre-sorted

   Real databases also pay for page reads and cache misses. This table is
   deliberately approximate. PostgreSQL's planner uses richer cost models,
   but these approximations build strong intuition.


.. dropdown:: Queries, Scalability, and Big O
   :class-container: sd-border-secondary

   - ``1,000 x 1,000 = 1,000,000``
   - ``1,000,000 x 1,000,000 = 1,000,000,000,000``
   - Toy datasets can hide terrible plans.
   - Selectivity and indexes change what is practical.
   - Your dev database may be lying to you: a plan that looks fine on 5,000
     rows can be catastrophic on 500 million.


Disk Storage Architecture
====================================================

.. dropdown:: Heap Tables and Index Files
   :class-container: sd-border-secondary
   :open:

   - PostgreSQL stores tables and indexes separately.
   - Access is **page-oriented**, not row-oriented.
   - PostgreSQL's default page size is **8 KB**.
   - Indexes tell PostgreSQL where to find tuples in the heap.


.. dropdown:: Why Disk Layout Changes Join Cost
   :class-container: sd-border-secondary

   - Sequential reads are usually cheaper than random reads.
   - Many index lookups can mean many random page fetches.
   - If many rows match, a seq scan can beat an index scan.
   - Bloat means more pages and more I/O.

   **A sequential scan is not a moral failure.** If the query needs a large
   fraction of the table, a seq scan may be the right plan.


Memory Storage Architecture
----------------------------------------------------

.. dropdown:: shared_buffers and work_mem
   :class-container: sd-border-secondary
   :open:

   - ``shared_buffers`` caches pages.
   - ``work_mem`` supports sorts and hash tables.
   - Spills go to temporary files.
   - Hash joins build hash tables in memory.
   - Merge joins may require sort memory.
   - Each sort/hash node can use its own ``work_mem``.
   - Too low -> temp files. Too high -> memory pressure.

   A single query can use multiple chunks of ``work_mem``, especially with
   complex plans or parallel execution.


Indexing
====================================================

Indexes reduce search space, enable better join strategies, but cost storage
and write overhead.

.. code-block:: sql

   CREATE INDEX orders_customer_id_idx
   ON orders(customer_id);

Indexes are one of the main tools for turning a painful join into an
acceptable one. They are not free; every insert/update/delete pays something.


.. dropdown:: Index Data Structures in PostgreSQL
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 15 35 35
      :header-rows: 1
      :class: compact-table

      * - **Index type**
        - **Best for**
        - **Join relevance**
      * - B-tree
        - equality, range, ordering
        - most common
      * - Hash
        - equality only
        - niche
      * - GiST
        - geometric/range-like search
        - specialized
      * - GIN
        - arrays, ``jsonb``, full text
        - membership/search
      * - BRIN
        - huge ordered tables
        - coarse filtering

   Default ``CREATE INDEX`` uses B-tree. Hash indexes exist, but **hash
   joins do not depend on hash indexes**.


B+ Trees
----------------------------------------------------

.. dropdown:: B+ Tree Intuition
   :class-container: sd-border-secondary
   :open:

   - High fan-out keeps trees shallow.
   - Leaves are ordered and linked.
   - Great for equality lookups and range scans.

   **Rules / how to build:**

   - Keys stay sorted in each node.
   - Insert into the appropriate leaf.
   - If a node overflows, split it.
   - Push a separator upward.
   - All leaves stay at the same depth -- this property keeps lookup cost
     predictable.


.. dropdown:: B+ Trees in Join Queries
   :class-container: sd-border-secondary

   .. code-block:: sql

      CREATE INDEX orders_customer_id_order_date_desc_idx
      ON orders(customer_id, order_date DESC);

   - Supports lookup by ``customer_id``.
   - Preserves useful order within each customer.
   - Helps join-heavy "latest order" patterns.
   - Pairs nicely with the ``LATERAL`` example above.


Designing Indexes for Joins
----------------------------------------------------

.. dropdown:: Index Design Guidelines
   :class-container: sd-border-secondary
   :open:

   - Index foreign-key / join columns on large tables.
   - Match data types and collations (implicit casts can block good index
     usage).
   - Use composite indexes for join + filter patterns.
   - Avoid functions/casts on join keys.
   - Do not over-index everything.
   - PostgreSQL does **not** automatically index referencing foreign-key
     columns.


Practical PostgreSQL Tuning Tips
====================================================

.. dropdown:: Tuning Checklist
   :class-container: sd-border-secondary
   :open:

   - Use ``EXPLAIN (ANALYZE, BUFFERS)``.
   - Keep stats fresh with ``ANALYZE``.
   - Use ``VACUUM`` / autovacuum to control bloat.
   - Adjust ``work_mem`` carefully.
   - Consider ``CREATE STATISTICS`` for correlated columns.

   **Tuning without measurement is just storytelling.** If you are forcing
   planner settings before fixing statistics, you are often treating the
   symptom rather than the disease.


Recap / Takeaways
====================================================

- Join = rows combined under a predicate.
- Outer joins preserve unmatched rows with ``NULL``.
- PostgreSQL can use nested loop, hash, or merge join.
- Big O gives intuition; I/O and memory make it real.
- Indexes and B+ tree ideas explain many fast plans.

A simple summary:

1. Get the join semantics right.
2. Inspect the plan.
3. Design indexes around actual workload patterns.
