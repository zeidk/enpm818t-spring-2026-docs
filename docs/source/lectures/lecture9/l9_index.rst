====================================================
L9: Document Store Databases
====================================================

Overview
--------

This lecture introduces **document store databases** -- a category of NoSQL
databases that store data as self-contained, semi-structured documents
(typically JSON or BSON). We begin by contrasting the document model with
the relational model, examining why application payloads that are nested,
irregular, and fast-changing can benefit from a flexible schema. The core
database used throughout the lecture is **MongoDB**, the most widely
deployed document database.

We cover the document data model in depth: BSON types, nested documents and
arrays, and the critical decision of **embedding vs referencing** related
data. The lecture then moves through MongoDB's CRUD operations, the
aggregation pipeline (with side-by-side SQL comparisons), indexing
strategies (compound, multikey, wildcard, partial), and query execution
plans. The internals section covers WiredTiger storage, journaling,
checkpoints, and crash recovery. We conclude with replication (replica
sets, elections, read/write concerns), sharding (shard keys, chunks,
balancers), common design patterns and anti-patterns, and production
operations.

Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the document model and how it differs from the relational model.
- Choose when to **embed** related data vs **reference** it in a separate collection.
- Write MongoDB CRUD operations: ``insertOne``, ``find``, ``updateOne``, ``deleteOne``.
- Build aggregation pipelines using ``$match``, ``$group``, ``$sort``, ``$lookup``.
- Design indexes for real queries: compound, multikey, wildcard, and partial indexes.
- Read ``explain()`` output and distinguish ``IXSCAN`` from ``COLLSCAN``.
- Reason about replication (replica sets, elections, oplog) and sharding (shard keys, chunks).
- Identify common anti-patterns: bloated documents, unbounded arrays, over-reliance on ``$lookup``.
- Decide when a document store is the right choice vs a relational database.

.. toctree::
   :hidden:
   :maxdepth: 2
   :titlesonly:

   l9_lecture
   l9_mongodb_setup
   l9_exercises
   l9_quiz
   l9_references
   l9_cheat_sheet

Next Steps
----------

- Before next class: complete the take-home exercises on the exercises
  page and experiment with MongoDB queries using the sample database
  from the setup guide.
- Optional reading: MongoDB official documentation on data modeling,
  indexing, and replication.
