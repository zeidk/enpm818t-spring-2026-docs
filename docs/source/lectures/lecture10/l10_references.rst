References
==========


.. dropdown:: Lecture 10
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L10: Key/Value Stores and Graph Databases**

        Covers two NoSQL families that sit at opposite ends of the
        modeling spectrum. **Part 1 (Key/Value Stores)**: data model,
        ``put``/``get``/``delete`` API, in-memory vs persistent stores,
        schemaless design, worked Twitter-clone example, LevelDB
        internals (LSM tree, MemTable, SSTable, compaction, bloom
        filters), distributed challenges (consensus, rendezvous
        hashing), CAP and PACELC, and hands-on Redis. **Part 2 (Graph
        Databases)**: property-graph data model (nodes, labels,
        relationships, properties), use cases, the Cypher query
        language (CRUD + analytics patterns like shortest path,
        friend-of-a-friend, collaborative filtering), and hands-on
        Neo4j.

        **Before next class**: complete the take-home exercises and
        experiment with Redis and Neo4j using the sample data from the
        setup guides.


.. dropdown:: Redis Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Install Redis
            :link: https://redis.io/docs/latest/operate/oss_and_stack/install/
            :class-card: sd-border-secondary

            **Redis -- Install**

            Official installation guide for Redis OSS and Redis Stack
            across macOS, Linux, Windows (via WSL / Docker), and
            Kubernetes.

            +++

            - Docker quickstart
            - Redis Stack (modules: Bloom, Search, JSON, ...)
            - Native packages for Ubuntu/Debian and macOS

        .. grid-item-card:: Redis Data Types
            :link: https://redis.io/docs/latest/develop/data-types/
            :class-card: sd-border-secondary

            **Redis -- Data Types**

            Reference for every Redis type: strings, lists, hashes,
            sets, sorted sets, streams, bitmaps, HyperLogLog,
            geospatial, bloom filters.

            +++

            - When to pick each type
            - Command cheat-sheet per type
            - Memory and complexity notes

        .. grid-item-card:: Redis Commands
            :link: https://redis.io/commands/
            :class-card: sd-border-secondary

            **Redis -- Commands Reference**

            Full list of Redis commands with syntax, complexity, and
            examples.

            +++

            - Search by prefix (``BF.*``, ``ZADD``, ...)
            - Complexity for every command
            - Cluster / replication notes where relevant

        .. grid-item-card:: Redis Persistence
            :link: https://redis.io/docs/latest/operate/oss_and_stack/management/persistence/
            :class-card: sd-border-secondary

            **Redis -- Persistence**

            RDB snapshots, AOF logs, hybrid mode, and what each buys
            you when the in-memory process dies.

            +++

            - RDB vs AOF trade-offs
            - Durability vs latency
            - Recovery semantics


.. dropdown:: Neo4j / Cypher Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Neo4j Operations Manual
            :link: https://neo4j.com/docs/operations-manual/current/
            :class-card: sd-border-secondary

            **Neo4j -- Operations Manual**

            Production-oriented guide: installation, configuration,
            backup, cluster topology, authentication, monitoring.

            +++

            - Docker + Kubernetes deployment
            - Indexes and constraints
            - Security and authentication

        .. grid-item-card:: Cypher Manual
            :link: https://neo4j.com/docs/cypher-manual/current/
            :class-card: sd-border-secondary

            **Cypher -- Reference Manual**

            Complete reference for the Cypher query language used by
            Neo4j (and compatible engines).

            +++

            - Patterns, ``MATCH``, ``CREATE``, ``SET``, ``DELETE``
            - Variable-length paths and ``shortestPath``
            - Aggregations, ``WITH``, ``UNWIND``

        .. grid-item-card:: Neo4j GraphAcademy
            :link: https://graphacademy.neo4j.com/
            :class-card: sd-border-secondary

            **Free Neo4j Courses**

            Free courses on graph fundamentals, Cypher, Neo4j, and
            applied topics (recommendations, fraud, knowledge graphs).

            +++

            - Beginner: Cypher fundamentals
            - Intermediate: data modeling
            - Applied: recommendations, fraud detection

        .. grid-item-card:: GQL / openCypher
            :link: https://opencypher.org/
            :class-card: sd-border-secondary

            **openCypher / ISO GQL**

            The open specification for Cypher and its evolution into
            ISO/IEC 39075 (GQL) -- a standard graph query language.

            +++

            - Language evolution
            - Adoption across Neo4j, Memgraph, AWS Neptune
            - Relation to GQL


.. dropdown:: Textbook References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Silberschatz, Korth, Sudarshan
            :class-card: sd-border-secondary

            **Database System Concepts (7th Edition)**

            - Chapter 10: Big Data -- NoSQL categories including
              key/value stores, document stores, and graph databases.
            - Chapter 14: Indexing -- B+ trees and hash indexes
              (relevant for comparing B-trees with LSM trees).

        .. grid-item-card:: Sadalage & Fowler
            :class-card: sd-border-secondary

            **NoSQL Distilled (2012)**

            - Chapter 8: Key-Value Databases -- use cases,
              consistency, scaling.
            - Chapter 11: Graph Databases -- property graphs,
              traversal-based queries, Neo4j.
            - Short, readable introduction to NoSQL for readers with
              a relational background.

        .. grid-item-card:: Robinson, Webber, Eifrem
            :class-card: sd-border-secondary

            **Graph Databases (2nd Edition, O'Reilly)**

            - Property graph modeling, Cypher, and production
              operational concerns.
            - Available as a free e-book from Neo4j.

        .. grid-item-card:: Kleppmann
            :class-card: sd-border-secondary

            **Designing Data-Intensive Applications**

            - Chapter 3: Storage and Retrieval -- excellent treatment
              of LSM trees vs B-trees.
            - Chapter 5: Replication and Chapter 9: Consistency and
              Consensus -- foundational material for CAP/PACELC and
              distributed K/V design.


.. dropdown:: Additional Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: LevelDB (GitHub)
            :link: https://github.com/google/leveldb
            :class-card: sd-border-secondary

            **LevelDB**

            Google's embedded K/V library. The implementation is
            compact and readable -- useful reference for LSM-tree
            mechanics.

        .. grid-item-card:: RocksDB Wiki
            :link: https://github.com/facebook/rocksdb/wiki
            :class-card: sd-border-secondary

            **RocksDB**

            Facebook's LevelDB fork, widely used as the engine under
            other databases. The wiki has in-depth articles on
            compaction, bloom filters, and tuning.

        .. grid-item-card:: Cassandra Paper (Lakshman & Malik)
            :link: https://www.cs.cornell.edu/projects/ladis2009/papers/lakshman-ladis2009.pdf
            :class-card: sd-border-secondary

            **Cassandra -- A Decentralized Structured Storage System**

            The original Cassandra paper. Landmark example of a
            distributed K/V (wide-column) store with eventual
            consistency.

        .. grid-item-card:: Dynamo Paper (DeCandia et al.)
            :link: https://www.allthingsdistributed.com/files/amazon-dynamo-sosp2007.pdf
            :class-card: sd-border-secondary

            **Dynamo: Amazon's Highly Available Key-value Store**

            The Dynamo paper. Introduces ideas that shape Cassandra,
            Riak, and DynamoDB (consistent hashing, sloppy quorums,
            hinted handoff).

        .. grid-item-card:: PACELC Paper (Abadi)
            :link: https://www.cs.umd.edu/~abadi/papers/abadi-pacelc.pdf
            :class-card: sd-border-secondary

            **Consistency Tradeoffs in Modern Distributed Database
            System Design**

            Daniel Abadi's paper proposing PACELC as a richer framing
            than CAP.

        .. grid-item-card:: Aphyr "Jepsen" Analyses
            :link: https://jepsen.io/analyses
            :class-card: sd-border-secondary

            **Jepsen Database Analyses**

            Empirical analyses of how real distributed databases
            (Cassandra, Redis, MongoDB, CockroachDB, ...) behave under
            partitions and stress. Essential reading before trusting a
            vendor's CAP/PACELC claims.
