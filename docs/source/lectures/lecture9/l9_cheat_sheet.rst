====================================================
Cheat Sheet
====================================================

A condensed, box-by-box reference covering all major topics from
Lecture 9: the document data model, BSON types, embedding vs referencing,
CRUD operations, aggregation pipeline, indexing, storage internals,
replication, sharding, and design patterns.

----

Document Model Quick Reference
-------------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Concept**
     - **Key Rule**
   * - Document
     - Self-contained BSON record; max **16 MiB**
   * - ``_id``
     - Required, unique per collection; auto-generated ``ObjectId`` if omitted
   * - Nested objects
     - Access with **dot notation**: ``"shipping.country"``
   * - Arrays
     - Hold values or sub-documents; create **multikey** indexes
   * - Flexible schema
     - Documents in the same collection can have different fields
   * - Schema validation
     - Optional; use ``$jsonSchema`` in ``db.createCollection()``

----

BSON Types
----------

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **JSON-like**
     - **BSON extras**
   * - object, array, string, number, boolean, null
     - ``ObjectId``, ``Date``, ``Decimal128``, ``BinData``, ``Timestamp``

----

Embedding vs Referencing
-------------------------

.. list-table::
   :widths: 15 42 43
   :header-rows: 1
   :class: compact-table

   * - **Strategy**
     - **When to use**
     - **Trade-off**
   * - Embed
     - Data is read together, bounded in size
     - Single read, atomic updates; risk of document bloat
   * - Reference
     - Independent lifecycle, unbounded, or shared across documents
     - Normalized, smaller documents; extra reads or ``$lookup``
   * - Subset
     - Embed a bounded slice (e.g., latest 3 reviews); reference the rest
     - Best of both for hot-path reads

----

CRUD Operations
----------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Operation**
     - **Example**
   * - Create
     - ``db.orders.insertOne({ customerId: 42, status: "OPEN" })``
   * - Read
     - ``db.orders.find({ status: "PAID", "shipping.country": "IE" })``
   * - Update
     - ``db.orders.updateOne({ _id: 9001 }, { $set: { status: "PAID" } })``
   * - Delete
     - ``db.orders.deleteOne({ _id: 9001 })``
   * - Upsert
     - ``db.orders.updateOne({ _id: 9001 }, { $set: {...} }, { upsert: true })``

----

Update Operators
-----------------

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - **Operator**
     - **Purpose**
   * - ``$set``
     - Set a field to a value
   * - ``$unset``
     - Remove a field
   * - ``$inc``
     - Increment a numeric field
   * - ``$push``
     - Append to an array
   * - ``$pull``
     - Remove from an array by condition
   * - ``$addToSet``
     - Append to array only if value is not already present

----

Aggregation Pipeline
---------------------

**Stage order for performance**: ``$match`` -> ``$group`` -> ``$sort``
(filter early, group late, sort the reduced set).

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - **Stage**
     - **SQL equivalent**
   * - ``$match``
     - ``WHERE`` / ``HAVING``
   * - ``$group``
     - ``GROUP BY`` + aggregation functions
   * - ``$sort``
     - ``ORDER BY``
   * - ``$project``
     - ``SELECT`` (column list)
   * - ``$unwind``
     - Unnest an array (no direct SQL equivalent)
   * - ``$lookup``
     - ``LEFT OUTER JOIN``
   * - ``$limit`` / ``$skip``
     - ``LIMIT`` / ``OFFSET``

----

Index Types
-----------

.. list-table::
   :widths: 22 78
   :header-rows: 1
   :class: compact-table

   * - **Type**
     - **Key Rule**
   * - Single field
     - One field; ``_id`` index is automatic and undeletable
   * - Compound
     - Multiple fields; **order matters** (supports prefix queries)
   * - Multikey
     - Auto-created when indexing an array field; one entry per element
   * - Wildcard
     - ``{ "$**": 1 }``; indexes all fields; slower than targeted indexes
   * - Partial
     - Only indexes documents matching a filter expression
   * - TTL
     - Single-field on a date; auto-deletes expired documents

**Index design rule**: equality fields first, sort field next, range
fields last (ESR).

----

Explain Output
--------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Indicator**
     - **Meaning**
   * - ``IXSCAN``
     - Index scan (good)
   * - ``COLLSCAN``
     - Full collection scan (usually bad at scale)
   * - ``totalDocsExamined``
     - How many documents were read
   * - ``totalKeysExamined``
     - How many index entries were scanned
   * - ``nReturned``
     - How many documents matched

**Goal**: ``totalDocsExamined`` should be close to ``nReturned``.

----

Storage Internals (WiredTiger)
-------------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Role**
   * - Journal (WAL)
     - Sequential write-ahead log; durability between checkpoints
   * - Checkpoint
     - Periodic flush of dirty pages to disk (default every 60s)
   * - B-tree indexes
     - Fast equality and range lookups (same as PostgreSQL B+tree concept)
   * - Block compression
     - On by default (snappy/zstd); reduces disk usage
   * - WiredTiger cache
     - In-memory pages; sized to ~50% of RAM by default

----

Replication
-----------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Concept**
     - **Key Rule**
   * - Replica set
     - One primary + secondaries; automatic failover
   * - Oplog
     - Capped collection recording all writes; secondaries tail it
   * - Elections
     - One primary at a time; RAFT-based; ~10-12 seconds to complete
   * - Read preference
     - ``primary``, ``secondary``, ``nearest`` -- controls **where** reads go
   * - Read concern
     - ``local``, ``majority``, ``snapshot`` -- controls **freshness**
   * - Write concern
     - ``w: 1``, ``w: "majority"`` -- controls **when** the write is acknowledged

----

Sharding
--------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Concept**
     - **Key Rule**
   * - Shard key
     - Determines how data is distributed; **hard to change** later
   * - ``mongos``
     - Query router; directs operations to correct shard(s)
   * - Chunks
     - Contiguous key ranges; migrated by the balancer
   * - Targeted query
     - Includes shard key; routed to one shard (fast)
   * - Scatter-gather
     - Missing shard key; broadcast to all shards (slow)

**Shard key checklist**: high cardinality, low frequency skew, not
monotonically increasing, supports common queries.

----

Anti-patterns
-------------

.. list-table::
   :widths: 25 40 35
   :header-rows: 1
   :class: compact-table

   * - **Anti-pattern**
     - **Symptom**
     - **Fix**
   * - Bloated documents
     - Working set exceeds RAM; high bandwidth
     - Split cold data to separate collection
   * - Unbounded arrays
     - Document growth; 16 MiB risk; slow multikey indexes
     - Subset pattern or reference
   * - Over-reliance on ``$lookup``
     - Slow reads; document store used like a relational DB
     - Embed data that is always read together
   * - Monotonic shard key
     - Hot shard; unbalanced writes
     - Use hashed sharding or compound key

----

Decision Checklist: Document vs Relational
-------------------------------------------

.. list-table::
   :widths: 40 30 30
   :header-rows: 1
   :class: compact-table

   * - **Signal**
     - **Lean document**
     - **Lean relational**
   * - Aggregate boundaries are clear
     - Yes
     -
   * - Schema changes frequently
     - Yes
     -
   * - Many-way joins dominate
     -
     - Yes
   * - Cross-document invariants dominate
     -
     - Yes
   * - Data is read mostly as whole objects
     - Yes
     -
