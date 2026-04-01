====================================================
Exercises
====================================================

This page contains exercises for Lecture 8. These exercises are designed to
reinforce your understanding of SQL JOINs (``CROSS``, ``INNER``, ``LEFT``,
``RIGHT``, ``FULL``, self-join, semi/anti), ``ON`` vs ``WHERE`` behavior,
``EXPLAIN`` output interpretation, Big O reasoning, and index design for
join-heavy workloads.

All exercises use the sample ``customers`` / ``orders`` schema from the
lecture unless stated otherwise.


.. dropdown:: Exercise 1 -- Cartesian Product Row Count
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build intuition for Cartesian products and ``CROSS JOIN`` by predicting
    row counts before running any SQL.

    **Specification**

    You have:

    - ``students``: 5 rows
    - ``projects``: 8 rows

    **Questions**

    1. How many rows does ``students CROSS JOIN projects`` return?
    2. Write SQL to generate every ``(student, project)`` pairing.
    3. If a third table ``semesters`` has 3 rows, how many rows does
       ``students CROSS JOIN projects CROSS JOIN semesters`` produce?

    .. dropdown:: Solution
       :class-container: sd-border-success

       1. Row count: ``5 x 8 = 40``

       2. SQL:

          .. code-block:: sql

             SELECT s.student_id, p.project_id
             FROM students s
             CROSS JOIN projects p;

          This is a legitimate use of ``CROSS JOIN``.

       3. ``5 x 8 x 3 = 120`` rows.


.. dropdown:: Exercise 2 -- Choosing the Right Join
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Choose the best join type or SQL pattern for each task.

    **Tasks**

    1. Customers that placed at least one order.
    2. All customers, plus any order IDs.
    3. Customers with no orders.
    4. All orders, plus customer info if available.
    5. Every customer-product combination (for a recommendation grid).

    .. dropdown:: Solution
       :class-container: sd-border-success

       1. ``INNER JOIN`` or ``EXISTS`` (semi join).
       2. ``LEFT JOIN``.
       3. ``NOT EXISTS`` or ``LEFT JOIN ... WHERE o.order_id IS NULL`` (anti join).
       4. ``RIGHT JOIN`` or (preferred) rewrite as ``LEFT JOIN`` with orders on the left.
       5. ``CROSS JOIN``.


.. dropdown:: Exercise 3 -- JOIN Result Predictor
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Predict the exact output of join queries before running them.

    **Setup**

    Use the sample ``customers`` and ``orders`` tables from the lecture:

    .. code-block:: sql

       -- customers: (1, Ada, Berlin), (2, Bruno, Lisbon),
       --            (3, Chandra, Delhi), (4, Diana, Oslo)
       -- orders:    (101, 1, 2026-03-01, 120),
       --            (102, 1, 2026-03-05, 75),
       --            (103, 3, 2026-03-07, 200)

    **Predict the output of each query before running it:**

    .. code-block:: sql

       -- A
       SELECT c.customer_name, o.order_id
       FROM customers c
       JOIN orders o ON c.customer_id = o.customer_id;

       -- B
       SELECT c.customer_name, o.order_id
       FROM customers c
       LEFT JOIN orders o ON c.customer_id = o.customer_id;

       -- C
       SELECT c.customer_name, o.order_id
       FROM customers c
       LEFT JOIN orders o
         ON c.customer_id = o.customer_id
        AND o.total > 100;

       -- D
       SELECT c.customer_name, o.order_id
       FROM customers c
       LEFT JOIN orders o
         ON c.customer_id = o.customer_id
       WHERE o.total > 100;

    .. dropdown:: Solution
       :class-container: sd-border-success

       **A (INNER JOIN):** 3 rows -- (Ada, 101), (Ada, 102), (Chandra, 103).
       Bruno and Diana have no orders, so they do not appear.

       **B (LEFT JOIN):** 5 rows -- (Ada, 101), (Ada, 102), (Bruno, NULL),
       (Chandra, 103), (Diana, NULL).

       **C (LEFT JOIN with filter in ON):** 5 rows -- (Ada, 101),
       (Ada, NULL for order 102 since 75 <= 100), (Bruno, NULL),
       (Chandra, 103), (Diana, NULL). The ``ON`` filter excludes
       non-matching right rows but still preserves every left row.

       **D (LEFT JOIN with filter in WHERE):** 2 rows -- (Ada, 101),
       (Chandra, 103). The ``WHERE`` filter eliminates all rows where
       ``o.total`` is NULL or <= 100, effectively turning the LEFT JOIN
       into an INNER JOIN.


.. dropdown:: Exercise 4 -- Match Join Algorithm to Scenario
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Match each scenario to the most likely best join algorithm.

    **Scenarios**

    A. 20 customers joined to 100M orders, with an index on
       ``orders.customer_id``.
    B. 10M customers joined to 100M orders on equality, unsorted, enough
       memory.
    C. Two large tables already sorted by join key.

    .. dropdown:: Solution
       :class-container: sd-border-success

       - **A -> Nested loop** with index lookups (small outer side + indexed
         inner side).
       - **B -> Hash join** (equality predicate, large tables, sufficient
         memory).
       - **C -> Merge join** (pre-sorted input avoids sort cost).

       Caveat: PostgreSQL may choose differently if cost estimates differ.


.. dropdown:: Exercise 5 -- Index Design for a Join Query (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Design optimal indexes for a given join query.

    **Query**

    .. code-block:: sql

       SELECT c.customer_name, o.order_date, o.total
       FROM customers c
       JOIN orders o
         ON o.customer_id = c.customer_id
       WHERE c.city = 'Berlin'
         AND o.order_date >= DATE '2026-03-01';

    **Questions**

    1. Which indexes would you add?
    2. Which index would you **not** duplicate?
    3. Think in terms of: (a) filter on ``customers``, (b) join into
       ``orders``, (c) range condition on ``orders.order_date``.

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: sql

          CREATE INDEX customers_city_idx
          ON customers(city);

          CREATE INDEX orders_customer_id_order_date_idx
          ON orders(customer_id, order_date)
          INCLUDE (total);

       - Do **not** duplicate the primary key index on
         ``customers(customer_id)`` -- it already exists.
       - Optional refinement: ``(city, customer_id)`` if this access pattern
         is frequent.
       - Primary keys are indexed automatically.
       - Foreign keys are **not automatically indexed** on the referencing
         side in PostgreSQL.
       - ``INCLUDE (total)`` can help index-only scan patterns.


.. dropdown:: Exercise 6 -- Self Join and Hierarchy (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice self-joins for hierarchical data.

    **Setup**

    .. code-block:: sql

       CREATE TABLE employees (
           employee_id   INTEGER PRIMARY KEY,
           employee_name VARCHAR(100) NOT NULL,
           manager_id    INTEGER REFERENCES employees(employee_id)
       );

       INSERT INTO employees VALUES
           (1, 'Alice',   NULL),
           (2, 'Bob',     1),
           (3, 'Charlie', 1),
           (4, 'Diana',   2),
           (5, 'Eve',     2);

    **Tasks**

    1. Write a query to list every employee with their manager's name
       (show ``NULL`` for the top-level manager).
    2. List employees who are managers (i.e., someone reports to them).
    3. Count how many direct reports each manager has.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1. Employee-Manager listing:**

       .. code-block:: sql

          SELECT e.employee_name,
                 m.employee_name AS manager_name
          FROM employees e
          LEFT JOIN employees m
            ON e.manager_id = m.employee_id;

       **2. Employees who are managers (semi join):**

       .. code-block:: sql

          SELECT DISTINCT m.employee_name
          FROM employees e
          JOIN employees m
            ON e.manager_id = m.employee_id;

       Or using ``EXISTS``:

       .. code-block:: sql

          SELECT e.employee_name
          FROM employees e
          WHERE EXISTS (
            SELECT 1
            FROM employees sub
            WHERE sub.manager_id = e.employee_id
          );

       **3. Direct report count:**

       .. code-block:: sql

          SELECT m.employee_name,
                 COUNT(e.employee_id) AS direct_reports
          FROM employees m
          LEFT JOIN employees e
            ON e.manager_id = m.employee_id
          GROUP BY m.employee_id, m.employee_name
          HAVING COUNT(e.employee_id) > 0
          ORDER BY direct_reports DESC;

       Result: Alice has 2 reports (Bob, Charlie), Bob has 2 reports
       (Diana, Eve).
