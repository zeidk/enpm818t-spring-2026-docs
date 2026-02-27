===========================================================
Group Project 3: MongoDB Document Database Integration
===========================================================

Overview
--------

Add MongoDB to handle semi-structured clinical documents and healthcare data with flexible schemas. Integrate with your PostgreSQL system to create a polyglot persistence architecture for unified patient records.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 2 weeks |
   **Weight**: 10 points (20% of final project) |
   **Team Size**: 4 students

**Builds on**: Your secure PostgreSQL system from GP2


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Recognize when document databases are appropriate for clinical data
- Design flexible document schemas for clinical documentation
- Choose embedding vs. referencing for healthcare data
- Write MongoDB aggregation pipelines for clinical analytics
- Implement text search on clinical narratives
- Integrate multiple databases for unified patient records


Part 1: Polyglot Persistence Design
------------------------------------

**Objective**: Analyze your clinical data and decide what belongs in PostgreSQL vs. MongoDB.

.. dropdown:: Task 1.1: Data Partitioning Analysis (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   For each data type, evaluate whether it belongs in PostgreSQL or MongoDB. Consider these factors:

   1. **Structure**: Fixed schema or variable by clinical context?
   2. **Consistency**: Strong ACID needed or eventual consistency OK?
   3. **Relationships**: Many foreign keys or self-contained documents?
   4. **Query Pattern**: Complex JOINs or hierarchical document access?
   5. **Volume**: Moderate or high write throughput?
   6. **Evolution**: Schema stable or changes with clinical practice?

   **Decision Template** (use for each data type):

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
      Justification: Variable structure per note type, text search needed,
                     minimal relational needs, schema evolves with practice

   **Keep in PostgreSQL** (from GP2):

   - Patient demographics (structured, ACID transactions, access-controlled)
   - Appointments and scheduling (complex relationships)
   - Prescriptions and medications (strong consistency required)
   - Insurance claims and billing (financial accuracy, ACID)

   **Move to MongoDB** (new in GP3):

   - **Clinical notes**: variable structure by note type (progress, consult, discharge)
   - **Medical imaging metadata**: DICOM headers vary by modality (CT, MRI, X-ray)
   - **Care plans**: nested protocols, goals, and interventions
   - **Patient surveys**: different question sets by survey type (PHQ-9, GAD-7, pain scales)

   **Document your decisions and rationale** in ``docs/polyglot_design.md``. This file should also include your collection schemas (see Part 2) and index strategy.

   **File to create**: ``docs/polyglot_design.md``


Part 2: MongoDB Schema Design
------------------------------

**Objective**: Design document schemas for at least 4 collections with appropriate indexes.

.. dropdown:: Task 2.1: Required Collections (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Design **at least 4 collections**. We show two detailed examples below; design at least two more of your own.

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

   **3-4. Your additional collections**: Choose from care_plans, patient_surveys, adverse_events, telemedicine_sessions, or others that make sense for your system.

   **Schema Documentation Format** (include in ``docs/polyglot_design.md``):

   .. code-block:: text

      Collection: clinical_notes

      Purpose: Store clinical documentation with variable structure by note type

      Document Structure:
      - _id: ObjectId (auto-generated)
      - patient_id: Integer (references PostgreSQL)
      - provider_id: Integer (references PostgreSQL)
      - encounter_date: ISODate
      - note_type: String (enum: progress_note, consultation, discharge_summary)
      - [remaining fields vary by note_type]

      Embedding Rationale: Vital signs embedded within physical_exam because
        they are always queried with the parent note and are bounded.

.. dropdown:: Embedding vs. Referencing
   :icon: gear
   :class-container: sd-border-primary

   **Decision Tree**:

   .. code-block:: text

      Is clinical data queried together?
      |-- YES: Consider embedding
      |   |-- Will embedding cause unbounded growth?
      |       |-- YES: Use referencing
      |       |-- NO: Embed
      |-- NO: Use referencing

   **Healthcare Examples**:

   - Embed: Vital signs within clinical note (always queried together, bounded)
   - Embed: Survey responses within survey document (always read together)
   - Do not embed: All clinical notes within patient doc (unbounded growth)
   - Reference: patient_id and provider_id to PostgreSQL (different databases)

.. dropdown:: Task 2.2: Index Strategy (1 point)
   :icon: gear
   :class-container: sd-border-primary

   For each collection, define appropriate indexes and document them in ``docs/polyglot_design.md``.

   **Index Types to Consider**:

   - **Compound Indexes**: (patient_id, encounter_date) for patient timeline queries
   - **Text Indexes**: Full-text search on clinical narratives (chief_complaint, assessment, plan)
   - **TTL Indexes**: Auto-delete telemedicine session logs after retention period
   - **Partial Indexes**: Unsigned notes only (for provider review workflow)


Part 3: MongoDB Implementation
-------------------------------

**Objective**: Set up MongoDB collections and write clinical queries.

.. dropdown:: Task 3.1: Database Setup (1 point)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Create ``mongo_setup.js`` to define collections with validation and indexes:

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

   **Files to create**: ``mongodb/mongo_setup.js`` and ``mongodb/mongo_data.js``

.. dropdown:: Task 3.2: Query Development (2 points)
   :icon: gear
   :class-container: sd-border-primary

   Write **at least 6 MongoDB queries** covering the following categories:

   **Aggregation Pipelines (3 queries minimum)**

   Examples:

   - *"Clinical documentation volume by provider and note type."*
   - *"Patient survey scoring and trend analysis (e.g., PHQ-9 depression screening)."*
   - *"Average time between admission and discharge summary completion."*

   **Text Search (1 query minimum)**

   Example: *"Search clinical notes for a specific diagnosis or symptom across all note types."*

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


Part 4: Python Integration
---------------------------

**Objective**: Extend your GP2 Python application with MongoDB support and cross-database clinical services.

.. dropdown:: Task 4.1: Cross-Database Integration (2 points)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Extend your project structure**:

   .. code-block:: text

      healthcare-management/
      ├── config/
      │   ├── database.py      # Existing: PostgreSQL
      │   └── mongodb.py       # New: MongoDB connection
      ├── repositories/
      │   ├── postgres/        # Existing from GP2
      │   └── mongodb/         # New: MongoDB repositories
      │       ├── clinical_notes_repo.py
      │       └── imaging_repo.py
      ├── services/
      │   └── clinical_service.py # New: cross-database clinical records

   **Unified Clinical Record Service**:

   .. code-block:: python

      class ClinicalRecordService:
          def get_complete_record(self, patient_id, user_id,
                                 user_role):
              """Build complete patient record from both databases."""
              # PostgreSQL: Demographics, medications, labs
              patient = self.pg_patient_repo.find_by_id(
                  patient_id, user_id, user_role
              )
              medications = self.pg_prescription_repo.find_active(
                  patient_id
              )

              # MongoDB: Clinical notes, care plans
              notes = self.mongo_notes_repo.find_by_patient(
                  patient_id, limit=10
              )

              return {
                  "demographics": patient,
                  "active_medications": medications,
                  "clinical_notes": notes
              }

   **New CLI Menu Options** (at least 3):

   - View recent clinical notes for a patient (MongoDB query)
   - Search clinical notes by keyword (text search)
   - Complete patient record combining PostgreSQL and MongoDB data (cross-database)

   Update ``cli/main.py`` to include these new options alongside your GP2 options.


Folder Structure
----------------

.. code-block:: text

   GP3_Healthcare_Team{X}/
   ├── mongodb/
   │   ├── mongo_setup.js          # Collection creation with validation
   │   ├── mongo_data.js           # Sample clinical document data
   │   └── mongo_queries.js        # 6+ documented queries
   ├── src/
   │   ├── config/
   │   │   ├── database.py         # Existing: PostgreSQL
   │   │   └── mongodb.py          # New: MongoDB connection
   │   ├── repositories/
   │   │   ├── postgres/           # Existing from GP2
   │   │   └── mongodb/            # New: MongoDB repositories
   │   │       ├── clinical_notes_repo.py
   │   │       └── imaging_repo.py
   │   ├── services/
   │   │   └── clinical_service.py # New: cross-database records
   │   └── cli/
   │       └── main.py             # Updated: new MongoDB menu options
   ├── docs/
   │   └── polyglot_design.md      # Partitioning, schemas, indexes
   ├── requirements.txt
   ├── .env.example
   ├── README.md
   └── team_contributions.md


Documentation Files
-------------------

.. dropdown:: What goes in each file
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **docs/polyglot_design.md**

   This is the main design document for GP3. It should contain three sections: (1) your data partitioning analysis explaining what stays in PostgreSQL and what moves to MongoDB with clinical justifications for each data type, (2) your MongoDB collection schemas with document structures, embedding rationale, and expected volumes, and (3) your index strategy listing all indexes for each collection with their type and purpose.

   **requirements.txt**

   Updated from GP2 to include ``pymongo``.

   **.env.example**

   Updated from GP2 to include MongoDB connection variables.

   **README.md**

   Updated from GP2. Add MongoDB prerequisites (MongoDB 6+), setup instructions, and a data partitioning summary table.

   **team_contributions.md**

   List each team member's name, tasks completed, hours contributed, and contribution percentage. Percentages must sum to 100%.


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP3_Healthcare_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP3_Healthcare_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **Design Document**:

   - [ ] ``polyglot_design.md`` covers partitioning, schemas, and indexes
   - [ ] Each data type has a clear PostgreSQL vs. MongoDB justification
   - [ ] 4+ collections documented with embedding rationale

   **MongoDB Files**:

   - [ ] ``mongo_setup.js`` creates all collections with validation and indexes
   - [ ] ``mongo_data.js`` loads realistic clinical document data (runs without errors)
   - [ ] ``mongo_queries.js`` contains 6+ queries with documentation

   **Python Application**:

   - [ ] MongoDB connection configured (pymongo)
   - [ ] Repository classes for clinical document collections
   - [ ] Cross-database ClinicalRecordService working
   - [ ] 3+ new CLI menu options for MongoDB data

   **Supporting Files**:

   - [ ] README.md updated with MongoDB setup instructions
   - [ ] .env.example updated with MongoDB variables
   - [ ] requirements.txt updated with pymongo
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
   * - **Part 1: Data Partitioning**
     - 2
     - Clear clinical rationale for each data type (1pt); documented decision framework (1pt)
   * - **Part 2: Schema and Indexes**
     - 3
     - 4+ collections with complete schemas and embedding rationale (2pts); appropriate indexes with justification (1pt)
   * - **Part 3: Setup and Queries**
     - 3
     - Collections with validation and realistic data (1pt); 6+ queries covering all categories with correct results (2pts)
   * - **Part 4: Python Integration**
     - 2
     - MongoDB repositories and cross-database clinical service (1pt); 3+ new CLI menu options working (1pt)
   * - **Total**
     - **10**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Treating MongoDB like SQL (use embedding for related clinical data, not separate collections for everything)
   - No schema validation (MongoDB is flexible, not lawless; validate required clinical fields)
   - Same note structure for all types (progress notes, consults, and discharge summaries have different fields)
   - Missing text indexes (clinical narrative search requires text indexes)
   - No cross-database service (the unified patient record is the key deliverable)


Tips for Success
----------------

.. tip::

   - **Think like a clinician**: A doctor viewing a patient record wants notes, labs, medications, and care plans together. Design your cross-database service to support this workflow.
   - **Embrace document diversity**: The whole point of MongoDB here is that different clinical notes have different structures. Lean into this.
   - **Test aggregation pipelines incrementally**: Build one stage at a time in mongosh. Verify results before adding the next stage.
   - **Use realistic clinical vocabulary**: Reference real ICD-10 codes, real medication names, and realistic clinical narratives in your sample data.
   - **Use office hours**: Bring your schema designs for review. Discuss clinical document modeling with instructors.
