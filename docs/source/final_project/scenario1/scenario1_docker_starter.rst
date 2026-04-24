============================================================================
Docker Compose Starter (Scenario 1)
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

- **Four services** wired together: ``postgres``, ``mongodb``,
  ``redis``, and ``app`` (your Python CLI).
- **Two seed sidecars**: PostgreSQL's standard
  ``/docker-entrypoint-initdb.d`` pattern seeds SQL on first boot;
  a ``mongo-seed`` sidecar runs your ``mongodb/mongo_setup.js`` and
  ``mongodb/mongo_data.js``.
- **Healthchecks** on every database. The app uses
  ``depends_on: { condition: service_healthy }`` so it launches only
  after each database is actually ready, not just after the
  container exists.
- **Named volumes** for durability; wipe them with
  ``docker-compose down -v`` when you change your schema.
- **Service-name networking**: the app connects to ``postgres:5432``,
  ``mongodb:27017``, and ``redis:6379`` (not ``localhost``).
- **Env-var-driven passwords** via a ``.env`` file, with sensible
  class-wide defaults if you don't override them.


How to Adopt It
-----------------

1. Copy the two skeleton files into your project root:

   .. code-block:: text

      GP3_Traffic_Team{X}/
      ├── docker-compose.yml        <-- copied from starter
      ├── Dockerfile                <-- copied from starter
      ├── .env                      <-- you create (see below)
      ├── .env.example              <-- template, placeholders only
      ├── requirements.txt          <-- add pymongo, redis, psycopg2
      ├── postgresql/
      │   ├── schema.sql            <-- from GP2
      │   └── data.sql
      ├── mongodb/
      │   ├── mongo_setup.js
      │   └── mongo_data.js
      └── cli/
          └── main.py

2. Create your ``.env`` using the **recommended class-wide defaults**
   (or your own -- just make sure ``README.md`` lists them):

   .. code-block:: text

      PG_USER=enpm
      PG_PASSWORD=enpm818t
      PG_DB=traffic_management
      MONGO_DB=traffic_management

3. Make sure your ``requirements.txt`` includes the database drivers:

   .. code-block:: text

      psycopg2-binary
      pymongo
      redis

4. Bring it up:

   .. code-block:: bash

      docker-compose up --build

5. Watch the logs. You should see, in order:

   - ``postgres`` and ``mongodb`` reaching ``(healthy)``
   - ``mongo-seed`` loading setup and data, then **exiting**
   - ``redis`` reaching ``(healthy)``
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
   build context and runs ``python -m cli.main``. Adjust the
   module path if your entrypoint lives elsewhere.
2. **Your Python drivers**. Add the ones you need to
   ``requirements.txt`` (at minimum: ``psycopg2-binary``,
   ``pymongo``, ``redis``).
3. **Redis seeding.** Redis does not get seeded at container boot;
   your ``redis_setup.py`` / ``redis_operations.py`` in the app
   layer populate the structures. If you prefer a seed sidecar,
   you can add one analogous to ``mongo-seed``.
4. **Retry logic for first-query flakes.** The healthchecks wait
   until databases are *reachable*, but if your app code makes a
   query the instant it connects it can still race against Mongo's
   replica-set setup or index builds. Wrap your first few queries in
   a short retry loop.
5. **Log hygiene.** Quiet down pymongo / redis DEBUG logs before
   the grader tries to read your output.


Common First-Run Problems
--------------------------

.. dropdown:: "My app can't connect -- it says ``localhost: Connection refused``"
   :icon: alert
   :class-container: sd-border-warning

   You're using ``localhost`` inside the Compose network. From a
   container's point of view, ``localhost`` is itself, not the host
   machine. Use the **service name** (``postgres``, ``mongodb``,
   ``redis``) -- these are auto-resolved on the Compose network.

.. dropdown:: "I changed ``schema.sql`` but my changes aren't visible"
   :icon: alert
   :class-container: sd-border-warning

   ``/docker-entrypoint-initdb.d`` scripts only run on the **first
   boot of an empty data volume**. Subsequent ``docker-compose up``
   runs skip them. To re-seed:

   .. code-block:: bash

      docker-compose down -v   # destroys the volume
      docker-compose up --build

.. dropdown:: "``mongo-seed`` failed -- ``mongo_setup.js`` not found"
   :icon: alert
   :class-container: sd-border-warning

   The sidecar mounts ``./mongodb`` into ``/workdir`` read-only.
   Make sure the files actually exist at that path in your project
   root, and check that your script names match
   (``mongo_setup.js``, ``mongo_data.js``).

.. dropdown:: "Redis container exits immediately"
   :icon: alert
   :class-container: sd-border-warning

   Usually a permissions issue on the volume, or a typo in the
   ``command:`` array. Run ``docker-compose logs redis`` to see the
   actual error.
