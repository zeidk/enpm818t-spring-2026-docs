====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 9: Document Store Databases.
Topics include the document data model, BSON, embedding vs referencing,
CRUD operations, the aggregation pipeline, indexing (compound, multikey,
wildcard, partial), WiredTiger storage internals, replication (replica
sets, oplog, elections), sharding (shard keys, chunks), design patterns,
and anti-patterns.

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

   What is the maximum size of a single MongoDB document?

   A. 4 MiB

   B. 16 MiB

   C. 64 MiB

   D. No limit

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- 16 MiB

   MongoDB enforces a hard 16 MiB limit per document. This prevents
   unbounded growth from patterns like unbounded arrays.


.. admonition:: Question 2
   :class: hint

   Which format does MongoDB use to store documents on disk?

   A. JSON

   B. XML

   C. BSON

   D. Protocol Buffers

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- BSON

   BSON (Binary JSON) extends JSON with additional types like
   ``ObjectId``, ``Date``, ``Decimal128``, and preserves field order.


.. admonition:: Question 3
   :class: hint

   In MongoDB, which field is required in every document and must be
   unique within a collection?

   A. ``name``

   B. ``_id``

   C. ``key``

   D. ``id``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``_id``

   Every MongoDB document must have an ``_id`` field. If not provided,
   the driver generates an ``ObjectId``. The ``_id`` index is created
   automatically and cannot be dropped.


.. admonition:: Question 4
   :class: hint

   When should you prefer **embedding** related data inside a document
   rather than referencing it in a separate collection?

   A. When the related data is unbounded and grows forever.

   B. When the related data has an independent lifecycle.

   C. When the related data is always read together with the parent
      and is bounded in size.

   D. When you need to join data from five or more collections.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- When the related data is always read together with the
   parent and is bounded in size.

   Embedding optimizes for read locality and atomic writes. Unbounded
   data (A) should be referenced. Independent lifecycle (B) suggests
   a separate collection. Heavy joining (D) suggests relational may
   be more appropriate.


.. admonition:: Question 5
   :class: hint

   What does ``$push`` do in a MongoDB update operation?

   A. Replaces the entire document.

   B. Increments a numeric field by a given amount.

   C. Appends a value to an array field.

   D. Removes a field from the document.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Appends a value to an array field.

   ``$push`` adds an element to the end of an array. ``$inc``
   increments, ``$unset`` removes a field, and ``$set`` sets a value.


.. admonition:: Question 6
   :class: hint

   Which aggregation stage is the MongoDB equivalent of SQL's
   ``GROUP BY``?

   A. ``$match``

   B. ``$project``

   C. ``$group``

   D. ``$unwind``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``$group``

   ``$group`` groups documents by a key and applies accumulators like
   ``$sum``, ``$avg``, ``$count``. ``$match`` is equivalent to
   ``WHERE`` / ``HAVING``.


.. admonition:: Question 7
   :class: hint

   What type of join does ``$lookup`` perform?

   A. Inner join

   B. Right outer join

   C. Left outer join

   D. Cross join

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Left outer join

   ``$lookup`` performs a left outer join: all documents from the
   input collection are preserved, and matching documents from the
   ``from`` collection are added as an array.


.. admonition:: Question 8
   :class: hint

   In MongoDB's ``explain()`` output, what does ``COLLSCAN`` indicate?

   A. The query used a compound index.

   B. The query used a collection-level lock.

   C. The query performed a full collection scan (no index used).

   D. The query was cached by the query planner.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- The query performed a full collection scan (no index used).

   ``COLLSCAN`` means every document in the collection was examined.
   ``IXSCAN`` indicates an index was used.


.. admonition:: Question 9
   :class: hint

   What happens when you create an index on an array field in MongoDB?

   A. The index is rejected -- arrays cannot be indexed.

   B. A **multikey index** is created with one entry per array element.

   C. Only the first element of the array is indexed.

   D. The entire array is stored as a single index key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A multikey index is created with one entry per array element.

   Multikey indexes allow efficient queries on array contents. A
   compound index can have at most one array field.


.. admonition:: Question 10
   :class: hint

   What is the purpose of a **partial index** in MongoDB?

   A. To index only a subset of fields in each document.

   B. To index only documents that match a filter expression.

   C. To index only the first 100 documents in a collection.

   D. To create an index that is only used during off-peak hours.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To index only documents that match a filter expression.

   Partial indexes reduce storage and maintenance cost by indexing
   only the "hot" subset (e.g., only ``OPEN`` orders).


.. admonition:: Question 11
   :class: hint

   What is MongoDB's default storage engine?

   A. RocksDB

   B. InnoDB

   C. WiredTiger

   D. LevelDB

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- WiredTiger

   WiredTiger has been MongoDB's default storage engine since version
   3.2. It provides document-level concurrency, compression, and
   journaling.


.. admonition:: Question 12
   :class: hint

   In a MongoDB replica set, which component records all write
   operations for replication?

   A. The journal

   B. The oplog

   C. The balancer

   D. The config server

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The oplog

   The oplog (operations log) is a capped collection that records
   write operations. Secondaries tail the oplog to replicate data.
   The journal is for local crash recovery.


.. admonition:: Question 13
   :class: hint

   What is the primary risk of using a monotonically increasing field
   (like a timestamp) as a shard key?

   A. It causes data loss during failover.

   B. All new inserts go to the same shard, creating a hot spot.

   C. It prevents the use of compound indexes.

   D. It makes ``$lookup`` operations fail.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- All new inserts go to the same shard, creating a hot spot.

   Monotonically increasing keys route all new writes to the shard
   holding the ``MaxKey`` range. Hashed sharding is a common fix.


.. admonition:: Question 14
   :class: hint

   Which anti-pattern involves embedding an ever-growing list inside
   a document?

   A. Bloated documents

   B. Unbounded arrays

   C. Over-normalized design

   D. Orphaned references

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Unbounded arrays

   Unbounded arrays grow without limit, degrading read performance,
   inflating document size, and risking the 16 MiB limit. Fix with
   the subset pattern or references.


.. admonition:: Question 15
   :class: hint

   What does ``w: "majority"`` mean in a MongoDB write concern?

   A. The write is acknowledged after it reaches the primary only.

   B. The write is acknowledged after a majority of replica set
      members confirm it.

   C. The write is acknowledged after it is flushed to disk on the
      primary.

   D. The write is acknowledged after it reaches all shards.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The write is acknowledged after a majority of replica set
   members confirm it.

   ``w: "majority"`` provides stronger durability guarantees than
   ``w: 1`` (primary only). It ensures the write survives a primary
   failover.


.. admonition:: Question 16
   :class: hint

   In the aggregation pipeline, what is the recommended order of
   stages for best performance?

   A. ``$sort`` -> ``$group`` -> ``$match``

   B. ``$match`` -> ``$group`` -> ``$sort``

   C. ``$group`` -> ``$match`` -> ``$sort``

   D. ``$project`` -> ``$match`` -> ``$group``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``$match`` -> ``$group`` -> ``$sort``

   Filter early (``$match``) to reduce the number of documents
   flowing through the pipeline, group the reduced set, then sort
   the final output.


.. admonition:: Question 17
   :class: hint

   What is the role of ``mongos`` in a sharded MongoDB cluster?

   A. It stores the data for the busiest shard.

   B. It acts as a query router, directing operations to the
      correct shard(s).

   C. It manages replica set elections.

   D. It compresses data before writing to disk.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- It acts as a query router, directing operations to the
   correct shard(s).

   ``mongos`` examines the query, determines which shard(s) hold the
   relevant data (based on the shard key), and routes the operation
   accordingly.


.. admonition:: Question 18
   :class: hint

   A TTL index in MongoDB is used to:

   A. Limit the number of indexes on a collection.

   B. Automatically delete documents after a specified time.

   C. Throttle write operations during peak hours.

   D. Track the time-to-live of network connections.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Automatically delete documents after a specified time.

   TTL indexes are single-field indexes on a date field. MongoDB
   runs a background thread that removes expired documents.


----


True / False (Questions 19-28)
================================

.. admonition:: Question 19
   :class: hint

   **True or False:** In MongoDB, a single document write (e.g.,
   ``updateOne``) is atomic.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Single-document operations (insert, update, delete) are always
   atomic in MongoDB. This is the fundamental consistency guarantee.


.. admonition:: Question 20
   :class: hint

   **True or False:** MongoDB collections enforce a fixed schema by
   default -- all documents must have the same fields.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   MongoDB collections have a **flexible schema** by default.
   Documents in the same collection can have different fields.
   Optional schema validation can be added with JSON Schema.


.. admonition:: Question 21
   :class: hint

   **True or False:** The ``_id`` index in MongoDB can be dropped to
   save storage space.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The ``_id`` index is created automatically and **cannot be
   dropped**. It ensures unique identification of every document.


.. admonition:: Question 22
   :class: hint

   **True or False:** In a compound index ``{ a: 1, b: 1, c: 1 }``,
   a query filtering only on ``b`` can efficiently use this index.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Compound indexes support **prefix queries** (left to right). A
   query on ``b`` alone cannot use this index because ``a`` is not
   in the filter. The index supports queries on ``a``, ``a + b``,
   or ``a + b + c``.


.. admonition:: Question 23
   :class: hint

   **True or False:** ``$lookup`` in MongoDB performs an inner join,
   dropping documents with no match.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``$lookup`` performs a **left outer join**. Documents with no
   match get an empty array for the joined field.


.. admonition:: Question 24
   :class: hint

   **True or False:** ``updateMany()`` is atomic across all matched
   documents as a single unit.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   ``updateMany()`` is atomic **per document**, not as one giant
   unit. Each individual document update is atomic, but other
   operations can interleave between documents.


.. admonition:: Question 25
   :class: hint

   **True or False:** WiredTiger uses document-level write concurrency,
   meaning two writes to different documents in the same collection
   can proceed concurrently.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   WiredTiger provides document-level concurrency control, unlike
   older MongoDB storage engines that used collection-level locking.


.. admonition:: Question 26
   :class: hint

   **True or False:** In a sharded cluster, queries that do not
   include the shard key must be sent to every shard (scatter-gather).

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   Without the shard key, ``mongos`` cannot determine which shard
   holds the data, so it broadcasts the query to all shards. This
   is called a scatter-gather query.


.. admonition:: Question 27
   :class: hint

   **True or False:** Hashed sharding preserves range query efficiency
   on the shard key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Hashed sharding distributes writes evenly but **destroys key
   order**. Range queries on the shard key become scatter-gather
   because adjacent key values are spread across different shards.


.. admonition:: Question 28
   :class: hint

   **True or False:** MongoDB's journal (WAL) can be disabled in
   current versions to improve write performance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   In current MongoDB versions, journaling is **always enabled** and
   cannot be turned off. It is essential for crash recovery.


----


Essay Questions (Questions 29-32)
=================================

.. admonition:: Question 29
   :class: hint

   Explain the difference between **embedding** and **referencing** in
   MongoDB. Give one scenario where embedding is preferred and one where
   referencing is preferred.

.. dropdown:: Answer
   :class-container: sd-border-success

   **Embedding** places related data inside the parent document (e.g.,
   line items inside an order). It provides single-document reads and
   atomic updates. It is preferred when the related data is **always
   read together** with the parent and is **bounded in size** (e.g.,
   shipping address inside an order).

   **Referencing** stores related data in a separate collection linked
   by an ID. It avoids document bloat and supports independent
   lifecycles. It is preferred when the related data is **unbounded**
   (e.g., all reviews for a product) or **changes independently**
   (e.g., customer profile).


.. admonition:: Question 30
   :class: hint

   Describe the role of the **oplog** in MongoDB replication. How does
   it relate to **change streams**?

.. dropdown:: Answer
   :class-container: sd-border-success

   The **oplog** (operations log) is a capped collection in the
   ``local`` database that records all write operations on the
   primary. Secondaries tail the oplog to apply the same operations,
   keeping their data in sync. The oplog is the foundation of
   MongoDB's replication mechanism.

   **Change streams** are an application-level API built on top of
   the oplog. They let applications subscribe to real-time data
   changes without directly tailing the oplog. This provides a
   cleaner, resumable interface for event-driven architectures.


.. admonition:: Question 31
   :class: hint

   A teammate proposes sharding a ``userActivity`` collection on the
   ``createdAt`` timestamp field. Explain why this is problematic and
   suggest a better shard key.

.. dropdown:: Answer
   :class-container: sd-border-success

   Sharding on ``createdAt`` is problematic because timestamps are
   **monotonically increasing**. All new inserts would route to the
   shard holding the ``MaxKey`` range, creating a **hot shard** that
   bears all the write load while other shards sit idle.

   A better choice is **``userId``** (or **hashed ``userId``**). This
   distributes writes across shards based on user identity. Since most
   queries likely filter by user, ``mongos`` can route queries to a
   single shard instead of scatter-gathering. If range queries by user
   and time are important, a compound key ``{ userId: 1, createdAt: 1 }``
   may work.


.. admonition:: Question 32
   :class: hint

   Compare how MongoDB and PostgreSQL handle the **write path**.
   Mention the role of the journal/WAL, checkpoints, and
   acknowledgment.

.. dropdown:: Answer
   :class-container: sd-border-success

   Both MongoDB (WiredTiger) and PostgreSQL use a **write-ahead log
   (WAL)** pattern:

   1. The write is first recorded in a sequential log (MongoDB's
      **journal**, PostgreSQL's **WAL**).
   2. The data pages and indexes are modified in memory.
   3. The operation is **acknowledged** to the client (in MongoDB,
      per the ``writeConcern``; in PostgreSQL, after WAL flush for
      synchronous commit).
   4. A background process periodically **checkpoints** dirty pages
      to disk (MongoDB's WiredTiger checkpoints, PostgreSQL's
      ``CHECKPOINT``).

   The key similarity is that both systems prioritize durability
   through the log and defer full page writes to checkpoints. The
   difference is that MongoDB adds replication through the **oplog**
   (a separate logical log), while PostgreSQL uses WAL shipping or
   logical replication.
