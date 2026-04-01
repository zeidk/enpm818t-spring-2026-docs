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


Contents
--------

.. toctree::
   :maxdepth: 3
   :titlesonly:

   lecture1/l1_index
   lecture2/l2_index
   lecture3/l3_index
   lecture4-5/l4_5_index
   lecture6/l6_index
   lecture7/l7_index
   lecture8/l8_index