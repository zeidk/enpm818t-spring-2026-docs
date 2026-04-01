====================================================
Lecture Material
====================================================

.. raw:: latex

   \setcounter{figure}{0}


This page covers SQL topics required for **GP2** that are not part of the
main L8 lecture on JOINs. Specifically: ``SELECT`` fundamentals, aggregate
functions, ``GROUP BY`` / ``HAVING``, and subqueries (non-correlated and
correlated).

All examples use PostgreSQL syntax and the same ``customers`` / ``orders``
schema from the main lecture unless stated otherwise.


SELECT Fundamentals
====================================================

``SELECT`` retrieves rows from one or more tables. The logical evaluation
order of a ``SELECT`` statement is:

.. list-table::
   :widths: 10 25 65
   :header-rows: 1
   :class: compact-table

   * - **Step**
     - **Clause**
     - **Purpose**
   * - 1
     - ``FROM`` / ``JOIN``
     - Identify source tables and join them
   * - 2
     - ``WHERE``
     - Filter individual rows before grouping
   * - 3
     - ``GROUP BY``
     - Collapse rows into groups
   * - 4
     - ``HAVING``
     - Filter groups after aggregation
   * - 5
     - ``SELECT``
     - Choose columns and compute expressions
   * - 6
     - ``DISTINCT``
     - Remove duplicate rows
   * - 7
     - ``ORDER BY``
     - Sort the result set
   * - 8
     - ``LIMIT`` / ``OFFSET``
     - Restrict output to a page of rows

.. admonition:: Key Insight
   :class: tip

   ``WHERE`` filters **rows** before grouping. ``HAVING`` filters **groups**
   after aggregation. Mixing them up is a common source of bugs.


WHERE -- Filtering Rows
----------------------------------------------------

.. dropdown:: WHERE Clause
   :class-container: sd-border-secondary
   :open:

   ``WHERE`` removes rows that do not satisfy a boolean condition. It is
   evaluated **before** ``GROUP BY`` and aggregate functions.

   .. code-block:: sql

      -- Customers in Berlin
      SELECT customer_id, customer_name, city
      FROM customers
      WHERE city = 'Berlin';

      -- Orders above 100 placed in March 2026
      SELECT order_id, customer_id, total
      FROM orders
      WHERE total > 100
        AND order_date >= DATE '2026-03-01'
        AND order_date < DATE '2026-04-01';

   **Operators**: ``=``, ``<>``, ``<``, ``>``, ``<=``, ``>=``, ``AND``,
   ``OR``, ``NOT``, ``IN``, ``BETWEEN``, ``LIKE``, ``IS NULL``,
   ``IS NOT NULL``.


.. dropdown:: Common WHERE Patterns
   :class-container: sd-border-secondary

   .. code-block:: sql

      -- IN: match any value in a list
      SELECT * FROM customers
      WHERE city IN ('Berlin', 'Delhi', 'Oslo');

      -- BETWEEN: inclusive range
      SELECT * FROM orders
      WHERE order_date BETWEEN '2026-03-01' AND '2026-03-31';

      -- LIKE: pattern matching (% = any chars, _ = one char)
      SELECT * FROM customers
      WHERE customer_name LIKE 'A%';

      -- IS NULL: check for missing values
      SELECT * FROM orders
      WHERE customer_id IS NULL;


ORDER BY -- Sorting Results
----------------------------------------------------

.. dropdown:: ORDER BY Clause
   :class-container: sd-border-secondary
   :open:

   ``ORDER BY`` sorts the result set. Without it, PostgreSQL makes **no
   guarantee** about row order.

   .. code-block:: sql

      -- Sort by total descending
      SELECT order_id, customer_id, total
      FROM orders
      ORDER BY total DESC;

      -- Multi-column sort: city ascending, then name descending
      SELECT customer_id, customer_name, city
      FROM customers
      ORDER BY city ASC, customer_name DESC;

   ``ASC`` (ascending) is the default. ``NULLS FIRST`` / ``NULLS LAST``
   controls where ``NULL`` values appear.


LIMIT and OFFSET -- Pagination
----------------------------------------------------

.. dropdown:: LIMIT and OFFSET
   :class-container: sd-border-secondary
   :open:

   ``LIMIT`` restricts the number of rows returned. ``OFFSET`` skips a
   number of rows before starting to return. Together they implement
   pagination.

   .. code-block:: sql

      -- First page: 10 rows
      SELECT order_id, order_date, total
      FROM orders
      ORDER BY order_date DESC
      LIMIT 10 OFFSET 0;

      -- Second page: next 10 rows
      SELECT order_id, order_date, total
      FROM orders
      ORDER BY order_date DESC
      LIMIT 10 OFFSET 10;

   .. warning::

      Always use ``ORDER BY`` with ``LIMIT`` / ``OFFSET``. Without a
      deterministic sort, pages may contain duplicate or missing rows
      across requests.

   For large datasets, **keyset pagination** (``WHERE id > last_seen_id``)
   is more efficient than ``OFFSET``, which must scan and discard skipped
   rows.


Aggregate Functions
====================================================

Aggregate functions compute a single value from a set of rows. They are
the building blocks of summary reports, dashboards, and analytical queries.


.. dropdown:: Core Aggregate Functions
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1
      :class: compact-table

      * - **Function**
        - **Purpose**
        - **Example**
      * - ``COUNT(*)``
        - Count all rows (including NULLs)
        - ``SELECT COUNT(*) FROM orders;``
      * - ``COUNT(col)``
        - Count non-NULL values in a column
        - ``SELECT COUNT(customer_id) FROM orders;``
      * - ``COUNT(DISTINCT col)``
        - Count distinct non-NULL values
        - ``SELECT COUNT(DISTINCT customer_id) FROM orders;``
      * - ``SUM(col)``
        - Sum of all non-NULL values
        - ``SELECT SUM(total) FROM orders;``
      * - ``AVG(col)``
        - Average of all non-NULL values
        - ``SELECT AVG(total) FROM orders;``
      * - ``MIN(col)``
        - Smallest value
        - ``SELECT MIN(order_date) FROM orders;``
      * - ``MAX(col)``
        - Largest value
        - ``SELECT MAX(total) FROM orders;``

   Aggregates ignore ``NULL`` values (except ``COUNT(*)``). If all input
   values are ``NULL``, the aggregate returns ``NULL`` (except ``COUNT``,
   which returns ``0``).


.. dropdown:: Aggregates Without GROUP BY
   :class-container: sd-border-secondary

   When used without ``GROUP BY``, aggregates collapse the entire table into
   a single summary row.

   .. code-block:: sql

      -- Total revenue and number of orders
      SELECT COUNT(*) AS num_orders,
             SUM(total) AS total_revenue,
             AVG(total) AS avg_order_value,
             MIN(total) AS smallest_order,
             MAX(total) AS largest_order
      FROM orders;

   .. rubric:: Result

   .. list-table::
      :widths: 18 20 22 20 20
      :header-rows: 1
      :class: compact-table

      * - ``num_orders``
        - ``total_revenue``
        - ``avg_order_value``
        - ``smallest_order``
        - ``largest_order``
      * - 3
        - 395
        - 131.67
        - 75
        - 200


GROUP BY
====================================================

``GROUP BY`` partitions rows into groups based on one or more columns. Each
group is then collapsed into a single summary row by the aggregate functions
in the ``SELECT`` list.


.. dropdown:: GROUP BY Basics
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Order count and total spent per customer
      SELECT customer_id,
             COUNT(*) AS num_orders,
             SUM(total) AS total_spent
      FROM orders
      GROUP BY customer_id;

   .. rubric:: Result

   .. list-table::
      :widths: 25 25 25
      :header-rows: 1
      :class: compact-table

      * - ``customer_id``
        - ``num_orders``
        - ``total_spent``
      * - 1
        - 2
        - 195
      * - 3
        - 1
        - 200

   Every column in the ``SELECT`` list must either appear in ``GROUP BY``
   or be inside an aggregate function. PostgreSQL raises an error otherwise.


.. dropdown:: GROUP BY with JOIN
   :class-container: sd-border-secondary
   :open:

   ``GROUP BY`` is frequently combined with ``JOIN`` to produce reports that
   span multiple tables.

   .. code-block:: sql

      -- Order count per customer, showing customer name
      SELECT c.customer_name,
             COUNT(o.order_id) AS num_orders,
             COALESCE(SUM(o.total), 0) AS total_spent
      FROM customers c
      LEFT JOIN orders o
        ON o.customer_id = c.customer_id
      GROUP BY c.customer_id, c.customer_name
      ORDER BY total_spent DESC;

   .. rubric:: Result

   .. list-table::
      :widths: 25 25 25
      :header-rows: 1
      :class: compact-table

      * - ``customer_name``
        - ``num_orders``
        - ``total_spent``
      * - Chandra
        - 1
        - 200
      * - Ada
        - 2
        - 195
      * - Bruno
        - 0
        - 0
      * - Diana
        - 0
        - 0

   Note the ``LEFT JOIN`` to include customers with no orders, and
   ``COALESCE`` to turn ``NULL`` sums into ``0``.


.. dropdown:: Multi-Column GROUP BY
   :class-container: sd-border-secondary

   You can group by multiple columns to produce finer breakdowns.

   .. code-block:: sql

      -- Incident count by severity and status
      SELECT severity, status,
             COUNT(*) AS incident_count
      FROM incident
      GROUP BY severity, status
      ORDER BY severity, status;

   Each unique combination of ``(severity, status)`` becomes its own group.


HAVING -- Filtering Groups
====================================================

``HAVING`` filters groups **after** aggregation, in contrast to ``WHERE``,
which filters rows **before** grouping.

.. dropdown:: HAVING Clause
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Customers who placed more than 1 order
      SELECT customer_id,
             COUNT(*) AS num_orders
      FROM orders
      GROUP BY customer_id
      HAVING COUNT(*) > 1;

   .. rubric:: Result

   .. list-table::
      :widths: 30 30
      :header-rows: 1
      :class: compact-table

      * - ``customer_id``
        - ``num_orders``
      * - 1
        - 2


.. dropdown:: WHERE vs HAVING
   :class-container: sd-border-secondary
   :open:

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1
      :class: compact-table

      * - **Clause**
        - **Filters**
        - **Evaluated**
      * - ``WHERE``
        - Individual rows
        - Before ``GROUP BY``
      * - ``HAVING``
        - Aggregated groups
        - After ``GROUP BY``

   .. code-block:: sql

      -- Combine WHERE and HAVING:
      -- Among orders from March 2026, find customers
      -- whose total spending exceeds 100
      SELECT customer_id,
             SUM(total) AS march_total
      FROM orders
      WHERE order_date >= DATE '2026-03-01'
        AND order_date < DATE '2026-04-01'
      GROUP BY customer_id
      HAVING SUM(total) > 100;

   ``WHERE`` filters rows first (only March orders), then ``GROUP BY``
   groups them by customer, then ``HAVING`` keeps only groups with total
   spending above 100.


.. dropdown:: GP2-Style Aggregate Queries
   :class-container: sd-border-secondary

   These examples mirror the kinds of queries expected in GP2.

   **Scenario 1 -- Traffic Management:**

   .. code-block:: sql

      -- Count sensors per intersection; find those with fewer than 2
      SELECT i.intersection_id, i.intersection_name,
             COUNT(s.sensor_id) AS sensor_count
      FROM intersection i
      LEFT JOIN sensor s
        ON s.intersection_id = i.intersection_id
      GROUP BY i.intersection_id, i.intersection_name
      HAVING COUNT(s.sensor_id) < 2
      ORDER BY sensor_count;

   .. code-block:: sql

      -- Average incident resolution time by severity level
      SELECT severity,
             COUNT(*) AS incident_count,
             AVG(EXTRACT(EPOCH FROM (resolved_at - reported_at)) / 3600)
                AS avg_resolution_hours
      FROM incident
      WHERE resolved_at IS NOT NULL
      GROUP BY severity
      ORDER BY avg_resolution_hours DESC;

   **Scenario 2 -- Healthcare:**

   .. code-block:: sql

      -- Appointment counts and no-show rate by provider
      SELECT p.first_name || ' ' || p.last_name AS provider_name,
             COUNT(*) AS total_appointments,
             COUNT(*) FILTER (WHERE a.status = 'no_show') AS no_shows,
             ROUND(
               COUNT(*) FILTER (WHERE a.status = 'no_show')::NUMERIC
               / NULLIF(COUNT(*), 0) * 100, 1
             ) AS no_show_pct
      FROM provider p
      JOIN appointment a
        ON a.provider_id = p.provider_id
      GROUP BY p.provider_id, p.first_name, p.last_name
      ORDER BY no_show_pct DESC;

   .. code-block:: sql

      -- Patients with 5+ active prescriptions (polypharmacy risk)
      SELECT pt.patient_id, pt.first_name, pt.last_name,
             COUNT(rx.prescription_id) AS active_rx_count
      FROM patient pt
      JOIN prescription rx
        ON rx.patient_id = pt.patient_id
      WHERE rx.status = 'active'
      GROUP BY pt.patient_id, pt.first_name, pt.last_name
      HAVING COUNT(rx.prescription_id) >= 5
      ORDER BY active_rx_count DESC;


Subqueries
====================================================

A **subquery** is a ``SELECT`` statement nested inside another SQL statement.
Subqueries can appear in ``WHERE``, ``FROM``, ``SELECT``, or ``HAVING``
clauses.


Non-Correlated Subqueries
----------------------------------------------------

A non-correlated subquery runs **once**, independently of the outer query.
Its result is then used by the outer query.


.. dropdown:: Single-Row Subqueries
   :class-container: sd-border-secondary
   :open:

   A single-row subquery returns exactly **one row and one column**. It can
   be used with comparison operators (``=``, ``<``, ``>``, etc.).

   .. code-block:: sql

      -- Order with the highest total
      SELECT order_id, customer_id, total
      FROM orders
      WHERE total = (
          SELECT MAX(total)
          FROM orders
      );

   .. code-block:: sql

      -- Employees hired on the earliest date (most senior)
      SELECT employee_id, first_name, last_name, hire_date
      FROM employees
      WHERE hire_date = (
          SELECT MIN(hire_date)
          FROM employees
      );

   .. warning::

      If a single-row subquery returns more than one row, PostgreSQL raises
      ``ERROR: more than one row returned by a subquery used as an expression``.
      Test your subquery independently first.


.. dropdown:: Multi-Row Subqueries (IN, ANY, ALL)
   :class-container: sd-border-secondary
   :open:

   Multi-row subqueries return multiple rows. Use ``IN``, ``ANY``, or
   ``ALL`` to compare against the result set.

   **IN -- match any value in the result:**

   .. code-block:: sql

      -- Orders placed by customers in Berlin
      SELECT order_id, customer_id, total
      FROM orders
      WHERE customer_id IN (
          SELECT customer_id
          FROM customers
          WHERE city = 'Berlin'
      );

   **ANY -- true if comparison holds for at least one row:**

   .. code-block:: sql

      -- Employees earning more than the lowest salary in dept 10
      SELECT employee_id, first_name, salary
      FROM employees
      WHERE salary > ANY (
          SELECT salary
          FROM employees
          WHERE department_id = 10
      );

   **ALL -- true if comparison holds for every row:**

   .. code-block:: sql

      -- Employees earning more than everyone in dept 5
      SELECT employee_id, first_name, salary
      FROM employees
      WHERE salary > ALL (
          SELECT salary
          FROM employees
          WHERE department_id = 5
      );


.. dropdown:: Subqueries in FROM (Derived Tables)
   :class-container: sd-border-secondary

   A subquery in the ``FROM`` clause creates a temporary result set (derived
   table) that the outer query can reference.

   .. code-block:: sql

      -- Department with the highest average salary
      SELECT department_id, avg_salary
      FROM (
          SELECT department_id,
                 AVG(salary) AS avg_salary
          FROM employees
          GROUP BY department_id
      ) AS dept_avg
      ORDER BY avg_salary DESC
      LIMIT 1;

   The subquery must have an alias (``AS dept_avg``).


.. dropdown:: Subqueries in SELECT (Scalar Subqueries)
   :class-container: sd-border-secondary

   A scalar subquery in the ``SELECT`` list computes a value per output row.

   .. code-block:: sql

      -- Each customer with their total order count
      SELECT c.customer_name,
             (SELECT COUNT(*)
              FROM orders o
              WHERE o.customer_id = c.customer_id
             ) AS order_count
      FROM customers c;

   This is technically a correlated scalar subquery (it references ``c``
   from the outer query). It is simple enough to illustrate the pattern,
   but for large tables, a ``LEFT JOIN`` with ``GROUP BY`` is usually
   more efficient.


Correlated Subqueries
----------------------------------------------------

A correlated subquery references columns from the outer query. It is
re-evaluated **once for each row** of the outer query.


.. dropdown:: Correlated Subquery Basics
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Employees earning above their department's average
      SELECT e.employee_id, e.first_name, e.salary,
             e.department_id
      FROM employees e
      WHERE e.salary > (
          SELECT AVG(salary)
          FROM employees
          WHERE department_id = e.department_id
      );

   The subquery calculates the average salary for the department of the
   **current outer row** (``e.department_id``). It runs once per employee.


.. dropdown:: EXISTS and NOT EXISTS (Revisited)
   :class-container: sd-border-secondary
   :open:

   ``EXISTS`` is a correlated subquery pattern covered in the main lecture.
   It is repeated here because it is essential for GP2 queries.

   .. code-block:: sql

      -- Customers who have placed at least one order
      SELECT c.customer_id, c.customer_name
      FROM customers c
      WHERE EXISTS (
          SELECT 1
          FROM orders o
          WHERE o.customer_id = c.customer_id
      );

      -- Crews that have never been assigned a critical task
      SELECT mc.crew_id, mc.crew_name
      FROM maintenance_crew mc
      WHERE NOT EXISTS (
          SELECT 1
          FROM maintenance_task mt
          WHERE mt.crew_id = mc.crew_id
            AND mt.priority = 'critical'
      );

   ``EXISTS`` stops scanning as soon as one match is found, making it
   efficient for membership checks. Prefer ``NOT EXISTS`` over ``NOT IN``
   when the subquery column may contain ``NULL`` values.


.. dropdown:: Correlated Subquery Performance
   :class-container: sd-border-secondary

   .. warning::

      Correlated subqueries execute the inner query once per outer row. For
      large outer tables, this can be expensive.

   **Best practices:**

   - Index columns used in the subquery's ``WHERE`` clause.
   - Consider rewriting as a ``JOIN`` if the optimizer does not flatten the
     subquery automatically.
   - Use ``EXPLAIN (ANALYZE, BUFFERS)`` to verify the plan.
   - Sometimes ``EXISTS`` is more efficient than ``IN``; test both.


.. dropdown:: GP2-Style Subquery Examples
   :class-container: sd-border-secondary

   **Scenario 1 -- Intersections with more incidents than average:**

   .. code-block:: sql

      -- Find intersections with more incidents than the citywide average
      SELECT i.intersection_id, i.intersection_name,
             COUNT(inc.incident_id) AS incident_count
      FROM intersection i
      JOIN incident inc
        ON inc.intersection_id = i.intersection_id
      GROUP BY i.intersection_id, i.intersection_name
      HAVING COUNT(inc.incident_id) > (
          SELECT AVG(cnt)
          FROM (
              SELECT COUNT(*) AS cnt
              FROM incident
              GROUP BY intersection_id
          ) AS avg_per_intersection
      )
      ORDER BY incident_count DESC;

   **Scenario 2 -- Patients whose most recent appointment was a no-show:**

   .. code-block:: sql

      SELECT pt.patient_id, pt.first_name, pt.last_name
      FROM patient pt
      WHERE (
          SELECT a.status
          FROM appointment a
          WHERE a.patient_id = pt.patient_id
          ORDER BY a.appointment_date DESC
          LIMIT 1
      ) = 'no_show';


Putting It All Together
====================================================

A complete analytical query typically combines most of the concepts on this
page. Here is a realistic example that uses ``JOIN``, ``WHERE``,
``GROUP BY``, ``HAVING``, ``ORDER BY``, and ``LIMIT``.

.. dropdown:: Full Example
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      -- Top 5 intersections by incident count in the last 30 days,
      -- showing sensor coverage and average resolution time
      SELECT i.intersection_name,
             COUNT(DISTINCT inc.incident_id) AS recent_incidents,
             COUNT(DISTINCT s.sensor_id)     AS sensor_count,
             ROUND(
               AVG(EXTRACT(EPOCH FROM (inc.resolved_at - inc.reported_at))
                   / 3600)::NUMERIC, 1
             ) AS avg_resolution_hours
      FROM intersection i
      JOIN incident inc
        ON inc.intersection_id = i.intersection_id
      LEFT JOIN sensor s
        ON s.intersection_id = i.intersection_id
      WHERE inc.reported_at >= CURRENT_DATE - INTERVAL '30 days'
      GROUP BY i.intersection_id, i.intersection_name
      HAVING COUNT(DISTINCT inc.incident_id) >= 2
      ORDER BY recent_incidents DESC
      LIMIT 5;

   **Clause-by-clause breakdown:**

   1. ``FROM`` / ``JOIN``: start with intersections, join incidents and
      sensors.
   2. ``WHERE``: keep only incidents from the last 30 days (row filter).
   3. ``GROUP BY``: one row per intersection.
   4. ``HAVING``: keep only intersections with 2+ recent incidents (group
      filter).
   5. ``SELECT``: compute counts and averages.
   6. ``ORDER BY``: sort by incident count descending.
   7. ``LIMIT``: return the top 5.
