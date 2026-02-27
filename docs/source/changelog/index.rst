====================================================
Changelog
====================================================

All notable changes to the ENPM818T Spring 2026 course documentation are recorded here.


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
