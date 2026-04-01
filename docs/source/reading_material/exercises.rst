====================================================
Exercises
====================================================

These exercises reinforce the topics from the
:doc:`select_aggregates_subqueries` reading material: ``SELECT``
fundamentals, aggregate functions, ``GROUP BY`` / ``HAVING``, and
subqueries. They progress from basic to GP2-level complexity.

All exercises use the following schema unless stated otherwise. Run the
setup block first.

.. dropdown:: Schema Setup
   :class-container: sd-border-secondary
   :open:

   .. code-block:: sql

      DROP TABLE IF EXISTS order_items, orders, products, customers CASCADE;

      CREATE TABLE customers (
          customer_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          customer_name VARCHAR(100) NOT NULL,
          city          VARCHAR(50) NOT NULL
      );

      CREATE TABLE products (
          product_id   INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          product_name VARCHAR(100) NOT NULL,
          category     VARCHAR(50) NOT NULL,
          price        NUMERIC(10,2) NOT NULL
      );

      CREATE TABLE orders (
          order_id    INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          customer_id INTEGER NOT NULL REFERENCES customers(customer_id),
          order_date  DATE NOT NULL,
          status      VARCHAR(20) NOT NULL DEFAULT 'completed'
      );

      CREATE TABLE order_items (
          order_item_id INTEGER GENERATED ALWAYS AS IDENTITY PRIMARY KEY,
          order_id      INTEGER NOT NULL REFERENCES orders(order_id),
          product_id    INTEGER NOT NULL REFERENCES products(product_id),
          qty           INTEGER NOT NULL CHECK (qty > 0),
          unit_price    NUMERIC(10,2) NOT NULL
      );

      INSERT INTO customers (customer_name, city) VALUES
          ('Ada',     'Berlin'),
          ('Bruno',   'Lisbon'),
          ('Chandra', 'Delhi'),
          ('Diana',   'Oslo'),
          ('Elena',   'Berlin');

      INSERT INTO products (product_name, category, price) VALUES
          ('Laptop',    'Electronics', 999.99),
          ('Mouse',     'Electronics',  29.99),
          ('Notebook',  'Stationery',    4.50),
          ('Pen',       'Stationery',    1.25),
          ('Backpack',  'Accessories',  59.99);

      INSERT INTO orders (customer_id, order_date, status) VALUES
          (1, '2026-03-01', 'completed'),
          (1, '2026-03-05', 'completed'),
          (3, '2026-03-07', 'completed'),
          (2, '2026-03-10', 'cancelled'),
          (1, '2026-03-15', 'completed'),
          (3, '2026-03-20', 'completed'),
          (5, '2026-03-22', 'completed');

      INSERT INTO order_items (order_id, product_id, qty, unit_price) VALUES
          (1, 1, 1, 999.99),
          (1, 2, 2,  29.99),
          (2, 3, 5,   4.50),
          (2, 4, 10,  1.25),
          (3, 1, 1, 999.99),
          (3, 5, 1,  59.99),
          (4, 2, 1,  29.99),
          (5, 2, 3,  29.99),
          (5, 3, 2,   4.50),
          (6, 4, 20,  1.25),
          (6, 5, 2,  59.99),
          (7, 1, 1, 999.99),
          (7, 3, 3,   4.50);


----


.. dropdown:: Exercise 1 -- SELECT and WHERE Basics
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Practice filtering and sorting.

    **Tasks:**

    1. List all customers in Berlin.
    2. List all completed orders placed after March 10, sorted by date
       descending.
    3. Find all products in the 'Electronics' category priced under 100.
    4. List all orders that are **not** completed, showing order_id,
       customer_id, and status.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT customer_id, customer_name, city
          FROM customers
          WHERE city = 'Berlin';

       **2.**

       .. code-block:: sql

          SELECT order_id, customer_id, order_date, status
          FROM orders
          WHERE status = 'completed'
            AND order_date > DATE '2026-03-10'
          ORDER BY order_date DESC;

       **3.**

       .. code-block:: sql

          SELECT product_id, product_name, price
          FROM products
          WHERE category = 'Electronics'
            AND price < 100;

       **4.**

       .. code-block:: sql

          SELECT order_id, customer_id, status
          FROM orders
          WHERE status <> 'completed';


.. dropdown:: Exercise 2 -- LIMIT, OFFSET, and Pagination
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Practice pagination patterns.

    **Tasks:**

    1. Return the 3 most recent orders (by date).
    2. Return orders 4 through 6 (page 2, page size 3), sorted by date
       descending.
    3. Explain in one sentence why ``ORDER BY`` is required when using
       ``LIMIT`` / ``OFFSET``.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT order_id, customer_id, order_date
          FROM orders
          ORDER BY order_date DESC
          LIMIT 3;

       **2.**

       .. code-block:: sql

          SELECT order_id, customer_id, order_date
          FROM orders
          ORDER BY order_date DESC
          LIMIT 3 OFFSET 3;

       **3.** Without a deterministic sort, PostgreSQL may return rows in
       any order, so pages could contain duplicates or miss rows between
       requests.


.. dropdown:: Exercise 3 -- Basic Aggregates
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Use aggregate functions without ``GROUP BY``.

    **Tasks:**

    1. Count the total number of orders.
    2. Count the number of **distinct** customers who have placed at least
       one order.
    3. Find the total revenue across all order items (``SUM(qty * unit_price)``).
    4. Find the cheapest and most expensive product.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT COUNT(*) AS total_orders
          FROM orders;

       **2.**

       .. code-block:: sql

          SELECT COUNT(DISTINCT customer_id) AS unique_customers
          FROM orders;

       **3.**

       .. code-block:: sql

          SELECT SUM(qty * unit_price) AS total_revenue
          FROM order_items;

       **4.**

       .. code-block:: sql

          SELECT MIN(price) AS cheapest,
                 MAX(price) AS most_expensive
          FROM products;


.. dropdown:: Exercise 4 -- GROUP BY
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Practice grouping rows and computing per-group summaries.

    **Tasks:**

    1. Count orders per customer. Show ``customer_id`` and ``num_orders``.
    2. Calculate total revenue per order (sum of ``qty * unit_price`` for
       each ``order_id``).
    3. Count products per category and show the average price per category.
    4. For each city, show how many customers live there and how many
       orders they placed in total. (Hint: join ``customers`` and ``orders``.)

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT customer_id,
                 COUNT(*) AS num_orders
          FROM orders
          GROUP BY customer_id
          ORDER BY num_orders DESC;

       **2.**

       .. code-block:: sql

          SELECT order_id,
                 SUM(qty * unit_price) AS order_total
          FROM order_items
          GROUP BY order_id
          ORDER BY order_total DESC;

       **3.**

       .. code-block:: sql

          SELECT category,
                 COUNT(*) AS num_products,
                 ROUND(AVG(price), 2) AS avg_price
          FROM products
          GROUP BY category
          ORDER BY avg_price DESC;

       **4.**

       .. code-block:: sql

          SELECT c.city,
                 COUNT(DISTINCT c.customer_id) AS num_customers,
                 COUNT(o.order_id) AS total_orders
          FROM customers c
          LEFT JOIN orders o
            ON o.customer_id = c.customer_id
          GROUP BY c.city
          ORDER BY total_orders DESC;


.. dropdown:: Exercise 5 -- HAVING
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Filter groups after aggregation.

    **Tasks:**

    1. Find customers who placed more than 2 orders (show ``customer_id``
       and count).
    2. Find product categories where the average price is above 30.
    3. Find orders whose total (sum of ``qty * unit_price``) exceeds 100.
    4. Combine ``WHERE`` and ``HAVING``: among **completed** orders only,
       find customers whose total spending exceeds 500.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT customer_id,
                 COUNT(*) AS num_orders
          FROM orders
          GROUP BY customer_id
          HAVING COUNT(*) > 2;

       **2.**

       .. code-block:: sql

          SELECT category,
                 ROUND(AVG(price), 2) AS avg_price
          FROM products
          GROUP BY category
          HAVING AVG(price) > 30;

       **3.**

       .. code-block:: sql

          SELECT order_id,
                 SUM(qty * unit_price) AS order_total
          FROM order_items
          GROUP BY order_id
          HAVING SUM(qty * unit_price) > 100
          ORDER BY order_total DESC;

       **4.**

       .. code-block:: sql

          SELECT o.customer_id,
                 SUM(oi.qty * oi.unit_price) AS total_spent
          FROM orders o
          JOIN order_items oi ON oi.order_id = o.order_id
          WHERE o.status = 'completed'
          GROUP BY o.customer_id
          HAVING SUM(oi.qty * oi.unit_price) > 500
          ORDER BY total_spent DESC;


.. dropdown:: Exercise 6 -- Non-Correlated Subqueries
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Write subqueries that run independently of the outer query.

    **Tasks:**

    1. Find the order(s) with the highest single-item line total
       (``qty * unit_price``). Use a subquery to find the max, then
       select matching rows.
    2. Find all customers who have placed at least one order using ``IN``
       with a subquery.
    3. Find all products that have **never** been ordered using ``NOT IN``
       with a subquery.
    4. Using a derived table (subquery in ``FROM``), find the category
       with the highest total revenue.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT order_id, product_id, qty, unit_price,
                 qty * unit_price AS line_total
          FROM order_items
          WHERE qty * unit_price = (
              SELECT MAX(qty * unit_price)
              FROM order_items
          );

       **2.**

       .. code-block:: sql

          SELECT customer_id, customer_name
          FROM customers
          WHERE customer_id IN (
              SELECT DISTINCT customer_id
              FROM orders
          );

       **3.**

       .. code-block:: sql

          SELECT product_id, product_name
          FROM products
          WHERE product_id NOT IN (
              SELECT DISTINCT product_id
              FROM order_items
          );

       **4.**

       .. code-block:: sql

          SELECT category, total_revenue
          FROM (
              SELECT p.category,
                     SUM(oi.qty * oi.unit_price) AS total_revenue
              FROM order_items oi
              JOIN products p ON p.product_id = oi.product_id
              GROUP BY p.category
          ) AS cat_rev
          ORDER BY total_revenue DESC
          LIMIT 1;


.. dropdown:: Exercise 7 -- Correlated Subqueries
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Write subqueries that reference the outer query.

    **Tasks:**

    1. For each customer, find their most recent order date using a
       correlated scalar subquery in the ``SELECT`` list.
    2. Find products priced above the average price of their category.
    3. Find customers who have spent more than the average customer
       (use a correlated subquery or a derived table -- your choice).
    4. Rewrite task 2 using ``EXISTS`` instead of a comparison operator.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **1.**

       .. code-block:: sql

          SELECT c.customer_id, c.customer_name,
                 (SELECT MAX(o.order_date)
                  FROM orders o
                  WHERE o.customer_id = c.customer_id
                 ) AS most_recent_order
          FROM customers c;

       **2.**

       .. code-block:: sql

          SELECT p.product_id, p.product_name, p.price, p.category
          FROM products p
          WHERE p.price > (
              SELECT AVG(p2.price)
              FROM products p2
              WHERE p2.category = p.category
          );

       **3.** Using a derived table approach:

       .. code-block:: sql

          SELECT c.customer_id, c.customer_name,
                 cust_totals.total_spent
          FROM customers c
          JOIN (
              SELECT o.customer_id,
                     SUM(oi.qty * oi.unit_price) AS total_spent
              FROM orders o
              JOIN order_items oi ON oi.order_id = o.order_id
              GROUP BY o.customer_id
          ) AS cust_totals ON cust_totals.customer_id = c.customer_id
          WHERE cust_totals.total_spent > (
              SELECT AVG(sub.total_spent)
              FROM (
                  SELECT SUM(oi.qty * oi.unit_price) AS total_spent
                  FROM orders o
                  JOIN order_items oi ON oi.order_id = o.order_id
                  GROUP BY o.customer_id
              ) AS sub
          )
          ORDER BY cust_totals.total_spent DESC;

       **4.** Using ``EXISTS`` to find products above category average
       is awkward; the comparison-based approach in task 2 is more natural.
       A valid ``EXISTS`` rewrite:

       .. code-block:: sql

          SELECT p.product_id, p.product_name, p.price, p.category
          FROM products p
          WHERE EXISTS (
              SELECT 1
              FROM products p2
              WHERE p2.category = p.category
              GROUP BY p2.category
              HAVING p.price > AVG(p2.price)
          );


.. dropdown:: Exercise 8 -- GP2-Style Combined Query (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal:** Combine JOINs, aggregates, GROUP BY, HAVING, subqueries,
    ORDER BY, and LIMIT in a single query.

    **Task:**

    Write a query that answers: *"Which customers in Berlin have spent more
    than the overall average customer spend, and what products did they buy
    most frequently?"*

    Specifically, produce a result with columns: ``customer_name``,
    ``total_spent``, ``favorite_product`` (the product they ordered the
    most units of), and ``units_ordered``.

    Hints:

    - Start by computing total spend per customer using a CTE or derived
      table.
    - Compute the overall average spend.
    - Filter for Berlin customers above that average.
    - For the favorite product, use a correlated subquery or ``LATERAL``
      join.

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: sql

          WITH customer_spend AS (
              SELECT o.customer_id,
                     SUM(oi.qty * oi.unit_price) AS total_spent
              FROM orders o
              JOIN order_items oi ON oi.order_id = o.order_id
              WHERE o.status = 'completed'
              GROUP BY o.customer_id
          ),
          avg_spend AS (
              SELECT AVG(total_spent) AS avg_total FROM customer_spend
          )
          SELECT c.customer_name,
                 cs.total_spent,
                 fav.product_name AS favorite_product,
                 fav.total_qty    AS units_ordered
          FROM customers c
          JOIN customer_spend cs ON cs.customer_id = c.customer_id
          CROSS JOIN avg_spend
          LEFT JOIN LATERAL (
              SELECT p.product_name,
                     SUM(oi.qty) AS total_qty
              FROM orders o
              JOIN order_items oi ON oi.order_id = o.order_id
              JOIN products p    ON p.product_id = oi.product_id
              WHERE o.customer_id = c.customer_id
                AND o.status = 'completed'
              GROUP BY p.product_id, p.product_name
              ORDER BY total_qty DESC
              LIMIT 1
          ) fav ON true
          WHERE c.city = 'Berlin'
            AND cs.total_spent > avg_spend.avg_total
          ORDER BY cs.total_spent DESC;

       This uses a CTE for readability, ``LATERAL`` for the per-customer
       favorite product, and combines ``WHERE`` filtering with aggregate
       pre-computation. A valid alternative would use correlated subqueries
       in the ``SELECT`` list instead of ``LATERAL``.
