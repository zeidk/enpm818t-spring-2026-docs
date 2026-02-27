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

Your team will design and implement a comprehensive database system for a regional healthcare network operating 5 hospitals. The system must handle patient care workflows, clinical documentation, insurance billing, and medical knowledge while supporting clinical decision-making.

.. important::

   **Polyglot Persistence Architecture**

   This scenario demonstrates the power of using **three complementary databases**:

   - **PostgreSQL** for structured patient and operational data with ACID transactions
   - **MongoDB** for clinical documents and flexible healthcare data with semi-structured schemas
   - **Neo4j** for medical knowledge graph, drug interactions, and clinical decision support


Technology Stack
----------------

.. tab-set::

   .. tab-item:: PostgreSQL

      .. card:: Relational Database for Patient and Operational Data

         **Purpose**: Structured data with strong consistency and ACID transactions

         **What Data**:

         - Patient demographics (name, DOB, contact, insurance)
         - Healthcare providers (credentials, specialties, privileges)
         - Appointments (scheduling, status, check-in workflows)
         - Prescriptions (medications, dosages, refills, controlled substances)
         - Lab orders and results (test requests, findings, critical values)
         - Hospital admissions (inpatient stays, discharge summaries)
         - Insurance claims (billing, payment tracking, denials)
         - Medication formulary (approved drugs, interactions)

         **Why PostgreSQL**:

         - ACID transactions for billing and appointments
         - Complex relationships between patients, providers, services

   .. tab-item:: MongoDB

      .. card:: Document Database for Clinical Documentation

         **Purpose**: Semi-structured clinical documents that vary significantly by type and context

         **What Data**:

         - Clinical notes (progress notes, consultation reports, discharge summaries)
         - Medical imaging metadata (DICOM headers, study information)
         - Care plans (treatment protocols, goals, interventions)
         - Patient surveys (health questionnaires with different question sets)

         **Why MongoDB**:

         - Flexible schemas for different clinical note types
         - Embedded documents for complex nested data (care plans with protocols)
         - Variable question sets in surveys (PHQ-9, GAD-7, pain scales)
         - Text search on clinical narratives

   .. tab-item:: Neo4j

      .. card:: Graph Database for Medical Knowledge

         **Purpose**: Model and query complex medical relationships for clinical decision support and drug safety checking

         **Nodes**: Disease, Symptom, Medication, Procedure, Lab Test, ICD-10 Code

         **Relationships**: Disease PRESENTS_WITH Symptom, Disease TREATED_BY Medication, Medication INTERACTS_WITH Medication (critical for safety!), Procedure INDICATED_FOR Disease, Lab Test DIAGNOSES Disease, Medication CONTRAINDICATED_IN Disease

         **Why Neo4j**:

         - Drug interaction checking (path finding between medications)
         - Disease pathway analysis (treatment options)
         - Symptom differential diagnosis
         - Natural representation of medical relationships


Progressive Development
-----------------------

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
     - Chen ERD, Crow's Foot ERD, design report (8 to 12 pages)
   * - **GP2**
     - PostgreSQL + Python
     - 3 weeks
     - Secure schema, clinical queries, CLI application
   * - **GP3**
     - MongoDB Integration
     - 2 weeks
     - Clinical document schemas, aggregations, cross-database services
   * - **GP4**
     - Complete System
     - 2 weeks
     - Neo4j knowledge graph, Docker deployment, final report

.. dropdown:: GP1: Relational Database Design (2 weeks)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Design the PostgreSQL schema for patient and operational data:

   - Identify healthcare entities covering all seven business areas
   - Create **Conceptual Model** using Chen notation with (min,max) participation
   - Create **Logical Model** using Crow's Foot notation
   - Define keys with healthcare identifiers (MRN, NPI, DEA)
   - Identify healthcare-specific identifiers (MRN, NPI, DEA)
   - Normalize to 3NF with functional dependency proofs

   **Deliverables**: Chen ERD, Crow's Foot ERD, design report (8 to 12 pages)

.. dropdown:: GP2: PostgreSQL + Python Implementation (3 weeks)
   :icon: gear
   :class-container: sd-border-primary

   Implement secure relational database:

   - Create schema with constraints, indexes, and triggers
   - Generate synthetic healthcare data (NEVER use real patient data!)
   - Write 8+ clinical, financial, and operational SQL queries

   **Deliverables**: SQL scripts, Python CLI application

.. dropdown:: GP3: MongoDB Integration (2 weeks)
   :icon: gear
   :class-container: sd-border-primary

   Add document database for clinical documentation:

   - Design 4+ MongoDB collections for clinical documents
   - Choose embedding vs. referencing for clinical data
   - Write 6+ aggregation pipelines and text search queries
   - Integrate with PostgreSQL for unified patient records

   **Deliverables**: MongoDB schemas, clinical queries, integrated Python application

.. dropdown:: GP4: Neo4j + Complete System (2 weeks)
   :icon: gear
   :class-container: sd-border-primary

   Add medical knowledge graph and complete the system:

   - Design graph with 6+ node types (diseases, medications, symptoms)
   - Model 6+ relationship types (interactions, treatments, contraindications)
   - Write 6+ Cypher queries for clinical decision support
   - Implement drug interaction checking
   - Deploy with Docker Compose
   - Write final technical report (8 to 12 pages)

   **Deliverables**: Neo4j graph, clinical decision support CLI, deployed system, final report


Key Design Challenges
---------------------

.. warning::

   **Critical Decisions You'll Make**

   These choices will significantly impact your system's safety and usability.

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Challenge 1: Healthcare Data Complexity

      **Question**: How do you model complex clinical workflows with interconnected data?

      **Considerations**:

      - De-identification for research use
      - Minimum necessary access principle

   .. grid-item-card:: Challenge 2: Data Partitioning

      **Question**: Which clinical data belongs in which database?

      **Approaches**:

      - PostgreSQL: Structured transactional data (demographics, appointments, billing)
      - MongoDB: Variable-structure documents (clinical notes, care plans, surveys)
      - Neo4j: Medical knowledge relationships (drug interactions, disease pathways)

      You must justify every decision!

   .. grid-item-card:: Challenge 3: Drug Interaction Safety

      **Question**: How do you check for dangerous drug combinations?

      **Solution with Neo4j**:

      - Model medications as nodes
      - INTERACTS_WITH relationships with severity levels
      - Graph queries to find interaction paths
      - Real-time checking when prescriptions are created

   .. grid-item-card:: Challenge 4: Cross-Database Clinical Workflows

      **Question**: How do you query patient data spanning three databases?

      **Example**:

      - Patient demographics from PostgreSQL
      - Recent clinical notes from MongoDB
      - Drug interaction check from Neo4j
      - Combine in Python service layer


Common Pitfalls
---------------

.. danger::

   **Avoid These Mistakes**

   - **Using real patient data**: NEVER use real patient data. Always use synthetic data.
   - **Over-simplifying insurance**: Primary/secondary coverage, pre-auth, and claims lifecycle are all important.
   - **Ignoring provider credentials**: Licenses expire. DEA numbers are required for controlled substances.
   - **Treating all clinical notes the same**: Progress notes, consultation reports, and discharge summaries have different structures.
   - **No drug interaction checking**: Patient safety depends on automated medication safety checks.


Support Resources
-----------------

.. grid:: 2
   :gutter: 3

   .. grid-item-card:: Office Hours
      :class-card: sd-border-info

      - Bring healthcare-specific questions
      - Discuss schema design strategies
      - Review clinical workflow designs
      - Show your ERD sketches for feedback
      - Debug complex Neo4j graph queries

   .. grid-item-card:: Technical Documentation
      :class-card: sd-border-info

      - `HL7 FHIR <https://www.hl7.org/fhir/>`_
      - `ICD-10 Codes <https://www.icd10data.com/>`_
      - `RxNorm (Medications) <https://www.nlm.nih.gov/research/umls/rxnorm/>`_


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
