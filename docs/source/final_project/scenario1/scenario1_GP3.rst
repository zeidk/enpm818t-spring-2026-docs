====================================================================
Group Project 3: Complete Polyglot System (MongoDB + Redis)
====================================================================

Overview
--------

This is the **final deliverable** of the course. You will combine MongoDB
(for high-volume traffic events and flexible sensor schemas) and Redis
(for real-time state and caching) with the PostgreSQL system you built
in GP2, producing a **complete three-database polyglot architecture**
deployed via Docker Compose. You will also write a final **technical
report** documenting the system end-to-end.

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP3 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Posted**
        - Friday 04/24/2026
      * - **Due**
        - Monday 05/12/2026 at 11:59 PM
      * - **Duration**
        - ~2.5 weeks
      * - **Weight**
        - 25 points (50% of final project, includes final report)
      * - **Builds on**
        - Your PostgreSQL system from GP2
      * - **Team Size**
        - 4 students
      * - **Submission**
        - Canvas + GitHub repository link

.. admonition:: What Changed from the Original Schedule
   :class: note

   This assignment **combines the original GP3 (MongoDB) and GP4
   (Redis + complete system + report)** into a single final deliverable
   because of the compressed end-of-semester schedule. The scope has
   been trimmed so the project remains achievable in ~2.5 weeks:

   - Redis/third-DB queries and operations reduced from 6+ to 4
   - Unified cross-database CLI operations reduced from 3 to 2
   - Technical report: outline kept; no strict page limit
   - Optional presentation has been dropped

.. dropdown:: Suggested Team Work Plan (~2.5 weeks)
   :icon: clock
   :class-container: sd-border-success
   :open:

   With 4 team members, the workload is roughly **10--14 hours per
   student** over 2.5 weeks (~4--6 hours/week each). Use this table
   to plan your work and parallelize across team members.

   .. list-table::
      :header-rows: 1
      :widths: 48 12
      :class: compact-table

      * - Deliverable
        - Effort
      * - Data partitioning analysis + Decision Templates
        - 2--3 h
      * - 4 MongoDB collection schemas + index strategy
        - 3--4 h
      * - ``mongo_setup.js`` with validation
        - 2 h
      * - ``mongo_data.js`` (500+ events, 200+ sensor readings)
        - 3--4 h
      * - 6 MongoDB queries with documentation
        - 4--5 h
      * - Redis: 5 data structures + 4 operations
        - 4--5 h
      * - 2 config modules (``mongodb.py``, ``redis_config.py``)
        - 1--2 h
      * - Repository classes for MongoDB + Redis
        - 3--4 h
      * - 2 unified CLI operations (cross-database)
        - 4--6 h
      * - Docker Compose + Dockerfile (starter provided)
        - 2--3 h
      * - ``polyglot_design.pdf``
        - 4--5 h
      * - ``technical_report.pdf`` (7 sections)
        - 6--8 h
      * - README update, ``team_contributions.md``, ``.env`` files
        - 1--2 h
      * - **Total (team)**
        - **~40--55 h**

   .. tip::

      **Parallelize aggressively.** Two members can work on MongoDB
      (Parts 2--3) while the other two work on Redis (Part 4). The
      integration layer (Part 5) requires all pieces, so finish the
      database-specific work by the end of week 1. Start Docker
      early -- do not wait until the last day to containerize.

.. admonition:: What Carries Over from GP2
   :class: important

   GP3 **extends** the system you built in GP2 -- you are not starting
   from scratch. Your GP2 deliverables form the PostgreSQL layer of the
   final polyglot system:

   - **postgresql/schema.sql** and **postgresql/data.sql**: Reuse
     directly. Place them in the ``postgresql/`` directory so Docker
     Compose seeds them on first boot.
   - **postgresql/queries.sql**: Include in your submission for
     completeness; no changes required.
   - **config/**, **models/**, **repositories/**, **services/**,
     **cli/**: If your GP2 submission placed these under a ``src/``
     directory, move them to the **project root** so the folder
     structure matches the GP3 layout below and the provided
     Dockerfile (which runs ``python -m cli.main``).
   - **config/database.py**: Your existing PostgreSQL connection
     module. You will add ``mongodb.py`` and ``redis_config.py``
     alongside it.
   - **repositories/**: Extend with ``mongodb/`` and ``redis/``
     subdirectories. Move your existing PostgreSQL repositories into
     a ``postgres/`` subdirectory for organization.
   - **services/**, **cli/main.py**: Extend with MongoDB and Redis
     support. Your existing PostgreSQL menu options should continue
     to work unchanged.
   - **models/**: Keep your existing dataclasses; add new ones only
     if needed for cross-database service results.
   - **requirements.txt**: Add ``pymongo`` and ``redis`` to your
     existing dependencies.
   - **.env.example**: Add ``MONGO_*`` and ``REDIS_*`` variables
     alongside your existing ``DB_*`` variables.
   - **.env**: GP2 required ``.env`` to be in ``.gitignore``. For
     GP3 you must **commit** ``.env`` with actual values so
     I can run your system (see "Credentials for Grading"
     below).


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Recognize when document databases and key-value stores are appropriate
  vs. relational
- Design flexible document schemas with embedding and referencing
- Write MongoDB aggregation pipelines and array operations
- Design Redis data structures for real-time state and caching
- Implement cache-aside and write-through caching patterns
- Use Redis pub/sub for real-time event broadcasting
- Build a complete three-database architecture
- Deploy polyglot systems using Docker Compose
- Document complex distributed systems professionally


Part 1: Polyglot Persistence Design
------------------------------------

**Objective**: Analyze your data and decide what belongs in PostgreSQL,
MongoDB, or Redis.

.. admonition:: Task 1.1: Data Partitioning Analysis (2 points)
   :class: task

   For each data type in your traffic management system, evaluate
   whether it belongs in **PostgreSQL**, **MongoDB**, or **Redis**.
   Consider these factors:

   1. **Structure**: Fixed schema or variable?
   2. **Consistency**: Strong ACID needed or eventual consistency OK?
   3. **Relationships**: Many foreign keys or mostly independent?
   4. **Query Pattern**: Complex JOINs, hierarchical/time-range access,
      or sub-ms key lookups?
   5. **Volume**: Moderate or high write throughput?
   6. **Evolution**: Schema stable or frequently changing?
   7. **Staleness tolerance**: How fresh must reads be?

   .. list-table::
      :header-rows: 1
      :widths: 22 26 26 26
      :class: compact-table

      * - Characteristic
        - PostgreSQL
        - MongoDB
        - Redis
      * - Schema
        - Fixed, rigid
        - Flexible, variable
        - Key-addressed blobs
      * - Relationships
        - Many FKs, JOINs
        - Nested documents
        - None
      * - Consistency
        - Strong ACID
        - Eventual OK
        - Best-effort (in-mem)
      * - Volume
        - Moderate writes
        - High writes
        - Very high r/w
      * - Latency
        - ms range
        - ms range
        - sub-ms
      * - Evolution
        - Migrations
        - Schema-less
        - Ad-hoc keys

   **Decision Template** -- complete one entry for each **new** data
   type you are adding to MongoDB or Redis (e.g., traffic flow events,
   sensor readings, signal states, congestion rankings). You do not
   need to re-justify data that stays in PostgreSQL from GP2 -- a
   brief summary table listing those data types and stating "remains
   in PostgreSQL (unchanged from GP2)" is sufficient. The example
   below shows the expected depth for new data types; include your
   completed templates in ``docs/polyglot_design.pdf``.

   .. code-block:: text

      Data Type: Traffic Flow Events

      Analysis:
      1. Structure: Variable (different intersection types produce different data)
      2. Consistency: Eventual OK (analytics, not transactional)
      3. Relationships: Minimal (references intersection_id only)
      4. Query Pattern: Time-range aggregation, not JOINs
      5. Volume: High write throughput
      6. Evolution: Sensor types added frequently

      Decision: MongoDB
      Justification: High volume, flexible schema, time-series access
                     pattern, minimal relational needs

.. dropdown:: Suggested Data Assignment
   :icon: light-bulb
   :class-container: sd-border-info

   The following is a **recommended** starting point, not a mandate.
   You may follow these suggestions, adjust them, or propose a
   different partitioning -- as long as you justify every decision
   in your ``docs/polyglot_design.pdf`` using the Decision Template
   above.

   **Keep in PostgreSQL** (from GP2):

   - Intersection metadata (referenced frequently, structured)
   - Sensor configuration (structured, low-volume)
   - Maintenance schedules (ACID transactions needed)
   - Emergency routes (complex relationships)

   **Candidates for MongoDB**:

   - **Traffic flow events**: high-volume time-series measurements
   - **Sensor readings**: variable schema per sensor type (camera,
     radar, lidar)
   - **Incident reports**: embedded witness statements, flexible
     detail fields
   - **Traffic predictions**: ML model outputs, nested arrays

   **Candidates for Redis**:

   - **Current signal states**: read 100+ times/second, <10ms latency
   - **Live intersection metrics**: hashes with per-intersection
     status
   - **Congestion rankings**: sorted-set leaderboard
   - **Recent incidents queue**: list (newest-first)
   - **Traffic alert broadcasting**: pub/sub channel

   If you deviate from these suggestions, explain what you changed
   and why in your design document.

   Document your decisions and rationale in
   ``docs/polyglot_design.pdf``. This file should also include your
   MongoDB collection schemas (Part 2), Redis structure catalog
   (Part 4), and index strategy.

   **File to create**: ``docs/polyglot_design.pdf``


Part 2: MongoDB Schema Design
------------------------------

**Objective**: Design document schemas for at least 4 collections with
appropriate indexes.

.. admonition:: Task 2.1: Required Collections (2 points)
   :class: task

   Design **at least 4 collections**. Two detailed examples are
   provided below; design at least two more of your own.

   **1. traffic_flow_events**

   Real-time traffic measurements:

   .. code-block:: javascript

      {
        "_id": ObjectId(...),
        "intersection_id": 15,  // References PostgreSQL
        "timestamp": ISODate("2026-02-19T14:30:00Z"),
        "vehicle_count": 127,
        "avg_speed": 28.5,
        "congestion_level": "moderate",
        "lane_distribution": [
          {"lane": 1, "count": 42, "avg_speed": 30.2},
          {"lane": 2, "count": 45, "avg_speed": 27.8},
          {"lane": 3, "count": 40, "avg_speed": 27.5}
        ]
      }

   - **TTL Index**: Expire after 90 days
   - **Compound Index**: (intersection_id, timestamp)

   **2. sensor_readings**

   Variable schema by sensor type:

   .. code-block:: javascript

      // Camera sensor
      {
        "sensor_id": 42,
        "sensor_type": "camera",
        "timestamp": ISODate(...),
        "detection_results": [
          {"type": "car", "count": 12, "confidence": 0.94},
          {"type": "truck", "count": 3, "confidence": 0.89}
        ],
        "image_ref": "s3://traffic-images/2026/02/19/..."
      }

      // Radar sensor
      {
        "sensor_id": 43,
        "sensor_type": "radar",
        "timestamp": ISODate(...),
        "velocity_data": {
          "min_speed": 15.2,
          "max_speed": 45.8,
          "avg_speed": 28.3
        }
      }

   **3-4. Your additional collections**: Choose from
   incident_reports, traffic_predictions, congestion_patterns, or
   others that make sense for your system.

   **Schema Documentation Format** (include in
   ``docs/polyglot_design.pdf``):

   .. code-block:: text

      Collection: traffic_flow_events

      Purpose: Store real-time traffic measurements from all intersections

      Document Structure:
      - _id: ObjectId (auto-generated)
      - intersection_id: Integer (references PostgreSQL)
      - timestamp: ISODate (measurement time)
      - vehicle_count: Integer (total vehicles in period)
      - avg_speed: Double (km/h)
      - congestion_level: String (enum: low, moderate, high, severe)
      - lane_distribution: Array of subdocuments

      Embedding Rationale: Lane distribution embedded because it is
        always queried with the parent event and is bounded (max 6 lanes)

.. admonition:: Task 2.2: Index Strategy (1 point)
   :class: task

   For each collection, define appropriate indexes and document them
   in ``docs/polyglot_design.pdf``.

   **MongoDB index types to consider**:

   - **Compound Indexes**: (intersection_id, timestamp) for
     time-range queries
   - **TTL Indexes**: Auto-delete old data (e.g., 90-day retention)
   - **Text Indexes**: Full-text search on incident descriptions

   **Index Documentation Format**:

   .. code-block:: text

      Collection: traffic_flow_events

      Index 1: { intersection_id: 1, timestamp: -1 }
      Type: Compound
      Purpose: Time-range queries filtered by intersection

      Index 2: { timestamp: 1 }, { expireAfterSeconds: 7776000 }
      Type: TTL
      Purpose: Automatically remove documents older than 90 days


Part 3: MongoDB Implementation
-------------------------------

**Objective**: Set up MongoDB collections and write queries.

.. admonition:: Task 3.1: Database Setup (1 point)
   :class: task

   Create ``mongo_setup.js`` to define collections with validation
   and indexes:

   .. code-block:: javascript

      // Create database and collections
      use traffic_management;

      // Create collection with validation
      db.createCollection("traffic_flow_events", {
        validator: {
          $jsonSchema: {
            bsonType: "object",
            required: ["intersection_id", "timestamp", "vehicle_count"],
            properties: {
              intersection_id: { bsonType: "int" },
              timestamp: { bsonType: "date" },
              vehicle_count: { bsonType: "int", minimum: 0 }
            }
          }
        }
      });

      // Create indexes
      db.traffic_flow_events.createIndex(
        { intersection_id: 1, timestamp: -1 }
      );

      db.traffic_flow_events.createIndex(
        { timestamp: 1 },
        { expireAfterSeconds: 7776000 }  // 90 days
      );

   Create ``mongo_data.js`` with realistic sample data:

   - 500+ traffic flow events across multiple intersections
   - 200+ sensor readings (mix of camera, radar, lidar types)
   - Appropriate volumes for your additional collections

   **Files to create**: ``mongodb/mongo_setup.js`` and
   ``mongodb/mongo_data.js``

.. admonition:: Task 3.2: Query Development (2 points)
   :class: task

   Write **at least 6 MongoDB queries** covering the following
   categories:

   **Aggregation Pipelines (4 queries minimum)**

   Use $match, $group, $sort, $project, and other pipeline stages.

   Examples:

   - *"Calculate hourly average vehicle counts by intersection."*
   - *"Find the top 5 most congested intersections over the past week."*
   - *"Summarize sensor readings by type and day."*
   - *"Compare average speeds across intersections for the last 24 hours."*

   **Array Operations (2 queries minimum)**

   Use $unwind, $elemMatch, or array operators to analyze nested data.

   Examples:

   - *"Analyze lane-specific traffic patterns using $unwind on
     lane_distribution."*
   - *"Find events where any lane had average speed below 10 km/h."*

   **Query Documentation Format**:

   .. code-block:: javascript

      // Query #X: [Title]
      // Business Question: [Problem being solved]
      // Collections Used: [List collections]
      // Pipeline Stages: [e.g., $match, $group, $sort]

      [YOUR MONGODB QUERY]

      // Expected Output: [Description of result shape]
      // Sample Results: [First 2-3 documents]

   **File to create**: ``mongodb/mongo_queries.js``


Part 4: Redis Architecture and Implementation
----------------------------------------------

**Objective**: Design a caching strategy, select appropriate Redis data
structures, and implement them.

.. admonition:: Task 4.1: Caching Strategy and Data Structures (2 points)
   :class: task

   Evaluate each data type for Redis suitability by considering read
   frequency, latency requirements, and staleness tolerance.

   **Caching Decision Template** (use for each data type you plan to
   cache):

   .. code-block:: text

      Data: Current Signal States

      Read Frequency: 100+ times/second (every dashboard refresh)
      Write Frequency: Every 30-90 seconds (signal cycle changes)
      Latency Requirement: <10ms (real-time display)
      Staleness Tolerance: 5 seconds acceptable

      Decision: Cache in Redis
      Pattern: Write-through (update Redis on every signal change)
      TTL: 300 seconds (safety net if writer fails)
      Key Format: signal:{intersection_id}:{position}:state

   Design **at least 5 Redis data structures**, using **one of each**
   of the following types minimum. Document each structure with its
   type, key pattern, TTL, write source, read pattern, and example
   commands.

   **1. Strings** -- Simple key-value:

   .. code-block:: text

      signal:15:north:state = "green"  (TTL: 300 seconds)

   **2. Hashes** -- Objects with multiple fields:

   .. code-block:: text

      intersection:15:status = {
        vehicle_count: 127,
        avg_speed: 28.5,
        congestion_level: "moderate",
        last_update: "2026-02-19T14:30:00Z"
      }

   **3. Sorted Sets** -- Rankings:

   .. code-block:: text

      congestion:rankings = {
        "intersection:15": 85.3,  // score = congestion level
        "intersection:42": 91.5,
        "intersection:23": 72.1
      }

   **4. Lists** -- Queues:

   .. code-block:: text

      incidents:recent = [incident_id_1, incident_id_2, ...]  // FIFO queue

   **5. Pub/Sub** -- Broadcasting:

   .. code-block:: text

      channel:traffic_alerts = real-time alert broadcasting

   **Data Structure Documentation Format**:

   .. code-block:: text

      Structure #1: Signal States

      Redis Type: String
      Key Pattern: signal:{intersection_id}:{position}:state
      Value: Signal state string (green, yellow, red, flashing)
      TTL: 300 seconds

      Write Source: Signal controller updates (write-through)
      Read Pattern: Dashboard polls every 2 seconds

      Example Commands:
        SET signal:15:north:state "green" EX 300
        GET signal:15:north:state

.. dropdown:: Caching Patterns Reference
   :icon: gear
   :class-container: sd-border-primary

   **Cache-Aside Pattern** (Lazy Loading):

   1. Application checks Redis
   2. If MISS: Query PostgreSQL/MongoDB, store in Redis, return data
   3. If HIT: Return cached data

   **Write-Through Pattern**:

   1. Application writes to database
   2. Write to Redis cache immediately
   3. Return success

   **Cache Invalidation**: The hardest problem!

   - Time-based: TTL expiration (simple but may serve stale data)
   - Event-driven: Invalidate when source data changes (precise but
     complex)
   - Hybrid: TTL with manual invalidation for critical updates

   **Document your chosen pattern for each cached data type with
   justification** in ``docs/polyglot_design.pdf``.

.. admonition:: Task 4.2: Redis Setup and Operations (2 points)
   :class: task

   **redis/redis_setup.py**: initialize all data structures with
   sample data.

   **redis/redis_operations.py**: implement **at least 4 operations**
   covering the structure types you designed (write-through update,
   sorted-set ranking query, pub/sub publish, cache-aside read).

   .. note::

      You do not need a separate operation for every one of the 5
      data structures, but the 4 operations should collectively
      cover **at least 3** of the 5 structure types (e.g., strings,
      sorted sets, and pub/sub).

   .. code-block:: python

      class RedisTrafficManager:
          def update_signal_state(self, intersection_id, position, state):
              """Update signal state with TTL."""
              key = f"signal:{intersection_id}:{position}:state"
              self.redis.setex(key, 300, state)  # 5 min TTL

          def get_top_congested(self, limit=10):
              """Get most congested intersections from sorted set."""
              return self.redis.zrevrange(
                  "congestion:rankings",
                  0,
                  limit - 1,
                  withscores=True
              )

          def publish_alert(self, channel, message):
              """Broadcast traffic alert via pub/sub."""
              self.redis.publish(
                  f"channel:{channel}",
                  json.dumps(message)
              )

   **Files to create**: ``redis/redis_setup.py`` and
   ``redis/redis_operations.py``


Part 5: System Integration and Docker Deployment
-------------------------------------------------

**Objective**: Integrate all three databases in Python, add
cross-database CLI operations, and deploy the whole system with
Docker Compose.

.. admonition:: Task 5.1: Multi-Database Python Integration (2 points)
   :class: task

   **Extend your project structure**:

   .. code-block:: text

      traffic-management/
      ├── config/
      │   ├── database.py      # Existing: PostgreSQL
      │   ├── mongodb.py       # New: MongoDB connection
      │   └── redis_config.py  # New: Redis connection
      ├── repositories/
      │   ├── postgres/        # Existing from GP2
      │   ├── mongodb/         # New
      │   │   ├── traffic_events_repo.py
      │   │   └── sensor_readings_repo.py
      │   └── redis/           # New
      │       └── cache_repo.py
      ├── services/
      │   └── traffic_service.py  # Updated: three-database operations

   **Cross-Database Service Example** (combines all three):

   .. code-block:: python

      class TrafficDashboardService:
          def get_real_time_dashboard(self, intersection_id):
              # PostgreSQL: infrastructure metadata (cached)
              intersection = self._get_cached_intersection(intersection_id)

              # Redis: real-time metrics
              current_metrics = self.redis.hgetall(
                  f"intersection:{intersection_id}:status"
              )

              # MongoDB: recent history
              recent_events = self.mongo_repo.find_recent_events(
                  intersection_id, minutes=60
              )

              return {
                  "intersection": intersection,
                  "current": current_metrics,
                  "recent_history": recent_events,
              }

          def _get_cached_intersection(self, intersection_id):
              """Cache-aside pattern for PostgreSQL data."""
              cache_key = f"cache:intersection:{intersection_id}"
              cached = self.redis.get(cache_key)
              if cached:
                  return json.loads(cached)

              # Cache miss: fetch from PostgreSQL
              intersection = self.pg_repo.find_by_id(intersection_id)
              if intersection:
                  self.redis.setex(
                      cache_key, 3600, json.dumps(intersection.to_dict())
                  )
              return intersection.to_dict() if intersection else None

.. admonition:: Task 5.2: Unified CLI Operations (2 points)
   :class: task

   Add CLI menu options that demonstrate all three databases working
   together. You need **at least 2 unified operations**:

   **Operation 1: Intersection Dashboard**

   - PostgreSQL: infrastructure details
   - MongoDB: last 60 min of traffic events
   - Redis: current signal states and live metrics

   **Operation 2: Report New Incident**

   - Validate and insert into PostgreSQL
   - Add detailed report to MongoDB
   - Publish alert via Redis pub/sub
   - Add to Redis recent incidents queue

   (A third example you can use: **Top Congested Intersections**
   -- Redis rankings joined to PostgreSQL metadata. Include it if
   you have time.)

   For each operation, document which databases are involved and why:

   .. code-block:: text

      Operation: Intersection Dashboard

      Description: Real-time intersection view combining all databases

      Databases Used:
      - PostgreSQL: intersection metadata, signal config
      - MongoDB: last 60 min of traffic events, sensor readings
      - Redis: current signal states, live metrics

   Update ``cli/main.py`` to include these new options alongside your
   GP2 options and MongoDB options.

.. dropdown:: Example: Intersection Dashboard Output
   :icon: terminal
   :class-container: sd-border-info

   Below is an example of what the **Intersection Dashboard** unified
   operation might look like when all three databases are working
   together. Your exact output will differ, but this shows the
   expected level of detail.

   .. code-block:: text

      $ python -m cli.main

      ╔══════════════════════════════════════╗
      ║    Traffic Management System         ║
      ╠══════════════════════════════════════╣
      ║  1. Intersection CRUD                ║
      ║  2. Incident CRUD                    ║
      ║  3. Sensor CRUD                      ║
      ║  4. Run SQL Queries                  ║
      ║  5. MongoDB Queries                  ║
      ║  6. Intersection Dashboard           ║
      ║  7. Report New Incident              ║
      ║  0. Exit                             ║
      ╚══════════════════════════════════════╝

      Select option: 6
      Enter intersection ID: 15

      ══════════════════════════════════════════════════════════════
                  INTERSECTION DASHBOARD — ID: 15
      ══════════════════════════════════════════════════════════════

      ── PostgreSQL: Infrastructure ──────────────────────────────
        Name:           5th Ave & Main St
        Type:           4-way signalized
        Jurisdiction:   Downtown District
        Lanes:          3 per direction
        Sensors:        4 installed (2 camera, 1 radar, 1 lidar)
        Last Maintained: 2026-03-12

      ── Redis: Real-Time State ──────────────────────────────────
        Signal North:   GREEN   (TTL: 247s)
        Signal South:   GREEN   (TTL: 247s)
        Signal East:    RED     (TTL: 247s)
        Signal West:    RED     (TTL: 247s)
        Vehicle Count:  127
        Avg Speed:      28.5 km/h
        Congestion:     moderate
        Last Update:    2026-04-24 14:30:02 (3s ago)

      ── MongoDB: Recent Traffic Events (last 60 min) ───────────
        Events Found: 12

        14:30  | vehicles: 127 | avg speed: 28.5 | congestion: moderate
        14:25  | vehicles: 134 | avg speed: 26.1 | congestion: moderate
        14:20  | vehicles: 118 | avg speed: 31.2 | congestion: low
        14:15  | vehicles: 142 | avg speed: 22.8 | congestion: high
        14:10  | vehicles: 139 | avg speed: 24.0 | congestion: high
        ...    (7 more events)

      ── Redis: Congestion Ranking ───────────────────────────────
        This intersection: #8 of 50 (score: 85.3)
        Most congested:    Intersection 42 (score: 96.1)

      ══════════════════════════════════════════════════════════════

.. dropdown:: Example: Report New Incident Output
   :icon: terminal
   :class-container: sd-border-info

   Below is an example of what the **Report New Incident** unified
   operation might look like. (Assumes the user selected option
   **7** from the main menu.)

   .. code-block:: text

      Select option: 7

      ══════════════════════════════════════════════════════════════
                      REPORT NEW INCIDENT
      ══════════════════════════════════════════════════════════════

      Enter intersection ID: 15
      Incident type [accident/breakdown/hazard]: accident
      Severity [minor/moderate/major/critical]: major
      Description: Multi-vehicle collision blocking eastbound lanes

      ── PostgreSQL: Inserting incident record ───────────────────
        ✓ Incident #1247 created
          Intersection: 5th Ave & Main St (ID: 15)
          Type:         accident
          Severity:     major
          Status:       open
          Reported at:  2026-04-24 14:32:15

      ── MongoDB: Storing detailed report ────────────────────────
        ✓ Detailed incident document inserted
          Collection:   incident_reports
          Document ID:  662a1f0f3b...
          Fields:       description, responding_units, weather,
                        road_conditions, estimated_clearance

      ── Redis: Broadcasting alert ───────────────────────────────
        ✓ Alert published to channel:traffic_alerts
          Subscribers notified: 3
        ✓ Added to incidents:recent queue (position: 1 of 25)
        ✓ Congestion score updated for intersection:15
          New score: 98.7 (was 85.3)
          New ranking: #2 of 50

      ══════════════════════════════════════════════════════════════

.. dropdown:: Docker Compose Primer
   :icon: info
   :class-container: sd-border-info
   :open:

   **What is Docker Compose?**

   Docker Compose is a tool for defining and running multi-container
   applications. Instead of running ``docker run ...`` for each service
   (one for PostgreSQL, one for MongoDB, one for Redis), you write a
   single ``docker-compose.yml`` file that declares:

   - Which **image** each service uses (e.g., ``postgres:14``)
   - What **ports** are exposed to the host (e.g., ``5432``)
   - What **volumes** persist data across container restarts
   - What **environment variables** each service needs
   - **Dependencies** between services (e.g., the app waits for the
     databases before starting)

   All services defined in the file share a Docker network and can
   reach each other by **service name** (e.g., your Python app
   connects to ``postgres:5432``, not ``localhost:5432``).

   **Everyday commands**:

   .. list-table::
      :widths: 45 55
      :header-rows: 1
      :class: compact-table

      * - **Command**
        - **What it does**
      * - ``docker-compose up --build``
        - Build the app image and start all services in the
          foreground. Stops on Ctrl+C.
      * - ``docker-compose up -d``
        - Start everything detached (background).
      * - ``docker-compose down``
        - Stop and remove all containers (keeps named volumes).
      * - ``docker-compose down -v``
        - Also remove named volumes (destroys persisted data).
      * - ``docker-compose logs -f <service>``
        - Tail logs for a specific service
          (``postgres``, ``mongodb``, ``redis``, or ``app``).
      * - ``docker-compose exec <service> <cmd>``
        - Run a command inside a running service
          (e.g., ``docker-compose exec postgres psql -U postgres``).
      * - ``docker-compose ps``
        - List the running services and their status.
      * - ``docker-compose restart <service>``
        - Restart one service without touching the others.

   **Why it matters for this project**

   A single command -- ``docker-compose up --build`` -- starts
   PostgreSQL, MongoDB, Redis, and your Python app together. That is
   how polyglot systems are typically deployed in production, and it
   is what I will use to run your submission. If your
   Compose file works, your three-database system is demonstrably
   reproducible on any machine with Docker installed.

   **Minimal file anatomy**

   .. code-block:: yaml

      version: '3.8'         # Compose file format version
      services:              # One block per service
        postgres:            # Service name (also the DNS name)
          image: postgres:14 # Image to pull / build
          ports:             # Host:container port mapping
            - "5432:5432"
          volumes:           # Named volume for persistence
            - postgres_data:/var/lib/postgresql/data
          environment:       # Env vars inside the container
            POSTGRES_PASSWORD: ${PG_PASSWORD}  # From .env file
      volumes:
        postgres_data:       # Named-volume declaration

   **Gotchas to plan for**

   - When the app runs inside Compose, it connects to **service names**
     (``postgres``, ``mongodb``, ``redis``), not ``localhost``. Your
     ``.env`` should reflect this; supply both values for local dev
     and in-compose use, or just use the service names.
   - ``depends_on`` only waits for containers to **start**, not for
     the database inside to be **ready** to accept connections. Your
     app should retry connecting on startup.
   - Schema-loading files placed in
     ``./postgresql/:/docker-entrypoint-initdb.d`` run only on the
     **first** boot of an empty data volume. Run
     ``docker-compose down -v`` to re-seed.


.. admonition:: Task 5.3: Docker Compose Deployment (1 point)
   :class: task

   .. tip::

      **Do not write the compose file from scratch.** Start from the
      skeleton provided on the
      :doc:`Docker Compose Starter <scenario1_docker_starter>` page,
      which gives you all four services (``postgres``, ``mongodb``,
      ``redis``, ``app``) plus a ``mongo-seed`` sidecar, with
      healthchecks and ``service_healthy`` dependencies already wired
      up. Adapt it to your project rather than reinventing it -- the
      grading target is a working three-database system.

   For reference, a minimal structure looks like the following (the
   starter is a superset of this):

   .. code-block:: yaml

      version: '3.8'
      services:
        postgres:
          image: postgis/postgis:14-3.3
          environment:
            POSTGRES_DB: traffic_management
          volumes:
            - postgres_data:/var/lib/postgresql/data
            - ./postgresql:/docker-entrypoint-initdb.d
          ports:
            - "5432:5432"

        mongodb:
          image: mongo:6
          volumes:
            - mongo_data:/data/db
          ports:
            - "27017:27017"

        redis:
          image: redis:7-alpine
          command: redis-server --maxmemory 256mb
          volumes:
            - redis_data:/data
          ports:
            - "6379:6379"

        app:
          build: .
          depends_on:
            - postgres
            - mongodb
            - redis

   After running ``docker-compose up --build``, verify:

   1. PostgreSQL: schema loaded and data present
   2. MongoDB: collections exist and data loaded
   3. Redis: ``PING`` returns ``PONG``
   4. Application starts and connects to all three databases

   **Files to create**: ``docker-compose.yml`` and ``Dockerfile``


Part 6: Final Technical Report
-------------------------------

**Objective**: Write a technical report documenting the complete
system. **No strict page limit** -- be thorough but concise. Submit
as PDF.

.. admonition:: Task 6.1: Report Outline (8 points)
   :class: task

   Your report must include **all of the following sections**:

   **1. Executive Summary**

   System overview, three-database architecture, and key achievements.

   **2. Data Partitioning Rationale**

   Why each data type lives in its chosen database. Trade-offs
   between consistency, flexibility, and performance. Cross-database
   referencing strategy.

   **3. Architecture Overview**

   System architecture diagram, component descriptions, and data flow
   diagrams showing how data moves between PostgreSQL, MongoDB, and
   Redis. Explicitly call out which database is the source of truth
   for each data type.

   **4. Database Design Decisions**

   For each database (PostgreSQL, MongoDB, Redis): what data it
   holds, why that database was chosen over the alternatives,
   schema/structure highlights, and key design decisions (embedding
   vs. referencing, key patterns, indexes, TTLs).

   **5. Integration Architecture**

   Cross-database operations, consistency strategies, cache
   invalidation approach, and error handling when one database is
   unavailable.

   **6. Lessons Learned**

   What worked well, challenges you faced, what you would do
   differently.

   **7. Team Contributions**

   Each member's name, tasks completed, and contribution percentage
   (sum to 100%).

   **File to create**: ``docs/technical_report.pdf``


Folder Structure
----------------

.. code-block:: text

   GP3_Traffic_Team{X}/
   ├── postgresql/                 # From GP2
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── mongodb/
   │   ├── mongo_setup.js          # Collection creation with validation
   │   ├── mongo_data.js           # Sample data for all collections
   │   └── mongo_queries.js        # 6+ documented queries
   ├── redis/
   │   ├── redis_setup.py          # Initialize all data structures
   │   └── redis_operations.py     # 4+ operations across structures
   ├── config/
   │   ├── database.py             # Existing from GP2
   │   ├── mongodb.py              # New
   │   └── redis_config.py         # New
   ├── models/                       # Existing from GP2
   │   └── [entity].py
   ├── repositories/
   │   ├── postgres/               # Existing from GP2
   │   ├── mongodb/
   │   └── redis/
   ├── services/
   │   └── traffic_service.py      # Three-database operations
   ├── cli/
   │   └── main.py                 # Updated with 2+ unified operations
   ├── docs/
   │   ├── polyglot_design.pdf      # Partitioning, schemas, indexes,
   │   │                           # caching strategy, Redis structures
   │   └── technical_report.pdf
   ├── docker-compose.yml
   ├── Dockerfile
   ├── requirements.txt
   ├── .env.example              # template with placeholder values
   ├── .env                      # actual values (committed for
   │                             # grading -- see policy below)
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **docs/polyglot_design.pdf**

   The main design document. **Submit as PDF** (you may author in
   Word, Google Docs, Markdown, LaTeX -- whatever you prefer --
   then export to PDF at submission time; do not submit a raw
   ``.md`` or ``.docx``). It should contain four sections:
   (1) data partitioning analysis across PostgreSQL, MongoDB, and
   Redis with justifications for each data type;
   (2) MongoDB collection schemas with document structures,
   embedding rationale, and expected volumes;
   (3) Index strategy for MongoDB with each index's type, purpose,
   and supported queries;
   (4) Redis caching strategy and data-structure catalog
   documenting all 5+ structures with type, key pattern, TTL, write
   source, read pattern, and example commands.

   **docs/technical_report.pdf**

   The final report (see Part 6 for required sections).

   **requirements.txt**

   Updated from GP2 to include ``pymongo`` and ``redis``.

   **.env.example** (template, no real values)

   Updated to include MongoDB and Redis connection variables. Use
   obvious placeholders so it is clear this file is a template:

   .. code-block:: text

      # --- PostgreSQL ---
      DB_HOST=localhost            # use "postgres" inside Docker Compose
      DB_PORT=5432
      DB_NAME=traffic_management
      DB_USER=enpm
      DB_PASSWORD=<fill-in-your-password>

      # --- MongoDB ---
      MONGO_HOST=localhost         # use "mongodb" inside Docker Compose
      MONGO_PORT=27017
      MONGO_DB=traffic_management

      # --- Redis ---
      REDIS_HOST=localhost         # use "redis" inside Docker Compose
      REDIS_PORT=6379

   .. note::

      When your app runs **inside Docker Compose**, it must connect to
      the service names (``postgres``, ``mongodb``, ``redis``) instead
      of ``localhost``. The provided
      :doc:`Docker Compose Starter <scenario1_docker_starter>` already
      sets the correct values in the ``app`` service's ``environment:``
      block, so the ``.env`` values above are only used for **local
      development** outside of Docker.

   **.env** (actual values used by your system -- see the
   "Credentials for Grading" section below for the policy and
   recommended defaults)

   **README.md**

   Updated from GP2. Add:

   - MongoDB and Redis prerequisites.
   - Docker quick-start instructions
     (``docker-compose up --build``).
   - An architecture summary table showing which database holds
     which data.
   - A description of the unified CLI operations.

   **team_contributions.md**

   List each team member's name, tasks completed, hours contributed,
   and contribution percentage. Percentages must sum to 100%.


Credentials for Grading
-----------------------

You need passwords to run the databases locally and inside Docker
Compose. Because I have to run your submission, you must
share the passwords you used. **The policy for this assignment is:**

1. Commit **both** ``.env.example`` (template with placeholders) and
   ``.env`` (actual values you used) in your submission.
2. The ``.env`` file must contain the exact values your
   ``docker-compose.yml`` and application read at runtime, so that
   ``docker-compose up --build`` works for me with zero
   manual edits.

.. warning::

   In a real project, ``.env`` **must be in ``.gitignore``** --
   committing secrets to a repository is a security anti-pattern.
   For this course we explicitly override that practice so
   I can run your system reproducibly. Treat every value in
   your ``.env`` as disposable and **do not reuse any password that
   protects a real account, service, or personal project**.

**Recommended class-wide defaults** (use these unless you have a
specific reason not to -- fewer variations make grading faster).
These are the values the
:doc:`Docker Compose Starter <scenario1_docker_starter>` uses by
default:

.. code-block:: text

   PG_USER=enpm
   PG_PASSWORD=enpm818t
   PG_DB=traffic_management
   MONGO_DB=traffic_management

If you use different values, your ``README.md`` must list them in
a short "Credentials" section so I can verify them at a
glance.


Submission
----------

.. important::

   **Two things to submit:**

   1. **Canvas**: Upload **one** ZIP file named
      ``GP3_Traffic_Team{X}.zip`` (replace ``{X}`` with your team
      number, e.g., ``GP3_Traffic_Team03.zip``). The ZIP must
      contain the complete folder structure shown above.

   2. **GitHub**: Paste your team's **GitHub repository link** in
      the Canvas submission comments. The repository must be
      **private** with me (``zeidk``) added as a
      **collaborator**. The repository should contain the same
      code as the ZIP.

   **Due**: Monday **05/12/2026** at 11:59 PM.

   .. warning::

      Any commits pushed to the GitHub repository **after the
      deadline** will result in a **5-point deduction**.
      I will check the commit history.


.. admonition:: Submission Checklist
   :class: tip

   **Design Document**:

   - [ ] ``polyglot_design.pdf`` covers partitioning, MongoDB schemas,
     indexes, caching strategy, and Redis structures
   - [ ] Each data type has a clear PostgreSQL / MongoDB / Redis
     justification
   - [ ] 4+ MongoDB collections documented with embedding rationale
   - [ ] 5+ Redis structures documented (1 of each core type
     minimum)

   **MongoDB Files**:

   - [ ] ``mongo_setup.js`` creates all collections with validation
     and indexes
   - [ ] ``mongo_data.js`` loads realistic sample data (runs without
     errors)
   - [ ] ``mongo_queries.js`` contains 6+ queries with documentation

   **Redis Files**:

   - [ ] ``redis_setup.py`` initializes all structures with sample
     data
   - [ ] ``redis_operations.py`` implements 4+ operations covering
     at least 3 of the 5 structure types

   **Python Application**:

   - [ ] MongoDB and Redis connections configured
   - [ ] Repository classes for each database
   - [ ] 2+ unified CLI operations using all three databases

   **Deployment**:

   - [ ] ``docker-compose.yml`` starts all three databases and the
     application
   - [ ] ``Dockerfile`` builds the application correctly
   - [ ] ``docker-compose up --build`` results in a working system

   **Final Report**:

   - [ ] PDF with all seven required sections (Exec Summary, Data
     Partitioning, Architecture, Database Design Decisions, Integration,
     Lessons Learned, Team Contributions)
   - [ ] Architecture diagram included
   - [ ] All three databases discussed with rationale

   **Supporting Files**:

   - [ ] ``README.md`` updated with Docker quick-start instructions
     (and a Credentials section if non-default values are used)
   - [ ] ``requirements.txt`` updated with ``pymongo`` and ``redis``
   - [ ] ``.env.example`` updated with MongoDB and Redis variables
     (placeholders only)
   - [ ] ``.env`` committed with the **actual** values used (policy:
     see "Credentials for Grading")
   - [ ] ``team_contributions.md`` (percentages sum to 100%)


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 38 10 52
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Data Partitioning**
     - 2
     - Clear rationale for each data type across PostgreSQL,
       MongoDB, and Redis; documented decision framework
   * - **Part 2: MongoDB Schema + Indexes**
     - 3
     - 4+ collections with complete schemas and embedding rationale
       (2 pts); appropriate indexes with justification (1 pt)
   * - **Part 3: MongoDB Setup + Queries**
     - 3
     - Setup with validation + realistic data (1 pt); 6+ queries
       covering all categories with correct results (2 pts)
   * - **Part 4: Redis Architecture + Implementation**
     - 4
     - Caching decisions and 5+ data structures documented (2 pts);
       setup + 4+ operations across structure types (2 pts)
   * - **Part 5: Integration + Docker**
     - 5
     - Multi-database Python integration (2 pts); 2+ unified CLI
       operations using all three databases (2 pts); working
       Docker Compose (1 pt)
   * - **Part 6: Technical Report**
     - 8
     - All seven required sections (3 pts); architecture well-diagrammed
       and justified (2 pts); database design decisions and
       integration clearly explained (2 pts); lessons learned and
       professional quality (1 pt)
   * - **Total**
     - **25**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Treating MongoDB like SQL (many small collections with
     references instead of embedding related data)
   - No schema validation (MongoDB is flexible, not lawless)
   - Missing TTL indexes (leads to unbounded storage growth)
   - Caching everything (Redis memory is limited; be strategic)
   - No TTL on cached data (stale data served indefinitely)
   - Docker volumes not configured (data lost on container restart)
   - Hardcoded connection strings (use environment variables)
   - No cache invalidation (updating PostgreSQL but forgetting to
     invalidate Redis)
   - Pub/sub without subscribers (publishing alerts but no service
     listens)
   - Only 10 documents per collection (does not demonstrate realistic
     usage)


Tips for Success
----------------

.. tip::

   - **Start by sketching the three-database diagram**: which data
     lives where, and which service touches which database.
     Everything else follows from this.
   - **Design MongoDB schemas before coding**. Decide what to embed
     vs. reference. Think about what gets queried together.
   - **Design Redis keys before coding**. Use a consistent
     ``entity:id:field`` pattern. Think about TTLs.
   - **Implement cache-aside first** for one entity, then extend.
   - **Test with Docker early**. Do not wait until the last day to
     containerize. Build and test Docker Compose incrementally.
   - **Write the report throughout**. Capture architecture decisions
     and screenshots as you build. Do not try to reconstruct
     everything at the end.
   - **Use office hours**. Bring schema designs, Docker issues, and
     report structure for review.


Final Project Summary
---------------------

.. admonition:: Cumulative Achievement
   :class: note

   **Points**:

   - GP1: Relational Design = 10 points
   - GP2: PostgreSQL + Python = 15 points
   - GP3: Complete Polyglot System = 25 points
   - **Total**: 50 points

**Your Achievement**:

You have built a production-grade polyglot persistence system
demonstrating relational database design and normalization, complex
SQL query optimization, document databases for high-volume flexible
data, in-memory caching and pub/sub for real-time performance,
cross-database integration, CLI application development, Docker
deployment, and professional technical documentation.
