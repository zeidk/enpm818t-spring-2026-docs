====================================================
L10: Key/Value Stores and Graph Databases
====================================================

Overview
--------

This lecture introduces two more families of NoSQL databases: **key/value
stores** and **graph databases**. Both are extensions of our ongoing
survey of non-relational storage, but they sit at opposite ends of the
modeling spectrum.

**Key/value stores** (Part 1) reduce the database API to three operations
-- ``put``, ``get``, and ``delete`` -- and trade rich query languages for
raw speed, horizontal scalability, and operational simplicity. We cover
the basic data model, in-memory vs persistent stores, schema-less design
(and why schemas always exist implicitly), how to model data when the
store gives you no help (naming conventions, composite keys), a worked
Twitter-clone example, **LevelDB** internals (LSM trees, MemTables,
SSTables, compaction, bloom filters), distributed challenges (consensus,
**rendezvous hashing**), and **CAP** / **PACELC** trade-offs. We close
with hands-on work in **Redis**.

**Graph databases** (Part 2) go the other way: they make relationships
first-class. Data is stored as **nodes**, **edges**, and **properties**,
and the database engine is optimized for traversal rather than scanning
or aggregation. We cover the property-graph model, use cases (social
networks, recommendations, fraud detection, knowledge graphs), the
**Cypher** query language, and CRUD + analytics patterns
(friend-of-a-friend, shortest path, collaborative filtering). Hands-on
work uses **Neo4j**.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain what a key/value store is and how it differs from other NoSQL
  families (document, graph, relational).
- Describe the basic K/V API (``put``/``get``/``delete``) and recognize
  when it is (and is not) enough for your use case.
- Model application data against a K/V store using **naming conventions**
  and **composite keys**, accepting that the schema lives in application
  code.
- Explain LevelDB's **LSM tree** architecture: MemTables, SSTables,
  compaction, tombstones, and bloom filters.
- Contrast LSM trees with B-trees and pick the right one for a given
  workload (write-heavy vs read/write-balanced).
- Use **rendezvous hashing** to shard data across nodes with minimal
  movement on topology changes.
- State the **CAP** theorem and the **PACELC** extension, and place
  systems like Cassandra, MongoDB, CosmosDB, and HBase on the PACELC map.
- Perform CRUD operations in **Redis** (``SET``, ``GET``, ``EXPIRE``,
  ``TTL``, ``BF.*``) and choose appropriate Redis data types (strings,
  lists, hashes, sets, sorted sets) for common problems.
- Explain the property-graph data model: **nodes**, **labels**,
  **relationships** (with types and direction), and **properties**.
- Identify problems where a graph database outperforms relational or
  document models (many-hop traversals, recommendation, fraud patterns).
- Write **Cypher** queries for CRUD and simple analytics (shortest path,
  friend-of-a-friend, collaborative filtering) in **Neo4j**.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l10_kv_lecture
   l10_graph_lecture
   l10_redis_setup
   l10_neo4j_setup
   l10_exercises
   l10_quiz
   l10_references
   l10_cheat_sheet

Next Steps
----------

- Before next class: complete the take-home exercises on the exercises
  page. Spin up **Redis** and **Neo4j** from the setup guides and work
  through the CRUD walkthroughs.
- Optional reading: Redis data types documentation, Neo4j Cypher manual,
  and the Aphyr "Jepsen" posts for how CAP/PACELC trade-offs play out in
  real deployments.
