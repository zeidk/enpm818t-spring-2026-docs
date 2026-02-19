====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 1: Course Introduction,
Data Storage & Access Needs, Storage Hierarchies, Storage Architectures,
and PostgreSQL Overview.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2–4 sentences).
   - Answers are provided at the bottom of the page.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is the primary difference between a **database** and a **DBMS**?

   A. A database is software; a DBMS is data.

   B. A database is the organized collection of data; a DBMS is the software that manages it.

   C. A database runs on servers; a DBMS runs on clients.

   D. There is no difference; the terms are interchangeable.


.. admonition:: Question 2
   :class: hint

   Which of the following is **NOT** a responsibility of a Database Management System (DBMS)?

   A. Query processing and optimization

   B. Transaction management (ACID)

   C. Writing application business logic

   D. Backup and recovery


.. admonition:: Question 3
   :class: hint

   In the storage hierarchy, which tier offers the **fastest access times** but is **volatile** (loses data when powered off)?

   A. Secondary Storage

   B. Tertiary Storage

   C. Primary Storage

   D. Quaternary Storage


.. admonition:: Question 4
   :class: hint

   A hospital needs to store patient records in a database that requires **sub-millisecond latency**, **high availability**, and **block-level access**. Which storage architecture is most appropriate?

   A. NAS (Network-Attached Storage)

   B. Object Storage (e.g., AWS S3)

   C. SAN (Storage Area Network)

   D. DAS (Direct-Attached Storage)


.. admonition:: Question 5
   :class: hint

   Which protocol is used by **NAS** devices to provide file-level access to Linux clients?

   A. iSCSI

   B. Fibre Channel

   C. NFS

   D. NVMe


.. admonition:: Question 6
   :class: hint

   What PostgreSQL background process is responsible for **reclaiming storage from deleted rows** and **updating table statistics**?

   A. Postmaster

   B. Background Writer

   C. Autovacuum

   D. Checkpointer


.. admonition:: Question 7
   :class: hint

   Which of the following is a key advantage of using a DBMS over storing data in flat files (CSV, JSON)?

   A. Lower storage costs

   B. Data independence — applications don't need to know how data is physically stored

   C. Simpler deployment with no configuration required

   D. Faster read speeds for all workloads


.. admonition:: Question 8
   :class: hint

   What does **MVCC** stand for, and what problem does it solve in PostgreSQL?

   A. Multi-Value Column Control — allows multiple values in a single column

   B. Multi-Version Concurrency Control — allows concurrent transactions without locking

   C. Managed Virtual Cluster Computing — enables distributed database processing

   D. Memory-based Virtual Cache Control — manages RAM allocation for queries


.. admonition:: Question 9
   :class: hint

   Which data privacy regulation can impose fines of up to **€20 million or 4% of global annual revenue**?

   A. HIPAA

   B. PCI-DSS

   C. GDPR

   D. CCPA


.. admonition:: Question 10
   :class: hint

   In PostgreSQL's architecture, what is the role of the **Postmaster**?

   A. Writes dirty pages from shared buffers to disk

   B. Listens for client connections and spawns backend processes

   C. Maintains the write-ahead log for crash recovery

   D. Automatically vacuums tables to reclaim storage


----


True or False
=============

.. admonition:: Question 11
   :class: hint

   **True or False:** Object storage (e.g., AWS S3) uses a hierarchical file system with directories and subdirectories.


.. admonition:: Question 12
   :class: hint

   **True or False:** PostgreSQL is classified as an Object-Relational Database Management System (ORDBMS) because it extends the relational model with object-oriented features.


.. admonition:: Question 13
   :class: hint

   **True or False:** DAS (Direct-Attached Storage) can be shared across multiple servers simultaneously.


.. admonition:: Question 14
   :class: hint

   **True or False:** The Write-Ahead Log (WAL) in PostgreSQL ensures durability by logging changes *after* they are written to data files.


.. admonition:: Question 15
   :class: hint

   **True or False:** Tape storage (LTO) is still widely used today by major companies like Google, Microsoft, and Amazon for archival and backup purposes.


.. admonition:: Question 16
   :class: hint

   **True or False:** Block-level storage access (used by SAN and DAS) is generally better suited for databases than file-level access (used by NAS).


.. admonition:: Question 17
   :class: hint

   **True or False:** In the data management lifecycle, "Archival & Deletion" is the final stage, and data never cycles back to earlier stages.


.. admonition:: Question 18
   :class: hint

   **True or False:** PostgreSQL's Shared Buffers should typically be configured to use about 25% of system RAM.


.. admonition:: Question 19
   :class: hint

   **True or False:** HIPAA is a regulation that governs the protection of payment card information.


.. admonition:: Question 20
   :class: hint

   **True or False:** Cloud-managed PostgreSQL services like AWS RDS handle backups, patching, and scaling automatically.


----


Essay Questions
===============

.. admonition:: Question 21
   :class: hint

   **Explain the trade-offs in the storage hierarchy.** Describe how speed, cost, and capacity change as you move from primary storage to quaternary storage. Give one example of a storage medium at each level.

   *(2–4 sentences)*


.. admonition:: Question 22
   :class: hint

   **Compare DAS, NAS, and SAN.** For each architecture, identify: (a) the access type (block or file level), (b) whether it can be shared across multiple servers, and (c) one ideal use case.

   *(3–5 sentences)*


.. admonition:: Question 23
   :class: hint

   **Why is data independence an important benefit of using a DBMS?** Explain what data independence means and describe a scenario where it would be valuable.

   *(2–4 sentences)*


.. admonition:: Question 24
   :class: hint

   **Describe three key challenges in data management** discussed in the lecture. For each challenge, briefly explain the problem and one solution approach.

   *(3–5 sentences)*


.. admonition:: Question 25
   :class: hint

   **Explain why a company might choose PostgreSQL over MySQL.** Reference at least two specific features or characteristics that differentiate PostgreSQL.

   *(2–4 sentences)*


----


.. _quiz1-answers:

Answer Key
==========

Multiple Choice Answers
-----------------------

.. dropdown:: Click to reveal Multiple Choice answers
   :class-container: sd-border-success
   :class-title: sd-font-weight-bold

   1. **B** — A database is the organized collection of data; a DBMS is the software that manages it.

      *Explanation:* The database is the actual data stored electronically, while the DBMS (like PostgreSQL) is the software layer that provides an interface for defining, querying, and administering that data.

   2. **C** — Writing application business logic

      *Explanation:* A DBMS handles data storage, query processing, transactions, concurrency, security, and recovery. Business logic belongs in the application layer, not the database management system.

   3. **C** — Primary Storage

      *Explanation:* Primary storage includes CPU cache, RAM, and registers. It offers nanosecond access times but is volatile—data is lost when power is removed.

   4. **C** — SAN (Storage Area Network)

      *Explanation:* SANs provide block-level access with very low latency, support high availability through clustering and failover, and are the standard choice for enterprise database deployments in healthcare and finance.

   5. **C** — NFS

      *Explanation:* NFS (Network File System) is the standard protocol for file-level access on Linux/Unix systems. SMB/CIFS is used for Windows, and iSCSI/Fibre Channel are block-level protocols used by SANs.

   6. **C** — Autovacuum

      *Explanation:* The Autovacuum process automatically reclaims storage from dead tuples (deleted rows) and updates the statistics that the query planner uses for optimization.

   7. **B** — Data independence — applications don't need to know how data is physically stored

      *Explanation:* Data independence means you can change storage structures, add indexes, or reorganize tables without rewriting application code. This is a fundamental advantage of the DBMS abstraction layer.

   8. **B** — Multi-Version Concurrency Control — allows concurrent transactions without locking

      *Explanation:* MVCC enables multiple transactions to read and write data simultaneously by maintaining multiple versions of rows. Each transaction sees a consistent snapshot without blocking others.

   9. **C** — GDPR

      *Explanation:* The General Data Protection Regulation (GDPR) is the EU's comprehensive data privacy law. It can impose fines up to €20 million or 4% of global annual revenue, whichever is higher.

   10. **B** — Listens for client connections and spawns backend processes

       *Explanation:* The Postmaster is PostgreSQL's main daemon process. It listens on port 5432 (by default) and forks a new backend process for each client connection.


True/False Answers
------------------

.. dropdown:: Click to reveal True/False answers
   :class-container: sd-border-success
   :class-title: sd-font-weight-bold

   11. **False**

       *Explanation:* Object storage uses a flat namespace with unique object IDs, not a hierarchical directory structure. Objects are accessed via HTTP/REST APIs using keys, not file paths.

   12. **True**

       *Explanation:* PostgreSQL is indeed an ORDBMS. It extends the relational model with features like custom data types, table inheritance, and user-defined functions—all object-oriented concepts.

   13. **False**

       *Explanation:* DAS (Direct-Attached Storage) is physically connected to a single server and cannot be shared. For shared storage, you need NAS (file-level) or SAN (block-level).

   14. **False**

       *Explanation:* WAL logs changes *before* they are written to data files, not after. This "write-ahead" approach ensures that committed transactions can be recovered after a crash.

   15. **True**

       *Explanation:* Despite being one of the oldest storage technologies (invented 1951), tape remains critically important. Google, Microsoft, Amazon, banks, healthcare organizations, and film studios all use tape for long-term archival.

   16. **True**

       *Explanation:* Databases require direct control over storage blocks for optimal performance, transaction integrity, and recovery. Block-level access (SAN, DAS) provides this; file-level access (NAS) adds overhead that impacts database performance.

   17. **False**

       *Explanation:* The data management lifecycle is cyclical. Archived data may be retrieved and re-processed, analysis results may generate new data, and the cycle continues as data is repurposed.

   18. **True**

       *Explanation:* PostgreSQL documentation recommends setting shared_buffers to approximately 25% of system RAM as a starting point for most workloads.

   19. **False**

       *Explanation:* HIPAA (Health Insurance Portability and Accountability Act) governs healthcare data, not payment cards. PCI-DSS is the standard for payment card information security.

   20. **True**

       *Explanation:* Managed database services like AWS RDS, Google Cloud SQL, and Azure Database for PostgreSQL handle operational tasks including automated backups, security patching, scaling, and high availability configuration.


Essay Question Guidelines
-------------------------

.. dropdown:: Click to reveal Essay answer guidelines
   :class-container: sd-border-success
   :class-title: sd-font-weight-bold

   **Question 21 — Storage Hierarchy Trade-offs**

   *Key points to include:*

   - As you move down the hierarchy (primary → quaternary), speed decreases, cost per GB decreases, and capacity increases.
   - Primary: CPU cache/RAM — nanosecond access, volatile, expensive, limited capacity (GB).
   - Secondary: SSD/HDD — microsecond to millisecond access, persistent, moderate cost (TB).
   - Tertiary: Tape libraries/cloud nearline — seconds to minutes access, cheap, high capacity.
   - Quaternary: Glacier Deep Archive/offline tape — hours to days access, very cheap, massive capacity.

   ----

   **Question 22 — DAS vs. NAS vs. SAN**

   *Key points to include:*

   - **DAS**: Block-level access, single server only (not shared), ideal for development workstations or small single-server databases.
   - **NAS**: File-level access (NFS/SMB), shared across multiple clients, ideal for team file sharing, media libraries, and collaboration.
   - **SAN**: Block-level access, shared across multiple servers, ideal for enterprise databases, virtualization, and high-availability clusters.

   ----

   **Question 23 — Data Independence**

   *Key points to include:*

   - Data independence means applications don't need to know how data is physically stored or organized on disk.
   - You can change storage structures (add indexes, reorganize tables, switch storage engines) without rewriting application code.
   - Example scenario: A DBA can add a new index to improve query performance or migrate data to faster storage without any changes to the application connecting to the database.

   ----

   **Question 24 — Data Management Challenges**

   *Key points to include (any three):*

   - **Scalability**: Managing growing datasets. Solutions: partitioning, sharding, cloud auto-scaling.
   - **Security & Privacy**: Protecting sensitive data. Solutions: encryption, role-based access control.
   - **Data Consistency**: Maintaining accuracy across systems. Solutions: ACID transactions, validation rules.
   - **Cost Management**: Controlling infrastructure expenses. Solutions: tiered storage, auto-scaling.
   - **Performance**: Minimizing latency. Solutions: caching, indexing, load balancing.
   - **Governance & Compliance**: Meeting regulations (GDPR, HIPAA). Solutions: audit trails, access policies.

   ----

   **Question 25 — PostgreSQL vs. MySQL**

   *Key points to include (any two):*

   - **Advanced features**: PostgreSQL offers native JSON/JSONB support, full-text search, window functions, and CTEs that MySQL lacks or implements less completely.
   - **SQL standards compliance**: PostgreSQL has stronger adherence to ANSI SQL standards.
   - **Extensibility**: PostgreSQL allows custom data types, operators, and functions; supports Foreign Data Wrappers for querying external sources.
   - **MVCC implementation**: PostgreSQL's MVCC is more sophisticated, providing better concurrent read/write performance.
   - **Advanced indexing**: PostgreSQL supports B-tree, Hash, GiST, GIN, and BRIN indexes for different workloads.