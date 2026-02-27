====================================================
Group Project 1: Relational Database Design
====================================================

Overview
--------

Design the PostgreSQL database schema that will serve as the transactional backbone of your traffic management system. You will identify entities from business requirements, model their relationships, define keys and constraints, and prove your design is in Third Normal Form (3NF).

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 2 weeks |
   **Weight**: 10 points (20% of final project) |
   **Team Size**: 4 students


.. important::

   **What You'll Deliver**

   This project requires **3 deliverables** submitted as a single ZIP file:

   1. **Conceptual ER Diagram** in Chen notation (PDF)
   2. **Logical ER Diagram** in Crow's Foot notation (PDF)
   3. **Design Report** covering entities, keys, normalization, and denormalization (PDF, 8 to 12 pages)

   **Submission**: Single ZIP file named ``GP1_Traffic_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Extract entities and attributes from narrative business requirements
- Design Entity-Relationship Diagrams using Chen and Crow's Foot notations
- Use (min,max) notation to express participation and cardinality constraints
- Identify and justify primary keys, candidate keys, and foreign keys
- Apply normalization theory (1NF, 2NF, 3NF) to relational schemas
- Analyze functional dependencies and evaluate denormalization trade-offs
- Document design decisions professionally


Business Requirements
---------------------

Your traffic management system must track the following information:

.. dropdown:: Infrastructure Management
   :icon: gear
   :class-container: sd-border-primary
   :open:

   The city needs to track all traffic intersections with their physical characteristics (location coordinates, intersection type, traffic handling capacity, installation date, jurisdictional district, elevation). Each intersection has a unique identifier and may have multiple traffic signals positioned at different approaches (north, south, east, west).

   Signals have specific types (LED, incandescent, pedestrian), timing modes (fixed, adaptive, emergency), power sources, maintenance history, and warranty information. Each signalized intersection is monitored by multiple sensors of different types (inductive loops, radar, cameras, lidar, acoustic) that track traffic flow, vehicle speeds, and occupancy.

.. dropdown:: Road Network
   :icon: gear
   :class-container: sd-border-primary

   Roads connect intersections, and each road segment has specific characteristics: number of lanes, lane widths, speed limits, surface type (asphalt, concrete), length, grade (slope), and indicates whether bike lanes and sidewalks are present. The system must support routing and traffic flow analysis across the network.

.. dropdown:: Maintenance Operations
   :icon: gear
   :class-container: sd-border-primary

   The city's maintenance department schedules work for all traffic infrastructure. Each maintenance task specifies the asset type, maintenance type (preventive, corrective, inspection, upgrade), scheduled date and time, estimated duration, priority level, and assigned crew. Maintenance crews have supervisors, specializations (electrical, mechanical, civil, software), certification levels, and availability status.

.. dropdown:: Incident Management
   :icon: gear
   :class-container: sd-border-primary

   The system tracks all traffic incidents including accidents, vehicle breakdowns, road hazards, construction activities, and special events. Each incident has a type, severity level (minor, moderate, major, critical), precise location (intersection or road segment), reported/verified/resolved timestamps, number of lanes blocked, and reporting source (sensor, public, officer, camera). Incidents must be linked to locations for analysis and emergency response.

.. dropdown:: Emergency Response
   :icon: gear
   :class-container: sd-border-primary

   Emergency vehicles need optimized routes from facilities (hospitals, fire stations, police stations) to incident locations. The system stores predefined emergency routes with priority levels, start and end intersections, alternative routes, and historical performance data (average response times, usage counts). Emergency facilities have specific capabilities, capacity, operating hours, and contact information.

.. dropdown:: Environmental Monitoring
   :icon: gear
   :class-container: sd-border-primary

   Weather conditions significantly impact traffic flow. Weather stations at key intersections monitor temperature, humidity, precipitation, wind, and visibility. The system needs location, sensor suite capabilities, operational status, and data transmission frequency for each station.

.. dropdown:: Parking Management
   :icon: gear
   :class-container: sd-border-primary

   The city manages parking facilities (surface lots, garages, street parking) with total capacity, designated EV charging spots, accessible spaces, pricing structure, operating hours, and payment methods. Parking information helps predict traffic patterns in downtown areas.

.. dropdown:: Traffic Control Zones
   :icon: gear
   :class-container: sd-border-primary

   The city divides the urban area into traffic control zones (downtown, residential, industrial, school zones) with specific default speed limits, special restrictions (time-based, vehicle-type), and enforcement levels. Zones contain multiple intersections, and some intersections may belong to multiple zones.


Deliverable 1: Conceptual ER Diagram (Chen Notation)
-----------------------------------------------------

Create a **conceptual ER diagram** using **Chen notation** that captures all business requirements.

.. dropdown:: Requirements and Notation Guide
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Requirements**:

   - Entities covering all eight business areas listed above (you decide how many entities are appropriate for your design)
   - All relationships shown as diamonds
   - **(min,max) notation** on each side of every relationship to express both participation and cardinality constraints (e.g., an intersection participates in the "has" relationship with traffic signals as (0,N) on the signal side and (1,1) on the intersection side)
   - You do **not** need double lines for total participation. The (min,max) notation is sufficient to capture participation constraints.

   **Notation Elements**:

   - **Rectangles** for entities
   - **Diamonds** for relationships
   - **Ovals** for attributes (connected to entities)
   - **Underlined attributes** for primary keys
   - **Double ovals** for multivalued attributes
   - **Dashed ovals** for derived attributes
   - **Composite attributes** shown with sub-ovals
   - **(min,max)** labels on relationship lines for participation and cardinality

   **Purpose**: Focus on **what** data exists and **how** entities relate conceptually.

   **Recommended Tools**:

   - `Draw.io <https://app.diagrams.net/>`_
   - `Lucidchart <https://www.lucidchart.com/>`_
   - `ERDPlus <https://erdplus.com/>`_
   - `Inkscape <https://inkscape.org/>`_ -- SVG templates used for in-class lectures are available at https://github.com/zeidk/enpm818t-spring-2026-code

   Hand-drawn diagrams are acceptable if very neat and legible.

   **File to create**: ``chen_conceptual_model.pdf``


Deliverable 2: Logical ER Diagram (Crow's Foot Notation)
---------------------------------------------------------

Create a **logical ER diagram** using **Crow's Foot notation** that shows how entities will be implemented as relational tables.

.. dropdown:: Requirements and Notation Guide
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Requirements**:

   - Same entities as the Chen diagram
   - Attributes listed inside entity rectangles with data types
   - Primary keys marked (PK) and foreign keys indicated (FK)

   **Cardinality Symbols**:

   - Single line: One
   - Crow's foot (three lines): Many
   - Circle: Optional (minimum 0)
   - Bar: Mandatory (minimum 1)

   **Purpose**: Show **how** entities will be implemented as relational tables with their columns, keys, and relationships.

   **Recommended Tools**:

   - `Lucidchart <https://www.lucidchart.com/>`_ (excellent for Crow's Foot)
   - `Draw.io <https://app.diagrams.net/>`_
   - `ERDPlus <https://erdplus.com/>`_
   - `PlantUML <https://plantuml.com/>`_ -- Examples of PlantUML code used during lectures are available at https://github.com/zeidk/enpm818t-spring-2026-code

   **File to create**: ``crows_foot_logical_model.pdf``


Deliverable 3: Design Report
-----------------------------

Write a single PDF report (8 to 12 pages) documenting your complete database design. The report consolidates all analysis into one organized document.

.. dropdown:: Report Outline
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Use the following structure. Page counts are approximate guidelines.

   **1. Introduction** (0.5 page)

   Brief overview of your design approach and summary of entities identified.

   **2. Entity Catalog** (2 to 3 pages)

   For each entity, document:

   - Entity name and purpose (one sentence)
   - Primary key and justification (why this key was chosen)
   - Candidate keys, if any
   - Business rules and constraints for this entity (e.g., "traffic capacity must be positive", "severity level must be one of: minor, moderate, major, critical")

   **3. Relationship Documentation** (1 to 2 pages)

   A table listing all relationships:

   .. list-table::
      :header-rows: 1
      :widths: 15 15 15 15 40
      :class: compact-table

      * - Parent Entity
        - Child Entity
        - Relationship
        - (min,max)
        - Business Rule
      * - INTERSECTION
        - TRAFFIC_SIGNAL
        - has
        - (1,1) and (0,N)
        - Each intersection has 0 to many signals; each signal belongs to exactly one intersection
      * - INTERSECTION
        - SENSOR
        - monitors
        - (1,1) and (0,N)
        - Each intersection monitored by 0 to many sensors
      * - ...
        - ...
        - ...
        - ...
        - Continue for all relationships

   **4. Normalization Proofs** (2 to 3 pages)

   For each entity, prove it is in 3NF by showing:

   - Functional dependencies identified
   - 1NF: All attributes atomic, no repeating groups
   - 2NF: No partial dependencies (or single-attribute PK, so automatic)
   - 3NF: No transitive dependencies

   Example:

   .. code-block:: text

      Entity: INTERSECTION

      Functional Dependencies:
        FD1: intersection_id -> all other attributes
        FD2: (latitude, longitude) -> intersection_id

      1NF: All attributes atomic, no repeating groups
      2NF: Single-attribute PK, automatically in 2NF
      3NF: No transitive dependencies
           - jurisdiction does NOT determine anything else
           - intersection_type does NOT determine anything else
           - All non-key attributes depend only on intersection_id

      Conclusion: INTERSECTION is in 3NF

   **5. Denormalization Analysis** (1 to 2 pages)

   Analyze **2 to 3 scenarios** where denormalization might improve performance. For each, discuss the opportunity, benefits, costs, alternatives (e.g., materialized views), and your recommendation.

   **6. Team Contributions** (0.5 page)

   List each team member's name, tasks completed, and contribution percentage. Contributions must sum to 100%.


Folder Structure
----------------

.. code-block:: text

   GP1_Traffic_Team{X}/
   ├── chen_conceptual_model.pdf
   ├── crows_foot_logical_model.pdf
   └── design_report.pdf


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP1_Traffic_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP1_Traffic_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **Diagrams** (2 files):

   - [ ] Chen notation conceptual model (PDF)
   - [ ] Crow's Foot logical model (PDF)
   - [ ] Both diagrams cover all eight business areas
   - [ ] Chen diagram uses (min,max) notation on all relationships
   - [ ] Diagrams are high resolution and legible

   **Design Report** (1 file):

   - [ ] Follows the report outline (sections 1 through 6)
   - [ ] 8 to 12 pages, submitted as PDF
   - [ ] Entity catalog covers all entities with keys and business rules
   - [ ] All relationships documented with (min,max) cardinality
   - [ ] 3NF proofs for all entities
   - [ ] 2 to 3 denormalization scenarios analyzed
   - [ ] Team contributions section included


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 10 55
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Conceptual ERD (Chen)**
     - 2.5
     - Entities cover all business areas (0.5pt); correct relationships with (min,max) notation (1.5pt); proper Chen notation elements (0.5pt)
   * - **Logical ERD (Crow's Foot)**
     - 2.5
     - Consistent with Chen diagram (0.5pt); attributes with data types, PKs, and FKs shown (1pt); correct Crow's Foot cardinality (1pt)
   * - **Report: Entity Catalog**
     - 2
     - All entities documented with purpose and business rules (1pt); well-chosen primary keys with candidate key analysis (1pt)
   * - **Report: Normalization**
     - 2
     - Complete 3NF proofs with functional dependencies for all entities (1.5pt); denormalization analysis with trade-offs (0.5pt)
   * - **Report: Quality**
     - 1
     - Relationship documentation complete (0.5pt); report is well-organized and professionally written (0.5pt)
   * - **Total**
     - **10**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Illegible diagrams with tiny text or poor layout
   - Not covering all eight business areas
   - Using cardinality ratios (1:N) instead of (min,max) notation in the Chen diagram
   - Proving 3NF for only some entities
   - Denormalization section that only lists scenarios without analyzing trade-offs
   - Team contributions that do not sum to 100%


Tips for Success
----------------

.. tip::

   - **Start early**: Your first ERD draft will not be your final version. Iterate.
   - **Meet regularly**: Schedule 2 to 3 team meetings per week. Divide the report sections but review everything together.
   - **Use office hours**: Bring your ERD sketches for feedback. Discuss design trade-offs with instructors.
   - **Test your design mentally**: Walk through real workflows like "How would we query for intersections with high incident rates?" If your design makes this difficult, reconsider.
   - **Write as you go**: Do not wait until the end to write the report. Capture decisions and rationale as you make them.

.. note::

   **Your GP1 design is the foundation** for GP2 (PostgreSQL implementation), GP3 (MongoDB integration), and GP4 (complete system).

   A strong relational design now makes implementation much easier later!
