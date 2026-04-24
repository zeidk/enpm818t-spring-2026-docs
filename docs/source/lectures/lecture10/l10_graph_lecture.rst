====================================================
Part 2 -- Graph Databases
====================================================

.. raw:: latex

   \setcounter{figure}{0}


Graph Databases
====================================================

Concepts, the property-graph model, Cypher, and Neo4j in practice. Part
2 covers:

- The property-graph data model: nodes, labels, relationships,
  properties
- Use cases where graph databases outperform relational and document
  stores
- The **Cypher** query language: pattern-matching with ASCII-art
- CRUD operations and common analytics patterns (shortest path,
  friend-of-a-friend, collaborative filtering)
- Hands-on **Neo4j**

Today's arc: **what a graph database is**, **how to model connected
data**, **how to query with Cypher**, and **when to reach for a graph
engine instead of a relational or document store**.


Why This Topic Matters
----------------------------------------------------

- Many real-world domains are naturally graphs: social networks,
  recommendations, fraud rings, supply chains, knowledge graphs.
- Relational databases can model graphs via join tables, but
  **multi-hop traversals** get exponentially slower as depth grows.
- Graph databases make **relationships first-class**: traversal is the
  fast path, not the slow path.

.. admonition:: Key Insight
   :class: tip

   In a relational store, a "relationship" is something you
   **reconstruct** at query time by joining tables. In a graph store, a
   relationship is a **stored, typed, directed edge** that you can walk
   in constant time.


1 -- What Is a Graph Database?
====================================================


Definition
----------------------------------------------------

**Graph databases** store and manage data as:

- **Nodes** (entities -- discrete objects in a domain).
- **Edges / Relationships** (connections between nodes).

Some graph databases (property graphs) also attach:

- **Properties** (key/value pairs on nodes *and* edges).

Graph databases are designed for **efficient querying and analysis of
complex relationships**. Unlike relational databases -- which model
relationships *implicitly* through tables and joins -- graph databases
model data **and** its relationships **directly**.


Property-Graph Core Concepts
----------------------------------------------------

- **Nodes** describe entities (discrete objects) of a domain.
- **Nodes** can have zero or more **labels** to classify what kind of
  node they are (e.g., ``Person``, ``Manager``).
- **Relationships** describe a connection between a source node and a
  target node.
- **Relationships always have a direction** (exactly one direction).
- **Relationships must have a type** (exactly one type) to classify
  what kind of relationship they are (e.g., ``FRIENDS_WITH``,
  ``MANAGES``).
- **Nodes and relationships can both have properties** (key/value
  pairs) that further describe them.


Example: People, Cars, and Relationships
----------------------------------------------------

Consider a small domain with two people and a shared car:

- Nodes: ``(p1:Person {name: "Daniel"})``,
  ``(p2:Person {name: "Sunita"})``, ``(c:Car {brand: "Volvo"})``.
- Relationships:

  - ``(p1)-[:BROTHER_OF]->(p2)``   -- *Daniel* is the brother of Sunita
  - ``(p2)-[:SISTER_OF]->(p1)``    -- *Sunita* is the sister of Daniel
  - ``(p2)-[:OWNS {since: "2011-01-10"}]->(c)``
  - ``(p1)-[:DRIVES {since: "2013-03-15"}]->(c)``
  - ``(p2)-[:DRIVES {since: "2011-01-10"}]->(c)``

The same data in RDF or a relational schema would require a network of
join tables, triples, or blank nodes. In a property graph, it reads
like the English sentence it represents.


Graph Use Cases
----------------------------------------------------

- **Social networks**: representing and analyzing relationships between
  users; perfect for social platforms.
- **Recommendation systems**: model user preferences and item attributes
  for personalized recommendations.
- **Fraud detection**: identify suspicious patterns (e.g., rings of
  accounts sharing devices or IPs).
- **Knowledge graphs**: structured representation of knowledge for AI
  and search applications.
- **Supply chain management**: visualize and manage the flow of goods
  and information through supply chains.


Reflection and Discussion
----------------------------------------------------

.. admonition:: Class Discussion
   :class: hint

   - **Data modeling**: what are the unique considerations for data
     modeling in graph (and column-family) databases compared to
     document or relational stores?
   - **Performance**: what performance implications follow from making
     relationships explicit in storage, rather than reconstructing them
     with joins at query time?


2 -- The Cypher Query Language
====================================================


About Cypher
----------------------------------------------------

There are multiple graph query languages (Gremlin, SPARQL,
GQL/ISO-GQL). Today we focus on **Cypher**:

- Cypher is the **primary query language** for most property graphs
  today (Neo4j, Memgraph, AWS Neptune with openCypher, ...).
- Cypher mixes some SQL-ish syntax with **ASCII-art diagrams** to
  represent graph patterns.
- In practice, it looks **absolutely nothing like SQL**.


Cypher Style
----------------------------------------------------

.. list-table::
   :widths: 30 70
   :header-rows: 1
   :class: compact-table

   * - **Element**
     - **Style**
   * - Node variables
     - lowercase ``camelCase`` (e.g., ``p``, ``user``, ``friend``)
   * - Node labels
     - uppercase ``camelCase`` (e.g., ``Person``, ``Product``)
   * - Properties
     - lowercase ``camelCase`` (e.g., ``name``, ``createdAt``)
   * - Relationship types
     - ``UPPER_SNAKE_CASE`` (e.g., ``KNOWS``, ``FRIENDS_WITH``)


Cypher Nodes
----------------------------------------------------

Nodes are written in parentheses. Cypher uses a consistent set of
shortcuts for describing them:

.. list-table::
   :widths: 45 55
   :header-rows: 1
   :class: compact-table

   * - **Pattern**
     - **Meaning**
   * - ``()``
     - An empty/anonymous node (present but uninteresting for the query)
   * - ``(n)``
     - A node referred to by the variable ``n``, reusable in the query
   * - ``(p:Person)``
     - A node with a **label** (like a type/class/category)
   * - ``(p:Person:Manager)``
     - A node with multiple labels
   * - ``(p:Person {name: 'Théo', age: 22})``
     - A node with properties
   * - ``p.name``
     - A node's property accessed with **dot notation**


3 -- Cypher CRUD
====================================================


Create a Node
----------------------------------------------------

.. code-block:: cypher

   CREATE (a:Person {name: "Théo Gauchoux"})
   RETURN a

``RETURN`` is what makes a query produce output. It can return multiple
values: ``RETURN a, b``.


Create a Relationship (with Two New Nodes)
----------------------------------------------------

.. code-block:: cypher

   CREATE (a:Person)-[k:KNOWS]->(b:Person)
   RETURN a, k, b

Read carefully: parentheses are nodes, square brackets are
relationships, and arrows give direction. The pattern reads like the
graph it describes.


Match All Nodes
----------------------------------------------------

.. code-block:: cypher

   MATCH (n)
   RETURN n

.. warning::

   On a large database, ``MATCH (n) RETURN n`` is the graph-database
   equivalent of ``SELECT * FROM orders`` with no ``LIMIT``. Always
   add a ``LIMIT`` for exploration.


Match by Label
----------------------------------------------------

.. code-block:: cypher

   MATCH (a:Person)
   RETURN a


Match by Label and Property
----------------------------------------------------

.. code-block:: cypher

   MATCH (a:Person {name: "Théo Gauchoux"})
   RETURN a


Match by Relationship (Undirected)
----------------------------------------------------

.. code-block:: cypher

   MATCH (a)-[:KNOWS]-(b)
   RETURN a, b

Dashes with no arrow means "traverse this relationship in either
direction".


Match by Relationship (Directed)
----------------------------------------------------

.. code-block:: cypher

   MATCH (a)-[:MANAGES]->(b)
   RETURN a, b


Match with a ``WHERE`` Clause
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person {name: "Théo Gauchoux"})-[s:LIVES_IN]->(city:City)
   WHERE s.since = 2015
   RETURN p, city


Update: Replace All Properties of a Node
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person)
   WHERE p.name = "Théo Gauchoux"
   SET p = {name: "Michel", age: 23}


Update: Add a New Property
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person)
   WHERE p.name = "Théo Gauchoux"
   SET p += {studies: "IT Engineering"}


Update: Add a Label
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person)
   WHERE p.name = "Théo Gauchoux"
   SET p:Internship


Delete a Node (with Its Relationships)
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person)-[relationship]-()
   WHERE p.name = "Théo Gauchoux"
   DELETE relationship, p

A node cannot be deleted while relationships still point to it; you
must delete the relationships first (or use ``DETACH DELETE``).


Remove a Property
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person)
   WHERE p.name = "Théo Gauchoux"
   REMOVE p.age

.. admonition:: REMOVE vs DELETE
   :class: warning

   ``REMOVE`` is for **properties and labels**; ``DELETE`` is for
   **nodes and relationships**. They are not interchangeable.


4 -- Cypher Analytics Patterns
====================================================


Friend-of-a-Friend
----------------------------------------------------

.. code-block:: cypher

   MATCH (user)-[:KNOWS]-(friend)-[:KNOWS]-(foaf)
   RETURN foaf

Two hops. In SQL, this is two self-joins on a bridge table. In Cypher,
it is just two dashes.


Shortest Path
----------------------------------------------------

.. code-block:: cypher

   MATCH path = shortestPath( (user)-[:KNOWS*..5]-(other) )
   RETURN path

- ``*..5`` means "traverse the ``KNOWS`` relationship up to 5 hops".
- ``shortestPath`` returns the shortest path up to that bound. Critical
  for mutual-friend / recommendation features.


Collaborative Filtering
----------------------------------------------------

.. code-block:: cypher

   MATCH (user)-[:PURCHASED]->(product)<-[:PURCHASED]-()-[:PURCHASED]->(otherProduct)
   RETURN otherProduct

"People who bought X also bought Y" in one pattern.


Tree Navigation
----------------------------------------------------

.. code-block:: cypher

   MATCH (root)<-[:PARENT*]-(leaf:Category)-[:ITEM]->(data:Product)
   RETURN root, leaf, data

``*`` means "zero or more hops", great for walking hierarchies of
unknown depth.


Neo4j Workshop (Walkthrough)
====================================================

A detailed Docker-based setup for Neo4j -- including sample data -- is
in the :doc:`Neo4j Setup Guide <l10_neo4j_setup>`. This section is a
condensed preview of the walkthrough.

1. Install **Neo4j** (Docker is preferred for this course; Neo4j
   Desktop or the cloud AuraDB free tier are also fine).
2. Create a database called ``socialNetwork``.
3. Create three nodes and two relationships:

   .. code-block:: cypher

      CREATE (:Person {name: "Alice", age: 30})
      CREATE (:Person {name: "Bob",   age: 28})
      CREATE (:Person {name: "Charlie", age: 34})

      MATCH (a:Person {name: "Alice"}), (b:Person {name: "Bob"})
      CREATE (a)-[:FRIENDS_WITH]->(b)

      MATCH (b:Person {name: "Bob"}), (c:Person {name: "Charlie"})
      CREATE (b)-[:FRIENDS_WITH]->(c)

4. Query all friends of Alice:

   .. code-block:: cypher

      MATCH (a:Person)-[:FRIENDS_WITH]->(b)
      WHERE a.name = "Alice"
      RETURN b.name

5. Update Charlie's age to 35:

   .. code-block:: cypher

      MATCH (c:Person {name: "Charlie"})
      SET c.age = 35

6. Delete the relationship between Alice and Bob:

   .. code-block:: cypher

      MATCH (a:Person {name: "Alice"})-[r:FRIENDS_WITH]->(b:Person {name: "Bob"})
      DELETE r

7. Find the shortest path between Alice and Charlie:

   .. code-block:: cypher

      MATCH p = shortestPath((a:Person)-[*]->(c:Person))
      WHERE a.name = "Alice" AND c.name = "Charlie"
      RETURN p

8. Visualize the graph and interpret the results in the Neo4j Browser.


Summary
====================================================

- Graph databases store **nodes**, **labeled and typed relationships**,
  and **properties** -- making connections a first-class construct.
- The property-graph model is the default today (Neo4j, Memgraph, AWS
  Neptune, Memgraph); RDF triple stores are a second branch.
- **Cypher** uses ASCII-art patterns: nodes in ``()``, relationships
  in ``[]``, direction with arrows.
- CRUD in Cypher reads like the graph it manipulates; traversals
  (shortest path, friend-of-a-friend, collaborative filtering) are the
  native fast path.
- Reach for a graph database when **relationships are the interesting
  part** of your problem, and when multi-hop queries dominate.

.. admonition:: Discussion to Close
   :class: hint

   - What does your existing application look like if you re-model it
     as a graph? What queries become easier? What becomes harder?
   - Which is more dangerous: modeling a graph in a relational store,
     or modeling a relational workload in a graph store?
