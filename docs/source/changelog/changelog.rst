====================================================
Changelog
====================================================

All notable changes to the ENPM818T Spring 2026 course documentation are recorded here.

.. dropdown:: v3.2.0 -- Right-Side TOC Collapse Behavior (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: conf.py

   - Changed ``show_toc_level`` from ``2`` to ``1`` in ``html_theme_options``
     so the right-hand table of contents starts collapsed at H1 sections and
     expands to reveal H2 subsections on scroll or click, matching the
     enpm818z documentation style.


.. dropdown:: v3.1.0 -- Lecture 8: JOINs, Query Execution, and Indexing (2026-04-01)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: lectures/lecture8/ (new)

   Six new RST files created from the Marp markdown lecture and supplemented
   with content from the prior-year LaTeX slide deck:

   - **l8_index.rst**: overview, learning objectives, toctree, next steps.
   - **l8_lecture.rst**: full lecture covering Cartesian products, relational
     algebra (with :math:`\sigma`, :math:`\pi`, :math:`\times`,
     :math:`\bowtie` symbols), all SQL join types (``INNER``, ``LEFT``,
     ``RIGHT``, ``FULL OUTER``, ``CROSS``, self-join, ``USING`` /
     ``NATURAL``, semi/anti via ``EXISTS`` / ``NOT EXISTS``, ``LATERAL``),
     ``ON`` vs ``WHERE`` semantics, physical join strategies (nested loop,
     hash, merge), ``EXPLAIN (ANALYZE, BUFFERS)`` interpretation, Big O
     analysis of join algorithms, disk and memory architecture (heap pages,
     ``shared_buffers``, ``work_mem``), B+ tree indexing, composite indexes,
     and PostgreSQL tuning tips. Includes business-domain result tables
     (CUSTOMERS / ORDERS) from the LaTeX slide deck for ``LEFT JOIN`` and
     ``FULL OUTER JOIN``.
   - **l8_exercises.rst**: six exercises -- Cartesian product row counts,
     choosing join types, join result predictor (``ON`` vs ``WHERE``),
     join-algorithm-to-scenario matching, index design (take-home), and
     self-join hierarchy (take-home). All include solutions.
   - **l8_quiz.rst**: 30 questions (18 multiple choice, 8 true/false,
     4 essay) covering joins, ``EXPLAIN``, Big O, indexing, and storage
     architecture.
   - **l8_references.rst**: PostgreSQL official docs (table expressions,
     ``EXPLAIN``, indexes, planner/optimizer), textbook references
     (Silberschatz, Elmasri & Navathe), and additional resources
     (Use The Index Luke, pgMustard, PostgreSQL wiki).
   - **l8_cheat_sheet.rst**: condensed reference tables for join types,
     ``ON`` vs ``WHERE`` rules, semi/anti patterns, physical join
     strategies with Big O, ``EXPLAIN`` checklist, index types, B+ tree
     rules, and tuning checklist.

   .. rubric:: lectures/index.rst

   - Added L8 row to the schedule table with topic "JOINs, Query Execution,
     and Indexing" and key concepts.
   - Added ``lecture8/l8_index`` to the ``.. toctree::``.


.. dropdown:: v3.0.0 -- L6 Lecture Updated for DDL v4.0 Slides (2026-03-28)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: lecture6/lecture.rst

   Six targeted additions to bring the RST document into full alignment
   with the v4.0 Beamer slide deck.

   - **Prerequisites promoted to top-level section**: the DataGrip
     four-step setup block (create database, point console, select schema,
     run script) was previously a dropdown buried inside "From Logical to
     Physical"; it is now a standalone ``====`` section at the top of the
     file, matching the slide deck hierarchy. The duplicate
     "Setting Up in DataGrip" dropdown was removed.
   - **University schema figure placeholder added**: light/dark/LaTeX
     variants added below the "From Logical to Physical" intro using the
     standard ``only-light`` / ``only-dark`` / ``only:: latex`` pattern,
     pointing to ``/_static/images/L6/university_full_light.png`` and
     ``university_full_dark.png``.
   - **NO ACTION vs. RESTRICT comparison table added**: the three-row
     table (Check timing / Deferrable / Blocks delete) from the slides
     now appears inline in the FOREIGN KEY section, with accompanying
     prose explaining the key difference (``NO ACTION`` defers to
     end-of-statement and is compatible with ``DEFERRABLE``;
     ``RESTRICT`` checks immediately and can never be deferred).
   - **Person column nullability/uniqueness reference table added**: the
     ``NULL ok?`` / ``Duplicate ok?`` table covering all eight columns
     of the ``person`` table (``person_id``, ``first_name``,
     ``last_name``, ``middle_name``, ``date_of_birth``, ``street``,
     ``state``, ``zip``) now appears in the NOT NULL and UNIQUE section,
     with the ``CREATE TABLE`` statement for context.
   - **Deferability-by-constraint-type table restructured**: the old
     malformed four-column table (with a spurious empty column) replaced
     with a clean three-column table (Constraint type / Deferrable? /
     Why) covering ``FOREIGN KEY``, ``UNIQUE``, ``PRIMARY KEY``,
     ``NOT NULL``, and ``CHECK``. The three-deferral-modes comparison
     table (Mode 1 / Mode 2 / Default: Check timing, Always deferred,
     Per-txn opt-in, Overridable) added separately as a
     ``.. rubric::``.
   - **Exclusive-arc data table added inline**: the five-row table
     showing valid and rejected ``vehicle_owner`` rows with arc sum
     annotations (arc sum = 1 valid; arc sum = 2 and arc sum = 0
     rejected) now appears before Demo 16, matching the "Exclusive-Arc
     in Data" slide frame.


.. dropdown:: v2.7.0 -- Lectures Index Updated with L7 Row (2026-03-28)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: lectures/index.rst

   - Added L7 row to the schedule table: topic "DML, Transactions, and
     Python" with key concepts ``INSERT``, ``UPDATE``, ``DELETE``,
     upsert with ``ON CONFLICT``, ACID properties, transaction lifecycle
     (``BEGIN`` / ``COMMIT`` / ``ROLLBACK``), savepoints, isolation
     levels, psycopg3 (connection management, parameterized queries,
     server-side cursors, connection pooling), and loading data from
     CSV with Python.
   - Added ``lecture7/index`` to the ``.. toctree::`` directive.


.. dropdown:: v2.6.0 -- GP2 psycopg3 Migration and Scope Adjustment (2026-03-23)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: scenario1/project2.rst

   **psycopg2 → psycopg3 migration**

   - Replaced ``psycopg2-binary`` with ``psycopg[binary]`` and added ``psycopg-pool`` in all requirements references
   - Replaced ``psycopg2.pool.SimpleConnectionPool`` with ``psycopg_pool.ConnectionPool`` throughout
   - Connection management example rewritten: removed manual ``getconn()``/``putconn()``/``@contextmanager`` pattern; replaced with ``pool.connection()`` context manager (psycopg3 handles commit/rollback automatically)
   - Pool parameters changed from ``minconn``/``maxconn`` to ``min_size``/``max_size`` with ``open=True``
   - Error handling updated from ``psycopg2.OperationalError`` to ``psycopg.OperationalError``
   - Shutdown method changed from ``cls._pool.closeall()`` to ``cls._pool.close()``
   - Repository example updated: plain ``conn.cursor()`` replaced with ``conn.cursor(row_factory=dict_row)`` using ``from psycopg.rows import dict_row``
   - All ``import psycopg2`` references changed to ``import psycopg``
   - Added ``_conninfo()`` classmethod to ``DatabaseConfig`` that builds connection string from individual env vars (matches L7 lecture)
   - Submission checklist updated: "Connection pooling implemented with context manager" → "Connection pooling implemented with psycopg3 pool"
   - Learning objectives updated: "using psycopg2" → "using psycopg3"

   **PostGIS removed**

   - Removed PostGIS extension, geography columns, and GIST index from Task 1.1 schema requirements
   - Removed "PostGIS Geospatial (2 queries minimum)" category from Part 2 SQL queries
   - Total minimum query count reduced from 8+ to **6+** (3 JOINs + 2 aggregates + 1 subquery)
   - Removed geospatial CLI menu option from Task 3.4
   - Removed "Geographic coordinates form a realistic grid" from data quality checks
   - Removed "PostGIS integration with triggers and ENUMs" from grading rubric; replaced with "triggers and ENUMs"
   - Removed PostGIS from README prerequisites and submission checklist
   - Learning objectives updated: removed "and geospatial queries"

   **Scope reduction: 5 → 3 full CRUD tables**

   - Full CRUD repositories + CLI required for **3 tables**: ``INTERSECTION``, ``INCIDENT``, ``SENSOR``
   - Read-only repositories (``find_by_id`` and ``find_all`` only) required for **2 tables**: ``TRAFFIC_SIGNAL``, ``ROAD_SEGMENT``
   - Supporting tables unchanged: ``MAINTENANCE_TASK``, ``MAINTENANCE_CREW``
   - Task 3.3 Repository Pattern updated to distinguish full CRUD (3 tables) from read-only (2 tables)
   - Submission checklist and grading rubric updated accordingly

   **CLI minimum reduced from 6 to 4**

   - Minimum menu options changed from 6 to **4**: CRUD (1), Complex queries (1), Analytics (1), team's choice (1)
   - Example interaction updated to show 5 options (4 + Exit)
   - Grading rubric updated: "6+ working menu options" → "4+ working menu options"

   .. rubric:: scenario2/project2.rst

   **psycopg2 → psycopg3 migration**

   - Same psycopg3 migration changes as scenario1 (imports, pool class, connection management, repository cursors, requirements, checklist, learning objectives)

   **Scope reduction: 5 → 3 full CRUD tables**

   - Full CRUD repositories + CLI required for **3 tables**: ``PATIENT``, ``APPOINTMENT``, ``PRESCRIPTION``
   - Read-only repositories (``find_by_id`` and ``find_all`` only) required for **2 tables**: ``PROVIDER``, ``PATIENT_INSURANCE``
   - Supporting tables unchanged: ``MEDICATION``, ``FACILITY``/``LOCATION``
   - Task 3.3 Repository Pattern updated to distinguish full CRUD (3 tables) from read-only (2 tables)
   - Submission checklist and grading rubric updated accordingly

   **CLI minimum reduced from 6 to 4**

   - Minimum menu options changed from 6 to **4**: Clinical (1), Provider (1), Analytics (1), team's choice (1)
   - Example interaction updated to show 5 options (4 + Exit)
   - Grading rubric updated: "6+ working menu options" → "4+ working menu options"


.. dropdown:: v2.5.0 -- GP1 and GP2 Scope Reduction (2026-03-22)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: scenario1/project1.rst and scenario2/project1.rst

   - Added ``.. important::`` block titled **Revised Scope for the Design Report** in the Deliverable 3 / Task 2 section of both scenario files
   - Report scope for Entity Catalog, Relationship Documentation/Analysis, and Normalization Proofs reduced from all entities to **five named tables per scenario**
   - Scenario 1 focus tables: ``INTERSECTION``, ``TRAFFIC_SIGNAL``, ``SENSOR``, ``ROAD_SEGMENT``, ``INCIDENT``
   - Scenario 2 focus tables: ``PATIENT``, ``PROVIDER``, ``PATIENT_INSURANCE``, ``APPOINTMENT``, ``PRESCRIPTION``
   - ER diagram scope unchanged: both diagrams must still cover all eight (Scenario 1) and seven (Scenario 2) business areas
   - Submission checklists updated to reference "five required tables" in place of "all entities"
   - Grading rubric wording updated accordingly in both files (Entity Catalog and Normalization rows)
   - Relationship Documentation/Analysis tables updated: starter rows now illustrate only relationships among the five required tables; open-ended continuation row retained

   .. rubric:: scenario1/project2.rst

   - Added ``.. important::`` block titled **Revised Scope for GP2** immediately after the Learning Objectives section
   - ``schema.sql`` and ``data.sql`` scope unchanged: all GP1 tables must be implemented (FK integrity requires it)
   - Full Python repository pattern (CRUD + custom queries) and CLI menu coverage required only for the five core tables: ``INTERSECTION``, ``TRAFFIC_SIGNAL``, ``SENSOR``, ``ROAD_SEGMENT``, ``INCIDENT``
   - Two supporting tables added as explicit requirements because queries and CLI features depend on them: ``MAINTENANCE_TASK`` and ``MAINTENANCE_CREW``
   - All remaining GP1 tables (``EMERGENCY_ROUTE``, ``PARKING_FACILITY``, ``WEATHER_STATION``, ``TRAFFIC_CONTROL_ZONE``) must appear in SQL files but do not require Python repositories or CLI menu options
   - Minimum data volumes revised: core table minimums retained; removed volumes for tables outside the revised scope; added note that remaining tables need representative rows for FK validity
   - SQL query examples revised: geospatial example updated from "5 nearest emergency facilities" to "5 nearest intersections" to stay within scope
   - models/ and repositories/ layer descriptions updated to name the five core tables and note that MAINTENANCE_TASK / MAINTENANCE_CREW need only partial or read-only repositories
   - CLI analytics menu option expanded to mention open maintenance tasks as a metric
   - Folder structure comments updated: ``schema.sql`` and ``data.sql`` annotated as covering all tables; models and repositories annotated as covering core tables
   - Submission checklist updated: "Repository pattern with CRUD for the five core tables" replaces "Repository pattern with CRUD for major entities"
   - Grading rubric updated: "Complete DDL for all tables" and "CRUD for core tables" wording clarified

   .. rubric:: scenario2/project2.rst

   - Added ``.. important::`` block titled **Revised Scope for GP2** immediately after the Learning Objectives section
   - ``schema.sql`` and ``data.sql`` scope unchanged: all GP1 tables must be implemented
   - Full Python repository pattern and CLI menu coverage required only for the five core tables: ``PATIENT``, ``PROVIDER``, ``PATIENT_INSURANCE``, ``APPOINTMENT``, ``PRESCRIPTION``
   - Two supporting tables added as explicit requirements because of FK dependencies and query coverage: ``MEDICATION`` (referenced by ``PRESCRIPTION``) and ``FACILITY`` / ``LOCATION`` (referenced by ``APPOINTMENT``)
   - All remaining GP1 tables (``LAB_ORDER``, ``LAB_RESULT``, ``ADMISSION``, ``INSURANCE_CLAIM``) must appear in SQL files but do not require Python repositories or CLI menu options
   - Minimum data volumes revised: core table minimums retained (100+ patients, 30+ providers, 100+ insurance records, 200+ appointments, 150+ prescriptions, 30+ medications, 5 hospitals + 10+ locations); removed separate volumes for lab orders, admissions, claims
   - Clinical queries revised: "patient care coordination" query simplified from "demographics + active medications + recent lab results" to "demographics + insurance coverage + active prescriptions"; readmission and claim denial queries replaced with queries drawable from core tables (provider workload, insurance coverage summary, prescription costs, appointment status breakdown)
   - Financial queries revised: "claim denial analytics" and "aging report" replaced with "insurance coverage summary" and "prescription costs by patient" to avoid requiring ``INSURANCE_CLAIM``
   - models/ and repositories/ layer descriptions updated to name the five core tables and note that MEDICATION / FACILITY need only partial or read-only repositories
   - CLI menu revised: "claim denial analytics" and "accounts receivable aging" replaced with "look up provider by NPI" and "show provider appointments"; financial menu category replaced with provider category to align with reduced scope
   - Example CLI interaction updated to reflect new menu options
   - Folder structure comments updated to match scenario1 pattern
   - Submission checklist and grading rubric updated with "core tables" wording


.. dropdown:: v2.4.0 -- Lecture 6 Documentation (2026-03-15)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: lecture6/index.rst

   - Created top-level index for Lecture 6 with overview, learning objectives, toctree (lecture, exercises, quiz, glossary, references, cheat_sheet), and next-steps pointer to L7 (DML, transactions, psycopg3)
   - Added L6 row to the course-wide ``lectures/index.rst`` schedule table: topic "From Logical to Physical: Implementing Your Database in PostgreSQL" with full key-concepts list

   .. rubric:: lecture6/lecture.rst

   - Created full lecture document organized into six thematic sections: From Logical to Physical, PostgreSQL Data Types, Constraints, Building the University Schema, ALTER TABLE and Schema Evolution, DELETE / TRUNCATE / DROP, and Best Practices and Mistakes to Avoid
   - All 21 demos formatted as named ``.. admonition::`` boxes (``Demo 1`` through ``Demo 21``), each containing the instruction text and the complete SQL from ``lecture6_schema.sql``
   - **Demo 1**: FLOAT vs. NUMERIC -- ``grade_wrong`` (FLOAT) and ``grade_correct`` (NUMERIC) comparison; ``gpa = 3.9 AS exact_match`` behavior
   - **Demo 2**: PRIMARY KEY simple and composite -- column-level unnamed, table-level named, composite ``pk_enrollment``; duplicate insert error message comparison
   - **Demo 3**: Named vs. unnamed PK constraints -- ``department_pkey`` vs. ``pk_course`` in error output
   - **Demo 4**: SERIAL silent bypass -- sequence counter frozen at 1; duplicate key error surfaces two inserts later
   - **Demo 5**: GENERATED ALWAYS AS IDENTITY -- bypass rejected immediately; ``OVERRIDING SYSTEM VALUE``; ``START WITH 1000`` custom sequence
   - **Demo 6**: ISA shared-PK pattern -- ``person`` / ``student`` tables; FK violation on non-existent ``person_id``; two-hop CASCADE on delete
   - **Demo 7**: NO ACTION vs. RESTRICT vs. deferred -- three ``professor`` variants; timing of FK error
   - **Demo 8**: ON DELETE CASCADE -- Alice's enrollment rows disappear on student delete
   - **Demo 9**: ON DELETE SET NULL -- professors survive department deletion with ``dept_id = NULL``; ``SET NOT NULL`` blocked by existing nulls
   - **Demo 10**: ON DELETE SET DEFAULT -- fallback to ``dept_id = 0`` sentinel; fails when sentinel row is absent
   - **Demo 11**: Deferrable FKs -- circular ``department`` / ``professor`` insert succeeds inside ``BEGIN``/``COMMIT``
   - **Demo 12**: Mode 1 vs. Mode 2 deferral -- ``INITIALLY DEFERRED`` (automatic) vs. ``INITIALLY IMMEDIATE`` with ``SET CONSTRAINTS``
   - **Demo 13**: UNIQUE and the NULL trap -- two NULL plates coexist; ``plate = plate`` returns NULL; ``ALTER TABLE SET NOT NULL`` blocked
   - **Demo 14**: UNIQUE NULLS NOT DISTINCT -- fourth NULL insert fails; plain UNIQUE allows all four
   - **Demo 15**: CHECK constraints -- cross-column date check; IN-list vocabulary; NULL trap exposed by dropping ``NOT NULL``
   - **Demo 16**: Category exclusive-arc CHECK pattern -- ``vehicle_owner`` with three supertypes; arc sum = 2 rejected; arc sum = 0 rejected
   - **Demo 17**: EXCLUDE with GIST and INT4RANGE -- ``exam_schedule``; ``[40,80)`` rejected; adjacent ``[50,80)`` accepted; ``&&`` vs. ``=`` proof
   - **Demo 18**: Verifying the schema with catalog views -- ``information_schema.table_constraints``, ``referential_constraints``, ``pg_sequences``; FK-to-``student`` query
   - **Demo 19**: Common ALTER TABLE operations -- nullable add (instant); NOT NULL no default (error); NOT NULL with DEFAULT FALSE (instant); rename; drop column
   - **Demo 20**: Safe migration pattern -- four-step NOT VALID / VALIDATE CONSTRAINT; new writes blocked immediately at Step 3; ``convalidated`` verification
   - **Demo 21**: DELETE, TRUNCATE, and DROP -- five enrollment rows; DELETE two; TRUNCATE; RESTART IDENTITY; DROP; IF EXISTS safe drop
   - Added Think Prompt / Answer dropdowns for ISA shared-PK, CHECK NULL trap, EXCLUDE vs. UNIQUE, deferrable FKs (ON DELETE action selection), and DELETE / TRUNCATE / DROP semester-reload scenario
   - Added ``\d`` / ``\d+`` psql meta-command reference table and catalog view (``information_schema`` vs. ``pg_catalog``) comparison

   .. rubric:: lecture6/exercises.rst

   - Created four exercises covering all major L6 topics
   - **Exercise 1 -- Type Auditor**: audit a nine-column poorly typed ``grant_proposal`` table; identify seven or more mistakes; rewrite with correct types and named constraints; add ``submitted_at TIMESTAMPTZ`` via two ``ALTER TABLE`` statements
   - **Exercise 2 -- Constraint Detective**: predict SUCCEED / FAIL for a seven-statement sequence on ``person`` / ``student`` tables; explain the UNIQUE NULL behavior for two NULL emails; explain CASCADE result after ``DELETE FROM person``; write a ``NULLS NOT DISTINCT`` fix
   - **Exercise 3 -- ISA Hierarchy Builder**: design a three-level hierarchy (``person`` > ``researcher`` > ``graduate_researcher``) with ORCID ``UNIQUE NULLS NOT DISTINCT`` and grad-year ``CHECK``; verify two-hop CASCADE; add a fourth subtype ``postdoc_researcher``
   - **Exercise 4 -- Schema Migration Challenge**: apply four independent requirements changes to a live ``course_section`` table -- R1: safe NOT VALID / VALIDATE pattern for capacity NOT NULL; R2: regex CHECK for ``meeting_room`` using ``~`` operator; R3: rename ``section_no`` to ``section_code`` and retype to ``CHAR(4)``; R4: rename system-generated PK constraint to ``pk_course_section`` via ``ALTER TABLE ... RENAME CONSTRAINT``

   .. rubric:: lecture6/quiz.rst

   - Created 32 questions: 18 multiple choice (Q1-Q18), 10 true/false (Q19-Q28), and 4 essay (Q29-Q32)
   - Topics covered: NUMERIC vs. FLOAT, VARCHAR vs. TEXT, GENERATED ALWAYS vs. SERIAL, ``OVERRIDING SYSTEM VALUE`` and ``setval()``, ISA shared-PK, ON DELETE actions, deferrable constraints, CHECK NULL trap, UNIQUE NULL behavior, NULLS NOT DISTINCT, EXCLUDE vs. UNIQUE, ALTER TABLE rewrite cost, four-step migration pattern, TRUNCATE vs. DELETE, DROP CASCADE, anonymous vs. named constraints, deferrable constraint types, RESTART IDENTITY, FK naming convention
   - Essay questions cover: SERIAL silent bypass and ``setval()`` fix; shared-PK ISA rationale; DELETE / TRUNCATE / DROP four-dimension comparison; four-step migration pattern with lock levels

   .. rubric:: lecture6/glossary.rst

   - Created alphabetical glossary with 40 entries from ACCESS EXCLUSIVE Lock through VARCHAR(n)
   - Entries organized under letters A, B, C, D, E, F, G, I, L, N, O, P, R, S, T, U, V with RST ``.. _t6-glossary-x:`` anchor labels for in-page navigation links
   - Key entries: GENERATED ALWAYS AS IDENTITY, GiST Index, btree_gist, ISA Hierarchy, Shared-PK Strategy, NULLS NOT DISTINCT, NOT VALID, VALIDATE CONSTRAINT, SHARE UPDATE EXCLUSIVE Lock, RESTART IDENTITY, Exclusive-Arc Pattern (via Category pattern entry)

   .. rubric:: lecture6/references.rst

   - Created four dropdown sections: Lecture 6 card, PostgreSQL Official Documentation (nine cards: CREATE TABLE, ALTER TABLE, Data Types, Constraints, DELETE, TRUNCATE, DROP TABLE, Range Types, GiST Indexes), Textbooks (Elmasri & Navathe Ch. 3-4, Silberschatz Ch. 4-5), Online Resources (psql reference, Use The Index Luke, pgpedia GENERATED ALWAYS, DataGrip docs), Related Topics (L3, L4-L5, L7, L8)

   .. rubric:: lecture6/cheat_sheet.rst

   - Created condensed reference with nine labeled sections: Data Types table, Constraint Quick Reference table, SERIAL vs. GENERATED ALWAYS table, ON DELETE / ON UPDATE Actions table, ISA Shared-PK Pattern code block, Category Exclusive-Arc Pattern code block, Deferrable Constraints table, Creation Order (university waves) table, ALTER TABLE Operations table plus Safe Migration Pattern four-step code block, DELETE / TRUNCATE / DROP comparison tables, Schema Verification Quick Reference table, Naming Conventions table, Six Most Common DDL Mistakes table


.. dropdown:: v2.3.0 -- GP1 Updates (2026-03-06)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: scenario1/project1.rst

   - **Learning Objectives**: added "(ERDs)" acronym expansion to "Design Entity-Relationship Diagrams using Chen and Crow's Foot notations"
   - **Deliverable 2 (Crow's Foot)**: added "plus junction tables for any many-to-many relationships" to the entity requirements bullet
   - **Deliverable 3 (Design Report)**: added ``.. note::`` before the Report Outline dropdown linking to the L4-5 lecture (``../../lectures/lecture4/lecture``), the cheat sheet (``../../lectures/lecture4/cheat_sheet``), and a ``:download:`` link to the printable ``Normalization-Cheat-Sheet.pdf`` at ``/_static/images/l4/``

   .. rubric:: scenario2/project1.rst

   - **Learning Objectives**: added "(ERDs)" acronym expansion to "Design Entity-Relationship Diagrams for healthcare data"
   - **Part A (Chen)**: updated file path from ``diagrams/chen_erd.pdf`` to ``chen_erd.pdf``
   - **Part B (Crow's Foot)**: added "plus junction tables for any many-to-many relationships"; updated file path from ``diagrams/crows_foot_erd.pdf`` to ``crows_foot_erd.pdf``
   - **Task 2 (Design Report)**: added ``.. note::`` before the Report Outline dropdown linking to the L4-5 lecture, the cheat sheet, and the printable PDF (identical cross-references as scenario1)
   - **Folder Structure**: replaced nested ``diagrams/`` subfolder with flat structure matching scenario1; removed ``README.md`` and ``team_contributions.md``
   - **Documentation Files**: removed section entirely (no longer applicable)
   - **Submission Checklist**: removed "Supporting Files" block (README.md, team_contributions.md)


.. dropdown:: v2.2.0 -- Cheat Sheet Fixes (2026-03-06)
   :icon: tag
   :class-container: sd-border-success

   .. rubric:: lecture4/cheat_sheet.rst

   **Sphinx Build Fixes**

   - Replaced ``.. tabs::`` / ``.. tab::`` directives (unknown to docutils) with four nested ``.. dropdown::`` directives inside Box 4 (Attribute Closure), one per worked closure example
   - Fixed figure path from ``_static/...`` to ``/_static/...`` (root-relative) to resolve the ``image.not_readable`` warning when building from a subdirectory source file
   - Added ``cheat_sheet`` to the lecture4 ``index.rst`` toctree to resolve the ``document isn't included in any toctree`` warning

   **Layout Restructure**

   - Removed all ``.. grid::`` / ``.. grid-item-card::`` directives; all 15 boxes are now sequential ``.. dropdown::`` directives (one per box, full-width, vertical stack)
   - Box 14 (Lossless Join & Dependency Preservation): removed internal two-column grid; lossless join test and dependency preservation test are now sequential ``.. rubric::`` sections
   - Removed all ``----`` horizontal rule separators (previously used as visual dividers between grid rows)
   - Removed ``:open:`` from all dropdowns; all 15 boxes are collapsed by default


.. dropdown:: v2.1.0 -- Scenario 2 Rewrite (2026-02-27)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Scenario 2: Healthcare Patient Management Platform

   **Major Changes**

   - Replaced FastAPI REST API requirement with a **menu-driven CLI application** across GP2, GP3, and GP4
   - Added a **Data Generation Guide** reference with a ready-to-use LLM prompt so students can generate synthetic healthcare data that fits their own schema
   - Removed unrealistic system requirements from the index page (concurrent clinical users, sub-second response times)
   - Removed redundant index sections: System Requirements grid, Business Context narrative, Learning Objectives checklist, Success Criteria table, Getting Started, and What's Next

   **GP1: Relational Database Design (simplified)**

   - Consolidated 13 files (2 diagrams + 9 documentation PDFs + README + team contributions) into **3 deliverables**: Chen ERD (PDF), Crow's Foot ERD (PDF), and one design report (PDF, 8 to 12 pages)
   - Removed fixed entity count ("13+ required"); students decide how many entities their design needs, as long as all **eight business areas** are covered
   - Chen diagram now uses **(min,max) notation** for participation and cardinality instead of cardinality ratios
   - Removed separate files: entity_catalog.pdf, relationship_documentation.pdf, keys_analysis.pdf, constraints_catalog.pdf, relational_schema.pdf, normalization_proofs.pdf, denormalization_analysis.pdf, phi_matrix.pdf, healthcare_identifier_strategy.pdf
   - All content consolidated into design report with four sections: entity catalog, relationship analysis, healthcare identifiers and PHI designation, and normalization analysis
   - Entity catalog simplified: name, purpose, PK justification, candidate keys, business rules (no full attribute list with data types)
   - All tools now include hyperlinks; Inkscape and PlantUML entries point to lecture code at https://github.com/zeidk/enpm818t-spring-2026-code
   - File format standardized to PDF only (removed SVG option)
   - Fixed weight from 25% to **20%**

   **GP2: PostgreSQL + Python Integration (rewritten)**

   - Timeline changed from 5 weeks to **3 weeks**
   - Python application is now a **CLI with 6+ menu options** instead of a FastAPI REST API with 8+ endpoints
   - Sample data generation guided by a provided LLM prompt (internal link to Data Generation Guide)
   - Reduced queries from 10 to **8** (3 clinical, 2 financial, 3 operational)
   - Removed EXPLAIN ANALYZE requirement and query_catalog.md
   - Removed 5 documentation files (index_strategy.md, query_catalog.md, architecture.md, api_documentation.md, hipaa_compliance.md)
   - Reduced sample data volumes (100+ patients instead of 200+, 30+ providers instead of 50+)
   - Testing made **optional** (previously required 70% coverage)
   - Added Documentation Files section explaining each file's content
   - Removed verbose README and team contributions templates, "Required Files by Task", "Next Steps"
   - Fixed weight from 37.5% to **30%**
   - Fixed grading rubric: HIPAA Schema (3) + Synthetic Data (2) + Queries (5) + Python App (3) + CLI (2) = 15 points

   **GP3: MongoDB Integration (revised)**

   - Reduced from 8 required collections to **4** (2 provided examples + 2 student-designed)
   - Reduced queries from 8 to **6** (3 aggregation pipelines, 1 text search, 2 array operations)
   - Consolidated 3 documentation files (polyglot_design.md, mongodb_schema.md, integration_strategy.md) into a **single polyglot_design.md** covering partitioning, schemas, and indexes
   - Reduced sample data volumes (200+ clinical notes instead of 500+, 100+ imaging records instead of 100+)
   - New CLI menu options reduced from 4 to **3**; replaced REST API endpoints with CLI descriptions
   - Removed tests from required deliverables
   - Removed verbose README and team contributions templates, "Required Files by Task", "Next Steps"
   - Added yellow card for timeline/weight/team size (consistent with GP1/GP2)
   - Fixed weight from 25% to **20%**

   **GP4: Neo4j + Complete System (revised)**

   - Reduced node types from 12 to **6** (Disease, Symptom, Medication, Procedure, Lab Test, ICD-10 Code)
   - Reduced relationship types from 10 to **6**
   - Reduced Cypher queries from 8 to **6** (3 drug safety + 3 clinical decision support)
   - Reduced final report from 10-15 pages to **8-12 pages** and from 8 sections to **6 sections**
   - Reduced minimum graph sizes (30+ medications instead of 50+, 50+ interactions instead of 100+)
   - Removed mandatory performance benchmarks
   - Increased report rubric weight from 3 to **4 points** to reflect its importance as the capstone deliverable
   - Added "Drug Safety Integration" rubric row (2pts) for prescription safety workflow
   - Replaced REST API endpoints with **CLI operations**
   - Removed tests from required deliverables
   - Removed verbose README and team contributions templates, "Required Files by Task"
   - Added yellow card for timeline/weight/team size (consistent with GP1/GP2/GP3)
   - Fixed weight from 12.5% to **30%**

   **Consistency Fixes Across All Files**

   - Fixed weight percentages: GP1 = 20%, GP2 = 30%, GP3 = 20%, GP4 = 30% (previously incorrect)
   - Standardized all dropdown icons to ``:icon: gear`` (Octicon) across index.rst and all four project files
   - Removed all emoji from dropdown titles, admonition titles, and card headers
   - Aligned all requirement counts between index.rst and project files
   - Replaced all HIPAA/PHI compliance language with general terminology; then removed security controls entirely (audit triggers, RBAC, role-based field filtering, AuditService, audit_log table, access_reason tracking) to reduce scope and avoid confusing students
   - Reduced GP1 from eight business areas to **seven** (removed "Audit and Compliance")
   - GP2 now matches Scenario 1 structure: schema with constraints, synthetic data, queries, repository pattern, and CLI (no security layer)
   - GP4 report Section 2 renamed from "Security Approach" to "Data Partitioning Rationale"
   - Added scenario-specific **Data Generation Guide** with healthcare entities, synthetic data requirements, and verification queries (no audit_log generation)


.. dropdown:: v2.0.0 -- Scenario 1 Rewrite (2026-02-27)
   :icon: tag
   :class-container: sd-border-warning

   .. rubric:: Scenario 1: Smart City Traffic Management

   **Major Changes**

   - Replaced FastAPI REST API requirement with a **menu-driven CLI application** across GP2, GP3, and GP4
   - Added a **Data Generation Guide** with a ready-to-use LLM prompt so students can generate sample data that fits their own schema, rather than generating data from scratch or adapting a provided dataset
   - Removed unrealistic performance requirements from the index page (1,000+ sensor readings/sec, 500+ concurrent API users, <100ms response times)

   **GP1: Relational Database Design (simplified)**

   - Consolidated 7 separate PDF deliverables plus README and team contributions into a **single 8-to-12-page design report**
   - Deliverables reduced from 11 files to 3: Chen ERD (PDF), Crow's Foot ERD (PDF), and one design report (PDF)
   - Removed fixed entity count requirement ("11+ entities"); students decide how many entities their design needs, as long as all eight business areas are covered
   - Chen diagram now uses **(min,max) notation** for participation and cardinality instead of cardinality ratios; double lines for total participation are not required
   - Removed FK matrix, constraints catalog, and relational schema sections from the report (students have not seen SQL at this point)
   - Entity catalog simplified: name, purpose, primary key justification, candidate keys, and business rules (no attribute list with data types)
   - Report outline provided with section-by-section guidance and approximate page counts
   - All tools now include hyperlinks; Inkscape and PlantUML entries point to lecture code at https://github.com/zeidk/enpm818t-spring-2026-code
   - File format standardized to PDF only (removed SVG option)

   **GP2: PostgreSQL + Python Integration (rewritten)**

   - Timeline changed from 5 weeks to **3 weeks**
   - Python application is now a CLI with 8+ menu options instead of a FastAPI REST API with 8+ endpoints
   - Sample data generation guided by a provided LLM prompt (internal link to Data Generation Guide)
   - SQL query categories revised: removed CTEs and window functions (taught after GP2 submission); replaced with more JOINs, aggregates, subqueries, and PostGIS geospatial queries
   - Removed Task 1.2 (Index Strategy Document) to reduce deliverable count
   - Expanded Task 3.2 (Connection Management): each requirement (pool size, context manager, error handling, environment variables) now has a full explanatory paragraph and a complete code example
   - Clarified Task 4.1 (Testing): specific test cases listed for repositories (CRUD, not-found, constraint violations) and services (business logic, combined output, edge cases)
   - Added Documentation Files section explaining the content expected in each ``.md`` file, ``requirements.txt``, ``.env.example``, ``README.md``, and ``team_contributions.md``
   - Removed "Next Steps" section
   - Removed fixed constraint count ("15+ constraints") from schema task
   - Reduced test coverage requirement from 70% to 50%
   - Fixed grading rubric: Schema (3) + Data Loading (2) + Queries (5) + Python App (3) + CLI (2) = 15 points
   - Trimmed redundant sections (README template, team contributions template, duplicate file listings)

   **GP3: MongoDB Integration (revised)**

   - Reduced from 6 required collections to **4** (2 provided examples + 2 student-designed)
   - Reduced queries from 8 to **6** (3 aggregation pipelines, 1 geospatial, 2 array operations)
   - Consolidated 3 documentation files (polyglot_design.md, mongodb_schema.md, integration_strategy.md) into a **single polyglot_design.md** covering partitioning, schemas, and indexes
   - Reduced sample data volumes (500+ traffic events, 200+ sensor readings instead of 1000+/500+)
   - New CLI menu options reduced from 4 to **3**; fixed REST-style notation (``GET /path``) to CLI descriptions
   - Removed tests from required deliverables (consistent with GP2)
   - Removed verbose README and team contributions templates; replaced with Documentation Files section
   - Removed redundant "Required Files by Task" section
   - Removed "Next Steps" section
   - Added yellow card for timeline/weight/team size (consistent with GP1/GP2)

   **GP4: Redis + Complete System (revised)**

   - Reduced Redis data structures from 8 to **5** (strings, hashes, sorted sets, lists, pub/sub)
   - Consolidated caching_strategy.md and redis_data_structures.md into a **single caching_strategy.md**
   - Reduced final report from 10-15 pages to **8-12 pages** and from 8 sections to **6 sections**
   - Removed mandatory performance benchmarks (previously required before/after comparisons)
   - Increased report rubric weight from 2 to **4 points** to reflect its importance as the capstone deliverable
   - Removed tests from required deliverables
   - Removed verbose README and team contributions templates; replaced with Documentation Files section
   - Removed redundant "Required Files by Task" section
   - Added yellow card for timeline/weight/team size (consistent with GP1/GP2/GP3)

   **Consistency Fixes Across All Files**

   - Fixed weight percentages: GP1 = 20%, GP2 = 30%, GP3 = 20%, GP4 = 30% (previously incorrect)
   - Standardized all dropdown icons to ``:icon: gear`` (Octicon) across index.rst and all four project files
   - Removed emoji from admonition titles
   - Aligned collection count: index page now says "4+ collections" matching GP3 spec


.. dropdown:: v1.0.0 -- Sphinx Build Fixes (2026-02-27)
   :icon: tag
   :class-container: sd-border-success

   Resolved all 197 Sphinx build warnings across lectures 1 through 4.

   .. rubric:: Lecture Files (rubric conversions)

   - **lecture2/lecture.rst**: Converted 43 indented section titles inside ``.. dropdown::`` directives from RST heading syntax to ``.. rubric::`` directives
   - **lecture3/lecture.rst**: Converted 50 indented section titles to ``.. rubric::``; fixed 2 ``:widths:`` mismatches in ``.. list-table::`` directives; extended 6 title underlines to match title length
   - **lecture4/lecture.rst**: Converted 47 indented section titles to ``.. rubric::``

   .. rubric:: Exercise Files (transition removal + icon standardization)

   - **lecture1/exercises.rst**: Removed 6 indented ``----`` transitions; replaced 3 emoji dropdown icons with ``:icon: gear``
   - **lecture2/exercises.rst**: Removed 9 indented ``----`` transitions; replaced 4 emoji dropdown icons with ``:icon: gear``
   - **lecture3/exercises.rst**: Removed 8 indented ``----`` transitions; replaced 4 emoji dropdown icons with ``:icon: gear``
   - **lecture4/exercises.rst**: Removed 12 indented ``----`` transitions; replaced 6 emoji dropdown icons with ``:icon: gear``

   .. rubric:: Quiz Files (transition removal + format restructuring)

   - **lecture1/quiz.rst**: Removed 4 indented ``----`` transitions; restructured from bulk "Answer Key" at bottom to inline ``.. dropdown:: Answer`` after each question (25 questions)
   - **lecture2/quiz.rst**: Removed 2 indented ``----`` transitions; restructured to inline answers (38 questions)

   .. rubric:: Glossary Files (duplicate term removal)

   - **lecture3/glossary.rst**: Removed 6 duplicate term definitions already present in lecture2 glossary (Candidate Key, Composite Key, Crow's Foot Notation, Key Attribute, Logical Data Model, Superkey)
   - **lecture4/glossary.rst**: Removed 2 duplicate term definitions (First Normal Form, Normalization)