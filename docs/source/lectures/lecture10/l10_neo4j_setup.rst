====================================================
Neo4j Setup Guide
====================================================

This guide walks you through installing Neo4j, connecting with the
``cypher-shell``, and loading a small sample graph that matches the
lecture's social-network / recommendation examples. Three installation
options are provided: **Docker** (recommended for this course), **Neo4j
Desktop**, and **Neo4j AuraDB** (cloud, free tier).


Option A: Docker (Recommended)
====================================================

Docker provides the fastest, cleanest setup. You can remove everything
with a single command, and the database is reachable from
``cypher-shell`` and from the Neo4j Browser web UI on port 7474.


Prerequisites
----------------------------------------------------

- Docker Desktop installed and running.

  - **macOS / Windows**: download from https://www.docker.com/products/docker-desktop/
  - **Linux**: install Docker Engine via your package manager.

- Verify Docker is working:

  .. code-block:: bash

     docker --version
     # Docker version 27.x.x or later


Pull and Start Neo4j
----------------------------------------------------

.. code-block:: bash

   # Pull the official Neo4j image (Community Edition)
   docker pull neo4j:5-community

   # Start a Neo4j container
   docker run -d \
     --name neo4j \
     -p 7474:7474 \
     -p 7687:7687 \
     -e NEO4J_AUTH=neo4j/enpm818t \
     -v neo4j_data:/data \
     -v neo4j_logs:/logs \
     neo4j:5-community

This command:

- Runs Neo4j in the background (``-d``).
- Maps port ``7474`` (Neo4j Browser / HTTP API) and ``7687``
  (Bolt protocol for drivers and ``cypher-shell``) to your machine.
- Sets the password to ``enpm818t`` (change it to something else if you
  prefer -- must be at least 8 characters).
- Persists the database and logs in Docker volumes so data survives
  container restarts.

.. tip::

   Visit http://localhost:7474 in your browser to open the **Neo4j
   Browser**, a web UI that runs Cypher, shows results, and visualizes
   the graph. Use ``neo4j`` / ``enpm818t`` to log in (or whatever
   password you set).


Connect with ``cypher-shell``
----------------------------------------------------

``cypher-shell`` is the command-line Cypher client that ships inside
the container:

.. code-block:: bash

   docker exec -it neo4j cypher-shell -u neo4j -p enpm818t

You should see a prompt like:

.. code-block:: text

   Connected to Neo4j using Bolt protocol version 5.x at neo4j://localhost:7687 as user neo4j.
   Type :help for a list of available commands or :exit to exit the shell.
   Bolt+routing connection established.

   neo4j@neo4j>

Sanity check:

.. code-block:: cypher

   RETURN "hello" AS greeting;


Stop and Restart
----------------------------------------------------

.. code-block:: bash

   # Stop the container
   docker stop neo4j

   # Start it again (data is preserved)
   docker start neo4j

   # Remove the container entirely
   docker rm -f neo4j

   # Remove the data volumes too (destroys all data)
   docker volume rm neo4j_data neo4j_logs


Option B: Neo4j Desktop
====================================================

`Neo4j Desktop <https://neo4j.com/docs/desktop-manual/current/installation/download-installation/>`_
is a one-click installer that bundles the server + Neo4j Browser for
macOS, Windows, and Linux.

1. Download and install Neo4j Desktop from the link above.
2. Create a new **Local DBMS**, choose a password (at least 8
   characters), and click **Start**.
3. Click **Open with Neo4j Browser** -- you are ready.

Neo4j Desktop is convenient for local development but heavier than the
Docker option. Use whichever you prefer.


Option C: Neo4j AuraDB Free (Cloud)
====================================================

`Neo4j AuraDB <https://neo4j.com/cloud/aura/>`_ has a free tier that is
useful if you cannot or do not want to run Neo4j locally.

1. Sign up for a free account.
2. Create a new **AuraDB Free** instance; Neo4j gives you a connection
   URI (``neo4j+s://...``) and an auto-generated password -- copy both.
3. Open the built-in Cypher workspace in the browser, or connect via
   ``cypher-shell``:

   .. code-block:: bash

      cypher-shell -a neo4j+s://<your-host> -u neo4j -p <your-password>


Verify Your Installation
====================================================

In Neo4j Browser or ``cypher-shell``:

.. code-block:: cypher

   CALL db.ping();
   // Should return true


Loading the Sample Graph
====================================================

The sample graph is a small social network with purchase relationships,
mirroring the lecture's examples (friend-of-a-friend, collaborative
filtering, shortest path).

Copy and paste the following Cypher into the Neo4j Browser or
``cypher-shell``:

.. code-block:: cypher

   // -- Clean slate (safe on a fresh DB) --
   MATCH (n) DETACH DELETE n;

   // -- People --
   CREATE (ada:Person     {name: "Ada",     city: "Berlin"})
   CREATE (bruno:Person   {name: "Bruno",   city: "Lisbon"})
   CREATE (chandra:Person {name: "Chandra", city: "Delhi"})
   CREATE (diana:Person   {name: "Diana",   city: "Oslo"})
   CREATE (emeka:Person   {name: "Emeka",   city: "Lagos"})

   // -- Friendships (undirected in meaning; stored as directed edges) --
   CREATE (ada)-[:FRIENDS_WITH {since: 2023}]->(bruno)
   CREATE (bruno)-[:FRIENDS_WITH {since: 2023}]->(chandra)
   CREATE (chandra)-[:FRIENDS_WITH {since: 2024}]->(diana)
   CREATE (ada)-[:FRIENDS_WITH {since: 2024}]->(emeka)

   // -- Products --
   CREATE (kb:Product   {sku: "A-42", title: "Mechanical Keyboard", price: 19.99})
   CREATE (hub:Product  {sku: "B-07", title: "USB-C Hub",           price: 7.50})
   CREATE (stand:Product {sku: "C-99", title: "Notebook Stand",     price: 12.50})
   CREATE (cam:Product  {sku: "D-15", title: "Webcam HD",           price: 34.99})
   CREATE (lamp:Product {sku: "E-33", title: "Desk Lamp",           price: 22.00})

   // -- Purchases --
   CREATE (ada)-[:PURCHASED {qty: 2, at: date("2026-03-01")}]->(kb)
   CREATE (ada)-[:PURCHASED {qty: 1, at: date("2026-03-05")}]->(stand)
   CREATE (bruno)-[:PURCHASED {qty: 1, at: date("2026-03-10")}]->(lamp)
   CREATE (chandra)-[:PURCHASED {qty: 2, at: date("2026-03-07")}]->(cam)
   CREATE (emeka)-[:PURCHASED {qty: 1, at: date("2026-03-12")}]->(kb)
   CREATE (emeka)-[:PURCHASED {qty: 1, at: date("2026-03-12")}]->(lamp)
   CREATE (diana)-[:PURCHASED {qty: 1, at: date("2026-03-14")}]->(hub)
   ;


Verify the Data
----------------------------------------------------

.. code-block:: cypher

   // Count nodes by label
   MATCH (n) RETURN labels(n) AS label, count(*) AS n;

   // Count relationships by type
   MATCH ()-[r]->() RETURN type(r) AS rel, count(*) AS n;


Create Useful Indexes and Constraints
----------------------------------------------------

Indexes are not automatic in Neo4j; add them for the properties you
actually filter by.

.. code-block:: cypher

   // Uniqueness constraint on Person.name (also creates an index)
   CREATE CONSTRAINT person_name_unique IF NOT EXISTS
   FOR (p:Person) REQUIRE p.name IS UNIQUE;

   // Uniqueness constraint on Product.sku
   CREATE CONSTRAINT product_sku_unique IF NOT EXISTS
   FOR (p:Product) REQUIRE p.sku IS UNIQUE;

   // Index on Person.city for city-based filters
   CREATE INDEX person_city_idx IF NOT EXISTS
   FOR (p:Person) ON (p.city);


Try Some Queries
====================================================

These confirm everything is working and map directly to concepts from
the lecture.


Basic Match
----------------------------------------------------

.. code-block:: cypher

   MATCH (p:Person) RETURN p.name, p.city;

   MATCH (p:Person)-[r:PURCHASED]->(prod:Product)
   RETURN p.name, prod.title, r.qty, r.at;


Friends and Friend-of-a-Friend
----------------------------------------------------

.. code-block:: cypher

   // Direct friends of Ada
   MATCH (ada:Person {name: "Ada"})-[:FRIENDS_WITH]-(friend)
   RETURN friend.name;

   // Friends of friends of Ada (not Ada herself)
   MATCH (ada:Person {name: "Ada"})-[:FRIENDS_WITH*2]-(foaf)
   WHERE foaf.name <> "Ada"
   RETURN DISTINCT foaf.name;


Shortest Path
----------------------------------------------------

.. code-block:: cypher

   MATCH p = shortestPath(
     (a:Person {name: "Ada"})-[:FRIENDS_WITH*..5]-(d:Person {name: "Diana"})
   )
   RETURN p;


Collaborative Filtering
----------------------------------------------------

.. code-block:: cypher

   // "Other people who bought the keyboard also bought..."
   MATCH (me:Person {name: "Ada"})-[:PURCHASED]->(p:Product)
         <-[:PURCHASED]-(other:Person)-[:PURCHASED]->(rec:Product)
   WHERE rec <> p
   RETURN rec.title AS recommendation, count(*) AS score
   ORDER BY score DESC;


Update and Delete
----------------------------------------------------

.. code-block:: cypher

   // Update a property
   MATCH (p:Person {name: "Ada"})
   SET p.city = "Munich";

   // Remove a property
   MATCH (p:Person {name: "Ada"})
   REMOVE p.city;

   // Delete a relationship
   MATCH (:Person {name: "Ada"})-[r:FRIENDS_WITH]->(:Person {name: "Emeka"})
   DELETE r;

   // Detach and delete a whole node
   MATCH (p:Person {name: "Emeka"})
   DETACH DELETE p;


Cleanup
====================================================

Wipe the graph (keep the database around):

.. code-block:: cypher

   MATCH (n) DETACH DELETE n;

Or, if using Docker, tear down the whole instance:

.. code-block:: bash

   docker rm -f neo4j
   docker volume rm neo4j_data neo4j_logs


Further Reading
====================================================

- Neo4j install reference: https://neo4j.com/docs/operations-manual/current/installation/
- Cypher manual: https://neo4j.com/docs/cypher-manual/current/
- Neo4j Docker image: https://hub.docker.com/_/neo4j
- Sample datasets: https://neo4j.com/graphgists/
