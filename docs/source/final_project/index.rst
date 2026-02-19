====================================================
Final Project: Polyglot Persistence Systems
====================================================

Overview
--------

The final project is the capstone experience of ENPM818T, where you will design, implement, and deploy a complete polyglot persistence system. Working in teams of 4 students, you will build a real-world database application that leverages multiple database technologies, each chosen for its specific strengths.

The project spans 10 weeks through four progressive group projects (GP1 through GP4), allowing you to apply everything you learn in lectures to a substantial, portfolio-worthy system.


What is Polyglot Persistence?
------------------------------

.. important::
   
   **Polyglot Persistence** is an architectural approach where different types of data are stored in different databases, each selected based on how the data will be used.

Rather than forcing all data into a single database technology (the traditional "one size fits all" approach), polyglot persistence recognizes that:

- **Relational databases** excel at structured data with complex relationships and ACID transactions
- **Document databases** handle high-volume, flexible-schema data efficiently
- **Key-value stores** provide sub-millisecond access to frequently changing data
- **Graph databases** model and query complex relationships naturally

**Core Principle**: Use the right database for the right job.

**Example in This Project**:

Your traffic management system will use:

- **PostgreSQL** for infrastructure data (intersections, signals, maintenance schedules)
- **MongoDB** for high-volume traffic events (1000+ writes per second)
- **Redis** for real-time signal states (sub-millisecond latency required)

Each database is chosen because it solves a specific problem better than the alternatives.


Learn More About Polyglot Persistence
--------------------------------------

.. admonition:: 📚 Recommended Reading
   :class: note

   **Foundational Articles**:
   
   - Martin Fowler: "Polyglot Persistence" (2011)
     
     https://martinfowler.com/bliki/PolyglotPersistence.html
     
     The article that introduced and popularized the term. Essential reading.
   
   - Pramod J. Sadalage & Martin Fowler: "NoSQL Distilled" (Book, 2012)
     
     Chapters on polyglot persistence and choosing database technologies.
   
   **Academic Papers**:
   
   - Hecht, R. & Jablonski, S. (2011). "NoSQL Evaluation: A Use Case Oriented Survey"
     
     Proceedings of the International Conference on Cloud and Service Computing.
     
     https://ieeexplore.ieee.org/document/6138489
   
   - Abramova, V., Bernardino, J., & Furtado, P. (2014). "Which NoSQL Database? A Performance Overview"
     
     Open Journal of Databases (OJDB), Vol. 1, No. 2.
     
     Comparative analysis of different NoSQL databases.
   
   **Industry Perspectives**:
   
   - Netflix Tech Blog: "Polyglot Persistence at Netflix"
     
     https://netflixtechblog.com/
     
     Real-world case study of using multiple databases in production.
   
   - LinkedIn Engineering: "Data Infrastructure at LinkedIn"
     
     https://engineering.linkedin.com/
     
     How LinkedIn uses multiple database technologies (Espresso, Voldemort, etc.).
   
   **Recent Research**:
   
   - Davoudian, A., Chen, L., & Liu, M. (2018). "A Survey on NoSQL Stores"
     
     ACM Computing Surveys, Vol. 51, No. 2.
     
     https://dl.acm.org/doi/10.1145/3158661
     
     Comprehensive survey covering database selection criteria.


Project Weight
--------------

The final project accounts for **40% of your overall course grade** and consists of:

.. list-table::
   :header-rows: 1
   :widths: 40 15 15 30
   :class: compact-table

   * - Component
     - Points
     - % of Project
     - Duration
   * - GP1: Relational Database Design
     - 10
     - 25%
     - 2 weeks
   * - GP2: PostgreSQL + Python Integration
     - 15
     - 37.5%
     - 3 weeks
   * - GP3: NoSQL Database Integration
     - 10
     - 25%
     - 2 weeks
   * - GP4: System Integration + Report
     - 15
     - 12.5%
     - 3 weeks
   * - **Total**
     - **50**
     - **100%**
     - **10 weeks**


Learning Objectives
-------------------

By completing the final project, you will be able to:

- Design normalized relational database schemas using ER modeling and functional dependency analysis
- Implement production-ready PostgreSQL databases with proper constraints, indexes, and triggers
- Write complex SQL queries supporting real-world business requirements
- Integrate Python applications with databases using industry-standard libraries
- Evaluate and select appropriate NoSQL databases based on data characteristics and query patterns
- Design document schemas, graph structures, or wide-column families for semi-structured data
- Implement cross-database queries and maintain data consistency in polyglot systems
- Deploy multi-database systems using Docker and cloud infrastructure
- Document technical architecture and justify design decisions professionally


Project Scenarios
-----------------

You will choose **one** of two scenarios for your team project:

**Scenario 1: Smart City Traffic Management System**

Build a system managing traffic flow across 500+ urban intersections using:

- **PostgreSQL**: Infrastructure data (intersections, signals, sensors, maintenance)
- **MongoDB**: High-volume traffic events and sensor readings (1000+ writes/sec)
- **Redis**: Real-time signal states and live congestion metrics (<10ms latency)

*Focus*: Real-time performance, geospatial queries, high write throughput

**Scenario 2: Healthcare Patient Management Platform**

Build an integrated clinical and administrative system using:

- **PostgreSQL**: Patient records, appointments, prescriptions, billing (HIPAA-compliant)
- **MongoDB**: Clinical documents, imaging metadata, care plans (flexible schemas)
- **Neo4j**: Medical knowledge graph for drug interactions and clinical decision support

*Focus*: Regulatory compliance, complex relationships, clinical workflows


Progressive Structure
---------------------

Each group project builds on the previous work:

**GP1: Relational Database Design (2 weeks)**

- Create **Conceptual Model** using Chen notation (entities with attributes as ovals)
- Create **Logical Model** using Crow's Foot notation (entity tables with cardinalities)
- Identify keys, constraints, and relationships
- Normalize to 3NF with functional dependency analysis
- Analyze denormalization trade-offs

**GP2: PostgreSQL Implementation (3 weeks)**

- Implement your GP1 design in PostgreSQL
- Generate realistic sample data
- Write 10+ complex SQL queries (JOINs, CTEs, window functions)
- Build Python application with repository and service layers
- Create REST API using FastAPI
- Write comprehensive tests

**GP3: NoSQL Integration (2 weeks)**

- Design schemas for high-volume or semi-structured data
- Choose appropriate NoSQL database for your scenario
- Implement document collections, graph nodes, or key-value structures
- Write 8+ complex NoSQL queries (aggregations, graph traversals)
- Integrate with existing PostgreSQL application
- Handle cross-database queries

**GP4: Complete System Integration (3 weeks)**

- Add second NoSQL database (Redis for Traffic, Neo4j for Healthcare)
- Implement complete three-database architecture
- Deploy using Docker Compose
- Write comprehensive technical report (10 to 15 pages)
- Optional: Present system to class


Team Formation
--------------

**Timeline**: Form teams by end of Week 3

**Team Size**: 4 students per team

**Selection Process**:

1. Review both scenario specifications carefully
2. Form teams with complementary skills:
   
   - Strong SQL background
   - Python/API development experience
   - System architecture interest
   - Documentation skills

3. Choose your scenario (cannot change after Week 4)
4. Submit team roster and scenario choice via Canvas


Academic Integrity
------------------

.. warning::

   **No AI-Generated Code**
   
   Per syllabus, you may NOT use ChatGPT, GitHub Copilot, or similar tools to generate code for group projects. All code must be original team work.
   
   **Permitted**:
   - Using AI for brainstorming ideas
   - Getting help understanding concepts
   - Debugging assistance (must understand and explain fixes)
   
   **Prohibited**:
   - Generating complete functions or queries
   - Copy-pasting AI-generated code
   - Using AI to write documentation
   
   Violations will be treated as academic dishonesty.

**Collaboration Guidelines**:

- Work within your team - all team members must contribute meaningfully
- Do not share code between teams
- You may discuss concepts with other teams but not share implementations
- Cite any external libraries or code snippets used
- Each team member must be able to explain all code in your repository


Grading Philosophy
------------------

Your project will be evaluated on:

**Technical Excellence (60%)**

- Database designs follow best practices
- Implementations are correct and efficient
- Code is clean, well-structured, and maintainable
- Proper use of each database technology

**Critical Thinking (20%)**

- Design decisions are well-justified
- Trade-offs are analyzed thoroughly
- Alternative approaches are considered
- Learning from mistakes is documented

**Professional Quality (15%)**

- Complete and accurate documentation
- Working deployments
- Comprehensive testing
- Production-ready approach

**Collaboration (5%)**

- Equitable team contributions (peer evaluation)
- Effective coordination
- Professional team dynamics


Getting Started
---------------

1. **Review both scenarios** (this week)
2. **Form your team** (by end of Week 3)
3. **Choose your scenario** (Week 3-4)
4. **Begin GP1** (Week 4):

   - Read business requirements carefully
   - Identify entities from narratives
   - Start ERD sketches
   - Use office hours with questions

5. **Plan your semester**:

   - Schedule regular team meetings
   - Set up version control (Git)
   - Establish communication channels
   - Divide responsibilities


Support Resources
-----------------

**Office Hours**

- Instructor: By appointment (email zeidk@umd.edu)
- TA: By appointment (email zhanif@umd.edu)

**Technical Documentation**

- PostgreSQL: https://www.postgresql.org/docs/
- MongoDB: https://docs.mongodb.com/
- Redis: https://redis.io/documentation
- Neo4j: https://neo4j.com/docs/
- FastAPI: https://fastapi.tiangolo.com/

**Discussion Forum**

- Use Canvas discussions for:
  
  - Clarification questions
  - Concept discussions
  - Technical troubleshooting (not sharing code)


Scenario Details
----------------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   scenario1/index
   scenario2/index


Next Steps
----------

- **This Week**: Review both scenario specifications
- **Week 3**: Form teams and choose scenario
- **Week 4**: Begin GP1 (Relational Database Design)
- **Ongoing**: Attend office hours with questions