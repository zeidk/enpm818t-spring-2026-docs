====================================================
Group Project 4: Redis Integration + Complete System
====================================================

Overview
--------

Add Redis for real-time caching and state management, complete your three-database polyglot system, deploy with Docker Compose, and write a final technical report.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 2 weeks |
   **Weight**: 15 points (30% of final project, includes final report) |
   **Team Size**: 4 students

**Builds on**: Your PostgreSQL + MongoDB system from GP2 and GP3


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Design Redis data structures for real-time state and caching
- Implement cache-aside and write-through caching patterns
- Use Redis pub/sub for real-time event broadcasting
- Build a complete three-database architecture
- Deploy polyglot systems using Docker Compose
- Document complex distributed systems professionally


Part 1: Redis Architecture Design
----------------------------------

**Objective**: Design a caching strategy and select appropriate Redis data structures.

.. dropdown:: Task 1.1: Caching Strategy and Data Structures (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Evaluate each data type for Redis suitability by considering read frequency, latency requirements, and staleness tolerance.

   **Caching Decision Template** (use for each data type you plan to cache):

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

   Design **at least 5 Redis data structures** using appropriate types. Document each structure with its Redis type, key pattern, TTL, write source, and example commands.

   **Required structure types** (one of each, minimum):

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

   **File to create**: ``docs/caching_strategy.md`` (include both caching decisions and data structure catalog)

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
   - Event-driven: Invalidate when source data changes (precise but complex)
   - Hybrid: TTL with manual invalidation for critical updates

   **Document your chosen pattern for each cached data type with justification.**


Part 2: Redis Implementation
-----------------------------

**Objective**: Implement Redis setup and operations with multi-database integration.

.. dropdown:: Task 2.1: Redis Setup and Operations (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **redis_setup.py**: Initialize all data structures with sample data.

   **redis_operations.py**: Operations for each structure:

   .. code-block:: python

      class RedisTrafficManager:
          def update_signal_state(self, intersection_id, position, state):
              """Update signal state with TTL"""
              key = f"signal:{intersection_id}:{position}:state"
              self.redis.setex(key, 300, state)  # 5 min TTL

          def get_top_congested(self, limit=10):
              """Get most congested intersections from sorted set"""
              return self.redis.zrevrange(
                  "congestion:rankings",
                  0,
                  limit-1,
                  withscores=True
              )

          def publish_alert(self, channel, message):
              """Broadcast traffic alert via pub/sub"""
              self.redis.publish(
                  f"channel:{channel}",
                  json.dumps(message)
              )

   **Files to create**: ``redis/redis_setup.py`` and ``redis/redis_operations.py``

.. dropdown:: Task 2.2: Cache Integration (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Implement services combining all three databases:

   .. code-block:: python

      class TrafficDashboardService:
          def get_real_time_dashboard(self, intersection_id):
              # PostgreSQL: Infrastructure metadata (cached)
              intersection = self._get_cached_intersection(intersection_id)

              # Redis: Real-time metrics
              current_metrics = self.redis.hgetall(
                  f"intersection:{intersection_id}:status"
              )

              # MongoDB: Recent history
              recent_events = self.mongo_repo.find_recent_events(
                  intersection_id,
                  minutes=60
              )

              return {
                  "intersection": intersection,
                  "current": current_metrics,
                  "recent_history": recent_events
              }

          def _get_cached_intersection(self, intersection_id):
              """Cache-aside pattern for PostgreSQL data"""
              cache_key = f"cache:intersection:{intersection_id}"
              cached = self.redis.get(cache_key)

              if cached:
                  return json.loads(cached)

              # Cache miss: fetch from PostgreSQL
              intersection = self.pg_repo.find_by_id(intersection_id)
              if intersection:
                  self.redis.setex(
                      cache_key,
                      3600,  # 1 hour TTL
                      json.dumps(intersection.to_dict())
                  )
              return intersection.to_dict() if intersection else None


Part 3: Complete System Integration
------------------------------------

**Objective**: Build unified CLI operations using all three databases and deploy the full system with Docker Compose.

.. dropdown:: Task 3.1: Unified CLI Operations (3 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Add CLI menu options that demonstrate all three databases working together. You need at least **3 unified operations**:

   **Operation 1: Intersection Dashboard**

   - PostgreSQL: Infrastructure details
   - MongoDB: Recent traffic history
   - Redis: Real-time metrics

   **Operation 2: Top Congested Intersections**

   - Redis: Get rankings (fast)
   - PostgreSQL: Look up intersection details

   **Operation 3: Report New Incident**

   - Validate and insert into PostgreSQL
   - Add detailed report to MongoDB
   - Publish alert via Redis pub/sub
   - Add to Redis recent incidents queue

   For each operation, document which databases are involved and why:

   .. code-block:: text

      Operation: Intersection Dashboard

      Description: Real-time intersection view combining all databases

      Databases Used:
      - PostgreSQL: intersection metadata, signal config
      - MongoDB: last 60 min of traffic events, sensor readings
      - Redis: current signal states, live metrics

.. dropdown:: Task 3.2: Docker Deployment (2 points)
   :icon: gear
   :class-container: sd-border-primary

   **docker-compose.yml**:

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
   3. Redis: PING returns PONG
   4. Application starts and connects to all three databases

   **Files to create**: ``docker-compose.yml`` and ``Dockerfile``


Part 4: Final Technical Report
-------------------------------

**Objective**: Write a comprehensive technical report documenting the complete system.

.. dropdown:: Task 4.1: Report Structure (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **8 to 12 pages, submitted as PDF.**

   **1. Executive Summary** (1 page)

   System overview, three-database architecture, and key achievements.

   **2. Architecture Overview** (2 to 3 pages)

   System architecture diagram, component descriptions, and data flow diagrams showing how data moves between PostgreSQL, MongoDB, and Redis.

   **3. Database Design Decisions** (2 to 3 pages)

   For each database (PostgreSQL, MongoDB, Redis): what data it holds, why that database was chosen, schema/structure highlights, and key design decisions.

   **4. Integration Architecture** (1 to 2 pages)

   Cross-database operations, consistency strategies, cache invalidation approach, and error handling.

   **5. Lessons Learned** (1 page)

   What worked well, challenges faced, and what you would do differently.

   **6. Team Contributions** (0.5 page)

   Each member's name, tasks completed, and contribution percentage.

   **File to create**: ``docs/technical_report.pdf``


Folder Structure
----------------

.. code-block:: text

   GP4_Traffic_Team{X}/
   ├── postgresql/              # From GP2
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── mongodb/                 # From GP3
   │   ├── mongo_setup.js
   │   ├── mongo_data.js
   │   └── mongo_queries.js
   ├── redis/
   │   ├── redis_setup.py
   │   └── redis_operations.py
   ├── src/
   │   ├── config/
   │   │   ├── database.py
   │   │   ├── mongodb.py
   │   │   └── redis_config.py
   │   ├── models/
   │   ├── repositories/
   │   │   ├── postgres/
   │   │   ├── mongodb/
   │   │   └── redis/
   │   ├── services/
   │   │   └── traffic_service.py
   │   └── cli/
   │       └── main.py
   ├── docker-compose.yml
   ├── Dockerfile
   ├── requirements.txt
   ├── docs/
   │   ├── caching_strategy.md
   │   └── technical_report.pdf
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **docs/caching_strategy.md**

   Your Redis design document. Contains two sections: (1) caching decisions for each data type (using the decision template from Task 1.1), and (2) your data structure catalog documenting all 5+ Redis structures with their type, key pattern, TTL, write source, read pattern, and example commands.

   **docs/technical_report.pdf**

   The final report (8 to 12 pages) following the outline in Part 4.

   **requirements.txt**

   Updated from GP3 to include ``redis``.

   **README.md**

   Updated from GP3. Add Docker quick-start instructions (``docker-compose up --build``), an architecture summary table showing which database holds which data, and a description of the unified CLI operations.

   **team_contributions.md**

   List each team member's name, tasks completed, hours contributed, and contribution percentage. Percentages must sum to 100%.


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP4_Traffic_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP4_Traffic_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **Redis Design and Implementation**:

   - [ ] ``caching_strategy.md`` with caching decisions and 5+ data structure specs
   - [ ] ``redis_setup.py`` initializes all structures with sample data
   - [ ] ``redis_operations.py`` implements operations for each structure type
   - [ ] Cache-aside pattern implemented for PostgreSQL data
   - [ ] Pub/sub broadcasting for traffic alerts

   **System Integration**:

   - [ ] 3+ unified CLI operations using all three databases
   - [ ] Cache invalidation strategy implemented

   **Deployment**:

   - [ ] ``docker-compose.yml`` starts all three databases and the application
   - [ ] ``Dockerfile`` builds the application correctly
   - [ ] ``docker-compose up --build`` results in a working system

   **Final Report**:

   - [ ] 8 to 12 pages, submitted as PDF
   - [ ] Architecture diagram included
   - [ ] All three databases discussed with rationale
   - [ ] Lessons learned section included

   **Supporting Files**:

   - [ ] README.md with Docker quick-start instructions
   - [ ] requirements.txt with all dependencies
   - [ ] team_contributions.md


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 10 55
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Caching Strategy**
     - 2
     - Well-reasoned caching decisions (1pt); 5+ data structures with appropriate types and documentation (1pt)
   * - **Part 2: Redis Implementation**
     - 2
     - Working setup and operations (1pt); cache-aside pattern and pub/sub implemented (1pt)
   * - **Part 2: Cache Integration**
     - 2
     - Clean integration with PostgreSQL and MongoDB (1pt); cache invalidation working (1pt)
   * - **Part 3: Unified Operations**
     - 3
     - 3+ operations using all three databases (1.5pts); correct results and error handling (1.5pts)
   * - **Part 3: Deployment**
     - 2
     - Working Docker Compose (1pt); all services start and connect (1pt)
   * - **Part 4: Technical Report**
     - 4
     - Comprehensive architecture overview (1.5pts); database design decisions well-justified (1.5pt); lessons learned and professional quality (1pt)
   * - **Total**
     - **15**
     -


Optional Presentation (+4 points bonus)
-----------------------------------------

.. dropdown:: Presentation Requirements
   :icon: gear
   :class-container: sd-border-primary

   **Format**: 15-minute team presentation

   **Content**:

   1. System architecture overview (2 min)
   2. Database selection rationale (3 min)
   3. Live demonstration (5 min): show three-database operations and cross-database data flow
   4. Challenges and solutions (3 min)
   5. Q&A (2 min)

   **Grading** (+4 points possible):

   .. list-table::
      :header-rows: 1
      :widths: 50 10
      :class: compact-table

      * - Criteria
        - Points
      * - Clarity and organization
        - 1
      * - Technical depth
        - 1.5
      * - Live demo quality
        - 1
      * - Q&A responses
        - 0.5
      * - **Total Bonus**
        - **4**


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Caching everything (Redis memory is limited; be strategic)
   - No TTL on cached data (leads to stale data being served indefinitely)
   - Docker volumes not configured (data lost on container restart)
   - Hardcoded connection strings (use environment variables)
   - No cache invalidation (updating PostgreSQL but forgetting to invalidate Redis)
   - Pub/sub without subscribers (publishing alerts but no service listens)
   - Final report under 8 pages or missing required sections


Tips for Success
----------------

.. tip::

   - **Design Redis structures before coding**: Sketch key patterns on paper. Think about TTLs and access patterns.
   - **Implement cache-aside first**: Start with the simplest caching pattern for one entity, then extend.
   - **Test with Docker early**: Do not wait until the last day to containerize. Build and test Docker Compose incrementally.
   - **Write the report throughout**: Capture architecture decisions and screenshots as you build. Do not try to reconstruct everything at the end.
   - **Use office hours**: Bring Docker issues early. Discuss caching strategies and report structure with instructors.


Final Project Summary
---------------------

.. admonition:: Cumulative Achievement
   :class: note

   **Points**:

   - GP1: Relational Design = 10 points
   - GP2: PostgreSQL + Python = 15 points
   - GP3: MongoDB Integration = 10 points
   - GP4: Redis + Complete System = 15 points
   - **Total**: 50 points
   - **Optional Presentation**: +4 points bonus

**Your Achievement**:

You have built a production-grade polyglot persistence system demonstrating relational database design and normalization, complex SQL query optimization, document databases for high-volume data, in-memory caching for performance, cross-database integration, CLI application development, Docker deployment, and professional technical documentation.
