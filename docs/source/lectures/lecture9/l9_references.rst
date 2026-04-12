References
==========


.. dropdown:: Lecture 9
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L9: Document Store Databases**

        Covers document store databases from first principles through
        production use: the document data model (BSON, nested documents,
        arrays), embedding vs referencing, CRUD operations, the
        aggregation pipeline (``$match``, ``$group``, ``$sort``,
        ``$lookup``), indexing (compound, multikey, wildcard, partial),
        ``explain()`` output, WiredTiger storage internals (journaling,
        checkpoints, compression), replication (replica sets, oplog,
        elections, read/write concerns), sharding (shard keys, chunks,
        balancers), design patterns (subset, schema versioning), and
        anti-patterns (bloated documents, unbounded arrays, over-reliance
        on ``$lookup``).

        **Before next class**: complete the take-home exercises (Exercises
        5 and 6) and experiment with MongoDB queries using the sample
        database from the setup guide.


.. dropdown:: MongoDB Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Data Modeling
            :link: https://www.mongodb.com/docs/manual/core/data-modeling-introduction/
            :class-card: sd-border-secondary

            **MongoDB -- Data Modeling Introduction**

            Official guide to document data modeling: embedding vs
            referencing, one-to-one, one-to-many, and many-to-many
            relationships, and the subset pattern.

            +++

            - Embedding vs referencing guidelines
            - Relationship patterns
            - Schema validation with JSON Schema
            - Schema versioning

        .. grid-item-card:: CRUD Operations
            :link: https://www.mongodb.com/docs/manual/crud/
            :class-card: sd-border-secondary

            **MongoDB -- CRUD Operations**

            Complete reference for insert, find, update, and delete
            operations, including update operators (``$set``, ``$inc``,
            ``$push``, ``$pull``), array updates, and bulk operations.

            +++

            - ``insertOne`` / ``insertMany``
            - ``find`` with filters and projections
            - Update operators
            - ``deleteOne`` / ``deleteMany``

        .. grid-item-card:: Aggregation Pipeline
            :link: https://www.mongodb.com/docs/manual/core/aggregation-pipeline/
            :class-card: sd-border-secondary

            **MongoDB -- Aggregation Pipeline**

            Reference for all aggregation stages including ``$match``,
            ``$group``, ``$sort``, ``$project``, ``$unwind``,
            ``$lookup``, ``$merge``, and ``$out``.

            +++

            - Pipeline stages and operators
            - SQL-to-aggregation mapping
            - Pipeline optimization
            - ``$lookup`` for joins

        .. grid-item-card:: Indexes
            :link: https://www.mongodb.com/docs/manual/indexes/
            :class-card: sd-border-secondary

            **MongoDB -- Indexes**

            Comprehensive guide to MongoDB index types: single field,
            compound, multikey, text, wildcard, partial, TTL, and
            geospatial indexes.

            +++

            - Compound index field order
            - Multikey index restrictions
            - Partial indexes with filter expressions
            - TTL indexes for automatic expiration

        .. grid-item-card:: Replication
            :link: https://www.mongodb.com/docs/manual/replication/
            :class-card: sd-border-secondary

            **MongoDB -- Replication**

            Guide to replica sets, elections, the oplog, read preference,
            read concern, and write concern.

            +++

            - Replica set architecture
            - Election protocol
            - Oplog and change streams
            - Read/write concern levels

        .. grid-item-card:: Sharding
            :link: https://www.mongodb.com/docs/manual/sharding/
            :class-card: sd-border-secondary

            **MongoDB -- Sharding**

            Documentation on sharded clusters, shard keys, chunks,
            balancers, and query routing with ``mongos``.

            +++

            - Shard key selection guidelines
            - Hashed vs ranged sharding
            - Chunk migration and balancing
            - Scatter-gather vs targeted queries


.. dropdown:: Textbook References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Silberschatz, Korth, Sudarshan
            :class-card: sd-border-secondary

            **Database System Concepts (7th Edition)**

            - Chapter 10: Big Data -- covers NoSQL systems including
              document stores, key-value stores, and column-family stores.
            - Chapter 14: Indexing -- B+ trees and hash indexes (applies
              to MongoDB's WiredTiger B-tree indexes).

        .. grid-item-card:: Sadalage & Fowler
            :class-card: sd-border-secondary

            **NoSQL Distilled (2012)**

            - Chapter 2: Aggregate Data Models -- the concept of
              aggregate-oriented databases.
            - Chapter 8: Document Databases -- MongoDB, CouchDB, and
              document modeling patterns.
            - Concise introduction to NoSQL concepts for those with a
              relational background.


.. dropdown:: Additional Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: MongoDB University
            :link: https://learn.mongodb.com/
            :class-card: sd-border-secondary

            **Free MongoDB Courses**

            Official free courses from MongoDB covering data modeling,
            aggregation, indexing, and cluster administration.

        .. grid-item-card:: MongoDB Schema Design Anti-Patterns
            :link: https://www.mongodb.com/developer/products/mongodb/schema-design-anti-pattern-summary/
            :class-card: sd-border-secondary

            **Schema Design Anti-Patterns Blog Series**

            Blog series covering common schema design mistakes:
            massive arrays, unnecessary indexes, bloated documents,
            and separating data that is accessed together.

        .. grid-item-card:: MongoDB vs PostgreSQL
            :link: https://www.mongodb.com/compare/mongodb-postgresql
            :class-card: sd-border-secondary

            **MongoDB vs PostgreSQL Comparison**

            Official comparison covering data model, query language,
            scaling, and use case alignment for both databases.

        .. grid-item-card:: RAFT Consensus Paper
            :link: https://raft.github.io/raft.pdf
            :class-card: sd-border-secondary

            **In Search of an Understandable Consensus Algorithm**

            The RAFT consensus paper. MongoDB's replica-set election
            protocol inherits from RAFT. Understanding RAFT helps
            explain elections, leader leases, and split-brain
            prevention.
