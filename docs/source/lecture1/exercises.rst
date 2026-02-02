====================================================
Exercises
====================================================

This page contains the take-home exercises for Lecture 1.  The in-class
portion focuses on installing and configuring your environment; these
exercises ask you to **explore that environment on your own** and
document what you find.


.. dropdown:: 🖥️ Exercise 1 – Explore psql
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Verify your PostgreSQL installation and become familiar with the
    ``psql`` interactive terminal and its meta-commands.

    ----

    **Specification**

    1. Open a terminal and connect to PostgreSQL:

       .. code-block:: bash

          psql -U postgres

    2. Run each of the following meta-commands and observe the output:

       .. list-table::
          :widths: 20 60
          :header-rows: 1

          * - Command
            - Description
          * - ``\l``
            - List all databases.
          * - ``\du``
            - List all users/roles.
          * - ``\conninfo``
            - Display current connection information.
          * - ``\?``
            - Help on psql meta-commands.
          * - ``\h``
            - Help on SQL commands.
          * - ``\timing``
            - Toggle query execution timing display.
          * - ``\x``
            - Toggle expanded output mode.
          * - ``\q``
            - Quit psql.

       .. note::

          Meta-commands start with ``\`` and are processed by psql itself,
          not sent to the server.  They do not require a semicolon.

    3. While still in psql, run the following SQL statement to find your
       data directory:

       .. code-block:: sql

          SHOW data_directory;

    4. Navigate to that directory in your file manager or terminal and
       identify the following components:

       .. list-table::
          :widths: 30 60
          :header-rows: 1

          * - Directory / File
            - Purpose
          * - ``base/``
            - Database files (one subdirectory per database).
          * - ``pg_wal/``
            - Write-ahead log files (transaction logs).
          * - ``postgresql.conf``
            - Main server configuration file.
          * - ``pg_hba.conf``
            - Client authentication configuration.
          * - ``pg_ident.conf``
            - User name mapping configuration.
          * - ``postmaster.pid``
            - Process ID of running server.

       .. warning::

          Never modify files in the data directory manually while
          PostgreSQL is running.  Always use proper PostgreSQL commands or
          configuration tools.

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Screenshot 1**: Output of ``psql --version`` showing your PostgreSQL version.
    - **Screenshot 2**: psql output of the ``\l`` command showing databases.
    - **Screenshot 3**: psql output of the ``\conninfo`` command.
    - **Short Answer** (2–3 sentences): What default databases exist in
      your PostgreSQL installation?  What do you think ``template0`` and
      ``template1`` are used for?  *(Hint: check the PostgreSQL
      documentation.)*


.. dropdown:: 🗄️ Exercise 2 – Explore DataGrip
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Connect DataGrip to your local PostgreSQL instance and explore the
    graphical interface.

    ----

    **Specification**

    1. Open DataGrip and create a new PostgreSQL data source using the
       connection details from the lecture (host ``localhost``, port
       ``5432``, user ``postgres``).

    2. In the **Database Explorer** (left panel):

       - Expand your connection to see databases.
       - Navigate to ``postgres`` → **Schemas** → **public**.
       - Note the ``pg_catalog`` schema (system tables).

    3. Open a **Query Console**:

       - Right-click the ``postgres`` database → **New** → **Query Console**.
       - This is where you will write SQL queries starting next week.

    4. Explore the **Data Editor**:

       - Double-click any table inside ``pg_catalog`` to view its contents
         (read-only).
       - Try browsing ``pg_catalog.pg_database`` — this is the system table
         that stores information about every database on your server.

    5. Generate a **Database Diagram**:

       - Right-click a schema → **Diagrams** → **Show Visualization**.
       - This feature generates ER diagrams automatically.

    ----

    **Deliverables**

    Submit the following via Canvas:

    - **Screenshot 4**: DataGrip showing a successful connection to
      PostgreSQL (Database Explorer visible with expanded tree).
    - **Screenshot 5**: DataGrip Query Console open (empty is fine).


.. dropdown:: 💾 Exercise 3 – Storage Architecture Matching
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Reinforce your understanding of storage architectures by matching
    real-world scenarios to the most appropriate storage type.

    ----

    **Specification**

    Create a file ``lecture1/storage_matching.txt`` (plain text or
    Markdown) that contains your answers to the following.  For each
    scenario, state which storage architecture (DAS, NAS, SAN, Object
    Storage, or Cloud Storage) is the **best fit** and write **2–3
    sentences** explaining your reasoning.  Reference at least one
    characteristic from the lecture (e.g., access type, latency,
    scalability, cost).

    1. A solo developer running PostgreSQL on their laptop for a side
       project.
    2. A design agency where 15 employees need to access the same library
       of brand assets (images, fonts, templates) over the office network.
    3. A hospital system running an electronic health records (EHR)
       database that must guarantee sub-millisecond read latency and
       99.999% uptime.
    4. A startup that needs to store 50 TB of user-uploaded photos and
       serve them to a mobile app via an API.
    5. A machine-learning team at a university that needs GPU instances
       and a managed PostgreSQL database but has no budget for physical
       hardware.

    ----

    **Deliverables**

    Submit the following via Canvas:

    - ``lecture1/storage_matching.txt`` containing your five answers.
    - Each answer must name the architecture, give a brief justification
      (2–3 sentences), and reference a relevant characteristic.