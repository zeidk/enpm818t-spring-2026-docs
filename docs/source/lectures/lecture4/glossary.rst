====================================================
Glossary
====================================================

:ref:`A <t4-glossary-a>` · :ref:`B <t4-glossary-b>` · :ref:`C <t4-glossary-c>` · :ref:`D <t4-glossary-d>` · :ref:`E <t4-glossary-e>` · :ref:`F <t4-glossary-f>` · :ref:`L <t4-glossary-l>` · :ref:`M <t4-glossary-m>` · :ref:`N <t4-glossary-n>` · :ref:`O <t4-glossary-o>` · :ref:`P <t4-glossary-p>` · :ref:`R <t4-glossary-r>` · :ref:`S <t4-glossary-s>` · :ref:`T <t4-glossary-t>` · :ref:`U <t4-glossary-u>`

----


.. _t4-glossary-a:

A
=

.. glossary::

   Anomaly
      A side effect of poor table design that causes data integrity
      problems. Three types exist: insertion anomaly (cannot add data
      without unrelated data), deletion anomaly (removing data causes
      unintended loss of other data), and update anomaly (changing data
      requires modifying multiple rows).

   Armstrong's Axioms
      A set of three inference rules (reflexivity, augmentation,
      transitivity) for deriving functional dependencies. Proven to be
      both sound (every derived FD is true) and complete (every true FD
      can be derived). Published by William W. Armstrong in 1974.

   Attribute Closure
      The set of all attributes that a given set of attributes :math:`X`
      functionally determines under a set of FDs :math:`F`, written
      :math:`X^{+}`. Computed by iteratively applying FDs until no new
      attributes can be added. Used to test superkeys, candidate keys,
      and FD implication.

   Augmentation
      Armstrong's second axiom: if :math:`X \to Y`, then :math:`XZ \to YZ`
      for any attribute set :math:`Z`. Adding attributes to both sides of
      an FD preserves its validity.


.. _t4-glossary-b:

B
=

.. glossary::

   BCNF (Boyce-Codd Normal Form)
      A relation is in BCNF if for every non-trivial FD :math:`X \to Y`,
      :math:`X` is a superkey. Stricter than 3NF: eliminates all FD-based
      anomalies but may not preserve all dependencies during
      decomposition.


.. _t4-glossary-c:

C
=

.. glossary::

   Canonical Cover
      An equivalent, simplified version of an FD set :math:`F` with three
      properties: every right-hand side is a single attribute, no
      left-hand side contains extraneous attributes, and no FD is
      redundant. Also called a minimal cover. Computed via a three-step
      algorithm: decompose, reduce left sides, remove redundant FDs.


.. _t4-glossary-d:

D
=

.. glossary::

   Decomposition
      The process of splitting a relation into two or more smaller
      relations to eliminate normalization violations. A good
      decomposition is lossless (no spurious tuples) and ideally
      dependency-preserving.

   Deletion Anomaly
      An anomaly where removing a tuple causes the unintended loss of
      other information. Example: deleting the last enrollment for a
      course also removes all course data when course and enrollment
      information are stored in the same table.

   Denormalization
      The intentional introduction of redundancy into a normalized schema
      to improve read performance. Common techniques include materialized
      views, redundant columns, summary tables, and stored derived
      attributes. Should only be applied after profiling identifies
      proven bottlenecks.

   Dependency Preservation
      A property of a decomposition where every FD in the original set
      can be checked within at least one decomposed relation without
      joining tables. Guaranteed by 3NF synthesis but not always by BCNF
      decomposition.

   Determinant
      The left-hand side (:math:`X`) of a functional dependency
      :math:`X \to Y`. The attribute(s) whose values determine the
      values of the dependent.


.. _t4-glossary-e:

E
=

.. glossary::

   ETL (Extract-Transform-Load)
      A process for populating denormalized OLAP schemas from normalized
      OLTP sources. Extracts data from the source, transforms it
      (aggregation, joining, cleaning), and loads it into a data
      warehouse. Enables a hybrid approach: normalized writes,
      denormalized reads.

   Extraneous Attribute
      An attribute on the left side of an FD that can be removed without
      changing the FD's effect. Detected during canonical cover
      computation by checking if the remaining left-side attributes
      still determine the right side.


.. _t4-glossary-f:

F
=

.. glossary::

   Functional Dependency (FD)
      A constraint :math:`X \to Y` stating that for any two tuples with
      the same values on all attributes in :math:`X`, their values on
      all attributes in :math:`Y` must also be the same. Derived from
      business rules, not from inspecting data. The foundation of all
      normalization decisions.


.. _t4-glossary-l:

L
=

.. glossary::

   Lossless Join
      A property of a decomposition ensuring that joining the decomposed
      relations exactly reconstructs the original relation with no
      spurious tuples. Tested by checking that the common attributes of
      the decomposed relations form a superkey of at least one side.
      Required for every valid decomposition.


.. _t4-glossary-m:

M
=

.. glossary::

   Materialized View
      A database object that stores the result of a query as a physical
      table. Used as a denormalization technique to precompute expensive
      joins or aggregations. Must be refreshed periodically or on demand
      to stay current.


.. _t4-glossary-n:

N
=

.. glossary::

   Non-Prime Attribute
      An attribute that does not belong to any candidate key. Non-prime
      attributes are the focus of 2NF and 3NF tests: they must not be
      partially or transitively dependent on a candidate key.

   Non-Trivial FD
      A functional dependency :math:`X \to Y` where :math:`Y` contains at
      least one attribute not already in :math:`X` (i.e.,
      :math:`Y \not\subseteq X`). These encode real business constraints
      and are the FDs that matter for normalization.

   Normal Form
      A classification of a relation schema based on the types of FDs it
      allows. The hierarchy is: 1NF :math:`\subset` 2NF :math:`\subset`
      3NF :math:`\subset` BCNF. Each level eliminates a broader class of
      anomalies.

.. _t4-glossary-o:

O
=

.. glossary::

   OLAP (Online Analytical Processing)
      A workload pattern characterized by complex, ad-hoc read queries,
      aggregations, and batch updates. Typically uses denormalized
      schemas (star or snowflake) optimized for reads. Example:
      enrollment analytics dashboard.

   OLTP (Online Transaction Processing)
      A workload pattern characterized by fast, simple writes and reads
      with strong data integrity requirements. Typically uses normalized
      schemas (3NF or BCNF). Example: course registration system.


.. _t4-glossary-p:

P
=

.. glossary::

   Partial Dependency
      A functional dependency where a non-prime attribute depends on only
      part of a composite candidate key. Violates 2NF. Example:
      ``course_id`` :math:`\to` ``title`` in a relation with composite
      key {``course_id``, ``section_no``}.

   Prime Attribute
      An attribute that belongs to at least one candidate key. Prime
      attributes are exempt from certain normalization rules (the 3NF
      escape clause).


.. _t4-glossary-r:

R
=

.. glossary::

   Redundancy
      The storage of the same fact in multiple places within a database.
      Causes update anomalies (inconsistency risk), wasted storage, and
      maintenance complexity. Normalization eliminates redundancy;
      denormalization intentionally reintroduces it.

   Redundant FD
      A functional dependency that can be derived from the other FDs in
      the set using Armstrong's axioms. Removed during canonical cover
      computation because it adds no information.

   Reflexivity
      Armstrong's first axiom: if :math:`Y \subseteq X`, then
      :math:`X \to Y`. A set of attributes always determines any of its
      subsets. This is why trivial FDs are always true.


.. _t4-glossary-s:

S
=

.. glossary::

   Second Normal Form (2NF)
      A relation is in 2NF if it is in 1NF and no non-prime attribute is
      partially dependent on any candidate key. Violations can only occur
      with composite candidate keys.

   Summary Table
      A denormalization technique where precomputed aggregates (SUM,
      COUNT, AVG) are stored in a dedicated table. Example: average GPA
      per student per semester. Must be maintained via triggers or
      periodic batch jobs.


.. _t4-glossary-t:

T
=

.. glossary::

   Third Normal Form (3NF)
      A relation is in 3NF if it is in 2NF and no non-prime attribute is
      transitively dependent on any candidate key. Equivalently, for
      every non-trivial FD :math:`X \to Y`, either :math:`X` is a
      superkey or every attribute in :math:`Y` is prime.

   Transitive Dependency
      A dependency chain :math:`A \to B \to C` where :math:`B` is not a
      superkey and :math:`B \not\to A`. The non-key attribute :math:`C`
      depends on the key :math:`A` only indirectly through the middleman
      :math:`B`. Violates 3NF.

   Transitivity
      Armstrong's third axiom: if :math:`X \to Y` and :math:`Y \to Z`,
      then :math:`X \to Z`. Allows chaining functional dependencies.

   Trivial FD
      A functional dependency :math:`X \to Y` where :math:`Y \subseteq X`.
      Always true by reflexivity. Trivial FDs reveal no new information
      and are ignored during normalization.


.. _t4-glossary-u:

U
=

.. glossary::

   Union Rule
      A shortcut derived from Armstrong's axioms: if :math:`X \to Y` and
      :math:`X \to Z`, then :math:`X \to YZ`. Allows combining FDs with
      the same determinant.

   Update Anomaly
      An anomaly where changing a single fact requires modifying multiple
      rows. Partial updates create inconsistency. Example: changing a
      professor's name must update every row containing that professor in
      an unnormalized enrollment table.
