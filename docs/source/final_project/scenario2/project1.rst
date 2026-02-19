====================================================
Group Project 1: Relational Database Design
====================================================

Overview
--------

Design the PostgreSQL database schema that will serve as the HIPAA-compliant transactional backbone of your healthcare management system. You'll model clinical workflows, identify entities with protected health information (PHI), define healthcare-specific constraints, and ensure regulatory compliance.

**Timeline**: 3 weeks

**Weight**: 10 points (25% of final project)

**Team Size**: 4 students


.. important::
   
   **What You'll Deliver**
   
   This project requires **13 files** in an organized folder structure:
   
   - 2 ER diagrams (Chen notation + Crow's Foot notation)
   - 8 documentation PDFs (catalogs, analysis, proofs, PHI matrix)
   - 1 healthcare identifier strategy document
   - 2 supporting files (README, team contributions)
   
   **Submission**: Single ZIP file named ``GP1_Healthcare_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Extract healthcare entities from clinical and administrative requirements
- Design Entity-Relationship Diagrams with HIPAA compliance considerations
- Identify healthcare-specific identifiers (MRN, NPI, DEA numbers)
- Model clinical workflows and temporal relationships
- Apply normalization theory (1NF, 2NF, 3NF) to healthcare data
- Designate and document Protected Health Information (PHI)
- Design audit trail requirements for regulatory compliance
- Evaluate denormalization trade-offs in clinical contexts


Business Requirements
---------------------

Your healthcare management system must track the following information:

.. dropdown:: 📋 Patient Information Management
   :class-container: sd-border-primary
   :open:

   The healthcare network needs comprehensive patient records including demographic information (name, date of birth, Social Security Number, contact details, emergency contacts), insurance coverage with primary and secondary insurance details (policy numbers, group numbers, copay amounts), and unique medical record numbers (MRN) that follow patients across all 5 hospitals in the network. The system must track patient communication preferences, preferred pharmacy, primary care physician assignment, known allergies, and any special needs or accessibility requirements. Patient language preference and cultural considerations must be recorded for appropriate care delivery.

.. dropdown:: 📋 Healthcare Provider Directory
   :class-container: sd-border-primary

   The network employs physicians, nurse practitioners, physician assistants, specialists, and surgeons. Each provider needs credentials tracked including medical degree, board certifications, state license numbers with expiration dates, DEA number for prescribing controlled substances, and National Provider Identifier (NPI). Providers have specialties (primary care, cardiology, oncology, surgery, etc.), hospital privileges at specific facilities, office locations, and availability schedules. The system must track malpractice insurance, continuing education credits, and certification renewal dates.

.. dropdown:: 📋 Appointment Scheduling
   :class-container: sd-border-primary

   Patients schedule appointments with specific providers at specific facilities for various appointment types (routine checkup, follow-up, procedure, consultation, urgent care). Each appointment has date, time, duration, location (hospital, clinic, room number), status (scheduled, confirmed, checked-in, in-progress, completed, no-show, cancelled), reason for visit, and any special instructions. The system must prevent double-booking providers, track cancellations and no-shows for patient compliance monitoring, and handle appointment reminders. Different appointment types have different durations and billing implications.

.. dropdown:: 📋 Prescription Management
   :class-container: sd-border-primary

   Providers write prescriptions for patients specifying medication (generic or brand name), dosage, frequency, duration, number of refills allowed, special instructions (take with food, avoid alcohol), and pharmacy information. Prescriptions have status (active, completed, discontinued, cancelled) and must track refill history. For controlled substances (Schedule II-V), additional DEA number validation and tracking is required. The system must support electronic prescribing (e-prescribe) and maintain current medication lists for interaction checking.

.. dropdown:: 📋 Laboratory Services
   :class-container: sd-border-primary

   Providers order laboratory tests for patients including blood work, imaging studies (X-ray, CT, MRI), cultures, and pathology. Lab orders specify test type, priority (routine, urgent, stat), ordering provider, collection date/time, specimen type, and clinical indication. Lab results include test values, reference ranges (normal ranges by age/gender), abnormal flags (high, low, critical), interpretation notes from pathologist or radiologist, and performing technician. Results must be linked to orders and made available to ordering providers. Critical values require immediate notification.

.. dropdown:: 📋 Hospital Admissions
   :class-container: sd-border-primary

   When patients are admitted to a hospital, the system tracks admission date/time, admitting physician, attending physician of record, admission diagnosis, assigned room and bed, admission type (emergency, urgent, elective, observation), and expected length of stay. During hospitalization, the system records daily progress notes, procedures performed, consultations with specialists, medications administered, and condition changes. Discharge information includes discharge date/time, discharge disposition (home, skilled nursing facility, rehabilitation, transfer to another facility), discharge diagnosis, discharge instructions, follow-up appointments, and prescribed medications.

.. dropdown:: 📋 Insurance and Billing
   :class-container: sd-border-primary

   The system manages insurance claims submitted to insurance companies for services rendered. Each claim includes patient information, insurance policy details, service date, procedure codes (CPT codes), diagnosis codes (ICD-10), charge amounts, provider information, and facility information. Claims have statuses tracking their lifecycle (draft, submitted, pending, under review, approved, partially approved, denied, appealed). The system tracks claim submission dates, insurance adjudication dates, payment amounts, patient responsibility (copay, deductible, coinsurance), denial reasons with codes, and appeal workflows.

.. dropdown:: 📋 Medication Formulary
   :class-container: sd-border-primary

   The healthcare network maintains a medication formulary listing all approved medications with detailed information: generic name, brand names, drug class (therapeutic category), dosage forms (tablet, capsule, liquid), available strengths, route of administration, typical dosing guidelines, known contraindications (conditions where medication should not be used), documented drug-drug interactions, common adverse effects, pregnancy category, controlled substance schedule if applicable, and formulary tier affecting insurance coverage.

.. dropdown:: 📋 Audit and Compliance
   :class-container: sd-border-primary

   HIPAA regulations require comprehensive audit trails tracking all access to Protected Health Information (PHI). The system must log who accessed patient data, when access occurred, what data was accessed (table and record identifiers), why the access was necessary (required by HIPAA), whether access was successful or denied, user's role at time of access, and IP address. Audit logs must be tamper-proof and retained for regulatory periods (typically 6 years).


Task 1: Entity-Relationship Diagrams
-------------------------------------

**Objective**: Design conceptual and logical data models with HIPAA considerations.

.. dropdown:: 📋 Minimum Entities (13+ required)
   :class-container: sd-border-primary
   :open:

   Your models must include entities covering:
   
   - **Patient Care**: Patients, providers, appointments, prescriptions
   - **Clinical Services**: Lab orders, lab results, admissions
   - **Financial**: Insurance claims, insurance companies
   - **Reference Data**: Medication formulary
   - **Compliance**: Audit logs, staff/users
   - **Administrative**: Healthcare facilities
   
   **Healthcare-Specific Design Questions**:
   
   - What identifies a patient uniquely across the network?
   - How do you model insurance (patients can have multiple policies)?
   - What is the relationship between prescriptions and medications?
   - How do lab orders relate to lab results (one order, multiple results)?

.. dropdown:: 📋 Part A: Conceptual Model - Chen Notation
   :class-container: sd-border-primary

   Create a **conceptual ER diagram** using **Chen notation**.
   
   **Minimum Requirements**:
   
   - 13+ entities covering all business areas
   - All relationships shown as diamonds
   - Cardinality ratios (1:1, 1:N, M:N) labeled
   - Participation constraints (total/partial) indicated
   - PHI attributes marked or highlighted
   
   **Notation Elements**:
   
   - **Rectangles** for entities
   - **Diamonds** for relationships
   - **Ovals** for attributes (connected to entities)
   - **Underlined attributes** for primary keys
   - **Double ovals** for multivalued attributes (e.g., patient phone numbers)
   - **Dashed ovals** for derived attributes (e.g., patient age from DOB)
   - **Composite attributes** shown with sub-ovals (e.g., patient address)
   
   **Healthcare Considerations**:
   
   - Mark which attributes contain PHI (Protected Health Information)
   - Show healthcare identifiers (MRN, NPI, DEA) clearly
   - Indicate multivalued attributes (e.g., multiple insurance policies)
   
   **Purpose**: Focus on **what** healthcare data exists and **how** entities relate conceptually.
   
   **Tools**:
   
   - Inkscape (recommended for SVG format)
   - Lucidchart
   - Draw.io
   - Hand-drawn (if very neat)
   
   **File to create**: ``diagrams/chen_conceptual_model.pdf`` (or ``.svg``)

.. dropdown:: 📋 Part B: Logical Model - Crow's Foot Notation
   :class-container: sd-border-primary

   Create a **logical ER diagram** using **Crow's Foot notation**.
   
   **Minimum Requirements**:
   
   - Same 13+ entities as Chen diagram
   - Attributes listed inside entity rectangles
   - Primary keys marked (PK)
   - Foreign keys indicated (FK)
   - Healthcare identifiers clearly shown (MRN, NPI, DEA)
   
   **Notation Elements**:
   
   - **Rectangles** for entities (tables)
   - **Lines** connecting entities for relationships
   - **Cardinality symbols**:
     
     - Single line: One
     - Crow's foot (three lines): Many
     - Circle: Optional (minimum 0)
     - Bar: Mandatory (minimum 1)
   
   **Purpose**: Show **how** entities will be implemented as relational tables.
   
   **Tools**:
   
   - Lucidchart (excellent for Crow's Foot)
   - Draw.io
   - ERDPlus
   - Inkscape (manual layout)
   
   **File to create**: ``diagrams/crows_foot_logical_model.pdf``

.. dropdown:: 📋 PHI Designation Matrix
   :class-container: sd-border-primary

   Identify which entities and attributes contain **Protected Health Information**.
   
   PHI includes 18 identifiers under HIPAA:
   
   - Names, addresses, dates (birth, admission, discharge, etc.)
   - Phone numbers, email addresses, fax numbers
   - Medical record numbers, account numbers
   - Social Security Numbers
   - Health plan beneficiary numbers
   - Any unique identifying number or code
   
   **Format**: Table
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Entity
        - Attribute
        - PHI Type
        - Protection Required
      * - PATIENT
        - patient_name
        - Name (HIPAA #1)
        - Audit logging, RBAC, encryption
      * - PATIENT
        - date_of_birth
        - Date (HIPAA #3)
        - Audit logging, RBAC
      * - PATIENT
        - ssn
        - SSN (HIPAA #6)
        - Audit logging, RBAC, encryption, restricted access
      * - PATIENT
        - mrn
        - Medical Record # (HIPAA #10)
        - Audit logging, RBAC
   
   **Mark PHI entities** in your documentation. These require:
   
   - Audit logging for all access
   - Role-based access control
   - Encryption considerations
   - Retention policies
   
   **File to create**: ``documentation/phi_matrix.pdf``

.. dropdown:: 📋 Healthcare Identifiers Strategy
   :class-container: sd-border-primary

   Understand and document how these standard identifiers are used in your design:
   
   **MRN (Medical Record Number)**:
   
   - Uniquely identifies patient within healthcare organization
   - May be facility-specific or network-wide
   - Your design decision: One MRN across all hospitals?
   
   **NPI (National Provider Identifier)**:
   
   - 10-digit unique identifier for healthcare providers
   - Federally assigned, does not change
   - Required for Medicare/Medicaid billing
   
   **DEA Number**:
   
   - Required for providers prescribing controlled substances
   - Format: 2 letters + 7 digits
   - Must be validated for Schedule II-V prescriptions
   
   **Document your decisions** about each identifier:
   
   .. code-block:: text
   
      Identifier: MRN (Medical Record Number)
      
      Design Decision: Network-wide MRN (single MRN per patient)
      
      Justification:
      - Patients visit multiple hospitals in our 5-hospital network
      - Single MRN prevents duplicate records across facilities
      - Simplifies cross-facility queries and reporting
      
      Implementation:
      - Primary key: patient_id (SERIAL, surrogate)
      - Candidate key: mrn (VARCHAR(10), UNIQUE, NOT NULL)
      - Format: 10-digit zero-padded number
      - Generation: Centralized MRN assignment service
      
      Alternative Considered: Facility-specific MRN
      - Rejected because: Requires complex mapping tables,
        increases risk of duplicate patient records
   
   **File to create**: ``documentation/healthcare_identifier_strategy.pdf``

.. dropdown:: 📋 Entity Catalog
   :class-container: sd-border-primary

   Document **each entity** (13+ required) with complete details.
   
   **Format**: One section per entity
   
   **Required Information**:
   
   - Entity name and purpose
   - Complete attribute list with data types
   - Primary key justification
   - PHI designation (yes/no, which attributes)
   - Business rules for this entity
   - Sample record example
   
   **Example Entry**:
   
   .. code-block:: text
   
      Entity: PATIENT
      
      Purpose: Represents a patient registered in the healthcare network
      
      PHI Entity: YES (contains multiple HIPAA identifiers)
      
      Attributes:
      - patient_id (SERIAL) - Internal surrogate key
      - mrn (VARCHAR(10)) - Medical Record Number [PHI]
      - first_name (VARCHAR(50)) - Legal first name [PHI]
      - last_name (VARCHAR(50)) - Legal last name [PHI]
      - date_of_birth (DATE) - Date of birth [PHI]
      - ssn (VARCHAR(11)) - Social Security Number [PHI]
      - gender (VARCHAR(20)) - Gender identity
      - phone_primary (VARCHAR(15)) - Primary phone [PHI]
      - email (VARCHAR(100)) - Email address [PHI]
      - address_street (VARCHAR(200)) - Street address [PHI]
      - address_city (VARCHAR(100)) - City [PHI]
      - address_state (CHAR(2)) - State code [PHI]
      - address_zip (VARCHAR(10)) - ZIP code [PHI]
      - preferred_language (VARCHAR(50)) - Communication language
      - primary_provider_id (INTEGER) - FK to PROVIDER
      - preferred_pharmacy_id (INTEGER) - FK to PHARMACY
      - emergency_contact_name (VARCHAR(100)) - Emergency contact [PHI]
      - emergency_contact_phone (VARCHAR(15)) - Emergency phone [PHI]
      - created_at (TIMESTAMP) - Record creation
      - updated_at (TIMESTAMP) - Last modification
      
      Primary Key: patient_id
      Justification: Surrogate key provides stable internal identifier.
                     MRN serves as unique candidate key for external use.
      
      Business Rules:
      - MRN must be unique across the network
      - SSN must be unique (validated format: XXX-XX-XXXX)
      - Date of birth cannot be in the future
      - Primary provider must be an active provider
      - At least one contact method required (phone or email)
      
      Sample Record:
      (1001, '0000012345', 'Maria', 'Rodriguez', '1985-03-15',
       '555-12-3456', 'Female', '301-555-0123', 'maria.r@email.com',
       '123 Oak Street', 'Bethesda', 'MD', '20814', 'Spanish',
       42, 15, 'Carlos Rodriguez', '301-555-0456',
       '2024-01-15 09:30:00', '2026-02-10 14:22:00')
   
   **File to create**: ``documentation/entity_catalog.pdf``

.. dropdown:: 📋 Relationship Documentation
   :class-container: sd-border-primary

   Document **all relationships** between entities.
   
   **Format**: Table
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Parent Entity
        - Child Entity
        - Relationship Name
        - Cardinality
        - Business Rule
        - Example Scenario
      * - PATIENT
        - APPOINTMENT
        - schedules
        - 1:N
        - Each patient has 0 to many appointments
        - Maria has 3 upcoming appointments (cardiology, lab, follow-up)
      * - PROVIDER
        - PRESCRIPTION
        - writes
        - 1:N
        - Each provider writes 0 to many prescriptions
        - Dr. Smith wrote 15 prescriptions this week
      * - PATIENT
        - INSURANCE_COVERAGE
        - has
        - 1:N
        - Each patient has 1 to many insurance policies
        - John has primary (BlueCross) and secondary (Medicare)
      * - LAB_ORDER
        - LAB_RESULT
        - produces
        - 1:N
        - Each order produces 1 to many results
        - CBC order produces WBC, RBC, hemoglobin results
   
   **File to create**: ``documentation/relationship_documentation.pdf``


Task 2: Keys and Constraints
-----------------------------

**Objective**: Define keys and constraints for healthcare data integrity.

.. dropdown:: 📋 Healthcare-Specific Primary Keys
   :class-container: sd-border-primary
   :open:

   **Patient Primary Key Decision**:
   
   Should you use:
   
   A. MRN as primary key (natural key)
   B. SERIAL patient_id with MRN as unique candidate key (surrogate)
   C. Composite key combining facility and MRN
   
   Consider:
   
   - Does your network use unified MRN or facility-specific?
   - What if MRN needs to change (data correction)?
   - How does this affect foreign keys throughout system?
   
   **Provider Primary Key**:
   
   - Use NPI (10-digit national identifier)?
   - Use internal provider_id with NPI as candidate key?
   - What about providers without NPI (students, interns)?
   
   **Decision Framework**:
   
   .. code-block:: text
   
      Does a natural healthcare identifier exist?
      ├── YES: Is it stable (won't change)?
      │   ├── YES: Is it universal (all records have one)?
      │   │   ├── YES: Consider using as PK (e.g., NPI for providers)
      │   │   └── NO: Use surrogate PK, natural as candidate key
      │   └── NO: Use surrogate PK (natural may change)
      └── NO: Use surrogate key (SERIAL)
   
   **Format**: Table
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Entity
        - Primary Key
        - Type
        - Data Type
        - Generation
        - Justification
      * - PATIENT
        - patient_id
        - Surrogate
        - SERIAL
        - Auto-increment
        - MRN may need correction; surrogate is stable
      * - PROVIDER
        - provider_id
        - Surrogate
        - SERIAL
        - Auto-increment
        - Not all providers have NPI (students, interns)
      * - MEDICATION
        - medication_id
        - Surrogate
        - SERIAL
        - Auto-increment
        - RxNorm codes may change; surrogate is stable
   
   **File to create**: ``documentation/keys_analysis.pdf`` (Section 1)

.. dropdown:: 📋 Candidate Keys
   :class-container: sd-border-primary

   Identify **alternative unique identifiers** for each entity.
   
   **Example**:
   
   .. code-block:: text
   
      Entity: PATIENT
      
      Primary Key: patient_id
      
      Candidate Keys:
      1. mrn - Medical Record Number (unique across network)
         - Not chosen as PK: May need correction/reassignment
         - UNIQUE constraint: YES
      2. ssn - Social Security Number
         - Not chosen as PK: Sensitive PHI, not always available
         - UNIQUE constraint: YES (where NOT NULL)
      
      Entity: PROVIDER
      
      Primary Key: provider_id
      
      Candidate Keys:
      1. npi - National Provider Identifier (10-digit)
         - Not chosen as PK: Not all providers have NPI
         - UNIQUE constraint: YES (where NOT NULL)
      2. dea_number - DEA registration number
         - Not chosen as PK: Only prescribing providers have one
         - UNIQUE constraint: YES (where NOT NULL)
   
   **File to create**: ``documentation/keys_analysis.pdf`` (Section 2)

.. dropdown:: 📋 Healthcare-Specific Foreign Keys
   :class-container: sd-border-primary

   Define **referential integrity rules** for clinical relationships.
   
   **Critical Scenarios**:
   
   *"If a patient requests data deletion under privacy laws, what happens to their prescriptions, lab results, appointment history?"*
   
   - **RESTRICT**: Cannot delete patient if records exist (maintain clinical history)
   - **CASCADE**: Delete all records (loses medical information)
   - **SET NULL**: Keep records, remove patient link (anonymize but keep data)
   - **Special handling**: Flag as "deleted" but retain data for legal periods
   
   *"If a provider leaves the network, what happens to their historical prescriptions and clinical orders?"*
   
   - Cannot delete provider (historical records reference them)
   - May need "active" flag rather than physical deletion
   - Transfer active patients to new provider
   
   **Format**: Table
   
   .. list-table::
      :header-rows: 1
      :class: compact-table
   
      * - Child Entity
        - FK Column
        - References
        - ON DELETE
        - ON UPDATE
        - Justification
      * - APPOINTMENT
        - patient_id
        - PATIENT(patient_id)
        - RESTRICT
        - CASCADE
        - Cannot delete patient with appointment history
      * - PRESCRIPTION
        - provider_id
        - PROVIDER(provider_id)
        - RESTRICT
        - CASCADE
        - Prescriber history must be preserved (legal requirement)
      * - PRESCRIPTION
        - patient_id
        - PATIENT(patient_id)
        - RESTRICT
        - CASCADE
        - Prescription history is part of medical record
      * - INSURANCE_CLAIM
        - patient_id
        - PATIENT(patient_id)
        - RESTRICT
        - CASCADE
        - Financial records must be retained
   
   **File to create**: ``documentation/keys_analysis.pdf`` (Section 3)

.. dropdown:: 📋 Healthcare Business Rules (Constraints)
   :class-container: sd-border-primary

   Document **minimum 20 constraints** across all entities.
   
   **Clinical Constraints**:
   
   .. code-block:: text
   
      Constraint #1
      Entity/Attribute: PATIENT.date_of_birth
      Type: CHECK
      Business Rule: Patient age must be medically valid
      SQL Expression: CHECK (date_of_birth <= CURRENT_DATE
                      AND EXTRACT(YEAR FROM AGE(date_of_birth)) <= 120)
      Valid Example: '1985-03-15'
      Invalid Example: '2030-01-01', '1850-01-01'
      Clinical Justification: Prevents data entry errors that could affect dosing calculations
      
      Constraint #2
      Entity/Attribute: APPOINTMENT.appointment_end
      Type: CHECK
      Business Rule: Appointment must end after it starts
      SQL Expression: CHECK (appointment_end > appointment_start)
      Valid Example: start='2026-02-19 09:00', end='2026-02-19 09:30'
      Invalid Example: start='2026-02-19 09:30', end='2026-02-19 09:00'
      Clinical Justification: Prevents scheduling errors
      
      Constraint #3
      Entity/Attribute: PRESCRIPTION.dosage_amount
      Type: CHECK
      Business Rule: Dosage must be positive
      SQL Expression: CHECK (dosage_amount > 0)
      Valid Example: 10.0 (mg)
      Invalid Example: 0, -5
      Clinical Justification: Zero or negative dosage is medically meaningless and dangerous
      
      Constraint #4
      Entity/Attribute: PRESCRIPTION (conditional)
      Type: CHECK
      Business Rule: Controlled substances require prescriber DEA number
      SQL Expression: CHECK (controlled_substance_schedule IS NULL
                      OR prescriber_dea_number IS NOT NULL)
      Valid Example: Schedule II with DEA 'AB1234567'
      Invalid Example: Schedule II with NULL DEA
      Clinical Justification: Federal law requires DEA for controlled substance prescriptions
      
      Constraint #5
      Entity/Attribute: ADMISSION.discharge_date
      Type: CHECK
      Business Rule: Discharge cannot precede admission
      SQL Expression: CHECK (discharge_date IS NULL OR discharge_date >= admission_date)
      Valid Example: admit='2026-02-10', discharge='2026-02-15'
      Invalid Example: admit='2026-02-15', discharge='2026-02-10'
      Clinical Justification: Temporal integrity of patient stay records
   
   **Categories to Cover**:
   
   - Clinical validity (ages, dosages, dates)
   - Temporal integrity (start < end, admission < discharge)
   - Controlled substance compliance (DEA requirements)
   - Financial accuracy (copay + deductible <= billed)
   - Insurance validity (effective_date <= termination_date)
   - Enumerated values (statuses, types, priorities)
   - Mandatory fields (NOT NULL for critical clinical data)
   
   **File to create**: ``documentation/constraints_catalog.pdf``


Task 3: Normalization and Schema
---------------------------------

**Objective**: Convert ERD to normalized relational schema while preserving clinical usability.

.. dropdown:: 📋 Relational Schema Notation
   :class-container: sd-border-primary
   :open:

   Express **each entity** in relational notation.
   
   **Format**:
   
   .. code-block:: text
   
      ENTITY_NAME(attribute1, attribute2, attribute3, ...)
      
      Primary Key: attribute1
      Candidate Keys: (attr_x, attr_y), attr_z
      Foreign Keys: attr -> PARENT_ENTITY(parent_pk)
      PHI: YES/NO (list PHI attributes)
   
   **Example**:
   
   .. code-block:: text
   
      PATIENT(patient_id, mrn, first_name, last_name, date_of_birth,
              ssn, gender, phone_primary, email, address_street,
              address_city, address_state, address_zip,
              preferred_language, primary_provider_id,
              preferred_pharmacy_id, emergency_contact_name,
              emergency_contact_phone, created_at, updated_at)
      
      Primary Key: patient_id
      Candidate Keys: mrn, ssn
      Foreign Keys: primary_provider_id -> PROVIDER(provider_id)
      PHI: YES (mrn, first_name, last_name, date_of_birth, ssn,
           phone_primary, email, address_*, emergency_contact_*)
      
      PRESCRIPTION(prescription_id, patient_id, provider_id,
                   medication_id, dosage_amount, dosage_unit,
                   frequency, duration_days, refills_allowed,
                   refills_used, special_instructions, pharmacy_id,
                   status, prescribed_date, controlled_substance_schedule,
                   prescriber_dea_number, created_at, updated_at)
      
      Primary Key: prescription_id
      Candidate Keys: None
      Foreign Keys: patient_id -> PATIENT(patient_id),
                    provider_id -> PROVIDER(provider_id),
                    medication_id -> MEDICATION(medication_id)
      PHI: YES (patient_id links to PHI)
   
   Continue for **all 13+ entities**.
   
   **File to create**: ``documentation/relational_schema.pdf``

.. dropdown:: 📋 Normalization Proofs
   :class-container: sd-border-primary

   Prove **each entity** is in 3NF.
   
   **For Each Entity, Verify**:
   
   **First Normal Form (1NF)**:
   
   - All attributes atomic (no arrays or lists)
   - No repeating groups
   - Each row unique (has primary key)
   - Each column single-valued
   
   **Second Normal Form (2NF)**:
   
   - In 1NF
   - No partial dependencies
   - Note: If single-attribute PK, automatically in 2NF
   - If composite PK: all non-key attributes depend on **entire** key
   
   **Third Normal Form (3NF)**:
   
   - In 2NF
   - No transitive dependencies
   - No non-key attribute determines another non-key attribute
   
   **Example Proof**:
   
   .. code-block:: text
   
      Entity: PATIENT
      
      Functional Dependencies:
      FD1: patient_id -> all other attributes
      FD2: mrn -> patient_id (and transitively, all attributes)
      FD3: ssn -> patient_id (and transitively, all attributes)
      
      1NF: All attributes atomic, no repeating groups
           Note: address split into street, city, state, zip (atomic)
           Note: phone numbers are single-valued per column
      
      2NF: Single-attribute primary key (patient_id)
           Automatically satisfies 2NF (no partial dependencies possible)
      
      3NF: No transitive dependencies
           - address_state does NOT determine address_city
             (multiple cities per state)
           - preferred_language does NOT determine any other attribute
           - All non-key attributes depend only on patient_id
      
      Conclusion: PATIENT is in 3NF
   
   **File to create**: ``documentation/normalization_proofs.pdf``

.. dropdown:: 📋 Healthcare Normalization Challenges
   :class-container: sd-border-primary

   Analyze these healthcare-specific normalization decisions:
   
   **Challenge 1: Patient Contact Information**
   
   Should patient addresses be:
   
   - Attributes in PATIENT table (simple but not normalized)?
   - Separate PATIENT_ADDRESS table (normalized, supports multiple addresses)?
   - Composite attributes (street, city, state, zip as separate columns)?
   
   Consider: Patients may have home, work, and mailing addresses.
   
   **Challenge 2: Provider Credentials**
   
   Should licenses and certifications be:
   
   - Columns in PROVIDER table (license_number, license_state, expiration)?
   - Separate PROVIDER_LICENSE table (handles multiple state licenses)?
   - Mixed approach (some in PROVIDER, complex ones in separate table)?
   
   Consider: Providers may have licenses in multiple states, multiple board certifications.
   
   **Challenge 3: Medication Information**
   
   Should prescription include medication details or just reference?
   
   - Store medication_name in PRESCRIPTION table (denormalized)?
   - Only store medication_id, get name from MEDICATION_FORMULARY (normalized)?
   
   Consider: Medication names can change (brand discontinued), but prescription record must stay accurate.

.. dropdown:: 📋 Denormalization Analysis
   :class-container: sd-border-primary

   Analyze **5 healthcare-specific denormalization scenarios**.
   
   **Scenario Template**:
   
   - **Opportunity**: What data could be denormalized?
   - **Benefits**: Faster queries? Simpler access?
   - **Costs**: Redundancy? Update complexity? Staleness risk?
   - **Alternative**: Materialized view or computed column possible?
   - **Recommendation**: Keep normalized or denormalize? Why?
   
   **Example Scenario 1**:
   
   .. code-block:: text
   
      Scenario: Patient Age Calculation
      
      Opportunity: Store date_of_birth AND calculated age in PATIENT
      
      Benefits:
      - Faster query: many clinical decisions depend on age
      - Simpler SQL: no AGE() function in every query
      - Used in medication dosing, reference ranges
      
      Costs:
      - Age changes daily (gets stale immediately)
      - Must recalculate continuously
      - Risk of using stale age for critical decisions
      
      Alternative: Computed column or view
      CREATE VIEW patient_with_age AS
      SELECT *, EXTRACT(YEAR FROM AGE(date_of_birth)) AS age
      FROM patient;
      
      Recommendation: Use computed view
      Justification:
      - Age is always current (computed on query)
      - No staleness risk for clinical decisions
      - Minimal performance impact
      - Best practice for derived clinical data
   
   **Example Scenario 2**:
   
   .. code-block:: text
   
      Scenario: Current Medication List
      
      Opportunity: Maintain PATIENT_CURRENT_MEDS summary table
      
      Benefits:
      - Checked at every appointment, before every procedure
      - Critical for drug interaction checking
      - Faster than querying PRESCRIPTION with status filter
      
      Costs:
      - Must update on every prescription change
      - Potential inconsistency if trigger fails
      - Dual maintenance burden
      
      Alternative: Materialized view refreshed on prescription changes
      
      Recommendation: Use materialized view with trigger refresh
      Justification:
      - Medication list is safety-critical (must be current)
      - Materialized view provides fast reads
      - Trigger ensures refresh on any prescription change
      - Acceptable trade-off for patient safety
   
   **File to create**: ``documentation/denormalization_analysis.pdf``


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP1_Healthcare_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP1_Healthcare_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP1_Healthcare_Team{X}/
   ├── diagrams/
   │   ├── chen_conceptual_model.pdf      (or .svg)
   │   └── crows_foot_logical_model.pdf
   ├── documentation/
   │   ├── entity_catalog.pdf
   │   ├── relationship_documentation.pdf
   │   ├── keys_analysis.pdf
   │   ├── constraints_catalog.pdf
   │   ├── relational_schema.pdf
   │   ├── normalization_proofs.pdf
   │   ├── denormalization_analysis.pdf
   │   ├── phi_matrix.pdf
   │   └── healthcare_identifier_strategy.pdf
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Task 1: Entity-Relationship Diagrams
   :class-container: sd-border-info

   **Diagrams** (2 files):
   
   - ``diagrams/chen_conceptual_model.pdf`` (or ``.svg``)
   - ``diagrams/crows_foot_logical_model.pdf``
   
   **Documentation** (4 files):
   
   - ``documentation/entity_catalog.pdf``
   - ``documentation/relationship_documentation.pdf``
   - ``documentation/phi_matrix.pdf``
   - ``documentation/healthcare_identifier_strategy.pdf``

.. dropdown:: 📄 Task 2: Keys and Constraints
   :class-container: sd-border-info

   **Documentation** (2 files):
   
   - ``documentation/keys_analysis.pdf``
     
     - Section 1: Primary Keys
     - Section 2: Candidate Keys
     - Section 3: Foreign Key Matrix
   
   - ``documentation/constraints_catalog.pdf``

.. dropdown:: 📄 Task 3: Normalization and Schema
   :class-container: sd-border-info

   **Documentation** (3 files):
   
   - ``documentation/relational_schema.pdf``
   - ``documentation/normalization_proofs.pdf``
   - ``documentation/denormalization_analysis.pdf``

.. dropdown:: 📄 Supporting Files
   :class-container: sd-border-info

   **Required** (2 files):
   
   - ``README.md`` - Project overview and file guide
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP1: Healthcare Patient Management - Relational Database Design
   
   **Team Number**: [Your team number]
   
   **Scenario**: Healthcare Patient Management Platform
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Project Overview
   
   [2-3 sentence description of your design approach]
   
   ## Key Design Decisions
   
   1. **MRN Strategy**: [Network-wide vs. facility-specific, rationale]
   2. **Provider Keys**: [NPI usage, handling of providers without NPI]
   3. **PHI Protection**: [Approach to identifying and protecting PHI]
   
   ## Entity Summary
   
   Our design includes [X] entities:
   
   1. PATIENT - [Brief purpose]
   2. PROVIDER - [Brief purpose]
   3. APPOINTMENT - [Brief purpose]
   4. [Continue for all entities]
   
   ## HIPAA Compliance Notes
   
   - [X] entities contain PHI
   - Audit logging designed for all PHI tables
   - Role-based access control defined
   
   ## File Guide
   
   - `diagrams/chen_conceptual_model.pdf` - Conceptual ER diagram
   - `diagrams/crows_foot_logical_model.pdf` - Logical ER diagram
   - `documentation/entity_catalog.pdf` - Complete entity documentation
   - `documentation/phi_matrix.pdf` - PHI designation for all entities
   - [List all files with brief descriptions]
   
   ## Tools Used
   
   - **ER Diagrams**: [Inkscape, Lucidchart, Draw.io, etc.]
   - **Documentation**: [Google Docs, LaTeX, Microsoft Word, etc.]
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP1
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Created Chen notation ER diagram
   - Documented entities: PATIENT, PROVIDER, APPOINTMENT
   - Wrote PHI matrix
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Created Crow's Foot ER diagram
   - Documented entities: PRESCRIPTION, MEDICATION, LAB_ORDER, LAB_RESULT
   - Created healthcare identifier strategy document
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Documented entities: ADMISSION, INSURANCE_CLAIM, INSURANCE_COMPANY
   - Created constraints catalog (all 20+ constraints)
   - Wrote denormalization analysis
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Documented entities: AUDIT_LOG, FACILITY, STAFF
   - Created primary and candidate key analysis
   - Wrote normalization proofs and compiled README
   
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

   **Diagrams** (2 files):
   
   - [ ] Chen notation conceptual model (PDF or SVG)
   - [ ] Crow's Foot logical model (PDF)
   - [ ] Both diagrams show all 13+ entities
   - [ ] PHI attributes marked or highlighted in diagrams
   - [ ] Healthcare identifiers (MRN, NPI, DEA) visible
   - [ ] Diagrams are high resolution and legible
   
   **Documentation** (9 files):
   
   - [ ] Entity catalog (one section per entity, 13+ entities)
   - [ ] Relationship documentation (table format)
   - [ ] Keys analysis (PK, candidate keys, FK matrix)
   - [ ] Constraints catalog (20+ constraints with clinical justification)
   - [ ] Relational schema (all entities in notation)
   - [ ] Normalization proofs (1NF/2NF/3NF for each entity)
   - [ ] Denormalization analysis (5 healthcare scenarios)
   - [ ] PHI designation matrix
   - [ ] Healthcare identifier strategy
   
   **Supporting Files** (2 files):
   
   - [ ] README.md (project overview and file guide)
   - [ ] team_contributions.md (individual contributions)
   
   **Quality Checks**:
   
   - [ ] All PDFs open correctly (not corrupted)
   - [ ] File names match specification exactly
   - [ ] All team member names in README
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP1_Healthcare_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Over-simplifying insurance** - Insurance is complex (primary/secondary, pre-auth, claims lifecycle)
   
   ❌ **Forgetting audit trails** - HIPAA requires comprehensive logging. Design it from Day 1
   
   ❌ **Using real patient data** - NEVER use real data anywhere. This is a HIPAA violation
   
   ❌ **Ignoring provider credentials** - Licenses expire, DEA numbers are required for controlled substances
   
   ❌ **Missing PHI designation** - Every entity must be evaluated for PHI content
   
   ❌ **Too few entities** - 13+ required covering clinical, financial, and compliance domains
   
   ❌ **No clinical constraint justification** - Each constraint needs medical rationale
   
   ❌ **Wrong ZIP naming** - Not following ``GP1_Healthcare_Team{X}.zip`` format


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Task 1: ERD**
     - 4
     - 13+ entities including clinical and administrative (1pt); Relationships correct with HIPAA considerations (1.5pts); Proper notation with PHI designated (1pt); Complete documentation (0.5pt)
   * - **Task 2: Keys & Constraints**
     - 3
     - Healthcare identifiers (MRN, NPI, DEA) used appropriately (1pt); Foreign keys with clinical deletion scenarios (1pt); 20+ constraints with medical justifications (1pt)
   * - **Task 3: Normalization**
     - 3
     - Correct relational schema with PHI marked (1pt); 3NF proofs for healthcare entities (1pt); Thoughtful clinical denormalization analysis (1pt)
   * - **Total**
     - **10**
     - 


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP1**
   
   - **Research healthcare workflows** - Look up how real EHR systems work. Understanding clinical workflows (appointment to order to result to billing) helps design.
   - **HIPAA first** - Design audit and PHI protection from the beginning, not as an afterthought. Identify PHI attributes as you create each entity.
   - **Ask healthcare questions** - Office hours are perfect for healthcare domain questions. We expect you will need clarification!
   - **Use real examples** - Your own medical records (appointments, prescriptions, lab results) can inspire realistic attributes and relationships.
   - **Meet regularly** - Schedule 2-3 team meetings per week. Divide work but review together.
   - **Document as you go** - Do not wait until the end to write documentation. Capture decisions and rationale as you make them.


Next Steps
----------

After completing GP1, you will:

- Receive feedback from instructors
- Identify needed changes to your design
- Begin GP2: Implementing this schema in PostgreSQL with HIPAA security
- Create audit triggers, role-based access, and secure REST API

.. note::
   
   **Your GP1 design is the foundation** for GP2 (PostgreSQL with HIPAA audit logging), GP3 (MongoDB for clinical documents), and GP4 (Neo4j for medical knowledge graph).
   
   A strong relational design with proper PHI designation now makes HIPAA-compliant implementation much easier later!