====================================================
Scenario 1: Smart City Traffic Management System
====================================================

.. only:: html

   .. figure:: /_static/images/final_project/traffic_intersections_light.png
      :alt: Smart City Traffic Intersection Network (credit OpenAI)
      :width: 80%
      :align: center
      :class: only-light

      *Intelligent traffic management across 500+ urban intersections (credit OpenAI)*

   .. figure:: /_static/images/final_project/traffic_intersections_dark.png
      :alt: Smart City Traffic Intersection Network (credit OpenAI)
      :width: 80%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/final_project/traffic_intersections_light.png
      :alt: Smart City Traffic Intersection Network
      :width: 80%
      :align: center

      *Intelligent traffic management across 500+ urban intersections*

Overview
--------

Your team will design and implement a comprehensive database system for a metropolitan city managing traffic flow across 500+ intersections. The system must handle real-time traffic control, historical pattern analysis, incident management, and infrastructure maintenance while providing sub-second response times for critical operations.

.. important::
   
   **Polyglot Persistence Architecture**
   
   This scenario demonstrates the power of using **three complementary databases**:
   
   - **PostgreSQL** for structured infrastructure and operational data
   - **MongoDB** for high-volume traffic events and flexible sensor schemas
   - **Redis** for real-time signal states and sub-millisecond caching


System Requirements
-------------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🚦 Core Capabilities
      :class-card: sd-border-primary
      
      - Infrastructure management (intersections, signals, sensors)
      - Real-time traffic monitoring and signal control
      - Incident detection and emergency response
      - Maintenance scheduling and crew coordination
      - Historical traffic pattern analysis
      - Weather condition monitoring

   .. grid-item-card:: ⚡ Performance Requirements
      :class-card: sd-border-success
      
      - 1,000+ sensor readings per second
      - API response < 100ms for real-time queries
      - 500+ concurrent API users
      - 90-day data retention
      - Sub-second cache refresh


Technology Stack
----------------

.. tab-set::

   .. tab-item:: PostgreSQL

      .. card:: Relational Database for Infrastructure
         :class-card: sd-bg-light
      
         **Purpose**: Structured data with strong consistency and complex relationships
         
         **What Data**:
         
         - Intersection details (location, type, capacity, jurisdiction)
         - Traffic signals and sensors (configuration, status, maintenance)
         - Road network (segments, lanes, speed limits)
         - Maintenance schedules and crew assignments
         - Incidents (accidents, breakdowns, hazards)
         - Emergency routes and facilities
         
         **Why PostgreSQL**:
         
         - Complex relationships between infrastructure
         - ACID transactions for scheduling
         - PostGIS for geospatial queries
         - Mature indexing for complex JOINs
         - Referential integrity enforcement

   .. tab-item:: MongoDB

      .. card:: Document Database for Events
         :class-card: sd-bg-light
      
         **Purpose**: High-volume, write-heavy traffic event data with flexible schemas
         
         **What Data**:
         
         - Traffic flow events (1.4M documents/day)
         - Sensor readings with variable structure (camera, radar, lidar)
         - Connected vehicle telemetry
         - Incident reports with embedded witness statements
         - Traffic predictions from ML models
         - Congestion patterns
         
         **Why MongoDB**:
         
         - High write throughput (1000+ inserts/sec)
         - Flexible schema per sensor type
         - TTL indexes for automatic data expiration
         - Efficient aggregation pipelines
         - Horizontal scalability

   .. tab-item:: Redis

      .. card:: In-Memory Store for Real-Time State
         :class-card: sd-bg-light
      
         **Purpose**: Sub-millisecond access to frequently changing real-time state
         
         **What Data**:
         
         - Current signal states (red/yellow/green)
         - Live intersection metrics (vehicle count, avg speed)
         - Real-time congestion rankings
         - Recent incident queue
         - Active connected vehicles by grid sector
         - Sensor data streams
         - Traffic alert broadcasting (pub/sub)
         
         **Why Redis**:
         
         - In-memory storage for sub-millisecond latency
         - Built-in data structures (sorted sets, streams)
         - Pub/sub for real-time alerts
         - Automatic expiration (TTL)
         - Atomic operations


Progressive Development
-----------------------

.. admonition:: 🏗️ Four Cumulative Projects
   :class: tip

   Each group project builds on the previous work, creating a complete system by the end!

.. list-table::
   :header-rows: 1
   :widths: 15 30 15 40
   :class: compact-table

   * - Project
     - Focus
     - Duration
     - Key Deliverables
   * - **GP1**
     - Relational Design
     - 2 weeks
     - Chen & Crow's Foot ERDs, Normalization
   * - **GP2**
     - PostgreSQL + Python
     - 3 weeks
     - Schema, Queries, REST API, Tests
   * - **GP3**
     - MongoDB Integration
     - 2 weeks
     - Document schemas, Aggregations, Integration
   * - **GP4**
     - Complete System
     - 3 weeks
     - Redis caching, Docker deployment, Final report


.. dropdown:: 🔍 GP1: Relational Database Design (2 weeks)
   :class-container: sd-border-primary
   :open:

   Design the PostgreSQL schema for infrastructure and operations:
   
   - Create **Conceptual Model** using Chen notation
   - Create **Logical Model** using Crow's Foot notation
   - Identify 11+ entities from business requirements
   - Define primary keys, foreign keys, constraints
   - Normalize to 3NF with functional dependency analysis
   - Analyze denormalization trade-offs
   
   **Deliverables**: ERDs (both notations), entity catalog, normalization proofs

.. dropdown:: 💻 GP2: PostgreSQL + Python Implementation (3 weeks)
   :class-container: sd-border-primary

   Implement and integrate the relational database:
   
   - Create schema with tables, indexes, constraints, triggers
   - Generate realistic sample data (10+ records per table)
   - Write 10+ complex queries (JOINs, CTEs, window functions, geospatial)
   - Build Python application with repositories and services
   - Create REST API with FastAPI
   - Write comprehensive tests (>70% coverage)
   
   **Deliverables**: SQL scripts, Python application, API docs, test suite

.. dropdown:: 📊 GP3: MongoDB Integration (2 weeks)
   :class-container: sd-border-primary

   Add document database for high-volume traffic data:
   
   - Design 10+ MongoDB collections for event data
   - Choose embedding vs. referencing strategies
   - Create indexes for query optimization
   - Write 8+ aggregation pipelines and geospatial queries
   - Integrate with PostgreSQL application
   - Implement cross-database operations
   
   **Deliverables**: MongoDB schemas, queries, Python integration, performance analysis

.. dropdown:: 🚀 GP4: Redis + Complete System (3 weeks)
   :class-container: sd-border-primary

   Add caching layer and complete the system:
   
   - Design 8+ Redis data structures (strings, hashes, sorted sets, streams)
   - Implement cache-aside pattern
   - Build pub/sub for real-time alerts
   - Create APIs using all three databases
   - Deploy with Docker Compose
   - Write comprehensive technical report (10 to 15 pages)
   
   **Deliverables**: Redis implementation, integrated system, deployment, final report


Key Design Challenges
---------------------

.. warning::
   
   **Critical Decisions You'll Make**
   
   These aren't trivial choices - they'll significantly impact your system's performance and maintainability!

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🎯 Challenge 1: Data Partitioning
      
      **Question**: Which data belongs in which database?
      
      **Considerations**:
      
      - PostgreSQL: Structured, relational, transactional
      - MongoDB: High-volume, flexible schema, append-mostly
      - Redis: Frequently accessed, rapidly changing, cacheable
      
      You must justify every decision!

   .. grid-item-card:: 🔗 Challenge 2: Cross-Database Queries
      
      **Question**: How do you query data spanning multiple databases?
      
      **Approaches**:
      
      - Application-level joins
      - Data denormalization
      - Caching strategies
      - Event-driven synchronization
      
      Trade-offs matter!

   .. grid-item-card:: 🔄 Challenge 3: Data Consistency
      
      **Question**: How do you maintain consistency across databases?
      
      **Options**:
      
      - Eventual consistency (accept temporary inconsistencies)
      - Two-phase commit (complex, rarely used)
      - Saga pattern (compensating transactions)
      - Single source of truth with derived views

   .. grid-item-card:: ⚡ Challenge 4: Real-Time Performance
      
      **Question**: How do you achieve <100ms API response times?
      
      **Strategies**:
      
      - Strategic caching (Redis)
      - Proper indexing (PostgreSQL, MongoDB)
      - Query optimization
      - Connection pooling
      - Asynchronous operations


Learning Objectives
-------------------

.. admonition:: 🎓 What You'll Master
   :class: note

   By completing this scenario, you will:
   
   ✅ Design relational schemas for infrastructure with geospatial data
   
   ✅ Implement PostGIS queries for location-based operations
   
   ✅ Model high-volume time-series data in document databases
   
   ✅ Use MongoDB aggregation pipelines for traffic analytics
   
   ✅ Design Redis data structures for real-time state management
   
   ✅ Implement caching strategies for performance optimization
   
   ✅ Build APIs serving data from multiple databases
   
   ✅ Deploy polyglot systems using Docker Compose
   
   ✅ Handle data consistency across multiple databases


Success Criteria
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Category
     - Evaluation Criteria
   * - **Functionality** (30%)
     - All required features implemented; Queries return correct results; APIs work as documented; System handles concurrent users
   * - **Design Quality** (25%)
     - Appropriate database selection; Well-normalized PostgreSQL schema; Efficient MongoDB documents; Strategic Redis caching; Clean architecture
   * - **Performance** (15%)
     - Meets response time requirements; Efficient query execution; Proper index usage; Scalability considerations
   * - **Code Quality** (15%)
     - Clean, readable code; Proper error handling; Comprehensive tests; Good documentation
   * - **Technical Report** (15%)
     - Clear architecture explanation; Design decisions justified; Trade-offs analyzed; Professional presentation


Common Pitfalls
---------------

.. danger::
   
   **Avoid These Mistakes!**
   
   Learn from past teams' experiences:

.. grid:: 2
   :gutter: 2

   .. grid-item::
      
      ❌ **Over-normalizing MongoDB**
      
      Don't treat it like a relational database. Embrace document embedding!

   .. grid-item::
      
      ❌ **Under-normalizing PostgreSQL**
      
      Missing normalization opportunities leads to update anomalies.

   .. grid-item::
      
      ❌ **Caching everything in Redis**
      
      Memory is limited. Be strategic about what you cache.

   .. grid-item::
      
      ❌ **Ignoring indexes**
      
      Poor query performance is often just missing indexes.

   .. grid-item::
      
      ❌ **Tight coupling between databases**
      
      Keep databases loosely coupled for maintainability.

   .. grid-item::
      
      ❌ **No error handling**
      
      Databases fail. Handle it gracefully!


Getting Started
---------------

.. tip::
   
   **First Steps**
   
   1. Review this specification thoroughly
   2. Form your team (4 students)
   3. Discuss whether this scenario interests your team
   4. Compare with Scenario 2 (Healthcare)
   5. Submit scenario choice via Canvas

.. admonition:: 📅 Project Timeline
   :class: important

   Once you begin:
   
   - **Immediately**: Read business requirements carefully
   - **First Few Days**: Identify entities (intersections, sensors, etc.)
   - **Throughout GP1**: Sketch initial ERD, identify relationships
   - **Continuously**: Use office hours for questions
   
   **Pro Tips**:
   
   - Start early - each GP takes substantial time
   - Meet regularly as a team (2-3 times per week)
   - Use version control from Day 1 (Git/GitHub)
   - Document decisions as you make them


Support Resources
-----------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 👥 Office Hours
      :class-card: sd-border-info
      
      - Bring specific questions and work in progress
      - Show your ERD sketches for feedback
      - Discuss design trade-offs
      - Debug complex queries
      - Review architecture decisions

   .. grid-item-card:: 💬 Discussion Forum
      :class-card: sd-border-info
      
      - Post clarification questions
      - Share general challenges (not code)
      - Learn from other teams' questions
      - Collaborative problem-solving

.. card:: 📚 Technical Documentation
   :class-card: sd-bg-light
   
   - **PostGIS**: https://postgis.net/documentation/
   - **MongoDB Geospatial**: https://docs.mongodb.com/manual/geospatial-queries/
   - **Redis Data Structures**: https://redis.io/docs/data-types/
   - **FastAPI**: https://fastapi.tiangolo.com/
   - **Docker Compose**: https://docs.docker.com/compose/


Project Details
---------------

.. toctree::
   :maxdepth: 1
   :caption: Group Projects

   project1
   project2
   project3
   project4


What's Next?
------------

.. admonition:: 🚀 Ready to Build?
   :class: seealso

   - Review all four Group Project specifications
   - Discuss with your team whether traffic management excites you
   - Compare with Scenario 2 (Healthcare + HIPAA compliance)
   - Make your scenario selection
   - Begin sketching initial entity ideas!

.. note::
   
   **Remember**: This is a portfolio-worthy project. Take pride in your work, ask questions when stuck, and enjoy building a real-world polyglot persistence system!