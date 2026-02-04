====================================================
Lecture
====================================================




Course Introduction
====================================================


Course Objectives
-----------------

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **What You Will Learn**

    - **Design** efficient database schemas using ER diagrams and normalization techniques.
    - **Select and implement** appropriate key strategies (surrogate vs. natural, composite keys).
    - **Write and optimize** complex SQL queries for relational databases.
    - **Evaluate and implement** appropriate NoSQL solutions based on use cases.
    - **Develop** scalable database architectures using partitioning, sharding, and replication.
    - **Integrate** databases with Python applications using industry-standard libraries.
    - **Deploy and manage** databases in cloud environments.
    - **Select** the right database technology for specific data requirements.

.. important::

   This course emphasizes **PostgreSQL** as the primary relational database and includes explicit **Python integration** with psycopg2, SQLAlchemy, and PyMongo.


Grading Structure
-----------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📊 Grade Distribution
        :class-card: sd-border-info

        .. list-table::
           :widths: 60 20
           :header-rows: 1

           * - Component
             - Weight
           * - Homework Assignments (3)
             - 35%
           * - Quizzes (5)
             - 20%
           * - Participation & Engagement
             - 5%
           * - Final Project
             - 40%
           * - **Total**
             - **100%**

    .. grid-item-card:: 🏗️ Final Project Milestones
        :class-card: sd-border-info

        - **Week 3**: Team Formation.
        - **Week 6**: Proposal Document Due.
        - **Week 11**: Progress Report Due.
        - **Week 15**: Application + Report + Peer Evaluation Due.

        Teams build a **polyglot persistence system** using one of
        three preset project proposals, integrating PostgreSQL,
        MongoDB, Redis, Cassandra, and Neo4j into a unified Python
        application deployed to a cloud environment.

.. warning::

   **No Final Exam** — Replaced by enhanced project assessment.


Assignment Progression
----------------------

Each assignment builds on the previous one, culminating in your final
project:

- **HW1** (Weeks 2–4): Data Modeling — design ERD, keys, and logical model for your project domain.
- **HW2** (Weeks 7–10): SQL and Python Integration — implement your model in PostgreSQL with complex queries and psycopg2.
- **HW3** (Weeks 10–12): NoSQL Implementation — identify and implement appropriate NoSQL components (MongoDB, Redis, Cassandra, or Neo4j).
- **Project** (Week 15): Integrate all components into a working polyglot persistence system deployed to a cloud environment.

.. tip::

   Choose a project domain early — every assignment feeds directly into
   the final deliverable.


Course Schedule
---------------

.. list-table::
   :widths: 5 55 25
   :header-rows: 1

   * - Wk
     - Topic
     - Deliverable
   * - 1
     - Course Intro + Data Storage + Setup
     -
   * - 2
     - Conceptual Data Modeling (ERD) + Keys Introduction
     - HW1 Posted
   * - 3
     - Logical Data Modeling + Normalization + Denormalization Intro
     - Quiz 1, Team Formation
   * - 4
     - Physical Data Model + Keys Implementation + Transactions
     - HW1 Due
   * - 5
     - SQL-1: Foundations + Python (psycopg2)
     - Quiz 2
   * - 6
     - SQL-2: Joins & Relationships
     - Proposal Doc Due
   * - 7
     - SQL-3a: Subqueries + CTEs
     - HW2 Posted
   * - 8
     - *Spring Break*
     -
   * - 9
     - SQL-3b: Window Functions + Views + Denormalization
     - Quiz 3
   * - 10
     - Query Optimization + Indexing + Scaling
     - HW2 Due, HW3 Posted
   * - 11
     - Production Operations: Migrations, Cloud, Backup + SQLAlchemy ORM
     - Quiz 4, Progress Report Due
   * - 12
     - Document Databases: MongoDB + PyMongo
     - HW3 Due
   * - 13
     - Key-Value (Redis) + Column-Family (Cassandra)
     -
   * - 14
     - Graph Databases: Neo4j + Python
     - Quiz 5
   * - 15
     - Database Internals + Vector Databases + Career Wrap-up
     - Final Project Due (Application + Report + Peer Eval)

.. note::

   This is a tentative schedule and subject to change as necessary —
   monitor ELMS-Canvas for current deadlines.


Lecture Format
--------------

Each weekly meeting follows a standard 2-hour-40-minute structure:

- **0:00 – 1:20** — Concept presentation (80 min).
- **1:20 – 1:30** — Break.
- **1:30 – 2:00** — Hands-on exercise (30 min).
- **2:00 – 2:40** — Solution review, Q&A, preview next week.

.. note::

   **One exercise per lecture** — Exercises reinforce concepts and
   contribute to your participation grade.


Data Storage & Access Needs
====================================================

Understanding **why databases exist** and how they fit into the broader
data management landscape.


Introduction to Data Management
-------------------------------

**Data management** involves organizing, storing, and maintaining data
throughout its lifecycle.

.. card::
    :class-card: sd-border-success sd-shadow-sm

    **Why Data Management Matters**

    - **Supports Decision-Making**: Accurate, up-to-date data for informed decisions.
    - **Ensures Compliance**: Meet regulatory requirements (GDPR, HIPAA, SOC 2).
    - **Enhances Performance**: Optimized queries and efficient processing.
    - **Reduces Costs**: Prevents duplication, improves storage efficiency.
    - **Improves Security**: Encryption, access control, backup policies.


Data Management Lifecycle
-------------------------

Data moves through five key stages — and the cycle repeats as data is
used and repurposed within an organization.

1. **Creation & Ingestion** — Data enters the system through user input, sensors, APIs, or ETL pipelines.
2. **Storage & Organization** — Data is persisted in databases, file systems, or object stores with defined schemas and access policies.
3. **Processing & Retrieval** — Queries, transformations, and indexing make the data usable.
4. **Analysis & Presentation** — Dashboards, reports, and machine-learning pipelines derive insight.
5. **Archival & Deletion** — Inactive data is moved to cheaper tiers or purged per retention rules.

.. note::

   This lifecycle is **cyclical** — data moves through these stages
   multiple times as it is used and repurposed within an organization.


Challenges in Data Management
-----------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📈 Scalability
        :class-card: sd-border-warning

        Managing large, growing datasets.

        **Solutions:** Partitioning, sharding, cloud scaling.

    .. grid-item-card:: 🔒 Security & Privacy
        :class-card: sd-border-warning

        Protecting sensitive data.

        **Solutions:** Encryption, access control.

    .. grid-item-card:: ✅ Data Consistency
        :class-card: sd-border-warning

        Accuracy across systems.

        **Solutions:** ACID transactions, validation.

    .. grid-item-card:: 💰 Cost Management
        :class-card: sd-border-warning

        Optimizing infrastructure expenses.

        **Solutions:** Tiered storage, auto-scaling.

    .. grid-item-card:: ⚡ Performance
        :class-card: sd-border-warning

        Reducing latency.

        **Solutions:** Caching, indexing, load balancing.

    .. grid-item-card:: 📋 Governance & Compliance
        :class-card: sd-border-warning

        Meeting regulatory requirements.

        **Solutions:** Audit trails, access policies.


Database Regulation & Compliance
--------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📜 What is Database Regulation?
        :class-card: sd-border-info

        - Laws governing how data is collected, stored, processed, and shared.
        - Protects individual privacy and sensitive information.
        - Varies by industry and region.

        **Key Regulations:**

        - **GDPR** (EU) — Personal data protection.
        - **HIPAA** (US) — Healthcare data.
        - **PCI-DSS** — Payment card data.
        - **CCPA** (California) — Consumer privacy.
        - **FERPA** (US) — Student education records.

    .. grid-item-card:: ✅ How to Comply
        :class-card: sd-border-info

        - Encrypt sensitive data (at rest and in transit).
        - Implement role-based access control.
        - Maintain audit logs of data access.
        - Define data retention and deletion policies.
        - Obtain user consent for data collection.

        **How Regulators Verify Compliance:**

        - Request audit logs and access records.
        - Review data handling policies.
        - Conduct on-site or remote audits.
        - Investigate breach reports and complaints.
        - Impose fines for non-compliance.

.. warning::

   **Example:** GDPR fines can reach €20 million or 4% of global annual
   revenue, whichever is higher.


Database vs DBMS
----------------

A **database** is an organized collection of structured data, typically
stored electronically.  It is the actual data itself.

A **Database Management System (DBMS)** is the software that interacts
with users, applications, and the database itself to capture, store, and
analyze data.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🛠️ DBMS Responsibilities
        :class-card: sd-border-info

        - Data storage and retrieval
        - Query processing and optimization
        - Transaction management (ACID)
        - Concurrency control
        - Security and access control
        - Backup and recovery

    .. grid-item-card:: 🗄️ Examples of DBMS
        :class-card: sd-border-info

        - **Relational**: PostgreSQL, MySQL, Oracle, SQL Server
        - **Document**: MongoDB, CouchDB
        - **Key-Value**: Redis, DynamoDB
        - **Graph**: Neo4j, Amazon Neptune
        - **Column-Family**: Cassandra, HBase


Why Use a DBMS?
---------------

Why not just store data in files (CSV, JSON, XML)?

.. list-table::
   :widths: 20 35 35
   :header-rows: 1

   * - Aspect
     - File System
     - DBMS
   * - Data Redundancy
     - High (duplicate data across files)
     - Low (normalization, single source of truth)
   * - Data Integrity
     - Manual enforcement
     - Constraints, triggers, foreign keys
   * - Concurrent Access
     - File locking issues
     - MVCC, transaction isolation
   * - Query Capability
     - Custom code for each query
     - SQL (declarative, optimized)
   * - Security
     - OS-level permissions
     - Row-level, column-level access control
   * - Recovery
     - Manual backup/restore
     - Point-in-time recovery, WAL
   * - Scalability
     - Limited
     - Replication, sharding, partitioning

.. important::

   A DBMS provides **data independence** — applications don't need to
   know how data is physically stored.  You can change storage structures
   without rewriting application code.


Storage Hierarchies
====================================================

A **storage hierarchy** is an organized structure for data storage,
designed to balance speed, cost, and capacity.


Overview
--------

.. list-table::
   :widths: 15 20 55
   :header-rows: 1

   * - Tier
     - Level
     - Description
   * - Primary
     - Fastest, most expensive
     - RAM, CPU cache, registers
   * - Secondary
     - Fast, moderate cost
     - SSD, HDD, NVMe
   * - Tertiary
     - Slower, cheaper
     - Tape libraries, cloud nearline (S3-IA)
   * - Quaternary
     - Slowest, cheapest
     - Cold/offline storage, Glacier Deep Archive

.. tip::

   As you move down the hierarchy, **speed decreases**, **cost per GB
   decreases**, but **capacity increases**.  Choose storage tier based on
   access frequency requirements.


Primary Storage
---------------

Primary storage refers to high-speed, **volatile** memory that directly
interacts with the CPU for immediate data processing.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Volatile**: Data lost when power is off.
        - **Extremely fast**: Nanosecond access times.
        - **Direct CPU access**: No intermediary.
        - **Limited capacity**: MB to hundreds of GB.

    .. grid-item-card:: 💡 Examples
        :class-card: sd-border-info

        - **CPU Cache** (L1, L2, L3): Ultra-fast, inside CPU.
        - **RAM**: Temporary storage for active apps.
        - **Registers**: Immediate instruction storage.

.. note::

   **Analogy:** Registers = notes in your hand; L1 Cache = notes on
   desk; RAM = books on bookshelf.


Secondary Storage
-----------------

Secondary storage refers to **non-volatile**, persistent storage
solutions that retain data even when powered off.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Non-volatile**: Data persists without power.
        - **Moderate speed**: Microsecond to millisecond access.
        - **Large capacity**: GB to PB.
        - **Direct access**: No robotic retrieval needed.

    .. grid-item-card:: 💡 Examples
        :class-card: sd-border-info

        - **HDD**: Magnetic platters, high capacity, lower cost.
        - **SSD**: Flash memory, faster, more expensive.
        - **NVMe**: Ultra-fast SSDs via PCIe.
        - **NAS**: Network-attached file storage.

.. important::

   **Database Context:** PostgreSQL stores its data files on secondary
   storage (SSD/HDD) but uses primary storage (RAM) for caching
   frequently accessed data via shared buffers.


Tertiary and Quaternary Storage
-------------------------------

**Tertiary Storage (Nearline)**

- **Purpose**: Medium-term archival and backup.
- **Examples**: Tape libraries, optical jukeboxes, cloud nearline (Google Nearline, AWS S3-IA).
- **Access time**: Seconds to minutes.
- **Use case**: Data accessed occasionally but needs to be available.

**Quaternary Storage (Cold/Offline)**

- **Purpose**: Long-term archival, regulatory compliance.
- **Examples**: Offline tapes, AWS Glacier Deep Archive, Azure Archive Storage.
- **Access time**: Minutes to hours (or days).
- **Use case**: Rarely accessed data, disaster recovery, legal retention.

.. note::

   **Cost Comparison:** AWS S3 Standard costs ~$0.023/GB/month vs.
   Glacier Deep Archive at ~$0.00099/GB/month — roughly a 23× difference.


Tape Storage
------------

Despite being one of the oldest storage technologies (invented 1951),
tape storage remains **critically important** for enterprise backup and
archival.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Capacity**: Up to 45 TB per cartridge (LTO-9).
        - **Cost**: $0.01–0.02 per GB (cheapest option).
        - **Durability**: 30+ year lifespan.
        - **Access**: Sequential (not random access).
        - **Speed**: Up to 400 MB/s sustained write.

    .. grid-item-card:: 📼 Current Technology: LTO
        :class-card: sd-border-info

        - **LTO** = Linear Tape-Open (industry standard).
        - **LTO-9** (2021): 18 TB native, 45 TB compressed.
        - **LTO-10** (planned): 36 TB native.
        - Roadmap extends to LTO-14 (1.4 PB compressed).

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🎯 Use Cases
        :class-card: sd-border-secondary

        - Long-term archival (legal, medical, financial records).
        - Disaster recovery and offsite backup.
        - Cold data rarely accessed.
        - Air-gapped security (ransomware protection).
        - Regulatory compliance (HIPAA, SOX, GDPR).

    .. grid-item-card:: 🏢 Who Uses Tape Today?
        :class-card: sd-border-secondary

        - Google, Microsoft, Amazon (cloud archive backend).
        - Banks and financial institutions.
        - Healthcare organizations.
        - Government agencies.
        - Film studios (Netflix, Disney, Warner Bros).

.. tip::

   **Database Relevance:** PostgreSQL backups (``pg_dump``,
   ``pg_basebackup``) are often written to tape for long-term retention
   and disaster recovery.  Tape provides an "air gap" against
   ransomware.


Storage Cost Comparison
-----------------------

.. list-table::
   :widths: 18 12 12 14 14 14
   :header-rows: 1

   * - Metric
     - SSD
     - HDD
     - S3 Standard
     - S3 Glacier
     - Tape (LTO-9)
   * - Cost/TB/month
     - ~$80
     - ~$20
     - ~$23
     - ~$4
     - ~$2
   * - Access Time
     - µs
     - ms
     - ms
     - hours
     - minutes
   * - Durability
     - ~5 years
     - ~5 years
     - 11 nines
     - 11 nines
     - 30+ years
   * - Random Access
     - Yes
     - Yes
     - Yes
     - No
     - No

.. note::

   There is no single "best" storage — choose based on access patterns,
   retention requirements, and budget.  Most organizations use a
   **tiered approach** combining multiple technologies.


Storage Architectures
====================================================

**Storage architecture** refers to the design framework that dictates
how data is stored, retrieved, managed, and protected.


Block-Level vs. File-Level Access
---------------------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🧱 Block-Level Access
        :class-card: sd-border-info

        - Storage provides **raw blocks** (512B or 4KB chunks).
        - OS/application manages file system.
        - Appears as a local disk (e.g., ``/dev/sda``).
        - **Protocols**: iSCSI, Fibre Channel, NVMe.
        - **Examples**: SAN, DAS, AWS EBS.

        .. note::

           **Best For:** Databases (PostgreSQL, MySQL, Oracle) — direct
           control, low latency, reliable transactions.

    .. grid-item-card:: 📁 File-Level Access
        :class-card: sd-border-info

        - Storage provides **files and directories**.
        - Storage system manages file system.
        - Appears as network share (e.g., ``/mnt/share``).
        - **Protocols**: NFS, SMB/CIFS.
        - **Examples**: NAS, AWS EFS, network drives.

        .. note::

           **Best For:** Shared documents, media files, collaboration —
           easy access from multiple clients.

.. tip::

   **Analogy:** Block-level is like renting an empty warehouse — you
   organize everything.  File-level is like renting a storage unit with
   pre-built shelves — organization is provided.


Direct-Attached Storage (DAS)
-----------------------------

DAS is storage that is **physically connected directly to a single
server or workstation** without any network in between.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Connection**: Direct cable (SATA, SAS, USB, NVMe).
        - **Access Type**: Block-level.
        - **Sharing**: Single server only.
        - **Latency**: Very low (no network overhead).
        - **Scalability**: Limited by server capacity.

    .. grid-item-card:: 💡 Examples
        :class-card: sd-border-info

        - Internal hard drives and SSDs.
        - External USB/Thunderbolt drives.
        - RAID enclosures connected via SAS.
        - NVMe drives in PCIe slots.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ Advantages
        :class-card: sd-border-success

        - Simple setup and management.
        - Low cost.
        - High performance (no network latency).
        - No network dependency.

    .. grid-item-card:: ❌ Disadvantages
        :class-card: sd-border-danger

        - Cannot share storage across servers.
        - Limited scalability.
        - Single point of failure.
        - Difficult centralized management.


Network-Attached Storage (NAS)
------------------------------

NAS is a **dedicated file server connected to a network** that provides
file-level storage to multiple clients simultaneously.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Connection**: Standard Ethernet (LAN).
        - **Access Type**: File-level (NFS, SMB/CIFS).
        - **Sharing**: Multiple clients can access simultaneously.
        - **Protocols**: NFS (Linux), SMB (Windows), AFP (Mac).
        - **Management**: Web interface, dedicated OS.

    .. grid-item-card:: 💡 Examples
        :class-card: sd-border-info

        - Synology DiskStation.
        - QNAP NAS devices.
        - Western Digital My Cloud.
        - TrueNAS (open-source).

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ Advantages
        :class-card: sd-border-success

        - Easy file sharing across network.
        - Centralized storage management.
        - Built-in RAID for redundancy.
        - Remote access capabilities.

    .. grid-item-card:: ❌ Disadvantages
        :class-card: sd-border-danger

        - Network bandwidth dependent.
        - Higher latency than DAS.
        - Not ideal for databases (file-level).
        - Network congestion impacts performance.


Storage Area Network (SAN)
--------------------------

A SAN is a **dedicated high-speed network** that connects servers to a
shared pool of storage devices, providing block-level access.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Connection**: Dedicated network (Fibre Channel, iSCSI).
        - **Access Type**: Block-level (appears as local disk).
        - **Sharing**: Multiple servers access shared storage pool.
        - **Protocols**: FC (Fibre Channel), iSCSI, FCoE.
        - **Speed**: Up to 128 Gbps (FC), 100 Gbps (iSCSI).

    .. grid-item-card:: 💡 Examples
        :class-card: sd-border-info

        - Dell EMC Unity/PowerStore.
        - NetApp AFF/FAS Series.
        - HPE Nimble Storage.
        - Pure Storage FlashArray.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ Advantages
        :class-card: sd-border-success

        - High performance and low latency.
        - Centralized storage management.
        - Excellent for databases (block-level).
        - Supports clustering and failover.

    .. grid-item-card:: ❌ Disadvantages
        :class-card: sd-border-danger

        - High cost (hardware + expertise).
        - Complex setup and management.
        - Requires dedicated infrastructure.
        - Specialized skills needed.


Object Storage
--------------

Object storage manages data as **discrete objects** (file + metadata +
unique ID) rather than blocks or files in a hierarchy.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 📋 Characteristics
        :class-card: sd-border-info

        - **Access Type**: Object-level via HTTP/REST APIs.
        - **Structure**: Flat namespace (no folders).
        - **Metadata**: Rich, customizable metadata per object.
        - **Scalability**: Virtually unlimited (exabytes).
        - **Durability**: 99.999999999% (11 nines) typical.

    .. grid-item-card:: 💡 Examples
        :class-card: sd-border-info

        - **AWS S3**: Most popular object storage.
        - **Google Cloud Storage**.
        - **Azure Blob Storage**.
        - **MinIO**: Open-source, S3-compatible.
        - **Ceph**: Distributed storage system.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ Advantages
        :class-card: sd-border-success

        - Massive scalability (exabytes).
        - Cost-effective for large datasets.
        - Built-in redundancy and durability.
        - Rich metadata support.

    .. grid-item-card:: ❌ Disadvantages
        :class-card: sd-border-danger

        - Higher latency than block storage.
        - Not suitable for databases directly.
        - No file system semantics.
        - Eventual consistency (some systems).


Cloud Storage
-------------

Cloud storage provides **on-demand, remotely managed storage** via the
internet, combining various storage types (block, file, object).

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ☁️ Storage Types in Cloud
        :class-card: sd-border-info

        - **Block Storage**: EBS (AWS), Persistent Disk (GCP).
        - **File Storage**: EFS (AWS), Filestore (GCP).
        - **Object Storage**: S3 (AWS), GCS, Azure Blob.

    .. grid-item-card:: 🗄️ Managed Database Services
        :class-card: sd-border-info

        - **AWS**: RDS, Aurora PostgreSQL.
        - **Google Cloud**: Cloud SQL, AlloyDB.
        - **Azure**: Azure Database for PostgreSQL.
        - **Specialized**: Supabase, Neon, PlanetScale.

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ Advantages
        :class-card: sd-border-success

        - Scalable and flexible (pay-as-you-go).
        - No hardware maintenance.
        - Geographic redundancy built-in.
        - Automated backups and recovery.

    .. grid-item-card:: ❌ Disadvantages
        :class-card: sd-border-danger

        - Internet dependency.
        - Ongoing operational costs.
        - Data sovereignty concerns.
        - Potential vendor lock-in.

.. important::

   Cloud-managed PostgreSQL services handle backups, patching, scaling,
   and high availability automatically.  This is increasingly the
   preferred deployment model for production databases.


Architecture Comparison
-----------------------

.. list-table::
   :widths: 18 14 14 14 16 16
   :header-rows: 1

   * - Aspect
     - DAS
     - NAS
     - SAN
     - Object
     - Cloud
   * - Access Type
     - Block
     - File
     - Block
     - Object (HTTP)
     - All types
   * - Network
     - None
     - LAN
     - Dedicated
     - Internet
     - Internet
   * - Sharing
     - Single
     - Multiple
     - Multiple
     - Unlimited
     - Unlimited
   * - Scalability
     - Limited
     - Moderate
     - High
     - Very High
     - Very High
   * - Cost
     - Low
     - Moderate
     - High
     - Low/GB
     - Variable
   * - Latency
     - Very Low
     - Medium
     - Low
     - High
     - Variable
   * - Best For
     - Dev / Small
     - File sharing
     - Enterprise DB
     - Backups / Media
     - Managed services

.. tip::

   **PostgreSQL Storage Recommendations:**

   - **Development**: DAS (local SSD) — simple, fast.
   - **Small Production**: Cloud managed (RDS, Cloud SQL) — minimal ops overhead.
   - **Enterprise**: SAN with replication — performance + high availability.
   - **Backups**: Object storage (S3) — cost-effective, durable.


PostgreSQL Overview
====================================================

PostgreSQL is a powerful, open-source **object-relational database
management system** (ORDBMS) with over 35 years of active development.


History
-------

- **1977**: Michael Stonebraker creates INGRES at UC Berkeley.
- **1986**: POSTGRES project begins ("Post-Ingres").
- **1994**: Andrew Yu and Jolly Chen add SQL support (Postgres95).
- **1996**: Renamed to PostgreSQL; community-driven development begins.
- **Present**: Major releases annually; PostgreSQL 18 released September 2025.

.. note::

   The name is pronounced "post-GRES-Q-L" or simply "Postgres".  The
   elephant logo is named "Slonik".


Key Features
------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ⚙️ Core Features
        :class-card: sd-border-info

        - **ACID Compliance**: Full transaction support.
        - **MVCC**: Multi-Version Concurrency Control.
        - **Advanced Indexing**: B-tree, Hash, GiST, GIN, BRIN.
        - **Full-Text Search**: Built-in text search engine.
        - **JSON/JSONB**: Native JSON support.
        - **Window Functions**: Advanced analytics.
        - **CTEs**: Common Table Expressions.

    .. grid-item-card:: 🏢 Enterprise Features
        :class-card: sd-border-info

        - **Replication**: Streaming, logical replication.
        - **Partitioning**: Table partitioning for large datasets.
        - **Foreign Data Wrappers**: Query external data sources.
        - **Parallel Queries**: Multi-core query execution.
        - **Point-in-Time Recovery**: Continuous archiving.
        - **Row-Level Security**: Fine-grained access control.
        - **Extensibility**: Custom types, functions, operators.

.. note::

   **PostgreSQL vs MySQL:** PostgreSQL offers more advanced features
   (JSON, full-text search, window functions) and better SQL standards
   compliance.  MySQL is often perceived as simpler but less
   feature-rich.


Architecture
------------

PostgreSQL uses a **multi-process** architecture.  Each client
connection is handled by a dedicated backend process, and all processes
communicate through shared memory.

.. list-table::
   :widths: 25 65
   :header-rows: 1

   * - Component
     - Description
   * - Postmaster
     - Main daemon that listens for connections and spawns backend processes.
   * - Backend Process
     - One per client connection; executes queries and returns results.
   * - Shared Buffers
     - In-memory cache for frequently accessed data pages (typically 25% of RAM).
   * - WAL (Write-Ahead Log)
     - Ensures durability by logging changes before writing to data files.
   * - Background Writer
     - Periodically writes dirty pages from shared buffers to disk.
   * - Autovacuum
     - Reclaims storage from deleted rows and updates table statistics.
   * - Checkpointer
     - Writes all dirty buffers to disk at regular intervals.

The typical data flow is:

1. A **client** (Python app, ``psql``, DataGrip) connects to the **Postmaster**.
2. Postmaster spawns a **Backend Process** to handle the session.
3. The backend reads/writes **Shared Buffers** (in-memory cache).
4. Background processes flush dirty buffers to **Storage** (data files, WAL files).


Who Uses PostgreSQL?
--------------------

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: 🏢 Major Users
        :class-card: sd-border-secondary

        - **Apple**: iCloud infrastructure.
        - **Instagram**: Primary database (billions of rows).
        - **Spotify**: Music metadata storage.
        - **Netflix**: Content management.
        - **Reddit**: Core data platform.
        - **Twitch**: User and stream data.
        - **Uber**: Geospatial data (PostGIS).
        - **NASA**: Scientific data management.

    .. grid-item-card:: 🏆 Why They Choose PostgreSQL
        :class-card: sd-border-secondary

        - **Reliability**: Proven track record since 1996.
        - **Performance**: Handles large workloads efficiently.
        - **Standards**: Strong SQL compliance.
        - **Extensibility**: Custom types and functions.
        - **Cost**: No licensing fees.
        - **Community**: Active development and support.

.. note::

   PostgreSQL consistently ranks in the **top 4** most popular databases
   worldwide on `DB-Engines <https://db-engines.com/en/ranking>`_, and
   was named **DBMS of the Year** in 2017, 2020, 2021, and 2023.


Ecosystem
---------

.. grid:: 1 3 3 3
    :gutter: 3

    .. grid-item-card:: 💻 CLI Tools
        :class-card: sd-border-info

        - **psql**: Interactive terminal.
        - **pg_dump**: Backup utility.
        - **pg_restore**: Restore from backup.
        - **createdb** / **dropdb**: DB management.
        - **pg_ctl**: Server control.

    .. grid-item-card:: 🖥️ GUI Tools
        :class-card: sd-border-info

        - **DataGrip**: JetBrains IDE (our choice).
        - **pgAdmin 4**: Official GUI.
        - **DBeaver**: Multi-database tool.
        - **TablePlus**: Modern GUI.
        - **Postico**: macOS native.

    .. grid-item-card:: 🧩 Extensions
        :class-card: sd-border-info

        - **PostGIS**: Geospatial data.
        - **pg_stat_statements**: Query stats.
        - **pgcrypto**: Encryption.
        - **uuid-ossp**: UUID generation.
        - **pg_trgm**: Fuzzy matching.

**Cloud Offerings:**

- **AWS RDS for PostgreSQL** / **Aurora PostgreSQL**.
- **Google Cloud SQL** for PostgreSQL.
- **Azure Database for PostgreSQL**.
- **Supabase**, **Neon**, **CockroachDB** (PostgreSQL-compatible).


Environment Setup
====================================================

Setting up your development environment for the course.

.. important::

   **Required Software:**

   - **PostgreSQL 18+** — Primary relational database.
   - **Python 3.10+** — Programming language for database integration.
   - **DataGrip** — JetBrains database IDE (free for students).
   - **VS Code** — Code editor for Python development.


PostgreSQL Installation
-----------------------

.. tab-set::

    .. tab-item:: Windows

        1. Download from `postgresql.org <https://www.postgresql.org/download/windows/>`_.
        2. Run installer, select all components.
        3. Set password for the ``postgres`` user.
        4. Note the port (default: ``5432``).

    .. tab-item:: macOS

        Install via Homebrew:

        .. code-block:: bash

           brew install postgresql@18
           brew services start postgresql@18

    .. tab-item:: Linux (Ubuntu/Debian)

        .. code-block:: bash

           sudo apt update
           sudo apt install postgresql
           sudo systemctl start postgresql

**Verify Installation:**

.. code-block:: bash

   psql --version
   psql -U postgres

.. warning::

   Remember the password you set for the ``postgres`` superuser.  You
   will need it to connect from DataGrip and Python.


DataGrip Installation
---------------------

DataGrip is a powerful, cross-platform database IDE from JetBrains that
supports PostgreSQL, MySQL, MongoDB, and many other databases.

1. Apply for a `JetBrains Educational License <https://www.jetbrains.com/community/education/>`_ (free for students).
2. Download from `jetbrains.com/datagrip <https://www.jetbrains.com/datagrip/>`_.
3. Install and activate with your educational license.

**Key Features:**

- Intelligent SQL code completion.
- Query execution and results visualization.
- Schema navigation and ER diagrams.
- Data export/import in multiple formats.
- Version control integration.
- Multiple database support.


Connecting DataGrip to PostgreSQL
---------------------------------

1. Open DataGrip → click **+** (New) → **Data Source** → **PostgreSQL**.
2. Enter connection details:

.. list-table::
   :widths: 30 50
   :header-rows: 1

   * - Field
     - Value
   * - Host
     - ``localhost``
   * - Port
     - ``5432``
   * - User
     - ``postgres``
   * - Password
     - *(your password)*
   * - Database
     - ``postgres`` (default)

3. Click **Test Connection** to verify.
4. Click **OK** to save.

.. tip::

   DataGrip will prompt you to download the PostgreSQL JDBC driver on
   first connection.  Click **Download** to install it automatically.


Python Installation
-------------------

.. tab-set::

    .. tab-item:: Windows

        Download from `python.org <https://python.org/downloads>`_.
        Check **"Add to PATH"** during installation.

    .. tab-item:: macOS

        .. code-block:: bash

           brew install python@3.11

    .. tab-item:: Linux

        Usually pre-installed.  Verify with ``python3 --version``.

**Verify Installation:**

.. code-block:: bash

   python --version
   python -m pip --version

**Required Packages:**

.. code-block:: bash

   python -m pip install psycopg2-binary
   python -m pip install sqlalchemy
   python -m pip install pymongo
   python -m pip install redis
   python -m pip install pandas

**Virtual Environment (recommended):**

.. tab-set::

    .. tab-item:: Windows

        .. code-block:: bash

           python -m venv enpm818t
           enpm818t\Scripts\activate

    .. tab-item:: Linux/macOS

        .. code-block:: bash

           python -m venv enpm818t
           source enpm818t/bin/activate


VS Code Installation
--------------------

1. Download from `code.visualstudio.com <https://code.visualstudio.com>`_.
2. Install the following extensions:

   - **Python** (Microsoft) — Python language support.
   - **Ruff** — Linting and formatting.
   - **Pylance** — Enhanced Python IntelliSense (should be installed with Python extension).
   - **GitLens** (optional) — Git integration.

3. Configure Python interpreter:

   - Press ``Ctrl+Shift+P``.
   - Type "Python: Select Interpreter".
   - Choose your Python 3.10+ installation.

.. note::

   We will use DataGrip for SQL development and VS Code for Python
   development.  Both tools complement each other well.


Putting It All Together
====================================================

.. grid:: 1 2 2 2
    :gutter: 3

    .. grid-item-card:: ✅ What We Covered
        :class-card: sd-border-success

        - Course structure, grading, and assignment chain.
        - Data management fundamentals and lifecycle.
        - Storage hierarchies (primary through quaternary).
        - Storage architectures (DAS, NAS, SAN, Object, Cloud).
        - PostgreSQL history, features, and architecture.
        - Environment setup (PostgreSQL, DataGrip, Python, VS Code).

    .. grid-item-card:: 🔜 Preview: L2 — Conceptual Data Modeling
        :class-card: sd-border-primary

        - Entity-Relationship diagrams.
        - Entities, attributes, and relationships.
        - Cardinality and participation constraints.
        - Designing your project domain model.
        - HW1 posted.