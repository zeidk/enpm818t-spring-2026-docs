====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 10: **Key/Value Stores**
(Part 1) and **Graph Databases** (Part 2). Topics include the K/V data
model, Redis data types, LSM-tree internals, rendezvous hashing, CAP
and PACELC, the property-graph model, and Cypher.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is
     correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-18)
================================


.. admonition:: Question 1
   :class: hint

   Which of these is **not** part of the fundamental K/V API?

   A. ``Put(key, value)``

   B. ``Get(key)``

   C. ``Delete(key)``

   D. ``Join(keyA, keyB)``

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``Join`` is not part of the K/V API. K/V stores
   intentionally omit join functionality; cross-item relationships are
   the application's responsibility.


.. admonition:: Question 2
   :class: hint

   Which statement about K/V stores is most accurate?

   A. K/V stores enforce a fixed schema per collection.

   B. K/V stores are schemaless in the database, but schemas still
      exist implicitly in application code.

   C. K/V stores have no schema at any level of the system.

   D. K/V stores require a SQL-like query language.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The database does not enforce a schema, but an implicit
   schema always exists wherever the data is read or written. Pretending
   otherwise leads to bugs.


.. admonition:: Question 3
   :class: hint

   What data structure does LevelDB use internally?

   A. B+ tree

   B. Log-structured merge tree (LSM)

   C. Hash index with chaining

   D. R-tree

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- LevelDB is built on an LSM tree (MemTable → SSTable flush →
   compaction).


.. admonition:: Question 4
   :class: hint

   Which Redis data type best supports a leaderboard with fast rank
   lookups?

   A. String

   B. List

   C. Hash

   D. Sorted set

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- Sorted sets (``ZADD`` / ``ZRANGE`` / ``ZREVRANGE`` /
   ``ZRANK``) give O(log N) rank operations.


.. admonition:: Question 5
   :class: hint

   In an LSM tree, where do writes land first?

   A. On disk in a sorted SSTable

   B. In the MemTable (in-memory)

   C. In a bloom filter

   D. Directly in the highest level of sorted files

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Writes are appended to the MemTable (usually a red-black
   tree). The MemTable is flushed to disk as an SSTable once full.


.. admonition:: Question 6
   :class: hint

   What is a **bloom filter** used for in LevelDB?

   A. Persistent storage of keys

   B. Fast probabilistic "definitely not here" checks for SSTables

   C. Replication across nodes

   D. Sorting keys inside the MemTable

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Bloom filters let LevelDB skip SSTables that *probably*
   don't contain a key, reducing disk I/O on reads.


.. admonition:: Question 7
   :class: hint

   The CAP theorem says a distributed data store can guarantee at most
   how many of Consistency, Availability, and Partition tolerance
   simultaneously?

   A. One

   B. Two

   C. Three

   D. It depends on write concern

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- At most two. In practice, real networks force partition
   tolerance, reducing the choice to CP vs AP.


.. admonition:: Question 8
   :class: hint

   Under PACELC, a system that prioritizes availability during a
   partition and low latency otherwise is classified as:

   A. PC/EC

   B. PA/EC

   C. PA/EL

   D. PC/EL

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- PA/EL. Cassandra and DynamoDB are typical examples.


.. admonition:: Question 9
   :class: hint

   What is the key advantage of **rendezvous hashing** over naive
   hashing for sharding?

   A. It produces faster hashes.

   B. It adds replication.

   C. It minimizes data movement when servers join or leave.

   D. It eliminates hash collisions.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Only the data that a departing server "won" needs to move,
   and only the subset that a new server scores highest for is
   rebalanced.


.. admonition:: Question 10
   :class: hint

   Which of these is **not** a Redis data type?

   A. String

   B. Hash

   C. Tree

   D. Sorted set

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Redis has strings, lists, hashes, sets, sorted sets,
   streams, bitmaps, HyperLogLog, geospatial indexes, and (via
   modules) bloom filters, JSON documents, and vectors. "Tree" isn't a
   Redis type.


.. admonition:: Question 11
   :class: hint

   In a property graph, which of the following is **true**?

   A. Relationships are undirected by default.

   B. Relationships always have a direction and a type.

   C. Only nodes can have properties.

   D. A node may have at most one label.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Relationships are always directed and always have a type.
   Nodes and relationships can both have properties, and nodes can have
   multiple labels.


.. admonition:: Question 12
   :class: hint

   In Cypher, what does ``(p:Person {name: "Ada"})`` represent?

   A. A relationship labeled Person with a name property.

   B. A node referred to by ``p``, with label ``Person`` and property
      ``name = "Ada"``.

   C. A function call on ``Person``.

   D. A comment in the query.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Parentheses define a node. The variable ``p`` refers to the
   node, ``:Person`` is its label, and ``{name: "Ada"}`` is a property
   filter.


.. admonition:: Question 13
   :class: hint

   Which Cypher query returns all people in the graph?

   A. ``SELECT * FROM Person``

   B. ``MATCH (p:Person) RETURN p``

   C. ``FIND Person``

   D. ``GET /person``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Cypher uses pattern-matching. ``MATCH (p:Person) RETURN p``
   is the graph-database equivalent of ``SELECT * FROM person``.


.. admonition:: Question 14
   :class: hint

   In Cypher, which keyword removes a **property** from a node
   (without deleting the node)?

   A. ``DELETE``

   B. ``DETACH DELETE``

   C. ``REMOVE``

   D. ``DROP``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``REMOVE`` is for properties and labels; ``DELETE`` is for
   nodes and relationships.


.. admonition:: Question 15
   :class: hint

   Which of these workloads is the **best fit** for a graph database?

   A. Storing millions of cache entries with sub-millisecond reads.

   B. A fraud-detection system searching for rings of accounts
      sharing devices and IPs.

   C. Bulk analytics over 10TB of log data.

   D. A point-of-sale ledger requiring strict ACID guarantees.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Finding rings is a multi-hop traversal pattern, which is
   exactly where graph databases outperform relational joins.


.. admonition:: Question 16
   :class: hint

   Which Cypher fragment expresses "zero or more hops of the PARENT
   relationship"?

   A. ``-[:PARENT]->``

   B. ``-[:PARENT*]->``

   C. ``-[:PARENT..5]->``

   D. ``-[:PARENT?]->``

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- ``*`` means "variable length, zero or more hops". Always
   cap it in production.


.. admonition:: Question 17
   :class: hint

   In Redis, ``EXPIRE key 60`` does what?

   A. Sets the key's value to 60.

   B. Deletes the key after 60 milliseconds.

   C. Sets the key's time-to-live to 60 seconds.

   D. Refuses to serve reads for 60 seconds.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- TTL of 60 seconds. The key is auto-deleted once the TTL
   expires.


.. admonition:: Question 18
   :class: hint

   The main *cost* of LSM trees compared to B-trees is:

   A. Higher storage consumption in all cases.

   B. Compaction overhead and sometimes higher read latency.

   C. Lack of ordered range scans.

   D. Inability to handle more than 1 GB of data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Compaction runs in the background and consumes I/O and CPU;
   multi-level lookups can make single-point reads slower than a B-tree
   in the worst case.


----


True / False (Questions 19-28)
================================


.. admonition:: Question 19
   :class: hint

   **True or False:** Key/value stores typically support ``JOIN``
   operations natively.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- K/V stores deliberately do not support joins. If you
   need joins, reach for a relational or document store.


.. admonition:: Question 20
   :class: hint

   **True or False:** In an LSM tree, SSTables are mutable files that
   are updated in place on disk.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- SSTables are **immutable**. Changes are written to a
   new MemTable / SSTable; compaction merges old SSTables into new
   ones.


.. admonition:: Question 21
   :class: hint

   **True or False:** Every distributed K/V store must choose between
   consistency and availability during a network partition.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- That is the core content of CAP. Partitions always
   happen in the real world; pick C or A.


.. admonition:: Question 22
   :class: hint

   **True or False:** Redis is a persistent disk-first database by
   default.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Redis is **in-memory**. It can persist via RDB
   snapshots or AOF logs, but its default execution model is
   RAM-resident.


.. admonition:: Question 23
   :class: hint

   **True or False:** In Cypher, a relationship must have exactly one
   type and exactly one direction.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- Relationships are always typed and directed. (You can
   *traverse* them undirected via ``(a)-[:R]-(b)``, but they are stored
   directionally.)


.. admonition:: Question 24
   :class: hint

   **True or False:** A node in Neo4j can have more than one label.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- ``(p:Person:Manager)`` is valid; labels are set-like.


.. admonition:: Question 25
   :class: hint

   **True or False:** ``DETACH DELETE`` in Cypher deletes a node only
   if it has no incoming or outgoing relationships.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- ``DETACH DELETE`` deletes a node **along with** all its
   relationships in one step. Plain ``DELETE`` fails if relationships
   remain.


.. admonition:: Question 26
   :class: hint

   **True or False:** Rendezvous hashing rebalances the entire dataset
   whenever a new server joins the cluster.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Rendezvous hashing rebalances **only** the subset of
   keys where the new server scores highest. Minimal movement is the
   point.


.. admonition:: Question 27
   :class: hint

   **True or False:** An LSM tree can delete a key without rewriting
   existing SSTables immediately.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True** -- Deletions are recorded as **tombstones** and physically
   removed during the next compaction.


.. admonition:: Question 28
   :class: hint

   **True or False:** Graph databases are always faster than relational
   databases for every query.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False** -- Graph databases are faster for traversal-heavy,
   multi-hop queries. For aggregations over large flat tables,
   relational engines are usually faster.


----


Essay Questions (Questions 29-32)
=================================


.. admonition:: Question 29
   :class: hint

   Explain why K/V stores are often described as "schemaless" and why
   that label is misleading. Give one concrete example of a bug that
   could occur if developers truly acted as if their data had no
   schema.

.. dropdown:: Answer
   :class-container: sd-border-success

   "Schemaless" means the **database** does not enforce constraints on
   values. But any code that reads or writes data implicitly assumes
   some structure -- field names, types, value ranges. The schema
   still exists; it has just moved from the database into application
   code.

   Example: service A writes user profiles with ``age`` stored as an
   integer. Service B (deployed later) writes ``age`` as a string
   ("30"). Consumer code that computes ``age + 1`` now returns
   ``"301"`` silently. A relational database would have rejected the
   string; the K/V store happily stored both.


.. admonition:: Question 30
   :class: hint

   Describe, at a high level, the write and read paths in an LSM tree.
   What role do the MemTable, SSTables, bloom filters, and compaction
   play?

.. dropdown:: Answer
   :class-container: sd-border-success

   **Write path**: a write is appended to the WAL for durability, then
   placed into the in-memory **MemTable** (a sorted structure, often a
   red-black tree). When the MemTable is full, it is flushed to disk
   as an immutable, sorted **SSTable**.

   **Read path**: the MemTable is checked first; if the key is absent,
   the reader walks through levels of SSTables from smallest to
   largest. Each SSTable's **bloom filter** is consulted to skip files
   that definitely don't contain the key, avoiding unnecessary disk
   reads.

   **Compaction** periodically merges SSTables, removes tombstoned
   entries, and keeps the levels organized. Compaction is the price
   an LSM tree pays for its write efficiency.


.. admonition:: Question 31
   :class: hint

   A colleague proposes modeling a social-network friend graph on top
   of a K/V store. Describe two specific operations that would be
   awkward or expensive, and what graph-database primitive solves each.

.. dropdown:: Answer
   :class-container: sd-border-success

   - **Friend-of-a-friend**: in a K/V store, you must look up Ada's
     friends, then loop over that list and look up each friend's
     friends (N+1 round trips). In a graph database, the Cypher
     ``(user)-[:KNOWS]-(friend)-[:KNOWS]-(foaf)`` executes as a native
     traversal.

   - **Shortest path / connectivity**: computing the shortest path
     between two users in a K/V store requires application-side BFS
     over many round trips. Graph databases expose ``shortestPath``
     as a first-class primitive that runs inside the engine against
     pointer-like edges.

   Both cases come down to the same thing: graph engines store edges
   as traversable pointers, not as rows or values the application has
   to reconstruct.


.. admonition:: Question 32
   :class: hint

   Contrast the CAP theorem with PACELC. Why does PACELC matter
   for real-world deployments?

.. dropdown:: Answer
   :class-container: sd-border-success

   **CAP** says that in the presence of a network partition, a system
   must choose between Consistency and Availability. It is a useful
   framing but only describes behavior **during a partition**.

   **PACELC** extends this: if Partitioned, pick A or C (same as
   CAP); **Else** (during normal operation), pick between lower
   Latency (L) and stronger Consistency (C). This second branch
   matters because real systems spend most of their time **not**
   partitioned, and the latency-vs-consistency trade-off dominates
   everyday behavior. Knowing that a system is PA/EL (Cassandra) vs
   PC/EC (HBase) tells you how it feels to run against day-to-day, not
   just in the rare partition case.
