====================================================
Group Project 2: PostgreSQL + Python Integration
====================================================

Overview
--------

Implement your GP1 design in PostgreSQL, populate with realistic data, write complex SQL queries supporting traffic operations, and build a Python application with REST API.

**Timeline**: 6 weeks

**Weight**: 15 points (37.5% of final project)

**Team Size**: 4 students

**Builds on**: Your GP1 relational design


.. important::
   
   **What You'll Deliver**
   
   This project requires a **complete PostgreSQL implementation** with Python integration:
   
   - 3 SQL files (schema, data, queries)
   - 4 documentation files (index strategy, query catalog, architecture, API docs)
   - 1 Python application (config, models, repositories, services, API)
   - 1 test suite with coverage report
   - 1 README file
   
   **Submission**: Single ZIP file named ``GP2_Traffic_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Translate conceptual designs into physical PostgreSQL schemas
- Write DDL with tables, constraints, indexes, and triggers
- Generate realistic test data respecting all constraints
- Master complex SQL (JOINs, CTEs, window functions, geospatial queries)
- Optimize queries using indexes and EXPLAIN ANALYZE
- Integrate PostgreSQL with Python using psycopg2
- Design repository and service layer architecture
- Build REST APIs with FastAPI
- Write comprehensive tests (>70% coverage)


Part 1: Physical Database Implementation
-----------------------------------------

**Objective**: Transform your GP1 design into a working PostgreSQL database with realistic data.

.. dropdown:: 📋 Task 1.1: Schema Implementation (3 points)
   :class-container: sd-border-primary
   :open:

   Create ``schema.sql`` with:
   
   - **Database setup**: Extensions (PostGIS for geospatial)
   - **Custom types**: ENUMs for constrained values
   - **All tables**: Complete with all columns from GP1
   - **Primary keys**: All defined correctly
   - **Foreign keys**: With ON DELETE/UPDATE rules from GP1
   - **Check constraints**: All business rules (15+ constraints)
   - **NOT NULL constraints**: All mandatory fields
   - **UNIQUE constraints**: All candidate keys
   - **Indexes**: Strategic indexes for query performance
   - **Triggers**: Automatic updated_at timestamps
   
   **PostGIS Integration**:
   
   .. code-block:: sql
   
      CREATE EXTENSION IF NOT EXISTS postgis;
      
      ALTER TABLE intersection 
      ADD COLUMN location GEOGRAPHY(POINT, 4326);
      
      CREATE INDEX idx_intersection_location 
      ON intersection USING GIST (location);
   
   **File to create**: ``postgresql/schema.sql``

.. dropdown:: 📋 Task 1.2: Index Strategy
   :class-container: sd-border-primary

   For each index, document:
   
   - **Purpose**: What queries does this speed up?
   - **Type**: B-tree (default), GIST (spatial), GIN (full-text)
   - **Cost**: Impact on write performance
   - **Justification**: Why benefits outweigh costs
   
   **Common Patterns**:
   
   - Foreign keys: Always index for JOIN performance
   - Frequently filtered columns: Index if selective
   - Geospatial: Use GIST indexes
   - Composite: Consider query patterns (WHERE + ORDER BY)
   
   **Example Entry**:
   
   .. code-block:: text
   
      Index: idx_incident_severity_reported
      Table: incident
      Columns: (severity_level, reported_at DESC)
      Type: B-tree (composite)
      
      Purpose: Speeds up dashboard query "recent critical incidents"
      Query Pattern: WHERE severity_level = 'critical' ORDER BY reported_at DESC
      
      Justification:
      - This query runs every 30 seconds on the operations dashboard
      - Without index: sequential scan on 75+ incident rows
      - With index: direct lookup + already sorted
      - Write cost: Minimal (incidents inserted ~10/day)
   
   **File to create**: ``docs/index_strategy.md``

.. dropdown:: 📋 Task 1.3: Sample Data Generation (2 points)
   :class-container: sd-border-primary

   Create ``data.sql`` with minimum data volumes:
   
   - 50+ intersections in realistic city grid
   - 100+ traffic signals across intersections
   - 150+ sensors (multiple per intersection)
   - 50+ road segments connecting intersections
   - 100+ maintenance records (various dates)
   - 10+ maintenance crews
   - 75+ incidents (last 90 days)
   - 20+ emergency routes
   - 10+ emergency facilities
   - 5+ weather stations
   - 10+ parking facilities
   - 5+ traffic control zones
   
   **Realistic Patterns**:
   
   - Geographic clustering (downtown vs. suburbs)
   - Temporal distribution (incidents during rush hour)
   - Logical relationships (sensors match intersection type)
   - Edge cases (NULL optional fields, boundary values)
   
   **Data Quality Checks**:
   
   .. code-block:: text
   
      After loading data, verify:
      
      1. All FK references resolve (no orphan records)
      2. All CHECK constraints pass
      3. Geographic coordinates form a realistic grid
      4. Temporal data spans at least 90 days
      5. Every intersection has at least one signal
      6. Every zone contains multiple intersections
   
   **File to create**: ``postgresql/data.sql``


Part 2: Complex SQL Queries
----------------------------

**Objective**: Write 10+ queries demonstrating mastery of SQL features.

.. dropdown:: 📋 Multi-Table JOINs (2 queries minimum)
   :class-container: sd-border-primary
   :open:

   Combine 4+ tables to answer business questions.
   
   **Example Challenge**: 
   *"Which intersections have the most incidents, and what is the maintenance status of their infrastructure?"*
   
   Requires: INTERSECTION, INCIDENT, TRAFFIC_SIGNAL, MAINTENANCE_SCHEDULE

.. dropdown:: 📋 Aggregate Functions (2 queries minimum)
   :class-container: sd-border-primary

   Use COUNT, SUM, AVG, MIN, MAX with GROUP BY and HAVING.
   
   **Example Challenge**:
   *"Calculate average incident resolution time by severity level and zone"*

.. dropdown:: 📋 Window Functions (2 queries minimum)
   :class-container: sd-border-primary

   Use RANK(), ROW_NUMBER(), NTILE(), or aggregate window functions.
   
   **Example Challenge**:
   *"Rank intersections by incident count with running totals and 7-day moving average"*

.. dropdown:: 📋 CTEs and Subqueries (2 queries minimum)
   :class-container: sd-border-primary

   Use Common Table Expressions for complex logic.
   
   **Example Challenge**:
   *"Find intersections with above-average incident rates in their zone"*

.. dropdown:: 📋 Advanced Features (2 queries minimum)
   :class-container: sd-border-primary

   Choose from:
   
   - **Recursive CTEs**: Route finding between intersections
   - **PostGIS Geospatial**: Find infrastructure within 500m of incidents
   - **ROLLUP/CUBE**: Hierarchical summaries by zone/type/severity
   - **Materialized Views**: Pre-computed performance metrics

.. dropdown:: 📋 Query Documentation Template
   :class-container: sd-border-primary

   Use this format for **every query** in ``queries.sql``:
   
   .. code-block:: sql
   
      -- Query #X: [Title]
      -- Business Question: [Problem being solved]
      -- Complexity Features: [JOINs, aggregates, windows used]
      -- Tables Used: [List all tables]
      -- Index Usage: [Which indexes help this query]
      -- Performance Notes: [Execution time, row estimates]
      
      [YOUR SQL QUERY]
      
      -- Expected Output: [Description of result columns]
      -- Sample Results: [First 3 rows with representative data]
   
   **File to create**: ``postgresql/queries.sql``

.. dropdown:: 📋 Query Catalog
   :class-container: sd-border-primary

   Create a summary document cataloging all queries:
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Query #
        - Title
        - Category
        - Tables Used
        - Key Features
      * - 1
        - High-Incident Intersections
        - Multi-Table JOIN
        - INTERSECTION, INCIDENT, SIGNAL, MAINTENANCE
        - 4-table JOIN, COUNT, GROUP BY
      * - 2
        - Resolution Time by Severity
        - Aggregate
        - INCIDENT, TRAFFIC_ZONE
        - AVG, HAVING, date arithmetic
   
   Include EXPLAIN ANALYZE output for **at least 5 queries** showing:
   
   - Execution plan (index scans vs. sequential scans)
   - Actual vs. estimated rows
   - Total execution time
   - Buffer usage
   
   **File to create**: ``docs/query_catalog.md``


Part 3: Python Integration
---------------------------

**Objective**: Build a layered Python application connecting to your PostgreSQL database.

.. dropdown:: 📋 Task 3.1: Application Architecture (5 points)
   :class-container: sd-border-primary
   :open:

   .. code-block:: text
   
      traffic-management/
      ├── requirements.txt
      ├── .env.example
      ├── config/
      │   └── database.py          # Connection pooling
      ├── models/
      │   ├── intersection.py      # Dataclasses
      │   └── [other models].py
      ├── repositories/
      │   ├── base_repository.py
      │   ├── intersection_repo.py # CRUD operations
      │   └── [other repos].py
      ├── services/
      │   └── traffic_service.py   # Business logic
      ├── api/
      │   └── endpoints.py         # FastAPI routes
      └── tests/

.. dropdown:: 📋 Connection Management
   :class-container: sd-border-primary

   Implement connection pooling with psycopg2:
   
   - Pool size: 2-10 connections
   - Context manager for automatic cleanup
   - Error handling for connection failures
   - Configuration from environment variables
   
   **Example**:
   
   .. code-block:: python
   
      from psycopg2 import pool
      import os
      
      class DatabaseConfig:
          _pool = None
          
          @classmethod
          def get_pool(cls):
              if cls._pool is None:
                  cls._pool = pool.SimpleConnectionPool(
                      minconn=2,
                      maxconn=10,
                      host=os.getenv("DB_HOST", "localhost"),
                      port=os.getenv("DB_PORT", "5432"),
                      dbname=os.getenv("DB_NAME", "traffic_management"),
                      user=os.getenv("DB_USER", "postgres"),
                      password=os.getenv("DB_PASSWORD")
                  )
              return cls._pool

.. dropdown:: 📋 Repository Pattern
   :class-container: sd-border-primary

   Each major entity needs a repository with:
   
   - ``find_by_id(id)`` - Single record lookup
   - ``find_all(limit, offset)`` - Paginated list
   - ``create(entity)`` - Insert new record
   - ``update(entity)`` - Update existing
   - ``delete(id)`` - Remove record
   - Custom query methods (e.g., ``find_by_zone(zone_id)``)
   
   **Example**:
   
   .. code-block:: python
   
      class IntersectionRepository:
          def __init__(self, pool):
              self.pool = pool
          
          def find_by_id(self, intersection_id):
              conn = self.pool.getconn()
              try:
                  with conn.cursor() as cur:
                      cur.execute(
                          "SELECT * FROM intersection WHERE intersection_id = %s",
                          (intersection_id,)
                      )
                      row = cur.fetchone()
                      return Intersection.from_row(row) if row else None
              finally:
                  self.pool.putconn(conn)

.. dropdown:: 📋 Task 3.2: REST API (3 points)
   :class-container: sd-border-primary

   Implement **at least 8 endpoints**:
   
   **Basic CRUD** (3 minimum):
   
   - ``GET /intersections/{id}`` - Retrieve intersection
   - ``GET /intersections`` - List with pagination
   - ``GET /incidents/recent`` - Recent incidents with filters
   
   **Complex Queries** (3 minimum):
   
   - ``GET /intersections/high-incident`` - Problematic intersections
   - ``GET /analytics/incident-trends`` - Trends over time
   - ``GET /maintenance/overdue`` - Overdue maintenance tasks
   
   **Geospatial** (1 minimum):
   
   - ``GET /intersections/nearby?lat={lat}&lon={lon}&radius={m}``
   
   **Analytics** (1 minimum):
   
   - ``GET /analytics/performance`` - System-wide metrics

.. dropdown:: 📋 API Documentation
   :class-container: sd-border-primary

   FastAPI provides automatic Swagger docs. Ensure:
   
   - All endpoints have descriptions
   - Query parameters documented
   - Response models defined
   - Example responses provided
   - Error responses documented
   
   **File to create**: ``docs/api_documentation.md``


Part 4: Testing
---------------

**Objective**: Write automated tests covering all application layers.

.. dropdown:: 📋 Task 4.1: Test Categories (integrated into score)
   :class-container: sd-border-primary
   :open:

   **Repository Tests**:
   
   - CRUD operations work correctly
   - Complex queries return expected results
   - Error handling (constraint violations, not found)
   
   **Service Tests**:
   
   - Business logic functions correctly
   - Multi-repository operations
   - Edge cases handled
   
   **API Tests**:
   
   - Endpoints return correct status codes
   - Response format matches specification
   - Input validation works
   - Error responses appropriate

**Requirements**: Minimum 70% code coverage


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP2_Traffic_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP2_Traffic_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP2_Traffic_Team{X}/
   ├── postgresql/
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── src/
   │   ├── config/
   │   │   └── database.py
   │   ├── models/
   │   │   ├── intersection.py
   │   │   └── [other models].py
   │   ├── repositories/
   │   │   ├── base_repository.py
   │   │   ├── intersection_repo.py
   │   │   └── [other repos].py
   │   ├── services/
   │   │   └── traffic_service.py
   │   └── api/
   │       └── endpoints.py
   ├── tests/
   │   ├── test_repositories.py
   │   ├── test_services.py
   │   └── test_api.py
   ├── docs/
   │   ├── index_strategy.md
   │   ├── query_catalog.md
   │   ├── architecture.md
   │   └── api_documentation.md
   ├── requirements.txt
   ├── .env.example
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Part 1: Physical Database Implementation
   :class-container: sd-border-info

   **SQL Files** (3 files):
   
   - ``postgresql/schema.sql`` - Complete DDL with constraints, indexes, triggers
   - ``postgresql/data.sql`` - Realistic sample data meeting volume requirements
   - ``postgresql/queries.sql`` - 10+ documented queries
   
   **Documentation** (2 files):
   
   - ``docs/index_strategy.md`` - Index justifications
   - ``docs/query_catalog.md`` - Query summaries with EXPLAIN ANALYZE

.. dropdown:: 📄 Part 3: Python Integration
   :class-container: sd-border-info

   **Application** (full src/ directory):
   
   - ``src/config/database.py`` - Connection pooling
   - ``src/models/*.py`` - Dataclass models
   - ``src/repositories/*.py`` - CRUD and custom queries
   - ``src/services/*.py`` - Business logic layer
   - ``src/api/endpoints.py`` - FastAPI routes
   
   **Documentation** (2 files):
   
   - ``docs/architecture.md`` - Application architecture overview
   - ``docs/api_documentation.md`` - API endpoint documentation

.. dropdown:: 📄 Part 4: Testing + Supporting Files
   :class-container: sd-border-info

   **Tests** (3+ files):
   
   - ``tests/test_repositories.py``
   - ``tests/test_services.py``
   - ``tests/test_api.py``
   
   **Supporting Files** (3 files):
   
   - ``requirements.txt`` - Python dependencies
   - ``README.md`` - Project overview and setup guide
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP2: Traffic Management System - PostgreSQL + Python Integration
   
   **Team Number**: [Your team number]
   
   **Scenario**: Smart City Traffic Management
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Project Overview
   
   [2-3 sentence description of your implementation approach]
   
   ## Setup Instructions
   
   ### Prerequisites
   
   - PostgreSQL 18 with PostGIS extension
   - Python 3.10+
   - pip
   
   ### Database Setup
   
   ```bash
   createdb traffic_management
   psql -d traffic_management -f postgresql/schema.sql
   psql -d traffic_management -f postgresql/data.sql
   ```
   
   ### Application Setup
   
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with your database credentials
   uvicorn src.api.endpoints:app --reload
   ```
   
   ### Running Tests
   
   ```bash
   pytest tests/ --cov=src --cov-report=html
   ```
   
   ## Key Design Decisions
   
   1. **Decision 1**: [Brief explanation and rationale]
   2. **Decision 2**: [Brief explanation and rationale]
   3. **Decision 3**: [Brief explanation and rationale]
   
   ## Query Highlights
   
   - Query #X: [Most interesting query and what it demonstrates]
   - Query #Y: [Another highlight]
   
   ## API Endpoints Summary
   
   | Method | Endpoint | Description |
   |--------|----------|-------------|
   | GET | /intersections/{id} | Retrieve intersection |
   | GET | /intersections | List with pagination |
   | [Continue for all endpoints] | | |
   
   ## File Guide
   
   - `postgresql/schema.sql` - Database schema with constraints and indexes
   - `postgresql/data.sql` - Sample data (50+ intersections, 100+ signals, etc.)
   - `postgresql/queries.sql` - 10+ complex SQL queries
   - `src/` - Python application (config, models, repositories, services, API)
   - `tests/` - Test suite with 70%+ coverage
   - `docs/` - Technical documentation
   
   ## Tools Used
   
   - **Database**: PostgreSQL 18 + PostGIS
   - **Language**: Python 3.x
   - **Framework**: FastAPI
   - **Testing**: pytest + pytest-cov
   - **Documentation**: [Swagger/OpenAPI, Markdown, etc.]
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP2
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Created schema.sql with all tables and constraints
   - Implemented PostGIS integration
   - Wrote index strategy document
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Generated sample data (data.sql)
   - Wrote queries 1-5 (JOINs and aggregates)
   - Created query catalog with EXPLAIN ANALYZE
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Built Python application (models, repositories, services)
   - Implemented connection pooling
   - Wrote architecture documentation
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Built REST API with FastAPI
   - Wrote all tests (70%+ coverage)
   - Created API documentation and README
   
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

   **SQL Files** (3 files):
   
   - [ ] schema.sql creates all tables, constraints, indexes, triggers
   - [ ] schema.sql includes PostGIS extension and geography columns
   - [ ] data.sql meets minimum volume requirements (50+ intersections, etc.)
   - [ ] data.sql passes all constraints (no errors on import)
   - [ ] queries.sql contains 10+ queries with documentation headers
   
   **Python Application**:
   
   - [ ] Application runs with ``uvicorn`` without errors
   - [ ] Connection pooling implemented and configured
   - [ ] Repository pattern with CRUD for major entities
   - [ ] Service layer with business logic
   - [ ] 8+ API endpoints working
   - [ ] FastAPI auto-docs accessible at ``/docs``
   
   **Tests**:
   
   - [ ] Test suite runs with ``pytest``
   - [ ] Coverage report shows 70%+ coverage
   - [ ] Repository, service, and API tests included
   
   **Documentation** (4 files):
   
   - [ ] Index strategy with justifications for each index
   - [ ] Query catalog with EXPLAIN ANALYZE for 5+ queries
   - [ ] Architecture overview describing layer responsibilities
   - [ ] API documentation with all endpoints
   
   **Supporting Files**:
   
   - [ ] README.md with setup instructions
   - [ ] team_contributions.md with individual contributions
   - [ ] requirements.txt with all Python dependencies
   - [ ] .env.example with required environment variables
   
   **Quality Checks**:
   
   - [ ] ``schema.sql`` runs without errors on fresh database
   - [ ] ``data.sql`` loads without constraint violations
   - [ ] All API endpoints return correct responses
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP2_Traffic_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **No PostGIS extension** - Forgetting to enable PostGIS for geospatial queries
   
   ❌ **Hardcoded credentials** - Database passwords in source code instead of .env
   
   ❌ **Missing indexes** - Schema works but queries are painfully slow
   
   ❌ **Unrealistic data** - Random values that don't make geographic or temporal sense
   
   ❌ **No error handling** - Application crashes on bad input or missing records
   
   ❌ **Queries without documentation** - SQL files with no comments explaining purpose
   
   ❌ **Tests that don't run** - Test suite depends on specific data or environment
   
   ❌ **No EXPLAIN ANALYZE** - Missing query performance analysis


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Schema**
     - 3
     - Complete DDL (1pt); Proper constraints and indexes (1pt); PostGIS integration (0.5pt); Triggers and ENUMs (0.5pt)
   * - **Part 1: Sample Data**
     - 2
     - Meets volume requirements (1pt); Realistic patterns and edge cases (1pt)
   * - **Part 2: SQL Queries**
     - 5
     - 10+ queries covering all categories (2pts); Correct results (1.5pts); Documentation and EXPLAIN ANALYZE (1.5pts)
   * - **Part 3: Python App**
     - 3
     - Clean architecture with layers (1pt); Repository pattern with CRUD (1pt); Error handling and connection pooling (1pt)
   * - **Part 3: REST API**
     - 2
     - 8+ working endpoints (1pt); Documentation and response models (1pt)
   * - **Total**
     - **15**
     - 


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP2**
   
   - **Start with the schema** - Get your database working and data loaded before touching Python. A solid schema prevents headaches later.
   - **Test queries in psql first** - Write and debug SQL interactively before embedding in Python code.
   - **Use EXPLAIN ANALYZE frequently** - Understand query plans early. Add indexes when you see sequential scans on large tables.
   - **Write tests as you go** - Don't wait until the end. Test each repository method as you build it.
   - **Layer your application** - Keep database logic in repositories, business logic in services, and HTTP handling in API. This separation makes testing much easier.
   - **Use office hours** - Bring your schema for review. Ask about query optimization strategies.


Next Steps
----------

After completing GP2, you will:

- Receive feedback from instructors
- Identify performance bottlenecks in your PostgreSQL system
- Begin GP3: Adding MongoDB for high-volume traffic event data
- Design document schemas for sensor readings and traffic flow

.. note::
   
   **Your GP2 implementation is the core** of the complete system. GP3 (MongoDB) and GP4 (Redis + deployment) extend this foundation.
   
   Start thinking: What data has flexible schemas or high write volume that might be better suited for a document database?