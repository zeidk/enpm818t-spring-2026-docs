====================================================
Quiz
====================================================

This quiz covers the key concepts from Lectures 4 and 5: Normalization and
Denormalization, including functional dependencies, Armstrong's axioms,
attribute closures, canonical covers, normal forms (1NF through BCNF),
decomposition algorithms (3NF synthesis and BCNF decomposition), lossless
join, dependency preservation, and denormalization trade-offs.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2-4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice (Questions 1-17)
================================

.. admonition:: Question 1
   :class: hint

   What is the primary goal of normalization?

   A. To maximize query performance by reducing the number of tables.

   B. To reduce redundancy and eliminate anomalies by decomposing relations based on functional dependencies.

   C. To combine multiple tables into a single denormalized table.

   D. To convert conceptual ER diagrams into SQL code.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To reduce redundancy and eliminate anomalies by decomposing relations based on functional dependencies.

   Normalization decomposes poorly structured relations into smaller, well-structured ones guided by FDs. This eliminates insertion, deletion, and update anomalies.


.. admonition:: Question 2
   :class: hint

   Which of the following correctly defines a functional dependency :math:`X \to Y`?

   A. Every value of :math:`Y` determines a unique value of :math:`X`.

   B. :math:`X` and :math:`Y` always have the same values.

   C. For every pair of tuples, if they agree on :math:`X`, they must agree on :math:`Y`.

   D. :math:`Y` is a subset of :math:`X`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- For every pair of tuples, if they agree on :math:`X`, they must agree on :math:`Y`.

   This is the formal definition: :math:`\forall\, t_1, t_2: t_1[X] = t_2[X] \implies t_1[Y] = t_2[Y]`.


.. admonition:: Question 3
   :class: hint

   Which anomaly occurs when deleting the last enrollment for a course also removes all course information?

   A. Insertion anomaly.

   B. Update anomaly.

   C. Deletion anomaly.

   D. Redundancy anomaly.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Deletion anomaly.

   A deletion anomaly occurs when removing a row causes the unintended loss of other information. Here, course data is lost because it was mixed with enrollment data.


.. admonition:: Question 4
   :class: hint

   Which of the following is Armstrong's **transitivity** axiom?

   A. If :math:`Y \subseteq X`, then :math:`X \to Y`.

   B. If :math:`X \to Y`, then :math:`XZ \to YZ`.

   C. If :math:`X \to Y` and :math:`Y \to Z`, then :math:`X \to Z`.

   D. If :math:`X \to Y` and :math:`X \to Z`, then :math:`X \to YZ`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- If :math:`X \to Y` and :math:`Y \to Z`, then :math:`X \to Z`.

   Transitivity chains two FDs together. Option A is reflexivity, B is augmentation, and D is the union shortcut.


.. admonition:: Question 5
   :class: hint

   What does the attribute closure :math:`X^{+}` represent?

   A. The set of all FDs in the canonical cover.

   B. The set of all attributes that :math:`X` functionally determines under :math:`F`.

   C. The set of all superkeys of the relation.

   D. The minimal set of attributes needed to form a candidate key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The set of all attributes that :math:`X` functionally determines under :math:`F`.

   The closure algorithm iteratively adds attributes reachable through the given FDs until no more can be added.


.. admonition:: Question 6
   :class: hint

   How do you test whether a set of attributes :math:`X` is a superkey of relation :math:`R`?

   A. Check if :math:`X` contains the primary key.

   B. Compute :math:`X^{+}` and check if :math:`X^{+} = R`.

   C. Check if :math:`X` appears on the left side of every FD.

   D. Verify that :math:`X` has no extraneous attributes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Compute :math:`X^{+}` and check if :math:`X^{+} = R`.

   If the closure of :math:`X` includes every attribute in :math:`R`, then knowing :math:`X` determines everything, making :math:`X` a superkey.


.. admonition:: Question 7
   :class: hint

   A relation is in **2NF** if it is in 1NF and:

   A. Every determinant is a superkey.

   B. No non-prime attribute is transitively dependent on any candidate key.

   C. No non-prime attribute is partially dependent on any candidate key.

   D. All attribute values are atomic.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- No non-prime attribute is partially dependent on any candidate key.

   2NF eliminates partial dependencies, where a non-prime attribute depends on only part of a composite candidate key.


.. admonition:: Question 8
   :class: hint

   What distinguishes BCNF from 3NF?

   A. BCNF requires atomic values; 3NF does not.

   B. BCNF does not allow the prime-attribute exception that 3NF permits.

   C. BCNF guarantees dependency preservation; 3NF does not.

   D. BCNF applies only to composite keys.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- BCNF does not allow the prime-attribute exception that 3NF permits.

   In 3NF, an FD :math:`X \to Y` is allowed if :math:`Y` consists entirely of prime attributes, even when :math:`X` is not a superkey. BCNF removes this exception: every determinant must be a superkey.


.. admonition:: Question 9
   :class: hint

   Which decomposition property guarantees that joining the decomposed relations exactly reconstructs the original data?

   A. Dependency preservation.

   B. Canonical cover.

   C. Lossless join.

   D. Attribute closure.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Lossless join.

   A lossless (non-additive) join decomposition ensures no spurious tuples are introduced when the decomposed relations are rejoined.


.. admonition:: Question 10
   :class: hint

   Which of the following is a valid reason to denormalize a schema?

   A. To eliminate all redundancy in the database.

   B. To optimize read performance for known, repetitive query patterns.

   C. To reduce the number of foreign keys.

   D. To ensure all FDs are preserved.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To optimize read performance for known, repetitive query patterns.

   Denormalization intentionally reintroduces redundancy to reduce join counts and improve query speed for read-heavy workloads. It trades write consistency for read performance.


.. admonition:: Question 11
   :class: hint

   A relation is in **First Normal Form (1NF)** if:

   A. Every non-prime attribute depends on the full candidate key.

   B. Every determinant is a superkey.

   C. Every attribute contains only atomic (indivisible) values.

   D. No non-prime attribute is transitively dependent on any candidate key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Every attribute contains only atomic (indivisible) values.

   1NF is the baseline requirement: no repeating groups, no nested relations, and no multi-valued attributes. Options A, B, and D describe 2NF, BCNF, and 3NF respectively.


.. admonition:: Question 12
   :class: hint

   Which step is performed **first** in the canonical cover algorithm?

   A. Remove redundant FDs.

   B. Test for extraneous left-side attributes.

   C. Split all FDs so each right-hand side is a single attribute.

   D. Compute the attribute closure of each left-hand side.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Split all FDs so each right-hand side is a single attribute.

   The three steps in order are: (1) decompose compound right sides, (2) reduce left sides by removing extraneous attributes, (3) remove redundant FDs. Steps 2 and 3 both rely on closure computations, but step 1 must come first so that the closure tests operate on single-attribute right sides.


.. admonition:: Question 13
   :class: hint

   In the relation ``Course``\(**course_id**, title, dept_id, dept_name), which FD creates a **3NF violation**?

   A. ``course_id`` :math:`\to` ``title``

   B. ``course_id`` :math:`\to` ``dept_id``

   C. ``dept_id`` :math:`\to` ``dept_name``

   D. {``course_id``, ``dept_id``} :math:`\to` ``title``

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- ``dept_id`` :math:`\to` ``dept_name``.

   ``dept_id`` is not a superkey: its closure is only {``dept_id``, ``dept_name``}, not all of :math:`R`. ``dept_name`` is non-prime. This is a transitive dependency -- the key ``course_id`` determines ``dept_id``, which in turn determines ``dept_name``. Options A and B both have the superkey ``course_id`` as determinant and therefore pass 3NF.


.. admonition:: Question 14
   :class: hint

   What is an **extraneous attribute** in the context of the canonical cover algorithm?

   A. An attribute on the right-hand side of an FD that can be removed without changing the implied FDs.

   B. An attribute on the left-hand side of an FD that can be removed without changing what the FD determines.

   C. An FD that can be derived entirely from other FDs in the set.

   D. An attribute that does not belong to any candidate key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- An attribute on the left-hand side of an FD that can be removed without changing what the FD determines.

   Formally, :math:`B` is extraneous in :math:`X \to A` if :math:`A \in (X - \{B\})^{+}` under :math:`F`. Option C describes a redundant FD (a distinct concept), and option D describes a non-prime attribute.


.. admonition:: Question 15
   :class: hint

   The **3NF escape clause** permits an FD :math:`X \to Y` even when :math:`X` is not a superkey, provided that:

   A. :math:`X` contains at least one prime attribute.

   B. Every attribute in :math:`Y` is prime.

   C. :math:`Y` is a single attribute.

   D. :math:`X` and :math:`Y` share no attributes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Every attribute in :math:`Y` is prime.

   An FD :math:`X \to Y` passes the 3NF test if either :math:`X` is a superkey **or** every attribute in :math:`Y` belongs to at least one candidate key. BCNF eliminates this escape clause: it requires every determinant to be a superkey with no exceptions.


.. admonition:: Question 16
   :class: hint

   The lossless join condition for decomposing :math:`R` into :math:`R_1` and :math:`R_2` requires that:

   A. Every FD in :math:`F` is entirely contained within :math:`R_1` or :math:`R_2`.

   B. :math:`R_1 \cap R_2 \to R_1` or :math:`R_1 \cap R_2 \to R_2` holds under :math:`F`.

   C. :math:`R_1` and :math:`R_2` share no attributes.

   D. The canonical cover of :math:`F` restricted to :math:`R_1` equals that restricted to :math:`R_2`.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- :math:`R_1 \cap R_2 \to R_1` or :math:`R_1 \cap R_2 \to R_2` holds under :math:`F`.

   The shared attributes must be a superkey of at least one side. This ensures the join is unambiguous and introduces no spurious tuples. Option A describes dependency preservation, not lossless join.


.. admonition:: Question 17
   :class: hint

   Which statement best describes the difference between **OLTP** and **OLAP** schema design?

   A. OLTP uses star schemas; OLAP uses BCNF schemas.

   B. OLTP favors high normalization for write integrity; OLAP favors low normalization for read performance.

   C. OLTP is read-heavy; OLAP is write-heavy.

   D. OLTP and OLAP schemas must use the same normalization level.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- OLTP favors high normalization for write integrity; OLAP favors low normalization for read performance.

   OLTP systems process frequent, simple reads and writes where data integrity is paramount, making 3NF/BCNF the right choice. OLAP systems run complex analytical queries and favor denormalized star or snowflake schemas that minimize joins. Option C has the workloads reversed.


----


True/False (Questions 18-27)
============================

.. admonition:: Question 18
   :class: hint

   **True or False:** Functional dependencies are derived from inspecting the current data in a table.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   FDs come from **business rules**, not from data inspection. Even if all current rows are consistent with an FD, that does not prove the FD holds. Only the business rule can establish an FD.


.. admonition:: Question 19
   :class: hint

   **True or False:** A trivial FD :math:`X \to Y` (where :math:`Y \subseteq X`) is always true regardless of the data.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   By Armstrong's reflexivity axiom, any set of attributes always determines any of its subsets. Trivial FDs are tautologies.


.. admonition:: Question 20
   :class: hint

   **True or False:** Armstrong's axioms are sound but not complete.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   Armstrong's axioms are both **sound** (every derived FD is true) and **complete** (every true FD can be derived). Together, they form a complete inference system for FDs.


.. admonition:: Question 21
   :class: hint

   **True or False:** If :math:`X^{+} = R` (all attributes), then :math:`X` is necessarily a candidate key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   :math:`X^{+} = R` makes :math:`X` a **superkey**, but not necessarily a candidate key. A candidate key must also be **minimal**: no proper subset of :math:`X` is also a superkey.


.. admonition:: Question 22
   :class: hint

   **True or False:** 2NF violations can only occur when the candidate key is composite.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   A partial dependency requires a non-prime attribute to depend on only *part* of a candidate key. If the candidate key is a single attribute, there is no "part" to depend on, so partial dependencies are impossible.


.. admonition:: Question 23
   :class: hint

   **True or False:** Every relation in BCNF is also in 3NF.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   BCNF is strictly stronger than 3NF. If every determinant is a superkey (BCNF), then the 3NF conditions are automatically satisfied.


.. admonition:: Question 24
   :class: hint

   **True or False:** The 3NF synthesis algorithm guarantees both lossless join and dependency preservation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The 3NF synthesis algorithm is specifically designed to achieve both properties. Step 3 (adding a candidate key relation) ensures lossless join, and creating a relation for each FD ensures dependency preservation.


.. admonition:: Question 25
   :class: hint

   **True or False:** BCNF decomposition always preserves all functional dependencies.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   BCNF decomposition guarantees lossless join but may sacrifice dependency preservation. Some FDs may only be enforceable by joining multiple decomposed relations.


.. admonition:: Question 26
   :class: hint

   **True or False:** A canonical cover :math:`F_c` may contain fewer FDs than the original set :math:`F`, but both sets imply exactly the same FDs.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   The canonical cover removes redundant FDs, extraneous left-side attributes, and compound right sides. The result is a simplified but equivalent set of FDs.


.. admonition:: Question 27
   :class: hint

   **True or False:** Denormalization should be applied proactively during initial schema design to avoid performance issues later.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   The golden rule is: **normalize first, denormalize later**. Always start with a normalized schema. Add denormalization only when performance testing identifies proven bottlenecks.


----


Essay Questions (Questions 28-31)
==================================

.. admonition:: Question 28
   :class: hint

   Explain the difference between a **superkey** and a **candidate key**. Describe how attribute closure is used to test each. Use the ``Course_Section`` relation as an example.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - A **superkey** is any set of attributes whose closure reaches all attributes in the relation (:math:`X^{+} = R`). It uniquely identifies rows but may contain unnecessary attributes.
   - A **candidate key** is a **minimal** superkey: removing any single attribute causes it to no longer be a superkey.
   - To test: compute :math:`X^{+}`. If it equals :math:`R`, :math:`X` is a superkey. Then test each proper subset; if no subset is also a superkey, :math:`X` is a candidate key.
   - Example: {``course_id``, ``section_no``}\ :sup:`+` = all attributes, so it is a superkey. {``course_id``} alone misses ``section_no`` and ``professor_person_id``; {``section_no``} alone reaches only itself. Neither proper subset is a superkey, so {``course_id``, ``section_no``} is a candidate key.


.. admonition:: Question 29
   :class: hint

   Describe the three types of anomalies (insertion, deletion, update) using the ``Course_Enrollment`` table from the lecture. For each, explain why decomposition solves the problem.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **Insertion anomaly**: Cannot add a new course without a student. After decomposition, courses exist independently in the ``Course`` table.
   - **Deletion anomaly**: Removing the last enrollment for a course loses all course data. After decomposition, course data lives in ``Course`` and is unaffected by enrollment changes.
   - **Update anomaly**: Changing a professor's name requires updating multiple rows. After decomposition, the professor's name is stored once in the ``Professor`` table.
   - The root cause in all three cases is that the original table mixed facts about multiple entities. Decomposition isolates each entity into its own relation.


.. admonition:: Question 30
   :class: hint

   Compare the 3NF synthesis algorithm with the BCNF decomposition algorithm. When would you choose one over the other? Give a concrete scenario for each.

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - **3NF synthesis** guarantees both lossless join and dependency preservation. Choose it when every FD must be enforceable within a single table (e.g., a constraint that must be checked on every INSERT without joining).
   - **BCNF decomposition** eliminates all FD-based anomalies but may lose dependency preservation. Choose it when maximum data integrity is required and cross-table constraint checks (via joins or triggers) are acceptable.
   - **Practical guideline**: Start with BCNF. If a critical dependency is lost (e.g., an FD that must be checked on every insert for real-time validation), fall back to 3NF for those specific relations.
   - **Scenario for 3NF**: A scheduling system where {``room_id``, ``time_slot``} :math:`\to` ``course_id`` must be enforced on every insert to prevent double-booking.
   - **Scenario for BCNF**: A data warehouse where anomaly-free data is paramount and constraints are enforced during batch ETL, not real-time inserts.


.. admonition:: Question 31
   :class: hint

   Explain the purpose of the **canonical cover** and describe each of its three properties. Why must the canonical cover be computed before running either the 3NF synthesis or BCNF decomposition algorithm?

   *(2-4 sentences)*

.. dropdown:: Answer Guidelines
   :class-container: sd-border-success

   *Key points to include:*

   - The canonical cover :math:`F_c` is an equivalent, simplified version of the FD set :math:`F` with all redundancy removed. It has three properties: (1) every right-hand side is a single attribute, (2) no left-hand side contains extraneous attributes, and (3) no FD is redundant (derivable from the others).
   - It is computed in three steps: decompose compound right sides, test and remove extraneous left-side attributes (using closure), and remove redundant FDs (using closure).
   - Computing it first ensures that decomposition algorithms operate on the minimal, non-redundant set of FDs. Redundant or bloated FDs would produce unnecessary or oversized relations in 3NF synthesis, and would complicate the BCNF violation check.
   - Both algorithms rely on attribute closure internally, so having a clean, single-attribute-RHS FD set is a prerequisite for correct execution.