====================================================
Glossary
====================================================

This glossary covers all key terms from the ENPM818T course. Entries are
organized alphabetically across all lectures. Click any letter to jump to
that section.

:ref:`A <g-a>` · :ref:`B <g-b>` · :ref:`C <g-c>` · :ref:`D <g-d>` ·
:ref:`E <g-e>` · :ref:`F <g-f>` · :ref:`G <g-g>` · :ref:`I <g-i>` ·
:ref:`J <g-j>` · :ref:`K <g-k>` · :ref:`L <g-l>` · :ref:`M <g-m>` ·
:ref:`N <g-n>` · :ref:`O <g-o>` · :ref:`P <g-p>` · :ref:`R <g-r>` ·
:ref:`S <g-s>` · :ref:`T <g-t>` · :ref:`U <g-u>` · :ref:`V <g-v>` ·
:ref:`W <g-w>`

.. only:: html

   .. raw:: html

      <div id="glossary-search-wrap" style="margin: 1.2em 0 1.4em 0;">
        <input
          id="glossary-search"
          type="search"
          placeholder="Filter terms..."
          autocomplete="off"
          spellcheck="false"
          style="
            width: 100%;
            max-width: 480px;
            padding: 0.45em 0.75em;
            font-size: 1em;
            border: 1px solid #ccc;
            border-radius: 4px;
            box-sizing: border-box;
          "
        />
        <span
          id="glossary-search-count"
          style="margin-left: 0.8em; font-size: 0.88em; color: #666;"
        ></span>
      </div>

      <script>
      (function () {
        /* Run after the DOM is ready. */
        function initGlossarySearch() {
          var input  = document.getElementById('glossary-search');
          var count  = document.getElementById('glossary-search-count');
          if (!input) return;

          /* Collect every letter section.
             Each section has the pattern:
               <section id="glossary-X"> or <div id="glossary-X">
                 <h2>X</h2>
                 <dl class="glossary"> ... </dl>
               </section>
             We work at the <dt> level and bubble up to hide empty sections. */

          function getLetterSection(el) {
            /* Walk up until we find the element whose id starts with "glossary-" */
            var node = el;
            while (node && node !== document.body) {
              if (node.id && /^glossary-[a-z]$/i.test(node.id)) return node;
              node = node.parentElement;
            }
            return null;
          }

          function run() {
            var query = input.value.trim().toLowerCase();

            /* All term headings rendered by .. glossary:: */
            var allDt = document.querySelectorAll('dl.glossary dt');
            var visible = 0;

            allDt.forEach(function (dt) {
              /* Each <dt> may have one or more <dd> siblings that follow it
                 until the next <dt>. Collect them so we hide/show together. */
              var siblings = [];
              var node = dt.nextElementSibling;
              while (node && node.tagName === 'DD') {
                siblings.push(node);
                node = node.nextElementSibling;
              }

              var text = dt.textContent.toLowerCase();
              var match = !query || text.indexOf(query) !== -1;

              dt.style.display = match ? '' : 'none';
              siblings.forEach(function (dd) { dd.style.display = match ? '' : 'none'; });
              if (match) visible++;
            });

            /* Hide letter-section headings and their <dl> when every term
               inside them is hidden. */
            var allDl = document.querySelectorAll('dl.glossary');
            allDl.forEach(function (dl) {
              var anyVisible = Array.prototype.some.call(
                dl.querySelectorAll('dt'),
                function (dt) { return dt.style.display !== 'none'; }
              );
              dl.style.display = anyVisible ? '' : 'none';

              /* Hide the heading (h2) that immediately precedes the dl */
              var section = getLetterSection(dl);
              if (section) {
                section.style.display = anyVisible ? '' : 'none';
              } else {
                /* Fallback: hide the nearest preceding h2 */
                var prev = dl.previousElementSibling;
                while (prev) {
                  if (prev.tagName === 'H2' || prev.tagName === 'H1') {
                    prev.style.display = anyVisible ? '' : 'none';
                    break;
                  }
                  prev = prev.previousElementSibling;
                }
              }
            });

            /* Update result count */
            if (query) {
              count.textContent = visible === 1
                ? '1 term found'
                : visible + ' terms found';
            } else {
              count.textContent = '';
            }
          }

          input.addEventListener('input', run);

          /* Also clear on Escape */
          input.addEventListener('keydown', function (e) {
            if (e.key === 'Escape') { input.value = ''; run(); input.blur(); }
          });
        }

        if (document.readyState === 'loading') {
          document.addEventListener('DOMContentLoaded', initGlossarySearch);
        } else {
          initGlossarySearch();
        }
      })();
      </script>
      
----


.. _g-a:

A
=

.. glossary::

   ACCESS EXCLUSIVE Lock
      The strongest PostgreSQL table lock, acquired by operations such as
      ``DROP TABLE`` and some ``ALTER TABLE`` variants. Blocks all concurrent
      access including reads. Should be held as briefly as possible in
      production environments.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Aggregation
      A higher-level abstraction in EER modeling that treats a relationship
      between entities as a single higher-level entity. Allows relationships
      to participate in other relationships. Represented by a rectangle
      around the relationship diamond.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   ALTER TABLE
      A DDL statement that modifies the structure of an existing table
      without dropping it. Supports adding or dropping columns and
      constraints, renaming columns or constraints, changing column types,
      and setting or removing defaults. Some operations are instant
      (metadata-only); others trigger a full table rewrite.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Alternate Key
      A candidate key that was not chosen as the primary key. Remains a
      valid unique identifier and is typically enforced with a ``UNIQUE``
      constraint.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Anomaly
      A side effect of poor table design that causes data integrity problems.
      Three types exist: insertion anomaly (cannot add data without unrelated
      data), deletion anomaly (removing data causes unintended loss of other
      data), and update anomaly (changing data requires modifying multiple
      rows).
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Armstrong's Axioms
      A set of three inference rules (reflexivity, augmentation, transitivity)
      for deriving functional dependencies. Proven to be both sound (every
      derived FD is true) and complete (every true FD can be derived).
      Published by William W. Armstrong in 1974.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Attribute
      A property or characteristic of an entity or relationship. Types include
      simple, composite, multi-valued, derived, and key attributes. Represented
      in Chen notation by an ellipse connected to its entity or relationship.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Attribute Closure
      The set of all attributes that a given set of attributes :math:`X`
      functionally determines under a set of FDs :math:`F`, written
      :math:`X^{+}`. Computed by iteratively applying FDs until no new
      attributes can be added. Used to test superkeys, candidate keys, and
      FD implication.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Augmentation
      Armstrong's second axiom: if :math:`X \to Y`, then :math:`XZ \to YZ`
      for any attribute set :math:`Z`. Adding attributes to both sides of an
      FD preserves its validity.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`


.. _g-b:

B
=

.. glossary::

   BCNF (Boyce-Codd Normal Form)
      A relation is in BCNF if for every non-trivial FD :math:`X \to Y`,
      :math:`X` is a superkey. Stricter than 3NF: eliminates all FD-based
      anomalies but may not preserve all dependencies during decomposition.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   BCNF Decomposition
      A top-down decomposition algorithm that starts with a relation :math:`R`
      and repeatedly splits it on BCNF violations until every resulting
      relation has only superkey determinants. Guarantees lossless join at
      every step but does not guarantee dependency preservation.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Binary Relationship
      A relationship involving exactly two entity types. The most common
      relationship arity in ER modeling.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   btree_gist
      A PostgreSQL extension that provides GiST index operator classes for
      standard data types such as integers and text. Required when using
      ``EXCLUDE USING GIST`` with a mix of range types and scalar equality
      columns.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-c:

C
=

.. glossary::

   Candidate Key
      A minimal superkey: a set of attributes whose closure equals the entire
      relation, and from which no attribute can be removed while preserving
      that property. A relation may have multiple candidate keys. One is
      designated the primary key; the rest are alternate keys.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Canonical Cover
      An equivalent, simplified version of an FD set :math:`F` with three
      properties: every right-hand side is a single attribute, no left-hand
      side contains extraneous attributes, and no FD is redundant. Also
      called a minimal cover. Computed via a three-step algorithm: decompose,
      reduce left sides, remove redundant FDs.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Cardinality Ratio
      Specifies the maximum number of relationship instances one entity can
      participate in: 1:1, 1:N, or M:N. Expressed in Chen notation as labels
      on the lines connecting entities to relationships.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   CASCADE (DROP)
      A modifier for ``DROP TABLE`` and ``TRUNCATE`` that automatically
      removes or truncates all dependent objects (tables with FK constraints
      referencing the target). Use with caution: silent propagation can
      destroy data in unrelated tables.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   CASCADE (FK)
      An ``ON DELETE`` or ``ON UPDATE`` referential action that propagates
      the parent change to all child rows automatically. Use when child rows
      are owned by the parent and have no meaningful existence without it.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Catalog View
      A read-only virtual table maintained by the database engine that
      exposes metadata about the database itself: tables, columns,
      constraints, indexes, sequences, and more. Queried with an ordinary
      ``SELECT`` statement; no special tool or privilege is required. Two
      families exist: ``information_schema`` (SQL standard, portable) and
      ``pg_catalog`` (PostgreSQL-specific, more detail).
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Category (Union Type)
      An EER construct where a subtype entity is a member of the union of
      two or more supertype entity classes. Each category instance is related
      to exactly one of the supertype entities. In SQL, implemented using the
      exclusive-arc CHECK pattern.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   CHAR(n)
      A fixed-length character type. Values shorter than n characters are
      right-padded with spaces. Appropriate for genuine fixed-width codes
      such as US state abbreviations (``CHAR(2)``) or ZIP codes (``CHAR(5)``).
      Avoid for general-purpose strings.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   CHECK Constraint
      A constraint that evaluates a Boolean expression for every inserted or
      updated row. The row is accepted if the expression is ``TRUE`` or
      ``NULL``; it is rejected only if the expression is definitively
      ``FALSE``. Must be paired with ``NOT NULL`` to block null values.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Chen Notation
      The original ER diagram notation introduced by Peter Chen in 1976.
      Uses rectangles for entities, diamonds for relationships, ellipses for
      attributes, and lines for participation. Cardinality is expressed as
      ratio labels (1, N, M) on relationship lines.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Completeness Constraint
      An EER constraint that specifies whether every superclass entity must
      belong to at least one subclass. Total specialization (double line in
      Chen notation) means every superclass entity must be in a subclass.
      Partial specialization (single line) means membership is optional.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Composite Attribute
      An attribute that can be subdivided into smaller subparts, each with
      independent meaning. Example: ``address`` composed of ``street``,
      ``city``, ``state``, and ``zip``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Composite Key
      A primary key consisting of two or more attributes whose combined values
      uniquely identify each entity instance.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   Creation Order
      The required sequencing when creating tables with FK relationships:
      parent tables must exist before child tables can reference them.
      Circular FK dependencies require at least one deferrable constraint
      to break the ordering requirement.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Crow's Foot Notation
      A widely used ER diagramming style that represents cardinality and
      participation using crow's foot symbols (many), single lines (one),
      and circle/bar modifiers (optional/mandatory). Standard in tools such
      as Lucidchart, draw.io, and DataGrip.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-d:

D
=

.. glossary::

   Data Management
      The practice of organizing, storing, and maintaining data throughout
      its lifecycle. Encompasses five key stages: creation and ingestion,
      storage and organization, processing and retrieval, analysis and
      presentation, and archival and deletion. Supports decision-making,
      regulatory compliance, performance, cost efficiency, and security.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Database
      An organized collection of structured data, typically stored
      electronically in a computer system. Distinct from the software
      (DBMS) used to manage it: the database is the actual data, organized
      according to a schema.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Database Management System (DBMS)
      Software that interacts with users, applications, and the database to
      capture, store, and analyze data. Responsibilities include query
      processing, transaction management (ACID), concurrency control,
      security and access control, and backup and recovery. Examples:
      PostgreSQL, MySQL, MongoDB, Redis, Neo4j.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   DAS (Direct-Attached Storage)
      Storage physically connected directly to a single server or workstation
      without any network in between. Provides block-level access via SATA,
      SAS, USB, or NVMe. Lowest latency storage option; cannot be shared
      across servers. Best suited for development environments and
      single-server deployments.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   DDL (Data Definition Language)
      The SQL sublanguage for creating, modifying, and removing database
      structure. Key commands: ``CREATE TABLE``, ``ALTER TABLE``,
      ``DROP TABLE``, ``TRUNCATE``. Changes made by DDL affect the schema,
      not the data.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   DEFERRABLE INITIALLY DEFERRED
      A constraint deferral mode that moves the constraint check from
      statement end to transaction commit for every transaction. Used to
      resolve circular FK dependencies where no valid insert order exists
      with immediate checking.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   DEFERRABLE INITIALLY IMMEDIATE
      A constraint deferral mode where the check fires at statement end by
      default. Individual transactions can opt in to deferral using
      ``SET CONSTRAINTS constraint_name DEFERRED``. Use when deferral is
      the exception rather than the rule.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Decomposition
      The process of splitting a relation into two or more smaller relations
      to eliminate normalization violations. A good decomposition is lossless
      (no spurious tuples) and ideally dependency-preserving.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Decomposition Rule
      A shortcut derived from Armstrong's axioms: if :math:`X \to YZ`, then
      :math:`X \to Y` and :math:`X \to Z`. Allows splitting a compound
      right-hand side into individual FDs.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   DELETE
      A DML statement that removes specific rows matching a ``WHERE`` clause.
      Fires row-level triggers, generates a WAL entry per row, and is
      rollbackable. Slow on large tables compared to ``TRUNCATE``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Deletion Anomaly
      An anomaly where removing a tuple causes the unintended loss of other
      information. Example: deleting the last enrollment for a course also
      removes all course data when course and enrollment information are
      stored in the same table.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Denormalization
      The intentional introduction of redundancy into a normalized schema to
      improve read performance. Common techniques include materialized views,
      redundant columns, summary tables, and stored derived attributes. Should
      only be applied after profiling identifies proven bottlenecks.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Dependency Preservation
      A property of a decomposition where every FD in the original set can
      be checked within at least one decomposed relation without joining
      tables. Guaranteed by 3NF synthesis but not always by BCNF
      decomposition.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Derived Attribute
      An attribute whose value can be computed from other stored attributes.
      Represented in Chen notation by a dashed ellipse. Example: ``age``
      derived from ``date_of_birth``.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Determinant
      The left-hand side (:math:`X`) of a functional dependency
      :math:`X \to Y`. The attribute(s) whose values determine the values
      of the dependent.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Discriminator
      In Crow's Foot notation, the column used to distinguish between
      subtypes in a category (union type) mapping. Holds a value identifying
      which supertype table a given category row references, enabling
      efficient querying without inspecting all nullable FK columns.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Disjointness Constraint
      An EER constraint that specifies whether an entity can belong to more
      than one subclass simultaneously. Disjoint (d): an entity belongs to
      at most one subclass. Overlapping (o): an entity may belong to multiple
      subclasses at the same time.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   DROP TABLE
      A DDL statement that removes a table entirely: its structure, data,
      constraints, and indexes. Not reversible outside a transaction.
      ``DROP TABLE IF EXISTS`` prevents an error if the table is already
      absent. ``DROP TABLE ... CASCADE`` removes dependent objects.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-e:

E
=

.. glossary::

   EER (Extended Entity-Relationship) Model
      An extension of the basic ER model that adds constructs for modeling
      inheritance and union types: specialization, generalization, aggregation,
      and categories. Used when the domain has clear hierarchical or
      cross-hierarchy relationships that the basic ER model cannot express
      cleanly.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Entity
      A real-world object or concept with an independent existence that is
      distinguishable from other objects. Represented in Chen notation by
      a rectangle.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Entity Type
      A collection of entities with the same attributes and structure.
      Corresponds to a table in the relational model.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   ER Diagram (ERD)
      Entity-Relationship Diagram. A graphical representation of the entities,
      attributes, and relationships in a domain. The primary output of
      conceptual data modeling.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   ETL (Extract-Transform-Load)
      A process for populating denormalized OLAP schemas from normalized OLTP
      sources. Extracts data from the source, transforms it (aggregation,
      joining, cleaning), and loads it into a data warehouse. Enables a
      hybrid approach: normalized writes, denormalized reads.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   EXCLUDE Constraint
      A PostgreSQL-specific constraint that generalizes ``UNIQUE`` from
      equality to any binary operator. Rejects a new row if any existing
      row satisfies all specified operator conditions simultaneously. Requires
      a GiST index (``EXCLUDE USING GIST``). Common use: prevent overlapping
      date or time ranges for a shared resource.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Exclusive-Arc Pattern
      The SQL implementation of a category (union type): one nullable FK
      column per possible supertype, plus a ``CHECK`` constraint that asserts
      exactly one FK is non-null at any time. The check casts each
      ``IS NOT NULL`` test to ``INT`` and verifies the sum equals 1.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Extraneous Attribute
      An attribute on the left side of an FD that can be removed without
      changing the FD's effect. Detected during canonical cover computation
      by checking if the remaining left-side attributes still determine the
      right side.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`


.. _g-f:

F
=

.. glossary::

   First Normal Form (1NF)
      A relation is in 1NF if every attribute contains only atomic
      (indivisible) values. No repeating groups, no nested relations, and
      no multi-valued attributes are permitted. The baseline requirement
      for all higher normal forms.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   FLOAT
      A binary floating-point type (aliases: ``REAL``, ``DOUBLE PRECISION``).
      Cannot represent most decimal fractions exactly. Never use for GPA,
      monetary amounts, or any value where equality comparison or exact
      decimal precision matters. Use ``NUMERIC(p,s)`` instead.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   FOREIGN KEY
      A constraint that enforces referential integrity between a child column
      and a parent column declared as ``PRIMARY KEY`` or ``UNIQUE``. Inserts
      or updates that would leave the child referencing a non-existent parent
      row are rejected immediately. ``ON DELETE`` and ``ON UPDATE`` clauses
      control what happens to child rows when the parent changes.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   Foreign Key
      An attribute (or set of attributes) in a relation whose values must
      match the primary key of another relation (or the same relation). The
      mechanism for implementing relationships in the relational model.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Functional Dependency (FD)
      A constraint :math:`X \to Y` stating that for any two tuples with the
      same values on all attributes in :math:`X`, their values on all
      attributes in :math:`Y` must also be the same. Derived from business
      rules, not from inspecting data. The foundation of all normalization
      decisions.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`


.. _g-g:

G
=

.. glossary::

   GENERATED ALWAYS AS IDENTITY
      The SQL standard (SQL:2003) mechanism for auto-incrementing columns.
      The engine owns the column: explicit value inserts are rejected unless
      ``OVERRIDING SYSTEM VALUE`` is specified. Supports custom sequence
      parameters inline (``START WITH``, ``INCREMENT BY``). Preferred over
      ``SERIAL`` for all new schemas.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Generalization
      A bottom-up EER process that combines entity types sharing common
      attributes into a higher-level supertype. The inverse of specialization.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   GiST Index
      Generalized Search Tree index. The only PostgreSQL index type that
      supports multi-column operator exclusion, required by
      ``EXCLUDE USING GIST`` constraints. Also used for full-text search
      and geometric types.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-i:

I
=

.. glossary::

   Identity Column
      A column whose values are automatically generated by the database engine
      using a sequence. Declared with ``GENERATED ALWAYS AS IDENTITY``
      (SQL standard) or the legacy ``SERIAL`` shorthand. The sequence is
      owned by the column and can be customized with ``START WITH`` and
      ``INCREMENT BY``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Identifying Relationship
      A relationship that connects a weak entity to its owner (strong) entity
      and provides the weak entity with its partial identity. Represented in
      Chen notation by a double diamond. A weak entity instance cannot be
      uniquely identified without its owner.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   information_schema
      A SQL-standard set of read-only catalog views available in PostgreSQL
      (and other RDBMS) that expose metadata about tables, columns,
      constraints, and referential actions. Portable across database systems.
      Key views: ``tables``, ``columns``, ``table_constraints``,
      ``referential_constraints``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Insertion Anomaly
      An anomaly where a new fact cannot be inserted into the database without
      also supplying unrelated data. Example: a new course cannot be added to
      an unnormalized enrollment table unless at least one student is enrolled
      in it, because the student ID is part of the primary key.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   ISA Hierarchy
      A generalization relationship where subtypes inherit the identity and
      common attributes of a supertype. Implemented in SQL using the shared-PK
      strategy: the subtype PK column receives the same value as the supertype
      PK and is simultaneously a FK referencing the supertype.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   ISA Relationship (Is-A)
      The inheritance relationship between a supertype and its subtypes in an
      EER hierarchy. Denoted by a triangle labeled "ISA" or "d" (disjoint)
      or "o" (overlapping).
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-j:

J
=

.. glossary::

   Junction Table
      A table used to implement a many-to-many relationship in the relational
      model. Contains at minimum the primary keys of both participating
      entities as foreign keys, forming a composite primary key.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-k:

K
=

.. glossary::

   Key Attribute
      An attribute or set of attributes that uniquely identifies each entity
      instance within an entity type. Represented in Chen notation by an
      underlined ellipse.
      :doc:`L2 </lectures/lecture2/l2_lecture>`


.. _g-l:

L
=

.. glossary::

   Logical Schema
      The relational representation of a conceptual ERD: tables, columns,
      primary keys, and foreign keys, expressed in terms of relations rather
      than implementation details. Does not specify data types, constraints,
      or creation order. The input to physical modeling.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   Lookup Table
      A small reference table that stores a fixed set of valid values for a
      column in another table. Enforces a controlled vocabulary via a foreign
      key constraint. More flexible than a CHECK IN(...) constraint when the
      vocabulary needs to change at runtime.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Lossless Join
      A property of a decomposition ensuring that joining the decomposed
      relations exactly reconstructs the original relation with no spurious
      tuples. Tested by checking that the common attributes of the decomposed
      relations form a superkey of at least one side. Required for every valid
      decomposition.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`


.. _g-m:

M
=

.. glossary::

   Many-to-Many Relationship (M:N)
      A relationship where one instance of entity A can be associated with
      many instances of entity B, and vice versa. Implemented in the
      relational model using a junction table.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   Materialized View
      A database object that stores the result of a query as a physical table.
      Used as a denormalization technique to precompute expensive joins or
      aggregations. Must be refreshed periodically or on demand to stay
      current.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   MVCC (Multi-Version Concurrency Control)
      A PostgreSQL concurrency mechanism that maintains multiple versions of
      rows to allow readers and writers to proceed without blocking each
      other. Readers see a consistent snapshot of the database as of the
      start of their transaction; writers create new row versions rather than
      overwriting existing ones. Dead row versions are reclaimed by autovacuum.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Multivalued Attribute
      An attribute that can have more than one value for a single entity
      instance. Represented in Chen notation by a double ellipse. Example:
      ``phone_numbers`` for a person. Mapped to a separate table in the
      relational model.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-n:

N
=

.. glossary::

   NAS (Network-Attached Storage)
      A dedicated file server connected to a standard Ethernet network that
      provides file-level storage to multiple clients simultaneously via NFS
      or SMB/CIFS protocols. Higher latency than DAS; not recommended as the
      primary storage for databases due to file-level access semantics.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Natural Key
      A primary key derived from real-world business data that already
      uniquely identifies an entity (e.g., SSN, ISBN, email). Carries
      semantic meaning but may change over time and can be lengthy.
      Recommended only as an alternate key with a ``UNIQUE`` constraint;
      surrogate keys are preferred as the physical PK.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   NO ACTION
      The default ``ON DELETE`` / ``ON UPDATE`` referential action. Rejects
      the parent change if child rows exist, checked at the end of the
      statement (or at ``COMMIT`` for deferred constraints). Functionally
      similar to ``RESTRICT`` but deferrable.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Non-Prime Attribute
      An attribute that does not belong to any candidate key. Non-prime
      attributes are the focus of 2NF and 3NF tests: they must not be
      partially or transitively dependent on a candidate key.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Non-Trivial FD
      A functional dependency :math:`X \to Y` where :math:`Y` contains at
      least one attribute not already in :math:`X` (i.e.,
      :math:`Y \not\subseteq X`). These encode real business constraints and
      are the FDs that matter for normalization.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Normal Form
      A classification of a relation schema based on the types of FDs it
      allows. The hierarchy is: 1NF :math:`\subset` 2NF :math:`\subset`
      3NF :math:`\subset` BCNF. Each level eliminates a broader class of
      anomalies.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   NOT NULL
      A column-level constraint that requires every row to supply a value for
      the column. Every column is nullable by default; ``NOT NULL`` is an
      explicit opt-in. Must be paired with ``CHECK`` constraints to fully
      enforce value-range business rules.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   NOT VALID
      A modifier for ``ADD CONSTRAINT`` that adds the constraint to the table
      without scanning existing rows. New inserts and updates are checked
      immediately; existing rows are assumed valid and checked later via
      ``VALIDATE CONSTRAINT``. Used in the safe four-step migration pattern
      to minimize lock duration.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   NULL
      The absence of a known value; not the same as zero or empty string.
      Participates in three-valued logic (TRUE, FALSE, NULL): any comparison
      involving ``NULL`` always produces a null result. This is why ``CHECK``
      constraints alone do not block ``NULL`` and why ``UNIQUE`` allows
      multiple ``NULL`` values.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   NULLS NOT DISTINCT
      A PostgreSQL 15+ modifier for ``UNIQUE`` constraints that treats
      ``NULL`` as a comparable value. With this modifier, at most one
      ``NULL`` is allowed in the column. Without it, multiple ``NULL``s are
      permitted because ``NULL`` is never equal to ``NULL`` in standard SQL.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   NUMERIC(p,s)
      An exact decimal type with p total digits and s digits after the decimal
      point. Stores values without binary rounding error. Required for GPA,
      monetary amounts, and any column where exact decimal precision and
      reliable equality comparison are needed.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-o:

O
=

.. glossary::

   Object Storage
      A storage architecture that manages data as discrete objects, each
      consisting of the data itself, metadata, and a unique identifier.
      Uses a flat namespace accessed via HTTP/REST APIs. Virtually unlimited
      scalability and 11-nines durability. Not suitable for direct database
      use due to high latency; ideal for backups, media, and large datasets.
      Examples: AWS S3, Google Cloud Storage, Azure Blob Storage.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   OLAP (Online Analytical Processing)
      A workload pattern characterized by complex, ad-hoc read queries,
      aggregations, and batch updates. Typically uses denormalized schemas
      (star or snowflake) optimized for reads. Example: enrollment analytics
      dashboard.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   OLTP (Online Transaction Processing)
      A workload pattern characterized by fast, simple writes and reads with
      strong data integrity requirements. Typically uses normalized schemas
      (3NF or BCNF). Example: course registration system.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   ON DELETE
      A clause in a ``FOREIGN KEY`` definition that specifies what happens
      to child rows when the referenced parent row is deleted. Options:
      ``NO ACTION`` (default), ``RESTRICT``, ``CASCADE``, ``SET NULL``,
      ``SET DEFAULT``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   One-to-Many Relationship (1:N)
      A relationship where one instance of entity A can be associated with
      many instances of entity B, but each instance of B is associated with
      at most one instance of A. The most common relationship type in
      normalized schemas.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   One-to-One Relationship (1:1)
      A relationship where each instance of entity A is associated with at
      most one instance of entity B, and vice versa. Often indicates that
      two entity types could be merged, or that an ISA hierarchy is present.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   OVERRIDING SYSTEM VALUE
      A clause in an ``INSERT`` statement that bypasses the ``GENERATED ALWAYS``
      guard and allows an explicit value to be written to an identity column.
      Used for database restores and migrations where original IDs must be
      preserved. Does not advance the sequence counter; a ``setval()`` call
      is required afterward.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-p:

P
=

.. glossary::

   Partial Dependency
      A functional dependency where a non-prime attribute depends on only part
      of a composite candidate key. Violates 2NF. Example: ``course_id``
      :math:`\to` ``title`` in a relation with composite key
      {``course_id``, ``section_no``}.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Partial Specialization
      An EER completeness constraint where not every superclass entity needs
      to belong to a subclass. An entity may exist solely as a supertype
      instance. Represented by a single line between the supertype and the
      specialization circle in Chen notation.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Participation Constraint
      Specifies whether every entity in an entity type must participate in a
      relationship. Total participation (mandatory) is shown as a double line
      in Chen notation; partial participation (optional) as a single line.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   pg_catalog
      A PostgreSQL-specific set of system catalog tables and views that expose
      detailed internal metadata not available in ``information_schema``.
      Useful for inspecting partial indexes, storage parameters, sequence
      state, and constraint validation status. Key views: ``pg_sequences``,
      ``pg_indexes``, ``pg_constraint``, ``pg_stat_user_tables``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Physical Model
      The implementation-ready specification of a database schema: exact data
      types, constraint definitions, creation order, and PostgreSQL-specific
      features. The output of translating a logical schema into SQL
      ``CREATE TABLE`` statements.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Prime Attribute
      An attribute that belongs to at least one candidate key. Prime attributes
      are exempt from certain normalization rules (the 3NF escape clause).
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   PRIMARY KEY
      A constraint that combines ``NOT NULL`` and ``UNIQUE`` on one or more
      columns. Uniquely identifies every row in a table. May be declared at
      the column level (single-attribute PKs) or at the table level (required
      for composite PKs and named constraints). Each table may have at most
      one primary key.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   Primary Key
      The chosen candidate key used to uniquely identify each tuple in a
      relation. Values must be unique and non-null. Corresponds to the
      ``PRIMARY KEY`` constraint in SQL.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   psql
      The PostgreSQL interactive command-line client. Provides SQL execution
      and meta-commands prefixed with ``\`` (e.g., ``\d``, ``\dt``, ``\ds``)
      that are processed by the client and never sent to the server. Essential
      for inspecting schema structure, constraint names, sequence state, and
      FK dependencies during development.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-r:

R
=

.. glossary::

   Redundancy
      The storage of the same fact in multiple places within a database.
      Causes update anomalies (inconsistency risk), wasted storage, and
      maintenance complexity. Normalization eliminates redundancy;
      denormalization intentionally reintroduces it.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Redundant FD
      A functional dependency that can be derived from the other FDs in the
      set using Armstrong's axioms. Removed during canonical cover computation
      because it adds no information.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Referential Integrity
      The constraint that every foreign key value in a child table must match
      an existing primary key value in the parent table, or be NULL. Enforced
      by the ``FOREIGN KEY`` constraint in SQL.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   Reflexivity
      Armstrong's first axiom: if :math:`Y \subseteq X`, then
      :math:`X \to Y`. A set of attributes always determines any of its
      subsets. This is why trivial FDs are always true.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Relation Instance
      A specific set of tuples conforming to a relation schema at a point in
      time. Changes with every ``INSERT``, ``UPDATE``, or ``DELETE``. The
      current state of the table -- the actual data that exists right now --
      as opposed to the structural definition (relation schema).
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Relation Schema
      The structural definition of a relation: the relation name, its
      attribute names, and their domains. The blueprint for a table, as
      opposed to the relation instance (the actual current data). Analogous
      to a class definition in object-oriented programming.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Relational Model
      A data model that organizes data into relations (tables) consisting of
      tuples (rows) and attributes (columns). Based on mathematical set
      theory. Introduced by E.F. Codd in 1970.
      :doc:`L3 </lectures/lecture3/l3_lecture>`

   Relationship
      An association among two or more entity instances. Represented in Chen
      notation by a diamond. Can have attributes of its own.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Relationship Type
      A set of relationships with the same structure and semantics among the
      same entity types.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   RESTART IDENTITY
      A modifier for ``TRUNCATE`` that resets the identity sequence to its
      start value after removing all rows. Use when reloading a table from
      scratch and clean sequential IDs are required from the next insert.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   RESTRICT
      An ``ON DELETE`` / ``ON UPDATE`` referential action that rejects the
      parent change immediately (at statement time, not deferred) if child
      rows exist. Stricter timing than ``NO ACTION``; cannot be declared
      ``DEFERRABLE``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-s:

S
=

.. glossary::

   SAN (Storage Area Network)
      A dedicated high-speed network that connects servers to a shared pool
      of storage devices, providing block-level access via Fibre Channel or
      iSCSI. Appears to each server as a local disk. High performance and
      low latency; supports clustering and failover. The preferred storage
      architecture for enterprise database deployments.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Second Normal Form (2NF)
      A relation is in 2NF if it is in 1NF and no non-prime attribute is
      partially dependent on any candidate key. Violations can only occur
      with composite candidate keys.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Sequence
      A named database object that produces a strictly increasing series of
      integers on demand. Every call to ``nextval()`` is atomic: concurrent
      sessions never receive the same value. Used as the backing mechanism
      for identity columns (``GENERATED ALWAYS AS IDENTITY``) and the legacy
      ``SERIAL`` type.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   SERIAL
      A legacy PostgreSQL shorthand for ``INTEGER`` with a sequence-backed
      ``DEFAULT``. Creates a sequence and wires it as a column default.
      Explicit value inserts are silently accepted, which can desynchronize
      the sequence and cause duplicate key errors later. Superseded by
      ``GENERATED ALWAYS AS IDENTITY``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   SET DEFAULT
      An ``ON DELETE`` / ``ON UPDATE`` referential action that resets the FK
      column to its declared ``DEFAULT`` value when the referenced parent row
      is deleted or updated. Requires both a ``DEFAULT`` declaration on the
      column and a valid parent row with that default value. Fails if the
      default value does not exist in the parent table.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   SET NULL
      An ``ON DELETE`` / ``ON UPDATE`` referential action that sets the FK
      column to ``NULL`` in child rows when the parent row is deleted or
      updated. Only valid when the FK column is nullable.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   SHARE UPDATE EXCLUSIVE Lock
      A PostgreSQL lock level that allows concurrent reads but blocks
      conflicting DDL. Acquired by ``VALIDATE CONSTRAINT``, making it safe
      to run on live tables without blocking readers.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Shared-PK Strategy
      The ISA implementation pattern where the subtype table's PK column
      receives the same value as the supertype PK, and the subtype PK is
      simultaneously a FK referencing the supertype. No new sequence is
      created on the subtype.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L6 </lectures/lecture6/l6_lecture>`

   Snowflake Schema
      A dimensional schema used in OLAP systems where dimension tables are
      further normalized into sub-dimension tables, forming a snowflake-like
      structure. More normalized than a star schema but requires more joins
      for queries.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Specialization
      A top-down EER process that defines subtype entity types from a
      higher-level supertype by identifying distinguishing characteristics.
      Subtypes inherit all attributes and relationships of the supertype.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Spurious Tuple
      A phantom row introduced when joining two decomposed relations whose
      shared attributes do not form a superkey of either side. The lossless
      join property prevents spurious tuples.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   SQL Sublanguage
      One of the five functional categories of SQL commands, each targeting
      a different operation type: DDL (structure), DML (row modification),
      DQL (querying), DCL (permissions), and TCL (transactions). The current
      standard is SQL:2023.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Star Schema
      A dimensional schema used in OLAP systems with a central fact table
      surrounded by denormalized dimension tables. Minimizes joins for
      read-heavy analytical queries at the cost of redundancy in the
      dimension tables.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Storage Hierarchy
      An organized structure of storage tiers designed to balance speed,
      cost, and capacity. From fastest to slowest: primary (RAM, CPU cache),
      secondary (SSD, HDD), tertiary (tape, nearline cloud), quaternary
      (cold/offline archive). Databases use primary storage for caching and
      secondary storage for persistent data files.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Strong Entity
      An entity type that has its own primary key and exists independently
      of other entity types. Drawn as a single rectangle in Chen notation.
      Contrasted with a weak entity, which depends on an owner entity for
      identification.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Subtype
      An entity type that inherits attributes from a supertype and adds its
      own distinguishing attributes. Participates in an ISA relationship.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   Summary Table
      A denormalization technique where precomputed aggregates (SUM, COUNT,
      AVG) are stored in a dedicated table. Must be maintained via triggers
      or periodic batch jobs.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Superkey
      A set of attributes whose closure equals the entire relation, meaning
      it can uniquely identify every tuple. A superkey may contain extra
      attributes beyond the minimum needed. Every candidate key is a
      superkey, but not every superkey is a candidate key.
      :doc:`L3 </lectures/lecture3/l3_lecture>` · :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Supertype
      An entity type that is generalized into one or more subtypes in an EER
      hierarchy. Contains attributes common to all subtypes.
      :doc:`L2 </lectures/lecture2/l2_lecture>` · :doc:`L3 </lectures/lecture3/l3_lecture>`

   Surrogate Key
      A system-generated primary key with no business meaning, typically an
      auto-incrementing integer or UUID. Never changes; immune to real-world
      data changes. Preferred over natural keys as the physical PK for
      stability and join performance.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-t:

T
=

.. glossary::

   Ternary Relationship
      A relationship involving exactly three entity types simultaneously.
      Requires a three-way join to query and is less common than binary
      relationships.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   TEXT
      PostgreSQL's unbounded variable-length character type. Identical in
      internal storage and performance to ``VARCHAR(n)`` without a length
      limit. The default choice for variable-length string columns where
      no maximum length business rule exists.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Third Normal Form (3NF)
      A relation is in 3NF if it is in 2NF and no non-prime attribute is
      transitively dependent on any candidate key. Equivalently, for every
      non-trivial FD :math:`X \to Y`, either :math:`X` is a superkey or
      every attribute in :math:`Y` is prime.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   3NF Synthesis
      A bottom-up decomposition algorithm that constructs relations directly
      from the canonical cover of :math:`F`, guaranteeing both lossless join
      and dependency preservation. The four steps are: (1) compute the
      canonical cover, (2) create one relation per FD (grouping FDs with
      the same left side), (3) add a candidate key relation if none of the
      resulting relations contains one, and (4) remove any relation that is
      a subset of another.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Three-Valued Logic
      The logic system used by SQL in which every Boolean expression can
      evaluate to TRUE, FALSE, or NULL (unknown). Any comparison involving
      ``NULL`` produces ``NULL``, not FALSE. Consequence: ``CHECK``
      constraints pass silently when an operand is ``NULL``, and ``WHERE``
      clauses exclude rows where the condition evaluates to ``NULL``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   TIMESTAMPTZ
      A PostgreSQL timestamp type that stores the time zone offset alongside
      the date and time. Always preferred over ``TIMESTAMP`` (without
      timezone) for event logs and audit columns. Stored as UTC internally;
      displayed in the session's configured time zone.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Total Specialization
      An EER completeness constraint where every superclass entity must
      belong to at least one subclass. No entity can exist solely as a
      supertype instance. Represented by a double line between the supertype
      and the specialization circle in Chen notation.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Transitive Dependency
      A dependency chain :math:`A \to B \to C` where :math:`B` is not a
      superkey and :math:`B \not\to A`. The non-key attribute :math:`C`
      depends on the key :math:`A` only indirectly through the middleman
      :math:`B`. Violates 3NF.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Transitivity
      Armstrong's third axiom: if :math:`X \to Y` and :math:`Y \to Z`,
      then :math:`X \to Z`. Allows chaining functional dependencies.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Trivial FD
      A functional dependency :math:`X \to Y` where :math:`Y \subseteq X`.
      Always true by reflexivity. Trivial FDs reveal no new information and
      are ignored during normalization.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   TRUNCATE
      A DDL statement that removes all rows from a table by deallocating data
      pages in bulk. Does not fire row-level triggers. Rollbackable in
      PostgreSQL. Significantly faster than ``DELETE`` on large tables. Does
      not support a ``WHERE`` clause.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Tuple
      A single row in a relation. Corresponds to an instance of the entity
      or relationship being modeled.
      :doc:`L3 </lectures/lecture3/l3_lecture>`


.. _g-u:

U
=

.. glossary::

   UNIQUE
      A constraint that enforces distinctness on non-null values across rows.
      Multiple ``NULL`` values are permitted by default (because ``NULL`` is
      never equal to ``NULL``). Use ``UNIQUE NULLS NOT DISTINCT`` (PG 15+)
      to allow at most one ``NULL``. Composite ``UNIQUE`` constraints span
      multiple columns and enforce uniqueness on the combination.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   Unary (Recursive) Relationship
      A relationship where an entity type is associated with itself. Both
      participants in the relationship are of the same entity type. Role
      labels are required on both ends to distinguish the two participant
      roles. Example: a ``COURSE`` entity that has prerequisites, also
      modeled as ``COURSE`` instances.
      :doc:`L2 </lectures/lecture2/l2_lecture>`

   Union Rule
      A shortcut derived from Armstrong's axioms: if :math:`X \to Y` and
      :math:`X \to Z`, then :math:`X \to YZ`. Allows combining FDs with
      the same determinant.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`

   Update Anomaly
      An anomaly where changing a single fact requires modifying multiple
      rows. Partial updates create inconsistency. Example: changing a
      professor's name must update every row containing that professor in an
      unnormalized enrollment table.
      :doc:`L4-L5 </lectures/lecture4-5/l4_5_lecture>`


.. _g-v:

V
=

.. glossary::

   VALIDATE CONSTRAINT
      An ``ALTER TABLE`` operation that scans existing rows to verify that all
      of them satisfy a constraint that was added with ``NOT VALID``. Acquires
      only ``SHARE UPDATE EXCLUSIVE``, allowing concurrent reads. Once
      complete, the constraint's ``convalidated`` flag is set to ``true`` in
      ``pg_constraint``.
      :doc:`L6 </lectures/lecture6/l6_lecture>`

   VARCHAR(n)
      A variable-length character type with a maximum of n characters. In
      PostgreSQL, has identical internal storage and performance to ``TEXT``.
      Use only when the length limit encodes a genuine business rule (e.g., a
      two-character state code). Do not use ``VARCHAR(255)`` out of habit;
      prefer ``TEXT`` for unbounded strings.
      :doc:`L6 </lectures/lecture6/l6_lecture>`


.. _g-w:

W
=

.. glossary::

   WAL (Write-Ahead Log)
      A PostgreSQL durability mechanism that records every change to a
      sequential log file before writing it to the actual data files. Ensures
      that committed transactions survive a crash: on recovery, PostgreSQL
      replays the WAL to restore a consistent state. Also the foundation of
      streaming replication and point-in-time recovery.
      :doc:`L1 </lectures/lecture1/l1_lecture>`

   Weak Entity Type
      An entity type that does not have its own key attribute and depends on
      a strong entity type (its owner) for identification. Represented by a
      double rectangle in Chen notation. The identifying relationship is shown
      as a double diamond. Identified by a partial key (discriminator)
      combined with the owner's primary key.
      :doc:`L2 </lectures/lecture2/l2_lecture>`
