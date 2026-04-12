====================================================
Lecture
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Document Store Databases
====================================================

Concepts, internals, and MongoDB in practice. This lecture covers:

- The document data model and how it differs from relational tables
- CRUD operations and the aggregation pipeline
- Indexing, query execution, and storage internals
- Replication, sharding, and production operations
- Design patterns and anti-patterns

Today's arc: **why documents exist**, **how to model and query them**,
**how the engine works underneath**, and **when to choose a document store
over a relational database**.


Why This Topic Matters
----------------------------------------------------

- Application payloads are often **nested**, **irregular**, and
  **fast-changing**.
- MongoDB is a **document database** built for application development
  and scaling.
- Similar ideas show up in **CouchDB**, **Amazon DocumentDB**, and
  **RethinkDB**.

.. admonition:: Key Insight
   :class: tip

   In earlier lectures we designed schemas around normalization and
   relational integrity. Document stores flip the priority: model around
   **access patterns** and **aggregate boundaries** rather than
   elimination of redundancy.


1 -- What Are Document Stores?
====================================================


What Is a Document Store?
----------------------------------------------------

A document store is a database that:

- Stores **self-contained records** as documents.
- Documents expose **named fields**, **objects**, and **arrays**.
- Collections can hold documents with **different shapes**.
- In MongoDB specifically, records are stored as **BSON documents**
  (Binary JSON).

Unlike relational tables where every row has the same columns, a document
collection allows each document to carry a different set of fields. This
is sometimes called a **flexible schema** (a better term than
"schema-free", since your application always has an implicit schema).


Why Flexibility Matters
----------------------------------------------------

- New fields can appear without a whole-table redesign (no ``ALTER TABLE
  ADD COLUMN``).
- One collection can hold **polymorphic** records (e.g., different product
  types with different attributes).
- Useful when requirements evolve faster than your schema migration cycle.

.. admonition:: Comparison with Relational
   :class: note

   In PostgreSQL, adding an optional column to a 100M-row table requires
   an ``ALTER TABLE`` (which may or may not rewrite the table depending on
   the default). In MongoDB, you simply start writing documents with the
   new field -- old documents without it continue to work.


The Core Promise: Aggregate-Oriented Data
----------------------------------------------------

The central idea behind document databases is:

   **Store what you usually read or write together.**

Consider an e-commerce order. In a relational database, this entity is
split across multiple tables: ``orders``, ``order_items``,
``shipping_addresses``, ``payments``. In a document database, you can
store the entire order as a single document:

.. only:: html

   .. figure:: /_static/images/l9/aggregate-data-tree-light.png
      :alt: Order document tree showing customerId, shipping, payment, and lineItems array with sku, qty, priceAtPurchase
      :width: 90%
      :align: center
      :class: only-light

      **Aggregate-oriented data**: store what you usually read or write together.

   .. figure:: /_static/images/l9/aggregate-data-tree-dark.png
      :alt: Order document tree showing customerId, shipping, payment, and lineItems array with sku, qty, priceAtPurchase
      :width: 90%
      :align: center
      :class: only-dark

      **Aggregate-oriented data**: store what you usually read or write together.

This means a single read returns the complete order -- no joins required.

.. admonition:: Class Discussion
   :class: hint

   **When is a row the wrong abstraction?**

   Think about scenarios where the relational row model creates friction:

   - Shopping carts with variable items
   - User profiles with optional/varying preferences
   - API session state
   - CMS pages with mixed content blocks
   - Event envelopes with variable payloads


2 -- The Document Data Model
====================================================


Document Anatomy
----------------------------------------------------

A MongoDB document is a JSON-like object stored internally as BSON:

.. code-block:: javascript

   {
     _id: ObjectId("..."),
     customerId: 42,
     status: "PAID",
     shipping: { country: "IE", city: "Dublin" },
     items: [
       { sku: "A-42", qty: 2, priceAtPurchase: 19.99 }
     ]
   }

Key properties:

- ``_id`` is **required and unique** within a collection. If you do not
  provide one, the driver generates an ``ObjectId``.
- **Nested objects and arrays are normal** -- not a special feature, but
  the default way to model related data.
- MongoDB documents have a **16 MiB maximum size**. This is a hard limit
  that prevents unbounded growth.


JSON vs BSON
----------------------------------------------------

MongoDB stores documents in **BSON** (Binary JSON), which extends JSON
with additional types:

.. list-table::
   :widths: 30 30
   :header-rows: 1
   :class: compact-table

   * - **JSON-like API**
     - **BSON extras**
   * - object
     - ``ObjectId``
   * - array
     - ``Date``
   * - string
     - ``Decimal128``
   * - number
     - ``BinData``
   * - boolean / null
     - ``Timestamp``

- BSON preserves **types** that plain JSON does not (e.g., distinguishing
  integers from floats, storing dates as native types).
- BSON document fields are **ordered** (field order matters for equality
  comparison of sub-documents).


Nested Documents and Arrays
----------------------------------------------------

- Documents can contain **sub-documents** (embedded objects).
- Documents can contain **arrays** (lists of values or sub-documents).
- Queries can target nested fields directly using **dot notation**.
- This maps naturally to objects in application code -- no
  object-relational impedance mismatch.


Named Fields + Typed Values
----------------------------------------------------

- Documents carry their **field names** in every record (unlike relational
  tables where column names are in the catalog, not in each row).
- BSON carries **value types** with each value.
- Collections may mix shapes unless you add validation.
- **"Flexible schema"** is the better term than "schema-free" -- your
  application always has expectations about document structure.


Embedding vs Referencing
====================================================

The most important modeling decision in a document database is whether
related data should be **embedded** inside the parent document or
**referenced** by ID in a separate collection.


Embedding Example
----------------------------------------------------

.. code-block:: javascript

   // Single document -- order with embedded items and shipping
   {
     _id: 9001,
     customerId: 42,
     shipping: { country: "IE", city: "Dublin" },
     items: [
       { sku: "A-42", qty: 2, priceAtPurchase: 19.99 },
       { sku: "B-07", qty: 1, priceAtPurchase: 7.50 }
     ]
   }

Benefits:

- **Single document read** -- one round trip returns the complete order.
- **Single atomic update** for related fields -- adding an item and
  updating the total happen atomically.
- **Denormalization is intentional** -- you accept data duplication in
  exchange for read performance.


Referencing Example
----------------------------------------------------

.. code-block:: javascript

   // orders collection
   { _id: 9001, customerId: 42, productIds: ["A-42", "B-07"] }

   // customers collection
   { _id: 42, name: "Ada" }

   // products collection
   { _id: "A-42", title: "Keyboard" }

Benefits:

- Better for **independent lifecycle and reuse** (customer profile changes
  independently of orders).
- **Avoids document bloat** (review history can grow without inflating the
  product document).
- May require extra reads or ``$lookup`` (MongoDB's left outer join).


Rule of Thumb: Embed vs Reference
----------------------------------------------------

Use this decision flowchart:

.. only:: html

   .. figure:: /_static/images/l9/embed-vs-reference-flowchart-light.png
      :alt: Decision flowchart for embedding vs referencing: read together? bounded size? independent lifecycle?
      :width: 70%
      :align: center
      :class: only-light

      **Embed vs reference decision flowchart.**

   .. figure:: /_static/images/l9/embed-vs-reference-flowchart-dark.png
      :alt: Decision flowchart for embedding vs referencing: read together? bounded size? independent lifecycle?
      :width: 70%
      :align: center
      :class: only-dark

      **Embed vs reference decision flowchart.**
      
1. **Are the data read together?**

   - **Usually yes** -> Is the embedded data **bounded in size**?

     - **Yes** -> **Embed**.
     - **No** -> **Reference** or use the **subset pattern** (embed a
       bounded slice, reference the full history).

   - **Usually no** -> Does the related entity have an **independent
     lifecycle**?

     - **Yes** -> **Reference**.
     - **No** -> Re-evaluate your aggregate boundaries.

.. admonition:: Key Insight
   :class: tip

   The hot path is often the **order** (or whatever your core aggregate
   is). Embed data that always travels with it. Reference data that lives
   independently or can grow without bound.


Example Domain Model: Order as Aggregate Root
----------------------------------------------------

.. only:: html

   .. figure:: /_static/images/l9/order-aggregate-root-light.png
      :alt: Order aggregate root diagram showing Items, Shipping, Payment embedded and customerId, promoCode referenced
      :width: 70%
      :align: center
      :class: only-light

      **Order as aggregate root**: the hot path is the order. Embed data that
      always travels with it; reference data that lives independently.

   .. figure:: /_static/images/l9/order-aggregate-root-dark.png
      :alt: Order aggregate root diagram showing Items, Shipping, Payment embedded and customerId, promoCode referenced
      :width: 70%
      :align: center
      :class: only-dark

      **Order as aggregate root**: the hot path is the order. Embed data that
      always travels with it; reference data that lives independently.

Relational vs Document: Side by Side
----------------------------------------------------

**Relational (PostgreSQL)**

.. code-block:: sql

   CREATE TABLE orders (
     id BIGINT PRIMARY KEY,
     customer_id BIGINT NOT NULL,
     shipping_country CHAR(2) NOT NULL
   );

   CREATE TABLE order_items (
     order_id BIGINT NOT NULL,
     sku TEXT NOT NULL,
     qty INT NOT NULL,
     PRIMARY KEY (order_id, sku)
   );

**Document (MongoDB)**

.. code-block:: javascript

   {
     _id: 9001,
     customerId: 42,
     shipping: { country: "IE", city: "Dublin" },
     items: [
       { sku: "A-42", qty: 2, priceAtPurchase: 19.99 },
       { sku: "B-07", qty: 1, priceAtPurchase: 7.50 }
     ]
   }


JOIN at Read Time vs Single-Document Read
----------------------------------------------------

**SQL** (requires a join to reassemble the order):

.. code-block:: sql

   SELECT o.id, o.shipping_country, i.sku, i.qty
   FROM orders o
   JOIN order_items i ON i.order_id = o.id
   WHERE o.id = 9001;

**MongoDB** (single document read):

.. code-block:: javascript

   db.orders.findOne({ _id: 9001 })

The trade is often **duplication on write** vs **joins on read**.


Querying Nested Fields with Dot Notation
----------------------------------------------------

.. code-block:: javascript

   db.orders.find({
     "shipping.country": "IE",
     "items.sku": "A-42"
   })

- **Dot notation** reaches inside nested objects.
- The same idea works for nested fields in **indexes**.
- Array fields can become **multikey** indexes.


Flexible Schema != No Governance
----------------------------------------------------

- Your application still has a schema -- it is just not enforced by the
  database by default.
- Some fields are **non-negotiable** (e.g., ``_id``, ``customerId``).
- Some fields are intentionally **optional or polymorphic**.
- Governance moves from "fixed tables" to **"explicit modeling +
  validation"**.


Schema Validation with JSON Schema
----------------------------------------------------

MongoDB supports optional schema validation using JSON Schema:

.. code-block:: javascript

   db.createCollection("students", {
     validator: {
       $jsonSchema: {
         bsonType: "object",
         required: ["name", "year"],
         properties: {
           name: { bsonType: "string" },
           year: { bsonType: "int", minimum: 1 }
         }
       }
     }
   })

- All inserts must match the rules.
- Invalid inserts/updates are **rejected by default**.
- You can set ``validationAction: "warn"`` to log violations without
  blocking writes.


Schema Versioning Pattern
----------------------------------------------------

When your document shape evolves over time, use a ``schemaVersion`` field:

.. code-block:: javascript

   // v1
   { _id: 1, name: "Taylor", work: "503-555-0110", schemaVersion: 1 }

   // v2
   {
     _id: 2,
     name: "Cameron",
     contactInfo: { work: "670-555-7878", linkedIn: "cam123" },
     schemaVersion: 2
   }

- Old and new shapes can **coexist** in one collection.
- Application code checks ``schemaVersion`` and handles both formats.
- Queries and indexes may need to cover **multiple field locations**.


3 -- CRUD and Aggregation
====================================================


CRUD in MongoDB: Mental Model
----------------------------------------------------

- **Create** documents in a collection (``insertOne``, ``insertMany``).
- **Read** with filter documents (``find``, ``findOne``).
- **Update** with operators (``updateOne``, ``updateMany``).
- **Delete** documents (``deleteOne``, ``deleteMany``).
- **Aggregate** when you need reshaping, grouping, joining, or analytics.


Create Examples
----------------------------------------------------

.. code-block:: javascript

   db.orders.insertOne({
     customerId: 42,
     status: "OPEN",
     shipping: { country: "IE" }
   })

   db.orders.insertMany([
     { customerId: 43, status: "PAID" },
     { customerId: 44, status: "OPEN" }
   ])

- If ``_id`` is omitted, the driver usually generates an ``ObjectId``.
- ``insertMany`` is more efficient for bulk loads (fewer round trips).


Read Examples
----------------------------------------------------

.. code-block:: javascript

   // Find one document by _id
   db.orders.findOne({ _id: 9001 })

   // Find multiple documents with filter
   db.orders.find({
     status: "PAID",
     "shipping.country": "IE"
   })

- Filters are **documents** -- not SQL strings.
- Nested-field queries use **dot notation**.
- Multiple fields in a filter are implicitly ``AND``-ed.


Projection and Sort
----------------------------------------------------

.. code-block:: javascript

   db.orders.find(
     { status: "OPEN" },
     { _id: 0, customerId: 1, total: 1 }
   ).sort({ createdAt: -1 })

- **Projections** reduce the data returned over the wire (similar to
  selecting specific columns in SQL).
- Use ``1`` to include a field, ``0`` to exclude. You cannot mix
  inclusions and exclusions (except for ``_id``).
- **Sorts** are cheapest when an index already matches the query/order
  pattern.


Update Operators
----------------------------------------------------

.. code-block:: javascript

   db.orders.updateOne(
     { _id: 9001 },
     {
       $set: { status: "PAID" },
       $inc: { version: 1 },
       $unset: { couponCode: "" }
     }
   )

- Think **patch**, not full-document rewrite.
- Operators express intent clearly:
  - ``$set`` -- set a field to a value.
  - ``$inc`` -- increment a numeric field.
  - ``$unset`` -- remove a field.
  - ``$push`` -- append to an array.
  - ``$pull`` -- remove from an array.
  - ``$addToSet`` -- append only if not already present.


Updating Arrays
----------------------------------------------------

.. code-block:: javascript

   db.orders.updateOne(
     { _id: 9001 },
     { $push: { items: { sku: "C-99", qty: 1, priceAtPurchase: 12.50 } } }
   )

- Arrays are powerful modeling tools -- they let you embed related data
  without a separate collection.
- They are also easy to let **grow out of control** -- always consider
  whether an array is bounded.


Delete + Expiration
----------------------------------------------------

.. code-block:: javascript

   // Explicit delete
   db.orders.deleteOne({ _id: 9001 })
   db.orders.deleteMany({ status: "CANCELLED" })

   // Automatic expiration with TTL index
   db.sessions.createIndex(
     { expiresAt: 1 },
     { expireAfterSeconds: 0 }
   )

- ``deleteOne()`` / ``deleteMany()`` remove documents.
- **TTL indexes** can automatically expire short-lived data (sessions,
  tokens, temporary records).
- TTL indexes are **single-field** indexes on a date field.


Document-Level Atomicity
----------------------------------------------------

.. code-block:: javascript

   db.accounts.updateOne(
     { _id: 1, balance: { $gte: 100 } },
     { $inc: { balance: -100 } }
   )

- **Single-document writes are atomic** -- this is the fundamental
  consistency guarantee in MongoDB.
- Encode the invariant in the **filter** when possible (the example above
  checks that the balance is sufficient before decrementing).
- ``updateMany()`` is atomic **per document**, not as one giant unit.
- Embedding matters because of this -- the document is the atomic
  boundary unless you intentionally pay for more.


Multi-Document Transactions
----------------------------------------------------

When the invariant spans multiple documents, collections, or shards:

**SQL**

.. code-block:: sql

   BEGIN;
   UPDATE accounts SET balance = balance - 100 WHERE id = 1;
   UPDATE accounts SET balance = balance + 100 WHERE id = 2;
   COMMIT;

**MongoDB**

.. code-block:: javascript

   session.withTransaction(() => {
     db.accounts.updateOne({_id: 1}, {$inc: {balance: -100}}, {session})
     db.accounts.updateOne({_id: 2}, {$inc: {balance: 100}}, {session})
   })

- Use when the invariant spans documents, collections, or shards.
- Supported in MongoDB 4.0+ (replica sets) and 4.2+ (sharded clusters).
- **Costlier** than staying inside one document -- good schema design
  minimizes the need for multi-document transactions.


Aggregation Pipeline
----------------------------------------------------

The aggregation pipeline is MongoDB's equivalent of SQL's ``GROUP BY``,
``HAVING``, window functions, and subqueries -- combined into a single
framework.

A pipeline is a **sequence of stages** over a document stream:

.. only:: html

   .. figure:: /_static/images/l9/aggregation-pipeline-light.png
      :alt: Aggregation pipeline flow: collection to $match to $group to $sort to result
      :width: 100%
      :align: center
      :class: only-light

      **Aggregation pipeline**: a sequence of stages over a document stream.

   .. figure:: /_static/images/l9/aggregation-pipeline-dark.png
      :alt: Aggregation pipeline flow: collection to $match to $group to $sort to result
      :width: 100%
      :align: center
      :class: only-dark

      **Aggregation pipeline**: a sequence of stages over a document stream.

- Most pipelines do **not modify** source documents unless they end with
  ``$merge`` or ``$out``.
- Each stage receives documents from the previous stage and outputs
  documents to the next.


SQL ``GROUP BY`` vs MongoDB Aggregation
----------------------------------------------------

**SQL**

.. code-block:: sql

   SELECT customer_id, SUM(total) AS revenue
   FROM orders
   WHERE status = 'PAID'
   GROUP BY customer_id;

**MongoDB**

.. code-block:: javascript

   db.orders.aggregate([
     { $match: { status: "PAID" } },
     { $group: { _id: "$customerId", revenue: { $sum: "$total" } } }
   ])

The mapping is direct:

- ``WHERE`` -> ``$match``
- ``GROUP BY`` -> ``$group``
- ``SUM()`` -> ``$sum``
- ``HAVING`` -> another ``$match`` after ``$group``


``$lookup`` as a Left Outer Join
----------------------------------------------------

**SQL**

.. code-block:: sql

   SELECT o.id, c.name
   FROM orders o
   LEFT JOIN customers c ON c.id = o.customer_id;

**MongoDB**

.. code-block:: javascript

   db.orders.aggregate([
     {
       $lookup: {
         from: "customers",
         localField: "customerId",
         foreignField: "_id",
         as: "customer"
       }
     }
   ])

- ``$lookup`` outputs an **array field** (even for 1:1 relationships).
- Overuse can hurt performance -- if data is almost always read together,
  **embed it** instead.


Common Aggregation Stages
----------------------------------------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - **Stage**
     - **Purpose**
   * - ``$match``
     - Filter documents (like ``WHERE``)
   * - ``$group``
     - Group and aggregate (like ``GROUP BY``)
   * - ``$sort``
     - Order results
   * - ``$project``
     - Reshape documents (include/exclude/compute fields)
   * - ``$unwind``
     - Deconstruct an array into one document per element
   * - ``$lookup``
     - Left outer join to another collection
   * - ``$limit``
     - Cap the number of output documents
   * - ``$skip``
     - Skip a number of documents (for pagination)
   * - ``$addFields``
     - Add computed fields without removing existing ones
   * - ``$merge``
     - Write pipeline output to a collection
   * - ``$out``
     - Replace a collection with pipeline output


4 -- Indexing and Query Execution
====================================================


Why Indexes Matter
----------------------------------------------------

- Without an index, MongoDB performs a **collection scan** (``COLLSCAN``)
  -- it reads every document.
- Indexes store a small, easy-to-traverse subset of collection data.
- Good indexes **reduce latency**; every extra index **increases write
  work**.
- The trade-off is the same as in relational databases: faster reads,
  slower writes, more storage.


B-tree Indexes and the Default ``_id`` Index
----------------------------------------------------

- MongoDB indexes use a **B-tree** data structure.
- Each collection gets a unique ``_id`` index automatically.
- The ``_id`` index **cannot be dropped**.
- All other indexes are optional and must be created explicitly.


Compound Indexes
----------------------------------------------------

.. code-block:: javascript

   db.orders.createIndex({ customerId: 1, createdAt: -1 })

- **Field order matters** -- the index supports queries that use a
  prefix of the index fields (left-to-right).
- Compound indexes support **prefix queries**: the index above supports
  queries on ``customerId`` alone, or ``customerId`` + ``createdAt``
  together, but **not** ``createdAt`` alone.
- Design them around your real **filter + sort** patterns.


Multikey Indexes for Arrays
----------------------------------------------------

.. code-block:: javascript

   db.orders.createIndex({ "items.sku": 1 })

- Indexing an array field automatically creates a **multikey index** --
  one index entry per array element per document.
- In a compound multikey index, each document can have **at most one
  indexed array field**.
- Array-heavy sorts may still require **in-memory sorting**.


Indexing Nested Fields
----------------------------------------------------

.. code-block:: javascript

   db.orders.createIndex({
     "shipping.country": 1,
     status: 1
   })

- Dot notation works in queries **and** indexes.
- Nested paths are **first-class citizens** -- no special syntax needed.


Wildcard Indexes
----------------------------------------------------

.. code-block:: javascript

   db.events.createIndex({ "$**": 1 })

- Useful when field names vary or are unknown in advance.
- Helpful for flexible metadata-style documents.
- Usually **worse** than targeted indexes on stable fields -- use them
  as a catch-all, not a replacement for thoughtful index design.


Partial Indexes
----------------------------------------------------

.. code-block:: javascript

   db.orders.createIndex(
     { status: 1, createdAt: -1 },
     { partialFilterExpression: { status: "OPEN" } }
   )

- Only index the **hot subset** of documents.
- **Lower storage cost** and **lower maintenance cost** than indexing
  everything.
- The query must include the partial filter expression for the index to
  be used.


Index Trade-offs
----------------------------------------------------

.. list-table::
   :widths: 33 33 34
   :header-rows: 1
   :class: compact-table

   * - **Read latency**
     - **Write cost**
     - **RAM / disk**
   * - usually decreases
     - usually increases
     - usually increases

- **Index only what real queries need** -- do not speculatively create
  indexes.
- **Remove unused indexes aggressively** -- they cost write performance
  and storage for no benefit.


Explain Plans
----------------------------------------------------

.. code-block:: javascript

   db.orders.find({
     status: "OPEN",
     "shipping.country": "IE"
   }).explain("executionStats")

Key things to look for:

- ``IXSCAN`` -> the query used an **index scan** (good).
- ``COLLSCAN`` -> the query did a **full collection scan** (usually bad
  at scale).
- ``totalDocsExamined`` vs returned rows tells you how much wasted work
  the query did.
- ``totalKeysExamined`` shows how many index entries were scanned.


Query Planner + Plan Cache
----------------------------------------------------

- MongoDB evaluates **candidate plans** during a trial period.
- The **winning plan** is cached by query shape.
- ``explain`` ignores the plan cache when it evaluates a query -- it
  always re-plans.
- The plan cache is cleared on index changes, collection drops, or
  server restart.


Slot-Based Execution Engine (SBE)
----------------------------------------------------

- Used for some queries since MongoDB 5.1.
- Avoids materializing intermediate results during execution.
- Often improves **CPU and memory efficiency**.
- Transparent to the application -- you do not need to change queries.


5 -- Core Data Structures and Storage
====================================================


Key Data Structures: A Mental Model
----------------------------------------------------

Think in layers:

.. only:: html

   .. figure:: /_static/images/l9/storage-architecture-light.png
      :alt: Layered architecture diagram showing Query API, Planner, Secondary indexes, Primary document store, Cache/pages, Journal/WAL, and Replication/change log
      :width: 50%
      :align: center
      :class: only-light

      **Key data structures**: records, indexes, durability, cache, distribution.

   .. figure:: /_static/images/l9/storage-architecture-dark.png
      :alt: Layered architecture diagram showing Query API, Planner, Secondary indexes, Primary document store, Cache/pages, Journal/WAL, and Replication/change log
      :width: 50%
      :align: center
      :class: only-dark

      **Key data structures**: records, indexes, durability, cache, distribution.

Each layer serves a purpose: **records**, **indexes**, **durability**,
**cache**, **distribution**.


MongoDB Storage Stack with WiredTiger
----------------------------------------------------

- **WiredTiger** is MongoDB's default storage engine (since MongoDB 3.2).
- Atlas deployments use WiredTiger.
- WiredTiger uses **document-level write concurrency** (no collection-wide
  locks for writes).
- **Journaling + checkpoints** provide durability and recovery.
- WiredTiger supports LSM trees, but MongoDB uses **B-trees**.


Write Path: Journal, Pages, Checkpoint
----------------------------------------------------

.. only:: html

   .. figure:: /_static/images/l9/write-path-sequence-light.png
      :alt: Sequence diagram showing write path from App through mongod, Journal (WAL append), Storage pages (modify document and indexes), acknowledge, and later checkpoint
      :width: 80%
      :align: center
      :class: only-light

      **Write path**: journal first, modify in memory, acknowledge, checkpoint later.

   .. figure:: /_static/images/l9/write-path-sequence-dark.png
      :alt: Sequence diagram showing write path from App through mongod, Journal (WAL append), Storage pages (modify document and indexes), acknowledge, and later checkpoint
      :width: 80%
      :align: center
      :class: only-dark

      **Write path**: journal first, modify in memory, acknowledge, checkpoint later.

When an application issues an ``updateOne()``:

1. **mongod** receives the operation.
2. A **WAL record** is appended to the journal (sequential write).
3. The document and its indexes are **modified in memory** (in WiredTiger
   pages).
4. The operation is **acknowledged** to the client (per ``writeConcern``).
5. Later, a **checkpoint** flushes dirty pages to disk.

This is the same WAL + checkpoint pattern used by PostgreSQL and most
modern databases.


B+tree Storage Formats in WiredTiger
----------------------------------------------------

- WiredTiger row-store and column-store file formats are **B+tree**
  key/value stores.
- WiredTiger also supports **LSM trees** as a tree of B+trees (not used
  by MongoDB).
- MongoDB indexes are exposed to users as **B-tree** structures.


Compression + Caches
----------------------------------------------------

- **Collection block compression** is on by default (snappy or zstd).
- **Index prefix compression** is on by default.
- MongoDB uses both the **WiredTiger internal cache** and the **filesystem
  cache**.
- Index prefix compression can reduce RAM usage significantly.


Recovery After a Crash
----------------------------------------------------

- The **journal** is a write-ahead log on disk.
- **Checkpoints** create a consistent on-disk snapshot (default every
  60 seconds).
- Recovery replays journaled operations since the last checkpoint.
- In current MongoDB, **journaling is always enabled** -- it cannot be
  turned off.


6 -- Replication and Sharding
====================================================


Replica-Set Oplog
----------------------------------------------------

- The **oplog** (operations log) is a special capped collection in the
  ``local`` database.
- The primary writes locally, then records operations in the oplog.
- Secondaries copy and apply oplog entries **asynchronously**.
- **Change streams** build on this idea so applications do not tail the
  oplog directly.


Replica Sets: Topology and Purpose
----------------------------------------------------

A replica set is a group of ``mongod`` instances that maintain the same
data set:

.. only:: html

   .. figure:: /_static/images/l9/replica-set-topology-light.png
      :alt: Replica set topology showing App, Primary mongod, Journal, Storage pages, and Secondary nodes with optional reads
      :width: 70%
      :align: center
      :class: only-light

      **Replica set topology**: one primary accepts writes; secondaries replicate
      via the oplog and optionally serve reads.

   .. figure:: /_static/images/l9/replica-set-topology-dark.png
      :alt: Replica set topology showing App, Primary mongod, Journal, Storage pages, and Secondary nodes with optional reads
      :width: 70%
      :align: center
      :class: only-dark

      **Replica set topology**: one primary accepts writes; secondaries replicate
      via the oplog and optionally serve reads.

- **High availability** -- automatic failover if the primary goes down.
- **Redundancy** -- data is replicated across members.
- **Optional read scaling** from secondaries (with caveats about
  staleness).
- MongoDB's election protocol inherits from **RAFT**.


Elections and Failover
----------------------------------------------------

- **One primary at a time** -- only the primary accepts writes.
- Higher-priority eligible secondaries are preferred in elections.
- Drivers can detect primary loss and retry some writes automatically
  (retryable writes).
- Elections typically complete in **10-12 seconds**.


Read Preference, Read Concern, Write Concern
----------------------------------------------------

.. list-table::
   :widths: 20 40 40
   :header-rows: 1
   :class: compact-table

   * - **Control**
     - **Main question**
     - **Examples**
   * - Read preference
     - **Where** do I read?
     - ``primary``, ``secondary``, ``nearest``
   * - Read concern
     - How **consistent/fresh** must reads be?
     - ``local``, ``majority``, ``snapshot``
   * - Write concern
     - **When** do I get success back?
     - ``w: 1``, ``w: "majority"``, ``j: true``

- Non-primary reads may be **stale**.
- ``majority`` read concern and journal-related write concerns change
  guarantees and cost.
- For most applications, ``w: "majority"`` is the recommended default.


Sharding Architecture
----------------------------------------------------

Sharding is MongoDB's approach to **horizontal scaling**:

.. only:: html

   .. figure:: /_static/images/l9/sharding-architecture-light.png
      :alt: Sharding architecture showing Clients connecting to Primary and optional reads to Secondary nodes
      :width: 90%
      :align: center
      :class: only-light

      **Sharding architecture**: ``mongos`` routes operations to the correct
      shard(s) based on the shard key.

   .. figure:: /_static/images/l9/sharding-architecture-dark.png
      :alt: Sharding architecture showing Clients connecting to Primary and optional reads to Secondary nodes
      :width: 90%
      :align: center
      :class: only-dark

      **Sharding architecture**: ``mongos`` routes operations to the correct
      shard(s) based on the shard key.

- Data is partitioned by **shard key** across multiple shards.
- Each shard is typically a **replica set**.
- ``mongos`` is a query router that directs operations to the correct
  shard(s).
- A **config server** replica set stores cluster metadata.


Chunks, Balancer, Range Migration
----------------------------------------------------

- Sharded data is partitioned into **chunks** (contiguous key ranges).
- Chunks cover inclusive-lower / exclusive-upper key ranges.
- A **balancer** runs in the background, migrating chunks between shards
  to even out the cluster.
- Chunk splits happen automatically as chunks grow.


Choosing a Shard Key
----------------------------------------------------

Shard key selection is one of the most critical decisions in a sharded
deployment:

- Optimize for **cardinality** -- the key should have many distinct
  values.
- Check **frequency** skew -- avoid keys where a few values dominate.
- Avoid **monotonic hot spots** -- monotonically increasing keys (like
  ``ObjectId`` or timestamps) route all new inserts toward the ``MaxKey``
  shard.
- Make sure the key supports your **common query patterns** -- queries
  that include the shard key are routed to a single shard; queries
  without it become **scatter-gather** (every shard must respond).


Hot Shards and Monotonic Keys
----------------------------------------------------

- **Low-cardinality** keys cap effective scale (e.g., sharding by country
  with only 30 values means at most 30 chunks).
- **High-frequency** values create bottleneck chunks.
- **Monotonically increasing** keys route new inserts toward the
  ``MaxKey`` side, creating a single hot shard.
- **Hashed sharding** is a common fix for monotonic keys -- it spreads
  writes evenly but loses range query efficiency.


Architecture Comparison
----------------------------------------------------

.. list-table::
   :widths: 15 45 40
   :header-rows: 1
   :class: compact-table

   * - **System**
     - **Core storage idea**
     - **Distinctive angle**
   * - MongoDB
     - WiredTiger pages + B-tree indexes + journal/checkpoints
     - replica-set oplog + sharding
   * - CouchDB
     - append-only B-trees + MVCC
     - replication-first, sync-friendly
   * - RethinkDB
     - B-Trees on a log-structured engine
     - range sharding + realtime changefeeds


7 -- Design Patterns and Anti-patterns
====================================================


Where Document Stores Shine
----------------------------------------------------

- **User profiles** and preference blobs.
- **Product catalogs** with variable attributes.
- **CMS pages** and content objects.
- **Orders, carts, sessions**, event envelopes.

These are all cases where the data is naturally aggregate-shaped and
schemas vary across instances.


Anti-pattern: Bloated Documents
----------------------------------------------------

- Too many fields stuffed into one hot document.
- Working set stops fitting in memory.
- Bandwidth and RAM usage rise.
- **Fix**: split cold or rarely-read data away from the hot path.


Anti-pattern: Unbounded Arrays
----------------------------------------------------

- Arrays keep growing forever (e.g., all comments on a post embedded in
  the post document).
- Read performance and index maintenance degrade.
- Documents risk hitting the **16 MiB size limit**.
- **Fix**: use the **subset pattern** (embed a bounded slice) or
  **reference** the full history in a separate collection.


Anti-pattern: Expecting Joins Everywhere
----------------------------------------------------

- ``$lookup`` exists, but ``$lookup`` is **not free**.
- If data is almost always read together, **embed it**.
- If data is large, unbounded, or independently updated, **reference it**.
- Heavy ``$lookup`` usage is a signal you might be better served by a
  relational database.


When *Not* to Use a Document Store
----------------------------------------------------

Warning signs that a document store is the wrong choice:

- Design depends on frequent **many-way joins**.
- Invariants span **many documents** all the time.
- Reporting-first workload expects **highly normalized relational shape**.
- You are paying constantly for ``$lookup`` and transactions.


SQL vs Document Store: Decision Checklist
----------------------------------------------------

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
   * - Cross-row invariants dominate
     -
     - Yes
   * - Data is read mostly as whole objects
     - Yes
     -


8 -- Production Operations and Ecosystem
====================================================


Production Monitoring: What to Watch
----------------------------------------------------

- **Atlas Query Profiler / Performance Advisor** (managed deployments).
- Self-managed: **database profiler** and ``$currentOp``.
- **WiredTiger cache** activity and dirty bytes.
- **Replication lag** and oplog headroom.
- **Page faults** and queueing symptoms.


Slow Query Workflow in Practice
----------------------------------------------------

1. **Find the slow operation** (profiler, slow query log, or Atlas).
2. Check ``planSummary`` for ``IXSCAN`` vs ``COLLSCAN``.
3. Run ``explain("executionStats")``.
4. **Add or fix the index**.
5. If that fails, **revisit the data model** (the index cannot save a
   bad schema).


Execution at Scale
----------------------------------------------------

- Keep the **working set** inside memory as much as possible.
- Watch cache reads/writes and page-fault symptoms.
- Every index increases **write amplification**.
- Review document size growth over time, not just today's shape.


Backup, Restore, Migration
----------------------------------------------------

- Atlas continuous backup supports **point-in-time restore**.
- ``mongodump`` / ``mongorestore`` are portable, but may not be the best
  low-impact production strategy.
- AWS supports migration to Amazon DocumentDB via **DMS** and MongoDB
  tooling.


Ecosystem Snapshot
----------------------------------------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - **System**
     - **Short description**
   * - MongoDB
     - BSON document database with WiredTiger, replica sets, sharding
   * - Amazon DocumentDB
     - MongoDB API-compatible managed document DB; compute/storage separated
   * - CouchDB
     - JSON document DB with append-only B-trees, MVCC, replication focus
   * - RethinkDB
     - Document DB with log-structured B-Trees, range sharding, realtime changefeeds


"MongoDB-compatible" Means "Test the Edge Cases"
----------------------------------------------------

- Wire protocol compatibility is **not** full behavioral equivalence.
- Feature support and planners can differ.
- Validate transactions, aggregation stages, index behavior, monitoring,
  and ops tooling when migrating between MongoDB and compatible systems.


Future Directions
----------------------------------------------------

- **Change streams** -> event-driven apps over operational data.
- **Time series collections** -> optimized internal storage for
  time-stamped measurements.
- **SQL Interface / MongoSQL** -> BI-friendly SQL-92-style access over
  document data.


Summary
====================================================

- Think in **aggregates**, not rows.
- Model around **access patterns**.
- Use **embedding** for locality and document-level atomicity.
- Use **indexes deliberately** -- every index costs write performance.
- Choose **shard keys carefully** -- they are hard to change later.
- Expect production symptoms to expose data-model mistakes.

.. admonition:: Discussion to Close
   :class: hint

   - What would make you choose PostgreSQL instead?
   - What would make you choose MongoDB instead?
   - Which part of the stack is hardest to change late?
