.. _cheat_sheet_l4:

====================================================
L4-L5 Cheat Sheet
====================================================

.. note::

   This cheat sheet is a compact reference for :doc:`L4-5 Lecture <lecture>`. It mirrors the
   lecture's section order so you can move between the two documents without
   losing your place. A printable version is also available: :download:`Normalization_Cheat_Sheet.pdf </_static/images/l4/Normalization_Cheat_Sheet.pdf>`.

.. figure:: /_static/images/l4/FLOWCHART.png
   :alt: Full normalization pipeline flowchart (Preparation, 1NF, 2NF, 3NF/BCNF, Verification)
   :align: center
   :width: 100%

   **Figure 1.** End-to-end normalization pipeline. See Box 6 (Canonical Cover) for Preparation,
   Boxes 7-11 for the normal form tests, Boxes 12-13 for the decomposition algorithms,
   and Box 14 for the Verification stage.


.. dropdown:: Box 1 -- Why Normalization Matters
   :class-container: sd-border-secondary

   **Definition**: Organizing a relational schema to reduce redundancy and improve
   data integrity by decomposing relations based on their functional dependencies.
   Each relation should represent *one fact about one entity*.

   .. rubric:: Three Anomalies (from poor table design)

   .. list-table::
      :widths: 20 80
      :header-rows: 1
      :class: compact-table

      * - Anomaly
        - Description
      * - **Insertion**
        - Cannot add data without unrelated data. E.g., cannot add a new course
          unless a section already exists.
      * - **Deletion**
        - Removing data loses unrelated facts. E.g., deleting the last section of
          a course loses the course title.
      * - **Update**
        - Changing one fact requires updating many rows; partial updates cause
          inconsistency. E.g., renaming a department requires changing every row
          that references it.


.. dropdown:: Box 2 -- Functional Dependencies (FDs)
   :class-container: sd-border-secondary

   **Definition**: A functional dependency :math:`X \to Y` states: for each value
   of :math:`X`, there is exactly one value of :math:`Y`.

   - :math:`X` = determinant (LHS), :math:`Y` = dependent (RHS).

   .. math::

      \forall\, t_1, t_2 \in r(R) : t_1[X] = t_2[X] \implies t_1[Y] = t_2[Y]

   .. warning::

      FDs come from **business rules**, not from inspecting data instances.
      A table might satisfy an FD by coincidence; only domain knowledge confirms it.

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Type
        - Definition
      * - **Trivial FD**
        - :math:`Y \subseteq X` -- always holds, useless for normalization.
      * - **Non-trivial FD**
        - :math:`Y \not\subseteq X` -- real constraint from business rules.


.. dropdown:: Box 3 -- Armstrong's Axioms
   :class-container: sd-border-secondary

   .. rubric:: Three Core Axioms (sound and complete)

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Axiom
        - Rule
      * - **Reflexivity**
        - If :math:`Y \subseteq X`, then :math:`X \to Y`.
      * - **Augmentation**
        - If :math:`X \to Y`, then :math:`XZ \to YZ`.
      * - **Transitivity**
        - If :math:`X \to Y` and :math:`Y \to Z`, then :math:`X \to Z`.

   .. rubric:: Two Derived Rules

   .. list-table::
      :widths: 25 75
      :header-rows: 1
      :class: compact-table

      * - Rule
        - Definition
      * - **Union**
        - If :math:`X \to Y` and :math:`X \to Z`, then :math:`X \to YZ`.
      * - **Decomposition**
        - If :math:`X \to YZ`, then :math:`X \to Y` and :math:`X \to Z`.

   .. card::
      :class-card: sd-border-info

      The set of all FDs derivable from :math:`F` via these rules is called
      :math:`F^+` (the closure of :math:`F`).


.. dropdown:: Box 4 -- Attribute Closure (:math:`X^+`)
   :class-container: sd-border-secondary

   **Definition**: Given FD set :math:`F` and attribute set :math:`X`, the closure
   :math:`X^+` is the set of all attributes functionally determined by :math:`X`.

   .. rubric:: Algorithm

   1. Initialize: :math:`X^+ = X`.
   2. For each FD :math:`Y \to Z` in :math:`F`: if :math:`Y \subseteq X^+`, then :math:`X^+ = X^+ \cup Z`.
   3. Repeat step 2 until no change occurs.

   .. rubric:: Three Key Uses

   .. list-table::
      :widths: 35 65
      :header-rows: 1
      :class: compact-table

      * - Use
        - How
      * - **Test if an FD holds**
        - :math:`X \to Y` holds under :math:`F` iff :math:`Y \subseteq X^+`.
      * - **Test if** :math:`X` **is a superkey**
        - :math:`X` is a superkey iff :math:`X^+ = R`.
      * - **Find candidate keys**
        - A candidate key is a minimal superkey: no proper subset is also a superkey.

   .. rubric:: Worked Example: :math:`R(A, B, C, D, E)`, :math:`F = \{A \to B,\; BC \to D,\; D \to E\}`

   .. dropdown:: Example 1: Compute :math:`\{A, C\}^+`
      :class-container: sd-border-info

      .. list-table::
         :widths: 8 30 30 32
         :header-rows: 1
         :class: compact-table

         * - Step
           - FD Applied
           - Why?
           - Closure After
         * - 0
           - (initialize)
           - Start with :math:`X`
           - :math:`\{A, C\}`
         * - 1
           - :math:`A \to B`
           - :math:`A \in \{A,C\}^+`
           - :math:`\{A, B, C\}`
         * - 2
           - :math:`BC \to D`
           - :math:`\{B,C\} \subseteq \{A,B,C\}`
           - :math:`\{A, B, C, D\}`
         * - 3
           - :math:`D \to E`
           - :math:`D \in \{A,B,C,D\}`
           - :math:`\{A, B, C, D, E\}`
         * - 4
           - (done)
           -
           -

      **Result**: :math:`\{A,C\}^+ = R` -- superkey.

   .. dropdown:: Example 2: Compute :math:`\{B, C\}^+`
      :class-container: sd-border-info

      .. list-table::
         :widths: 8 30 30 32
         :header-rows: 1
         :class: compact-table

         * - Step
           - FD Applied
           - Why?
           - Closure After
         * - 0
           - (initialize)
           -
           - :math:`\{B, C\}`
         * - 1
           - :math:`A \to B`
           - :math:`A \notin \{B,C\}` -- skip
           - :math:`\{B, C\}`
         * - 2
           - :math:`BC \to D`
           - :math:`\{B,C\} \subseteq \{B,C\}`
           - :math:`\{B, C, D\}`
         * - 3
           - :math:`D \to E`
           - :math:`D \in \{B,C,D\}`
           - :math:`\{B, C, D, E\}`
         * - 4
           - (done)
           -
           -

      **Result**: :math:`\{B,C\}^+ = \{B,C,D,E\} \neq R` -- not a superkey.

   .. dropdown:: Example 3: Compute :math:`\{A\}^+`
      :class-container: sd-border-info

      .. list-table::
         :widths: 8 30 30 32
         :header-rows: 1
         :class: compact-table

         * - Step
           - FD Applied
           - Why?
           - Closure After
         * - 0
           - (initialize)
           -
           - :math:`\{A\}`
         * - 1
           - :math:`A \to B`
           - :math:`A \in \{A\}`
           - :math:`\{A, B\}`
         * - 2
           - :math:`BC \to D`
           - :math:`C \notin \{A,B\}` -- skip
           - :math:`\{A, B\}`
         * - 3
           - :math:`D \to E`
           - :math:`D \notin \{A,B\}` -- skip
           - :math:`\{A, B\}`
         * - 4
           - (done)
           -
           -

      **Result**: :math:`\{A\}^+ = \{A,B\} \neq R` -- not a superkey.

   .. dropdown:: Example 4: Compute :math:`\{D\}^+`
      :class-container: sd-border-info

      .. list-table::
         :widths: 8 30 30 32
         :header-rows: 1
         :class: compact-table

         * - Step
           - FD Applied
           - Why?
           - Closure After
         * - 0
           - (initialize)
           -
           - :math:`\{D\}`
         * - 1
           - :math:`A \to B`
           - :math:`A \notin \{D\}` -- skip
           - :math:`\{D\}`
         * - 2
           - :math:`BC \to D`
           - :math:`\{B,C\} \not\subseteq \{D\}` -- skip
           - :math:`\{D\}`
         * - 3
           - :math:`D \to E`
           - :math:`D \in \{D\}`
           - :math:`\{D, E\}`
         * - 4
           - (done)
           -
           -

      **Result**: :math:`\{D\}^+ = \{D,E\} \neq R` -- not a superkey.


.. dropdown:: Box 5 -- Finding Superkeys & Candidate Keys
   :class-container: sd-border-secondary

   - **Superkey**: :math:`X` such that :math:`X^+ = R`.
   - **Candidate key (CK)**: A superkey where no proper subset is also a superkey (minimal).

   .. rubric:: Strategy

   1. **Identify must-have attributes**: Attributes that never appear on any RHS of any FD must be in every CK. Call this set :math:`M`.
   2. **Check if** :math:`M` **is a superkey**: Compute :math:`M^+`. If :math:`M^+ = R`, then :math:`M` is the only CK.
   3. **If not, expand** :math:`M`: For each attribute :math:`A \notin M^+`, try adding it to :math:`M` and recompute.
   4. **Minimize**: For each superkey found, verify removing any single attribute breaks :math:`X^+ = R`.
   5. **Repeat**: Try all combinations to find every CK.

   .. math::

      X \text{ is a CK iff } X^+ = R \text{ and } \forall A \in X:\; (X - \{A\})^+ \neq R.

   .. rubric:: Worked Example: :math:`R(A, B, C, D, E)`, :math:`F = \{A \to B,\; BC \to D,\; D \to E\}`

   .. card::
      :class-card: sd-border-info

      **Step 1** -- RHS attributes: :math:`\{B, D, E\}`. :math:`A` and :math:`C` never appear on any RHS, so :math:`M = \{A, C\}`.

      **Step 2** -- :math:`\{A,C\}^+ = R` (verified above). :math:`M` is a superkey.

      **Step 3** -- Test minimality: :math:`\{C\}^+ = \{C\} \neq R`; :math:`\{A\}^+ = \{A,B\} \neq R`. Neither proper subset is a superkey.

      **Step 4** -- Since :math:`M = \{A,C\}` already reaches :math:`R` and both attributes are mandatory, no other minimal combination exists.

      :math:`\therefore` The only candidate key is :math:`\{A, C\}`.


.. dropdown:: Box 6 -- Canonical Cover (:math:`F_c`)
   :class-container: sd-border-secondary

   :math:`F_c` is a **minimal, equivalent** set of FDs (same closure as :math:`F`, no redundancy).
   It is the prerequisite input for the 3NF synthesis algorithm.

   .. rubric:: Three-Step Algorithm

   .. list-table::
      :widths: 8 30 62
      :header-rows: 1
      :class: compact-table

      * - Step
        - Name
        - Action
      * - 1
        - **Decompose compound RHS**
        - Split each FD so every RHS has a single attribute: :math:`X \to YZ` becomes :math:`X \to Y` and :math:`X \to Z`.
      * - 2
        - **Reduce extraneous LHS**
        - For each FD :math:`X \to A` and each :math:`B \in X`: compute :math:`(X - \{B\})^+` under :math:`F`. If :math:`A \in (X-\{B\})^+`, then :math:`B` is extraneous -- remove it.
      * - 3
        - **Remove redundant FDs**
        - For each FD :math:`X \to A`: compute :math:`X^+` using :math:`F - \{X \to A\}`. If :math:`A \in X^+`, the FD is derivable from the rest -- remove it.

   .. rubric:: Worked Example: :math:`R(A, B, C, D)`, :math:`F = \{A \to BC,\; AB \to C,\; A \to B,\; D \to A\}`

   **Step 1 -- Decompose**: :math:`A \to BC` becomes :math:`A \to B` and :math:`A \to C`; remove duplicate :math:`A \to B`.

   :math:`F = \{A \to B,\; A \to C,\; AB \to C,\; D \to A\}`

   **Step 2 -- Reduce**: Check :math:`AB \to C`. Is :math:`B` extraneous? Compute :math:`\{A\}^+ = \{A,B,C\}`. :math:`C \in \{A,B,C\}` -- yes, :math:`B` is extraneous. :math:`AB \to C` simplifies to :math:`A \to C` (already present -- remove duplicate).

   :math:`F = \{A \to B,\; A \to C,\; D \to A\}`

   **Step 3 -- Remove redundant FDs**: Test :math:`A \to B`: under :math:`\{A \to C,\; D \to A\}`, :math:`\{A\}^+ = \{A,C\}`. :math:`B \notin \{A,C\}` -- keep. Test :math:`A \to C`: under :math:`\{A \to B,\; D \to A\}`, :math:`\{A\}^+ = \{A,B\}`. :math:`C \notin \{A,B\}` -- keep. Test :math:`D \to A`: under :math:`\{A \to B,\; A \to C\}`, :math:`\{D\}^+ = \{D\}`. :math:`A \notin \{D\}` -- keep.

   .. card::
      :class-card: sd-border-success

      :math:`\therefore F_c = \{A \to B,\; A \to C,\; D \to A\}`


.. dropdown:: Box 7 -- First Normal Form (1NF)
   :class-container: sd-border-secondary

   **Definition**: Every attribute contains only **atomic** (indivisible) values.
   No repeating groups, nested tables, or multi-valued attributes.

   .. rubric:: Steps to Test and Fix

   1. Inspect each attribute: does any cell hold multiple values (comma-separated lists, arrays, nested structures)?
   2. If yes -- violates 1NF.
   3. Decompose: remove the multi-valued attribute; create a new relation with the original PK (as FK) plus the attribute (one value per row). The PK of the new relation is the composite of both columns.

   .. rubric:: Before (violates 1NF)

   .. list-table::
      :widths: 30 30 40
      :header-rows: 1
      :class: compact-table

      * - **StudentID** (PK)
        - Name
        - Courses
      * - 101
        - Alice
        - DB, OS, AI
      * - 102
        - Bob
        - DB, Networks

   .. rubric:: After (1NF)

   **Student**\ (**StudentID**, Name) and **Student_Course**\ (**StudentID**, **Course**).


.. dropdown:: Box 8 -- Key Terminology
   :class-container: sd-border-secondary

   .. list-table::
      :widths: 30 70
      :header-rows: 1
      :class: compact-table

      * - Term
        - Definition
      * - **Prime attribute**
        - Belongs to at least one candidate key.
      * - **Non-prime attribute**
        - Not part of any candidate key; most susceptible to redundancy problems.
      * - **Full FD**
        - :math:`X \to Y` where no proper subset of :math:`X` determines :math:`Y`.
      * - **Partial FD**
        - :math:`\exists\, S \subsetneq X` such that :math:`S \to Y`. Only part of
          the LHS is needed.
      * - **Transitive dependency**
        - :math:`A \to B \to C` where :math:`B` is not a superkey and
          :math:`B \not\to A`. Attribute :math:`C` depends on the key only
          indirectly through :math:`B`.


.. dropdown:: Box 9 -- Second Normal Form (2NF)
   :class-container: sd-border-secondary

   **Definition**: 1NF + no non-prime attribute is **partially dependent** on any candidate key.
   Only relevant with composite CKs.

   .. rubric:: Steps to Test and Fix

   1. Find all candidate keys using attribute closure.
   2. Classify each attribute as prime or non-prime.
   3. For each proper subset :math:`S` of each composite CK, compute :math:`S^+`.
   4. If :math:`S^+` contains any non-prime attribute :math:`A` -- partial dependency -- violates 2NF.
   5. **Fix**: create a new relation :math:`S \cup \{A\}` with key :math:`S`; remove :math:`A` from the original.

   .. rubric:: Worked Example: :math:`R(A,B,C,D,E)`, :math:`F = \{A \to B,\; BC \to D,\; D \to E\}`

   CK = :math:`\{A,C\}`. Prime: :math:`A, C`. Non-prime: :math:`B, D, E`.

   :math:`\{A\}^+ = \{A,B\}` -- contains non-prime :math:`B`. Partial dep.: :math:`A \to B` -- **violates 2NF**.

   **Fix**: :math:`R_1(A,B)` (key: :math:`A`), :math:`R_2(A,C,D,E)` (key: :math:`\{A,C\}`).


.. dropdown:: Box 10 -- Third Normal Form (3NF)
   :class-container: sd-border-secondary

   **Definition**: 2NF + for every non-trivial FD :math:`X \to Y`: :math:`X` is a superkey
   **OR** every attribute in :math:`Y` is prime (the "escape clause").

   .. rubric:: Steps to Test and Fix

   1. Decompose all FDs to single-attribute RHS.
   2. For each FD :math:`X \to A`: compute :math:`X^+`. If :math:`X^+ = R` -- superkey -- passes. Else: is :math:`A` prime? If yes -- passes (escape clause). Neither -- **violates 3NF**.
   3. **Fix**: create new relation :math:`X \cup \{A\}`; drop :math:`A` from original.

   .. rubric:: Worked Example: :math:`R(G,H,I,J)`, :math:`F = \{G \to HI,\; I \to J\}`

   CK = :math:`\{G\}`. Prime: :math:`G`. Non-prime: :math:`H, I, J`.

   - :math:`G \to H`, :math:`G \to I`: :math:`\{G\}^+ = R` -- superkey -- **pass**.
   - :math:`I \to J`: :math:`\{I\}^+ = \{I,J\} \neq R`, and :math:`J` is non-prime -- **violates 3NF** (transitive: :math:`G \to I \to J`).

   **Fix**: :math:`R_1(I,J)` (key: :math:`I`), :math:`R_2(G,H,I)` (key: :math:`G`). Lossless join: :math:`R_1 \cap R_2 = \{I\}` is a superkey of :math:`R_1`.


.. dropdown:: Box 11 -- Boyce-Codd Normal Form (BCNF)
   :class-container: sd-border-secondary

   **Definition**: For every non-trivial FD :math:`X \to Y`, :math:`X` must be a
   superkey. **No exceptions** -- unlike 3NF there is no prime-attribute escape clause.

   .. list-table::
      :widths: 50 25 25
      :header-rows: 1
      :class: compact-table

      * - For every non-trivial FD :math:`X \to Y`
        - 3NF
        - BCNF
      * - :math:`X` is a superkey
        - Pass
        - Pass
      * - :math:`X` not SK, :math:`Y` all prime
        - Pass
        - **Fail**
      * - :math:`X` not SK, :math:`Y` has non-prime attrs
        - Fail
        - Fail

   .. rubric:: Worked Example: :math:`R(A,B,C)`, :math:`F = \{AB \to C,\; C \to B\}`

   CKs: :math:`\{A,B\}` and :math:`\{A,C\}`. All attributes are prime.

   - :math:`AB \to C`: :math:`\{A,B\}^+ = R` -- superkey -- **pass**.
   - :math:`C \to B`: :math:`\{C\}^+ = \{C,B\} \neq R` -- 3NF: :math:`B` is prime, passes via escape clause. BCNF: no escape clause -- **fails**.

   **Fix** on :math:`C \to B`: :math:`R_1(C,B)` (key: :math:`C`), :math:`R_2(A,C)` (key: :math:`\{A,C\}`).


.. dropdown:: Box 12 -- 3NF Synthesis (Bottom-Up)
   :class-container: sd-border-secondary

   **Input**: Relation :math:`R` with FD set :math:`F`. **Output**: Relations in 3NF.

   **Guarantees**: Lossless join and dependency preservation.

   .. rubric:: Algorithm

   1. Compute the canonical cover :math:`F_c`.
   2. For each FD :math:`X \to A` in :math:`F_c`: create relation :math:`R_i = X \cup \{A\}`. Combine FDs with the same LHS into one relation.
   3. If no :math:`R_i` contains a candidate key of :math:`R`, add a relation consisting of a candidate key.
   4. Remove any :math:`R_i` that is a subset of another :math:`R_j`.

   .. rubric:: Worked Example: :math:`R(A,B,C,D,E)`, :math:`F = \{AB \to C,\; C \to B,\; C \to D,\; D \to E\}`

   CKs: :math:`\{A,B\}` and :math:`\{A,C\}`. :math:`F_c = \{AB \to C,\; C \to B,\; C \to D,\; D \to E\}` (unchanged after all checks).

   **Step 2 -- Create relations**:

   .. list-table::
      :widths: 40 35 25
      :header-rows: 1
      :class: compact-table

      * - FD(s) in :math:`F_c`
        - Relation
        - Key
      * - :math:`AB \to C`
        - :math:`R_1(A, B, C)`
        - :math:`\{A, B\}`
      * - :math:`C \to B` and :math:`C \to D` (same LHS -- combine)
        - :math:`R_2(C, B, D)`
        - :math:`\{C\}`
      * - :math:`D \to E`
        - :math:`R_3(D, E)`
        - :math:`\{D\}`

   **Step 3** -- CK :math:`\{A,B\}` is already in :math:`R_1`. No extra relation needed.

   **Step 4** -- No :math:`R_i \subseteq R_j`. Keep all three.

   .. card::
      :class-card: sd-border-success

      **Result**: :math:`R_1(A,B,C)`, :math:`R_2(C,B,D)`, :math:`R_3(D,E)`. All in 3NF. Lossless join and dependency preservation guaranteed.


.. dropdown:: Box 13 -- BCNF Decomposition (Top-Down)
   :class-container: sd-border-secondary

   **Input**: Relation :math:`R` with FD set :math:`F`. **Output**: Relations in BCNF.

   **Guarantees**: Lossless join only. Dependency preservation **not** guaranteed.

   .. rubric:: Algorithm

   1. If :math:`R` is already in BCNF, stop.
   2. Find a violating FD :math:`X \to Y` (where :math:`X` is not a superkey).
   3. Decompose: :math:`R_1 = X \cup Y`, :math:`R_2 = R - (Y - X)`.
   4. Recursively apply to :math:`R_1` and :math:`R_2`.

   .. rubric:: Worked Example: :math:`R(A,B,C,D,E)`, :math:`F_c = \{A \to B,\; A \to C,\; C \to D,\; D \to E\}`

   CK = :math:`\{A\}`. Violating FD: :math:`C \to D` (:math:`\{C\}^+ = \{C,D,E\} \neq R`).

   **Decompose on** :math:`C \to D` (:math:`X = \{C\}`, :math:`Y = \{D\}`):

   - :math:`R_1 = \{C,D\}` -- key: :math:`C`. In BCNF.
   - :math:`R_2 = \{A,B,C,E\}` -- FDs on :math:`R_2`: :math:`\{A \to B,\; A \to C,\; A \to E\}`. :math:`\{A\}^+ = R_2`. In BCNF.

   .. card::
      :class-card: sd-border-success

      **Result**: :math:`R_1(C,D)`, :math:`R_2(A,B,C,E)`. Lossless join confirmed. However, :math:`D \to E` is lost: :math:`D` is in :math:`R_1` and :math:`E` is in :math:`R_2` -- no single relation contains both.


.. dropdown:: Box 14 -- Lossless Join & Dependency Preservation
   :class-container: sd-border-secondary

   .. rubric:: Lossless Join Test (non-negotiable)

   A decomposition of :math:`R` into :math:`R_1` and :math:`R_2` is lossless iff:

   .. math::

      R_1 \cap R_2 \to R_1 \quad \text{or} \quad R_1 \cap R_2 \to R_2

   The common attributes must be a superkey of at least one side. Failure produces **spurious tuples** (phantom rows that did not exist in the original data).

   .. note::

      Always decompose on a violating FD. The LHS becomes the common attribute and is automatically a superkey of :math:`R_1 = X \cup Y`.

   .. rubric:: Dependency Preservation Test

   For each FD :math:`X \to Y` in :math:`F`: does some :math:`R_i` contain all attributes of both :math:`X` and :math:`Y`? If yes for every FD, dependencies are preserved.

   .. list-table::
      :widths: 35 32 33
      :header-rows: 1
      :class: compact-table

      * - Property
        - 3NF Synthesis
        - BCNF Decomp.
      * - Lossless join
        - Always
        - Always
      * - Dep. preservation
        - Always
        - Not always
      * - All FD anomalies gone
        - Not always
        - Always

   .. rubric:: Verification: 3NF Synthesis Result (:math:`R_1(A,B,C)`, :math:`R_2(C,D)`, :math:`R_3(D,E)`)

   .. card::
      :class-card: sd-border-success

      **Lossless join**: :math:`R_1 \cap R_2 = \{C\}` is a superkey of :math:`R_2` (via :math:`C \to D`). :math:`R_2 \cap R_3 = \{D\}` is a superkey of :math:`R_3` (via :math:`D \to E`). No spurious tuples.

      **Dep. preservation**: :math:`A \to B` in :math:`R_1`; :math:`A \to C` in :math:`R_1`; :math:`C \to D` in :math:`R_2`; :math:`D \to E` in :math:`R_3`. Every FD checkable within a single relation.

   .. rubric:: Verification: BCNF Decomposition Result (:math:`R_1(C,D)`, :math:`R_2(A,B,C,E)`)

   .. card::
      :class-card: sd-border-warning

      **Lossless join**: :math:`R_1 \cap R_2 = \{C\}` is a superkey of :math:`R_1` (via :math:`C \to D`). Lossless.

      **Dep. preservation**: :math:`A \to B`, :math:`A \to C` preserved in :math:`R_2`. :math:`C \to D` preserved in :math:`R_1`. But :math:`D \to E`: :math:`D` is in :math:`R_1`, :math:`E` is in :math:`R_2` -- **not preserved**. To enforce :math:`D \to E`, the application needs a cross-table check or trigger.


.. dropdown:: Box 15 -- 3NF Synthesis: Steps 3 & 4 in Action
   :class-container: sd-border-secondary

   This example is specifically designed so that both Step 3 (add missing CK relation)
   and Step 4 (remove subset relation) are exercised -- unlike the Box 12 example where
   neither fired.

   .. rubric:: Worked Example: :math:`R(P, Q, S, T)`, :math:`F = \{P \to Q,\; Q \to S,\; S \to Q\}`

   **Find CKs**: :math:`\{P\}^+ = \{P,Q,S\} \neq R` (cannot reach :math:`T`). :math:`T` never appears on any RHS, so :math:`T` must be in every CK. :math:`\{P,T\}^+ = R`. CK = :math:`\{P,T\}`.

   **Step 1 -- Compute** :math:`F_c`:

   Redundancy checks: :math:`P \to Q` under :math:`\{Q \to S, S \to Q\}`: :math:`\{P\}^+ = \{P\}`. :math:`Q \notin \{P\}` -- keep. :math:`Q \to S` under :math:`\{P \to Q, S \to Q\}`: :math:`\{Q\}^+ = \{Q\}`. :math:`S \notin \{Q\}` -- keep. :math:`S \to Q` under :math:`\{P \to Q, Q \to S\}`: :math:`\{S\}^+ = \{S\}`. :math:`Q \notin \{S\}` -- keep.

   :math:`F_c = \{P \to Q,\; Q \to S,\; S \to Q\}`

   **Step 2 -- Create relations**:

   .. list-table::
      :widths: 40 35 25
      :header-rows: 1
      :class: compact-table

      * - FD
        - Relation
        - Key
      * - :math:`P \to Q`
        - :math:`R_1(P, Q)`
        - :math:`P`
      * - :math:`Q \to S`
        - :math:`R_2(Q, S)`
        - :math:`Q`
      * - :math:`S \to Q`
        - :math:`R_3(S, Q)`
        - :math:`S`

   **Step 3 -- CK check (fires)**: CK = :math:`\{P,T\}`. None of :math:`R_1`, :math:`R_2`, :math:`R_3` contain :math:`T`. Add :math:`R_4(P, T)`. Without this, :math:`T` would be disconnected from the schema.

   **Step 4 -- Subset check (fires)**: :math:`R_3 = \{S,Q\}` and :math:`R_2 = \{Q,S\}` -- same attributes. :math:`R_3 \subseteq R_2`. Remove :math:`R_3`. (:math:`S \to Q` can still be enforced within :math:`R_2`.)

   .. card::
      :class-card: sd-border-success

      **Result**: :math:`R_1(P,Q)`, :math:`R_2(Q,S)`, :math:`R_4(P,T)`. All in 3NF. Lossless join and dependency preservation guaranteed.

      Step 3 added :math:`R_4` to anchor the candidate key :math:`\{P,T\}`. Step 4 removed :math:`R_3` as a duplicate of :math:`R_2`.