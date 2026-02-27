=====================================================================
Group Project 4: Neo4j Medical Knowledge Graph + Complete System
=====================================================================

Overview
--------

Add Neo4j for medical knowledge relationships and clinical decision support, complete your three-database polyglot system, deploy with Docker Compose, and write a final technical report.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 2 weeks |
   **Weight**: 15 points (30% of final project, includes final report) |
   **Team Size**: 4 students

**Builds on**: Your PostgreSQL + MongoDB system from GP2 and GP3


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Design medical knowledge graphs with clinically meaningful relationships
- Write Cypher queries for drug interaction checking
- Implement clinical decision support using graph traversals
- Build a complete three-database healthcare architecture
- Deploy secure polyglot systems using Docker Compose
- Document complex clinical systems professionally


Part 1: Neo4j Graph Design
----------------------------

**Objective**: Design a medical knowledge graph with clinically meaningful node types and relationships.

.. dropdown:: Task 1.1: Graph Structure (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Design a graph with at least **6 node types** and **6 relationship types**.

   **Required Node Types**:

   - **Disease**: name, ICD-10 code, category, chronic/acute
   - **Symptom**: name, body system, severity range
   - **Medication**: name, drug class, dosage forms, controlled schedule
   - **Procedure**: name, CPT code, category
   - **Lab Test**: name, specimen type, units, reference range
   - **ICD-10 Code**: code, description, category

   You may add more node types (Gene, Protein, Clinical Trial, Biomarker) if they serve your clinical use cases.

   **Required Relationship Types**:

   - ``(:Disease)-[:PRESENTS_WITH {frequency}]->(:Symptom)``
   - ``(:Disease)-[:TREATED_BY {evidence_level}]->(:Medication)``
   - ``(:Medication)-[:INTERACTS_WITH {severity, description}]->(:Medication)`` **Critical for safety!**
   - ``(:Procedure)-[:INDICATED_FOR]->(:Disease)``
   - ``(:Lab_Test)-[:DIAGNOSES {sensitivity}]->(:Disease)``
   - ``(:Medication)-[:CONTRAINDICATED_IN]->(:Disease)``

   **Node Documentation Format**:

   .. code-block:: text

      Node: Medication

      Properties:
      - name: String (e.g., "Warfarin")
      - generic_name: String (e.g., "warfarin sodium")
      - drug_class: String (e.g., "Anticoagulant")
      - dosage_forms: List<String> (e.g., ["tablet", "injectable"])
      - controlled_schedule: String or null

      Sample Nodes: Warfarin, Aspirin, Lisinopril, Metformin, Omeprazole
      Approximate Count: 30+ medications in graph

   **Relationship Documentation Format**:

   .. code-block:: text

      Relationship: INTERACTS_WITH

      From: Medication
      To: Medication
      Direction: Bidirectional (create both directions)

      Properties:
      - severity: String ("minor", "moderate", "major", "contraindicated")
      - description: String (clinical description of interaction)

      Example:
      (Warfarin)-[:INTERACTS_WITH {
        severity: "major",
        description: "Increased bleeding risk"
      }]->(Aspirin)

   **File to create**: ``docs/neo4j_graph_design.md`` (include both node and relationship documentation, plus the caching/integration notes from below)

.. dropdown:: Task 1.2: Graph Setup and Data
   :icon: gear
   :class-container: sd-border-primary

   Create Neo4j setup script with sample medical knowledge:

   .. code-block:: text

      // Create medications
      CREATE (warfarin:Medication {
        name: 'Warfarin', drug_class: 'Anticoagulant',
        pregnancy_category: 'X'
      })
      CREATE (aspirin:Medication {
        name: 'Aspirin', drug_class: 'NSAID/Antiplatelet'
      })
      CREATE (lisinopril:Medication {
        name: 'Lisinopril', drug_class: 'ACE Inhibitor'
      })

      // Create diseases
      CREATE (hypertension:Disease {
        name: 'Hypertension', icd10: 'I10',
        category: 'Cardiovascular', chronic: true
      })

      // Create drug interactions (CRITICAL)
      CREATE (warfarin)-[:INTERACTS_WITH {
        severity: 'major',
        description: 'Increased bleeding risk'
      }]->(aspirin)
      CREATE (aspirin)-[:INTERACTS_WITH {
        severity: 'major',
        description: 'Increased bleeding risk'
      }]->(warfarin)

      // Create treatment relationships
      CREATE (hypertension)-[:TREATED_BY {
        evidence_level: 'A'
      }]->(lisinopril)

   **Minimum graph size**:

   - 30+ medication nodes
   - 20+ disease nodes
   - 20+ symptom nodes
   - 50+ INTERACTS_WITH relationships
   - 30+ TREATED_BY relationships
   - 15+ PRESENTS_WITH relationships
   - 10+ CONTRAINDICATED_IN relationships

   **Files to create**: ``neo4j/graph_setup.cypher`` and ``neo4j/graph_data.cypher``


Part 2: Clinical Decision Support Queries
------------------------------------------

**Objective**: Write Cypher queries that provide real clinical value.

.. dropdown:: Task 2.1: Drug Safety Queries (3 minimum)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Drug Interaction Checking** (single medication):

   .. code-block:: text

      // Find all medications that interact with Warfarin
      MATCH (m1:Medication {name: 'Warfarin'})
            -[i:INTERACTS_WITH]->(m2:Medication)
      RETURN m1.name AS drug, m2.name AS interacts_with,
             i.severity, i.description
      ORDER BY CASE i.severity
        WHEN 'contraindicated' THEN 1
        WHEN 'major' THEN 2
        WHEN 'moderate' THEN 3
        WHEN 'minor' THEN 4
      END

   **Check Patient's Full Medication List**:

   .. code-block:: text

      // Check all pairwise interactions for a medication list
      MATCH (m1:Medication)-[i:INTERACTS_WITH]->(m2:Medication)
      WHERE m1.name IN ['Warfarin', 'Aspirin', 'Lisinopril',
                         'Metformin', 'Omeprazole']
        AND m2.name IN ['Warfarin', 'Aspirin', 'Lisinopril',
                         'Metformin', 'Omeprazole']
        AND m1 <> m2
      RETURN DISTINCT m1.name, m2.name, i.severity, i.description
      ORDER BY i.severity

   **Contraindication Check**:

   .. code-block:: text

      // Check if medication is contraindicated for patient conditions
      MATCH (m:Medication {name: 'Metformin'})
            -[:CONTRAINDICATED_IN]->(d:Disease)
      WHERE d.name IN ['Chronic Kidney Disease', 'Heart Failure']
      RETURN m.name, d.name AS contraindicated_condition

.. dropdown:: Task 2.2: Clinical Decision Support (3 minimum)
   :icon: gear
   :class-container: sd-border-primary

   **Disease Pathway Analysis**:

   *"What are the treatment options for a patient with Type 2 Diabetes?"*

   .. code-block:: text

      MATCH (d:Disease {name: 'Type 2 Diabetes'})
            -[:TREATED_BY]->(m:Medication)
      OPTIONAL MATCH (m)-[:CONTRAINDICATED_IN]->(contra:Disease)
      RETURN m.name, m.drug_class,
             COLLECT(contra.name) AS contraindications
      ORDER BY m.drug_class

   **Symptom Differential Diagnosis**:

   *"Given symptoms [chest pain, shortness of breath], what diseases could this be?"*

   **Medication Alternatives**:

   *"Find alternatives for a medication that treat the same disease."*

   **Query Documentation Format**:

   .. code-block:: text

      // Query #X: [Title]
      // Clinical Context: [Why this matters for patient safety]
      // Graph Pattern: [Description of traversal]
      // Nodes Used: [List node types]
      // Relationships Used: [List relationship types]

      [YOUR CYPHER QUERY]

      // Expected Output: [Description of columns]
      // Clinical Use Case: [How a clinician would use this]

   **File to create**: ``neo4j/cypher_queries.cypher``


Part 3: Complete System Integration
-------------------------------------

**Objective**: Build unified CLI operations and deploy the full system with Docker Compose.

.. dropdown:: Task 3.1: Unified CLI Operations (3 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Add CLI menu options that demonstrate all three databases working together. You need at least **3 unified operations**:

   **Operation 1: Complete Patient Record**

   - PostgreSQL: Demographics, appointments, prescriptions, labs
   - MongoDB: Clinical notes, care plans
   - Neo4j: Current medication interaction check

   **Operation 2: Prescription Safety Check**

   - Validate patient and medication in PostgreSQL
   - Get patient's active medications from PostgreSQL
   - Check new medication against all active meds in Neo4j
   - If safe: insert prescription into PostgreSQL
   - If unsafe: display interaction warnings with severity

   **Operation 3: Treatment Options for a Disease**

   - Neo4j: Treatment pathways for disease
   - Neo4j: Contraindication checking against patient conditions
   - PostgreSQL: Patient's current medications for context

   For each operation, document which databases are involved and why.

.. dropdown:: Task 3.2: Docker Deployment (2 points)
   :icon: gear
   :class-container: sd-border-primary

   **docker-compose.yml**:

   .. code-block:: yaml

      version: '3.8'
      services:
        postgres:
          image: postgres:14
          environment:
            POSTGRES_DB: healthcare_management
            POSTGRES_USER: healthcare_admin
            POSTGRES_PASSWORD: ${PG_PASSWORD}
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

        neo4j:
          image: neo4j:5
          environment:
            NEO4J_AUTH: neo4j/${NEO4J_PASSWORD}
          volumes:
            - neo4j_data:/data
          ports:
            - "7474:7474"
            - "7687:7687"

        app:
          build: .
          depends_on:
            - postgres
            - mongodb
            - neo4j

   After running ``docker-compose up --build``, verify:

   1. PostgreSQL: schema loaded and data present
   2. MongoDB: collections exist and data loaded
   3. Neo4j: graph populated (Browser at localhost:7474)
   4. Application starts and connects to all three databases

   **Files to create**: ``docker-compose.yml`` and ``Dockerfile``


Part 4: Final Technical Report
-------------------------------

**Objective**: Write a comprehensive technical report documenting the complete system.

.. dropdown:: Task 4.1: Report Structure (4 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **8 to 12 pages, submitted as PDF.**

   **1. Executive Summary** (1 page)

   System overview, three-database architecture, and key achievements (polyglot architecture, drug safety).

   **2. Data Partitioning Rationale** (1 page)

   Why each data type lives in its chosen database. Trade-offs between consistency, flexibility, and query power. Cross-database referencing strategy.

   **3. Architecture Overview** (2 to 3 pages)

   System architecture diagram, data flow diagrams for clinical workflows, and component descriptions for each database layer.

   **4. Database Design Decisions** (2 to 3 pages)

   For each database (PostgreSQL, MongoDB, Neo4j): what data it holds, why that database was chosen, schema/structure highlights, and key design decisions.

   **5. Clinical Decision Support Design** (1 to 2 pages)

   Medical knowledge graph structure, drug interaction checking workflow, and how the prescription safety check works end-to-end.

   **6. Lessons Learned** (1 page)

   What worked well, challenges faced, what you would do differently, and team contributions with percentages.

   **File to create**: ``docs/technical_report.pdf``


Folder Structure
----------------

.. code-block:: text

   GP4_Healthcare_Team{X}/
   ├── postgresql/              # From GP2
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── mongodb/                 # From GP3
   │   ├── mongo_setup.js
   │   ├── mongo_data.js
   │   └── mongo_queries.js
   ├── neo4j/
   │   ├── graph_setup.cypher
   │   ├── graph_data.cypher
   │   └── cypher_queries.cypher
   ├── src/
   │   ├── config/
   │   │   ├── database.py
   │   │   ├── mongodb.py
   │   │   └── neo4j_config.py
   │   ├── models/
   │   ├── repositories/
   │   │   ├── postgres/
   │   │   ├── mongodb/
   │   │   └── neo4j/
   │   ├── services/
   │   │   ├── clinical_service.py
   │   │   └── prescription_safety.py
   │   └── cli/
   │       └── main.py
   ├── docker-compose.yml
   ├── Dockerfile
   ├── requirements.txt
   ├── docs/
   │   ├── neo4j_graph_design.md
   │   └── technical_report.pdf
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **docs/neo4j_graph_design.md**

   Your Neo4j design document. Contains node type documentation (properties, sample nodes, counts), relationship type documentation (direction, properties, examples), and a summary of how the graph integrates with PostgreSQL and MongoDB.

   **docs/technical_report.pdf**

   The final report (8 to 12 pages) following the outline in Part 4.

   **requirements.txt**

   Updated from GP3 to include ``neo4j`` (Python driver).

   **README.md**

   Updated from GP3. Add Docker quick-start instructions (``docker-compose up --build``), an architecture summary table showing which database holds which data, and key safety features (drug interaction checking).

   **team_contributions.md**

   List each team member's name, tasks completed, hours contributed, and contribution percentage. Percentages must sum to 100%.


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP4_Healthcare_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP4_Healthcare_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **Neo4j Graph**:

   - [ ] ``graph_setup.cypher`` creates 6+ node types with properties
   - [ ] ``graph_data.cypher`` populates 30+ medications, 20+ diseases, 50+ interactions
   - [ ] ``cypher_queries.cypher`` contains 6+ clinical decision support queries
   - [ ] Drug interaction checking works for medication lists

   **System Integration**:

   - [ ] 3+ unified CLI operations using all three databases
   - [ ] Prescription safety check works end-to-end
   - [ ] Complete patient record assembles from all three databases

   **Deployment**:

   - [ ] ``docker-compose.yml`` starts all services (PostgreSQL, MongoDB, Neo4j, app)
   - [ ] ``Dockerfile`` builds application correctly
   - [ ] ``docker-compose up --build`` results in working system

   **Final Report**:

   - [ ] 8 to 12 pages, submitted as PDF
   - [ ] Architecture diagram included
   - [ ] Clinical decision support design documented
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
   * - **Part 1: Neo4j Graph**
     - 2
     - 6+ node types with meaningful properties (1pt); 6+ relationship types with clinical relevance (1pt)
   * - **Part 2: Cypher Queries**
     - 2
     - Drug interaction checking works correctly (1pt); 6+ clinical decision support queries (1pt)
   * - **Part 2: Drug Safety Integration**
     - 2
     - Prescription safety check workflow implemented (1pt); contraindication checking works (1pt)
   * - **Part 3: Unified Operations**
     - 3
     - 3+ unified operations using all three databases (1.5pts); complete patient record from all databases (1.5pts)
   * - **Part 3: Deployment**
     - 2
     - Working Docker Compose with all services (1pt); all databases start and connect (1pt)
   * - **Part 4: Technical Report**
     - 4
     - Comprehensive architecture overview (1.5pts); data partitioning rationale and clinical decision support documented (1.5pts); lessons learned and professional quality (1pt)
   * - **Bonus: Presentation**
     - +4
     - Clarity (1pt), technical depth (1.5pts), live demo (1pt), Q&A (0.5pt)
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
   2. Data partitioning rationale (2 min)
   3. Live demonstration (6 min): show prescription safety check (drug interaction alert), complete patient record from all databases, Neo4j Browser with medical knowledge graph
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

   - Trivial graph (only 5 medications and 3 diseases does not demonstrate clinical value)
   - No bidirectional interactions (drug interactions go both ways; create both directions)
   - Prescription operation without safety check (the whole point of Neo4j is preventing unsafe prescriptions)
   - Docker volumes not configured (data lost on container restart)
   - Hardcoded connection strings (use environment variables)
   - Missing data partitioning section in report (document why each database holds its data)
   - Final report under 8 pages or missing required sections


Tips for Success
----------------

.. tip::

   - **Build a meaningful graph**: Use real medication names, real ICD-10 codes, and real drug interactions. RxNorm and interaction databases are freely available for reference.
   - **Test the safety flow end-to-end**: Write test cases like "What happens when I prescribe Warfarin to a patient already on Aspirin?" The answer should be a major interaction warning.
   - **Test with Docker early**: Do not wait until the last day to containerize. Build and test Docker Compose incrementally.
   - **Write the report throughout**: Capture architecture decisions and screenshots as you build. Do not try to reconstruct everything at the end.
   - **Use office hours**: Bring Docker issues early. Discuss graph design and Cypher query strategies with instructors.


Final Project Summary
---------------------

.. admonition:: Cumulative Achievement
   :class: note

   **Points**:

   - GP1: Relational Design = 10 points
   - GP2: PostgreSQL + Python = 15 points
   - GP3: MongoDB Integration = 10 points
   - GP4: Neo4j + Complete System = 15 points
   - **Total**: 50 points
   - **Optional Presentation**: +4 points bonus

**Your Achievement**:

You have built a production-grade secure polyglot healthcare system demonstrating relational database design, clinical document management with flexible schemas, medical knowledge graph for clinical decision support, drug interaction checking for patient safety, cross-database integration for unified patient records, Docker deployment, and professional technical documentation.
