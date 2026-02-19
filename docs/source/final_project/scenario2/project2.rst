====================================================
Group Project 2: PostgreSQL + Python Integration
====================================================

Overview
--------

Implement your GP1 design in PostgreSQL with HIPAA-compliant security controls, comprehensive audit logging, role-based access control, and a secure Python application with REST API.

**Timeline**: 6 weeks

**Weight**: 15 points (37.5% of final project)

**Team Size**: 4 students

**Builds on**: Your GP1 relational design


.. important::
   
   **What You'll Deliver**
   
   This project requires a **complete HIPAA-compliant PostgreSQL implementation** with Python integration:
   
   - 3 SQL files (schema with security controls, synthetic data, queries)
   - 5 documentation files (index strategy, query catalog, architecture, API docs, HIPAA compliance)
   - 1 Python application (config, models, repositories with audit, services, secure API)
   - 1 test suite with coverage report
   - 1 README file
   - 1 team contributions file
   
   **Submission**: Single ZIP file named ``GP2_Healthcare_Team{X}.zip``


Learning Objectives
-------------------

By completing this group project, you will be able to:

- Translate healthcare designs into HIPAA-compliant PostgreSQL schemas
- Implement role-based access control with database roles
- Create comprehensive audit triggers for all PHI access
- Generate realistic synthetic healthcare data (NEVER real patient data!)
- Write clinical, financial, and operational SQL queries
- Integrate PostgreSQL with Python using psycopg2
- Build a secure REST API with access reason tracking
- Write security-focused tests (>70% coverage)


Part 1: HIPAA-Compliant Schema Implementation
----------------------------------------------

**Objective**: Transform your GP1 design into a working PostgreSQL database with security controls.

.. dropdown:: 📋 Task 1.1: Schema with Security Controls (3 points)
   :class-container: sd-border-primary
   :open:

   Create ``schema.sql`` with:
   
   - **Database setup**: Extensions, schemas
   - **Database roles**: physician, nurse, billing_staff, auditor
   - **Custom types**: ENUMs for constrained healthcare values
   - **All tables**: Complete with all columns from GP1
   - **Primary keys**: All defined correctly
   - **Foreign keys**: With ON DELETE/UPDATE rules from GP1
   - **Check constraints**: All 20+ business rules
   - **NOT NULL constraints**: All mandatory clinical fields
   - **UNIQUE constraints**: All candidate keys (MRN, NPI, DEA)
   - **Indexes**: Strategic indexes for clinical query patterns
   - **Audit triggers**: Automatic logging for all PHI table access
   - **Timestamp triggers**: Automatic updated_at for all tables
   
   **Role-Based Access Control**:
   
   .. code-block:: sql
   
      -- Create roles
      CREATE ROLE physician;
      CREATE ROLE nurse;
      CREATE ROLE billing_staff;
      CREATE ROLE auditor;
      
      -- Physician: Full PHI access
      GRANT SELECT, INSERT, UPDATE ON patient TO physician;
      GRANT SELECT, INSERT, UPDATE ON prescription TO physician;
      GRANT SELECT, INSERT, UPDATE ON lab_order TO physician;
      
      -- Billing: Limited PHI (name, MRN, insurance only)
      GRANT SELECT (patient_id, mrn, first_name, last_name)
        ON patient TO billing_staff;
      GRANT SELECT, INSERT, UPDATE ON insurance_claim TO billing_staff;
      
      -- Auditor: Read-only de-identified access
      GRANT SELECT ON audit_log TO auditor;
   
   **Audit Trigger Example**:
   
   .. code-block:: plpgsql
   
      CREATE OR REPLACE FUNCTION log_phi_access()
      RETURNS TRIGGER AS $$
      BEGIN
        INSERT INTO audit_log (
          user_id, user_role, action, table_name,
          record_id, phi_accessed, access_reason,
          ip_address, timestamp
        ) VALUES (
          current_setting('app.current_user_id')::INTEGER,
          current_setting('app.current_user_role'),
          TG_OP, TG_TABLE_NAME,
          COALESCE(NEW.patient_id, OLD.patient_id),
          TRUE,
          current_setting('app.access_reason'),
          inet_client_addr(),
          NOW()
        );
        RETURN NEW;
      END;
      $$ LANGUAGE plpgsql;
      
      CREATE TRIGGER audit_patient_access
      AFTER INSERT OR UPDATE OR DELETE ON patient
      FOR EACH ROW EXECUTE FUNCTION log_phi_access();
   
   **File to create**: ``postgresql/schema.sql``

.. dropdown:: 📋 Task 1.2: Index Strategy
   :class-container: sd-border-primary

   For each index, document:
   
   - **Purpose**: What clinical queries does this speed up?
   - **Type**: B-tree (default), GIN (full-text), partial
   - **Cost**: Impact on write performance
   - **Justification**: Why benefits outweigh costs
   
   **Example Entry**:
   
   .. code-block:: text
   
      Index: idx_prescription_patient_active
      Table: prescription
      Columns: (patient_id) WHERE status = 'active'
      Type: Partial B-tree
      
      Purpose: Speeds up "current medication list" query
      Query Pattern: SELECT * FROM prescription
                     WHERE patient_id = ? AND status = 'active'
      
      Justification:
      - This query runs at every appointment and before procedures
      - Active prescriptions are a small fraction of all prescriptions
      - Partial index is much smaller than full index
      - Critical for drug interaction checking performance
   
   **File to create**: ``docs/index_strategy.md``

.. dropdown:: 📋 Task 1.3: Synthetic Data Generation (2 points)
   :class-container: sd-border-primary

   Create ``data.sql`` with **synthetic data only** (NEVER real patient data!).
   
   **Minimum data volumes**:
   
   - 200+ patients across the network
   - 50+ providers (physicians, nurses, specialists)
   - 500+ appointments (various statuses and types)
   - 300+ prescriptions (including controlled substances)
   - 200+ lab orders with 500+ lab results
   - 50+ hospital admissions with discharge info
   - 100+ insurance claims (various lifecycle stages)
   - 50+ medications in formulary
   - 5 hospitals and 20 clinic locations
   - 1000+ audit log entries
   
   **Realistic Clinical Patterns**:
   
   - Age distribution (pediatric through geriatric)
   - Common diagnosis codes (ICD-10) for conditions
   - Realistic medication combinations (some with interactions)
   - Appointment no-show rates (~15-20%)
   - Insurance claim denial rates (~5-10%)
   - Mix of controlled and non-controlled prescriptions
   - Critical lab values flagged appropriately
   
   **Use Python Faker library** for name/address generation.
   
   **File to create**: ``postgresql/data.sql``


Part 2: Clinical SQL Queries
-----------------------------

**Objective**: Write 10+ queries demonstrating clinical, financial, and operational mastery.

.. dropdown:: 📋 Clinical Queries (4 minimum)
   :class-container: sd-border-primary
   :open:

   **Patient Care Coordination**: Complete patient summary for appointment
   
   *"For patient MRN X arriving for an appointment, show demographics, active medications, recent lab results, and upcoming appointments."*
   
   **Medication Safety**: Polypharmacy alerts
   
   *"Find all patients with 5+ active prescriptions (polypharmacy risk) along with their prescribing providers."*
   
   **Quality Metrics**: 30-day readmission rates
   
   *"Calculate 30-day readmission rates by diagnosis, identifying patients readmitted within 30 days of discharge."*
   
   **Lab Efficiency**: Turnaround time analysis
   
   *"Calculate average lab result turnaround time by test type, flagging tests exceeding target times."*

.. dropdown:: 📋 Financial Queries (3 minimum)
   :class-container: sd-border-primary

   **Claim Denials**: Analysis by reason and payer
   
   *"Show claim denial rates by insurance company and denial reason, with total denied amounts."*
   
   **Outstanding Balances**: Accounts receivable aging
   
   *"Generate an aging report showing outstanding patient balances in 30/60/90/120+ day buckets."*
   
   **Revenue Analytics**: Payment trends and collection rates
   
   *"Calculate monthly revenue, payment rates, and average days to payment by insurance company."*

.. dropdown:: 📋 Operational Queries (3 minimum)
   :class-container: sd-border-primary

   **Provider Productivity**: Appointments and no-show rates
   
   *"Show appointment counts, no-show rates, and average patients per day by provider."*
   
   **Appointment Scheduling**: Open slot identification
   
   *"Find available appointment slots for a given provider in the next 2 weeks."*
   
   **Controlled Substances**: DEA audit monitoring
   
   *"Report all Schedule II controlled substance prescriptions by provider, required for DEA audits."*

.. dropdown:: 📋 Query Documentation Template
   :class-container: sd-border-primary

   Use this format for **every query** in ``queries.sql``:
   
   .. code-block:: sql
   
      -- Query #X: [Title]
      -- Clinical/Financial/Operational Context: [Why this matters]
      -- Tables Used: [List all tables]
      -- Complexity Features: [JOINs, CTEs, window functions used]
      -- HIPAA Note: [What PHI is accessed and why]
      -- Performance Notes: [Index usage, execution time]
      
      [YOUR SQL QUERY]
      
      -- Expected Output: [Description of result columns]
      -- Sample Results: [First 3 rows with synthetic data]
   
   Include EXPLAIN ANALYZE output for **at least 5 queries**.
   
   **File to create**: ``postgresql/queries.sql`` and ``docs/query_catalog.md``


Part 3: Secure Python Application
-----------------------------------

**Objective**: Build a layered Python application with HIPAA-compliant security.

.. dropdown:: 📋 Task 3.1: Application Architecture (5 points)
   :class-container: sd-border-primary
   :open:

   .. code-block:: text
   
      traffic-management/
      ├── requirements.txt
      ├── .env.example
      ├── config/
      │   └── database.py          # Connection pooling
      ├── models/
      │   ├── patient.py           # Dataclasses
      │   └── [other models].py
      ├── repositories/
      │   ├── base_repository.py   # With audit logging
      │   ├── patient_repo.py      # CRUD with PHI protection
      │   └── [other repos].py
      ├── services/
      │   ├── audit_service.py     # HIPAA audit logging
      │   ├── patient_service.py   # Business logic
      │   └── [other services].py
      ├── api/
      │   └── endpoints.py         # FastAPI routes with auth
      └── tests/

.. dropdown:: 📋 Audit Service Implementation
   :class-container: sd-border-primary

   **Every PHI access must be logged**:
   
   .. code-block:: python
   
      class AuditService:
          def log_access(self, user_id, user_role, action,
                        resource, resource_id, phi_accessed,
                        access_reason, success):
              """Log PHI access to audit_log table.
              CRITICAL: This must never fail silently."""
              try:
                  conn = self.pool.getconn()
                  with conn.cursor() as cur:
                      cur.execute("""
                          INSERT INTO audit_log
                          (user_id, user_role, action, table_name,
                           record_id, phi_accessed, access_reason,
                           success, timestamp)
                          VALUES (%s, %s, %s, %s, %s, %s, %s, %s, NOW())
                      """, (user_id, user_role, action, resource,
                            resource_id, phi_accessed,
                            access_reason, success))
                  conn.commit()
              finally:
                  self.pool.putconn(conn)

.. dropdown:: 📋 Repository with Audit
   :class-container: sd-border-primary

   **All repositories must integrate audit logging**:
   
   .. code-block:: python
   
      class PatientRepository:
          def __init__(self, pool, audit_service):
              self.pool = pool
              self.audit = audit_service
          
          def find_by_id(self, patient_id, user_id,
                        user_role, access_reason):
              """Retrieve patient with mandatory audit logging."""
              # Check role permissions
              if user_role == 'billing_staff':
                  columns = "patient_id, mrn, first_name, last_name"
              else:
                  columns = "*"
              
              conn = self.pool.getconn()
              try:
                  with conn.cursor() as cur:
                      cur.execute(
                          f"SELECT {columns} FROM patient WHERE patient_id = %s",
                          (patient_id,)
                      )
                      row = cur.fetchone()
                  
                  # Log access (success or failure)
                  self.audit.log_access(
                      user_id=user_id, user_role=user_role,
                      action="SELECT", resource="patient",
                      resource_id=patient_id, phi_accessed=True,
                      access_reason=access_reason,
                      success=row is not None
                  )
                  
                  return Patient.from_row(row) if row else None
              finally:
                  self.pool.putconn(conn)

.. dropdown:: 📋 Task 3.2: Secure REST API (2 points)
   :class-container: sd-border-primary

   Implement **at least 8 endpoints** with authentication and audit:
   
   **Clinical Endpoints** (3 minimum):
   
   - ``GET /patients/{id}`` - Retrieve patient (with access reason header)
   - ``GET /patients/{id}/medications`` - Active medication list
   - ``GET /patients/{id}/lab-results`` - Recent lab results
   
   **Financial Endpoints** (2 minimum):
   
   - ``GET /claims/denials`` - Claim denial analytics
   - ``GET /billing/aging`` - Accounts receivable aging
   
   **Operational Endpoints** (2 minimum):
   
   - ``GET /providers/{id}/productivity`` - Provider metrics
   - ``GET /controlled-substances/report`` - DEA audit report
   
   **Audit Endpoint** (1 minimum):
   
   - ``GET /audit/patient/{id}`` - PHI access history for patient
   
   **HIPAA Requirement**: Every endpoint accessing PHI requires:
   
   .. code-block:: python
   
      @app.get("/api/patients/{patient_id}")
      async def get_patient(
          patient_id: int,
          access_reason: str = Header(..., alias="X-Access-Reason"),
          user = Depends(get_current_user)
      ):
          # access_reason is HIPAA requirement
          # Must document WHY this data is being accessed
          return patient_service.get_patient(
              patient_id, user.id, user.role, access_reason
          )
   
   **File to create**: ``docs/api_documentation.md``


Part 4: Testing
---------------

**Objective**: Write security-focused automated tests.

.. dropdown:: 📋 Task 4.1: Test Categories (integrated into score)
   :class-container: sd-border-primary
   :open:

   **Security Tests** (critical):
   
   - Unauthorized access denied (billing staff cannot see full patient record)
   - Role-based field filtering works correctly
   - Audit logs created for all PHI access
   - Failed access attempts logged
   - Access reason validation (empty reason rejected)
   
   **Repository Tests**:
   
   - CRUD operations work correctly
   - Clinical queries return expected results
   - Error handling (constraint violations, not found)
   
   **API Tests**:
   
   - Endpoints return correct status codes
   - Missing access reason returns 400
   - Response format matches specification
   - Error responses appropriate

**Requirements**: Minimum 70% code coverage


Submission Requirements
------------------------

.. important::
   
   **Single ZIP File Submission**
   
   Submit **ONE** ZIP file to Canvas:
   
   ``GP2_Healthcare_Team{X}.zip``
   
   Replace ``{X}`` with your team number (e.g., ``GP2_Healthcare_Team03.zip``)


Folder Structure
----------------

.. code-block:: text

   GP2_Healthcare_Team{X}/
   ├── postgresql/
   │   ├── schema.sql
   │   ├── data.sql
   │   └── queries.sql
   ├── src/
   │   ├── config/
   │   │   └── database.py
   │   ├── models/
   │   │   ├── patient.py
   │   │   └── [other models].py
   │   ├── repositories/
   │   │   ├── base_repository.py
   │   │   ├── patient_repo.py
   │   │   └── [other repos].py
   │   ├── services/
   │   │   ├── audit_service.py
   │   │   ├── patient_service.py
   │   │   └── [other services].py
   │   └── api/
   │       └── endpoints.py
   ├── tests/
   │   ├── test_security.py
   │   ├── test_repositories.py
   │   ├── test_services.py
   │   └── test_api.py
   ├── docs/
   │   ├── index_strategy.md
   │   ├── query_catalog.md
   │   ├── architecture.md
   │   ├── api_documentation.md
   │   └── hipaa_compliance.md
   ├── requirements.txt
   ├── .env.example
   ├── README.md
   └── team_contributions.md


Required Files by Task
-----------------------

.. dropdown:: 📄 Part 1: HIPAA-Compliant Schema
   :class-container: sd-border-info

   **SQL Files** (3 files):
   
   - ``postgresql/schema.sql`` - DDL with roles, audit triggers, constraints
   - ``postgresql/data.sql`` - Synthetic clinical data
   - ``postgresql/queries.sql`` - 10+ documented clinical queries
   
   **Documentation** (2 files):
   
   - ``docs/index_strategy.md`` - Index justifications
   - ``docs/query_catalog.md`` - Query summaries with EXPLAIN ANALYZE

.. dropdown:: 📄 Part 3: Secure Python Application
   :class-container: sd-border-info

   **Application** (full src/ directory):
   
   - ``src/config/database.py`` - Connection pooling
   - ``src/models/*.py`` - Dataclass models
   - ``src/repositories/*.py`` - CRUD with audit integration
   - ``src/services/audit_service.py`` - HIPAA audit logging
   - ``src/services/*.py`` - Business logic
   - ``src/api/endpoints.py`` - Secure FastAPI routes
   
   **Documentation** (3 files):
   
   - ``docs/architecture.md`` - Application architecture
   - ``docs/api_documentation.md`` - API endpoints with security notes
   - ``docs/hipaa_compliance.md`` - HIPAA compliance documentation

.. dropdown:: 📄 Part 4: Testing + Supporting Files
   :class-container: sd-border-info

   **Tests** (4+ files):
   
   - ``tests/test_security.py`` - RBAC and audit tests
   - ``tests/test_repositories.py``
   - ``tests/test_services.py``
   - ``tests/test_api.py``
   
   **Supporting Files** (3 files):
   
   - ``requirements.txt`` - Python dependencies
   - ``README.md`` - Project overview with setup guide
   - ``team_contributions.md`` - Individual contributions


README.md Template
------------------

.. code-block:: markdown

   # GP2: Healthcare Patient Management - PostgreSQL + Python
   
   **Team Number**: [Your team number]
   
   **Scenario**: Healthcare Patient Management Platform
   
   ## Team Members
   
   - [Name 1] - [Email] - [Contribution %]
   - [Name 2] - [Email] - [Contribution %]
   - [Name 3] - [Email] - [Contribution %]
   - [Name 4] - [Email] - [Contribution %]
   
   ## Project Overview
   
   [2-3 sentence description of your HIPAA-compliant implementation]
   
   ## Setup Instructions
   
   ### Prerequisites
   
   - PostgreSQL 18
   - Python 3.10+
   
   ### Database Setup
   
   ```bash
   createdb healthcare_management
   psql -d healthcare_management -f postgresql/schema.sql
   psql -d healthcare_management -f postgresql/data.sql
   ```
   
   ### Application Setup
   
   ```bash
   pip install -r requirements.txt
   cp .env.example .env
   # Edit .env with database credentials
   uvicorn src.api.endpoints:app --reload
   ```
   
   ### Running Tests
   
   ```bash
   pytest tests/ --cov=src --cov-report=html
   ```
   
   ## HIPAA Compliance Summary
   
   - **Roles**: physician, nurse, billing_staff, auditor
   - **Audit**: All PHI access logged with access reason
   - **RBAC**: Field-level filtering by role
   - **Data**: 100% synthetic (Faker library)
   
   ## Notes for Graders
   
   [Any special notes, clarifications, or highlights]


Team Contributions Template
----------------------------

.. code-block:: markdown

   # Team Contributions - GP2
   
   ## [Member 1 Name]
   
   **Tasks Completed**:
   
   - Created schema.sql with roles and audit triggers
   - Implemented RBAC with column-level security
   - Wrote HIPAA compliance documentation
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 2 Name]
   
   **Tasks Completed**:
   
   - Generated synthetic data (data.sql) using Faker
   - Wrote clinical queries 1-5
   - Created query catalog with EXPLAIN ANALYZE
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 3 Name]
   
   **Tasks Completed**:
   
   - Built Python application (models, repositories with audit, services)
   - Implemented AuditService
   - Wrote architecture documentation
   
   **Hours Contributed**: [X hours]
   
   **Contribution Percentage**: 25%
   
   ## [Member 4 Name]
   
   **Tasks Completed**:
   
   - Built secure REST API with FastAPI
   - Wrote all tests including security tests (70%+ coverage)
   - Created API documentation and README
   
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

   **SQL Files** (3 files):
   
   - [ ] schema.sql creates roles (physician, nurse, billing_staff, auditor)
   - [ ] schema.sql includes audit triggers for all PHI tables
   - [ ] schema.sql includes all 20+ constraints from GP1
   - [ ] data.sql contains ONLY synthetic data (no real patient data!)
   - [ ] data.sql meets minimum volume requirements (200+ patients, etc.)
   - [ ] queries.sql contains 10+ queries with documentation headers
   
   **Python Application**:
   
   - [ ] AuditService logs all PHI access
   - [ ] Repositories integrate audit logging
   - [ ] Role-based field filtering works (billing sees limited PHI)
   - [ ] 8+ API endpoints with access reason header
   - [ ] FastAPI auto-docs accessible at ``/docs``
   
   **Tests**:
   
   - [ ] Security tests verify RBAC and audit logging
   - [ ] Coverage report shows 70%+ coverage
   
   **Documentation** (5 files):
   
   - [ ] Index strategy with clinical justifications
   - [ ] Query catalog with EXPLAIN ANALYZE for 5+ queries
   - [ ] Architecture overview with security layers
   - [ ] API documentation with HIPAA security notes
   - [ ] HIPAA compliance documentation
   
   **Quality Checks**:
   
   - [ ] ``schema.sql`` runs without errors on fresh database
   - [ ] ``data.sql`` loads without constraint violations
   - [ ] Contributions sum to 100%
   - [ ] ZIP file named correctly: ``GP2_Healthcare_Team{X}.zip``


Common Mistakes to Avoid
-------------------------

.. danger::
   
   **Frequent Submission Errors**
   
   Learn from past teams' mistakes:
   
   ❌ **Using real patient data** - NEVER. Always use Faker or manual synthetic data
   
   ❌ **Missing audit triggers** - Every PHI table needs audit logging
   
   ❌ **No access reason tracking** - HIPAA requires documenting WHY data was accessed
   
   ❌ **Hardcoded credentials** - Database passwords in source code instead of .env
   
   ❌ **Same access for all roles** - Billing staff should NOT see full patient records
   
   ❌ **Audit failures silently ignored** - Audit logging must never fail silently
   
   ❌ **No security tests** - Must verify RBAC and audit logging work correctly
   
   ❌ **Clinical queries without context** - Each query needs clinical/business justification


Grading Rubric
--------------

.. list-table::
   :header-rows: 1
   :widths: 30 10 60
   :class: compact-table

   * - Component
     - Points
     - Criteria
   * - **Part 1: HIPAA Schema**
     - 3
     - Security controls and roles (1pt); Audit triggers for PHI tables (1pt); Constraints and indexes (1pt)
   * - **Part 1: Synthetic Data**
     - 2
     - Realistic clinical patterns (1pt); Adequate volume and variety (1pt)
   * - **Part 2: SQL Queries**
     - 5
     - 10+ queries across clinical/financial/operational (2pts); Correct results (1.5pts); Documentation and EXPLAIN ANALYZE (1.5pts)
   * - **Part 3: Secure Python App**
     - 3
     - Audit service integration (1pt); RBAC in repositories (1pt); Clean layered architecture (1pt)
   * - **Part 3: REST API**
     - 2
     - 8+ secure endpoints (1pt); Access reason tracking and documentation (1pt)
   * - **Total**
     - **15**
     - 


Tips for Success
----------------

.. tip::
   
   **How to Excel in GP2**
   
   - **Start with security** - Implement roles and audit triggers before writing application code. Security is not an afterthought.
   - **Test queries in psql first** - Write and debug SQL interactively before embedding in Python.
   - **Use Faker creatively** - Generate realistic clinical data with appropriate age distributions, diagnosis codes, and medication combinations.
   - **Write security tests first** - Verify RBAC and audit logging before building more features.
   - **Think like a clinician** - For each query, ask "Why would a doctor/nurse/billing staff need this?"
   - **Use office hours** - Bring your schema for security review. Ask about HIPAA compliance strategies.


Next Steps
----------

After completing GP2, you will:

- Receive feedback on your HIPAA compliance implementation
- Identify clinical documentation that needs flexible schemas
- Begin GP3: Adding MongoDB for clinical notes, care plans, and surveys
- Design document schemas for variable-structure clinical data

.. note::
   
   **Your GP2 implementation is the secure core** of the complete system. GP3 (MongoDB) and GP4 (Neo4j + deployment) extend this HIPAA-compliant foundation.
   
   Start thinking: Which clinical documents have variable structures that would benefit from a document database?