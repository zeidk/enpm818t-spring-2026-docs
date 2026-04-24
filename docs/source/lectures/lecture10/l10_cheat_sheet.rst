====================================================
Cheat Sheet
====================================================

A condensed reference covering Lecture 10: **Key/Value Stores** (Redis,
LevelDB internals, CAP / PACELC, rendezvous hashing) and **Graph
Databases** (property-graph model, Cypher CRUD and analytics).

----

Part 1 -- Key/Value Stores
============================

K/V Data Model Quick Reference
--------------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Concept**
     - **Key Rule**
   * - Key
     - Unique identifier; usually a string or byte array
   * - Value
     - Any blob -- scalar, JSON, binary object
   * - API
     - ``Put(k, v)``, ``Get(k)``, ``Delete(k)`` -- and that's mostly it
   * - Schema
     - Database imposes none; application still has one implicitly
   * - In-memory vs persistent
     - Redis/Memcached (in-memory); LevelDB/RocksDB (persistent); DynamoDB/Cassandra (persistent + distributed)

----

K/V Modeling Patterns
-----------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Pattern**
     - **Example**
   * - Composite key with prefix
     - ``customer:42:email``, ``customer:42:city``
   * - One key per entity (JSON value)
     - ``user:1 -> '{"name":"Alice","age":25}'``
   * - Entity as a hash (field-level updates)
     - ``HSET user:1 name "Alice" age 25``
   * - Per-user list (feed, inbox)
     - ``LPUSH feed:ada message:ada:7``
   * - Per-user set (friends, tags)
     - ``SADD friends:ada bruno chandra``
   * - Leaderboard / ranked set
     - ``ZADD leaderboard 1500 "ada"``
   * - Short-lived state
     - ``SET session:abc "active"`` + ``EXPIRE session:abc 3600``

----

Common Redis Commands
-----------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Command**
     - **Purpose**
   * - ``SET k v`` / ``GET k``
     - Write / read a string value
   * - ``INCR k`` / ``DECR k``
     - Atomic counter increment / decrement
   * - ``EXPIRE k 60`` / ``TTL k``
     - Set / inspect time-to-live (seconds)
   * - ``HSET h f v`` / ``HGET h f`` / ``HGETALL h``
     - Hash field ops
   * - ``LPUSH l v`` / ``RPUSH l v`` / ``LRANGE l 0 -1``
     - List push / range read
   * - ``SADD s v`` / ``SMEMBERS s`` / ``SINTER s1 s2``
     - Set add / read / intersect
   * - ``ZADD z score m`` / ``ZREVRANGE z 0 9 WITHSCORES``
     - Sorted set add / top-N
   * - ``BF.RESERVE key err cap`` / ``BF.ADD`` / ``BF.EXISTS``
     - Bloom filter (Redis Stack)
   * - ``DEL k`` / ``FLUSHDB`` / ``FLUSHALL``
     - Delete a key / empty DB / empty all DBs

----

LSM Tree Mental Model
-----------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Component**
     - **Role**
   * - WAL
     - Write-ahead log; every write lands here first for durability
   * - MemTable
     - In-memory sorted structure (red-black tree) that absorbs writes
   * - SSTable
     - Immutable, sorted, on-disk key/value file flushed from MemTable
   * - Bloom filter
     - Per-SSTable probabilistic filter: "definitely not here" / "probably here"
   * - Compaction
     - Background merge of SSTables; removes tombstones; keeps levels tidy
   * - Tombstone
     - Marker indicating a key was deleted (removed during compaction)

**Trade-off**: LSM trees are optimized for **sequential writes** at the
cost of compaction overhead and sometimes higher read latency.

----

LSM Tree vs B-tree Choice
----------------------------

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Use LSM tree when**
     - **Use B-tree when**
   * - Writes dominate (time-series, event logs)
     - Balanced read / write or read-heavy
   * - Sequential I/O is crucial
     - Tight p99 read latency matters
   * - Compaction-driven latency is tolerable
     - Predictable per-operation latency is required
   * - Examples: LevelDB, RocksDB, Cassandra, HBase
     - Examples: PostgreSQL, MySQL InnoDB, MongoDB/WiredTiger

----

Rendezvous Hashing (for Sharding)
------------------------------------

For each item, compute ``hash(key, server_id)`` for every server, pick
the **top-K scoring servers** as owners.

- Minimal data movement when servers join or leave.
- Deterministic without a coordinator.
- Common choice in modern distributed K/V systems.

----

CAP and PACELC
----------------

.. list-table::
   :widths: 20 50 30
   :header-rows: 1
   :class: compact-table

   * - **Class**
     - **Meaning**
     - **Examples**
   * - PA/EL
     - On partition: availability; otherwise: low latency
     - Cassandra, DynamoDB
   * - PA/EC
     - On partition: availability; otherwise: consistency
     - MongoDB (default)
   * - PC/EL
     - On partition: consistency; otherwise: low latency
     - CosmosDB
   * - PC/EC
     - Always consistent
     - Bigtable, HBase

**CAP** is a partition-time framing. **PACELC** adds normal-operation
trade-offs (latency vs consistency), which matters because systems are
usually **not** partitioned.

----

Part 2 -- Graph Databases
============================

Property Graph Quick Reference
--------------------------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Concept**
     - **Key Rule**
   * - Node
     - Entity; has zero or more labels and any number of properties
   * - Label
     - Classifies a node (e.g., ``Person``, ``Product``)
   * - Relationship
     - **Always directed**, **always typed** (``:KNOWS``, ``:PURCHASED``)
   * - Properties
     - Key/value pairs on both nodes **and** relationships
   * - Query style
     - **Pattern matching** via Cypher (ASCII-art, not SQL)

----

Cypher Naming Conventions
---------------------------

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Element**
     - **Style**
   * - Node variables
     - lowercase ``camelCase`` (``p``, ``user``, ``friend``)
   * - Node labels
     - uppercase ``camelCase`` (``Person``, ``Product``)
   * - Properties
     - lowercase ``camelCase`` (``name``, ``createdAt``)
   * - Relationship types
     - ``UPPER_SNAKE_CASE`` (``FRIENDS_WITH``, ``PURCHASED``)

----

Cypher Patterns
-----------------

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Pattern**
     - **Meaning**
   * - ``()``
     - Anonymous / uninteresting node
   * - ``(n)``
     - Node referred to by ``n``
   * - ``(p:Person)``
     - Node with a label
   * - ``(p:Person {name: "Ada"})``
     - Node with label and property filter
   * - ``(a)-[:KNOWS]->(b)``
     - Directed ``KNOWS`` edge from ``a`` to ``b``
   * - ``(a)-[:KNOWS]-(b)``
     - ``KNOWS`` edge in either direction
   * - ``(a)-[:KNOWS*..5]-(b)``
     - Variable-length path of 1 to 5 ``KNOWS`` hops

----

Cypher CRUD
-------------

.. list-table::
   :widths: 25 75
   :header-rows: 1
   :class: compact-table

   * - **Operation**
     - **Example**
   * - Create node
     - ``CREATE (a:Person {name: "Ada"}) RETURN a``
   * - Create relationship
     - ``CREATE (a:Person)-[k:KNOWS]->(b:Person) RETURN a, k, b``
   * - Match all
     - ``MATCH (n) RETURN n``
   * - Match by label / property
     - ``MATCH (p:Person {name: "Ada"}) RETURN p``
   * - Update / add property
     - ``SET p.city = "Munich"`` / ``SET p += {age: 31}``
   * - Add label
     - ``SET p:Manager``
   * - Remove property / label
     - ``REMOVE p.age`` / ``REMOVE p:Manager``
   * - Delete relationship
     - ``MATCH ()-[r:KNOWS]->() DELETE r``
   * - Delete node + relationships
     - ``MATCH (n) DETACH DELETE n``

.. warning::

   ``REMOVE`` is for **properties and labels**; ``DELETE`` is for
   **nodes and relationships**. They are not interchangeable.

----

Cypher Analytics Patterns
---------------------------

.. list-table::
   :widths: 35 65
   :header-rows: 1
   :class: compact-table

   * - **Pattern**
     - **Cypher**
   * - Friend-of-a-friend
     - ``(user)-[:KNOWS]-(friend)-[:KNOWS]-(foaf)``
   * - Shortest path
     - ``shortestPath( (a)-[:KNOWS*..5]-(b) )``
   * - Collaborative filtering
     - ``(u)-[:PURCHASED]->(p)<-[:PURCHASED]-()-[:PURCHASED]->(rec)``
   * - Tree navigation
     - ``(root)<-[:PARENT*]-(leaf)-[:ITEM]->(data)``

----

Decision Checklist: Which NoSQL Family?
-----------------------------------------

.. list-table::
   :widths: 40 60
   :header-rows: 1
   :class: compact-table

   * - **Signal**
     - **Likely fit**
   * - Sub-millisecond CRUD on keyed data; caches, sessions
     - Key/Value (Redis / Memcached)
   * - Nested, variable-shape documents; aggregate reads
     - Document (MongoDB)
   * - Multi-row invariants, joins, reporting
     - Relational (PostgreSQL)
   * - Multi-hop traversals, recommendations, fraud rings
     - Graph (Neo4j / Memgraph)
   * - Very large, write-heavy logs/events
     - LSM-based K/V (Cassandra, HBase, RocksDB)
