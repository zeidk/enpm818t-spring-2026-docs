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

Your team will design and implement a comprehensive database system for a metropolitan city managing traffic flow across 500+ intersections. The system must handle traffic control, historical pattern analysis, incident management, and infrastructure maintenance. You will build this system progressively across four group projects, using three complementary databases.

.. important::

   **Polyglot Persistence Architecture**

   This scenario uses **three complementary databases**, each chosen for its strengths:

   - **PostgreSQL** for structured infrastructure and operational data
   - **MongoDB** for high-volume traffic events and flexible sensor schemas
   - **Redis** for real-time signal states and caching


Technology Stack
----------------

.. tab-set::

   .. tab-item:: PostgreSQL

      .. card:: Relational Database for Infrastructure

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

         - Traffic flow events (high-volume time-series data)
         - Sensor readings with variable structure (camera, radar, lidar)
         - Incident reports with embedded witness statements
         - Congestion patterns

         **Why MongoDB**:

         - High write throughput
         - Flexible schema per sensor type
         - TTL indexes for automatic data expiration
         - Efficient aggregation pipelines

   .. tab-item:: Redis

      .. card:: In-Memory Store for Real-Time State
         :class-card: sd-bg-light

         **Purpose**: Sub-millisecond access to frequently changing real-time state

         **What Data**:

         - Current signal states (red/yellow/green)
         - Live intersection metrics (vehicle count, avg speed)
         - Real-time congestion rankings
         - Recent incident queue
         - Traffic alert broadcasting (pub/sub)

         **Why Redis**:

         - In-memory storage for sub-millisecond latency
         - Built-in data structures (sorted sets, streams)
         - Pub/sub for real-time alerts
         - Automatic expiration (TTL)


Progressive Development
-----------------------

.. admonition:: Four Cumulative Projects
   :class: tip

   Each group project builds on the previous work, creating a complete system by the end.

.. list-table::
   :header-rows: 1
   :widths: 10 25 10 55
   :class: compact-table

   * - Project
     - Focus
     - Duration
     - Key Deliverables
   * - **GP1**
     - Relational Design
     - 2 weeks
     - Chen ERD, Crow's Foot ERD, design report (8 to 12 pages)
   * - **GP2**
     - PostgreSQL + Python
     - 3 weeks
     - Schema DDL, complex SQL queries, Python CLI application
   * - **GP3**
     - MongoDB Integration
     - 2 weeks
     - Document schemas, aggregation pipelines, cross-database services
   * - **GP4**
     - Complete System
     - 2 weeks
     - Redis caching, Docker deployment, 8-to-12-page technical report


.. dropdown:: GP1: Relational Database Design (2 weeks)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Design the PostgreSQL schema for infrastructure and operations:

   - Create **Conceptual Model** using Chen notation with (min,max) constraints
   - Create **Logical Model** using Crow's Foot notation
   - Write a consolidated design report (entities, keys, normalization, denormalization)

   **Deliverables**: Chen ERD, Crow's Foot ERD, design report (8 to 12 pages)

.. dropdown:: GP2: PostgreSQL + Python Implementation (5 weeks)
   :icon: gear
   :class-container: sd-border-primary

   Implement and integrate the relational database:

   - Create schema with tables, indexes, constraints, triggers
   - Generate realistic sample data using the provided prompt guide
   - Write 8+ SQL queries (JOINs, aggregates, subqueries, geospatial)
   - Build a Python CLI application with menu-driven interface
   - Implement repository and service layer architecture

   **Deliverables**: SQL scripts, Python application, query catalog, architecture docs

.. dropdown:: GP3: MongoDB Integration (2 weeks)
   :icon: gear
   :class-container: sd-border-primary

   Add document database for high-volume traffic data:

   - Design 4+ MongoDB collections for event data
   - Choose embedding vs. referencing strategies
   - Write 6+ aggregation pipelines and geospatial queries
   - Integrate with PostgreSQL application
   - Implement cross-database operations

   **Deliverables**: MongoDB schemas, queries, Python integration, polyglot design document

.. dropdown:: GP4: Redis + Complete System (2 weeks)
   :icon: gear
   :class-container: sd-border-primary

   Add caching layer and complete the system:

   - Design 5+ Redis data structures (strings, hashes, sorted sets, lists, pub/sub)
   - Implement cache-aside pattern
   - Build pub/sub for real-time alerts
   - Deploy with Docker Compose
   - Write final technical report (8 to 12 pages)

   **Deliverables**: Redis implementation, integrated system, deployment, final report


Key Design Challenges
---------------------

.. warning::

   **Critical Decisions You'll Make**

   These choices will significantly impact your system's architecture and maintainability.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Challenge 1: Data Partitioning

      **Question**: Which data belongs in which database?

      **Considerations**:

      - PostgreSQL: Structured, relational, transactional
      - MongoDB: High-volume, flexible schema, append-mostly
      - Redis: Frequently accessed, rapidly changing, cacheable

      You must justify every decision.

   .. grid-item-card:: Challenge 2: Cross-Database Queries

      **Question**: How do you query data spanning multiple databases?

      **Approaches**:

      - Application-level joins
      - Data denormalization
      - Caching strategies
      - Event-driven synchronization

   .. grid-item-card:: Challenge 3: Data Consistency

      **Question**: How do you maintain consistency across databases?

      **Options**:

      - Eventual consistency (accept temporary inconsistencies)
      - Saga pattern (compensating transactions)
      - Single source of truth with derived views

   .. grid-item-card:: Challenge 4: Caching Strategy

      **Question**: What data should be cached and for how long?

      **Strategies**:

      - Strategic caching (Redis)
      - Proper indexing (PostgreSQL, MongoDB)
      - Query optimization
      - TTL-based expiration


Learning Objectives
-------------------

.. admonition:: What You'll Master
   :class: note

   By completing this scenario, you will be able to:

   - Design relational schemas for infrastructure with geospatial data
   - Implement PostGIS queries for location-based operations
   - Model high-volume time-series data in document databases
   - Use MongoDB aggregation pipelines for traffic analytics
   - Design Redis data structures for real-time state management
   - Implement caching strategies for performance optimization
   - Build a Python application serving data from multiple databases
   - Deploy polyglot systems using Docker Compose
   - Handle data consistency across multiple databases


Success Criteria
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Category
     - Evaluation Criteria
   * - **Functionality** (30%)
     - All required features implemented; queries return correct results; application works as documented
   * - **Design Quality** (25%)
     - Appropriate database selection; well-normalized PostgreSQL schema; efficient MongoDB documents; strategic Redis caching
   * - **Code Quality** (20%)
     - Clean, readable code; proper error handling; good documentation; layered architecture
   * - **Technical Report** (15%)
     - Clear architecture explanation; design decisions justified; trade-offs analyzed; professional presentation
   * - **Performance Analysis** (10%)
     - Efficient query execution; proper index usage; caching impact measured


Getting Started
---------------

.. tip::

   **First Steps**

   1. Review this specification thoroughly
   2. Form your team (4 students)
   3. Discuss whether this scenario interests your team
   4. Compare with Scenario 2 (Healthcare)
   5. Submit scenario choice via Canvas

.. admonition:: Project Timeline
   :class: important

   Once you begin:

   - **Immediately**: Read business requirements carefully
   - **First Few Days**: Identify entities (intersections, sensors, etc.)
   - **Throughout GP1**: Sketch initial ERD, identify relationships
   - **Continuously**: Use office hours for questions

   **Pro Tips**:

   - Start early: each GP takes substantial time
   - Meet regularly as a team (2 to 3 times per week)
   - Use version control from Day 1 (Git/GitHub)
   - Document decisions as you make them


Support Resources
-----------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Office Hours
      :class-card: sd-border-info

      - Bring specific questions and work in progress
      - Show your ERD sketches for feedback
      - Discuss design trade-offs
      - Debug complex queries
      - Review architecture decisions

   .. grid-item-card:: Discussion Forum
      :class-card: sd-border-info

      - Post clarification questions
      - Share general challenges (not code)
      - Learn from other teams' questions
      - Collaborative problem-solving

.. card:: Technical Documentation

   - **PostGIS**: https://postgis.net/documentation/
   - **MongoDB Geospatial**: https://docs.mongodb.com/manual/geospatial-queries/
   - **Redis Data Structures**: https://redis.io/docs/data-types/
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
   data_generation_guide
