====================================================
Part 1 -- Key/Value Stores
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Key/Value Stores
====================================================

Concepts, internals, and Redis in practice. Part 1 covers:

- The key/value data model and how it differs from relational and
  document stores
- The ``put``/``get``/``delete`` API and what you lose (and gain) by
  staying that narrow
- How to model real application data against a schemaless store
- LevelDB and LSM-tree internals
- Distributed K/V concerns: consensus, sharding via rendezvous hashing
- CAP and PACELC trade-offs
- Hands-on Redis

Today's arc: **why K/V stores exist**, **how to model data against
them**, **how the engine works underneath**, and **how they behave in
distributed deployments**.


Why This Topic Matters
----------------------------------------------------

- Modern systems have a huge class of workloads that are dominated by
  fast, key-addressed reads and writes: caches, session stores, feature
  flags, counters, leaderboards, queues, and enrichment layers.
- K/V stores are often the **fastest** and **most horizontally
  scalable** option for those workloads.
- Redis, Memcached, DynamoDB, Aerospike, and Cassandra all expose a K/V
  (or K/V-like) interface at their core.

.. admonition:: Key Insight
   :class: tip

   Document and relational stores push the database to do more on your
   behalf. K/V stores push it to do less -- and let you buy performance
   and scale in exchange. The complexity has to live *somewhere*; in a
   K/V store it lives in your application code.


1 -- What Is a Key/Value Store?
====================================================


Definition
----------------------------------------------------

A **key/value store** is a NoSQL database that:

- Stores data as a collection of **key/value pairs**.
- Uses the **key as the sole primary access path** -- queries retrieve
  values by key.
- Places **few constraints** on what keys and values can be. Keys are
  usually strings or byte arrays; values can be anything from simple
  scalars to complex serialized objects.

K/V stores are **highly partitionable** and allow horizontal scaling at
levels that other database types struggle to match.


K/V Core Concepts
----------------------------------------------------

- **Key**: a unique identifier used to access a specific piece of data.
- **Value**: the data associated with a particular key.
- **In-memory storage**: data is stored exclusively in RAM (not written
  to disk). Redis and Memcached are the common examples.
- **Embedded database**: a DBMS tightly integrated with an application
  -- the database runs *inside* the process rather than as a standalone
  server. LevelDB and RocksDB are typical examples.

Example:

.. code-block:: text

   KEY              -> VALUE
   "user:1"         -> {"name": "Alice", "age": 25}
   "user:2"         -> {"name": "Bob",   "age": 30}
   "session:12345"  -> "active"
   "counter"        -> 42


The K/V Query Language
----------------------------------------------------

K/V stores are optimized for simple read/write performance, and they are
**low-feature** compared to other databases. The basic operations are:

.. code-block:: text

   Put(key, value)
   Get(key)
   Delete(key)

That's it. Some K/V stores layer additional functionality on top
(Redis's lists, sets, sorted sets; range scans; TTLs), but
``Put``/``Get``/``Delete`` are the fundamental operations.


K/V as a "Robust Hashmap"
----------------------------------------------------

You would not be wrong to think of a K/V store as a hashmap with extra
features (persistence, replication, TTL, etc.).

.. code-block:: java

   Map<String, String> m = new HashMap<>();
   m.get("A Key");
   m.put("Key", "Value");
   m.remove("Key");

The difference between a hashmap and a K/V store is mostly about what
happens when the process dies, when you have more data than fits on one
machine, and when multiple clients access it at once.


Benefits of K/V Stores
----------------------------------------------------

.. list-table::
   :widths: 20 80
   :header-rows: 1
   :class: compact-table

   * - **Property**
     - **What it buys you**
   * - Speed
     - Optimized for a narrow data-access pattern; microsecond latencies are common
   * - Scalability
     - Native horizontal sharding; add nodes as data/traffic grows
   * - Simplicity
     - Simple to implement, simple to reason about, simple to operate
   * - Flexibility
     - Few requirements on the shape of keys or values

.. admonition:: Class Discussion
   :class: hint

   - How would a K/V store work in a distributed environment? Is that
     easier or harder to reason about than a tree-based structure?
   - What kinds of use-cases lend themselves to being served by a K/V
     store? What kinds clearly do not?


Common Use Cases
----------------------------------------------------

- **Caching**: store frequently accessed data close to the application.
- **Enrichment**: add supplementary data (e.g., geo-IP lookups) at scale.
- **Leaderboards**: use sorted sets for ranking systems.
- **User profiles / preferences**: small, key-addressed blobs.
- **Configuration management**: feature flags, runtime parameters.
- **Session storage**: short-lived state keyed by a session token.


2 -- Modeling Data in a K/V Store
====================================================


"Schemaless" Is a Half-Truth
----------------------------------------------------

Key/value stores are often described as **schemaless** -- meaning the
database itself does not impose a fixed structure on values. This makes
K/V stores:

- Flexible compared to relational databases.
- Straightforward for storage and retrieval.
- Usable without the database knowing anything about the domain.

**But: complexity has to live somewhere.** The schema does not disappear
when you switch to a K/V store -- it moves into your application code.

.. admonition:: Your Data Always Has a Schema
   :class: note

   Schemas are representations of the *constraints* placed on your data.
   If you are doing anything useful with your data, a schema exists --
   at minimum, the implicit understanding in your code of what fields
   exist and how they relate. Pretending otherwise leads to an entire
   spectrum of pain. Seriously. A spectrum. Like a rainbow.


Modeling in a K/V Store
----------------------------------------------------

If a K/V store defers schema constraints to the application, what do we
do about it?

- For complex objects (e.g., a customer), you will want to store all the
  related details (name, email, address) as related data.
- Use a **consistent naming convention** to group related items. A
  **prefix** or **composite key** does the work that a foreign key
  would do in a relational store.
- Example: ``age:customer:1``, ``email:customer:1``, ``name:customer:1``.
- Another pattern: ``customer:1:age``, ``customer:1:email``, ...

There is no one right answer -- pick a convention and apply it
consistently across the codebase.


Worked Example: A Twitter-Clone
----------------------------------------------------

Let's model a simple Twitter-like application with K/V only. We need:

- Post messages.
- Access the last N messages for a feed.
- Maintain a per-user friend list.
- Implement direct messaging.

**Messages** store a message body keyed by ``message:<user>:<id>``:

.. code-block:: javascript

   // Value
   {
     "message_id": 7,
     "user_id": "zhanif@umd.edu",
     "message": "This is my first message!",
     "time": 1745358379
   }
   // Key
   message:zhanif@umd.edu:7

**Feed** stores a list of recent message keys under ``feed:<user>``:

.. code-block:: javascript

   // Value at key `feed:zhanif@umd.edu`
   {
     "user_id": "zhanif@umd.edu",
     "feed": [
       "message:zhanif@umd.edu:7",
       "message:zhanif@umd.edu:6",
       "message:zhanif@umd.edu:5",
       "message:zhanif@umd.edu:4"
     ]
   }

**Friend list** is just another keyed value at ``friends:<user>``:

.. code-block:: javascript

   {
     "user_id": "zhanif@umd.edu",
     "friends": ["someuser@someemail.com", "anotheruser@anotheremail.com"]
   }

**Direct messages** work the same way -- one key per message, plus a
per-recipient inbox key:

.. code-block:: javascript

   // Key: message:fd07ddccbc7d73cac26fc4a780546ce92df58641:90
   {
     "sender": "zhanif@umd.edu",
     "recipient": "other@umd.edu",
     "id": 90,
     "unread": true
   }

   // Update the recipient's inbox
   { "messages": ["message:fd07ddccbc7d73cac26fc4a780546ce92df58641:90"] }

Every feature becomes: **derive a key, put a value, read by key**. No
joins, no queries -- just careful key design.


3 -- K/V Stores in Practice
====================================================


K/V vs Other Database Types
----------------------------------------------------

K/V stores serve specific use-cases because of their unique features and
limitations. **Choose the database based on your use case, data shape,
and query patterns** -- not because K/V is fashionable.

K/V stores often **lack indexes and scan capabilities**. If you need to
perform anything beyond CRUD-by-key, a K/V store will fight you.


K/V vs Relational Databases
----------------------------------------------------

- **Relational**: structured data, relationships between entities, SQL,
  joins across tables.
- **K/V**: no explicit relationships; no rich query language; excellent
  for high-performance, scalable, simple-access workloads where query
  patterns are well-understood.

.. admonition:: Rule of Thumb
   :class: tip

   If you ever feel the need to ``JOIN`` data in a K/V store, tread
   carefully -- you may have selected the wrong tool.


K/V vs Graph Databases
----------------------------------------------------

- **Graph**: designed for connected data and traversing relationships at
  query time. The schema lives in the database; data modeling is the
  main cost.
- **K/V**: pairs are independent with no built-in way to express
  relationships between them.

**Reflection**: you *can* implement a graph structure on top of a K/V
store -- but should you? Nearly always, the answer is no.


K/V vs Document Databases
----------------------------------------------------

- **Document**: stores data in JSON/BSON/XML, with advanced querying and
  indexing inside the document structure. Often has SQL-like query
  languages.
- **K/V**: simpler; values are opaque to the store.
- Many K/V datastores have drifted closer to the document model over
  time (Redis Hashes, DynamoDB items), and the line is blurry.


When to Use a K/V Store
----------------------------------------------------

If your use case is:

- Robust to changes in underlying data structure, or can be
  asynchronously updated.
- Able to support multiple round-trips to "simulate" a complex query.
- Able to be split into sub-features or aggregated into a single value.
- Highly predictable in query patterns, with tight performance
  requirements.

...you probably have a supportable use case. Similarly, if:

- You don't have structured data.
- Structure changes frequently (in a backwards-compatible way).
- You can trivially predict or derive a unique identifier per item.

...you probably have supportable data.

.. admonition:: Choose Boring Technology
   :class: warning

   In most cases, **you probably do not have a K/V problem** --
   especially for long-lived systems. Choose boring technology; fit the
   store to the data, not the fashion. Trying to force a K/V pair into
   a relational database is often a recipe for disaster -- but so is
   the reverse.


Prominent K/V Stores
----------------------------------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **System**
     - **Short description**
   * - Redis
     - In-memory K/V store with rich data types (strings, hashes, lists, sets, sorted sets); common as cache / broker / primary
   * - Memcached
     - Pure in-memory cache; simpler than Redis, often deployed for caching only
   * - DynamoDB
     - Amazon's managed, distributed K/V store (PA/EL under PACELC)
   * - Aerospike
     - High-throughput hybrid memory/flash K/V store
   * - ScyllaDB
     - Cassandra-compatible, C++ rewrite optimized for latency and throughput
   * - Cassandra
     - Early distributed K/V (wide-column) store; a landmark design
   * - LevelDB / RocksDB
     - Embedded LSM-tree K/V libraries; backbones of many other systems


4 -- Internals: LevelDB and LSM Trees
====================================================


LevelDB at a Glance
----------------------------------------------------

- **LevelDB** is a K/V store built by Google in 2011.
- It supports **ordered mappings** of strings to strings (or generic
  byte arrays).
- Internally, it is based on the **log-structured merge tree (LSM)** --
  a write-optimized B-tree variant.
- It is specifically optimized for **large sequential writes** rather
  than small random writes.


Concurrency in LevelDB
----------------------------------------------------

- LevelDB allows **only one process** to open a database at a time.
- Within that process, multiple **threads** can access it.
- For multi-writer scenarios, only the **first writer** proceeds; others
  block.
- For read/write conflicts, readers can retrieve data from **immutable**
  state separate from the writing process. The updated version takes
  effect during the next compaction.


The LSM Mental Model
----------------------------------------------------

LevelDB is built around two storage artifacts:

- **MemTable**: an in-memory sorted structure (typically a red-black
  tree) that absorbs incoming writes.
- **SSTable** (**S**\ orted **S**\ tring **T**\ able): an immutable,
  sorted, on-disk file of key/value pairs.

To speed up reads, each SSTable has an associated **bloom filter** -- a
small probabilistic data structure that can tell you "definitely not
here" or "probably here" for a given key without reading the file.


LSM Writes
----------------------------------------------------

LevelDB uses a multi-stage write process to support fast sequential
operations:

1. **Write**: new data is first written to the in-memory **MemTable**.
2. **Flush**: when the MemTable is full, it is flushed to disk as an
   **SSTable**.
3. **Compaction**: periodically, multiple SSTables are merged and
   compacted into larger tables (merging duplicate keys, discarding
   older versions).
4. **Tombstones**: deletions are recorded as tombstones in SSTables and
   physically removed during compaction.

Because writes are always sequential (append to WAL, append to SSTable
on flush), an LSM tree amortizes the cost of writes very effectively.


LSM Reads
----------------------------------------------------

LevelDB's read path traverses SSTables looking for the requested key:

1. First, the **MemTable** is checked.

   - If the key is found, the value is returned. Done.

2. Otherwise, a **multi-level search** walks from the smallest /
   least-sorted levels up to higher, more-sorted levels.

3. Each SSTable block has an associated **bloom filter** that eliminates
   most SSTables from the search without reading them.

This is why LSM-tree reads are slower than B-tree reads in the worst
case -- you may have to check multiple levels.


LSM Tree Benefits
----------------------------------------------------

- **Efficient writes**: sequential disk I/O; writes are amortized over
  time through compaction.
- **Improved read performance** (for sequential keys): compaction +
  sorted SSTables means range scans are fast.
- **Suited for high write loads**: NoSQL databases, append-heavy
  transactional systems, event streams.


LSM Tree Drawbacks
----------------------------------------------------

- **Complexity**: more moving parts than a single B-tree.
- **Overhead**: compaction and multiple SSTables introduce ongoing
  background work.
- **Disk I/O**: compaction is a resource-intensive process that
  consumes disk I/O and CPU during background runs.


LSM Trees vs B-trees
----------------------------------------------------

.. list-table::
   :widths: 50 50
   :header-rows: 1
   :class: compact-table

   * - **LSM trees**
     - **B-trees**
   * - Organize data across multiple levels; buffer writes in memory; flush sorted runs to disk
     - Maintain a balanced tree on disk; writes update pages in place
   * - Require periodic compaction to merge and organize data
     - Relatively stable structure with in-place updates
   * - Prioritize **write optimization**; best when write throughput matters and slightly higher read latency is tolerable
     - More balanced between reads and writes; better when read latency must be tight
   * - Common in write-heavy NoSQL (LevelDB, RocksDB, Cassandra, HBase)
     - Default in most relational databases (PostgreSQL, MySQL/InnoDB, WiredTiger)

**Reflection**: which other large-data systems are built on LSM trees?
Which workloads justify the complexity?


5 -- Distributed K/V Structures
====================================================


Scalability and Availability
----------------------------------------------------

- K/V databases are designed to **scale horizontally** -- distribute
  data across multiple nodes or clusters.
- Adding nodes scales capacity and traffic without sacrificing
  per-operation performance.
- This makes K/V stores a natural fit for large, growing datasets.


Single-Node vs Distributed Systems
----------------------------------------------------

A **single-node** system (think SQLite) is:

- Simple to reason about.
- Easy to tune.
- Suitable for a wide array of use cases.

But single-node systems have challenges:

- **Throughput** ceiling.
- **Resource usage** on one box.
- **Resiliency** -- if the box dies, you're down.

When we move to **multiple nodes**, basic interactions get harder:

- We must decide how to **replicate writes**.
- A node can be **down** or **unreachable** at any time.
- Clients cannot manage **wall-clock time** perfectly.
- We have to agree on **entries** across nodes.
- We must decide **which values from node A are stored on node B**.
- We must **scale effectively** as load grows.


Challenges in Distributed Systems
----------------------------------------------------

Two challenges dominate:

- **Consensus**: do all nodes agree on what the keys and values are?
  Solving this in general is *hard* (see: Paxos, Raft).
- **Sharding**: how do we receive queries and route them to the right
  node? This one is more tractable in practice -- **rendezvous hashing**
  is increasingly the preferred solution.


Sharding Through Rendezvous Hashing
----------------------------------------------------

**Problem**: we need clients to agree on K choices from a set of N
possible servers, and we want to minimize how much data moves when
servers join or leave.

**Rendezvous hashing** (sometimes called *highest random weight
hashing*) works as follows:

1. For each data item, combine the data's **key** with each server's
   **identifier** through a hash function to produce a score.
2. The server with the **highest score** (or the top K servers with the
   highest scores) wins and is responsible for that data.
3. When a server disconnects, **only the data that specifically "won"
   by that server** needs to be redistributed.
4. When a new server is added, **only the subset of data where the new
   server scores higher** needs to be rebalanced.

This **minimal redistribution** property is crucial for maintaining
system performance under topology changes.


CAP Theorem
====================================================


The Three Guarantees
----------------------------------------------------

The **CAP theorem** states that any distributed data store can provide
only **two of the following three** guarantees:

- **Consistency (C)**: every read receives the most recent write or an
  error. (Note: this is a stricter notion than the ACID "C".)
- **Availability (A)**: every request received by a non-failing node
  must result in a response.
- **Partition tolerance (P)**: the system continues to operate despite
  arbitrary messages being dropped (or delayed) by the network between
  nodes, or a node being unavailable or unresponsive.


What Happens During a Partition
----------------------------------------------------

When a network partition happens, the system must choose one of:

- **Cancel the operation**: decrease availability but ensure
  consistency.
- **Proceed with the operation**: provide availability but risk
  inconsistency (which does not necessarily mean the system is highly
  available to users, just that it doesn't refuse to answer).

Thus, in a partition, you must pick either **consistency** or
**availability**.

.. admonition:: There Is *Always* a Partition
   :class: warning

   In real networks, partitions are not a rare failure mode -- they
   happen all the time at various scales (TCP stalls, switch failures,
   cross-region latency). Any real distributed system must have
   **partition tolerance**; CAP in practice reduces to a CP vs AP
   choice.


PACELC: The Extension
====================================================

**PACELC** extends CAP to capture behavior during normal operation too:

- **If Partitioned (P)**: choose between **Availability (A)** and
  **Consistency (C)**.
- **Else (E)**, during normal operation: choose between **Lowered
  Latency (L)** and **loss of Consistency (C)**.

The decision tree has two branches -- one for the partition case (PA vs
PC) and one for the normal-operation case (EL vs EC) -- giving four
combinations in total.

.. list-table::
   :widths: 15 45 40
   :header-rows: 1
   :class: compact-table

   * - **Class**
     - **Meaning**
     - **Example systems**
   * - PA/EL
     - Prioritize availability and low latency over consistency
     - Cassandra, DynamoDB (internal)
   * - PA/EC
     - Availability on partition; consistency otherwise
     - MongoDB
   * - PC/EL
     - Consistency on partition; latency otherwise
     - CosmosDB
   * - PC/EC
     - Consistency at all times
     - Bigtable, HBase


6 -- Redis
====================================================


Introduction to Redis
----------------------------------------------------

**Redis** (**RE**\ mote **DI**\ ctionary **S**\ erver) is a networked,
in-memory, key/value store that can be used as a database, a cache, or
a message broker.

- Supports multiple data structures: strings, lists, hashes, sets,
  sorted sets, streams, bloom filters, HyperLogLog, and more.
- Queries can operate on the structure itself (e.g., pop from a list,
  add to a sorted set with score).
- **Schemaless** -- no tables, no column definitions.
- Works alongside another primary database (as a cache or broker) or
  as a primary database itself.
- Strong fit for fast data ingestion with strict performance
  requirements, especially when replication and efficiency matter.


Redis Workshop (Walkthrough)
----------------------------------------------------

A detailed Docker-based setup, including commands and sample data, is
in the :doc:`Redis Setup Guide <l10_redis_setup>`. This section is a
condensed preview of the commands used during the lecture.

**Install and connect** (see the setup guide for Docker steps):

.. code-block:: bash

   # If running in Docker
   docker exec -it redis redis-cli

**Create a key/value pair**:

.. code-block:: text

   SET user:1 '{"name": "Alice", "age": 25}'

**Retrieve a value**:

.. code-block:: text

   GET user:1

**Experiment with key expiry**:

.. code-block:: text

   SET tempkey "value"
   EXPIRE tempkey 10
   TTL tempkey

**Create a bloom filter (Redis Stack module)**:

.. code-block:: text

   BF.RESERVE bikes:models 0.001 1000000
   BF.ADD bikes:models "Smoky Mountain Striker"
   BF.EXISTS bikes:models "Smoky Mountain Striker"

**Advanced Redis Work** (exercises page): re-implement the Twitter-clone
above using **Redis-native types** -- lists for feeds, sets for friends,
hashes for user profiles, timeouts for ephemeral state.


Summary
====================================================

- Think of a K/V store as a **robust, distributed hashmap**.
- You gain **speed, scalability, and simplicity** -- you lose rich
  query languages and cross-item relationships.
- **Schemas do not disappear**; they move from the database to your
  application code. Pretending otherwise hurts later.
- Internals worth knowing: **LSM trees** (MemTable + SSTable +
  compaction + bloom filters), which trade slightly higher read latency
  for very fast writes.
- Distributed K/V adds **consensus** (hard) and **sharding** (easier,
  solved by rendezvous hashing in practice).
- **CAP** tells you what you give up during a partition; **PACELC**
  tells you what you give up during normal operation too.
- **Redis** is the default practical K/V store for most applications --
  pick it first unless you have a specific reason not to.

.. admonition:: Discussion to Close
   :class: hint

   - When you hear "schemaless", what do you hear?
   - Would you trust a K/V store with financial-grade invariants? Why
     or why not?
   - Where would you place Redis on the PACELC map, and how confident
     are you?
