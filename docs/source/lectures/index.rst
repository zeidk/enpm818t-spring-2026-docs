====================================================
Lectures
====================================================

Overview
--------

The lectures in ENPM818T follow a progressive structure, starting with data storage fundamentals and relational database design, then building toward NoSQL technologies and polyglot persistence architectures. Each lecture introduces new concepts through explanation, live demonstrations, and hands-on exercises. Lecture materials, including slides and demo scripts, are available on Canvas.

.. tip::

   Review the exercises after each lecture and re-run them on your own machine. Experimenting with queries and schemas is the fastest way to internalize the concepts.


Schedule
--------

.. list-table::
   :widths: 10 45 45
   :header-rows: 1
   :class: compact-table

   * - Lecture
     - Topic
     - Key Concepts
   * - L1
     - Course Introduction, Data Storage, and Setup
     - Course structure, data management lifecycle, storage hierarchies, storage architectures, PostgreSQL overview, environment setup
   * - L2
     - Conceptual Data Modeling (ER Diagrams)
     - Chen notation, entities, attributes, keys, relationships, cardinality, participation constraints, EER (specialization, generalization, aggregation, categories)
   * - L3
     - Logical Data Modeling
     - Relational model, Crow's Foot notation, 7-step ER-to-Relational mapping algorithm, foreign keys, referential integrity, lookup tables, ISA mapping strategies, categories
   * - L4-L5
     - Normalization and Denormalization
     - Functional dependencies, Armstrong's axioms, attribute closure, canonical cover, normal forms (1NF, 2NF, 3NF, BCNF), 3NF synthesis algorithm, BCNF decomposition algorithm, lossless join, dependency preservation, denormalization patterns, OLTP vs. OLAP schema design
   * - L6
     - From Logical to Physical: Implementing Your Database in PostgreSQL
     - SQL sublanguages (DDL/DML/DQL/DCL/TCL), PostgreSQL data types (NUMERIC vs. FLOAT, TEXT vs. VARCHAR, TIMESTAMPTZ), PRIMARY KEY (simple and composite), GENERATED ALWAYS AS IDENTITY vs. SERIAL, ISA shared-PK pattern, FOREIGN KEY referential actions (CASCADE, SET NULL, SET DEFAULT, RESTRICT, NO ACTION), deferrable constraints (INITIALLY DEFERRED, INITIALLY IMMEDIATE), NOT NULL, UNIQUE, NULLS NOT DISTINCT, CHECK, EXCLUDE, category exclusive-arc pattern, creation order, ALTER TABLE (safe migration pattern, NOT VALID, VALIDATE CONSTRAINT), DELETE vs. TRUNCATE vs. DROP, naming conventions, common DDL mistakes
   * - L7
     - DML, Transactions, and Python
     - ``INSERT``, ``UPDATE``, ``DELETE``, upsert with ``ON CONFLICT``, ACID properties, transaction lifecycle (``BEGIN`` / ``COMMIT`` / ``ROLLBACK``), savepoints, isolation levels, psycopg3 (connection management, parameterized queries, server-side cursors, connection pooling), loading data from CSV with Python
   * - L8
     - JOINs, Query Execution, and Indexing
     - Cartesian product, relational algebra, ``INNER`` / ``LEFT`` / ``RIGHT`` / ``FULL OUTER`` / ``CROSS`` join, self-join, semi/anti join (``EXISTS`` / ``NOT EXISTS``), ``LATERAL``, ``ON`` vs ``WHERE`` semantics, logical vs physical joins (nested loop, hash, merge), ``EXPLAIN (ANALYZE, BUFFERS)``, Big O analysis, disk/memory architecture (heap pages, ``shared_buffers``, ``work_mem``), B+ tree indexing, composite indexes, index design for joins
   * - L9
     - Document Store Databases
     - Document data model, BSON, nested documents and arrays, embedding vs referencing, MongoDB CRUD (``insertOne``, ``find``, ``updateOne``, ``deleteOne``), aggregation pipeline (``$match``, ``$group``, ``$sort``, ``$lookup``), indexing (compound, multikey, wildcard, partial, TTL), ``explain()`` output, WiredTiger storage (journaling, checkpoints, compression), replication (replica sets, oplog, elections, read/write concerns), sharding (shard keys, chunks, ``mongos``), design patterns (subset, schema versioning), anti-patterns (bloated documents, unbounded arrays)
   * - L10
     - Key/Value Stores and Graph Databases
     - K/V data model, ``put``/``get``/``delete`` API, in-memory vs persistent stores, schemaless design, composite keys, LevelDB internals (LSM trees, MemTable, SSTable, compaction, bloom filters, tombstones), LSM vs B-tree trade-offs, distributed K/V (consensus, sharding via rendezvous hashing), CAP theorem, PACELC classification (PA/EL, PA/EC, PC/EL, PC/EC), Redis (strings, hashes, lists, sets, sorted sets, ``EXPIRE`` / ``TTL``, bloom filters); property-graph model (nodes, labels, directed and typed relationships, properties), graph use cases (social networks, recommendations, fraud detection, knowledge graphs), Cypher (``MATCH``, ``CREATE``, ``SET``, ``REMOVE``, ``DELETE``, ``DETACH DELETE``, variable-length paths, ``shortestPath``), Neo4j
   * - L11
     - Optimizing SQL Queries
     - Query optimizer and query plans, ``EXPLAIN`` vs ``EXPLAIN ANALYZE``, safe diagnostics on mutating queries (``BEGIN; ... ROLLBACK;``), reading basic plans (``Seq Scan``, cost, rows, width, ``Filter``, ``Rows Removed by Filter``, planning and execution time), PostgreSQL cost constants (``seq_page_cost``, ``random_page_cost``, ``cpu_tuple_cost``, ``cpu_index_tuple_cost``, ``cpu_operator_cost``, ``parallel_setup_cost``, ``parallel_tuple_cost``), latency "magic numbers" (L1/L2 cache, RAM, SSD, disk, network), unwinding advanced plans inside-out (``Sort``, ``Merge Join``, ``GroupAggregate``, ``Limit``), join-key selection and ``Memoize``, debugging CTE / view / temp-table plans, advanced analysis (``EXPLAIN (ANALYZE, BUFFERS)`` / ``(ANALYZE, MEMORY)`` / ``(ANALYZE, SERIALIZE)``), SARGABLE vs non-SARGABLE predicates, compound-index design (leftmost-prefix, ESR rule), index drawbacks (write amplification, index size), physical join strategies (``Nested Loop``, ``Merge Join``, ``Hash Join``), how PostgreSQL chooses a join strategy (``work_mem``, indexes, selectivity, join condition type)


.. Contents
.. --------

.. toctree::
   :hidden:
   :maxdepth: 3
   :titlesonly:

   lecture1/l1_index
   lecture2/l2_index
   lecture3/l3_index
   lecture4-5/l4_5_index
   lecture6/l6_index
   lecture7/l7_index
   lecture8/l8_index
   lecture9/l9_index
   lecture10/l10_index
   lecture11/l11_index