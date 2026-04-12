====================================================
Exercises
====================================================

This page contains exercises for Lecture 9. These exercises are designed to
reinforce your understanding of document data modeling (embedding vs
referencing), MongoDB CRUD operations, the aggregation pipeline, index
design, and storage internals.

All exercises use the ``enpm818t`` sample database from the
:doc:`MongoDB Setup Guide <l9_mongodb_setup>` unless stated otherwise.


.. dropdown:: Exercise 1 -- Model Product Reviews (Embed vs Reference)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice the embed-vs-reference decision by designing a document model
    for product reviews.

    **Requirements**

    - Product page must show **product info + latest 3 reviews** fast.
    - Full review history may grow **very large** (thousands of reviews).
    - Seller profile changes **independently** of products and reviews.
    - Decide: **embed vs reference** for each relationship.

    **Deliverable**

    Sketch the document structure for the ``products`` collection and any
    other collections you would create. Explain your rationale for each
    embed/reference decision.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **Recommended design:**

       - **Embed** a small bounded subset: the **latest 3 reviews** inside
         the product document (for fast display on the product page).
       - **Reference** the full review history in a separate ``reviews``
         collection (unbounded data should not live inside the product).
       - **Reference** the seller profile via ``sellerId`` (independent
         lifecycle -- seller info changes without touching product
         documents).

       **Example product document:**

       .. code-block:: javascript

          {
            _id: "A-42",
            title: "Mechanical Keyboard",
            sellerId: 101,
            latestReviews: [
              { customerId: 5, rating: 4, text: "Good build quality.", createdAt: ISODate("2026-03-15") },
              { customerId: 1, rating: 5, text: "Great keyboard!",    createdAt: ISODate("2026-03-03") }
            ]
          }

       **Rationale:** bounded hot data is embedded; unbounded or
       independently managed data is referenced. This is the **subset
       pattern**.


.. dropdown:: Exercise 2 -- Aggregation Pipeline: Revenue by Customer
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Write a MongoDB aggregation pipeline equivalent to a SQL query.

    **Input**

    The ``orders`` collection with fields: ``customerId``, ``status``,
    ``total``.

    **Task**

    Compute the total paid revenue per customer, sorted by revenue
    descending. You might want to first write the SQL equivalent, then
    translate it.

    **SQL equivalent:**

    .. code-block:: sql

       SELECT customer_id, SUM(total) AS revenue
       FROM orders
       WHERE status = 'PAID'
       GROUP BY customer_id
       ORDER BY revenue DESC;

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: javascript

          db.orders.aggregate([
            { $match: { status: "PAID" } },
            { $group: { _id: "$customerId", revenue: { $sum: "$total" } } },
            { $sort: { revenue: -1 } }
          ])

       **Pipeline strategy:**

       1. **Filter early** (``$match``) -- reduce the document stream
          before grouping.
       2. **Group late** (``$group``) -- aggregate only the filtered set.
       3. **Sort only the reduced result set** (``$sort``).

       **Expected output** (with the sample database):

       .. code-block:: javascript

          { _id: 3, revenue: 69.98 }
          { _id: 1, revenue: 59.98 }
          { _id: 5, revenue: 41.99 }


.. dropdown:: Exercise 3 -- Index Design for a Query Pattern
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Design a compound index for a frequent query shape.

    **Frequent query shape:**

    - Filter: ``status = "OPEN"``
    - Filter: ``shipping.country = "IE"``
    - Sort: ``createdAt DESC``

    **Questions**

    1. What compound index would you build?
    2. What is the recommended field order and why?
    3. **Bonus**: what changes if you also need to filter by ``tags``
       (an array field)?

    .. dropdown:: Solution
       :class-container: sd-border-success

       **Recommended starting point:**

       .. code-block:: javascript

          db.orders.createIndex({
            status: 1,
            "shipping.country": 1,
            createdAt: -1
          })

       **Rationale:**

       - **Equality filter fields first** (``status``, ``shipping.country``)
         -- these narrow the scan range.
       - **Sort field last** (``createdAt: -1``) -- the index can deliver
         results in sorted order without an in-memory sort.
       - This follows the **Equality-Sort-Range (ESR)** guideline.

       **Bonus -- array field:**

       If ``tags`` is an array field, the index becomes a **multikey
       index**. In a compound multikey index, at most one field can be an
       array. You would need to re-check whether the sort can still be
       served by the index (multikey sorts often require in-memory sorting).

       .. code-block:: javascript

          db.orders.createIndex({
            status: 1,
            tags: 1,
            createdAt: -1
          })


.. dropdown:: Exercise 4 -- Match the Structure to the Job
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build understanding of MongoDB's internal data structures by matching
    each structure to its purpose.

    **Structures:**

    1. B-tree index
    2. Journal / WAL
    3. Oplog / change log
    4. Checkpoint

    **Match each to one of these purposes:**

    - Fast equality/range lookup
    - Durability between snapshots
    - Async replication / streaming changes
    - Recovery baseline

    .. dropdown:: Solution
       :class-container: sd-border-success

       - **B-tree index** --> fast equality/range lookup
       - **Journal / WAL** --> durability between checkpoints
       - **Oplog / change log** --> async replication / event stream
       - **Checkpoint** --> crash-recovery baseline

       **Explanation:**

       - The **B-tree index** provides O(log n) lookups and range scans.
       - The **journal** (write-ahead log) ensures that operations are
         durable even if the server crashes before the next checkpoint.
       - The **oplog** is a capped collection that records all write
         operations. Secondaries tail it for replication, and change
         streams expose it to applications.
       - **Checkpoints** flush dirty pages to disk, creating a consistent
         snapshot that recovery can start from.


.. dropdown:: Exercise 5 -- Choose a Shard Key
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice shard key selection for a real-world scenario.

    **Scenario**

    Collection: ``deviceEvents``

    - Writes arrive in **time order**.
    - Most queries are by **deviceId**.
    - ``timestamp`` is always increasing.

    **Question**

    Would you shard on:

    A. ``timestamp``

    B. ``deviceId``

    C. hashed ``deviceId``

    Explain the trade-offs of each option.

    .. dropdown:: Solution
       :class-container: sd-border-success

       - **Do not** shard on ``timestamp`` alone -- it is monotonically
         increasing, so all new inserts would route to the same shard
         (hot shard on the ``MaxKey`` side).

       - Prefer **``deviceId``**, often **hashed ``deviceId``** for heavy
         write distribution.

       - If range queries by device and time dominate, revisit with a
         **compound shard key** (``{ deviceId: 1, timestamp: 1 }``) and
         benchmark carefully.

       **Trade-off summary:**

       .. list-table::
          :widths: 25 25 25 25
          :header-rows: 1
          :class: compact-table

          * - **Key**
            - **Write distribution**
            - **Query routing**
            - **Risk**
          * - ``timestamp``
            - Poor (hot shard)
            - Good for time ranges
            - Single-shard bottleneck
          * - ``deviceId``
            - Good (if many devices)
            - Targeted for device queries
            - Skew if some devices are very active
          * - hashed ``deviceId``
            - Excellent (even spread)
            - Targeted for device queries
            - Loses range query on deviceId


.. dropdown:: Exercise 6 -- Anti-pattern Identification (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Identify anti-patterns in a given document model and propose fixes.

    **Scenario**

    A social media application stores user profiles with the following
    structure:

    .. code-block:: javascript

       {
         _id: "user123",
         name: "Alice",
         bio: "...",
         followers: ["user456", "user789", ...],  // grows unbounded
         allPosts: [                               // every post ever made
           { text: "...", likes: 42, comments: [...], createdAt: ... },
           // ... hundreds or thousands of posts
         ],
         loginHistory: [                           // every login event
           { ip: "...", timestamp: ... },
           // ... thousands of entries
         ]
       }

    **Questions**

    1. Identify at least **three anti-patterns** in this design.
    2. For each anti-pattern, propose a concrete fix.
    3. What collections would you create, and what would you embed vs
       reference?

    .. dropdown:: Solution
       :class-container: sd-border-success

       **Anti-patterns identified:**

       1. **Unbounded ``followers`` array** -- can grow to millions for
          popular users, approaching or exceeding the 16 MiB document
          limit. Multikey index on this array becomes very expensive.

          **Fix**: Store follows in a separate ``follows`` collection:
          ``{ followerId: "user456", followeeId: "user123" }``.

       2. **Unbounded ``allPosts`` array** -- embedding every post
          inflates the user document. Reading the profile loads all posts.
          Comments nested inside posts add another unbounded layer.

          **Fix**: Move posts to a ``posts`` collection referencing the
          user: ``{ userId: "user123", text: "...", ... }``. Optionally
          embed the latest 3-5 posts in the user document (subset pattern).

       3. **Unbounded ``loginHistory`` array** -- operational/audit data
          that grows forever. Rarely read with the profile.

          **Fix**: Move to a ``loginHistory`` collection with a TTL index
          to auto-expire old entries:
          ``db.loginHistory.createIndex({ timestamp: 1 }, { expireAfterSeconds: 7776000 })``
          (90 days).

       4. **Bloated document** -- the combination of all three arrays
          means the user document is doing too much. The working set
          (hot data) cannot fit in RAM.

          **Fix**: Keep the user document lean (profile info +
          bounded embedded data). Reference everything else.
