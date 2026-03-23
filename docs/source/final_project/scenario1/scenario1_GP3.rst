=======================================================
Group Project 3: MongoDB Document Database Integration
=======================================================

Overview
--------

Add MongoDB to handle high-volume traffic event data with flexible schemas. Integrate with your PostgreSQL system to create a polyglot persistence architecture.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 2 weeks |
   **Weight**: 10 points (20% of final project) |
   **Team Size**: 4 students

**Builds on**: Your PostgreSQL system from GP2


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

.. dropdown:: Task 1.1: Data Partitioning Analysis (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   For each data type in your traffic management system, evaluate whether it belongs in PostgreSQL or MongoDB. Consider these factors:

   1. **Structure**: Fixed schema or variable?
   2. **Consistency**: Strong ACID needed or eventual consistency OK?
   3. **Relationships**: Many foreign keys or mostly independent?
   4. **Query Pattern**: Complex JOINs or hierarchical/time-range access?
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

   **Decision Template** (use for each data type):

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

.. dropdown:: Data Assignment Guidelines
   :icon: gear
   :class-container: sd-border-primary

   **Keep in PostgreSQL** (from GP2):

   - Intersection metadata (referenced frequently, structured)
   - Sensor configuration (structured, low-volume)
   - Maintenance schedules (ACID transactions needed)
   - Emergency routes (complex relationships)

   **Move to MongoDB** (new in GP3):

   - **Traffic flow events**: high-volume time-series measurements
   - **Sensor readings**: variable schema per sensor type (camera, radar, lidar)
   - **Incident reports**: embedded witness statements, flexible detail fields
   - **Traffic predictions**: ML model outputs, nested arrays

   **Document your decisions and rationale** in ``docs/polyglot_design.md``. This file should also include your collection schemas (see Part 2) and index strategy.

   **File to create**: ``docs/polyglot_design.md``


Part 2: MongoDB Schema Design
------------------------------

**Objective**: Design document schemas for at least 4 collections with appropriate indexes.

.. dropdown:: Task 2.1: Required Collections (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Design **at least 4 collections**. We show two detailed examples below; design at least two more of your own.

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

   **3-4. Your additional collections**: Choose from incident_reports, traffic_predictions, congestion_patterns, or others that make sense for your system.

   **Schema Documentation Format** (include in ``docs/polyglot_design.md``):

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

.. dropdown:: Embedding vs. Referencing
   :icon: gear
   :class-container: sd-border-primary

   **Decision Tree**:

   .. code-block:: text

      Is data queried together?
      |-- YES: Consider embedding
      |   |-- Will embedding cause unbounded growth?
      |       |-- YES: Use referencing
      |       |-- NO: Embed
      |-- NO: Use referencing

   **Examples**:

   - Embed: Lane distribution in traffic events (queried together, bounded)
   - Do not embed: All sensor readings in intersection doc (unbounded growth)
   - Reference: intersection_id to PostgreSQL (different databases)

.. dropdown:: Task 2.2: Index Strategy (1 point)
   :icon: gear
   :class-container: sd-border-primary

   For each collection, define appropriate indexes and document them in ``docs/polyglot_design.md``.

   **MongoDB Index Types to Consider**:

   - **Compound Indexes**: (intersection_id, timestamp) for time-range queries
   - **Geospatial Indexes**: 2dsphere for location queries
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

.. dropdown:: Task 3.1: Database Setup (1 point)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Create ``mongo_setup.js`` to define collections with validation and indexes:

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

   **Files to create**: ``mongodb/mongo_setup.js`` and ``mongodb/mongo_data.js``

.. dropdown:: Task 3.2: Query Development (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Write **at least 6 MongoDB queries** covering the following categories:

   **Aggregation Pipelines (3 queries minimum)**

   Use $match, $group, $sort, $project, and other pipeline stages.

   Examples:

   - *"Calculate hourly average vehicle counts by intersection."*
   - *"Find the top 5 most congested intersections over the past week."*
   - *"Summarize sensor readings by type and day."*

   **Geospatial Queries (1 query minimum)**

   Use MongoDB geospatial operators ($near, $geoWithin).

   Example: *"Find sensor readings within 500m of a given incident location."*

   **Array Operations (2 queries minimum)**

   Use $unwind, $elemMatch, or array operators to analyze nested data.

   Examples:

   - *"Analyze lane-specific traffic patterns using $unwind on lane_distribution."*
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


Part 4: Python Integration
---------------------------

**Objective**: Extend your GP2 Python application with MongoDB support and cross-database services.

.. dropdown:: Task 4.1: MongoDB Integration (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Extend your project structure**:

   .. code-block:: text

      traffic-management/
      ├── config/
      │   ├── database.py      # Existing: PostgreSQL
      │   └── mongodb.py       # New: MongoDB connection
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

   **New CLI Menu Options** (at least 3):

   - View recent traffic events for an intersection (MongoDB query)
   - Show hourly traffic patterns for an intersection (aggregation pipeline)
   - Intersection dashboard combining PostgreSQL metadata with MongoDB events (cross-database)

   Update ``cli/main.py`` to include these new options alongside your GP2 options.


Folder Structure
----------------

.. code-block:: text

   GP3_Traffic_Team{X}/
   ├── mongodb/
   │   ├── mongo_setup.js          # Collection creation with validation
   │   ├── mongo_data.js           # Sample data for all collections
   │   └── mongo_queries.js        # 6+ documented queries
   ├── src/
   │   ├── config/
   │   │   ├── database.py         # Existing: PostgreSQL
   │   │   └── mongodb.py          # New: MongoDB connection
   │   ├── repositories/
   │   │   ├── postgres/           # Existing from GP2
   │   │   └── mongodb/            # New: MongoDB repositories
   │   │       ├── traffic_events_repo.py
   │   │       └── sensor_readings_repo.py
   │   ├── services/
   │   │   └── traffic_service.py  # Updated: cross-database operations
   │   └── cli/
   │       └── main.py             # Updated: new MongoDB menu options
   ├── docs/
   │   └── polyglot_design.md      # Partitioning, schemas, indexes
   ├── requirements.txt
   ├── .env.example
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **docs/polyglot_design.md**

   This is the main design document for GP3. It should contain three sections: (1) your data partitioning analysis explaining what stays in PostgreSQL and what moves to MongoDB with justifications for each data type, (2) your MongoDB collection schemas with document structures, embedding rationale, and expected volumes, and (3) your index strategy listing all indexes for each collection with their type, purpose, and the query patterns they support.

   **requirements.txt**

   Updated from GP2 to include ``pymongo``.

   **.env.example**

   Updated from GP2 to include MongoDB connection variables:

   .. code-block:: text

      DB_HOST=localhost
      DB_PORT=5432
      DB_NAME=traffic_management
      DB_USER=postgres
      DB_PASSWORD=your_password_here
      MONGO_HOST=localhost
      MONGO_PORT=27017
      MONGO_DB=traffic_management

   **README.md**

   Updated from GP2. Add MongoDB prerequisites (MongoDB 6+), setup instructions (``mongosh < mongodb/mongo_setup.js`` and ``mongosh < mongodb/mongo_data.js``), verification commands, and a data partitioning summary table showing which data lives in which database.

   **team_contributions.md**

   List each team member's name, tasks completed, hours contributed, and contribution percentage. Percentages must sum to 100%.


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP3_Traffic_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP3_Traffic_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **Design Document**:

   - [ ] ``polyglot_design.md`` covers partitioning, schemas, and indexes
   - [ ] Each data type has a clear PostgreSQL vs. MongoDB justification
   - [ ] 4+ collections documented with embedding rationale

   **MongoDB Files**:

   - [ ] ``mongo_setup.js`` creates all collections with validation and indexes
   - [ ] ``mongo_data.js`` loads realistic sample data (runs without errors)
   - [ ] ``mongo_queries.js`` contains 6+ queries with documentation

   **Python Application**:

   - [ ] MongoDB connection configured (pymongo)
   - [ ] Repository classes for MongoDB collections
   - [ ] Cross-database service methods working
   - [ ] 3+ new CLI menu options for MongoDB data

   **Supporting Files**:

   - [ ] README.md updated with MongoDB setup instructions
   - [ ] .env.example updated with MongoDB variables
   - [ ] requirements.txt updated with pymongo
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
   * - **Part 1: Data Partitioning**
     - 2
     - Clear rationale for each data type (1pt); documented decision framework (1pt)
   * - **Part 2: Schema and Indexes**
     - 3
     - 4+ collections with complete schemas and embedding rationale (2pts); appropriate indexes with justification (1pt)
   * - **Part 3: Setup and Queries**
     - 3
     - Collections with validation and realistic data (1pt); 6+ queries covering all categories with correct results (2pts)
   * - **Part 4: Python Integration**
     - 2
     - MongoDB repositories and cross-database services (1pt); 3+ new CLI menu options working (1pt)
   * - **Total**
     - **10**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Treating MongoDB like SQL (many small collections with references instead of embedding related data)
   - No schema validation (MongoDB is flexible, not lawless)
   - Missing TTL indexes (leads to unbounded storage growth)
   - Using MongoDB ObjectIds to reference PostgreSQL without a clear strategy
   - Only 10 documents per collection (does not demonstrate realistic usage)
   - Choosing embed vs. reference without documented justification


Tips for Success
----------------

.. tip::

   - **Design schemas before coding**: Sketch your document structures on paper first. Think about what gets queried together.
   - **Embrace the document model**: If you find yourself creating many small collections with references between them, you are probably still thinking relationally.
   - **Test aggregation pipelines incrementally**: Build pipelines one stage at a time in mongosh. Add $match, verify results, then add $group, verify again.
   - **Use realistic cross-references**: When your MongoDB documents reference PostgreSQL intersection_ids, make sure those IDs actually exist in your GP2 data.
   - **Use office hours**: Bring your schema designs for review. Discuss embedding vs. referencing trade-offs with instructors.
