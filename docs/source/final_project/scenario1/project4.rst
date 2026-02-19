====================================================
Group Project 4: Redis Integration + Complete System
====================================================

Overview
--------

Add Redis for real-time caching and state management, complete your three-database polyglot system, deploy with Docker Compose, and write comprehensive technical documentation.

**Timeline**: 4 weeks

**Weight**: 15 points (12.5% of final project, includes final report)

**Team Size**: 4 students

**Builds on**: Your PostgreSQL + MongoDB system from GP2 and GP3


.. important::
   
   **What You'll Deliver**
   
   This project requires a **complete three-database system** with deployment and documentation:
   
   - 2 Redis files (setup, operations)
   - 2 deployment files (Dockerfile, docker-compose.yml)
   - 1 final technical report (10 to 15 pages, PDF)
   - 1 updated Python application (Redis integration + unified API)
   - 1 README file
   - 1 team contributions file
   
   **Submission**: Single ZIP file named ``GP4_Traffic_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Design Redis data structures for real-time state and caching
- Implement cache-aside and write-through caching patterns
- Use Redis pub/sub for real-time event broadcasting
- Build a complete three-database architecture
- Deploy polyglot systems using Docker Compose
- Document complex distributed systems professionally
- Analyze performance across multiple databases


Part 1: Redis Architecture Design
----------------------------------

**Objective**: Design a caching strategy that identifies what to cache, which patterns to use, and how to handle invalidation.

.. dropdown:: 📋 Task 1.1: Caching Strategy Design (2 points)
   :class-container: sd-border-primary
   :open:

   Evaluate each data type for Redis suitability:
   
   **Frequency**: How often is this read?
   
   - 100+ times/second: Excellent Redis candidate
   - 10 times/second: Good Redis candidate
   - Once per minute: Maybe Redis
   - Once per hour: Probably not Redis
   
   **Latency Requirements**:
   
   - <10ms required: Must use Redis
   - <100ms desired: Redis helps significantly
   - <1 second acceptable: Maybe Redis
   - >1 second OK: Do not need Redis
   
   **Recommended for Redis**:
   
   - Current signal states (updated every 30-90 sec, read constantly)
   - Live intersection metrics (vehicle counts, congestion level)
   - Real-time congestion rankings across city
   - Recent incident queue for emergency dispatch
   - Active connected vehicles by location
   
   **Caching Decision Template**:
   
   .. code-block:: text
   
      Data: Current Signal States
      
      Read Frequency: 100+ times/second (every dashboard refresh)
      Write Frequency: Every 30-90 seconds (signal cycle changes)
      Latency Requirement: <10ms (real-time display)
      Data Size: ~2KB per intersection (4 signals x fields)
      Staleness Tolerance: 5 seconds acceptable
      
      Decision: Cache in Redis
      Pattern: Write-through (update Redis on every signal change)
      TTL: 300 seconds (safety net if writer fails)
      Key Format: signal:{intersection_id}:{position}:state
   
   **File to create**: ``docs/caching_strategy.md``

.. dropdown:: 📋 Caching Patterns
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
   
   **Document your choice for each cached data type with justification.**


Part 2: Redis Data Structure Design
------------------------------------

**Objective**: Design at least 8 Redis data structures using appropriate types.

.. dropdown:: 📋 Task 2.1: Required Structures (2 points)
   :class-container: sd-border-primary
   :open:

   **1. Strings** - Simple key-value:
   
   .. code-block:: text
   
      signal:15:north:state = "green"  (TTL: 300 seconds)
      signal:23:south:state = "red"
   
   **2. Hashes** - Objects with multiple fields:
   
   .. code-block:: text
   
      intersection:15:status = {
        vehicle_count: 127,
        avg_speed: 28.5,
        congestion_level: "moderate",
        last_update: "2026-02-19T14:30:00Z"
      }
   
   **3. Sorted Sets** - Rankings:
   
   .. code-block:: text
   
      congestion:rankings = {
        "intersection:15": 85.3,  // score = congestion level
        "intersection:42": 91.5,
        "intersection:23": 72.1
      }
   
   **4. Lists** - Queues:
   
   .. code-block:: text
   
      incidents:recent = [incident_id_1, incident_id_2, ...]  // FIFO queue
   
   **5. Sets** - Unique collections:
   
   .. code-block:: text
   
      vehicles:grid_A3 = {vehicle_123, vehicle_456, vehicle_789}
   
   **6. Geospatial** - Location tracking:
   
   .. code-block:: text
   
      vehicles:active = geo index of vehicle locations
   
   **7. Streams** - Event log:
   
   .. code-block:: text
   
      stream:sensor_readings = append-only event stream
   
   **8. Pub/Sub** - Broadcasting:
   
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
      
      Estimated Memory: ~50 bytes per key x 4 positions x 500 intersections = ~100KB

.. dropdown:: 📋 Redis Data Structure Catalog
   :class-container: sd-border-primary

   Create a summary document cataloging all structures:
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Structure
        - Redis Type
        - Key Pattern
        - TTL
        - Purpose
      * - Signal States
        - String
        - signal:{id}:{pos}:state
        - 300s
        - Current signal colors
      * - Intersection Status
        - Hash
        - intersection:{id}:status
        - 60s
        - Live traffic metrics
      * - Congestion Rankings
        - Sorted Set
        - congestion:rankings
        - None
        - City-wide congestion rank
      * - Recent Incidents
        - List
        - incidents:recent
        - None
        - FIFO dispatch queue
   
   **File to create**: ``docs/redis_data_structures.md``


Part 3: Redis Implementation
-----------------------------

**Objective**: Implement Redis setup and operations with multi-database integration.

.. dropdown:: 📋 Task 3.1: Redis Setup and Operations (2 points)
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
   
   **File to create**: ``redis/redis_setup.py`` and ``redis/redis_operations.py``

.. dropdown:: 📋 Task 3.2: Cache Integration (2 points)
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
              
              # Redis: Congestion rank
              rank = self.redis.zrevrank(
                  "congestion:rankings", 
                  f"intersection:{intersection_id}"
              )
              
              # MongoDB: Recent history
              recent_events = self.mongo_repo.find_recent_events(
                  intersection_id,
                  minutes=60
              )
              
              return {
                  "intersection": intersection,
                  "current": current_metrics,
                  "rank": rank + 1 if rank is not None else None,
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


Part 4: Complete System Integration
------------------------------------

**Objective**: Build unified API endpoints and deploy the full system with Docker Compose.

.. dropdown:: 📋 Task 4.1: Unified API (3 points)
   :class-container: sd-border-primary
   :open:

   **Endpoint 1**: ``GET /dashboard/intersection/{id}``
   
   - PostgreSQL: Infrastructure details
   - MongoDB: Traffic history
   - Redis: Real-time metrics
   
   **Endpoint 2**: ``GET /real-time/top-congested``
   
   - Redis: Get rankings (fast!)
   - PostgreSQL: Lookup details
   - MongoDB: Recent context
   
   **Endpoint 3**: ``POST /events/incident``
   
   - Validate and insert into PostgreSQL
   - Add to MongoDB for detailed report
   - Publish to Redis pub/sub
   - Add to Redis recent incidents queue
   - Invalidate relevant caches
   
   **API Documentation**:
   
   For each endpoint, document:
   
   .. code-block:: text
   
      Endpoint: GET /dashboard/intersection/{id}
      
      Description: Real-time intersection dashboard combining all databases
      
      Databases Used:
      - PostgreSQL: intersection metadata, signal config, maintenance status
      - MongoDB: last 60 min of traffic events, sensor readings
      - Redis: current signal states, live metrics, congestion rank
      
      Response Time Target: <100ms
      
      Example Response:
      {
        "intersection": { "id": 15, "name": "Main St & 1st Ave", ... },
        "signals": { "north": "green", "south": "red", ... },
        "current_metrics": { "vehicle_count": 127, "avg_speed": 28.5 },
        "congestion_rank": 3,
        "recent_events": [ ... last 60 min ... ]
      }

.. dropdown:: 📋 Task 4.2: Production Deployment (2 points)
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
          ports:
            - "8000:8000"
   
   **Deployment Verification**:
   
   .. code-block:: text
   
      After running docker-compose up:
      
      1. PostgreSQL: psql connects, schema loaded, data present
      2. MongoDB: mongosh connects, collections exist, data loaded
      3. Redis: redis-cli connects, PING returns PONG
      4. App: http://localhost:8000/docs shows Swagger UI
      5. Dashboard endpoint returns data from all three databases
   
   **File to create**: ``docker-compose.yml`` and ``Dockerfile``


Part 5: Final Technical Report
-------------------------------

**Objective**: Write a comprehensive technical report documenting the complete system.

.. dropdown:: 📋 Task 5.1: Report Structure (2 points)
   :class-container: sd-border-primary
   :open:

   **10 to 15 pages, submitted as PDF.**
   
   **1. Executive Summary** (1 page)
   
   - System overview
   - Three-database architecture
   - Key achievements
   
   **2. System Requirements** (1 page)
   
   - Problem statement
   - Requirements
   - Success criteria
   
   **3. Architecture Overview** (2 to 3 pages)
   
   - System architecture diagram
   - Component descriptions
   - Data flow diagrams
   
   **4. Database Design Decisions** (3 to 4 pages)
   
   For each database (PostgreSQL, MongoDB, Redis):
   
   - What data and why
   - Schema/structure highlights
   - Key design decisions
   - Challenges and solutions
   
   **5. Integration Architecture** (2 to 3 pages)
   
   - Cross-database queries
   - Consistency strategies
   - Cache invalidation
   - Error handling
   
   **6. Performance Analysis** (1 to 2 pages)
   
   - Benchmark results
   - Before/after comparisons
   - Query optimization wins
   
   **7. Lessons Learned** (1 page)
   
   - What worked well
   - Challenges faced
   - What you would do differently
   
   **8. Future Improvements** (1 page)
   
   - Known limitations
   - Potential enhancements
   - Scalability roadmap
   
   **File to create**: ``docs/technical_report.pdf``


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP4_Traffic_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP4_Traffic_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP4_Traffic_Team{X}/
   ├── postgresql/          # From GP2
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── mongodb/             # From GP3
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
   │   └── api/
   │       └── endpoints.py
   ├── tests/
   │   ├── test_redis.py
   │   ├── test_integration.py
   │   └── test_api.py
   ├── docker-compose.yml
   ├── Dockerfile
   ├── requirements.txt
   ├── docs/
   │   ├── caching_strategy.md
   │   ├── redis_data_structures.md
   │   └── technical_report.pdf
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Part 1-2: Redis Design
   :class-container: sd-border-info

   **Documentation** (2 files):
   
   - ``docs/caching_strategy.md`` - Caching decisions with justifications
   - ``docs/redis_data_structures.md`` - 8+ data structure specifications

.. dropdown:: 📄 Part 3: Redis Implementation
   :class-container: sd-border-info

   **Redis Files** (2 files):
   
   - ``redis/redis_setup.py`` - Initialize all data structures
   - ``redis/redis_operations.py`` - Operations for each structure

.. dropdown:: 📄 Part 4: System Integration + Deployment
   :class-container: sd-border-info

   **Application** (updated src/ directory):
   
   - ``src/config/redis_config.py`` - Redis connection configuration
   - ``src/repositories/redis/*.py`` - Redis repository classes
   - ``src/services/traffic_service.py`` - Three-database service layer
   - ``src/api/endpoints.py`` - Unified API endpoints
   
   **Deployment** (2 files):
   
   - ``docker-compose.yml`` - All three databases + application
   - ``Dockerfile`` - Python application container

.. dropdown:: 📄 Part 5: Final Report + Supporting Files
   :class-container: sd-border-info

   **Report** (1 file):
   
   - ``docs/technical_report.pdf`` - 10 to 15 page comprehensive report
   
   **Supporting Files** (2 files):
   
   - ``README.md`` - Complete project overview with Docker setup
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP4: Traffic Management System - Complete Polyglot System
   
   **Team Number**: [Your team number]
   
   **Scenario**: Smart City Traffic Management
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Project Overview
   
   [2-3 sentence description of your complete polyglot system]
   
   ## Quick Start (Docker)
   
   ```bash
   docker-compose up --build
   ```
   
   This starts all three databases and the application:
   - PostgreSQL: localhost:5432
   - MongoDB: localhost:27017
   - Redis: localhost:6379
   - API: http://localhost:8000/docs
   
   ## Architecture Summary
   
   | Database | Purpose | Data |
   |----------|---------|------|
   | PostgreSQL | Infrastructure & operations | Intersections, signals, maintenance |
   | MongoDB | High-volume events | Traffic flow, sensor readings |
   | Redis | Real-time state & caching | Signal states, congestion rankings |
   
   ## Key API Endpoints
   
   | Method | Endpoint | Databases Used |
   |--------|----------|----------------|
   | GET | /dashboard/intersection/{id} | All three |
   | GET | /real-time/top-congested | Redis + PostgreSQL |
   | POST | /events/incident | All three |
   | [Continue for all endpoints] | | |
   
   ## Key Design Decisions
   
   1. **Decision 1**: [Brief explanation and rationale]
   2. **Decision 2**: [Brief explanation and rationale]
   3. **Decision 3**: [Brief explanation and rationale]
   
   ## Performance Highlights
   
   - Dashboard endpoint: [X]ms average response time
   - Congestion rankings: [X]ms (Redis sorted set)
   - Cache hit rate: [X]%
   
   ## File Guide
   
   - `postgresql/` - Schema, data, and queries (from GP2)
   - `mongodb/` - Setup, data, and queries (from GP3)
   - `redis/` - Setup and operations (GP4)
   - `src/` - Complete Python application
   - `docker-compose.yml` - Full system deployment
   - `docs/technical_report.pdf` - 10-15 page final report
   
   ## Tools Used
   
   - **Relational DB**: PostgreSQL 18 + PostGIS
   - **Document DB**: MongoDB 6
   - **Cache/State**: Redis 7
   - **Language**: Python 3.x
   - **Framework**: FastAPI
   - **Deployment**: Docker Compose
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP4
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Designed caching strategy document
   - Implemented redis_setup.py and redis_operations.py
   - Built cache-aside pattern for intersection data
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Built unified API endpoints (3-database queries)
   - Implemented pub/sub for traffic alerts
   - Wrote integration tests
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Created Docker Compose configuration
   - Built Dockerfile for application
   - Wrote deployment documentation
   - Performed performance benchmarking
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Wrote final technical report (10-15 pages)
   - Created architecture and data flow diagrams
   - Compiled README and team contributions
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## Collaboration Process
   
   - Met [X] times per week
   - Used [collaboration tools: Zoom, Discord, etc.]
   - Reviewed each other's work before finalizing
   - [Any other collaboration details]


Submission Checklist
---------------------

.. admonition:: ✅ Before Submitting
   :class: tip

   **Redis Design** (2 files):
   
   - [ ] Caching strategy with justifications for each data type
   - [ ] Redis data structure catalog documenting 8+ structures
   
   **Redis Implementation** (2 files):
   
   - [ ] redis_setup.py initializes all structures with sample data
   - [ ] redis_operations.py implements operations for each structure type
   
   **System Integration**:
   
   - [ ] Unified API endpoints use all three databases
   - [ ] Cache-aside pattern implemented for PostgreSQL data
   - [ ] Pub/sub broadcasting for traffic alerts
   - [ ] Cache invalidation strategy implemented
   - [ ] Tests cover Redis operations and integration
   
   **Deployment** (2 files):
   
   - [ ] docker-compose.yml starts all services
   - [ ] Dockerfile builds application correctly
   - [ ] ``docker-compose up`` results in working system
   - [ ] All databases accessible and loaded with data
   
   **Final Report** (1 file):
   
   - [ ] 10 to 15 pages, submitted as PDF
   - [ ] Architecture diagrams included
   - [ ] All three databases discussed with rationale
   - [ ] Performance analysis with benchmarks
   - [ ] Lessons learned section included
   
   **Supporting Files**:
   
   - [ ] README.md with Docker quick-start instructions
   - [ ] team_contributions.md with individual contributions
   - [ ] requirements.txt with all dependencies
   
   **Quality Checks**:
   
   - [ ] ``docker-compose up --build`` succeeds without errors
   - [ ] Dashboard endpoint returns data from all three databases
   - [ ] Redis operations demonstrate all 8 data structure types
   - [ ] Technical report is professional and well-organized
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP4_Traffic_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Caching everything** - Redis memory is limited. Be strategic about what you cache
   
   ❌ **No TTL on cached data** - Forgetting expiration leads to stale data being served indefinitely
   
   ❌ **Docker volumes not configured** - Data lost on container restart
   
   ❌ **Hardcoded connection strings** - Use environment variables for all database URLs
   
   ❌ **No cache invalidation** - Updating PostgreSQL but forgetting to invalidate the Redis cache
   
   ❌ **Pub/sub without subscribers** - Publishing alerts but no service listens for them
   
   ❌ **Thin technical report** - Under 10 pages or missing required sections
   
   ❌ **No performance benchmarks** - Report claims "faster" without actual measurements


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Caching Strategy**
     - 2
     - Well-reasoned caching decisions (1pt); Pattern selection with justification (1pt)
   * - **Part 2: Data Structures**
     - 2
     - 8+ structures with appropriate types (1pt); Complete documentation with memory estimates (1pt)
   * - **Part 3: Redis Implementation**
     - 2
     - Working setup and operations (1pt); Clean integration with existing system (1pt)
   * - **Part 3: Cache Integration**
     - 2
     - Cache-aside pattern working (1pt); Pub/sub and invalidation implemented (1pt)
   * - **Part 4: Unified API**
     - 3
     - Endpoints using all three databases (1.5pts); Correct responses and error handling (1.5pts)
   * - **Part 4: Deployment**
     - 2
     - Working Docker Compose (1pt); All services start and connect (1pt)
   * - **Part 5: Technical Report**
     - 2
     - Comprehensive and professional (1pt); Performance analysis with benchmarks (1pt)
   * - **Total**
     - **15**
     - 


Optional Presentation (+4 points bonus)
-----------------------------------------

.. dropdown:: 🎤 Presentation Requirements
   :class-container: sd-border-primary
   :open:

   **Format**: 15-minute team presentation
   
   **Content**:
   
   1. System architecture overview (2 min)
   2. Database selection rationale (3 min)
   3. Live demonstration (5 min):
      
      - Show API endpoints
      - Demonstrate three-database queries
      - Show performance comparisons
   
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


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP4**
   
   - **Design Redis structures before coding** - Sketch key patterns on paper. Think about TTLs, memory usage, and access patterns.
   - **Implement cache-aside first** - Start with the simplest caching pattern. Get it working for one entity, then extend.
   - **Test with Docker early** - Do not wait until the last day to containerize. Build and test Docker Compose incrementally.
   - **Measure performance** - Use actual benchmarks to show the impact of Redis caching. Before/after comparisons are very compelling in the report.
   - **Write the report throughout** - Capture architecture decisions, screenshots, and performance data as you build. Do not try to reconstruct everything at the end.
   - **Use office hours** - Bring Docker issues early. Discuss caching strategies and report structure with instructors.


Final Project Summary
---------------------

.. admonition:: 🏆 Cumulative Achievement
   :class: note

   **Points**:
   
   - GP1: Relational Design = 10 points
   - GP2: PostgreSQL + Python = 15 points
   - GP3: MongoDB Integration = 10 points
   - GP4: Redis + Complete System = 15 points
   - **Total**: 50 points (40% of course grade)
   - **Optional Presentation**: +4 points (10% bonus)

**Your Achievement**:

You have built a production-grade polyglot persistence system demonstrating:

- Relational database design and normalization
- Complex SQL query optimization
- Document database for high-volume data
- In-memory caching for performance
- Cross-database integration
- REST API development
- Docker deployment
- Professional technical documentation

.. note::
   
   **Congratulations on completing the final project!**
   
   This system showcases real-world database engineering skills valuable for your career. The polyglot persistence pattern you have implemented is used by companies managing large-scale infrastructure, and the architectural decisions you have made mirror those faced by professional database engineers.