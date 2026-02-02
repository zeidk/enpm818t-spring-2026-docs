====================================================
Glossary
====================================================

:ref:`A <t1-glossary-a>` · :ref:`B <t1-glossary-b>` · :ref:`C <t1-glossary-c>` · :ref:`D <t1-glossary-d>` · :ref:`F <t1-glossary-f>` · :ref:`I <t1-glossary-i>` · :ref:`L <t1-glossary-l>` · :ref:`M <t1-glossary-m>` · :ref:`N <t1-glossary-n>` · :ref:`O <t1-glossary-o>` · :ref:`P <t1-glossary-p>` · :ref:`Q <t1-glossary-q>` · :ref:`R <t1-glossary-r>` · :ref:`S <t1-glossary-s>` · :ref:`T <t1-glossary-t>` · :ref:`W <t1-glossary-w>`

----


.. _t1-glossary-a:

A
=

.. glossary::

   ACID
      A set of four properties — **Atomicity**, **Consistency**,
      **Isolation**, **Durability** — that guarantee reliable
      processing of database transactions.

   Autovacuum
      A PostgreSQL background process that automatically reclaims
      storage occupied by dead tuples and updates table statistics
      used by the query planner.


.. _t1-glossary-b:

B
=

.. glossary::

   Backend Process
      A PostgreSQL server process spawned by the :term:`Postmaster`
      to handle a single client connection.  Each backend executes
      queries and returns results independently.

   Block-Level Access
      A storage access method in which the operating system or
      application reads and writes fixed-size blocks (typically
      512 bytes – 4 KB) directly.  Used by :term:`DAS` and
      :term:`SAN`.


.. _t1-glossary-c:

C
=

.. glossary::

   Checkpointer
      A PostgreSQL background process that periodically writes all
      dirty shared-buffer pages to disk, ensuring a consistent
      on-disk state for crash recovery.

   Cloud Storage
      On-demand, remotely managed storage provided over the internet
      that can include block, file, and object storage types.
      Examples: AWS S3, Google Cloud Storage, Azure Blob Storage.

   Cold Storage
      The lowest tier in a :term:`Storage Hierarchy`, used for rarely
      accessed archival data.  Examples: AWS Glacier Deep Archive,
      offline tape.

   Concurrency Control
      Mechanisms that allow multiple transactions to execute
      simultaneously without conflicting.  PostgreSQL uses
      :term:`MVCC` for this purpose.


.. _t1-glossary-d:

D
=

.. glossary::

   DAS
      **Direct-Attached Storage** — storage physically connected to a
      single server via SATA, SAS, USB, or NVMe.  Offers very low
      latency but cannot be shared across servers.

   Data Independence
      The principle that applications should not need to know how data
      is physically stored.  A key benefit of using a :term:`DBMS`.

   Data Management
      The practice of organizing, storing, and maintaining data
      throughout its lifecycle, encompassing creation, storage,
      processing, analysis, and archival.

   Database
      An organized collection of structured data, typically stored
      electronically.  Distinguished from the :term:`DBMS`, which is
      the software that manages it.

   DBMS
      **Database Management System** — software that provides an
      interface for defining, creating, querying, updating, and
      administering databases.  Examples: PostgreSQL, MySQL, MongoDB.

   DataGrip
      A cross-platform database IDE from JetBrains supporting
      PostgreSQL, MySQL, MongoDB, and many other databases.  Used in
      this course for SQL development.


.. _t1-glossary-f:

F
=

.. glossary::

   Fibre Channel
      A high-speed networking technology (up to 128 Gbps) used
      primarily in :term:`SAN` environments to connect servers to
      shared storage arrays.

   File-Level Access
      A storage access method in which data is read and written as
      complete files within a directory hierarchy.  Used by
      :term:`NAS`.

   Foreign Data Wrapper
      A PostgreSQL extension mechanism that lets the server query
      data stored in external sources (other databases, CSV files,
      REST APIs) as if they were local tables.


.. _t1-glossary-i:

I
=

.. glossary::

   iSCSI
      **Internet Small Computer Systems Interface** — a protocol that
      carries SCSI commands over TCP/IP networks, allowing
      :term:`SAN`-like block storage over standard Ethernet.


.. _t1-glossary-l:

L
=

.. glossary::

   LTO
      **Linear Tape-Open** — an industry-standard magnetic tape
      format.  LTO-9 (2021) offers 18 TB native / 45 TB compressed
      per cartridge.  The roadmap extends to LTO-14.


.. _t1-glossary-m:

M
=

.. glossary::

   MVCC
      **Multi-Version Concurrency Control** — a technique used by
      PostgreSQL to allow multiple transactions to read and write
      data concurrently without locking.  Each transaction sees a
      consistent snapshot of the database.


.. _t1-glossary-n:

N
=

.. glossary::

   NAS
      **Network-Attached Storage** — a dedicated file server
      connected to a LAN that provides :term:`file-level access
      <File-Level Access>` to multiple clients simultaneously.
      Protocols include NFS, SMB/CIFS, and AFP.

   Normalization
      The process of organizing database tables to minimize data
      redundancy and improve data integrity.  Results in a schema
      where each fact is stored in exactly one place.

   NVMe
      **Non-Volatile Memory Express** — a host controller interface
      and storage protocol for SSDs connected via PCIe, offering
      significantly lower latency than SATA or SAS.


.. _t1-glossary-o:

O
=

.. glossary::

   Object Storage
      A storage architecture that manages data as discrete objects
      (data + metadata + unique ID) in a flat namespace rather than
      a hierarchical file system.  Accessed via HTTP/REST APIs.
      Examples: AWS S3, MinIO, Ceph.

   ORDBMS
      **Object-Relational Database Management System** — a DBMS that
      extends the relational model with object-oriented features such
      as custom types, inheritance, and functions.  PostgreSQL is
      classified as an ORDBMS.


.. _t1-glossary-p:

P
=

.. glossary::

   pg_hba.conf
      The PostgreSQL **Host-Based Authentication** configuration file
      that controls which clients can connect, to which databases,
      and with which authentication method.

   Postmaster
      The main PostgreSQL daemon process that listens for incoming
      client connections and forks a :term:`Backend Process` for each
      one.

   PostGIS
      A PostgreSQL extension that adds support for geographic objects,
      enabling location queries to be run in SQL.  Widely used for
      geospatial applications.

   psql
      The official PostgreSQL interactive command-line terminal.
      Supports SQL queries, meta-commands (prefixed with ``\``), and
      scripting.

   psycopg2
      The most widely used PostgreSQL adapter for Python.  Provides a
      DB-API 2.0–compliant interface for connecting to and querying
      PostgreSQL databases from Python code.


.. _t1-glossary-q:

Q
=

.. glossary::

   Quaternary Storage
      The lowest cost, highest latency tier in a :term:`Storage
      Hierarchy`.  Used for long-term archival and regulatory
      compliance.  Examples: offline tapes, AWS Glacier Deep Archive.


.. _t1-glossary-r:

R
=

.. glossary::

   Replication
      The process of copying data from one database server (primary)
      to one or more servers (replicas) to improve availability and
      read performance.  PostgreSQL supports both streaming and
      logical replication.

   Row-Level Security
      A PostgreSQL feature that restricts which rows a user can see
      or modify based on security policies defined on the table.


.. _t1-glossary-s:

S
=

.. glossary::

   SAN
      **Storage Area Network** — a dedicated high-speed network
      (Fibre Channel or iSCSI) connecting servers to shared storage
      arrays with :term:`block-level access <Block-Level Access>`.
      Common in enterprise database deployments.

   Shared Buffers
      An area of PostgreSQL's shared memory used to cache frequently
      accessed data pages in RAM.  Typically configured to about 25%
      of system memory.

   SQLAlchemy
      A popular Python SQL toolkit and Object-Relational Mapper (ORM)
      that provides a high-level interface for interacting with
      relational databases including PostgreSQL.

   Storage Hierarchy
      An organized, tiered structure for data storage designed to
      balance speed, cost, and capacity.  Levels range from
      :term:`primary <Primary Storage>` (fastest, most expensive)
      through :term:`quaternary <Quaternary Storage>` (slowest,
      cheapest).

   Primary Storage
      The fastest and most expensive tier in a :term:`Storage
      Hierarchy`, consisting of volatile memory (CPU cache, RAM,
      registers) with nanosecond access times.

   Secondary Storage
      The tier below primary in a :term:`Storage Hierarchy`,
      consisting of non-volatile persistent media (SSD, HDD, NVMe)
      with microsecond-to-millisecond access times.

   Tertiary Storage
      A mid-tier in a :term:`Storage Hierarchy` used for nearline
      archival and backup (tape libraries, cloud nearline storage).
      Access times range from seconds to minutes.


.. _t1-glossary-t:

T
=

.. glossary::

   Transaction
      A sequence of one or more database operations treated as a
      single logical unit of work.  Transactions in PostgreSQL follow
      the :term:`ACID` properties.


.. _t1-glossary-w:

W
=

.. glossary::

   WAL
      **Write-Ahead Log** — a mechanism used by PostgreSQL to ensure
      durability.  All changes are first written to a sequential log
      file before being applied to the actual data files, enabling
      crash recovery and point-in-time restore.