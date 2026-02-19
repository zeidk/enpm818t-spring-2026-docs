===========================================================
Group Project 3: MongoDB Document Database Integration
===========================================================

Overview
--------

Add MongoDB to handle semi-structured clinical documents and healthcare data with flexible schemas. Integrate with your PostgreSQL system to create a polyglot persistence architecture for unified patient records.

**Timeline**: 3 weeks

**Weight**: 10 points (25% of final project)

**Team Size**: 4 students

**Builds on**: Your HIPAA-compliant PostgreSQL system from GP2


.. important::
   
   **What You'll Deliver**
   
   This project requires a **complete MongoDB integration** with your existing PostgreSQL system:
   
   - 3 MongoDB files (setup script, data script, queries)
   - 3 documentation files (polyglot design, schema docs, integration strategy)
   - 1 updated Python application (MongoDB repositories + cross-database clinical services)
   - 1 README file
   - 1 team contributions file
   
   **Submission**: Single ZIP file named ``GP3_Healthcare_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Recognize when document databases are appropriate for clinical data
- Design flexible document schemas for clinical documentation
- Choose embedding vs. referencing for healthcare data
- Write MongoDB aggregation pipelines for clinical analytics
- Implement text search on clinical narratives
- Integrate multiple databases for unified patient records
- Handle cross-database queries with HIPAA compliance


Part 1: Polyglot Persistence Design
------------------------------------

**Objective**: Analyze your clinical data and decide what belongs in PostgreSQL vs. MongoDB.

.. dropdown:: 📋 Task 1.1: Data Partitioning Analysis (2 points)
   :class-container: sd-border-primary
   :open:

   For each data type, answer:
   
   1. **Structure**: Fixed schema or variable by clinical context?
   2. **Consistency**: Strong ACID or eventual OK?
   3. **Relationships**: Many foreign keys or self-contained documents?
   4. **Query Pattern**: Complex JOINs or hierarchical document access?
   5. **Volume**: Moderate or high write throughput?
   6. **Evolution**: Schema stable or changes with clinical practice?
   
   **Decision Template**:
   
   .. code-block:: text
   
      Data Type: Clinical Notes
      
      Analysis:
      1. Structure: Variable (progress notes, consult reports,
         discharge summaries all have different fields)
      2. Consistency: Eventual OK (notes are append-only, rarely edited)
      3. Relationships: Minimal (references patient_id and provider_id only)
      4. Query Pattern: Document retrieval by patient, text search
      5. Volume: Moderate (10-50 notes per patient per year)
      6. Evolution: High (new note templates added frequently)
      
      Decision: MongoDB
      Justification: Variable structure per note type, text search needed,
                     minimal relational needs, schema evolves with practice
   
   **Keep in PostgreSQL**:
   
   - Patient demographics (structured, ACID transactions, PHI)
   - Appointments and scheduling (complex relationships)
   - Prescriptions and medications (strong consistency required)
   - Insurance claims and billing (financial accuracy, ACID)
   - Audit logs (tamper-proof, regulated retention)
   
   **Move to MongoDB**:
   
   - **Clinical notes** (variable structure by note type)
   - **Medical imaging metadata** (DICOM headers vary by modality)
   - **Care plans** (nested protocols, goals, interventions)
   - **Patient surveys** (different question sets: PHQ-9, GAD-7, pain scales)
   - **Adverse events** (embedded investigation details)
   - **Telemedicine sessions** (session logs, transcripts)
   - **Research consents** (versioned consent forms)
   - **Patient preferences** (advanced directives, communication preferences)
   
   **File to create**: ``docs/polyglot_design.md``


Part 2: MongoDB Schema Design
------------------------------

**Objective**: Design document schemas for at least 8 clinical collections with appropriate indexes.

.. dropdown:: 📋 Task 2.1: Required Collections (2 points)
   :class-container: sd-border-primary
   :open:

   Design **at least 8 collections**:
   
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
        "history_present_illness": "Patient returns for 3-month...",
        "review_of_systems": {
          "cardiovascular": "No chest pain, no palpitations",
          "respiratory": "No shortness of breath",
          "neurological": "No headaches, no dizziness"
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
        "addendums": [
          {"date": ISODate(...), "author_id": 789, "text": "..."}
        ],
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
          "slice_thickness": 1.25,
          "contrast_agent": "Omnipaque 350"
        },
        "radiologist_report": {
          "provider_id": 321,
          "findings": "No pulmonary embolism...",
          "impression": "Normal CT chest",
          "critical_finding": false,
          "report_date": ISODate("2026-02-10T14:22:00Z")
        }
      }
   
   **3. care_plans**
   
   Nested treatment protocols with goals and interventions.
   
   **4. patient_surveys**
   
   Different question sets by survey type (PHQ-9, GAD-7, pain scales).
   
   **5. adverse_events**
   
   Incident reports with embedded investigation details.
   
   **6. telemedicine_sessions**
   
   Virtual visit records with session logs.
   
   **7. research_consents**
   
   Clinical trial participation with versioned consent forms.
   
   **8. patient_preferences**
   
   Advanced directives and communication preferences.
   
   **File to create**: ``docs/mongodb_schema.md``

.. dropdown:: 📋 Embedding vs. Referencing
   :class-container: sd-border-primary

   **Decision Tree**:
   
   .. code-block:: text
   
      Is clinical data queried together?
      ├── YES: Consider embedding
      │   └── Will embedding cause unbounded growth?
      │       ├── YES: Use referencing
      │       └── NO: Embed
      └── NO: Use referencing
   
   **Healthcare Examples**:
   
   - Embed: Vital signs within clinical note (always queried together, bounded)
   - Embed: Addendums within clinical note (queried together, bounded to ~5)
   - Do not embed: All clinical notes within patient doc (unbounded growth)
   - Reference: patient_id and provider_id to PostgreSQL (different databases)
   - Embed: Survey responses within survey document (always read together)

.. dropdown:: 📋 Task 2.2: Index Strategy (1 point)
   :class-container: sd-border-primary

   **Compound Indexes**: (patient_id, encounter_date) for patient timeline queries
   
   **Text Indexes**: Full-text search on clinical narratives
   
   .. code-block:: javascript
   
      db.clinical_notes.createIndex({
        "chief_complaint": "text",
        "history_present_illness": "text",
        "assessment": "text",
        "plan": "text"
      });
   
   **TTL Indexes**: Auto-delete telemedicine session logs after retention period
   
   **Partial Indexes**: Unsigned notes only (for provider review workflow)


Part 3: MongoDB Implementation
-------------------------------

**Objective**: Set up MongoDB collections and write clinical queries.

.. dropdown:: 📋 Task 3.1: Database Setup (1 point)
   :class-container: sd-border-primary
   :open:

   Create ``mongo_setup.js`` with collection creation and validation:
   
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
                       "discharge_summary", "procedure_note",
                       "operative_note"]
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
   
   **File to create**: ``mongodb/mongo_setup.js``

.. dropdown:: 📋 Task 3.2: Sample Data (integrated into score)
   :class-container: sd-border-primary

   Generate realistic clinical document data:
   
   - 500+ clinical notes across multiple note types
   - 100+ imaging metadata records (CT, MRI, X-ray)
   - 50+ care plans with nested goals and interventions
   - 200+ patient surveys (PHQ-9, GAD-7, pain scales)
   - 30+ adverse event reports
   - 100+ telemedicine session records
   - 50+ research consent documents
   - 100+ patient preference records
   
   **File to create**: ``mongodb/mongo_data.js``

.. dropdown:: 📋 Task 3.3: Query Development (2 points)
   :class-container: sd-border-primary

   Write **at least 8 MongoDB queries**:
   
   **Aggregation Pipelines** (3 queries minimum):
   
   - Clinical documentation volume by provider and note type
   - Patient survey scoring and trend analysis (e.g., PHQ-9 depression screening)
   - Adverse event reporting and investigation status
   
   **Text Search** (2 queries minimum):
   
   - Search clinical notes for specific diagnoses or symptoms
   - Full-text search with relevance scoring across note fields
   
   **Array Operations** (3 queries minimum):
   
   - Care plan progress tracking ($unwind goals array)
   - Multi-response survey analysis
   - Addendum and amendment tracking in clinical notes
   
   **Query Documentation Format**:
   
   .. code-block:: javascript
   
      // Query #X: [Title]
      // Clinical Context: [Why this matters for patient care]
      // Collections Used: [List collections]
      // Pipeline Stages: [e.g., $match, $group, $sort]
      // HIPAA Note: [What PHI is accessed]
      
      [YOUR MONGODB QUERY]
      
      // Expected Output: [Description of result shape]
      // Sample Results: [First 2-3 documents]
   
   **File to create**: ``mongodb/mongo_queries.js``


Part 4: Python Integration
---------------------------

**Objective**: Extend your GP2 Python application with MongoDB support and cross-database clinical services.

.. dropdown:: 📋 Task 4.1: Cross-Database Integration (2 points)
   :class-container: sd-border-primary
   :open:

   **Extend Project Structure**:
   
   .. code-block:: text
   
      healthcare-management/
      ├── config/
      │   ├── database.py      # Updated: PostgreSQL + MongoDB
      │   └── mongodb.py       # New: MongoDB-specific config
      ├── repositories/
      │   ├── postgres/        # Existing from GP2
      │   └── mongodb/         # New: MongoDB repositories
      │       ├── clinical_notes_repo.py
      │       ├── care_plans_repo.py
      │       └── surveys_repo.py
      ├── services/
      │   ├── audit_service.py    # Updated: Audit MongoDB access too
      │   └── clinical_service.py # New: Cross-database clinical records
   
   **Unified Clinical Record Service**:
   
   .. code-block:: python
   
      class ClinicalRecordService:
          def get_complete_record(self, patient_id, user_id,
                                 user_role, access_reason):
              """Build complete patient record from both databases."""
              # PostgreSQL: Demographics, medications, labs
              patient = self.pg_patient_repo.find_by_id(
                  patient_id, user_id, user_role, access_reason
              )
              medications = self.pg_prescription_repo.find_active(
                  patient_id
              )
              recent_labs = self.pg_lab_repo.find_recent(
                  patient_id, days=90
              )
              
              # MongoDB: Clinical notes, care plans, surveys
              notes = self.mongo_notes_repo.find_by_patient(
                  patient_id, limit=10
              )
              care_plan = self.mongo_care_repo.find_active(
                  patient_id
              )
              
              # Audit the cross-database access
              self.audit.log_access(
                  user_id, user_role, "COMPLETE_RECORD",
                  "cross_database", patient_id,
                  True, access_reason, True
              )
              
              return {
                  "demographics": patient,
                  "active_medications": medications,
                  "recent_labs": recent_labs,
                  "clinical_notes": notes,
                  "active_care_plan": care_plan
              }
   
   **New API Endpoints** (at least 4):
   
   - ``GET /patients/{id}/clinical-notes`` - Patient's clinical notes from MongoDB
   - ``GET /patients/{id}/complete-record`` - Cross-database unified record
   - ``GET /analytics/documentation-volume`` - Aggregation pipeline results
   - ``POST /clinical-notes`` - Create new clinical note in MongoDB


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP3_Healthcare_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP3_Healthcare_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP3_Healthcare_Team{X}/
   ├── mongodb/
   │   ├── mongo_setup.js
   │   ├── mongo_data.js
   │   └── mongo_queries.js
   ├── src/
   │   ├── config/
   │   │   ├── database.py
   │   │   └── mongodb.py
   │   ├── repositories/
   │   │   ├── postgres/
   │   │   └── mongodb/
   │   │       ├── clinical_notes_repo.py
   │   │       ├── care_plans_repo.py
   │   │       └── surveys_repo.py
   │   └── services/
   │       ├── audit_service.py
   │       └── clinical_service.py
   ├── tests/
   │   ├── test_mongo_repos.py
   │   └── test_cross_db.py
   ├── docs/
   │   ├── polyglot_design.md
   │   ├── mongodb_schema.md
   │   └── integration_strategy.md
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Part 1: Polyglot Persistence Design
   :class-container: sd-border-info

   **Documentation** (1 file):
   
   - ``docs/polyglot_design.md`` - Data partitioning analysis with clinical justifications

.. dropdown:: 📄 Part 2: MongoDB Schema Design
   :class-container: sd-border-info

   **Documentation** (1 file):
   
   - ``docs/mongodb_schema.md`` - Schema specs for 8+ collections with embedding rationale and index strategy

.. dropdown:: 📄 Part 3: MongoDB Implementation
   :class-container: sd-border-info

   **MongoDB Files** (3 files):
   
   - ``mongodb/mongo_setup.js`` - Collection creation with validation and indexes
   - ``mongodb/mongo_data.js`` - Sample clinical document data
   - ``mongodb/mongo_queries.js`` - 8+ documented queries

.. dropdown:: 📄 Part 4: Python Integration + Supporting Files
   :class-container: sd-border-info

   **Application** (updated src/ directory):
   
   - ``src/config/mongodb.py`` - MongoDB connection configuration
   - ``src/repositories/mongodb/*.py`` - MongoDB repository classes
   - ``src/services/clinical_service.py`` - Cross-database clinical records
   
   **Documentation** (1 file):
   
   - ``docs/integration_strategy.md`` - How PostgreSQL and MongoDB work together
   
   **Supporting Files** (2 files):
   
   - ``README.md`` - Updated project overview with MongoDB setup
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP3: Healthcare Patient Management - MongoDB Integration
   
   **Team Number**: [Your team number]
   
   **Scenario**: Healthcare Patient Management Platform
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Data Partitioning Summary
   
   | Data Type | Database | Rationale |
   |-----------|----------|-----------|
   | Patient demographics | PostgreSQL | Structured, ACID, PHI |
   | Clinical notes | MongoDB | Variable structure by type |
   | Care plans | MongoDB | Nested protocols and goals |
   | [Continue for all] | | |
   
   ## MongoDB Collections Summary
   
   | Collection | Document Count | Key Indexes |
   |------------|---------------|-------------|
   | clinical_notes | 500+ | (patient_id, date), text |
   | care_plans | 50+ | (patient_id), partial |
   | [Continue for all] | | |
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP3
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Wrote data partitioning analysis
   - Designed clinical_notes and medical_images schemas
   - Created mongo_setup.js with validation
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Designed care_plans, patient_surveys, adverse_events collections
   - Generated sample data (mongo_data.js)
   - Wrote aggregation pipeline queries
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Built MongoDB repository classes in Python
   - Implemented cross-database ClinicalRecordService
   - Wrote integration tests
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Wrote text search and array operation queries
   - Created new API endpoints for clinical documents
   - Wrote documentation (schema, integration strategy, README)
   
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

   **Design Documents** (3 files):
   
   - [ ] Polyglot design with clinical justification for each data type
   - [ ] MongoDB schema documentation for 8+ collections
   - [ ] Integration strategy describing cross-database clinical workflows
   
   **MongoDB Files** (3 files):
   
   - [ ] mongo_setup.js creates all collections with validation
   - [ ] mongo_setup.js creates all required indexes (compound, text, TTL)
   - [ ] mongo_data.js loads realistic clinical document data
   - [ ] mongo_queries.js contains 8+ documented queries
   
   **Python Application**:
   
   - [ ] MongoDB connection configured (pymongo)
   - [ ] Repository classes for clinical document collections
   - [ ] Cross-database ClinicalRecordService working
   - [ ] New API endpoints for clinical documents
   - [ ] Audit logging covers MongoDB access
   
   **Quality Checks**:
   
   - [ ] mongo_setup.js runs without errors
   - [ ] All 8+ queries execute successfully
   - [ ] Complete record endpoint returns data from both databases
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP3_Healthcare_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Treating MongoDB like SQL** - Use embedding for related clinical data, not separate collections for everything
   
   ❌ **No schema validation** - MongoDB is flexible, not lawless. Validate required clinical fields
   
   ❌ **Same note structure for all types** - Progress notes, consults, and discharge summaries have different fields
   
   ❌ **Missing text indexes** - Clinical narrative search requires text indexes
   
   ❌ **Forgetting audit logging** - MongoDB access to patient data must also be audited
   
   ❌ **Unrealistic data** - Only 10 clinical notes does not demonstrate the value of MongoDB
   
   ❌ **No cross-database service** - The unified patient record is the key deliverable
   
   ❌ **No embedding rationale** - Document every embed vs. reference decision


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: Data Partitioning**
     - 2
     - Clear clinical rationale for each data type (1pt); Documented decision framework (1pt)
   * - **Part 2: Schema Design**
     - 2
     - 8+ collections with complete specs (1pt); Appropriate embedding/referencing with rationale (1pt)
   * - **Part 2: Index Strategy**
     - 1
     - Appropriate indexes for clinical query patterns with justification
   * - **Part 3: Setup and Data**
     - 1
     - Collections with validation (0.5pt); Realistic clinical data (0.5pt)
   * - **Part 3: MongoDB Queries**
     - 2
     - 8+ queries covering all categories (1pt); Correct results with documentation (1pt)
   * - **Part 4: Python Integration**
     - 2
     - Clean MongoDB repositories (1pt); Working cross-database clinical services (1pt)
   * - **Total**
     - **10**
     - 


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP3**
   
   - **Think like a clinician** - A doctor viewing a patient record wants to see notes, labs, medications, and care plans together. Design your cross-database service to support this workflow.
   - **Embrace document diversity** - The whole point of MongoDB here is that different clinical notes have different structures. Lean into this.
   - **Test aggregation pipelines incrementally** - Build one stage at a time in mongosh. Verify results before adding the next stage.
   - **Use realistic clinical vocabulary** - Reference real ICD-10 codes, real medication names, and realistic clinical narratives in your sample data.
   - **Audit everything** - Even MongoDB access to patient-linked data must be logged for HIPAA compliance.
   - **Use office hours** - Bring your schema designs for review. Discuss clinical document modeling with instructors.


Next Steps
----------

After completing GP3, you will:

- Receive feedback from instructors
- Analyze which clinical decisions need medical knowledge support
- Begin GP4: Adding Neo4j for drug interaction checking and clinical decision support
- Deploy the full three-database system with Docker Compose

.. note::
   
   **Your GP3 integration creates the clinical document layer** for the complete system. GP4 (Neo4j + deployment + final report) adds medical knowledge and safety checking.
   
   Start thinking: What medical relationships matter most? How would you model drug interactions? What clinical decisions need graph-based support?