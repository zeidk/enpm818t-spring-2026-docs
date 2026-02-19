=====================================================================
Group Project 4: Neo4j Medical Knowledge Graph + Complete System
=====================================================================

Overview
--------

Add Neo4j for medical knowledge relationships and clinical decision support, complete your three-database polyglot system, deploy with Docker Compose, and write comprehensive technical documentation.

**Timeline**: 4 weeks

**Weight**: 15 points (12.5% of final project, includes final report)

**Team Size**: 4 students

**Builds on**: Your PostgreSQL + MongoDB system from GP2 and GP3


.. important::
   
   **What You'll Deliver**
   
   This project requires a **complete three-database healthcare system** with deployment and documentation:
   
   - 3 Neo4j files (graph setup, sample data, Cypher queries)
   - 2 deployment files (Dockerfile, docker-compose.yml)
   - 1 final technical report (10 to 15 pages, PDF)
   - 1 updated Python application (Neo4j integration + unified clinical API)
   - 1 README file
   - 1 team contributions file
   
   **Submission**: Single ZIP file named ``GP4_Healthcare_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Design medical knowledge graphs with clinically meaningful relationships
- Write Cypher queries for drug interaction checking
- Implement clinical decision support using graph traversals
- Build a complete three-database healthcare architecture
- Deploy HIPAA-compliant polyglot systems using Docker Compose
- Document complex clinical systems professionally
- Analyze performance across multiple databases


Part 1: Neo4j Graph Design
----------------------------

**Objective**: Design a medical knowledge graph with clinically meaningful node types and relationships.

.. dropdown:: 📋 Task 1.1: Node Types (12+ required)
   :class-container: sd-border-primary
   :open:

   Design nodes for:
   
   - **Disease** - name, ICD-10 code, category, chronic/acute
   - **Symptom** - name, body system, severity range
   - **Medication** - name, drug class, dosage forms, controlled schedule
   - **Procedure** - name, CPT code, category, typical duration
   - **Lab Test** - name, specimen type, units, reference range
   - **Gene** - name, chromosome, function
   - **Protein** - name, function, drug target status
   - **Patient Cohort** - demographics, condition criteria
   - **Clinical Trial** - trial ID, phase, status, enrollment criteria
   - **Biomarker** - name, type, clinical significance
   - **ICD-10 Code** - code, description, category
   - **CPT Code** - code, description, relative value units
   
   **Node Documentation Format**:
   
   .. code-block:: text
   
      Node: Medication
      
      Properties:
      - name: String (e.g., "Warfarin")
      - generic_name: String (e.g., "warfarin sodium")
      - drug_class: String (e.g., "Anticoagulant")
      - dosage_forms: List<String> (e.g., ["tablet", "injectable"])
      - controlled_schedule: String or null (e.g., null, "II", "IV")
      - pregnancy_category: String (e.g., "X")
      
      Sample Nodes: Warfarin, Aspirin, Lisinopril, Metformin, Omeprazole
      Approximate Count: 50+ medications in graph

.. dropdown:: 📋 Task 1.2: Relationship Types (10+ required)
   :class-container: sd-border-primary

   Design relationships connecting the medical knowledge graph:
   
   - ``(:Disease)-[:PRESENTS_WITH {frequency}]->(:Symptom)``
   - ``(:Disease)-[:TREATED_BY {evidence_level}]->(:Medication)``
   - ``(:Medication)-[:INTERACTS_WITH {severity, description}]->(:Medication)`` **Critical for safety!**
   - ``(:Medication)-[:TARGETS]->(:Protein)``
   - ``(:Disease)-[:ASSOCIATED_WITH]->(:Gene)``
   - ``(:Disease)-[:RISK_FACTOR {relative_risk}]->(:Disease)``
   - ``(:Procedure)-[:INDICATED_FOR]->(:Disease)``
   - ``(:Lab_Test)-[:DIAGNOSES {sensitivity, specificity}]->(:Disease)``
   - ``(:Medication)-[:CONTRAINDICATED_IN]->(:Disease)``
   - ``(:Patient_Cohort)-[:ENROLLED_IN]->(:Clinical_Trial)``
   
   **Relationship Documentation Format**:
   
   .. code-block:: text
   
      Relationship: INTERACTS_WITH
      
      From: Medication
      To: Medication
      Direction: Bidirectional (create both directions)
      
      Properties:
      - severity: String ("minor", "moderate", "major", "contraindicated")
      - description: String (clinical description of interaction)
      - mechanism: String (e.g., "CYP2C9 inhibition")
      - clinical_significance: String (e.g., "Increased bleeding risk")
      
      Example:
      (Warfarin)-[:INTERACTS_WITH {
        severity: "major",
        description: "Increased bleeding risk",
        mechanism: "Both affect coagulation pathway"
      }]->(Aspirin)
      
      Count: 100+ interaction relationships
   
   **File to create**: ``docs/neo4j_graph_design.md``

.. dropdown:: 📋 Task 1.3: Graph Setup and Data
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
      CREATE (diabetes:Disease {
        name: 'Type 2 Diabetes', icd10: 'E11',
        category: 'Endocrine', chronic: true
      })
      CREATE (hypertension:Disease {
        name: 'Hypertension', icd10: 'I10',
        category: 'Cardiovascular', chronic: true
      })
      
      // Create drug interactions (CRITICAL)
      CREATE (warfarin)-[:INTERACTS_WITH {
        severity: 'major',
        description: 'Increased bleeding risk',
        mechanism: 'Both affect coagulation'
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
   
   - 50+ medication nodes
   - 30+ disease nodes
   - 40+ symptom nodes
   - 100+ INTERACTS_WITH relationships
   - 50+ TREATED_BY relationships
   - 30+ PRESENTS_WITH relationships
   - 20+ CONTRAINDICATED_IN relationships
   
   **File to create**: ``neo4j/graph_setup.cypher`` and ``neo4j/graph_data.cypher``


Part 2: Clinical Decision Support Queries
------------------------------------------

**Objective**: Write Cypher queries that provide real clinical value.

.. dropdown:: 📋 Task 2.1: Drug Safety Queries (3+ queries)
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

.. dropdown:: 📋 Task 2.2: Clinical Decision Support (3+ queries)
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
   
   **Comorbidity Exploration**:
   
   *"What conditions are risk factors for a given disease?"*
   
   **Symptom Differential Diagnosis**:
   
   *"Given symptoms [chest pain, shortness of breath], what diseases could this be?"*
   
   **Medication Alternatives**:
   
   *"Find alternatives for a medication, avoiding drug class X"*
   
   **Research Protocol Matching**:
   
   *"Find clinical trials matching a patient's conditions"*

.. dropdown:: 📋 Task 2.3: Advanced Graph Queries (2+ queries)
   :class-container: sd-border-primary

   **Multi-Hop Drug Interaction Paths**:
   
   *"Find indirect interaction risks through shared metabolic pathways"*
   
   **Treatment Optimization**:
   
   *"Find treatments that address multiple comorbidities simultaneously"*
   
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

**Objective**: Build unified API endpoints and deploy the full system with Docker Compose.

.. dropdown:: 📋 Task 3.1: Three-Database APIs (3 points)
   :class-container: sd-border-primary
   :open:

   **Endpoint 1**: ``GET /patients/{id}/complete-record``
   
   - PostgreSQL: Demographics, appointments, prescriptions, labs
   - MongoDB: Clinical notes, care plans, surveys
   - Neo4j: Current medication interaction check
   
   **Endpoint 2**: ``POST /prescriptions`` (with safety check)
   
   - Validate patient exists in PostgreSQL
   - Check drug interactions in Neo4j against current medication list
   - Check contraindications against patient's conditions
   - If safe: Save prescription to PostgreSQL
   - If unsafe: Return interaction warnings with severity
   - Log to audit trail
   
   **Endpoint 3**: ``GET /clinical-decision-support/treatment-options/{disease}``
   
   - Neo4j: Treatment pathways for disease
   - Neo4j: Contraindication checking against patient conditions
   - PostgreSQL: Patient's current medications and conditions
   
   **Endpoint 4**: ``GET /patients/{id}/interaction-report``
   
   - PostgreSQL: Current active medications
   - Neo4j: Full pairwise interaction analysis
   - Return sorted by severity with clinical descriptions
   
   **Prescription Safety Check Flow**:
   
   .. code-block:: text
   
      POST /prescriptions
      
      1. Validate patient_id exists (PostgreSQL)
      2. Validate medication_id exists (PostgreSQL formulary)
      3. Get patient's active medications (PostgreSQL)
      4. Check new medication against all active meds (Neo4j)
         - If CONTRAINDICATED interactions found: BLOCK, return error
         - If MAJOR interactions found: WARN, require override
         - If MODERATE interactions found: WARN, allow
         - If no interactions: PROCEED
      5. Check contraindications against patient conditions (Neo4j)
      6. If safe: INSERT into prescription table (PostgreSQL)
      7. Log audit entry (PostgreSQL)
      8. Return prescription with any warnings

.. dropdown:: 📋 Task 3.2: Production Deployment (2 points)
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
          environment:
            - DATABASE_URL=postgresql://...
            - MONGODB_URL=mongodb://mongodb:27017
            - NEO4J_URL=bolt://neo4j:7687
          ports:
            - "8000:8000"
   
   **Deployment Verification**:
   
   .. code-block:: text
   
      After running docker-compose up:
      
      1. PostgreSQL: psql connects, schema loaded, data present
      2. MongoDB: mongosh connects, 8+ collections, data loaded
      3. Neo4j: Browser at :7474, graph populated
      4. App: Swagger UI at http://localhost:8000/docs
      5. Prescription safety check works end-to-end
      6. Complete patient record returns data from all three databases
   
   **File to create**: ``docker-compose.yml`` and ``Dockerfile``


Part 4: Final Technical Report
-------------------------------

**Objective**: Write a comprehensive technical report documenting the complete HIPAA-compliant system.

.. dropdown:: 📋 Task 4.1: Report Structure (2 points)
   :class-container: sd-border-primary
   :open:

   **10 to 15 pages, submitted as PDF.**
   
   **1. Executive Summary** (1 page)
   
   - System overview and clinical context
   - Three-database architecture rationale
   - Key achievements (HIPAA compliance, drug safety)
   
   **2. HIPAA Compliance Approach** (1 page)
   
   - PHI identification and protection strategy
   - Role-based access control implementation
   - Audit logging architecture
   - Synthetic data approach
   
   **3. Architecture Overview** (2 to 3 pages)
   
   - System architecture diagram
   - Data flow diagrams for clinical workflows
   - Component descriptions for each database layer
   
   **4. Database Design Decisions** (3 to 4 pages)
   
   For each database (PostgreSQL, MongoDB, Neo4j):
   
   - What data and why
   - Schema/structure highlights
   - Key design decisions
   - Challenges and solutions
   
   **5. Clinical Decision Support Design** (2 pages)
   
   - Medical knowledge graph structure
   - Drug interaction checking algorithm
   - Prescription safety workflow
   - Integration with clinical APIs
   
   **6. Integration Architecture** (1 to 2 pages)
   
   - Cross-database queries and workflows
   - Consistency strategies
   - Error handling across databases
   
   **7. Performance Analysis** (1 page)
   
   - Benchmark results for key queries
   - Drug interaction check response times
   - Complete record assembly performance
   
   **8. Lessons Learned** (1 page)
   
   - What worked well
   - Challenges faced
   - What you would do differently
   - Future improvements
   
   **File to create**: ``docs/technical_report.pdf``


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP4_Healthcare_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP4_Healthcare_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP4_Healthcare_Team{X}/
   ├── postgresql/          # From GP2
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── mongodb/             # From GP3
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
   │   │   ├── audit_service.py
   │   │   ├── clinical_service.py
   │   │   └── prescription_safety.py
   │   └── api/
   │       └── endpoints.py
   ├── tests/
   │   ├── test_neo4j.py
   │   ├── test_integration.py
   │   └── test_prescription_safety.py
   ├── docker-compose.yml
   ├── Dockerfile
   ├── requirements.txt
   ├── docs/
   │   ├── neo4j_graph_design.md
   │   └── technical_report.pdf
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Part 1: Neo4j Graph Design
   :class-container: sd-border-info

   **Neo4j Files** (3 files):
   
   - ``neo4j/graph_setup.cypher`` - Node and relationship type creation
   - ``neo4j/graph_data.cypher`` - Medical knowledge data
   - ``neo4j/cypher_queries.cypher`` - 8+ clinical decision support queries
   
   **Documentation** (1 file):
   
   - ``docs/neo4j_graph_design.md`` - Graph structure documentation

.. dropdown:: 📄 Part 3: System Integration + Deployment
   :class-container: sd-border-info

   **Application** (updated src/ directory):
   
   - ``src/config/neo4j_config.py`` - Neo4j connection
   - ``src/repositories/neo4j/*.py`` - Graph query repositories
   - ``src/services/prescription_safety.py`` - Drug interaction checking
   - ``src/api/endpoints.py`` - Unified three-database API
   
   **Deployment** (2 files):
   
   - ``docker-compose.yml`` - All three databases + application
   - ``Dockerfile`` - Python application container

.. dropdown:: 📄 Part 4: Final Report + Supporting Files
   :class-container: sd-border-info

   **Report** (1 file):
   
   - ``docs/technical_report.pdf`` - 10 to 15 page comprehensive report
   
   **Supporting Files** (2 files):
   
   - ``README.md`` - Complete project overview with Docker setup
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP4: Healthcare Patient Management - Complete Polyglot System
   
   **Team Number**: [Your team number]
   
   **Scenario**: Healthcare Patient Management Platform
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Quick Start (Docker)
   
   ```bash
   docker-compose up --build
   ```
   
   This starts all three databases and the application:
   - PostgreSQL: localhost:5432
   - MongoDB: localhost:27017
   - Neo4j Browser: http://localhost:7474
   - API: http://localhost:8000/docs
   
   ## Architecture Summary
   
   | Database | Purpose | Data |
   |----------|---------|------|
   | PostgreSQL | Patient records, billing, audit | Demographics, prescriptions, claims |
   | MongoDB | Clinical documentation | Notes, care plans, surveys |
   | Neo4j | Medical knowledge | Drug interactions, disease pathways |
   
   ## Key Safety Features
   
   - Drug interaction checking on every new prescription
   - Contraindication alerts for patient conditions
   - HIPAA-compliant audit logging across all databases
   - Role-based access control
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP4
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Designed Neo4j medical knowledge graph
   - Created graph_setup.cypher and graph_data.cypher
   - Wrote drug interaction Cypher queries
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Built prescription safety service (three-database)
   - Implemented unified API endpoints
   - Wrote integration tests
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Created Docker Compose configuration
   - Built Dockerfile for application
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
   - Used [collaboration tools]
   - [Any other details]


Submission Checklist
---------------------

.. admonition:: ✅ Before Submitting
   :class: tip

   **Neo4j Graph** (3 files):
   
   - [ ] graph_setup.cypher creates 12+ node types
   - [ ] graph_data.cypher populates 50+ medications, 30+ diseases, 100+ interactions
   - [ ] cypher_queries.cypher contains 8+ clinical decision support queries
   - [ ] Drug interaction checking works for medication lists
   
   **System Integration**:
   
   - [ ] Unified API endpoints use all three databases
   - [ ] Prescription safety check works end-to-end
   - [ ] Complete patient record assembles from all three databases
   - [ ] Audit logging covers Neo4j access
   - [ ] Tests cover prescription safety and integration
   
   **Deployment** (2 files):
   
   - [ ] docker-compose.yml starts all services (PostgreSQL, MongoDB, Neo4j, app)
   - [ ] Dockerfile builds application correctly
   - [ ] ``docker-compose up`` results in working system
   - [ ] All databases accessible and loaded with data
   - [ ] Neo4j Browser accessible at localhost:7474
   
   **Final Report** (1 file):
   
   - [ ] 10 to 15 pages, submitted as PDF
   - [ ] HIPAA compliance section included
   - [ ] Architecture diagrams included
   - [ ] Clinical decision support design documented
   - [ ] Performance analysis with benchmarks
   
   **Quality Checks**:
   
   - [ ] Drug interaction check returns correct results for test cases
   - [ ] Contraindication alerts fire for known unsafe combinations
   - [ ] Technical report is professional and well-organized
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP4_Healthcare_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Trivial graph** - Only 5 medications and 3 diseases does not demonstrate clinical value
   
   ❌ **No bidirectional interactions** - Drug interactions go both ways. Create both directions
   
   ❌ **Prescription endpoint without safety check** - The whole point of Neo4j is preventing unsafe prescriptions
   
   ❌ **Docker volumes not configured** - Data lost on container restart
   
   ❌ **Hardcoded connection strings** - Use environment variables for all database URLs
   
   ❌ **Missing HIPAA section in report** - Compliance documentation is required
   
   ❌ **Thin technical report** - Under 10 pages or missing required sections
   
   ❌ **No performance benchmarks** - Report claims "safer" without actual test cases


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Neo4j Graph**
     - 2
     - 12+ node types with meaningful properties (1pt); 10+ relationship types with clinical relevance (1pt)
   * - **Part 2: Cypher Queries**
     - 3
     - Drug interaction checking works correctly (1.5pts); 8+ clinical decision support queries (1.5pts)
   * - **Part 3: System Integration**
     - 3
     - Prescription safety endpoint works end-to-end (1.5pts); Complete patient record from all databases (1.5pts)
   * - **Part 3: Deployment**
     - 2
     - Working Docker Compose with all services (1pt); All databases start and connect (1pt)
   * - **Part 4: Technical Report**
     - 3
     - Comprehensive and professional (1pt); HIPAA compliance documented (1pt); Performance analysis (1pt)
   * - **Bonus: Presentation**
     - +4
     - Clarity (1pt), Technical depth (1.5pts), Live demo (1pt), Q&A (0.5pt)
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
   2. HIPAA compliance approach (2 min)
   3. Live demonstration (6 min):
      
      - Show prescription safety check (drug interaction alert)
      - Demonstrate complete patient record from all databases
      - Show Neo4j Browser with medical knowledge graph
   
   4. Challenges and solutions (3 min)
   5. Q&A (2 min)


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP4**
   
   - **Build a meaningful graph** - Use real medication names, real ICD-10 codes, and real drug interactions. RxNorm and interaction databases are freely available for reference.
   - **Test the safety flow end-to-end** - Write test cases: "What happens when I prescribe Warfarin to a patient already on Aspirin?" The answer should be a major interaction warning.
   - **Test with Docker early** - Do not wait until the last day to containerize. Build and test Docker Compose incrementally.
   - **Write the report throughout** - Capture architecture decisions, screenshots, and test results as you build. Do not try to reconstruct everything at the end.
   - **Think about clinical impact** - Frame everything in terms of patient safety and clinical workflow. This makes the report and presentation much more compelling.
   - **Use office hours** - Bring Docker issues early. Discuss graph design and Cypher query strategies with instructors.


Final Project Summary
---------------------

.. admonition:: 🏆 Cumulative Achievement
   :class: note

   **Points**:
   
   - GP1: Relational Design = 10 points
   - GP2: PostgreSQL + Python = 15 points
   - GP3: MongoDB Integration = 10 points
   - GP4: Neo4j + Complete System = 15 points
   - **Total**: 50 points (40% of course grade)
   - **Optional Presentation**: +4 points (10% bonus)

**Your Achievement**:

You have built a production-grade HIPAA-compliant polyglot healthcare system demonstrating:

- HIPAA-compliant relational database design
- Role-based access control and comprehensive audit logging
- Clinical document management with flexible schemas
- Medical knowledge graph for clinical decision support
- Drug interaction checking for patient safety
- Cross-database integration for unified patient records
- Docker deployment of complex distributed systems
- Professional technical documentation

.. note::
   
   **Congratulations on completing the final project!**
   
   This system showcases real-world healthcare database engineering skills. The HIPAA compliance patterns, clinical decision support, and polyglot architecture you have implemented mirror challenges faced by professional healthcare IT engineers. Patient safety, data security, and clinical workflow integration are skills valued across the healthcare technology industry.