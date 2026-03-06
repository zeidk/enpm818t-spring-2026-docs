====================================================
Group Project 1: Relational Database Design
====================================================

Overview
--------

Design the PostgreSQL database schema that will serve as the transactional backbone of your healthcare management system. You will model clinical workflows, identify healthcare-specific identifiers, and define clinical constraints.

.. card::
   :class-card: sd-bg-warning sd-bg-text-dark

   **Timeline**: 2 weeks |
   **Weight**: 10 points (20% of final project) |
   **Team Size**: 4 students


.. important::

   **What You'll Deliver**

   This project requires **3 deliverables** in an organized folder structure:

   - 2 ER diagrams (Chen notation PDF + Crow's Foot notation PDF)
   - 1 design report (PDF, 8 to 12 pages)

   **Submission**: Single ZIP file named ``GP1_Healthcare_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Extract healthcare entities from clinical and administrative requirements
- Design Entity-Relationship Diagrams (ERDs) for healthcare data
- Identify healthcare-specific identifiers (MRN, NPI, DEA numbers)
- Model clinical workflows and temporal relationships
- Apply normalization theory (1NF, 2NF, 3NF) to healthcare data
- Identify healthcare-specific identifiers (MRN, NPI, DEA numbers)


Business Requirements
---------------------

Your healthcare management system must track the following information:

.. dropdown:: Patient Information Management
   :icon: gear
   :class-container: sd-border-primary
   :open:

   The healthcare network needs comprehensive patient records including demographic information (name, date of birth, Social Security Number, contact details, emergency contacts), insurance coverage with primary and secondary insurance details (policy numbers, group numbers, copay amounts), and unique medical record numbers (MRN) that follow patients across all 5 hospitals in the network. The system must track patient communication preferences, preferred pharmacy, primary care physician assignment, and known allergies.

.. dropdown:: Healthcare Provider Directory
   :icon: gear
   :class-container: sd-border-primary

   The network employs physicians, nurse practitioners, physician assistants, specialists, and surgeons. Each provider needs credentials tracked including medical degree, board certifications, state license numbers with expiration dates, DEA number for prescribing controlled substances, and National Provider Identifier (NPI). Providers have specialties, hospital privileges at specific facilities, and availability schedules.

.. dropdown:: Appointment Scheduling
   :icon: gear
   :class-container: sd-border-primary

   Patients schedule appointments with specific providers at specific facilities for various appointment types (routine checkup, follow-up, procedure, consultation, urgent care). Each appointment has date, time, duration, location, status (scheduled, confirmed, checked-in, in-progress, completed, no-show, cancelled), and reason for visit. The system must prevent double-booking providers and track cancellations and no-shows.

.. dropdown:: Prescription Management
   :icon: gear
   :class-container: sd-border-primary

   Providers write prescriptions for patients specifying medication, dosage, frequency, duration, number of refills allowed, and special instructions. Prescriptions have status (active, completed, discontinued, cancelled) and must track refill history. For controlled substances (Schedule II-V), additional DEA number validation and tracking is required.

.. dropdown:: Laboratory Services
   :icon: gear
   :class-container: sd-border-primary

   Providers order laboratory tests for patients including blood work, imaging studies, cultures, and pathology. Lab orders specify test type, priority (routine, urgent, stat), ordering provider, and clinical indication. Lab results include test values, reference ranges, abnormal flags, and interpretation notes. Results must be linked to orders and made available to ordering providers.

.. dropdown:: Hospital Admissions
   :icon: gear
   :class-container: sd-border-primary

   When patients are admitted, the system tracks admission date/time, admitting physician, admission diagnosis, assigned room, admission type (emergency, urgent, elective, observation), and expected length of stay. Discharge information includes discharge date/time, discharge disposition, discharge diagnosis, discharge instructions, and follow-up appointments.

.. dropdown:: Insurance and Billing
   :icon: gear
   :class-container: sd-border-primary

   The system manages insurance claims submitted for services rendered. Each claim includes patient information, insurance policy details, service date, procedure codes (CPT), diagnosis codes (ICD-10), and charge amounts. Claims have statuses tracking their lifecycle (draft, submitted, pending, approved, denied, appealed). The system tracks payment amounts, patient responsibility, and denial reasons.


Task 1: Entity-Relationship Diagrams
-------------------------------------

**Objective**: Design conceptual and logical data models for healthcare data.

Your models must include entities covering these **seven business areas**: patient care, provider directory, appointment scheduling, prescription management, laboratory services, hospital admissions, and insurance and billing. You decide how many entities your design needs, as long as all seven areas are represented.

.. dropdown:: Part A: Conceptual Model -- Chen Notation
   :icon: gear
   :class-container: sd-border-primary
   :open:

   Create a **conceptual ER diagram** using **Chen notation** with **(min,max) participation notation**.

   **Notation Elements**:

   - **Rectangles** for entities
   - **Diamonds** for relationships
   - **Ovals** for key attributes (underlined for primary keys)
   - **(min,max)** labels on each side of a relationship to indicate participation and cardinality

   For example, if each patient has zero or many appointments, and each appointment belongs to exactly one patient, the PATIENT side is labeled (0,N) and the APPOINTMENT side is labeled (1,1).

   **Healthcare Considerations**:

   - Show healthcare identifiers (MRN, NPI, DEA) clearly

   **Tools** (with hyperlinks):

   - `Inkscape <https://inkscape.org/>`_ (recommended; see lecture code at `github.com/zeidk/enpm818t-spring-2026-code <https://github.com/zeidk/enpm818t-spring-2026-code>`_)
   - `PlantUML <https://plantuml.com/ie-diagram>`_ (see lecture code at `github.com/zeidk/enpm818t-spring-2026-code <https://github.com/zeidk/enpm818t-spring-2026-code>`_)
   - `Lucidchart <https://www.lucidchart.com/>`_
   - `Draw.io <https://app.diagrams.net/>`_

   **File to create**: ``chen_erd.pdf``

.. dropdown:: Part B: Logical Model -- Crow's Foot Notation
   :icon: gear
   :class-container: sd-border-primary

   Create a **logical ER diagram** using **Crow's Foot notation**.

   - Same entities as the Chen diagram, plus junction tables for any many-to-many relationships
   - Attributes listed inside entity rectangles
   - Primary keys marked (PK), foreign keys marked (FK)
   - Healthcare identifiers (MRN, NPI, DEA) clearly shown
   - Standard Crow's Foot cardinality symbols (one, many, optional, mandatory)

   **File to create**: ``crows_foot_erd.pdf``


Task 2: Design Report
-----------------------

**Objective**: Write an 8-to-12-page design report (PDF) that documents your design decisions.

The report should follow this structure. Approximate page counts are suggestions, not strict requirements.

.. note::

   The normalization concepts and algorithms used in this report are covered in
   :doc:`../../lectures/lecture4/lecture` (L4-5: Normalization & Denormalization).
   A compact reference is available as the
   :doc:`../../lectures/lecture4/cheat_sheet` or as a
   :download:`printable PDF </_static/images/l4/Normalization_Cheat_Sheet.pdf>`.

.. dropdown:: Report Outline
   :icon: gear
   :class-container: sd-border-primary
   :open:

   **Section 1: Entity Catalog (3 to 4 pages)**

   For each entity in your design, provide:

   - Entity name and purpose (one sentence)
   - Primary key and justification (why this key, surrogate vs. natural)
   - Candidate keys (alternative unique identifiers)
   - Business rules (constraints that apply to this entity)

   You do not need to list every attribute with data types. Focus on design decisions, not implementation details.

   **Example entry**:

   .. code-block:: text

      Entity: PATIENT

      Purpose: Represents a patient registered in the healthcare network.

      Primary Key: patient_id (surrogate, SERIAL)
      Justification: MRN may need correction; surrogate key provides
        stable internal identifier. MRN serves as candidate key for
        external use.

      Candidate Keys: mrn (unique across network), ssn (where not null)

      Business Rules:
      - MRN must be unique across the network
      - Date of birth cannot be in the future
      - At least one contact method required (phone or email)
      - Primary provider must be an active provider

   **Section 2: Relationship Analysis (1 to 2 pages)**

   Document key relationships between entities using a table format:

   .. list-table::
      :header-rows: 1
      :class: compact-table

      * - Parent Entity
        - Child Entity
        - Relationship
        - Cardinality
        - Business Rule
      * - PATIENT
        - APPOINTMENT
        - schedules
        - 1:N
        - Each patient has 0 to many appointments
      * - PROVIDER
        - PRESCRIPTION
        - writes
        - 1:N
        - Each provider writes 0 to many prescriptions
      * - LAB_ORDER
        - LAB_RESULT
        - produces
        - 1:N
        - Each order produces 1 to many results

   **Section 3: Healthcare Identifiers (1 to 2 pages)**

   Document your decisions about healthcare-specific identifiers:

   - **MRN**: Network-wide or facility-specific? Format? Generation strategy?
   - **NPI**: How handled for providers who do not yet have one (students, interns)?
   - **DEA Number**: Required only for controlled substance prescriptions. How enforced?

   **Section 4: Normalization Analysis (2 to 3 pages)**

   For each entity, prove it is in Third Normal Form (3NF):

   - List functional dependencies
   - Verify 1NF (atomic attributes, no repeating groups)
   - Verify 2NF (no partial dependencies)
   - Verify 3NF (no transitive dependencies)

   **Example**:

   .. code-block:: text

      Entity: PATIENT

      Functional Dependencies:
      FD1: patient_id -> all other attributes
      FD2: mrn -> patient_id (and transitively, all attributes)

      1NF: All attributes atomic. Address split into street, city,
           state, zip. Phone numbers single-valued per column.
      2NF: Single-attribute PK (patient_id), so automatically in 2NF.
      3NF: No transitive dependencies. address_state does NOT determine
           address_city (multiple cities per state). All non-key
           attributes depend only on patient_id.

      Conclusion: PATIENT is in 3NF.


Folder Structure
----------------

.. code-block:: text

   GP1_Healthcare_Team{X}/
   ├── chen_erd.pdf
   ├── crows_foot_erd.pdf
   └── design_report.pdf


Submission
----------

.. important::

   Submit **one** ZIP file to Canvas: ``GP1_Healthcare_Team{X}.zip``

   Replace ``{X}`` with your team number (e.g., ``GP1_Healthcare_Team03.zip``).


.. admonition:: Submission Checklist
   :class: tip

   **Diagrams**:

   - [ ] Chen ERD (PDF) using (min,max) notation
   - [ ] Crow's Foot ERD (PDF)
   - [ ] Both diagrams cover all seven business areas
   - [ ] Healthcare identifiers (MRN, NPI, DEA) visible
   - [ ] Diagrams are legible

   **Design Report**:

   - [ ] 8 to 12 pages, submitted as PDF
   - [ ] Entity catalog with PK justification, candidate keys, business rules
   - [ ] Relationship analysis table
   - [ ] Healthcare identifiers section
   - [ ] Normalization analysis (3NF proof for each entity)


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 35 10 55
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Task 1: ER Diagrams**
     - 4
     - Entities cover all seven business areas (1pt); relationships correct with (min,max) notation and healthcare identifiers visible (1.5pts); proper notation in both diagrams (1pt); healthcare identifiers visible (0.5pt)
   * - **Task 2: Entity Catalog and Relationships**
     - 2
     - Each entity has PK justification, candidate keys, business rules (1pt); relationship analysis complete with cardinality and business rules (1pt)
   * - **Task 2: Healthcare Identifiers**
     - 1
     - MRN/NPI/DEA strategy documented with justification
   * - **Task 2: Normalization**
     - 3
     - Correct functional dependencies identified (1pt); 3NF proofs for all entities (1pt); clear presentation (1pt)
   * - **Total**
     - **10**
     -


Common Mistakes to Avoid
-------------------------

.. danger::

   **Frequent Errors**

   - Over-simplifying insurance (primary/secondary, pre-auth, claims lifecycle are all important)
   - Using real patient data anywhere (NEVER use real patient data; always use synthetic data)
   - Ignoring provider credentials (licenses expire, DEA numbers are required for controlled substances)


Tips for Success
----------------

.. tip::

   - **Research healthcare workflows**: Look up how real EHR systems work. Understanding clinical workflows (appointment to order to result to billing) will help your design.
   - **Identifiers matter**: Plan your MRN, NPI, and DEA strategies early. These decisions affect multiple entities and constraints.
   - **Ask healthcare questions**: Office hours are perfect for healthcare domain questions. We expect you will need clarification.
   - **Meet regularly**: Schedule 2 to 3 team meetings per week. Divide work but review together.
   - **Document as you go**: Capture decisions and rationale as you make them rather than reconstructing at the end.