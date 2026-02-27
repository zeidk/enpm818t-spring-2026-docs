====================================================
Sample Data Generation Guide
====================================================

Once you have created your PostgreSQL schema (``schema.sql``), use the prompt
below to generate realistic synthetic data that fits **your** table structure.

.. danger::

   **NEVER use real patient data.** All data must be synthetic. Using real
   patient information, even from publicly available datasets, is prohibited.

.. important::

   **How to Use This Guide**

   1. Run your ``schema.sql`` to create all tables
   2. Export your schema definition (see instructions below)
   3. Paste the prompt below into an LLM (e.g., Claude, ChatGPT) along with your schema
   4. Review the generated SQL for correctness
   5. Load into your database


Step 1: Export Your Schema
--------------------------

Run this command to extract your table definitions:

.. code-block:: bash

   pg_dump -d healthcare_management --schema-only --no-owner --no-privileges > my_schema.sql

Alternatively, in ``psql``:

.. code-block:: psql

   \d+ patient
   \d+ provider
   -- repeat for all tables


Step 2: Generate Data
---------------------

Copy the prompt below and paste it into an LLM along with your schema
definition. Replace ``[PASTE YOUR SCHEMA HERE]`` with the output from Step 1.

.. dropdown:: Data Generation Prompt (click to expand, then copy)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   .. code-block:: text

      I have a PostgreSQL database for a Healthcare Patient Management System
      serving a 5-hospital regional network. Below is my complete schema.
      Generate realistic synthetic INSERT statements for all tables, following
      these requirements:

      IMPORTANT: All data must be entirely synthetic. Do not use any real
      patient information or real provider identities. Names, SSNs, MRNs,
      and all other identifiers must be fabricated.

      SCHEMA:
      [PASTE YOUR SCHEMA HERE]

      DATA REQUIREMENTS:

      1. Hospitals and Clinics: 5 hospitals (e.g., Regional Medical Center,
         Community Hospital, Children's Hospital, University Hospital,
         Memorial Hospital) and 10-12 outpatient clinics. Locations near
         Washington, D.C. / Maryland area.

      2. Patients: 100-120 patients with realistic age distribution
         (pediatric through geriatric). Include diverse demographics.
         Each patient gets a unique 10-digit MRN (zero-padded). SSNs
         should follow XXX-XX-XXXX format with fabricated numbers. Include
         primary and emergency contact information.

      3. Providers: 30-40 providers including physicians, nurse
         practitioners, and specialists. Each has a fabricated 10-digit
         NPI. Prescribing providers have fabricated DEA numbers (format:
         2 letters + 7 digits). Specialties: primary care, cardiology,
         orthopedics, oncology, neurology, pediatrics, psychiatry, surgery.
         Include license numbers with expiration dates.

      4. Appointments: 200-250 appointments spanning the past 6 months.
         Types: routine checkup, follow-up, procedure, consultation,
         urgent care. Status distribution: ~50% completed, ~15% scheduled
         (future), ~10% confirmed, ~5% in-progress, ~10% no-show, ~10%
         cancelled. Include realistic durations (15, 30, 45, 60 minutes).

      5. Medications (Formulary): 30-40 medications including common drugs
         from different classes: antihypertensives (lisinopril, amlodipine),
         diabetes (metformin, glipizide), pain (acetaminophen, ibuprofen),
         antibiotics (amoxicillin, azithromycin), cholesterol (atorvastatin),
         mental health (sertraline, alprazolam), and a few controlled
         substances (oxycodone Schedule II, lorazepam Schedule IV).

      6. Prescriptions: 150-175 prescriptions. Most should be "active"
         with some "completed" and "discontinued". Include a mix of
         controlled and non-controlled substances. Controlled substance
         prescriptions must have a valid prescriber DEA number. Dosages
         should be medically plausible (e.g., lisinopril 10mg daily,
         metformin 500mg twice daily). Include refill counts.

      7. Lab Orders and Results: 100-120 lab orders with 200-250 results.
         Common tests: CBC (complete blood count), BMP (basic metabolic
         panel), lipid panel, HbA1c, TSH, urinalysis. Each order can
         produce multiple results (e.g., CBC produces WBC, RBC,
         hemoglobin, hematocrit). Include reference ranges and flag
         some results as abnormal (high/low). A few should be "critical".
         Priority distribution: ~70% routine, ~20% urgent, ~10% stat.

      8. Hospital Admissions: 30-40 admissions. Types: emergency, urgent,
         elective, observation. Most should be discharged with realistic
         lengths of stay (1-14 days). Include 3-5 currently admitted
         patients (NULL discharge_date). Discharge dispositions: home,
         skilled nursing facility, rehabilitation, transfer.

      9. Insurance: Create 8-10 insurance companies (e.g., BlueCross,
         Aetna, Cigna, United, Medicare, Medicaid). Each patient should
         have at least one insurance policy. About 20% should have
         secondary insurance. Include policy numbers, group numbers,
         and copay amounts.

      10. Insurance Claims: 50-70 claims in various lifecycle stages.
          Distribution: ~30% approved, ~25% pending, ~15% submitted,
          ~10% denied, ~10% partially approved, ~10% under review.
          Include CPT codes (e.g., 99213 office visit, 99232 hospital
          visit) and ICD-10 codes matching patient conditions. Denied
          claims should have denial reason codes.

      CONSTRAINTS:
      - All foreign key references must be valid
      - All CHECK constraints in my schema must be satisfied
      - Use NULL where appropriate (optional fields, current admissions
        without discharge, pending claims without payment)
      - Dates should be realistic (appointments over last 6 months,
        provider licenses expiring 1-3 years in the future)
      - MRN, NPI, DEA, and SSN formats must be consistent

      OUTPUT FORMAT:
      - Pure SQL INSERT statements, one per table
      - Include a comment header with row counts per table
      - Order tables so that parent tables are populated before child tables
        (e.g., patient before appointment, medication before prescription)
      - Do not include any CREATE TABLE or DROP statements


Step 3: Verify Your Data
-------------------------

After loading the generated data, run these verification queries:

.. code-block:: sql

   -- Row counts
   SELECT 'patient' AS tbl, COUNT(*) FROM patient
   UNION ALL SELECT 'provider', COUNT(*) FROM provider
   UNION ALL SELECT 'appointment', COUNT(*) FROM appointment
   UNION ALL SELECT 'medication', COUNT(*) FROM medication
   UNION ALL SELECT 'prescription', COUNT(*) FROM prescription
   UNION ALL SELECT 'lab_order', COUNT(*) FROM lab_order
   UNION ALL SELECT 'lab_result', COUNT(*) FROM lab_result
   UNION ALL SELECT 'admission', COUNT(*) FROM admission
   UNION ALL SELECT 'insurance_claim', COUNT(*) FROM insurance_claim

   ORDER BY tbl;

   -- Check for orphan foreign keys (example for prescription)
   SELECT p.prescription_id
   FROM prescription p
   LEFT JOIN patient pt ON p.patient_id = pt.patient_id
   WHERE pt.patient_id IS NULL;

   -- Verify controlled substances have DEA numbers
   SELECT p.prescription_id, m.name, p.controlled_substance_schedule
   FROM prescription p
   JOIN medication m ON p.medication_id = m.medication_id
   WHERE p.controlled_substance_schedule IS NOT NULL
     AND p.prescriber_dea_number IS NULL;

   -- Verify temporal spread of appointments
   SELECT
       MIN(appointment_date) AS earliest,
       MAX(appointment_date) AS latest,
       COUNT(*) AS total
   FROM appointment;

.. tip::

   If the LLM generates data that violates a constraint, fix the specific
   rows rather than regenerating everything. Common issues include:

   - CHECK constraint violations (values outside allowed ranges)
   - Duplicate primary keys or unique values (MRN, NPI, SSN)
   - Foreign keys referencing non-existent parent rows
   - NULL in NOT NULL columns
   - Controlled substance prescriptions missing DEA numbers
   - Insurance claims with CPT/ICD-10 codes that do not match patient conditions

   You can also ask the LLM to fix specific errors by pasting the error
   message back into the conversation.
