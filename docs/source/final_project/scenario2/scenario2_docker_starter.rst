============================================================================
Docker Compose Starter (Scenario 2)
============================================================================

.. important::

   We provide a **known-good** ``docker-compose.yml`` and ``Dockerfile``
   as the baseline for your GP3 deployment. **Start from these files**
   and adapt them to your project rather than writing from scratch --
   the grading target is a working three-database system, not a DIY
   YAML adventure.

This page explains the skeleton and how to adopt it.


What the Skeleton Gives You
----------------------------

- **Five services** wired together: ``postgres``, ``mongodb``,
  ``neo4j``, ``mongo-seed``, ``neo4j-seed``, and ``app`` (your
  Python CLI).
- **Three seed flows**: PostgreSQL's standard
  ``/docker-entrypoint-initdb.d`` pattern seeds SQL on first boot;
  a ``mongo-seed`` sidecar runs your ``mongodb/mongo_setup.js`` and
  ``mongodb/mongo_data.js``; a ``neo4j-seed`` sidecar runs
  ``neo4j/graph_setup.cypher`` and ``neo4j/graph_data.cypher``.
- **Healthchecks** on every database -- including a Neo4j check with
  a generous ``start_period`` so Compose doesn't mark it unhealthy
  during its 30-60 second first boot. The app uses
  ``depends_on: { condition: service_healthy }`` so it launches only
  after each database is actually ready.
- **Named volumes** for durability; wipe them with
  ``docker-compose down -v`` when you change your schema / graph.
- **Service-name networking**: the app connects to ``postgres:5432``,
  ``mongodb:27017``, and ``bolt://neo4j:7687`` (not ``localhost``).
- **Env-var-driven passwords** via a ``.env`` file, with sensible
  class-wide defaults if you don't override them. (Neo4j requires
  passwords of **at least 8 characters**.)


How to Adopt It
-----------------

1. Copy the two skeleton files into your project root:

   .. code-block:: text

      GP3_Healthcare_Team{X}/
      ├── docker-compose.yml        <-- copied from starter
      ├── Dockerfile                <-- copied from starter
      ├── .env                      <-- you create (see below)
      ├── .env.example              <-- template, placeholders only
      ├── requirements.txt          <-- add pymongo, neo4j, psycopg2
      ├── postgresql/
      │   ├── schema.sql            <-- from GP2
      │   └── data.sql
      ├── mongodb/
      │   ├── mongo_setup.js
      │   └── mongo_data.js
      ├── neo4j/
      │   ├── graph_setup.cypher
      │   └── graph_data.cypher
      └── src/
          └── cli/
              └── main.py

2. Create your ``.env`` using the **recommended class-wide defaults**
   (or your own -- just make sure ``README.md`` lists them). Neo4j
   passwords must be **at least 8 characters**:

   .. code-block:: text

      PG_USER=healthcare_admin
      PG_PASSWORD=enpm818t
      PG_DB=healthcare_management
      MONGO_DB=healthcare_management
      NEO4J_PASSWORD=enpm818t-neo4j

3. Make sure your ``requirements.txt`` includes the database drivers:

   .. code-block:: text

      psycopg2-binary
      pymongo
      neo4j

4. Bring it up:

   .. code-block:: bash

      docker-compose up --build

5. Watch the logs. You should see, in order:

   - ``postgres`` and ``mongodb`` reaching ``(healthy)``
   - ``mongo-seed`` loading setup and data, then **exiting**
   - ``neo4j`` reaching ``(healthy)`` after ~30-60 seconds on first run
   - ``neo4j-seed`` loading Cypher and **exiting**
   - ``app`` starting and connecting to all three databases


The docker-compose.yml
-----------------------

.. literalinclude:: starter/docker-compose.yml
   :language: yaml
   :linenos:


The Dockerfile
---------------

.. literalinclude:: starter/Dockerfile
   :language: dockerfile
   :linenos:


What You Still Need to Do
--------------------------

The starter intentionally stops short of a few things so you can make
the decisions yourself:

1. **Your application code**. The ``Dockerfile`` copies the whole
   build context and runs ``python -m src.cli.main``. Adjust the
   module path if your entrypoint lives elsewhere.
2. **Your Python drivers**. Add the ones you need to
   ``requirements.txt`` (at minimum: ``psycopg2-binary``,
   ``pymongo``, ``neo4j``).
3. **Retry logic for first-query flakes.** The healthchecks wait
   until databases are *reachable*, but first-query races can still
   happen (Mongo replica-set setup, Neo4j index builds). Wrap your
   first few queries in a short retry loop.
4. **Application-side connection strings**. Your Python code should
   read the environment variables set in the ``app`` service
   (``NEO4J_URI``, ``NEO4J_USER``, ``NEO4J_PASSWORD``, etc.),
   **not** hard-coded values.
5. **Log hygiene.** Quiet down pymongo / neo4j DEBUG logs before
   the grader tries to read your output.


Common First-Run Problems
--------------------------

.. dropdown:: "My app can't connect -- it says ``localhost: Connection refused``"
   :icon: alert
   :class-container: sd-border-warning

   You're using ``localhost`` inside the Compose network. From a
   container's point of view, ``localhost`` is itself, not the host
   machine. Use the **service name** (``postgres``, ``mongodb``,
   ``neo4j``) -- these are auto-resolved on the Compose network.

.. dropdown:: "Neo4j keeps restarting / marked unhealthy"
   :icon: alert
   :class-container: sd-border-warning

   Most common cause: your ``NEO4J_PASSWORD`` is **under 8
   characters**, so Neo4j refuses to start. Check
   ``docker-compose logs neo4j`` for
   ``InvalidArgumentException: A password must be at least 8
   characters.`` The default value in the skeleton
   (``enpm818t-neo4j``, 14 chars) is fine; make sure your ``.env``
   doesn't override it with a shorter value.

.. dropdown:: "I changed ``schema.sql`` but my changes aren't visible"
   :icon: alert
   :class-container: sd-border-warning

   ``/docker-entrypoint-initdb.d`` scripts only run on the **first
   boot of an empty data volume**. The same is true of
   ``mongo-seed`` and ``neo4j-seed`` -- they seed once and exit, and
   re-running Compose won't re-run them against populated volumes.
   To re-seed from scratch:

   .. code-block:: bash

      docker-compose down -v   # destroys all volumes
      docker-compose up --build

.. dropdown:: "``neo4j-seed`` failed -- ``graph_setup.cypher`` not found"
   :icon: alert
   :class-container: sd-border-warning

   The sidecar mounts ``./neo4j`` into ``/workdir`` read-only.
   Make sure the files actually exist at that path in your project
   root, and check that your script names match
   (``graph_setup.cypher``, ``graph_data.cypher``).

.. dropdown:: "Neo4j Browser doesn't load at http://localhost:7474"
   :icon: alert
   :class-container: sd-border-warning

   Wait longer -- it really does take 30-60 seconds on first boot.
   If you still can't reach it after two minutes, check
   ``docker-compose ps`` and ``docker-compose logs neo4j``.
