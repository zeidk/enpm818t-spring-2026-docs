====================================================
Group Project 1: Relational Database Design
====================================================

Overview
--------

Design the PostgreSQL database schema that will serve as the transactional backbone of your traffic management system. You'll identify entities from business requirements, model their relationships, define keys and constraints, and prove your design is in Third Normal Form (3NF).

**Timeline**: 2 weeks

**Weight**: 10 points (25% of final project)

**Team Size**: 4 students


.. important::
   
   **What You'll Deliver**
   
   This project requires **11 files** in an organized folder structure:
   
   - 2 ER diagrams (Chen notation + Crow's Foot notation)
   - 7 documentation PDFs (catalogs, analysis, proofs)
   - 2 supporting files (README, team contributions)
   
   **Submission**: Single ZIP file named ``GP1_Traffic_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Extract entities and attributes from narrative business requirements
- Design Entity-Relationship Diagrams using Chen and Crow's Foot notations
- Identify and justify primary keys, candidate keys, and foreign keys
- Apply normalization theory (1NF, 2NF, 3NF) to relational schemas
- Analyze functional dependencies
- Evaluate denormalization trade-offs
- Document design decisions professionally


Business Requirements
---------------------

Your traffic management system must track the following information:

.. dropdown:: 📋 Infrastructure Management
   :class-container: sd-border-primary
   :open:

   The city needs to track all traffic intersections with their physical characteristics (location coordinates, intersection type, traffic handling capacity, installation date, jurisdictional district, elevation). Each intersection has a unique identifier and may have multiple traffic signals positioned at different approaches (north, south, east, west). 
   
   Signals have specific types (LED, incandescent, pedestrian), timing modes (fixed, adaptive, emergency), power sources, maintenance history, and warranty information. Each signalized intersection is monitored by multiple sensors of different types (inductive loops, radar, cameras, lidar, acoustic) that track traffic flow, vehicle speeds, and occupancy.

.. dropdown:: 📋 Road Network
   :class-container: sd-border-primary

   Roads connect intersections, and each road segment has specific characteristics: number of lanes, lane widths, speed limits, surface type (asphalt, concrete), length, grade (slope), and indicates whether bike lanes and sidewalks are present. The system must support routing and traffic flow analysis across the network.

.. dropdown:: 📋 Maintenance Operations
   :class-container: sd-border-primary

   The city's maintenance department schedules work for all traffic infrastructure. Each maintenance task specifies the asset type, maintenance type (preventive, corrective, inspection, upgrade), scheduled date and time, estimated duration, priority level, and assigned crew. Maintenance crews have supervisors, specializations (electrical, mechanical, civil, software), certification levels, and availability status.

.. dropdown:: 📋 Incident Management
   :class-container: sd-border-primary

   The system tracks all traffic incidents including accidents, vehicle breakdowns, road hazards, construction activities, and special events. Each incident has a type, severity level (minor, moderate, major, critical), precise location (intersection or road segment), reported/verified/resolved timestamps, number of lanes blocked, and reporting source (sensor, public, officer, camera). Incidents must be linked to locations for analysis and emergency response.

.. dropdown:: 📋 Emergency Response
   :class-container: sd-border-primary

   Emergency vehicles need optimized routes from facilities (hospitals, fire stations, police stations) to incident locations. The system stores predefined emergency routes with priority levels, start and end intersections, alternative routes, and historical performance data (average response times, usage counts). Emergency facilities have specific capabilities, capacity, operating hours, and contact information.

.. dropdown:: 📋 Environmental Monitoring
   :class-container: sd-border-primary

   Weather conditions significantly impact traffic flow. Weather stations at key intersections monitor temperature, humidity, precipitation, wind, and visibility. The system needs location, sensor suite capabilities, operational status, and data transmission frequency for each station.

.. dropdown:: 📋 Parking Management
   :class-container: sd-border-primary

   The city manages parking facilities (surface lots, garages, street parking) with total capacity, designated EV charging spots, accessible spaces, pricing structure, operating hours, and payment methods. Parking information helps predict traffic patterns in downtown areas.

.. dropdown:: 📋 Traffic Control Zones
   :class-container: sd-border-primary

   The city divides the urban area into traffic control zones (downtown, residential, industrial, school zones) with specific default speed limits, special restrictions (time-based, vehicle-type), and enforcement levels. Zones contain multiple intersections, and some intersections may belong to multiple zones.


Task 1: Entity-Relationship Diagrams
-------------------------------------

**Objective**: Design conceptual and logical data models capturing all business requirements.

.. dropdown:: 📋 Part A: Conceptual Model - Chen Notation
   :class-container: sd-border-primary
   :open:

   Create a **conceptual ER diagram** using **Chen notation**.
   
   **Minimum Requirements**:
   
   - 11+ entities covering all business areas
   - All relationships shown as diamonds
   - Cardinality ratios (1:1, 1:N, M:N) labeled
   - Participation constraints (total/partial) indicated
   
   **Notation Elements**:
   
   - **Rectangles** for entities
   - **Diamonds** for relationships
   - **Ovals** for attributes (connected to entities)
   - **Underlined attributes** for primary keys
   - **Double ovals** for multivalued attributes
   - **Dashed ovals** for derived attributes
   - **Composite attributes** shown with sub-ovals
   
   **Purpose**: Focus on **what** data exists and **how** entities relate conceptually.
   
   **Tools**:
   
   - Inkscape (recommended for SVG format)
   - Lucidchart
   - Draw.io
   - Hand-drawn (if very neat)
   
   **File to create**: ``diagrams/chen_conceptual_model.pdf`` (or ``.svg``)

.. dropdown:: 🔷 Part B: Logical Model - Crow's Foot Notation
   :class-container: sd-border-primary

   Create a **logical ER diagram** using **Crow's Foot notation**.
   
   **Minimum Requirements**:
   
   - Same 11+ entities as Chen diagram
   - Attributes listed inside entity rectangles
   - Primary keys marked (PK)
   - Foreign keys indicated (FK)
   
   **Notation Elements**:
   
   - **Rectangles** for entities (tables)
   - **Lines** connecting entities for relationships
   - **Cardinality symbols**:
     
     - Single line: One
     - Crow's foot (three lines): Many
     - Circle: Optional (minimum 0)
     - Bar: Mandatory (minimum 1)
   
   **Purpose**: Show **how** entities will be implemented as relational tables.
   
   **Tools**:
   
   - Lucidchart (excellent for Crow's Foot)
   - Draw.io
   - ERDPlus
   - Inkscape (manual layout)
   
   **File to create**: ``diagrams/crows_foot_logical_model.pdf``

.. dropdown:: 📚 Entity Catalog
   :class-container: sd-border-primary

   Document **each entity** (11+ required) with complete details.
   
   **Format**: One section per entity
   
   **Required Information**:
   
   - Entity name and purpose
   - Complete attribute list with data types
   - Primary key justification
   - Business rules for this entity
   - Sample record example
   
   **Example Entry**:
   
   .. code-block:: text
   
      Entity: INTERSECTION
      
      Purpose: Represents a traffic intersection in the urban network
      
      Attributes:
      - intersection_id (INTEGER) - Unique identifier
      - intersection_name (VARCHAR(100)) - Common name
      - latitude (DECIMAL(9,6)) - Geographic coordinate
      - longitude (DECIMAL(9,6)) - Geographic coordinate
      - intersection_type (VARCHAR(50)) - Type (4-way, T, roundabout)
      - traffic_capacity (INTEGER) - Vehicles per hour
      - installation_date (DATE) - When infrastructure installed
      - jurisdiction (VARCHAR(50)) - Responsible district
      - elevation (DECIMAL(6,2)) - Meters above sea level
      
      Primary Key: intersection_id
      Justification: Surrogate key provides stable identifier even if 
                     coordinates are corrected. Auto-increment ensures uniqueness.
      
      Business Rules:
      - Traffic capacity must be positive
      - Latitude must be between -90 and 90
      - Longitude must be between -180 and 180
      - Installation date cannot be in the future
      
      Sample Record:
      (15, 'Main St & 1st Ave', 38.897957, -77.036560, '4-way', 
       1200, '2015-03-15', 'Downtown', 12.5)
   
   **File to create**: ``documentation/entity_catalog.pdf``

.. dropdown:: 🔗 Relationship Documentation
   :class-container: sd-border-primary

   Document **all relationships** between entities.
   
   **Format**: Table with columns
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Parent Entity
        - Child Entity
        - Relationship Name
        - Cardinality
        - Business Rule
        - Example Scenario
      * - INTERSECTION
        - TRAFFIC_SIGNAL
        - has
        - 1:N
        - Each intersection has 0 to many signals
        - Main St & 1st Ave has 4 signals (N, S, E, W)
      * - INTERSECTION
        - SENSOR
        - monitors
        - 1:N
        - Each intersection monitored by 0 to many sensors
        - Intersection 15 has 6 sensors (3 loops, 2 cameras, 1 radar)
      * - MAINTENANCE_CREW
        - MAINTENANCE_SCHEDULE
        - assigned_to
        - 1:N
        - Each crew assigned to 0 to many tasks
        - Crew 5 has 12 scheduled tasks this month
   
   **File to create**: ``documentation/relationship_documentation.pdf``


Task 2: Keys and Constraints
-----------------------------

**Objective**: Define keys and constraints ensuring data integrity.

.. dropdown:: 🔑 Primary Key Analysis
   :class-container: sd-border-primary
   :open:

   For **each entity**, identify and justify the primary key.
   
   **Decision Framework**:
   
   .. code-block:: text
   
      Does a natural identifier exist?
      ├─ YES: Is it stable (won't change)?
      │   ├─ YES: Is it simple (not composite)?
      │   │   ├─ YES: Consider using natural key
      │   │   └─ NO: Consider surrogate key
      │   └─ NO: Use surrogate key (natural may change)
      └─ NO: Use surrogate key (SERIAL/UUID)
   
   **Format**: Table
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Entity
        - Primary Key
        - Type
        - Data Type
        - Generation
        - Justification
      * - INTERSECTION
        - intersection_id
        - Surrogate
        - SERIAL
        - Auto-increment
        - Coordinates may be corrected; surrogate is stable
      * - TRAFFIC_SIGNAL
        - signal_id
        - Surrogate
        - SERIAL
        - Auto-increment
        - Simpler than composite (intersection_id, position)
   
   **File to create**: ``documentation/keys_analysis.pdf`` (Section 1)

.. dropdown:: 🎯 Candidate Keys
   :class-container: sd-border-primary

   Identify **alternative unique identifiers** for each entity.
   
   **Example**:
   
   .. code-block:: text
   
      Entity: INTERSECTION
      
      Primary Key: intersection_id
      
      Candidate Keys:
      1. (latitude, longitude) - Unique geographic location
         - Not chosen as PK: Composite key, may need correction
         - UNIQUE constraint: YES (prevent duplicate locations)
      
      Entity: TRAFFIC_SIGNAL
      
      Primary Key: signal_id
      
      Candidate Keys:
      1. (intersection_id, signal_position) - Unique within intersection
         - Not chosen as PK: Composite, more complex
         - UNIQUE constraint: YES (one signal per position)
   
   **File to create**: ``documentation/keys_analysis.pdf`` (Section 2)

.. dropdown:: 🔗 Foreign Key Matrix
   :class-container: sd-border-primary

   Define **referential integrity rules** for all relationships.
   
   **Format**: Table
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Child Entity
        - FK Column
        - References
        - ON DELETE
        - ON UPDATE
        - Justification
      * - TRAFFIC_SIGNAL
        - intersection_id
        - INTERSECTION(intersection_id)
        - RESTRICT
        - CASCADE
        - Prevent deleting intersection with signals; propagate ID changes
      * - SENSOR
        - intersection_id
        - INTERSECTION(intersection_id)
        - RESTRICT
        - CASCADE
        - Cannot delete intersection with active sensors
      * - INCIDENT
        - location_intersection_id
        - INTERSECTION(intersection_id)
        - SET NULL
        - CASCADE
        - Keep incident record even if intersection removed
   
   **Decision Scenarios**:
   
   *"If an intersection is removed, what happens to its traffic signals?"*
   
   - **CASCADE**: Delete all signals (equipment removed with intersection)
   - **RESTRICT**: Cannot delete intersection if signals exist (preserve data)
   - **SET NULL**: Keep signals but mark intersection_id NULL (unlikely)
   
   **File to create**: ``documentation/keys_analysis.pdf`` (Section 3)

.. dropdown:: ✅ Constraints Catalog
   :class-container: sd-border-primary

   Document **minimum 15 constraints** across all entities.
   
   **Format**: One entry per constraint
   
   **Example Entries**:
   
   .. code-block:: text
   
      Constraint #1
      Entity/Attribute: INTERSECTION.traffic_capacity
      Type: CHECK
      Business Rule: Traffic capacity must be positive (vehicles/hour)
      SQL Expression: CHECK (traffic_capacity > 0)
      Valid Example: 1200
      Invalid Example: 0, -50
      
      Constraint #2
      Entity/Attribute: INTERSECTION.latitude
      Type: CHECK
      Business Rule: Latitude must be valid coordinate (-90 to 90)
      SQL Expression: CHECK (latitude BETWEEN -90 AND 90)
      Valid Example: 38.897957
      Invalid Example: 95.5, -100
      
      Constraint #3
      Entity/Attribute: TRAFFIC_SIGNAL.signal_position
      Type: CHECK
      Business Rule: Signal position limited to cardinal directions
      SQL Expression: CHECK (signal_position IN ('north', 'south', 'east', 'west'))
      Valid Example: 'north'
      Invalid Example: 'northeast', 'left'
      
      Constraint #4
      Entity/Attribute: INCIDENT.reported_at
      Type: NOT NULL
      Business Rule: All incidents must have report timestamp
      SQL Expression: NOT NULL
      Valid Example: '2026-02-19 14:30:00'
      Invalid Example: NULL
      
      Constraint #5
      Entity/Attribute: INCIDENT.severity_level
      Type: CHECK
      Business Rule: Severity must be one of defined levels
      SQL Expression: CHECK (severity_level IN ('minor', 'moderate', 'major', 'critical'))
      Valid Example: 'major'
      Invalid Example: 'low', 'extreme'
   
   **Categories to Cover**:
   
   - Positive values (capacities, counts)
   - Valid ranges (coordinates, speeds)
   - Date logic (start < end)
   - Enumerated values (types, statuses)
   - Mandatory fields (NOT NULL)
   
   **File to create**: ``documentation/constraints_catalog.pdf``


Task 3: Normalization and Schema
---------------------------------

**Objective**: Convert ERD to normalized relational schema and prove 3NF.

.. dropdown:: 📐 Relational Schema Notation
   :class-container: sd-border-primary
   :open:

   Express **each entity** in relational notation.
   
   **Format**:
   
   .. code-block:: text
   
      ENTITY_NAME(attribute1, attribute2, attribute3, ...)
      
      Primary Key: attribute1
      Candidate Keys: (attr_x, attr_y), attr_z
      Foreign Keys: attr → PARENT_ENTITY(parent_pk)
   
   **Example**:
   
   .. code-block:: text
   
      INTERSECTION(intersection_id, intersection_name, latitude, 
                   longitude, intersection_type, traffic_capacity, 
                   installation_date, jurisdiction, elevation, notes)
      
      Primary Key: intersection_id
      Candidate Keys: (latitude, longitude)
      Foreign Keys: None
      
      TRAFFIC_SIGNAL(signal_id, intersection_id, signal_position,
                     signal_type, timing_mode, power_source,
                     last_maintenance_date, manufacturer, model_number)
      
      Primary Key: signal_id
      Candidate Keys: (intersection_id, signal_position)
      Foreign Keys: intersection_id → INTERSECTION(intersection_id)
      
      SENSOR(sensor_id, intersection_id, sensor_type, location_detail,
             installation_date, manufacturer, model, status, 
             calibration_date, data_transmission_frequency)
      
      Primary Key: sensor_id
      Candidate Keys: None
      Foreign Keys: intersection_id → INTERSECTION(intersection_id)
   
   Continue for **all 11+ entities**.
   
   **File to create**: ``documentation/relational_schema.pdf``

.. dropdown:: 🔍 Normalization Proofs
   :class-container: sd-border-primary

   Prove **each entity** is in 3NF.
   
   **For Each Entity, Verify**:
   
   **First Normal Form (1NF)**:
   
   - ✓ All attributes atomic (no arrays or lists)
   - ✓ No repeating groups
   - ✓ Each row unique (has primary key)
   - ✓ Each column single-valued
   
   **Second Normal Form (2NF)**:
   
   - ✓ In 1NF
   - ✓ No partial dependencies
   - Note: If single-attribute PK, automatically in 2NF
   - If composite PK: all non-key attributes depend on **entire** key
   
   **Third Normal Form (3NF)**:
   
   - ✓ In 2NF
   - ✓ No transitive dependencies
   - No non-key attribute determines another non-key attribute
   
   **Example Proof**:
   
   .. code-block:: text
   
      Entity: INTERSECTION
      
      Functional Dependencies:
      FD1: intersection_id → all other attributes
      FD2: (latitude, longitude) → intersection_id
      
      1NF: ✓ All attributes atomic, no repeating groups
      
      2NF: ✓ Single-attribute primary key (intersection_id)
           Automatically satisfies 2NF (no partial dependencies possible)
      
      3NF: ✓ No transitive dependencies
           Verification: No non-key determines non-key
           - jurisdiction does NOT determine anything else
           - intersection_type does NOT determine anything else
           - All non-key attributes depend only on intersection_id
      
      Conclusion: INTERSECTION is in 3NF ✓
      
      
      Entity: TRAFFIC_SIGNAL
      
      Functional Dependencies:
      FD1: signal_id → all other attributes
      FD2: (intersection_id, signal_position) → signal_id
      
      1NF: ✓ All attributes atomic
      
      2NF: ✓ Single-attribute PK, automatically in 2NF
      
      3NF: ✓ Check for transitive dependencies
           - Does manufacturer → model_number? NO (same manufacturer, different models)
           - Does signal_type → timing_mode? NO (same type can have different modes)
           - No transitive dependencies found
      
      Conclusion: TRAFFIC_SIGNAL is in 3NF ✓
   
   **File to create**: ``documentation/normalization_proofs.pdf``

.. dropdown:: ⚖️ Denormalization Analysis
   :class-container: sd-border-primary

   Analyze **3 to 5 denormalization scenarios** with cost-benefit analysis.
   
   **Scenario Template**:
   
   - **Opportunity**: What data could be denormalized?
   - **Benefits**: Faster queries? Simpler JOINs?
   - **Costs**: Redundancy? Update complexity? Staleness risk?
   - **Alternative**: Materialized view possible?
   - **Recommendation**: Keep normalized or denormalize? Why?
   
   **Example Scenario 1**:
   
   .. code-block:: text
   
      Scenario: Store incident_count_90d in INTERSECTION table
      
      Opportunity: Add incident_count_90d column to INTERSECTION
      
      Benefits:
      - Dashboard query faster (no COUNT/JOIN needed)
      - Simpler SQL for "top problematic intersections"
      - Reduces load on INCIDENT table
      
      Costs:
      - Must update INTERSECTION on every incident (trigger complexity)
      - Redundant data (duplicates count from INCIDENT table)
      - Risk of staleness if trigger fails
      - 90-day window requires recalculation logic
      
      Alternative: Materialized view refreshed daily
      CREATE MATERIALIZED VIEW intersection_incident_summary AS
      SELECT intersection_id, COUNT(*) as incident_count_90d
      FROM incident
      WHERE reported_at >= CURRENT_DATE - INTERVAL '90 days'
      GROUP BY intersection_id;
      
      Recommendation: Use materialized view
      Justification:
      - Best of both worlds (fast reads, maintains normalization)
      - Daily refresh acceptable for dashboard (not real-time critical)
      - No risk of inconsistency from failed triggers
      - Can refresh during off-peak hours
   
   **Example Scenario 2**:
   
   .. code-block:: text
   
      Scenario: Store sensor_count in INTERSECTION table
      
      Opportunity: Add sensor_count column to INTERSECTION
      
      Benefits:
      - Faster query: "intersections with fewer than 3 sensors"
      - No JOIN to SENSOR table needed
      
      Costs:
      - Update on every sensor addition/removal
      - Potential inconsistency
      
      Alternative: Computed on demand (acceptable performance)
      
      Recommendation: Keep normalized
      Justification:
      - Sensor count changes infrequently (only during installation/removal)
      - Query is not time-critical
      - Simple COUNT query performs adequately
      - Avoid redundancy and update complexity
   
   **File to create**: ``documentation/denormalization_analysis.pdf``


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP1_Traffic_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP1_Traffic_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP1_Traffic_Team{X}/
   ├── diagrams/
   │   ├── chen_conceptual_model.pdf      (or .svg)
   │   └── crows_foot_logical_model.pdf
   ├── documentation/
   │   ├── entity_catalog.pdf
   │   ├── relationship_documentation.pdf
   │   ├── keys_analysis.pdf
   │   ├── constraints_catalog.pdf
   │   ├── relational_schema.pdf
   │   ├── normalization_proofs.pdf
   │   └── denormalization_analysis.pdf
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Task 1: Entity-Relationship Diagrams
   :class-container: sd-border-info

   **Diagrams** (2 files):
   
   - ``diagrams/chen_conceptual_model.pdf`` (or ``.svg``)
   - ``diagrams/crows_foot_logical_model.pdf``
   
   **Documentation** (2 files):
   
   - ``documentation/entity_catalog.pdf``
   - ``documentation/relationship_documentation.pdf``

.. dropdown:: 📄 Task 2: Keys and Constraints
   :class-container: sd-border-info

   **Documentation** (2 files):
   
   - ``documentation/keys_analysis.pdf``
     
     - Section 1: Primary Keys
     - Section 2: Candidate Keys  
     - Section 3: Foreign Key Matrix
   
   - ``documentation/constraints_catalog.pdf``

.. dropdown:: 📄 Task 3: Normalization and Schema
   :class-container: sd-border-info

   **Documentation** (3 files):
   
   - ``documentation/relational_schema.pdf``
   - ``documentation/normalization_proofs.pdf``
   - ``documentation/denormalization_analysis.pdf``

.. dropdown:: 📄 Supporting Files
   :class-container: sd-border-info

   **Required** (2 files):
   
   - ``README.md`` - Project overview and file guide
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP1: Traffic Management System - Relational Database Design
   
   **Team Number**: [Your team number]
   
   **Scenario**: Smart City Traffic Management
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Project Overview
   
   [2-3 sentence description of your design approach]
   
   ## Key Design Decisions
   
   1. **Decision 1**: [Brief explanation and rationale]
   2. **Decision 2**: [Brief explanation and rationale]
   3. **Decision 3**: [Brief explanation and rationale]
   
   ## Entity Summary
   
   Our design includes [X] entities:
   
   1. INTERSECTION - [Brief purpose]
   2. TRAFFIC_SIGNAL - [Brief purpose]
   3. [Continue for all entities]
   
   ## File Guide
   
   - `diagrams/chen_conceptual_model.pdf` - Conceptual ER diagram in Chen notation
   - `diagrams/crows_foot_logical_model.pdf` - Logical ER diagram in Crow's Foot notation
   - `documentation/entity_catalog.pdf` - Complete documentation of all entities
   - [List all files with brief descriptions]
   
   ## Tools Used
   
   - **ER Diagrams**: [Inkscape, Lucidchart, Draw.io, etc.]
   - **Documentation**: [Google Docs, LaTeX, Microsoft Word, etc.]
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP1
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Created Chen notation ER diagram
   - Documented entities: INTERSECTION, TRAFFIC_SIGNAL, SENSOR
   - Wrote normalization proofs for 4 entities
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Created Crow's Foot ER diagram
   - Documented entities: INCIDENT, MAINTENANCE_SCHEDULE, CREW
   - Created foreign key matrix
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Documented entities: ROAD_SEGMENT, PARKING_FACILITY, WEATHER_STATION
   - Created constraints catalog (all 15+ constraints)
   - Wrote denormalization analysis
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Documented entities: EMERGENCY_ROUTE, EMERGENCY_FACILITY, TRAFFIC_ZONE
   - Created primary and candidate key analysis
   - Compiled all documentation and created README
   
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

   **Diagrams** (2 files):
   
   - [ ] Chen notation conceptual model (PDF or SVG)
   - [ ] Crow's Foot logical model (PDF)
   - [ ] Both diagrams show all 11+ entities
   - [ ] Diagrams are high resolution and legible
   
   **Documentation** (7 files):
   
   - [ ] Entity catalog (one section per entity, 11+ entities)
   - [ ] Relationship documentation (table format)
   - [ ] Keys analysis (PK, candidate keys, FK matrix)
   - [ ] Constraints catalog (15+ constraints documented)
   - [ ] Relational schema (all entities in notation)
   - [ ] Normalization proofs (1NF/2NF/3NF for each entity)
   - [ ] Denormalization analysis (3-5 scenarios)
   
   **Supporting Files** (2 files):
   
   - [ ] README.md (project overview and file guide)
   - [ ] team_contributions.md (individual contributions)
   
   **Quality Checks**:
   
   - [ ] All PDFs open correctly (not corrupted)
   - [ ] File names match specification exactly
   - [ ] All team member names in README
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP1_Traffic_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Missing files** - Forgetting one of the 11 required files
   
   ❌ **Wrong file names** - Using different naming than specification
   
   ❌ **Corrupted PDFs** - Not testing if files open before submitting
   
   ❌ **Illegible diagrams** - Low resolution, tiny text, poor layout
   
   ❌ **Incomplete catalog** - Only 8 entities when 11+ required
   
   ❌ **Missing normalization** - Proving 3NF for only some entities
   
   ❌ **No team contributions** - Required for every GP!
   
   ❌ **Wrong ZIP naming** - Not following ``GP1_Traffic_Team{X}.zip`` format


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Task 1: ERD**
     - 4
     - All required entities (1pt); Relationships correct (1.5pts); Proper notation (1pt); Complete documentation (0.5pt)
   * - **Task 2: Keys & Constraints**
     - 3
     - Primary keys well-chosen (1pt); Foreign keys with proper rules (1pt); 15+ constraints documented (1pt)
   * - **Task 3: Normalization**
     - 3
     - Correct relational schema (1pt); Complete 3NF proofs (1pt); Thoughtful denormalization analysis (1pt)
   * - **Total**
     - **10**
     - 


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP1**
   
   - **Start early** - This requires substantial work and iteration. Your first ERD draft will not be your final version!
   - **Meet regularly** - Schedule 2-3 team meetings per week. Divide work but review together.
   - **Use office hours** - Bring your ERD sketches for feedback. Discuss design trade-offs with instructors.
   - **Test scenarios** - Walk through real workflows: "How would we query for intersections with high incident rates?" If your design makes this difficult, reconsider.
   - **Document as you go** - Don't wait until the end to write documentation. Capture decisions and rationale as you make them.


Next Steps
----------

After completing GP1, you will:

- Receive feedback from instructors
- Identify needed changes to your design
- Begin GP2: Implementing this schema in PostgreSQL
- Generate sample data and write SQL queries

.. note::
   
   **Your GP1 design is the foundation** for GP2 (PostgreSQL implementation), GP3 (MongoDB integration), and GP4 (complete system).
   
   A strong relational design now makes implementation much easier later!