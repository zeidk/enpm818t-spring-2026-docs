====================================================
Lecture
====================================================



Why Normalization Matters
====================================================


.. dropdown:: What Is Normalization?
   :class-container: sd-border-secondary
   :open:

   Definition
   ~~~~~~~~~~

   **Normalization** is the process of organizing a relational database schema to reduce redundancy and improve data integrity by decomposing relations into smaller, well-structured relations based on their functional dependencies.

   Key Ideas
   ^^^^^^^^^

   1. Each relation should represent **one fact about one entity**. A student table stores student data, not course data.

   2. Decomposition is guided by **functional dependencies** (formal rules about which attributes determine others).

   3. Normal forms (1NF, 2NF, 3NF, BCNF) provide **progressively stricter** criteria for a well-designed schema.

   .. card::
       :class-card: sd-border-info

       **Analogy**: Think of normalization as decluttering a filing cabinet. Instead of one overstuffed folder with duplicated papers, you create clearly labeled folders where each piece of information lives in exactly one place.


.. dropdown:: Where Normalization Fits
   :class-container: sd-border-secondary

   The Database Design Pipeline
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A careful ER design often produces schemas that are already close to normalized. However, mapping to relations can introduce redundancy, especially with composite keys, multi-valued attributes, and complex relationships. Normalization is a formal verification and repair step that catches what intuition may miss.

   The pipeline is: **Conceptual Model (ERD)** :math:`\to` **Logical Model (tables)** :math:`\to` **Normalization (verify and repair)** :math:`\to` **Physical Model (SQL)**.


.. dropdown:: The Problem: Data Redundancy
   :class-container: sd-border-secondary
   :open:

   A Poorly Designed Table
   ~~~~~~~~~~~~~~~~~~~~~~~~

   This ``Course_Enrollment`` table mixes facts about three entities (students, courses, and enrollments) into a single relation:

   .. list-table::
      :widths: 12 15 14 14 14 18
      :header-rows: 1
      :class: compact-table

      * - **student_id** (PK)
        - student_name
        - **course_id** (PK)
        - title
        - dept_name
        - professor_name
      * - S001
        - Alice
        - ENPM818T
        - Databases
        - CS
        - Dr. Smith
      * - S001
        - Alice
        - ENPM702
        - Robotics
        - ME
        - Dr. Lee
      * - S002
        - Bob
        - ENPM818T
        - Databases
        - CS
        - Dr. Smith
      * - S003
        - Carlos
        - ENPM818T
        - Databases
        - CS
        - Dr. Smith

   .. warning::

      **Redundancy**: Because course data is stored alongside every enrollment row, the title "Databases", department "CS", and professor "Dr. Smith" appear three times. If Dr. Smith's name changes, we must update *every* row where ENPM818T appears. Miss one, and you have **inconsistent data**.


.. dropdown:: The Three Anomalies
   :class-container: sd-border-secondary
   :open:

   What Goes Wrong?
   ~~~~~~~~~~~~~~~~

   Because the ``Course_Enrollment`` table stores facts about multiple entities in one relation, three types of anomalies arise:

   1. **Insertion Anomaly**: Can't add a new course unless at least one student enrolls in it. We want to add ENPM808X (Advanced Python) to the catalog, but the table requires a ``student_id``. Without a student, we cannot insert the course.

   2. **Deletion Anomaly**: Deleting the last enrollment for a course deletes course information. If Alice drops ENPM702 and she is the only student, we lose all information about that course (title, department, professor).

   3. **Update Anomaly**: Changing course information requires updating multiple rows. If Dr. Smith changes name to Dr. Smith-Jones, we must find and update *all* rows with ENPM818T. Partial updates create inconsistency: some rows say "Dr. Smith", others say "Dr. Smith-Jones".


.. dropdown:: The Solution: Normalization
   :class-container: sd-border-secondary

   After Normalization
   ~~~~~~~~~~~~~~~~~~~

   Decompose so each relation captures one entity:

   **Student**

   .. list-table::
      :widths: 30 30
      :header-rows: 1
      :class: compact-table

      * - **person_id** (PK)
        - first_name
      * - 201
        - Alice
      * - 202
        - Bob
      * - 203
        - Carlos

   **Course**

   .. list-table::
      :widths: 30 30
      :header-rows: 1
      :class: compact-table

      * - **course_id** (PK)
        - title
      * - ENPM818T
        - Databases
      * - ENPM702
        - Robotics
      * - ENPM808X
        - Python

   **Enrollment**

   .. list-table::
      :widths: 50 50
      :header-rows: 1
      :class: compact-table

      * - **student_person_id** (PK)
        - **course_id** (PK)
      * - 201
        - ENPM818T
      * - 201
        - ENPM702
      * - 202
        - ENPM818T
      * - 203
        - ENPM818T

   .. card::
       :class-card: sd-border-success

       **All three anomalies resolved**: **Insertion** -- ENPM808X exists in ``Course`` with no enrollments. **Deletion** -- Dropping an enrollment leaves ``Course`` and ``Professor`` intact. **Update** -- Changing a professor's name requires editing one row in ``Professor``.


.. dropdown:: Goals of Normalization
   :class-container: sd-border-secondary

   Four Primary Goals
   ~~~~~~~~~~~~~~~~~~

   1. **Minimize redundancy**: Store each fact exactly once. Reduces storage and prevents inconsistency from partial updates.

   2. **Eliminate anomalies**: Prevent the insertion, deletion, and update problems we just saw. Data integrity is enforced by schema structure, not application logic.

   3. **Isolate entities**: Each relation represents one concept. Updating a department name in ``Department`` requires changing one row, not every course that references it.

   4. **Support schema evolution**: Well-normalized schemas adapt to new requirements. Adding an attribute to ``Course`` does not require restructuring ``Enrollment`` or ``Student``.

   .. card::
       :class-card: sd-border-info

       **Trade-off**: More tables means more joins. For read-heavy workloads with predictable queries, strategic denormalization may improve performance (covered later in this lecture).



Functional Dependencies
====================================================


.. dropdown:: Why We Need Them
   :class-container: sd-border-secondary
   :open:

   From Intuition to Formalism
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~

   In the previous section, we relied on intuition to identify problems and decompose the ``Course_Enrollment`` table. But consider these questions: How do we **know** which columns cause redundancy? How do we decide **where to split** a table? How do we **prove** the result is correct?

   The Role of Functional Dependencies
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   A **functional dependency** (FD) captures the rule that one set of attributes uniquely determines another. In the enrollment example, we implicitly used these FDs:

   - ``student_id`` :math:`\to` ``student_name`` (knowing the student ID is enough to identify the name)
   - ``course_id`` :math:`\to` {``title``, ``dept_name``, ``professor_name``} (knowing the course ID is enough to identify the title, department, and professor)

   FDs give us a **formal language** to describe why redundancy exists and **algorithms** to eliminate it systematically.

   .. card::
       :class-card: sd-border-info

       **Bottom line**: Normalization without FDs is guesswork. FDs turn database design into an engineering discipline with provably correct decompositions.


.. dropdown:: Formal Definition
   :class-container: sd-border-secondary
   :open:

   Definition
   ~~~~~~~~~~

   A **functional dependency** (FD), written :math:`X \to Y`, states that for each value of :math:`X`, there is exactly one corresponding value of :math:`Y`. The name comes from mathematics: :math:`Y` is a *function* of :math:`X`. Both :math:`X` and :math:`Y` can be single attributes or sets of multiple attributes. Formally, given a relation schema :math:`R` with :math:`X, Y \subseteq R`:

   .. math::

      \forall\, t_{1}, t_{2}\in r(R): \; t_{1}[X] = t_{2}[X] \implies t_{1}[Y] = t_{2}[Y]

   For every pair of tuples :math:`t_1` and :math:`t_2` in the relation: if they have the same values on **all** attributes in :math:`X`, then they must also have the same values on **all** attributes in :math:`Y`.

   Terminology
   ^^^^^^^^^^^

   - :math:`X` is the **determinant** (left-hand side), one or more attributes
   - :math:`Y` is the **dependent** (right-hand side), one or more attributes
   - Read :math:`X \to Y` as ":math:`X` determines :math:`Y`"
   - Example: {``student_person_id``, ``course_id``, ``section_no``} :math:`\to` {``grade``} is an FD where :math:`X` has three attributes


.. dropdown:: FDs from University Business Rules
   :class-container: sd-border-secondary

   Intuition with Examples
   ~~~~~~~~~~~~~~~~~~~~~~~

   Here are some FDs from the university domain. Each is derived from a specific business rule, not from inspecting rows:

   .. list-table::
      :widths: 30 35 35
      :header-rows: 1
      :class: compact-table

      * - Business Rule
        - FD
        - Meaning
      * - Every person has a unique ID
        - ``person_id`` :math:`\to` {``first_name``, ``last_name``, ``date_of_birth``}
        - Person ID determines personal attributes
      * - Each course has one title, credit count, and department
        - ``course_id`` :math:`\to` {``title``, ``credits``, ``dept_id``}
        - Course ID determines all three
      * - Each section is taught by one professor
        - {``course_id``, ``section_no``} :math:`\to` ``professor_person_id``
        - Section determines professor
      * - Each department has a unique name
        - ``dept_id`` :math:`\to` ``dept_name``
        - Dept ID determines name

   .. card::
       :class-card: sd-border-info

       **Process**: When designing a schema, start by collecting business rules from stakeholders. Translate each rule into one or more FDs. These FDs then drive the normalization algorithms covered later in this lecture.

   .. warning::

      **Caution**: FDs come from **business rules**, not from inspecting data. Even if 99% of pairs agree, a single violation means the FD does not hold. Conversely, even if all current rows agree, that does not prove the FD. Only the business rule can do that.


.. dropdown:: Trivial and Non-Trivial FDs
   :class-container: sd-border-secondary

   Trivial FD: :math:`X \to Y` where :math:`Y \subseteq X`
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A trivial FD is one where the dependent is already part of the determinant. It is always true regardless of the data or business rules.

   Examples: {``student_person_id``, ``course_id``} :math:`\to` ``student_person_id``; {``course_id``, ``section_no``} :math:`\to` ``course_id``; ``person_id`` :math:`\to` ``person_id``.

   Normalization cares about FDs that reveal **hidden structure**: which attributes determine other, *different* attributes. Trivial FDs reveal nothing because the answer is already contained in the question.

   Non-Trivial FD: :math:`X \to Y` where :math:`Y \not\subseteq X`
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   A non-trivial FD is one where the dependent contains at least one attribute **not already in** the determinant. These encode real business constraints.

   **Example (no overlap)**: ``person_id`` :math:`\to` ``first_name``. The right side is entirely new information, requiring a business rule: each person has exactly one first name.

   **Example (partial overlap)**: {``course_id``, ``section_no``} :math:`\to` {``course_id``, ``professor_person_id``}. The ``course_id`` part of :math:`Y` is trivial, but ``professor_person_id`` is genuinely new. Because :math:`Y` is not entirely contained in :math:`X`, the overall FD is non-trivial.

   .. card::
       :class-card: sd-border-info

       **In practice**: Partial overlap FDs can always be decomposed into a trivial part plus the useful part with zero overlap. When listing FDs for normalization, we write only the zero-overlap form and discard the trivial component.


.. dropdown:: Armstrong's Axioms
   :class-container: sd-border-secondary
   :open:

   Why Do We Need Rules for Deriving FDs?
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   In practice, a set of known FDs implies **additional FDs** that are not explicitly stated. For example, if ``course_id`` :math:`\to` ``dept_id`` and ``dept_id`` :math:`\to` ``dept_name``, then ``course_id`` :math:`\to` ``dept_name`` also holds via transitivity. **Armstrong's axioms** (1974) provide a small set of inference rules that are **sound** (every derived FD is true) and **complete** (every true FD can be derived).

   The Three Axioms
   ^^^^^^^^^^^^^^^^

   1. **Reflexivity**: If :math:`Y \subseteq X`, then :math:`X \to Y`. A set of attributes always determines any of its subsets. This is why trivial FDs are always true.

   2. **Augmentation**: If :math:`X \to Y`, then :math:`XZ \to YZ` for any attribute set :math:`Z`. Adding extra attributes to both sides cannot break an existing FD. Example: given ``course_id`` :math:`\to` ``dept_id``, we get {``course_id``, ``section_no``} :math:`\to` {``dept_id``, ``section_no``}.

   3. **Transitivity**: If :math:`X \to Y` and :math:`Y \to Z`, then :math:`X \to Z`. If :math:`X` determines :math:`Y` and :math:`Y` determines :math:`Z`, then :math:`X` determines :math:`Z` through the chain.

   Two Useful Shortcuts
   ^^^^^^^^^^^^^^^^^^^^

   **Union**: If :math:`X \to Y` and :math:`X \to Z`, then :math:`X \to YZ`. Example: ``course_id`` :math:`\to` ``title`` and ``course_id`` :math:`\to` ``dept_id`` gives ``course_id`` :math:`\to` {``title``, ``dept_id``}.

   **Decomposition**: If :math:`X \to YZ`, then :math:`X \to Y` and :math:`X \to Z`.

   .. card::
       :class-card: sd-border-info

       **Why these matter**: Canonical covers (covered later) require every FD to have a single attribute on the right side. Decomposition lets us split compound right sides. Union lets us recombine them when needed.


.. dropdown:: Attribute Closure
   :class-container: sd-border-secondary
   :open:

   What Is Attribute Closure?
   ~~~~~~~~~~~~~~~~~~~~~~~~~~

   Given a set of FDs :math:`F` and a set of attributes :math:`X`, the **closure of** :math:`X` **under** :math:`F`, written :math:`X^{+}`, is the set of all attributes that are functionally determined by :math:`X`.

   Why Is This Useful?
   ^^^^^^^^^^^^^^^^^^^

   - **Test if an FD is implied**: Does :math:`X \to Y` follow from :math:`F`? Compute :math:`X^{+}` and check if :math:`Y \subseteq X^{+}`.
   - **Test if** :math:`X` **is a superkey**: Compute :math:`X^{+}` and check if :math:`X^{+} = R` (all attributes of the relation).
   - **Find candidate keys**: Find minimal sets of attributes whose closure equals :math:`R`.

   Algorithm to Compute :math:`X^{+}`
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   1. Initialize: :math:`X^{+} = X`
   2. Repeat until no change: For each FD :math:`Y \to Z` in :math:`F`, if **every attribute** in :math:`Y` is in :math:`X^{+}`, then :math:`X^{+} = X^{+} \cup Z`
   3. Return :math:`X^{+}`

   .. card::
       :class-card: sd-border-info

       **Intuition**: Start with what you know (:math:`X`). Scan the FDs. Whenever you already know the **entire** left side of an FD, add its right side to what you know. Repeat until nothing new is added. If you only know *some* attributes of the left side, you cannot fire that FD.


   Step-by-Step Closure Example
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   **Given**: ``Course_Section``(``course_id``, ``section_no``, ``title``, ``dept_id``, ``professor_person_id``) with FDs:

   - ``course_id`` :math:`\to` {``title``, ``dept_id``}
   - ``dept_id`` :math:`\to` ``dept_name``
   - {``course_id``, ``section_no``} :math:`\to` ``professor_person_id``

   **Compute** {``course_id``}\ :sup:`+`:

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
        - {``course_id``}
      * - 1
        - ``course_id`` :math:`\to` {``title``, ``dept_id``}
        - ``course_id`` :math:`\subseteq` closure
        - {``course_id``, ``title``, ``dept_id``}
      * - 2
        - ``dept_id`` :math:`\to` ``dept_name``
        - ``dept_id`` :math:`\subseteq` closure
        - {``course_id``, ``title``, ``dept_id``, ``dept_name``}
      * - 3
        - (none)
        - {``course_id``, ``section_no``} :math:`\not\subseteq` closure
        - Done

   **Result**: {``course_id``}\ :sup:`+` = {``course_id``, ``title``, ``dept_id``, ``dept_name``}.

   .. note::

      ``course_id`` :math:`\to` ``dept_name`` is not in :math:`F` directly, but the closure discovered it automatically via the chain ``course_id`` :math:`\to` ``dept_id`` :math:`\to` ``dept_name``.


.. dropdown:: Using Closures to Test Keys
   :class-container: sd-border-secondary

   Superkeys and Candidate Keys
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   - A **superkey** is any set of attributes whose closure reaches all attributes in the relation. It can uniquely identify every row, but it might contain extra columns.
   - A **candidate key** is a superkey with no unnecessary attributes. Remove any single attribute and it stops being a superkey.

   Testing {``course_id``, ``section_no``}
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   From the previous example, {``course_id``, ``section_no``}\ :sup:`+` includes all attributes, so it is a superkey. Is it minimal?

   - Test {``course_id``} alone: closure = {``course_id``, ``title``, ``dept_id``, ``dept_name``}. Missing ``section_no`` and ``professor_person_id``. **Not a superkey.**
   - Test {``section_no``} alone: closure = {``section_no``}. No FD has ``section_no`` alone on the left side. **Not a superkey.**

   Neither proper subset is a superkey, so {``course_id``, ``section_no``} is a **candidate key**.

   .. card::
       :class-card: sd-border-info

       **This confirms L3**: In the 7-step mapping algorithm, we defined the PK of ``Course_Section`` as (``course_id``, ``section_no``). Attribute closure gives us a formal proof that this choice is correct: it is a minimal superkey.


.. dropdown:: Canonical Cover (Minimal Cover)
   :class-container: sd-border-secondary

   Why Simplify FD Sets?
   ~~~~~~~~~~~~~~~~~~~~~

   FD sets collected from business rules are often messy. Before we can run normalization algorithms, we need to clean them up. Three types of clutter can appear:

   1. **Compound right sides**: :math:`X \to YZ` is really two FDs. Split it into :math:`X \to Y` and :math:`X \to Z`.

   2. **Extraneous attributes on the left side**: If {``course_id``, ``section_no``} :math:`\to` ``title`` but ``course_id`` :math:`\to` ``title`` already holds, the ``section_no`` is unnecessary.

   3. **Redundant FDs**: If ``course_id`` :math:`\to` ``dept_name`` is derivable from ``course_id`` :math:`\to` ``dept_id`` and ``dept_id`` :math:`\to` ``dept_name``, it adds no information.

   Algorithm
   ^^^^^^^^^

   A **canonical cover** :math:`F_c` is an equivalent, simplified version of :math:`F` with all three types of clutter removed:

   - **Step 1 (Decompose)**: Split all FDs so each right side is a single attribute.
   - **Step 2 (Reduce left sides)**: For each FD :math:`X \to A`, test if any attribute :math:`B \in X` is extraneous. :math:`B` is extraneous if :math:`A \in (X - \{B\})^{+}` under :math:`F`. If so, replace :math:`X` with :math:`X - \{B\}`.
   - **Step 3 (Remove redundant FDs)**: For each FD :math:`X \to A`, check if :math:`A \in X^{+}` using :math:`F - \{X \to A\}`. If yes, the FD is derivable from the others and can be removed.



Normal Forms: 1NF to BCNF
====================================================


.. dropdown:: From FDs to Normal Forms
   :class-container: sd-border-secondary
   :open:

   Connecting the Pieces
   ~~~~~~~~~~~~~~~~~~~~~

   Normal forms are tests we apply to a relation to check whether its FDs cause redundancy. Each normal form targets a specific type of problematic FD pattern. If a relation fails a test, we **decompose** it into smaller relations that pass.

   The normal forms are arranged in a hierarchy: each level eliminates a broader class of anomalies. A relation that satisfies a higher normal form automatically satisfies all lower ones.

   .. card::
       :class-card: sd-border-info

       **Workflow**: Collect business rules :math:`\to` translate to FDs :math:`\to` compute canonical cover (uses closures to remove redundancy) :math:`\to` use closures to find candidate keys :math:`\to` test each normal form :math:`\to` decompose if needed :math:`\to` verify lossless join and dependency preservation.


.. dropdown:: First Normal Form (1NF)
   :class-container: sd-border-secondary

   Definition
   ~~~~~~~~~~

   A relation is in **1NF** if every attribute contains only **atomic** (indivisible) values. No repeating groups, no nested relations, no multi-valued attributes.

   Violation Example
   ^^^^^^^^^^^^^^^^^

   .. list-table::
      :widths: 20 20 60
      :header-rows: 1
      :class: compact-table

      * - **person_id** (PK)
        - first_name
        - phone_numbers
      * - 201
        - Alice
        - 301-555-1000, 240-555-2000
      * - 202
        - Bob
        - 410-555-3000

   **Fix**: Create a separate ``Person_Phone`` table with one row per phone number.

   .. card::
       :class-card: sd-border-info

       **Recall L3**: We handled this exact pattern when mapping multi-valued attributes. The ER model flagged ``phone_numbers`` as multi-valued, and the mapping algorithm created a separate table automatically.


.. dropdown:: Second Normal Form (2NF)
   :class-container: sd-border-secondary

   Definition
   ~~~~~~~~~~

   A relation is in **2NF** if it is in 1NF, and no non-prime attribute is partially dependent on any candidate key.

   A **partial dependency** occurs when a non-prime attribute depends on only *part* of a composite candidate key. **Prime attribute**: belongs to at least one candidate key. **Non-prime attribute**: does not belong to any candidate key.

   .. note::

      2NF violations can only occur when the candidate key is **composite** (two or more attributes). If every candidate key is a single attribute, the relation is automatically in 2NF.

   Violation Example
   ^^^^^^^^^^^^^^^^^

   ``Section_Detail``\ (\ **course_id**, **section_no**, title, professor_person_id, capacity)

   FDs: ``course_id`` :math:`\to` ``title`` (partial dependency on part of the PK); {``course_id``, ``section_no``} :math:`\to` {``professor_person_id``, ``capacity``} (full dependency on the entire PK).

   **Fix**: Split into ``Course``\ (\ **course_id**, title) and ``Course_Section``\ (\ **course_id**, **section_no**, professor_person_id, capacity).


.. dropdown:: Third Normal Form (3NF)
   :class-container: sd-border-secondary

   Definition
   ~~~~~~~~~~

   A relation is in **3NF** if it is in 2NF, and no non-prime attribute is transitively dependent on any candidate key.

   A **transitive dependency** occurs when :math:`A \to B` and :math:`B \to C` (where :math:`B` is not a superkey and :math:`B \not\to A`), creating an indirect path :math:`A \to C`.

   **Formal test**: For every non-trivial FD :math:`X \to Y`, at least one must hold: :math:`X` is a superkey, or every attribute in :math:`Y` is prime (belongs to some candidate key).

   .. card::
       :class-card: sd-border-info

       **Intuition**: 3NF says non-key attributes must depend *directly* on the key, not through another non-key attribute. If ``course_id`` :math:`\to` ``dept_id`` :math:`\to` ``dept_name``, then ``dept_name`` reaches the key only via the middleman ``dept_id``. That middleman creates redundancy.

   Violation Example
   ^^^^^^^^^^^^^^^^^

   ``Course``\ (\ **course_id**, title, dept_id, dept_name)

   The FD ``dept_id`` :math:`\to` ``dept_name`` violates 3NF because ``dept_id`` is not a superkey.

   **Fix**: Split into ``Course``\ (\ **course_id**, title, dept_id) and ``Department``\ (\ **dept_id**, dept_name).


.. dropdown:: Boyce-Codd Normal Form (BCNF)
   :class-container: sd-border-secondary

   Definition
   ~~~~~~~~~~

   A relation :math:`R` is in **BCNF** if for every non-trivial FD :math:`X \to Y`, :math:`X` is a superkey. In other words: *every determinant must be a superkey*. No exceptions.

   How Does BCNF Differ from 3NF?
   ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

   3NF has an escape clause: the FD :math:`X \to Y` is allowed if :math:`Y` consists entirely of prime attributes, even when :math:`X` is not a superkey. BCNF removes this exception.

   .. list-table::
      :widths: 50 25 25
      :header-rows: 1
      :class: compact-table

      * - For every non-trivial FD :math:`X \to Y`
        - 3NF
        - BCNF
      * - :math:`X` is a superkey
        - Passes
        - Passes
      * - :math:`X` is not a superkey, but :math:`Y` is all prime
        - Passes
        - **Fails**
      * - :math:`X` is not a superkey and :math:`Y` has non-prime attrs
        - Fails
        - Fails

   .. card::
       :class-card: sd-border-info

       **Trade-off**: BCNF eliminates all FD-based anomalies, but its decomposition may not preserve all FDs. 3NF always preserves FDs but may leave some anomalies.


.. dropdown:: Normal Form Summary
   :class-container: sd-border-secondary

   Quick Reference
   ~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 12 40 48
      :header-rows: 1
      :class: compact-table

      * - NF
        - Requirement
        - Eliminates
      * - **1NF**
        - Atomic values only
        - Multi-valued attributes, nested tables
      * - **2NF**
        - 1NF + no partial dependencies
        - Redundancy from attributes depending on part of a composite key
      * - **3NF**
        - 2NF + no transitive dependencies
        - Redundancy from non-key attributes determining other non-key attributes
      * - **BCNF**
        - Every determinant is a superkey
        - All anomalies caused by functional dependencies

   .. card::
       :class-card: sd-border-info

       **Practical guideline**: Aim for BCNF in OLTP systems. Fall back to 3NF only when BCNF decomposition loses a dependency that must be enforced efficiently (without joins).



Decomposition Algorithms
====================================================


.. dropdown:: Desirable Properties
   :class-container: sd-border-secondary
   :open:

   Two Critical Properties
   ~~~~~~~~~~~~~~~~~~~~~~~

   1. **Lossless Join (Non-additive Join)**: Joining the decomposed relations reconstructs the original relation *exactly*. No spurious (phantom) tuples are introduced. **Always required**: Without this, decomposition corrupts data.

   2. **Dependency Preservation**: Every FD in the original set can be checked on at least one decomposed relation (without joining tables). Allows efficient constraint enforcement. **Desirable but not always achievable**: 3NF synthesis guarantees it; BCNF decomposition may sacrifice it.

   .. card::
       :class-card: sd-border-info

       **Trade-off**: 3NF decomposition preserves both properties. BCNF decomposition guarantees lossless join but may lose dependency preservation. Choose based on system requirements.

   Lossless Join Test
   ^^^^^^^^^^^^^^^^^^

   A decomposition of :math:`R` into :math:`R_1` and :math:`R_2` is lossless if and only if :math:`R_1 \cap R_2 \to R_1` or :math:`R_1 \cap R_2 \to R_2`. The common attributes must be a superkey of at least one side.


.. dropdown:: 3NF Synthesis Algorithm
   :class-container: sd-border-secondary

   Algorithm to Decompose into 3NF
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Input**: Relation :math:`R` with FD set :math:`F`

   **Output**: A set of relations in 3NF with both lossless join and dependency preservation.

   **Steps**:

   1. **Step 1**: Compute the canonical cover :math:`F_c`.
   2. **Step 2**: For each FD :math:`X \to A` in :math:`F_c`, create a relation :math:`R_i = X \cup \{A\}`. If multiple FDs share the same left side :math:`X`, combine them into one relation.
   3. **Step 3**: If none of the resulting relations contains a candidate key of :math:`R`, add a relation consisting of a candidate key.
   4. **Step 4**: Remove any relation :math:`R_i` that is a subset of another relation :math:`R_j`.

   .. card::
       :class-card: sd-border-info

       **Guarantees**: This algorithm always produces a lossless-join, dependency-preserving decomposition into 3NF. Step 3 ensures lossless join; the fact that every FD in :math:`F_c` has its own relation ensures dependency preservation.


.. dropdown:: BCNF Decomposition Algorithm
   :class-container: sd-border-secondary

   Algorithm to Decompose into BCNF
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Input**: Relation :math:`R` with FD set :math:`F`

   **Output**: A set of relations in BCNF with lossless join (dependency preservation not guaranteed).

   **Steps**:

   1. **Step 1**: Check if :math:`R` is in BCNF. If yes, stop.
   2. **Step 2**: Find an FD :math:`X \to Y` that violates BCNF (i.e., :math:`X` is not a superkey of :math:`R`).
   3. **Step 3**: Decompose :math:`R` into :math:`R_1 = X \cup Y` and :math:`R_2 = R - (Y - X)`.
   4. **Step 4**: Recursively apply to :math:`R_1` and :math:`R_2`.

   .. card::
       :class-card: sd-border-info

       **Why is this lossless?** At each step, :math:`R_1 \cap R_2 = X`, and :math:`X \to Y` means :math:`X` is a superkey of :math:`R_1 = X \cup Y`. The lossless join condition is satisfied at every decomposition step.


.. dropdown:: BCNF vs. 3NF Trade-offs
   :class-container: sd-border-secondary

   When to Use Each
   ~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 20 40 40
      :header-rows: 1
      :class: compact-table

      * - Property
        - 3NF Synthesis
        - BCNF Decomposition
      * - Lossless join
        - Always
        - Always
      * - Dependency preservation
        - Always
        - Not guaranteed
      * - Anomaly elimination
        - Eliminates most
        - Eliminates all FD-based anomalies
      * - When to use
        - FD enforcement must be efficient (no cross-table checks)
        - Data integrity is paramount and joins are acceptable

   .. card::
       :class-card: sd-border-info

       **Practical guideline**: Start with BCNF. If the decomposition loses a critical dependency (one that must be checked on every INSERT), fall back to 3NF for those specific relations. Most real-world schemas reach BCNF without losing any dependencies.



When to Denormalize
====================================================


.. dropdown:: Motivation
   :class-container: sd-border-secondary
   :open:

   Why Denormalize?
   ~~~~~~~~~~~~~~~~

   **Normalization optimizes for write consistency**. Denormalization optimizes for **read performance**.

   1. **Read-heavy workloads**: Reporting dashboards, analytics, data warehouses. Normalized schemas require many joins for complex queries. Denormalization reduces join count, improving query speed.

   2. **Predictable query patterns**: Known, repetitive queries. If 90% of queries need the same joined data, store it pre-joined.

   3. **Performance bottlenecks**: Profiling shows slow joins. Measure first: denormalize only proven pain points.

   .. warning::

      **Golden rule**: Normalize first, denormalize later. Always start with a normalized schema. Add denormalization only when performance testing justifies it.


.. dropdown:: Costs of Denormalization
   :class-container: sd-border-secondary

   The Price You Pay
   ~~~~~~~~~~~~~~~~~

   1. **Redundancy returns**: Data is duplicated across tables. Increased storage and risk of stale data.

   2. **Update complexity**: Changes must propagate to multiple locations. Application code or triggers must maintain consistency.

   3. **Anomalies return**: The insertion, deletion, and update anomalies come back, mitigated by triggers, application logic, or periodic reconciliation.

   4. **Schema rigidity**: Denormalized schemas are harder to evolve. Adding a new attribute may require updating multiple tables and their synchronization logic.


.. dropdown:: Denormalization Patterns
   :class-container: sd-border-secondary

   Common Techniques
   ~~~~~~~~~~~~~~~~~

   1. **Materialized Views**: Precompute and store query results as a physical table. Database refreshes the view periodically or on demand. Example: Store enrollment counts per course per semester.

   2. **Redundant Columns**: Copy a column from a related table into a frequently queried table. Example: Add ``dept_name`` to ``Course`` (even though it lives in ``Department``). Use triggers to keep copies synchronized.

   3. **Summary Tables**: Precompute aggregates (SUM, COUNT, AVG) into a dedicated table. Example: ``Semester_GPA_Summary`` with average GPA per student per semester.

   4. **Stored Derived Attributes**: Physically store a value that can be computed from other columns. Example: ``total_credits`` in ``Student`` derived from summing completed course credits.


.. dropdown:: Materialized View Example
   :class-container: sd-border-secondary

   Precomputing Expensive Joins
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   **Scenario**: A dashboard frequently needs student names with their enrollments and grades.

   **Normalized query** (requires 3 joins):

   .. code-block:: sql

      SELECT p.first_name, p.last_name, c.title, e.grade
      FROM Person p
      JOIN Enrollment e ON p.person_id = e.student_person_id
      JOIN Course_Section cs ON e.course_id = cs.course_id
                             AND e.section_no = cs.section_no
      JOIN Course c ON cs.course_id = c.course_id
      WHERE cs.semester = 'Spring' AND cs.year = 2026;

   **Denormalized solution**: Materialized view

   .. code-block:: sql

      CREATE MATERIALIZED VIEW Student_Enrollment_MV AS
      SELECT p.first_name, p.last_name, c.title,
             e.grade, cs.semester, cs.year
      FROM Person p
      JOIN Enrollment e ON p.person_id = e.student_person_id
      JOIN Course_Section cs ON e.course_id = cs.course_id
                             AND e.section_no = cs.section_no
      JOIN Course c ON cs.course_id = c.course_id;

   **Dashboard query** (zero joins):

   .. code-block:: sql

      SELECT * FROM Student_Enrollment_MV
      WHERE semester = 'Spring' AND year = 2026;


.. dropdown:: Redundant Column Example
   :class-container: sd-border-secondary

   Avoiding Repetitive Joins
   ~~~~~~~~~~~~~~~~~~~~~~~~~

   **Scenario**: Course listings always show department name alongside course title. The join to ``Department`` happens in 80% of queries.

   **Denormalized schema**: Add ``dept_name`` to ``Course``.

   **Maintenance**: Use a trigger to keep ``dept_name`` synchronized:

   .. code-block:: postgresql

      CREATE OR REPLACE FUNCTION sync_dept_name()
      RETURNS TRIGGER AS $$
      BEGIN
          UPDATE Course SET dept_name = NEW.dept_name
          WHERE dept_id = NEW.dept_id;
          RETURN NEW;
      END;
      $$ LANGUAGE plpgsql;

      CREATE TRIGGER trg_sync_dept_name
      AFTER UPDATE OF dept_name ON Department
      FOR EACH ROW EXECUTE FUNCTION sync_dept_name();


.. dropdown:: OLTP vs. OLAP
   :class-container: sd-border-secondary

   Different Needs, Different Schemas
   ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

   .. list-table::
      :widths: 18 41 41
      :header-rows: 1
      :class: compact-table

      * - Aspect
        - OLTP
        - OLAP
      * - Goal
        - Fast writes, data integrity
        - Fast reads, aggregations
      * - Normalization
        - High (3NF/BCNF)
        - Low (star/snowflake schemas)
      * - Queries
        - Simple, predictable (CRUD)
        - Complex, ad-hoc (joins, aggregates)
      * - Updates
        - Frequent
        - Rare (periodic batch loads)
      * - Schema
        - Normalized, many tables
        - Denormalized, few large tables
      * - Example
        - Course registration system
        - Enrollment analytics dashboard

   .. card::
       :class-card: sd-border-info

       **Hybrid approach**: Keep OLTP normalized. Use ETL (Extract-Transform-Load) to populate denormalized OLAP schemas (data warehouses). This cleanly separates write-optimized and read-optimized workloads.


.. dropdown:: Guidelines for Safe Denormalization
   :class-container: sd-border-secondary

   Best Practices
   ~~~~~~~~~~~~~~

   1. **Measure before optimizing**: Profile queries with ``EXPLAIN ANALYZE``. Identify actual bottlenecks, not perceived ones.

   2. **Consider alternatives first**: Indexes (can a covering index eliminate the join?), query optimization (can rewriting or caching help?), hardware (is the bottleneck disk I/O, CPU, or network?).

   3. **Automate consistency maintenance**: Use triggers, stored procedures, or application-layer sync. Never rely on manual updates.

   4. **Document the denormalization**: Explain why, when, and how to maintain it. Future developers must understand the trade-off.

   5. **Monitor data consistency**: Periodic audits to detect drift between source and copy. Reconciliation jobs to fix discrepancies.



Wrap-Up and Next Steps
====================================================


Key Takeaways
--------------

1. **Normalization eliminates anomalies** by ensuring each fact is stored exactly once.

2. **Functional dependencies** encode business rules and are the foundation of all normalization decisions.

3. **Armstrong's axioms** provide a sound and complete system for deriving new FDs from known ones.

4. **Normal forms form a hierarchy**: 1NF :math:`\subset` 2NF :math:`\subset` 3NF :math:`\subset` BCNF, each eliminating more anomalies.

5. **Attribute closure** (:math:`X^{+}`) is the workhorse tool: it tests FDs, identifies superkeys, and drives decomposition.

6. **Lossless join** is mandatory; **dependency preservation** is desirable (guaranteed by 3NF, not always by BCNF).

7. **Denormalization trades integrity for performance**; use it strategically for read-heavy workloads with proven bottlenecks.