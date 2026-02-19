=======================================================
Group Project 3: MongoDB Document Database Integration
=======================================================

Overview
--------

Add MongoDB to handle high-volume traffic event data with flexible schemas. Integrate with your PostgreSQL system to create a polyglot persistence architecture.

**Timeline**: 3 weeks

**Weight**: 10 points (25% of final project)

**Team Size**: 4 students

**Builds on**: Your PostgreSQL system from GP2


.. important::
   
   **What You'll Deliver**
   
   This project requires a **complete MongoDB integration** with your existing PostgreSQL system:
   
   - 3 MongoDB files (setup script, data script, queries)
   - 3 documentation files (polyglot design, schema docs, integration strategy)
   - 1 updated Python application (MongoDB repositories + cross-database services)
   - 1 README file
   - 1 team contributions file
   
   **Submission**: Single ZIP file named ``GP3_Traffic_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Recognize when document databases are appropriate vs. relational
- Design flexible document schemas with embedding and referencing
- Write MongoDB aggregation pipelines for complex analytics
- Implement geospatial queries in document databases
- Integrate multiple databases in a Python application
- Handle cross-database queries and data consistency


Part 1: Polyglot Persistence Design
------------------------------------

**Objective**: Analyze your data and decide what belongs in PostgreSQL vs. MongoDB.

.. dropdown:: 📋 Task 1.1: Data Partitioning Analysis (2 points)
   :class-container: sd-border-primary
   :open:

   For each data type, answer:
   
   1. **Structure**: Fixed schema or variable?
   2. **Consistency**: Strong ACID or eventual OK?
   3. **Relationships**: Many foreign keys or independent?
   4. **Query Pattern**: Complex JOINs or hierarchical access?
   5. **Volume**: Moderate or high write throughput?
   6. **Evolution**: Schema stable or frequently changing?
   
   .. list-table::
      :header-rows: 1
      :widths: 30 35 35
      :class: compact-table
   
      * - Characteristic
        - PostgreSQL
        - MongoDB
      * - Schema
        - Fixed, rigid
        - Flexible, variable
      * - Relationships
        - Many FKs, JOINs
        - Nested documents
      * - Consistency
        - Strong ACID
        - Eventual consistency
      * - Volume
        - Moderate writes
        - High write volume
      * - Evolution
        - Migrations required
        - Schema-less evolution
   
   **Decision Template**:
   
   .. code-block:: text
   
      Data Type: Traffic Flow Events
      
      Analysis:
      1. Structure: Variable (different intersection types produce different data)
      2. Consistency: Eventual OK (analytics, not transactional)
      3. Relationships: Minimal (references intersection_id only)
      4. Query Pattern: Time-range aggregation, not JOINs
      5. Volume: 1.4M documents/day (very high write throughput)
      6. Evolution: Sensor types added frequently
      
      Decision: MongoDB
      Justification: High volume, flexible schema, time-series access
                     pattern, minimal relational needs
   
   **File to create**: ``docs/polyglot_design.md``

.. dropdown:: 📋 Data Assignment
   :class-container: sd-border-primary

   **Keep in PostgreSQL**:
   
   - Intersection metadata (referenced frequently)
   - Sensor configuration (structured, low-volume)
   - Maintenance schedules (ACID transactions needed)
   - Emergency routes (complex relationships)
   
   **Move to MongoDB**:
   
   - **Traffic flow events** (1.4M docs/day, time-series)
   - **Sensor readings** (variable schema per sensor type)
   - **Incident reports** (embedded witness statements, images)
   - **Traffic predictions** (ML model outputs, nested arrays)
   - **Congestion patterns** (pre-aggregated analytics)


Part 2: MongoDB Schema Design
------------------------------

**Objective**: Design document schemas for at least 6 collections with appropriate indexes.

.. dropdown:: 📋 Task 2.1: Required Collections (2 points)
   :class-container: sd-border-primary
   :open:

   Design **at least 6 collections**:
   
   **1. traffic_flow_events**
   
   Real-time traffic measurements every 30 seconds:
   
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
   - **Expected volume**: 1.4M documents/day
   
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
   
   **3-6. Additional Collections**: incident_reports, traffic_predictions, congestion_patterns, connected_vehicle_data
   
   **Schema Documentation Format**:
   
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
        - lane: Integer
        - count: Integer
        - avg_speed: Double
      
      Embedding Rationale: Lane distribution embedded because it is
        always queried with the parent event and is bounded (max 6 lanes)
      
      Expected Volume: ~1.4M documents/day
      Retention: 90 days (TTL index)
   
   **File to create**: ``docs/mongodb_schema.md``

.. dropdown:: 📋 Embedding vs. Referencing
   :class-container: sd-border-primary

   **Decision Tree**:
   
   .. code-block:: text
   
      Is data queried together?
      ├── YES: Consider embedding
      │   └── Will embedding cause unbounded growth?
      │       ├── YES: Use referencing
      │       └── NO: Embed
      └── NO: Use referencing
   
   **Examples**:
   
   - Embed: Lane distribution in traffic events (queried together, bounded)
   - Do not embed: All sensor readings in intersection doc (unbounded growth)
   - Reference: intersection_id to PostgreSQL (different databases)

.. dropdown:: 📋 Task 2.2: Index Strategy (1 point)
   :class-container: sd-border-primary

   **MongoDB Index Types**:
   
   **Compound Indexes**: (intersection_id, timestamp) for time-range queries
   
   **Geospatial Indexes**: 2dsphere for location queries
   
   **TTL Indexes**: Auto-delete old data (90-day retention)
   
   **Text Indexes**: Full-text search on incident descriptions
   
   **Index Documentation Format**:
   
   .. code-block:: text
   
      Collection: traffic_flow_events
      
      Index 1: { intersection_id: 1, timestamp: -1 }
      Type: Compound
      Purpose: Time-range queries filtered by intersection
      Query Pattern: db.traffic_flow_events.find({
        intersection_id: 15,
        timestamp: { $gte: ISODate("2026-02-12"), $lt: ISODate("2026-02-19") }
      })
      
      Index 2: { timestamp: 1 }, { expireAfterSeconds: 7776000 }
      Type: TTL
      Purpose: Automatically remove documents older than 90 days
      Retention Policy: 90 days for raw events


Part 3: MongoDB Implementation
-------------------------------

**Objective**: Set up MongoDB collections and write complex queries.

.. dropdown:: 📋 Task 3.1: Database Setup (1 point)
   :class-container: sd-border-primary
   :open:

   **mongo_setup.js**:
   
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
   
   **File to create**: ``mongodb/mongo_setup.js``

.. dropdown:: 📋 Task 3.2: Sample Data (integrated into score)
   :class-container: sd-border-primary

   Generate realistic MongoDB sample data:
   
   - 1000+ traffic flow events across multiple intersections
   - 500+ sensor readings (mix of camera, radar, lidar types)
   - 50+ incident reports with embedded details
   - 100+ traffic predictions
   - 50+ congestion pattern summaries
   - 100+ connected vehicle records
   
   **File to create**: ``mongodb/mongo_data.js``

.. dropdown:: 📋 Task 3.3: Query Development (2 points)
   :class-container: sd-border-primary

   Write **at least 8 MongoDB queries**:
   
   **Aggregation Pipelines** (3 queries minimum):
   
   **Example Challenge**: *"Calculate hourly average vehicle counts by intersection"*
   
   .. code-block:: javascript
   
      db.traffic_flow_events.aggregate([
        { $match: { 
          timestamp: { $gte: ISODate("2026-02-12"), $lt: ISODate("2026-02-19") }
        }},
        { $group: {
          _id: {
            intersection_id: "$intersection_id",
            hour: { $hour: "$timestamp" }
          },
          avg_vehicles: { $avg: "$vehicle_count" },
          count: { $sum: 1 }
        }},
        { $sort: { "_id.intersection_id": 1, "_id.hour": 1 } }
      ]);
   
   **Geospatial Queries** (2 queries minimum):
   
   Find sensor readings within 500m of incident location.
   
   **Text Search** (1 query minimum):
   
   Search incident descriptions with relevance scoring.
   
   **Array Operations** (2 queries minimum):
   
   Analyze lane-specific data using $unwind.
   
   **Query Documentation Format**:
   
   .. code-block:: javascript
   
      // Query #X: [Title]
      // Business Question: [Problem being solved]
      // Collections Used: [List collections]
      // Pipeline Stages: [e.g., $match, $group, $sort]
      // Index Usage: [Which indexes help this query]
      
      [YOUR MONGODB QUERY]
      
      // Expected Output: [Description of result shape]
      // Sample Results: [First 2-3 documents]
   
   **File to create**: ``mongodb/mongo_queries.js``


Part 4: Python Integration
---------------------------

**Objective**: Extend your GP2 Python application with MongoDB support and cross-database services.

.. dropdown:: 📋 Task 4.1: MongoDB Integration (2 points)
   :class-container: sd-border-primary
   :open:

   **Extend Project Structure**:
   
   .. code-block:: text
   
      traffic-management/
      ├── config/
      │   ├── database.py      # Updated: PostgreSQL + MongoDB
      │   └── mongodb.py       # New: MongoDB-specific config
      ├── repositories/
      │   ├── postgres/        # Existing from GP2
      │   └── mongodb/         # New: MongoDB repositories
      │       ├── traffic_events_repo.py
      │       └── sensor_readings_repo.py
      ├── services/
      │   └── traffic_service.py  # Updated: Multi-database operations
   
   **Cross-Database Service Example**:
   
   .. code-block:: python
   
      class TrafficDashboardService:
          def get_intersection_dashboard(self, intersection_id):
              # PostgreSQL: Intersection metadata
              intersection = self.pg_repo.find_by_id(intersection_id)
              
              # MongoDB: Recent traffic events
              recent_events = self.mongo_repo.find_recent_events(
                  intersection_id, 
                  minutes=60
              )
              
              return {
                  "intersection": intersection.to_dict(),
                  "current_metrics": self._calculate_metrics(recent_events)
              }
   
   **New API Endpoints** (at least 4):
   
   - ``GET /traffic-events/{intersection_id}/recent`` - Recent events from MongoDB
   - ``GET /analytics/hourly-patterns/{intersection_id}`` - Aggregation pipeline results
   - ``GET /sensor-readings/nearby?lat={lat}&lon={lon}`` - Geospatial query
   - ``GET /dashboard/{intersection_id}`` - Cross-database dashboard


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP3_Traffic_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP3_Traffic_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP3_Traffic_Team{X}/
   ├── mongodb/
   │   ├── mongo_setup.js
   │   ├── mongo_data.js
   │   └── mongo_queries.js
   ├── src/
   │   ├── config/
   │   │   ├── database.py
   │   │   └── mongodb.py
   │   ├── repositories/
   │   │   ├── postgres/
   │   │   └── mongodb/
   │   │       ├── traffic_events_repo.py
   │   │       └── sensor_readings_repo.py
   │   └── services/
   │       └── traffic_service.py
   ├── tests/
   │   ├── test_mongo_repos.py
   │   └── test_cross_db.py
   ├── docs/
   │   ├── polyglot_design.md
   │   ├── mongodb_schema.md
   │   └── integration_strategy.md
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Part 1: Polyglot Persistence Design
   :class-container: sd-border-info

   **Documentation** (1 file):
   
   - ``docs/polyglot_design.md`` - Data partitioning analysis with justifications for each data type

.. dropdown:: 📄 Part 2: MongoDB Schema Design
   :class-container: sd-border-info

   **Documentation** (1 file):
   
   - ``docs/mongodb_schema.md`` - Schema specifications for 6+ collections with embedding rationale and index strategy

.. dropdown:: 📄 Part 3: MongoDB Implementation
   :class-container: sd-border-info

   **MongoDB Files** (3 files):
   
   - ``mongodb/mongo_setup.js`` - Collection creation with validation and indexes
   - ``mongodb/mongo_data.js`` - Sample data for all collections
   - ``mongodb/mongo_queries.js`` - 8+ documented queries

.. dropdown:: 📄 Part 4: Python Integration + Supporting Files
   :class-container: sd-border-info

   **Application** (updated src/ directory):
   
   - ``src/config/mongodb.py`` - MongoDB connection configuration
   - ``src/repositories/mongodb/*.py`` - MongoDB repository classes
   - ``src/services/traffic_service.py`` - Updated with cross-database operations
   
   **Documentation** (1 file):
   
   - ``docs/integration_strategy.md`` - How PostgreSQL and MongoDB work together
   
   **Supporting Files** (2 files):
   
   - ``README.md`` - Updated project overview with MongoDB setup
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP3: Traffic Management System - MongoDB Integration
   
   **Team Number**: [Your team number]
   
   **Scenario**: Smart City Traffic Management
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Project Overview
   
   [2-3 sentence description of your polyglot persistence approach]
   
   ## Setup Instructions
   
   ### Prerequisites
   
   - PostgreSQL 18 with PostGIS (from GP2)
   - MongoDB 6+
   - Python 3.10+
   
   ### MongoDB Setup
   
   ```bash
   mongosh < mongodb/mongo_setup.js
   mongosh < mongodb/mongo_data.js
   ```
   
   ### Verify Data
   
   ```bash
   mongosh traffic_management --eval "db.traffic_flow_events.countDocuments()"
   ```
   
   ## Data Partitioning Summary
   
   | Data Type | Database | Rationale |
   |-----------|----------|-----------|
   | Intersection metadata | PostgreSQL | Structured, relational, ACID |
   | Traffic flow events | MongoDB | High volume, time-series, flexible |
   | Sensor readings | MongoDB | Variable schema per sensor type |
   | [Continue for all data types] | | |
   
   ## Key Design Decisions
   
   1. **Decision 1**: [Brief explanation and rationale]
   2. **Decision 2**: [Brief explanation and rationale]
   3. **Decision 3**: [Brief explanation and rationale]
   
   ## MongoDB Collections Summary
   
   | Collection | Document Count | Key Indexes |
   |------------|---------------|-------------|
   | traffic_flow_events | 1000+ | (intersection_id, timestamp), TTL |
   | sensor_readings | 500+ | (sensor_id, timestamp) |
   | [Continue for all collections] | | |
   
   ## File Guide
   
   - `mongodb/mongo_setup.js` - Collection creation with validation
   - `mongodb/mongo_data.js` - Sample data generation
   - `mongodb/mongo_queries.js` - 8+ MongoDB queries
   - `src/` - Updated Python application with MongoDB integration
   - `docs/` - Polyglot design, schema docs, integration strategy
   
   ## Tools Used
   
   - **Relational DB**: PostgreSQL 18 + PostGIS
   - **Document DB**: MongoDB 6
   - **Language**: Python 3.x (pymongo)
   - **Framework**: FastAPI
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP3
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Wrote data partitioning analysis document
   - Designed traffic_flow_events and sensor_readings schemas
   - Created mongo_setup.js with validation rules
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Designed incident_reports, traffic_predictions collections
   - Generated sample data (mongo_data.js)
   - Wrote aggregation pipeline queries
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Built MongoDB repository classes in Python
   - Implemented cross-database service layer
   - Wrote integration tests
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Wrote geospatial and text search queries
   - Created new API endpoints for MongoDB data
   - Wrote documentation (schema, integration strategy, README)
   
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

   **Design Documents** (3 files):
   
   - [ ] Polyglot design with justification for each data type
   - [ ] MongoDB schema documentation for 6+ collections
   - [ ] Integration strategy describing cross-database operations
   
   **MongoDB Files** (3 files):
   
   - [ ] mongo_setup.js creates all collections with validation
   - [ ] mongo_setup.js creates all required indexes (compound, TTL, geospatial, text)
   - [ ] mongo_data.js loads realistic sample data
   - [ ] mongo_queries.js contains 8+ documented queries
   
   **Python Application**:
   
   - [ ] MongoDB connection configured (pymongo)
   - [ ] Repository classes for MongoDB collections
   - [ ] Cross-database service methods working
   - [ ] New API endpoints for MongoDB data
   - [ ] Tests for MongoDB operations
   
   **Supporting Files**:
   
   - [ ] README.md with MongoDB setup instructions
   - [ ] team_contributions.md with individual contributions
   
   **Quality Checks**:
   
   - [ ] mongo_setup.js runs without errors
   - [ ] mongo_data.js loads without validation failures
   - [ ] All 8+ queries execute successfully
   - [ ] Cross-database dashboard endpoint returns combined data
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP3_Traffic_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Treating MongoDB like SQL** - Using separate collections for everything instead of embedding related data
   
   ❌ **No schema validation** - MongoDB is flexible, not lawless. Use JSON Schema validation
   
   ❌ **Missing TTL indexes** - Forgetting data expiration leads to unbounded storage growth
   
   ❌ **Poor cross-database references** - Using MongoDB ObjectIds to reference PostgreSQL or vice versa without a clear strategy
   
   ❌ **No geospatial indexes** - Attempting location queries without 2dsphere indexes
   
   ❌ **Unrealistic data volume** - Only 10 documents per collection does not demonstrate scalability
   
   ❌ **Tight coupling** - Services that break if one database is unavailable
   
   ❌ **No embedding rationale** - Choosing embed vs. reference without documented justification


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Data Partitioning**
     - 2
     - Clear rationale for each data type (1pt); Documented decision framework (1pt)
   * - **Part 2: Schema Design**
     - 2
     - 6+ collections with complete specs (1pt); Appropriate embedding/referencing with rationale (1pt)
   * - **Part 2: Index Strategy**
     - 1
     - Appropriate indexes for all collections with justification
   * - **Part 3: Setup & Data**
     - 1
     - Collections with validation (0.5pt); Realistic sample data (0.5pt)
   * - **Part 3: MongoDB Queries**
     - 2
     - 8+ queries covering all categories (1pt); Correct results with documentation (1pt)
   * - **Part 4: Python Integration**
     - 2
     - Clean MongoDB repositories (1pt); Working cross-database services (1pt)
   * - **Total**
     - **10**
     - 


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP3**
   
   - **Design schemas before coding** - Sketch your document structures on paper first. Think about what gets queried together.
   - **Embrace the document model** - If you find yourself creating many small collections with references between them, you are probably still thinking relationally.
   - **Test aggregation pipelines incrementally** - Build pipelines one stage at a time in mongosh. Add $match, verify results, then add $group, verify again.
   - **Use realistic cross-references** - When your MongoDB documents reference PostgreSQL intersection_ids, make sure those IDs actually exist in your GP2 data.
   - **Think about data flow** - Draw a diagram showing how data moves from sensors to MongoDB to the API. This helps you design clean service layer methods.
   - **Use office hours** - Bring your schema designs for review. Discuss embedding vs. referencing trade-offs with instructors.


Next Steps
----------

After completing GP3, you will:

- Receive feedback from instructors
- Analyze which queries are slow and which data is accessed frequently
- Begin GP4: Adding Redis for real-time caching and completing the system
- Deploy the full three-database system with Docker Compose

.. note::
   
   **Your GP3 integration creates the polyglot foundation** for GP4 (Redis + deployment + final report).
   
   Start thinking: What data needs sub-second access? What can be cached? What events should be broadcast in real time?