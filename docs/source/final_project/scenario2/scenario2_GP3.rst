=========================================================================
Group Project 3: Complete Polyglot System (MongoDB + Neo4j)
=========================================================================

Overview
--------

This is the **final deliverable** of the course. You will combine MongoDB
(for semi-structured clinical documents) and Neo4j (for a medical
knowledge graph and clinical decision support) with the PostgreSQL
system you built in GP2, producing a **complete three-database polyglot
architecture** deployed via Docker Compose. You will also write a
final **technical report** documenting the system end-to-end.

.. card::
   :class-card: sd-bg-dark sd-text-white sd-shadow-sm

   **GP3 -- At a Glance**

   .. list-table::
      :widths: 30 70
      :class: compact-table

      * - **Posted**
        - Friday 04/24/2026
      * - **Due**
        - Monday 05/12/2026 at 11:59 PM
      * - **Duration**
        - ~2.5 weeks
      * - **Weight**
        - 25 points (50% of final project, includes final report)
      * - **Builds on**
        - Your secure PostgreSQL system from GP2
      * - **Team Size**
        - 4 students
      * - **Submission**
        - Canvas + GitHub repository link

.. admonition:: What Changed from the Original Schedule
   :class: note

   This assignment **combines the original GP3 (MongoDB) and GP4
   (Neo4j + complete system + report)** into a single final deliverable
   because of the compressed end-of-semester schedule. The scope has
   been trimmed so the project remains achievable in ~2.5 weeks:

   - Cypher queries reduced from 6+ to 4 (and graph minimum sizes
     reduced proportionally)
   - Unified cross-database CLI operations reduced from 3 to 2
   - Technical report: outline kept; no strict page limit
   - Optional presentation has been dropped

.. admonition:: What Carries Over from GP2
   :class: important

   GP3 **extends** the system you built in GP2 -- you are not starting
   from scratch. Your GP2 deliverables form the PostgreSQL layer of the
   final polyglot system:

   - **postgresql/schema.sql** and **postgresql/data.sql**: Reuse
     directly. Place them in the ``postgresql/`` directory so Docker
     Compose seeds them on first boot.
   - **postgresql/queries.sql**: Include in your submission for
     completeness; no changes required.
   - **config/**, **models/**, **repositories/**, **services/**,
     **cli/**: If your GP2 submission placed these under a ``src/``
     directory, move them to the **project root** so the folder
     structure matches the GP3 layout below and the provided
     Dockerfile (which runs ``python -m cli.main``).
   - **config/database.py**: Your existing PostgreSQL connection
     module. You will add ``mongodb.py`` and ``neo4j_config.py``
     alongside it.
   - **repositories/**: Extend with ``mongodb/`` and ``neo4j/``
     subdirectories. Move your existing PostgreSQL repositories into
     a ``postgres/`` subdirectory for organization.
   - **services/**, **cli/main.py**: Extend with MongoDB and Neo4j
     support. Your existing PostgreSQL menu options should continue
     to work unchanged.
   - **models/**: Keep your existing dataclasses; add new ones only
     if needed for cross-database service results.
   - **requirements.txt**: Add ``pymongo`` and ``neo4j`` to your
     existing dependencies.
   - **.env.example**: Add ``MONGO_*`` and ``NEO4J_*`` variables
     alongside your existing ``DB_*`` variables.
   - **.env**: GP2 required ``.env`` to be in ``.gitignore``. For
     GP3 you must **commit** ``.env`` with actual values so
     I can run your system (see "Credentials for Grading"
     below).


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Recognize when document databases are appropriate for clinical data
- Design flexible document schemas for clinical documentation
- Choose embedding vs. referencing for healthcare data
- Write MongoDB aggregation pipelines and text search on clinical
  narratives
- Design medical knowledge graphs with clinically meaningful
  relationships
- Write Cypher queries for drug interaction checking
- Implement clinical decision support using graph traversals
- Build a complete three-database healthcare architecture
- Deploy polyglot systems using Docker Compose
- Document complex clinical systems professionally


Part 1: Polyglot Persistence Design
------------------------------------

**Objective**: Analyze your clinical data and decide what belongs in
PostgreSQL, MongoDB, or Neo4j.

.. admonition:: Task 1.1: Data Partitioning Analysis (2 points)
   :class: task

   For each data type in your healthcare system, evaluate whether it
   belongs in **PostgreSQL**, **MongoDB**, or **Neo4j**. Consider:

   1. **Structure**: Fixed schema or variable by clinical context?
   2. **Consistency**: Strong ACID needed or eventual consistency OK?
   3. **Relationships**: Many foreign keys, self-contained documents,
      or networked knowledge?
   4. **Query Pattern**: Complex JOINs, document retrieval, or
      multi-hop graph traversal?
   5. **Volume**: Moderate or high write throughput?
   6. **Evolution**: Schema stable or changes with clinical practice?

   **Decision Template** -- complete one entry for each **new** data
   type you are adding to MongoDB or Neo4j (e.g., clinical notes,
   imaging metadata, care plans, diseases, medications, drug
   interactions). You do not need to re-justify data that stays in
   PostgreSQL from GP2 -- a brief summary table listing those data
   types and stating "remains in PostgreSQL (unchanged from GP2)" is
   sufficient. The example below shows the expected depth for new
   data types; include your completed templates in
   ``docs/polyglot_design.pdf``.

   .. code-block:: text

      Data Type: Clinical Notes

      Analysis:
      1. Structure: Variable (progress notes, consult reports,
         discharge summaries all have different fields)
      2. Consistency: Eventual OK (notes are append-only, rarely edited)
      3. Relationships: Minimal (references patient_id and provider_id)
      4. Query Pattern: Document retrieval by patient, text search
      5. Volume: Moderate (10-50 notes per patient per year)
      6. Evolution: High (new note templates added frequently)

      Decision: MongoDB
      Justification: Variable structure per note type, text search
                     needed, minimal relational needs, schema evolves
                     with practice

   The following is a **recommended** starting point, not a mandate.
   You may follow these suggestions, adjust them, or propose a
   different partitioning -- as long as you justify every decision
   in your ``docs/polyglot_design.pdf`` using the Decision Template
   above.

   **Keep in PostgreSQL** (from GP2):

   - Patient demographics (structured, ACID, access-controlled)
   - Appointments and scheduling (complex relationships)
   - Prescriptions and medications (strong consistency required)
   - Insurance claims and billing (financial accuracy, ACID)

   **Candidates for MongoDB**:

   - **Clinical notes**: variable structure by note type (progress,
     consult, discharge)
   - **Medical imaging metadata**: DICOM headers vary by modality
     (CT, MRI, X-ray)
   - **Care plans**: nested protocols, goals, interventions
   - **Patient surveys**: different question sets by survey type
     (PHQ-9, GAD-7, pain scales)

   **Candidates for Neo4j**:

   - **Diseases** with ICD-10 codes, category, chronic/acute
   - **Medications** with drug class, dosage forms
   - **Symptoms** and **lab tests**
   - **Drug interactions** (bidirectional, severity)
   - **Treatment pathways** (disease → medication) with evidence level
   - **Contraindications** (medication → disease)

   If you deviate from these suggestions, explain what you changed
   and why in your design document.

   Document your decisions and rationale in
   ``docs/polyglot_design.pdf``. This file should also include your
   MongoDB collection schemas (Part 2), Neo4j node/relationship
   catalog (Part 4), and index strategy.

   **File to create**: ``docs/polyglot_design.pdf``


Part 2: MongoDB Schema Design
------------------------------

**Objective**: Design document schemas for at least 4 collections with
appropriate indexes.

.. admonition:: Task 2.1: Required Collections (2 points)
   :class: task

   Design **at least 4 collections**. Two detailed examples are
   provided below; design at least two more of your own.

   **1. clinical_notes**

   Variable structure by note type:

   .. code-block:: javascript

      // Progress Note
      {
        "_id": ObjectId(...),
        "patient_id": 12345,       // References PostgreSQL
        "provider_id": 789,        // References PostgreSQL
        "encounter_date": ISODate("2026-02-15"),
        "note_type": "progress_note",
        "chief_complaint": "Follow-up for hypertension management",
        "review_of_systems": {
          "cardiovascular": "No chest pain, no palpitations",
          "respiratory": "No shortness of breath"
        },
        "physical_exam": {
          "vitals": {
            "bp_systolic": 138, "bp_diastolic": 85,
            "heart_rate": 72, "temperature": 98.6
          },
          "findings": "Heart regular rate and rhythm..."
        },
        "assessment": "Hypertension, improving on current regimen",
        "plan": "Continue lisinopril 10mg daily, recheck in 3 months",
        "icd10_codes": ["I10"],
        "signed": true,
        "signed_date": ISODate("2026-02-15T16:30:00Z")
      }

      // Consultation Report (different structure)
      {
        "_id": ObjectId(...),
        "patient_id": 12345,
        "provider_id": 456,
        "encounter_date": ISODate("2026-02-18"),
        "note_type": "consultation",
        "requesting_provider_id": 789,
        "reason_for_consultation": "Evaluate cardiac murmur",
        "findings": "Grade II/VI systolic murmur...",
        "recommendations": "Recommend echocardiogram...",
        "urgency": "routine"
      }

   **2. medical_images_metadata**

   DICOM headers vary by imaging modality:

   .. code-block:: javascript

      {
        "patient_id": 12345,
        "study_date": ISODate("2026-02-10"),
        "modality": "CT",
        "body_part": "chest",
        "study_description": "CT Chest with contrast",
        "dicom_metadata": {
          "study_uid": "1.2.840.113619...",
          "series_count": 3,
          "image_count": 245,
          "slice_thickness": 1.25
        },
        "radiologist_report": {
          "provider_id": 321,
          "findings": "No pulmonary embolism...",
          "impression": "Normal CT chest",
          "critical_finding": false
        }
      }

   **3-4. Your additional collections**: Choose from care_plans,
   patient_surveys, adverse_events, telemedicine_sessions, or others
   that make sense for your system.

   **Schema Documentation Format** (include in
   ``docs/polyglot_design.pdf``):

   .. code-block:: text

      Collection: clinical_notes

      Purpose: Store clinical documentation with variable structure by
      note type

      Document Structure:
      - _id: ObjectId (auto-generated)
      - patient_id: Integer (references PostgreSQL)
      - provider_id: Integer (references PostgreSQL)
      - encounter_date: ISODate
      - note_type: String (enum: progress_note, consultation,
        discharge_summary)
      - [remaining fields vary by note_type]

      Embedding Rationale: Vital signs embedded within physical_exam
        because they are always queried with the parent note and
        are bounded.

.. admonition:: Task 2.2: Index Strategy (1 point)
   :class: task

   For each collection, define appropriate indexes and document them
   in ``docs/polyglot_design.pdf``.

   **Index types to consider**:

   - **Compound Indexes**: (patient_id, encounter_date) for patient
     timeline queries
   - **Text Indexes**: Full-text search on clinical narratives
     (chief_complaint, assessment, plan)
   - **TTL Indexes**: Auto-delete telemedicine session logs after
     retention period
   - **Partial Indexes**: Unsigned notes only (for provider review
     workflow)


Part 3: MongoDB Implementation
-------------------------------

**Objective**: Set up MongoDB collections and write clinical queries.

.. admonition:: Task 3.1: Database Setup (1 point)
   :class: task

   Create ``mongo_setup.js`` to define collections with validation
   and indexes:

   .. code-block:: javascript

      use healthcare_management;

      db.createCollection("clinical_notes", {
        validator: {
          $jsonSchema: {
            bsonType: "object",
            required: ["patient_id", "provider_id",
                       "encounter_date", "note_type"],
            properties: {
              patient_id: { bsonType: "int" },
              provider_id: { bsonType: "int" },
              encounter_date: { bsonType: "date" },
              note_type: {
                enum: ["progress_note", "consultation",
                       "discharge_summary", "procedure_note"]
              }
            }
          }
        }
      });

      // Patient timeline index
      db.clinical_notes.createIndex(
        { patient_id: 1, encounter_date: -1 }
      );

      // Full-text search on clinical narratives
      db.clinical_notes.createIndex({
        "chief_complaint": "text",
        "assessment": "text",
        "plan": "text"
      });

   Create ``mongo_data.js`` with realistic clinical document data:

   - 200+ clinical notes across multiple note types
   - 100+ imaging metadata records
   - Appropriate volumes for your additional collections

   **Files to create**: ``mongodb/mongo_setup.js`` and
   ``mongodb/mongo_data.js``

.. admonition:: Task 3.2: Query Development (2 points)
   :class: task

   Write **at least 6 MongoDB queries** covering the following
   categories:

   **Aggregation Pipelines (3 queries minimum)**

   Examples:

   - *"Clinical documentation volume by provider and note type."*
   - *"Patient survey scoring and trend analysis (e.g., PHQ-9
     depression screening)."*
   - *"Average time between admission and discharge summary
     completion."*

   **Text Search (1 query minimum)**

   Example: *"Search clinical notes for a specific diagnosis or
   symptom across all note types."*

   **Array Operations (2 queries minimum)**

   Examples:

   - *"Care plan progress tracking using $unwind on goals array."*
   - *"Find notes with specific ICD-10 codes using $elemMatch."*

   **Query Documentation Format**:

   .. code-block:: javascript

      // Query #X: [Title]
      // Clinical Context: [Why this matters for patient care]
      // Collections Used: [List collections]
      // Pipeline Stages: [e.g., $match, $group, $sort]

      [YOUR MONGODB QUERY]

      // Expected Output: [Description of result shape]
      // Sample Results: [First 2-3 documents]

   **File to create**: ``mongodb/mongo_queries.js``


Part 4: Neo4j Medical Knowledge Graph
--------------------------------------

**Objective**: Design a medical knowledge graph with clinically
meaningful node types and relationships, and write Cypher queries for
clinical decision support.

.. admonition:: Task 4.1: Graph Structure (2 points)
   :class: task

   Design a graph with at least **4 node types** and **4
   relationship types**.

   **Required Node Types** (minimum 4):

   - **Disease**: name, ICD-10 code, category, chronic/acute
   - **Medication**: name, drug class, dosage forms, controlled
     schedule
   - **Symptom**: name, body system, severity range
   - **Procedure** or **Lab Test**: pick one

   You may add more node types (Gene, Protein, Clinical Trial,
   Biomarker) if they serve your clinical use cases.

   **Required Relationship Types** (minimum 4):

   - ``(:Medication)-[:INTERACTS_WITH {severity, description}]->(:Medication)`` **Critical for safety!**
   - ``(:Disease)-[:TREATED_BY {evidence_level}]->(:Medication)``
   - ``(:Medication)-[:CONTRAINDICATED_IN]->(:Disease)``
   - ``(:Disease)-[:PRESENTS_WITH {frequency}]->(:Symptom)``

   **Node Documentation Format** (include in
   ``docs/polyglot_design.pdf``):

   .. code-block:: text

      Node: Medication

      Properties:
      - name: String (e.g., "Warfarin")
      - generic_name: String (e.g., "warfarin sodium")
      - drug_class: String (e.g., "Anticoagulant")
      - dosage_forms: List<String> (e.g., ["tablet", "injectable"])
      - controlled_schedule: String or null

      Sample Nodes: Warfarin, Aspirin, Lisinopril, Metformin, Omeprazole
      Approximate Count: 15+ medications in graph

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

.. admonition:: Task 4.2: Graph Setup and Data (1 point)
   :class: task

   Create a Neo4j setup script with sample medical knowledge:

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

      // Drug interactions (CRITICAL)
      CREATE (warfarin)-[:INTERACTS_WITH {
        severity: 'major',
        description: 'Increased bleeding risk'
      }]->(aspirin)
      CREATE (aspirin)-[:INTERACTS_WITH {
        severity: 'major',
        description: 'Increased bleeding risk'
      }]->(warfarin)

      // Treatment relationships
      CREATE (hypertension)-[:TREATED_BY {
        evidence_level: 'A'
      }]->(lisinopril)

   **Minimum graph size** (reduced from original GP4):

   - **10+** medication nodes
   - **8+** disease nodes
   - **8+** symptom nodes (or equivalent fourth type)
   - **15+** INTERACTS_WITH relationships
   - **10+** TREATED_BY relationships
   - **8+** PRESENTS_WITH relationships
   - **5+**  CONTRAINDICATED_IN relationships

   .. note::

      Simplified or approximate medical data is acceptable. You do not
      need to verify every interaction against a clinical drug database
      -- use freely available references (e.g., RxNorm, Drugs.com
      interaction checker) for common medications and focus on building
      a graph large enough to demonstrate meaningful traversals.

   **Files to create**: ``neo4j/graph_setup.cypher`` and
   ``neo4j/graph_data.cypher``

.. admonition:: Task 4.3: Clinical Decision Support Queries (1 point)
   :class: task

   Write **at least 4 Cypher queries** (reduced from original 6+):

   **Required categories** (pick at least one from each):

   **(a) Drug Interaction Checking** (1 minimum):

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
      END;

   **(b) Patient Medication List Check** (1 minimum):

   .. code-block:: text

      // Check all pairwise interactions for a medication list
      MATCH (m1:Medication)-[i:INTERACTS_WITH]->(m2:Medication)
      WHERE m1.name IN ['Warfarin', 'Aspirin', 'Lisinopril',
                         'Metformin', 'Omeprazole']
        AND m2.name IN ['Warfarin', 'Aspirin', 'Lisinopril',
                         'Metformin', 'Omeprazole']
        AND m1 <> m2
      RETURN DISTINCT m1.name, m2.name, i.severity, i.description
      ORDER BY i.severity;

   **(c) Disease Pathway Analysis or Contraindication Check**
   (1 minimum):

   .. code-block:: text

      // Treatment options for Type 2 Diabetes with contraindications
      MATCH (d:Disease {name: 'Type 2 Diabetes'})
            -[:TREATED_BY]->(m:Medication)
      OPTIONAL MATCH (m)-[:CONTRAINDICATED_IN]->(contra:Disease)
      RETURN m.name, m.drug_class,
             COLLECT(contra.name) AS contraindications
      ORDER BY m.drug_class;

   **(d) Free Choice** (1+ minimum):

   Symptom differential diagnosis, medication alternatives, or any
   other clinically meaningful traversal.

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


Part 5: System Integration and Docker Deployment
-------------------------------------------------

**Objective**: Integrate all three databases in Python, add
cross-database CLI operations, and deploy the whole system with
Docker Compose.

.. admonition:: Task 5.1: Multi-Database Python Integration (2 points)
   :class: task

   **Extend your project structure**:

   .. code-block:: text

      healthcare-management/
      ├── config/
      │   ├── database.py      # Existing: PostgreSQL
      │   ├── mongodb.py       # New: MongoDB connection
      │   └── neo4j_config.py  # New: Neo4j connection
      ├── repositories/
      │   ├── postgres/        # Existing from GP2
      │   ├── mongodb/         # New
      │   │   ├── clinical_notes_repo.py
      │   │   └── imaging_repo.py
      │   └── neo4j/           # New
      │       └── knowledge_graph_repo.py
      ├── services/
      │   ├── clinical_service.py       # Existing, now cross-database
      │   └── prescription_safety.py    # New: uses Neo4j

   **Unified Clinical Record Service** (combines all three):

   .. code-block:: python

      class ClinicalRecordService:
          def get_complete_record(self, patient_id, user_id, user_role):
              """Build a complete patient record from all three
              databases."""
              # PostgreSQL: demographics, medications, labs
              patient = self.pg_patient_repo.find_by_id(
                  patient_id, user_id, user_role
              )
              medications = self.pg_prescription_repo.find_active(
                  patient_id
              )

              # MongoDB: clinical notes, care plans
              notes = self.mongo_notes_repo.find_by_patient(
                  patient_id, limit=10
              )

              # Neo4j: safety check across active medications
              med_names = [m.name for m in medications]
              interaction_alerts = self.neo4j_repo.check_interactions(
                  med_names
              )

              return {
                  "demographics": patient,
                  "active_medications": medications,
                  "clinical_notes": notes,
                  "safety_alerts": interaction_alerts,
              }

.. admonition:: Task 5.2: Unified CLI Operations (2 points)
   :class: task

   Add CLI menu options that demonstrate all three databases working
   together. You need **at least 2 unified operations**:

   **Operation 1: Complete Patient Record**

   - PostgreSQL: demographics, appointments, prescriptions, labs
   - MongoDB: recent clinical notes, care plans
   - Neo4j: drug-interaction check across active medications

   **Operation 2: Prescription Safety Check**

   - Validate patient and medication in PostgreSQL
   - Get patient's active medications from PostgreSQL
   - Check new medication against all active meds in Neo4j
   - If safe: insert prescription into PostgreSQL
   - If unsafe: display interaction warnings with severity and
     **do not** insert

   (A third example you can use: **Treatment Options for a Disease**
   -- Neo4j pathways + contraindication checking against the
   patient's conditions from PostgreSQL. Include it if you have time.)

   For each operation, document which databases are involved and why:

   .. code-block:: text

      Operation: Prescription Safety Check

      Description: Prevent unsafe prescriptions at order entry time.

      Databases Used:
      - PostgreSQL: patient record, active medication list, persistent
        prescription record
      - Neo4j: pairwise interaction lookup across active meds + new med
      - (MongoDB not required for this operation)

.. dropdown:: Example: Complete Patient Record Output
   :icon: terminal
   :class-container: sd-border-info

   Below is an example of what the **Complete Patient Record** unified
   operation might look like when all three databases are working
   together. Your exact output will differ, but this shows the
   expected level of detail.

   .. code-block:: text

      $ python -m cli.main

      ╔══════════════════════════════════════╗
      ║   Healthcare Management System       ║
      ╠══════════════════════════════════════╣
      ║  1. Patient CRUD                     ║
      ║  2. Appointment CRUD                 ║
      ║  3. Prescription CRUD                ║
      ║  4. Run SQL Queries                  ║
      ║  5. MongoDB Queries                  ║
      ║  6. Complete Patient Record          ║
      ║  7. Prescription Safety Check        ║
      ║  0. Exit                             ║
      ╚══════════════════════════════════════╝

      Select option: 6
      Enter patient MRN: 0000012345

      ══════════════════════════════════════════════════════════════
                COMPLETE PATIENT RECORD — MRN: 0000012345
      ══════════════════════════════════════════════════════════════

      ── PostgreSQL: Demographics & Medications ──────────────────
        Name:           Jane Doe
        DOB:            1968-03-15 (age 58)
        Insurance:      BlueCross PPO (ID: BC-9981234)
        Primary Provider: Dr. Sarah Chen (NPI: 1234567890)

        Active Medications (4):
          1. Lisinopril 10mg — daily — since 2025-08-01
          2. Metformin 500mg  — twice daily — since 2024-11-15
          3. Atorvastatin 20mg — at bedtime — since 2025-02-10
          4. Omeprazole 20mg — daily — since 2026-01-05

      ── MongoDB: Recent Clinical Notes ──────────────────────────
        Notes Found: 3 (last 6 months)

        2026-02-15 | progress_note | Dr. Chen
          Chief Complaint: Follow-up for hypertension management
          Assessment: Hypertension improving on current regimen
          Plan: Continue lisinopril 10mg, recheck in 3 months

        2026-02-18 | consultation | Dr. Patel (Cardiology)
          Reason: Evaluate cardiac murmur
          Findings: Grade II/VI systolic murmur, benign
          Recommendation: Echocardiogram in 6 months

        2025-12-10 | progress_note | Dr. Chen
          Chief Complaint: Diabetes management
          Assessment: HbA1c 7.2%, slightly above target
          Plan: Continue metformin, dietary counseling

      ── Neo4j: Drug Interaction Check ───────────────────────────
        Checking 4 active medications for interactions...

        ⚠ MODERATE: Lisinopril ↔ Metformin
          Risk of hypoglycemia; monitor blood glucose closely

        ✓ No other interactions found among active medications.

      ══════════════════════════════════════════════════════════════

.. dropdown:: Example: Prescription Safety Check Output
   :icon: terminal
   :class-container: sd-border-info

   Below is an example of what the **Prescription Safety Check**
   unified operation might look like — first a safe prescription,
   then an unsafe one. (Assumes the user selected option **7** from
   the main menu.)

   .. code-block:: text

      Select option: 7

      ══════════════════════════════════════════════════════════════
                    PRESCRIPTION SAFETY CHECK
      ══════════════════════════════════════════════════════════════

      Enter patient MRN: 0000012345
      Medication to prescribe: Amlodipine
      Dosage: 5mg daily

      ── PostgreSQL: Patient Lookup ──────────────────────────────
        ✓ Patient found: Jane Doe (MRN: 0000012345)
        Active medications: Lisinopril, Metformin, Atorvastatin,
                            Omeprazole

      ── Neo4j: Interaction Check ────────────────────────────────
        Checking Amlodipine against 4 active medications...

        ✓ Amlodipine ↔ Lisinopril     — no interaction
        ✓ Amlodipine ↔ Metformin      — no interaction
        ✓ Amlodipine ↔ Atorvastatin   — no interaction
        ✓ Amlodipine ↔ Omeprazole     — no interaction

        RESULT: SAFE — no interactions detected.

      ── PostgreSQL: Inserting Prescription ──────────────────────
        ✓ Prescription #3021 created
          Medication:  Amlodipine 5mg
          Frequency:   daily
          Prescriber:  Dr. Chen (NPI: 1234567890)
          Start Date:  2026-04-24

      ══════════════════════════════════════════════════════════════

   **Unsafe prescription example:**

   .. code-block:: text

      Enter patient MRN: 0000012345
      Medication to prescribe: Warfarin
      Dosage: 5mg daily

      ── PostgreSQL: Patient Lookup ──────────────────────────────
        ✓ Patient found: Jane Doe (MRN: 0000012345)
        Active medications: Lisinopril, Metformin, Atorvastatin,
                            Omeprazole, Amlodipine

      ── Neo4j: Interaction Check ────────────────────────────────
        Checking Warfarin against 5 active medications...

        ✗ MAJOR: Warfarin ↔ Omeprazole
          Omeprazole may increase Warfarin levels, raising
          bleeding risk. Consider alternative PPI or closer
          INR monitoring.

        ✗ MODERATE: Warfarin ↔ Atorvastatin
          Statins may potentiate anticoagulant effect.
          Monitor INR closely if co-prescribed.

        RESULT: UNSAFE — 2 interactions detected (1 major).
        ✗ Prescription NOT inserted.
        → Review interactions with prescribing physician.

      ══════════════════════════════════════════════════════════════

.. dropdown:: Docker Compose Primer
   :icon: info
   :class-container: sd-border-info
   :open:

   **What is Docker Compose?**

   Docker Compose is a tool for defining and running multi-container
   applications. Instead of running ``docker run ...`` for each service
   (one for PostgreSQL, one for MongoDB, one for Neo4j), you write a
   single ``docker-compose.yml`` file that declares:

   - Which **image** each service uses (e.g., ``postgres:14``)
   - What **ports** are exposed to the host (e.g., ``5432``,
     ``7474``, ``7687``)
   - What **volumes** persist data across container restarts
   - What **environment variables** each service needs
   - **Dependencies** between services (e.g., the app waits for the
     databases before starting)

   All services defined in the file share a Docker network and can
   reach each other by **service name** (e.g., your Python app
   connects to ``postgres:5432``, not ``localhost:5432``).

   **Everyday commands**:

   .. list-table::
      :widths: 45 55
      :header-rows: 1
      :class: compact-table

      * - **Command**
        - **What it does**
      * - ``docker-compose up --build``
        - Build the app image and start all services in the
          foreground. Stops on Ctrl+C.
      * - ``docker-compose up -d``
        - Start everything detached (background).
      * - ``docker-compose down``
        - Stop and remove all containers (keeps named volumes).
      * - ``docker-compose down -v``
        - Also remove named volumes (destroys persisted data).
      * - ``docker-compose logs -f <service>``
        - Tail logs for a specific service
          (``postgres``, ``mongodb``, ``neo4j``, or ``app``).
      * - ``docker-compose exec <service> <cmd>``
        - Run a command inside a running service
          (e.g., ``docker-compose exec postgres psql -U healthcare_admin``).
      * - ``docker-compose ps``
        - List the running services and their status.
      * - ``docker-compose restart <service>``
        - Restart one service without touching the others.

   **Why it matters for this project**

   A single command -- ``docker-compose up --build`` -- starts
   PostgreSQL, MongoDB, Neo4j, and your Python app together. That is
   how polyglot systems are typically deployed in production, and it
   is what I will use to run your submission. If your
   Compose file works, your three-database system is demonstrably
   reproducible on any machine with Docker installed.

   **Minimal file anatomy**

   .. code-block:: yaml

      version: '3.8'         # Compose file format version
      services:              # One block per service
        postgres:            # Service name (also the DNS name)
          image: postgres:14 # Image to pull / build
          ports:             # Host:container port mapping
            - "5432:5432"
          volumes:           # Named volume for persistence
            - postgres_data:/var/lib/postgresql/data
          environment:       # Env vars inside the container
            POSTGRES_PASSWORD: ${PG_PASSWORD}  # From .env file
      volumes:
        postgres_data:       # Named-volume declaration

   **Gotchas to plan for**

   - When the app runs inside Compose, it connects to **service names**
     (``postgres``, ``mongodb``, ``neo4j``), not ``localhost``. Your
     ``.env`` should reflect this; supply both values for local dev
     and in-compose use, or just use the service names.
   - ``depends_on`` only waits for containers to **start**, not for
     the database inside to be **ready** to accept connections. Your
     app should retry connecting on startup. Neo4j in particular can
     take 30-60 seconds to fully start.
   - Schema-loading files placed in
     ``./postgresql/:/docker-entrypoint-initdb.d`` run only on the
     **first** boot of an empty data volume. Run
     ``docker-compose down -v`` to re-seed.


.. admonition:: Task 5.3: Docker Compose Deployment (1 point)
   :class: task

   .. tip::

      **Do not write the compose file from scratch.** Start from the
      skeleton provided on the
      :doc:`Docker Compose Starter <scenario2_docker_starter>` page,
      which gives you all four services (``postgres``, ``mongodb``,
      ``neo4j``, ``app``) plus ``mongo-seed`` and ``neo4j-seed``
      sidecars, with healthchecks and ``service_healthy`` dependencies
      already wired up (including Neo4j's long first-boot handled by a
      ``start_period``). Adapt it to your project rather than
      reinventing it -- the grading target is a working three-database
      system.

   For reference, a minimal structure looks like the following (the
   starter is a superset of this):

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


Part 6: Final Technical Report
-------------------------------

**Objective**: Write a technical report documenting the complete
system. **No strict page limit** -- be thorough but concise. Submit
as PDF.

.. admonition:: Task 6.1: Report Outline (8 points)
   :class: task

   Your report must include **all of the following sections**:

   **1. Executive Summary**

   System overview, three-database architecture, and key achievements
   (polyglot architecture, drug safety).

   **2. Data Partitioning Rationale**

   Why each data type lives in its chosen database. Trade-offs
   between consistency, flexibility, and query power. Cross-database
   referencing strategy.

   **3. Architecture Overview**

   System architecture diagram, data flow diagrams for clinical
   workflows, and component descriptions for each database layer.

   **4. Database Design Decisions**

   For each database (PostgreSQL, MongoDB, Neo4j): what data it
   holds, why that database was chosen over the alternatives,
   schema/structure highlights, and key design decisions.

   **5. Clinical Decision Support Design**

   Medical knowledge graph structure, drug-interaction checking
   workflow, and how the prescription safety check works
   end-to-end.

   **6. Lessons Learned**

   What worked well, challenges faced, what you would do differently.

   **7. Team Contributions**

   Each member's name, tasks completed, and contribution percentage
   (sum to 100%).

   **File to create**: ``docs/technical_report.pdf``


Folder Structure
----------------

.. code-block:: text

   GP3_Healthcare_Team{X}/
   ├── postgresql/                 # From GP2
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── mongodb/
   │   ├── mongo_setup.js
   │   ├── mongo_data.js
   │   └── mongo_queries.js
   ├── neo4j/
   │   ├── graph_setup.cypher
   │   ├── graph_data.cypher
   │   └── cypher_queries.cypher
   ├── config/
   │   ├── database.py             # Existing from GP2
   │   ├── mongodb.py              # New
   │   └── neo4j_config.py         # New
   ├── models/                       # Existing from GP2
   │   └── [entity].py
   ├── repositories/
   │   ├── postgres/               # Existing from GP2
   │   ├── mongodb/
   │   └── neo4j/
   ├── services/
   │   ├── clinical_service.py     # Existing, now cross-database
   │   └── prescription_safety.py  # New: uses Neo4j
   ├── cli/
   │   └── main.py                 # Updated with 2+ unified operations
   ├── docs/
   │   ├── polyglot_design.pdf      # Partitioning, MongoDB schemas,
   │   │                           # Neo4j node/rel catalog, indexes
   │   └── technical_report.pdf
   ├── docker-compose.yml
   ├── Dockerfile
   ├── requirements.txt
   ├── .env.example              # template with placeholder values
   ├── .env                      # actual values (committed for
   │                             # grading -- see policy below)
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **docs/polyglot_design.pdf**

   The main design document. **Submit as PDF** (you may author in
   Word, Google Docs, Markdown, LaTeX -- whatever you prefer --
   then export to PDF at submission time; do not submit a raw
   ``.md`` or ``.docx``). It should contain four sections:
   (1) data partitioning analysis across PostgreSQL, MongoDB, and
   Neo4j with clinical justifications for each data type;
   (2) MongoDB collection schemas with document structures,
   embedding rationale, and expected volumes;
   (3) Index strategy for MongoDB;
   (4) Neo4j node and relationship catalog (node properties, sample
   nodes, counts, relationship direction, properties, examples).

   **docs/technical_report.pdf**

   The final report (see Part 6 for required sections).

   **requirements.txt**

   Updated from GP2 to include ``pymongo`` and ``neo4j`` (Python
   driver).

   **.env.example** (template, no real values)

   Updated to include MongoDB and Neo4j connection variables. Use
   obvious placeholders so it is clear this file is a template:

   .. code-block:: text

      # --- PostgreSQL ---
      DB_HOST=localhost            # use "postgres" inside Docker Compose
      DB_PORT=5432
      DB_NAME=healthcare_management
      DB_USER=healthcare_admin
      DB_PASSWORD=<fill-in-your-password>

      # --- MongoDB ---
      MONGO_HOST=localhost         # use "mongodb" inside Docker Compose
      MONGO_PORT=27017
      MONGO_DB=healthcare_management

      # --- Neo4j ---
      NEO4J_URI=bolt://localhost:7687   # use "bolt://neo4j:7687" inside Docker Compose
      NEO4J_USER=neo4j
      NEO4J_PASSWORD=<fill-in-your-password>

   .. note::

      When your app runs **inside Docker Compose**, it must connect to
      the service names (``postgres``, ``mongodb``, ``neo4j``) instead
      of ``localhost``. The provided
      :doc:`Docker Compose Starter <scenario2_docker_starter>` already
      sets the correct values in the ``app`` service's ``environment:``
      block, so the ``.env`` values above are only used for **local
      development** outside of Docker.

   **.env** (actual values used by your system -- see the
   "Credentials for Grading" section below for the policy and
   recommended defaults)

   **README.md**

   Updated from GP2. Add:

   - MongoDB and Neo4j prerequisites.
   - Docker quick-start instructions
     (``docker-compose up --build``).
   - An architecture summary table showing which database holds
     which data.
   - A description of key safety features (drug-interaction
     checking) and the unified CLI operations.

   **team_contributions.md**

   List each team member's name, tasks completed, hours contributed,
   and contribution percentage. Percentages must sum to 100%.


Credentials for Grading
-----------------------

You need passwords to run the databases locally and inside Docker
Compose. Because I have to run your submission, you must
share the passwords you used. **The policy for this assignment is:**

1. Commit **both** ``.env.example`` (template with placeholders) and
   ``.env`` (actual values you used) in your submission.
2. The ``.env`` file must contain the exact values your
   ``docker-compose.yml`` and application read at runtime, so that
   ``docker-compose up --build`` works for me with zero
   manual edits.

.. warning::

   In a real project, ``.env`` **must be in ``.gitignore``** --
   committing secrets to a repository is a security anti-pattern.
   For this course we explicitly override that practice so
   I can run your system reproducibly. Treat every value in
   your ``.env`` as disposable and **do not reuse any password that
   protects a real account, service, or personal project**.

**Recommended class-wide defaults** (use these unless you have a
specific reason not to -- fewer variations make grading faster).
Neo4j requires passwords of **at least 8 characters**. These are
the values the
:doc:`Docker Compose Starter <scenario2_docker_starter>` uses by
default:

.. code-block:: text

   PG_USER=healthcare_admin
   PG_PASSWORD=enpm818t
   PG_DB=healthcare_management
   MONGO_DB=healthcare_management
   NEO4J_PASSWORD=enpm818t-neo4j

If you use different values, your ``README.md`` must list them in
a short "Credentials" section so I can verify them at a
glance.


Submission
----------

.. important::

   **Two things to submit:**

   1. **Canvas**: Upload **one** ZIP file named
      ``GP3_Healthcare_Team{X}.zip`` (replace ``{X}`` with your
      team number, e.g., ``GP3_Healthcare_Team03.zip``). The ZIP
      must contain the complete folder structure shown above.

   2. **GitHub**: Paste your team's **GitHub repository link** in
      the Canvas submission comments. The repository must be
      **private** with me (``zeidk``) added as a
      **collaborator**. The repository should contain the same
      code as the ZIP.

   **Due**: Monday **05/12/2026** at 11:59 PM.

   .. warning::

      Any commits pushed to the GitHub repository **after the
      deadline** will result in a **5-point deduction**.
      I will check the commit history.


.. admonition:: Submission Checklist
   :class: tip

   **Design Document**:

   - [ ] ``polyglot_design.pdf`` covers partitioning, MongoDB schemas,
     indexes, and Neo4j node/relationship catalog
   - [ ] Each data type has a clear PostgreSQL / MongoDB / Neo4j
     justification
   - [ ] 4+ MongoDB collections documented with embedding rationale
   - [ ] 4+ Neo4j node types and 4+ relationship types documented

   **MongoDB Files**:

   - [ ] ``mongo_setup.js`` creates all collections with validation
     and indexes
   - [ ] ``mongo_data.js`` loads realistic clinical document data
     (runs without errors)
   - [ ] ``mongo_queries.js`` contains 6+ queries with documentation

   **Neo4j Files**:

   - [ ] ``graph_setup.cypher`` creates 4+ node types with properties
   - [ ] ``graph_data.cypher`` populates minimum graph (10+
     medications, 8+ diseases, 8+ symptoms, 15+ INTERACTS_WITH,
     10+ TREATED_BY, 8+ PRESENTS_WITH, 5+ CONTRAINDICATED_IN)
   - [ ] ``cypher_queries.cypher`` contains 4+ clinical decision
     support queries
   - [ ] Drug-interaction checking works for a list of medications

   **Python Application**:

   - [ ] MongoDB and Neo4j connections configured
   - [ ] Repository classes for each database
   - [ ] 2+ unified CLI operations using all three databases
   - [ ] Prescription safety check works end-to-end

   **Deployment**:

   - [ ] ``docker-compose.yml`` starts all services (PostgreSQL,
     MongoDB, Neo4j, app)
   - [ ] ``Dockerfile`` builds the application correctly
   - [ ] ``docker-compose up --build`` results in a working system

   **Final Report**:

   - [ ] PDF with all seven required sections (Exec Summary, Data
     Partitioning, Architecture, Database Design, Clinical Decision
     Support, Lessons Learned, Team Contributions)
   - [ ] Architecture diagram included
   - [ ] All three databases discussed with rationale

   **Supporting Files**:

   - [ ] ``README.md`` updated with Docker quick-start instructions
     (and a Credentials section if non-default values are used)
   - [ ] ``requirements.txt`` updated with ``pymongo`` and ``neo4j``
   - [ ] ``.env.example`` updated with MongoDB and Neo4j variables
     (placeholders only)
   - [ ] ``.env`` committed with the **actual** values used (policy:
     see "Credentials for Grading")
   - [ ] ``team_contributions.md`` (percentages sum to 100%)


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 38 10 52
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Data Partitioning**
     - 2
     - Clear clinical rationale for each data type across PostgreSQL,
       MongoDB, and Neo4j; documented decision framework
   * - **Part 2: MongoDB Schema + Indexes**
     - 3
     - 4+ collections with complete schemas and embedding rationale
       (2 pts); appropriate indexes with justification (1 pt)
   * - **Part 3: MongoDB Setup + Queries**
     - 3
     - Setup with validation and realistic data (1 pt); 6+ queries
       covering all categories with correct results (2 pts)
   * - **Part 4: Neo4j Graph + Queries**
     - 4
     - 4+ node types and 4+ relationship types with clinical relevance
       (2 pts); minimum graph populated (1 pt); 4+ clinical decision
       support queries (1 pt)
   * - **Part 5: Integration + Docker**
     - 5
     - Multi-database Python integration (2 pts); 2+ unified CLI
       operations using all three databases, including a working
       prescription safety check (2 pts); working Docker Compose
       (1 pt)
   * - **Part 6: Technical Report**
     - 8
     - All seven required sections (3 pts); architecture well-diagrammed
       and justified (2 pts); database design decisions and clinical
       decision support clearly explained (2 pts); lessons learned
       and professional quality (1 pt)
   * - **Total**
     - **25**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Treating MongoDB like SQL (use embedding for related clinical
     data, not separate collections for everything)
   - Same note structure for all types (progress notes, consults,
     and discharge summaries have different fields)
   - Missing text indexes (clinical narrative search requires text
     indexes)
   - Trivial graph (only a handful of medications and diseases does
     not demonstrate clinical value)
   - No bidirectional interactions (drug interactions go both ways;
     create both directions)
   - Prescription operation without safety check (the whole point of
     Neo4j is preventing unsafe prescriptions)
   - Docker volumes not configured (data lost on container restart)
   - Hardcoded connection strings (use environment variables)
   - Missing data-partitioning section in the report (document why
     each database holds its data)


Tips for Success
----------------

.. tip::

   - **Think like a clinician**. A doctor viewing a patient record
     wants notes, labs, medications, care plans, and safety alerts
     together. Design your cross-database service to support this
     workflow.
   - **Embrace document diversity**. The whole point of MongoDB here
     is that different clinical notes have different structures.
     Lean into this.
   - **Build a meaningful graph**. Use real medication names, real
     ICD-10 codes, and real drug interactions. RxNorm and interaction
     databases are freely available for reference.
   - **Test the safety flow end-to-end**. Write test cases like
     "What happens when I prescribe Warfarin to a patient already on
     Aspirin?" The answer should be a major interaction warning.
   - **Test with Docker early**. Do not wait until the last day to
     containerize. Build and test Docker Compose incrementally.
   - **Write the report throughout**. Capture architecture decisions
     and screenshots as you build.
   - **Use office hours**. Bring schema designs, Docker issues, and
     graph/Cypher questions for review.


Final Project Summary
---------------------

.. admonition:: Cumulative Achievement
   :class: note

   **Points**:

   - GP1: Relational Design = 10 points
   - GP2: PostgreSQL + Python = 15 points
   - GP3: Complete Polyglot System = 25 points
   - **Total**: 50 points

**Your Achievement**:

You have built a production-grade secure polyglot healthcare system
demonstrating relational database design, clinical document
management with flexible schemas, a medical knowledge graph for
clinical decision support, drug-interaction checking for patient
safety, cross-database integration for unified patient records,
Docker deployment, and professional technical documentation.
