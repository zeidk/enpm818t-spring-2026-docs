====================================================
Scenario 2: Healthcare Patient Management Platform
====================================================

.. only:: html

   .. figure:: /_static/images/final_project/hospital_light.png
      :alt: Healthcare patient management platform (credit OpenAI)
      :width: 80%
      :align: center
      :class: only-light

      *Healthcare patient management platform (credit OpenAI)*

   .. figure:: /_static/images/final_project/hospital_dark.png
      :alt: Healthcare patient management platform (credit OpenAI)
      :width: 80%
      :align: center
      :class: only-dark

.. only:: latex

   .. figure:: /_static/images/final_project/hospital_light.png
      :alt: Healthcare patient management platform
      :width: 80%
      :align: center

      *Healthcare patient management platform*

Overview
--------

Your team will design and implement a comprehensive database system for a regional healthcare network operating 5 hospitals. The system must handle patient care workflows, clinical documentation, insurance billing, and medical knowledge while maintaining strict HIPAA compliance and supporting clinical decision-making.

.. important::
   
   **Polyglot Persistence Architecture**
   
   This scenario demonstrates the power of using **three complementary databases**:
   
   - **PostgreSQL** for structured patient and operational data with ACID transactions and HIPAA audit trails
   - **MongoDB** for clinical documents and flexible healthcare data with semi-structured schemas
   - **Neo4j** for medical knowledge graph, drug interactions, and clinical decision support


System Requirements
-------------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🏥 Core Capabilities
      :class-card: sd-border-primary
      
      - Patient demographics and insurance management
      - Clinical workflows (appointments, prescriptions, lab orders)
      - Healthcare provider credentials and scheduling
      - Billing and insurance claims processing
      - Hospital admissions and discharge management
      - HIPAA-compliant audit trails for all PHI access

   .. grid-item-card:: 🔒 Compliance Requirements
      :class-card: sd-border-success
      
      - HIPAA Privacy Rule for all Protected Health Information
      - Audit logging for all PHI access (who, what, when, why)
      - Role-based access control (physicians, nurses, billing)
      - Medical record retention compliance
      - De-identification support for research use cases


Technology Stack
----------------

.. tab-set::

   .. tab-item:: PostgreSQL

      .. card:: Relational Database for Patient and Operational Data
         :class-card: sd-bg-light
      
         **Purpose**: Structured data with strong consistency, ACID transactions, and HIPAA audit trails
         
         **What Data**:
         
         - Patient demographics (name, DOB, contact, insurance)
         - Healthcare providers (credentials, specialties, privileges)
         - Appointments (scheduling, status, check-in workflows)
         - Prescriptions (medications, dosages, refills, controlled substances)
         - Lab orders and results (test requests, findings, critical values)
         - Hospital admissions (inpatient stays, discharge summaries)
         - Insurance claims (billing, payment tracking, denials)
         - Medication formulary (approved drugs, interactions)
         - Audit logs (all PHI access for HIPAA compliance)
         
         **Why PostgreSQL**:
         
         - ACID transactions for billing and appointments
         - Complex relationships between patients, providers, services
         - Mature security features (row-level security, roles)
         - Reliable audit logging with triggers
         - Referential integrity enforcement

   .. tab-item:: MongoDB

      .. card:: Document Database for Clinical Documentation
         :class-card: sd-bg-light
      
         **Purpose**: Semi-structured clinical documents and healthcare data that varies significantly by type and context
         
         **What Data**:
         
         - Clinical notes (progress notes, consultation reports, discharge summaries)
         - Medical imaging metadata (DICOM headers, study information, radiologist reports)
         - Care plans (treatment protocols, goals, interventions)
         - Patient surveys (health questionnaires with different question sets)
         - Adverse events (incident reports with embedded investigation details)
         - Telemedicine sessions (virtual visit records, session logs, transcripts)
         - Research consents (clinical trial participation, versioned consent forms)
         - Patient preferences (advanced directives, communication preferences)
         
         **Why MongoDB**:
         
         - Flexible schemas for different clinical note types
         - Embedded documents for complex nested data (care plans with protocols)
         - Variable question sets in surveys (PHQ-9, GAD-7, pain scales)
         - Text search on clinical narratives
         - Schema evolution without migrations

   .. tab-item:: Neo4j

      .. card:: Graph Database for Medical Knowledge
         :class-card: sd-bg-light
      
         **Purpose**: Model and query complex medical relationships for clinical decision support and drug safety checking
         
         **What Data**:
         
         **Nodes**: Disease, Symptom, Medication, Procedure, Lab Test, Gene, Protein, Patient Cohort, Clinical Trial, Biomarker, ICD-10 Code, CPT Code
         
         **Relationships**: Disease PRESENTS_WITH Symptom, Disease TREATED_BY Medication, Medication INTERACTS_WITH Medication (critical for safety!), Medication TARGETS Protein, Disease ASSOCIATED_WITH Gene, Disease RISK_FACTOR Disease, Procedure INDICATED_FOR Disease, Lab Test DIAGNOSES Disease, Medication CONTRAINDICATED_IN Disease
         
         **Why Neo4j**:
         
         - Drug interaction checking (path finding between medications)
         - Disease pathway analysis (treatment options for complex conditions)
         - Comorbidity exploration (related conditions)
         - Clinical decision support (graph queries for recommendations)
         - Symptom differential diagnosis (possible diseases from symptoms)
         - Natural representation of medical relationships


Business Context
----------------

.. admonition:: 🏥 The Challenge
   :class: note

   A regional healthcare network with 5 hospitals, 20 outpatient clinics, 500+ providers, and 250,000+ patients faces challenges with disconnected legacy systems. Clinical staff waste time searching multiple systems for patient information. Medication errors occur due to lack of integrated drug interaction checking. Insurance claim denials are high due to incomplete documentation. Research opportunities are missed because clinical data is not structured for analysis.

**Your Solution**:

Design a modern, integrated system that:

1. **Unifies** patient records across all facilities in the network
2. **Supports** clinical workflows from appointment scheduling through discharge
3. **Ensures** HIPAA compliance with comprehensive audit trails
4. **Prevents** medication errors through automated interaction checking
5. **Streamlines** billing with integrated claims management
6. **Enables** clinical research with de-identified data access
7. **Provides** clinical decision support using medical knowledge graphs

**Stakeholders**:

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Clinical Staff
      :class-card: sd-border-primary
      
      - **Physicians**: Complete patient history, drug interaction alerts, evidence-based treatment options
      - **Nurses**: Quick access to orders, medication administration records, care plans
      - **Pharmacists**: Prescription review, interaction checking, patient counseling

   .. grid-item-card:: Administrative Staff
      :class-card: sd-border-primary
      
      - **Billing Staff**: Insurance claims processing, payment tracking, patient balances
      - **Administrators**: Operational metrics, compliance monitoring, quality indicators
      - **Researchers**: De-identified data access for clinical studies


Progressive Development
-----------------------

.. admonition:: 🏗️ Four Cumulative Projects
   :class: tip

   Each group project builds on the previous work, creating a complete HIPAA-compliant system by the end!

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
     - 3 weeks
     - Chen and Crow's Foot ERDs, PHI Designation, Normalization
   * - **GP2**
     - PostgreSQL + Python
     - 6 weeks
     - HIPAA Schema, Clinical Queries, Secure REST API
   * - **GP3**
     - MongoDB Integration
     - 3 weeks
     - Clinical Document Schemas, Aggregations, Integration
   * - **GP4**
     - Complete System
     - 4 weeks
     - Neo4j Knowledge Graph, Docker Deployment, Final Report


.. dropdown:: 📋 GP1: Relational Database Design (3 weeks)
   :class-container: sd-border-primary
   :open:

   Design the PostgreSQL schema for patient and operational data:
   
   - Identify 13+ healthcare entities from business requirements
   - Create **Conceptual Model** using Chen notation
   - Create **Logical Model** using Crow's Foot notation
   - Define keys with healthcare identifiers (MRN, NPI, DEA)
   - Designate Protected Health Information (PHI)
   - Normalize to 3NF with clinical workflow analysis
   - Analyze denormalization trade-offs for healthcare data
   
   **Deliverables**: ERDs (both notations), entity catalog, PHI matrix, normalization proofs

.. dropdown:: 📋 GP2: PostgreSQL + Python Implementation (6 weeks)
   :class-container: sd-border-primary

   Implement HIPAA-compliant relational database:
   
   - Create schema with security controls and audit triggers
   - Generate synthetic healthcare data (NEVER use real patient data!)
   - Write 10+ clinical and business queries (medication safety, billing analytics, quality metrics)
   - Build Python application with role-based access control
   - Create secure REST API with audit logging
   - Write comprehensive tests (>70% coverage)
   
   **Deliverables**: SQL scripts, secure Python application, HIPAA compliance documentation

.. dropdown:: 📋 GP3: MongoDB Integration (3 weeks)
   :class-container: sd-border-primary

   Add document database for clinical documentation:
   
   - Design 8+ MongoDB collections for clinical documents
   - Choose embedding vs. referencing for clinical data
   - Create indexes for clinical query patterns
   - Write 8+ aggregation pipelines for healthcare analytics
   - Integrate with PostgreSQL for unified patient records
   - Implement cross-database clinical workflows
   
   **Deliverables**: MongoDB schemas, clinical queries, integrated Python application

.. dropdown:: 📋 GP4: Neo4j + Complete System (4 weeks)
   :class-container: sd-border-primary

   Add medical knowledge graph and complete the system:
   
   - Design graph with 12+ node types (diseases, medications, symptoms)
   - Model 10+ relationship types (interactions, treatments, contraindications)
   - Write 8+ Cypher queries for clinical decision support
   - Implement drug interaction checking
   - Create APIs using all three databases
   - Deploy with Docker Compose
   - Write comprehensive technical report (10 to 15 pages)
   
   **Deliverables**: Neo4j graph, clinical decision support API, deployed system, final report


Key Design Challenges
---------------------

.. warning::
   
   **Critical Decisions You'll Make**
   
   These are not trivial choices. They will significantly impact your system's compliance, safety, and usability!

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 🔒 Challenge 1: HIPAA Compliance
      
      **Question**: How do you protect PHI while enabling necessary clinical access?
      
      **Considerations**:
      
      - Role-based access control (physicians see everything, billing sees limited)
      - Audit logging for all PHI access (who, what, when, why)
      - Encryption at rest and in transit
      - De-identification for research use
      - Minimum necessary access principle

   .. grid-item-card:: 🎯 Challenge 2: Data Partitioning
      
      **Question**: Which clinical data belongs in which database?
      
      **Approaches**:
      
      - PostgreSQL: Structured transactional data (demographics, appointments, billing)
      - MongoDB: Variable-structure documents (clinical notes, care plans, surveys)
      - Neo4j: Medical knowledge relationships (drug interactions, disease pathways)
      
      You must justify every decision!

   .. grid-item-card:: 💊 Challenge 3: Drug Interaction Safety
      
      **Question**: How do you check for dangerous drug combinations?
      
      **Solution with Neo4j**:
      
      - Model medications as nodes
      - INTERACTS_WITH relationships with severity levels
      - Graph queries to find interaction paths
      - Real-time checking when prescriptions are created

   .. grid-item-card:: 🔗 Challenge 4: Cross-Database Clinical Workflows
      
      **Question**: How do you query patient data spanning three databases?
      
      **Example**:
      
      - Patient demographics from PostgreSQL
      - Recent clinical notes from MongoDB
      - Drug interaction check from Neo4j
      - Combine in Python service layer


Learning Objectives
-------------------

.. admonition:: 🎓 What You'll Master
   :class: note

   By completing this scenario, you will:
   
   ✅ Design HIPAA-compliant database schemas with audit controls
   
   ✅ Implement role-based access control and PHI protection
   
   ✅ Model healthcare-specific identifiers (MRN, NPI, DEA numbers)
   
   ✅ Write clinical and financial queries for healthcare operations
   
   ✅ Design flexible document schemas for clinical documentation
   
   ✅ Use MongoDB aggregation for healthcare analytics
   
   ✅ Model medical knowledge as graph structures
   
   ✅ Write Cypher queries for clinical decision support
   
   ✅ Implement drug interaction checking using graph traversals
   
   ✅ Deploy secure healthcare systems with compliance controls


Success Criteria
----------------

.. list-table::
   :header-rows: 1
   :widths: 30 70
   :class: compact-table

   * - Category
     - Evaluation Criteria
   * - **Functionality** (30%)
     - All clinical workflows implemented; Queries return medically accurate results; APIs work as documented; System handles concurrent clinical users
   * - **HIPAA Compliance** (25%)
     - Comprehensive audit logging; Role-based access control; PHI protection measures; Appropriate de-identification
   * - **Design Quality** (20%)
     - Appropriate database selection; Well-normalized PostgreSQL schema; Flexible MongoDB document designs; Meaningful Neo4j graph structure
   * - **Code Quality** (15%)
     - Clean, secure code; Proper error handling; Comprehensive tests; Security best practices
   * - **Technical Report** (10%)
     - Clear clinical context; Design decisions justified; HIPAA compliance explained; Professional presentation


Common Pitfalls
---------------

.. danger::
   
   **Avoid These Mistakes!**
   
   Learn from past teams' experiences:

.. grid:: 2
   :gutter: 2

   .. grid-item::
      
      ❌ **Using Real Patient Data**
      
      NEVER use real data. This is a HIPAA violation! Always use synthetic data.

   .. grid-item::
      
      ❌ **Missing Audit Trails**
      
      HIPAA requires comprehensive logging. Design audit from Day 1, not as an afterthought.

   .. grid-item::
      
      ❌ **Over-simplifying Insurance**
      
      Insurance is complex (primary/secondary, pre-auth, claims). Do not shortcut it.

   .. grid-item::
      
      ❌ **Ignoring Provider Credentials**
      
      Licenses expire and must be tracked. DEA numbers are required for controlled substances.

   .. grid-item::
      
      ❌ **Treating All Clinical Notes the Same**
      
      Progress notes, consultation reports, and discharge summaries have different structures.

   .. grid-item::
      
      ❌ **No Drug Interaction Checking**
      
      Patient safety depends on automated medication safety checks.


Getting Started
---------------

.. tip::
   
   **First Steps**
   
   1. Review this specification thoroughly
   2. Form your team (4 students)
   3. Discuss whether healthcare domain interests your team
   4. Compare with Scenario 1 (Traffic Management)
   5. Submit scenario choice via Canvas

.. admonition:: 📅 Project Timeline
   :class: important

   Once you begin:
   
   - **Immediately**: Read business requirements carefully
   - **First Few Days**: Research healthcare identifiers (MRN, NPI, DEA)
   - **Throughout GP1**: Sketch initial ERD, identify clinical entities and workflows
   - **Continuously**: Use office hours for healthcare domain questions
   
   **Pro Tips**:
   
   - Healthcare domain is complex. Ask questions early
   - Research real EHR workflows online
   - Think about patient safety throughout
   - HIPAA compliance is non-negotiable
   - Start early. Each GP takes substantial time
   - Use version control from Day 1 (Git/GitHub)


Support Resources
-----------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: 👥 Office Hours
      :class-card: sd-border-info
      
      - Bring healthcare-specific questions
      - Discuss HIPAA compliance strategies
      - Review clinical workflow designs
      - Show your ERD sketches for feedback
      - Debug complex Neo4j graph queries

   .. grid-item-card:: 💬 Discussion Forum
      :class-card: sd-border-info
      
      - Post healthcare domain questions
      - Share general HIPAA compliance strategies (not code)
      - Learn from other teams' challenges
      - Collaborative problem-solving

.. card:: 📚 Technical Documentation
   :class-card: sd-bg-light
   
   - **HL7 FHIR**: https://www.hl7.org/fhir/
   - **ICD-10 Codes**: https://www.icd10data.com/
   - **CPT Codes**: https://www.ama-assn.org/practice-management/cpt
   - **HIPAA Guidelines**: https://www.hhs.gov/hipaa/
   - **RxNorm (Medications)**: https://www.nlm.nih.gov/research/umls/rxnorm/
   - **PostgreSQL Security**: https://www.postgresql.org/docs/current/user-manag.html
   - **MongoDB Healthcare**: https://www.mongodb.com/solutions/industries/healthcare
   - **Neo4j Healthcare**: https://neo4j.com/use-cases/life-sciences-healthcare/


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
   - Discuss with your team whether healthcare excites you
   - Compare with Scenario 1 (Traffic Management)
   - Make your scenario selection
   - Begin researching clinical workflows and HIPAA requirements!

.. note::
   
   **Remember**: This is a portfolio-worthy project. Take pride in your work, ask questions when stuck, and enjoy building a real-world HIPAA-compliant polyglot persistence system!