====================================================
Exercises
====================================================

This page contains exercises for Lecture 10. Exercises 1-5 cover
**key/value stores** and **Redis**. Exercises 6-10 cover **graph
databases** and **Neo4j / Cypher**.

Exercises assume you have worked through the setup guides:

- :doc:`Redis Setup Guide <l10_redis_setup>`
- :doc:`Neo4j Setup Guide <l10_neo4j_setup>`


Part 1 -- Key/Value Stores and Redis
====================================================


.. dropdown:: Exercise 1 -- Design Keys for a Customer Domain
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice designing a **consistent naming convention** so that a
    schemaless K/V store stays navigable.

    **Requirements**

    You need to store the following information for each customer in a
    K/V store:

    - Name, email, city.
    - A list of recent orders (by order id).
    - A cached "lifetime value" number that is recomputed nightly.

    **Task**

    1. Propose a naming convention for keys. Write down 3-5 concrete
       example keys for customer ``42``.
    2. Decide which values are **plain strings**, which are **hashes**,
       which are **lists** or **sets**.
    3. Explain how you would handle a customer being renamed (the
       ``name`` field changes). Do any keys have to move?

    .. dropdown:: Solution
       :class-container: sd-border-success

       **One acceptable convention** uses ``customer:<id>:<field>`` or a
       single hash per customer:

       .. code-block:: text

          HSET customer:42 name "Ada" email "ada@example.com" city "Berlin"
          LPUSH customer:42:orders 9001 9002 9005
          SET customer:42:ltv 1234.50

       - ``customer:42`` is a **hash** because we want to update fields
         individually.
       - ``customer:42:orders`` is a **list** (order is meaningful and
         we want ``LPUSH``/``LRANGE`` semantics).
       - ``customer:42:ltv`` is a plain **string** because it is a single
         scalar re-written nightly.

       **Rename**: the identifier is ``42`` (stable), not ``name``, so
       renames are just ``HSET customer:42 name "New Name"``. If you
       keyed on name, any rename would force you to move every key --
       an important reason to prefer stable internal IDs over
       human-readable strings as keys.


.. dropdown:: Exercise 2 -- Implement a Rate-Limiter in Redis
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use Redis ``INCR`` and ``EXPIRE`` to build a fixed-window
    rate-limiter that allows at most **N** requests per **T** seconds
    per user.

    **Requirements**

    - First request in a window creates the counter and sets a TTL.
    - Each subsequent request increments the counter.
    - After the counter exceeds N, reject requests until the TTL
      expires.

    **Task**

    Write out the Redis commands you would issue, in order, for a
    ``POST /api/foo`` request made by user ``ada`` (limit = 5 per 60s).

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: text

          # On each request:
          INCR ratelimit:ada:/api/foo

          # If this is the first request (value == 1), set the TTL:
          EXPIRE ratelimit:ada:/api/foo 60 NX

          # Check the value; if > 5, reject the request.
          GET ratelimit:ada:/api/foo

       - ``INCR`` is atomic; two concurrent requests can't both "see 0".
       - ``EXPIRE ... NX`` sets the TTL only if one isn't already set,
         so the window is anchored to the first request.
       - After 60 seconds, the key disappears and the window resets.


.. dropdown:: Exercise 3 -- Leaderboard with Sorted Sets
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use a Redis **sorted set** (``ZSET``) to implement a leaderboard.

    **Task**

    Using the sample data from the Redis setup guide:

    1. Give Ada 200 more points. What command?
    2. Get the top 3 players.
    3. Get Bruno's current rank (0 = highest).
    4. Get the score of the player currently in 2nd place.

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: text

          ZINCRBY leaderboard 200 "ada"

          ZREVRANGE leaderboard 0 2 WITHSCORES

          ZREVRANK leaderboard "bruno"

          ZREVRANGE leaderboard 1 1 WITHSCORES

       Sorted sets give you O(log N) insert / update, O(log N) rank
       lookup, and O(log N + M) range retrieval. They are a near-perfect
       fit for leaderboards -- one of the strongest reasons to pick
       Redis over a generic K/V store.


.. dropdown:: Exercise 4 -- LSM Trees vs B-trees
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Choose between storage engines based on workload characteristics.

    **Scenario A**: A time-series ingestion pipeline accepting ~1M
    writes/sec, with range queries over the last 24 hours.

    **Scenario B**: An order-management system with balanced reads and
    writes, strict single-digit-millisecond read latency requirements.

    **Question**

    For each scenario, would you pick an LSM-tree store (LevelDB,
    RocksDB, Cassandra) or a B-tree store (PostgreSQL, MySQL InnoDB)?
    Justify.

    .. dropdown:: Solution
       :class-container: sd-border-success

       - **Scenario A -- LSM tree.** Sequential writes to MemTable +
         SSTable flush absorb high write throughput gracefully. Range
         queries on sorted SSTables are fast. The slightly higher read
         latency from multi-level lookups is acceptable for analytics.

       - **Scenario B -- B-tree.** B-trees keep read latency predictable
         and low. Compaction overhead in an LSM tree can introduce
         latency spikes that hurt tight p99 read SLAs. A relational
         engine with B-tree indexes (PostgreSQL) is typically the right
         answer.

       **General rule**: write-heavy & amortized-read → LSM. Balanced
       or read-heavy & latency-sensitive → B-tree.


.. dropdown:: Exercise 5 -- PACELC Classification (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Place real systems on the PACELC map.

    **Task**

    For each system, state (a) its PACELC classification and (b) **what
    that classification means for an application built on it**:

    1. Cassandra
    2. MongoDB (default configuration)
    3. CosmosDB (session / strong consistency)
    4. Google Bigtable / HBase
    5. Redis (single-primary, async replicas)

    .. dropdown:: Solution
       :class-container: sd-border-success

       - **Cassandra -- PA/EL**. Stays available during partitions and
         prefers low latency over strict consistency during normal
         operation. Applications must tolerate eventual consistency and
         handle reconciliation.

       - **MongoDB -- PA/EC**. During a partition, secondaries can serve
         stale reads (availability); during normal operation, the
         primary is strongly consistent. Applications usually target the
         primary for strong-read guarantees.

       - **CosmosDB -- PC/EL**. During a partition, prioritizes
         consistency (halts or errors out); during normal operation,
         optimizes for low latency at tunable consistency levels.

       - **Bigtable / HBase -- PC/EC**. Always chooses consistency.
         Availability suffers when a region server is partitioned.
         Suitable for workloads where correctness trumps uptime.

       - **Redis (single-primary, async replicas) -- PA/EL**.
         Primary-replica async replication means replicas can be stale
         (eventual consistency), and the system stays available as long
         as the primary is reachable. Write acknowledgment is local to
         the primary unless you enable WAIT.


Part 2 -- Graph Databases and Neo4j
====================================================


.. dropdown:: Exercise 6 -- Model a Movie Recommendation Graph
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Design a property-graph model for a movie-recommendation product.

    **Requirements**

    - Users have a ``name`` and ``age``.
    - Movies have a ``title``, ``year``, and zero or more ``genres``.
    - Users can ``RATE`` movies with a 1-5 ``stars`` property and a
      ``timestamp``.
    - Users can ``FRIEND`` each other (mutual).

    **Task**

    1. List the **node labels** and **relationship types** you would
       use.
    2. Draw (or describe) a small example: 3 users, 3 movies, a few
       ratings and friendships.
    3. Write the Cypher ``CREATE`` statements for your example.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **Labels**: ``User``, ``Movie``. **Relationships**: ``RATED``
       (directed, with ``stars`` and ``at``), ``FRIENDS_WITH``
       (directed but created in both directions to represent mutual
       friendship; or a single edge and traversed undirected).

       .. code-block:: cypher

          CREATE (alice:User   {name: "Alice", age: 30})
          CREATE (bob:User     {name: "Bob",   age: 28})
          CREATE (charlie:User {name: "Charlie", age: 34})

          CREATE (m1:Movie {title: "Arrival",    year: 2016, genres: ["Sci-Fi", "Drama"]})
          CREATE (m2:Movie {title: "The Matrix", year: 1999, genres: ["Sci-Fi", "Action"]})
          CREATE (m3:Movie {title: "Inception",  year: 2010, genres: ["Sci-Fi", "Thriller"]})

          CREATE (alice)-[:FRIENDS_WITH]->(bob)
          CREATE (bob)-[:FRIENDS_WITH]->(alice)
          CREATE (alice)-[:RATED {stars: 5, at: date("2026-04-01")}]->(m1)
          CREATE (bob)-[:RATED   {stars: 4, at: date("2026-04-02")}]->(m2)
          CREATE (charlie)-[:RATED {stars: 5, at: date("2026-04-05")}]->(m3);


.. dropdown:: Exercise 7 -- Cypher CRUD Warm-up
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice Cypher ``CREATE``, ``MATCH``, ``SET``, ``REMOVE``,
    ``DELETE``.

    **Task**

    Using the sample graph from the Neo4j setup guide:

    1. Give Chandra a new property ``age: 29``.
    2. Remove the ``city`` property from Ada.
    3. Add a new ``Person`` node for "Farouk" in "Cairo" and make him
       a friend of Emeka.
    4. Delete the friendship between Ada and Bruno (but keep both
       people).
    5. Completely remove Diana (including any relationships).

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: cypher

          // 1
          MATCH (c:Person {name: "Chandra"})
          SET c.age = 29;

          // 2
          MATCH (a:Person {name: "Ada"})
          REMOVE a.city;

          // 3
          MATCH (e:Person {name: "Emeka"})
          CREATE (e)-[:FRIENDS_WITH {since: 2026}]->(:Person {name: "Farouk", city: "Cairo"});

          // 4
          MATCH (:Person {name: "Ada"})-[r:FRIENDS_WITH]->(:Person {name: "Bruno"})
          DELETE r;

          // 5
          MATCH (d:Person {name: "Diana"})
          DETACH DELETE d;


.. dropdown:: Exercise 8 -- Shortest Path and Traversal Depth
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Use ``shortestPath`` and variable-length paths.

    **Task**

    On the sample social graph, write Cypher that:

    1. Finds the shortest path between Ada and Diana, following only
       ``FRIENDS_WITH`` edges, with a maximum depth of 5.
    2. Lists all people reachable from Ada in **exactly 2 hops** of
       ``FRIENDS_WITH``.
    3. Lists all people reachable from Ada in **1 to 3 hops** of
       ``FRIENDS_WITH``.

    .. dropdown:: Solution
       :class-container: sd-border-success

       .. code-block:: cypher

          // 1
          MATCH p = shortestPath(
            (a:Person {name: "Ada"})-[:FRIENDS_WITH*..5]-(d:Person {name: "Diana"})
          )
          RETURN p;

          // 2
          MATCH (a:Person {name: "Ada"})-[:FRIENDS_WITH*2]-(other)
          WHERE other.name <> "Ada"
          RETURN DISTINCT other.name;

          // 3
          MATCH (a:Person {name: "Ada"})-[:FRIENDS_WITH*1..3]-(other)
          WHERE other.name <> "Ada"
          RETURN DISTINCT other.name;

       **Reminder**: ``*N`` is "exactly N", ``*..N`` is "up to N",
       ``*M..N`` is "between M and N". Unbounded ``*`` is *dangerous* on
       large graphs -- always cap it.


.. dropdown:: Exercise 9 -- SQL vs Cypher for a 3-Hop Query
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Compare the effort required to express a multi-hop query in SQL
    vs Cypher.

    **Scenario**: You have a relational schema with
    ``people(id, name)`` and ``follows(follower_id, followee_id)``. You
    want everyone reachable from "Ada" in exactly 3 hops of follows.

    **Task**

    1. Write the SQL query (using 3 self-joins on ``follows``).
    2. Write the equivalent Cypher.
    3. Comment on the differences in clarity and performance
       characteristics.

    .. dropdown:: Solution
       :class-container: sd-border-success

       **SQL**:

       .. code-block:: sql

          SELECT p4.name
          FROM people p1
          JOIN follows f1 ON f1.follower_id = p1.id
          JOIN follows f2 ON f2.follower_id = f1.followee_id
          JOIN follows f3 ON f3.follower_id = f2.followee_id
          JOIN people p4  ON p4.id = f3.followee_id
          WHERE p1.name = 'Ada';

       **Cypher**:

       .. code-block:: cypher

          MATCH (:Person {name: "Ada"})-[:FOLLOWS*3]->(p)
          RETURN p.name;

       **Comparison**:

       - Cypher expresses "traverse three FOLLOWS hops" directly;
         SQL requires three explicit joins and the query grows linearly
         in the number of hops.
       - At scale, graph databases traverse via pointer chasing (often
         constant time per hop), while relational engines must join
         tables that grow with the dataset.
       - The difference matters most when hop count is variable or
         large (recommendations, fraud-ring detection).


.. dropdown:: Exercise 10 -- Choose the Right Tool (Take-Home)
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Match workload to database family.

    **Task**

    For each workload, pick **Relational**, **Document**, **Key/Value**,
    or **Graph**, and justify in 2-3 sentences.

    1. Session state for a web app (session token → user id + expiry).
    2. A product catalog with variable, rarely-changing attributes per
       product category.
    3. A bank's double-entry ledger with strict transactional
       guarantees.
    4. A fraud-detection system that searches for rings of accounts
       sharing devices, IPs, and credit cards.
    5. A real-time leaderboard for a multiplayer game (1M concurrent
       players, top-100 updates per second).
    6. A knowledge graph powering a chatbot.

    .. dropdown:: Solution
       :class-container: sd-border-success

       1. **K/V (Redis)** -- tiny, read-heavy, TTL-friendly, no cross-item
          queries needed.
       2. **Document (MongoDB)** -- flexible schema per category,
          nested attributes, whole-document reads.
       3. **Relational (PostgreSQL)** -- multi-row invariants, strong
          ACID transactions, decades of battle-tested tooling.
       4. **Graph (Neo4j)** -- the interesting query is a multi-hop
          pattern search; the problem *is* a graph problem.
       5. **K/V (Redis)** -- sorted-set leaderboards are the poster
          child for Redis; sub-millisecond latency.
       6. **Graph** -- entities and relationships are the unit of
          knowledge; traversal is the main query style. (Hybrid graph +
          vector systems are common here.)
