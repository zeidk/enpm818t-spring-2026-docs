====================================================
Lecture
====================================================



Why Normalization Matters
====================================================


.. dropdown:: What Is Normalization?
   :class-container: sd-border-secondary
   :open:

   .. rubric:: Definition


   **Normalization** is the process of organizing a relational database schema to reduce redundancy and improve data integrity by decomposing relations into smaller, well-structured relations based on their functional dependencies.

   .. rubric:: Key Ideas


   1. Each relation should represent **one fact about one entity**. A student table stores student data, not course data.

   2. Decomposition is guided by **functional dependencies** (formal rules about which attributes determine others).

   3. Normal forms (1NF, 2NF, 3NF, BCNF) provide **progressively stricter** criteria for a well-designed schema.

   .. card::
       :class-card: sd-border-info

       **Analogy**: Think of normalization as decluttering a filing cabinet. Instead of one overstuffed folder with duplicated papers, you create clearly labeled folders where each piece of information lives in exactly one place.


.. dropdown:: Where Normalization Fits
   :class-container: sd-border-secondary

   .. rubric:: The Database Design Pipeline


   A careful ER design often produces schemas that are already close to normalized. However, mapping to relations can introduce redundancy, especially with composite keys, multi-valued attributes, and complex relationships. Normalization is a formal verification and repair step that catches what intuition may miss.

   The pipeline is: **Conceptual Model (ERD)** :math:`\to` **Logical Model (tables)** :math:`\to` **Normalization (verify and repair)** :math:`\to` **Physical Model (SQL)**.


.. dropdown:: The Problem: Data Redundancy
   :class-container: sd-border-secondary
   :open:

   .. rubric:: A Poorly Designed Table


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

   .. rubric:: What Goes Wrong?


   Because the ``Course_Enrollment`` table stores facts about multiple entities in one relation, three types of anomalies arise:

   1. **Insertion Anomaly**: Can't add a new course unless at least one student enrolls in it. We want to add ENPM808X (Advanced Python) to the catalog, but the table requires a ``student_id``. Without a student, we cannot insert the course.

   2. **Deletion Anomaly**: Deleting the last enrollment for a course deletes course information. If Alice drops ENPM702 and she is the only student, we lose all information about that course (title, department, professor).

   3. **Update Anomaly**: Changing course information requires updating multiple rows. If Dr. Smith changes name to Dr. Smith-Jones, we must find and update *all* rows with ENPM818T. Partial updates create inconsistency: some rows say "Dr. Smith", others say "Dr. Smith-Jones".


.. dropdown:: The Solution: Normalization
   :class-container: sd-border-secondary

   .. rubric:: After Normalization


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

   .. rubric:: Four Primary Goals


   1. **Minimize redundancy**: Store each fact exactly once. Reduces storage and prevents inconsistency from partial updates.

   2. **Eliminate anomalies**: Prevent the insertion, deletion, and update problems we just saw. Data integrity is enforced by schema structure, not application logic.

   3. **Isolate entities**: Each relation represents one concept. Updating a department name in ``Department`` requires changing one row, not every course that references it.

   4. **Support schema evolution**: Well-normalized schemas adapt to new requirements. Adding an attribute to ``Course`` does not require restructuring ``Enrollment`` or ``Student``.

   .. card::
       :class-card: sd-border-info

       **Trade-off**: More tables means more joins. For read-heavy workloads with predictable queries, strategic denormalization may improve performance (covered later in this lecture).


.. dropdown:: Normalization Workflow
   :class-container: sd-border-secondary

   .. rubric:: From Business Rules to a Verified Schema


   The full normalization pipeline proceeds through these stages:

   **Collect business rules** :math:`\to` **Translate rules to FDs** :math:`\to` **Compute canonical cover** :math:`\to` **Find candidate keys (closures)** :math:`\to` **Test normal forms** :math:`\to` **Decompose if needed** :math:`\to` **Verify lossless join and dependency preservation**.

   .. card::
       :class-card: sd-border-info

       Each stage builds on the previous one. FDs encode the business rules. The canonical cover removes redundancy from the FD set. Closures test superkeys. Normal form tests identify violations. Decomposition eliminates them.


.. dropdown:: Discussion: Spot the Anomaly
   :class-container: sd-border-secondary

   .. rubric:: Discussion (5 min)


   Consider these two tables from the L3 schema:

   - ``Course``\(**course_id**, title, credits, *dept_id*)
   - ``Department``\(**dept_id**, dept_name, building, budget)

   **Imagine merging them** into a single flat table: ``Course_Dept``\(**course_id**, title, credits, dept_id, dept_name, building, budget).

   **With a partner, identify**:

   - Which columns would be repeated across rows?
   - Which of the three anomalies (insertion, deletion, update) would this merged table suffer from?
   - Write a concrete example row that demonstrates each problem.

   .. card::
       :class-card: sd-border-info

       **Goal**: Build intuition for why the L3 mapping algorithm already produces mostly-normalized schemas, and understand what normalization theory formalizes.



Functional Dependencies
====================================================


.. dropdown:: Why We Need Them
   :class-container: sd-border-secondary
   :open:

   .. rubric:: From Intuition to Formalism


   In the previous section, we relied on intuition to identify problems and decompose the ``Course_Enrollment`` table. But consider these questions: How do we **know** which columns cause redundancy? How do we decide **where to split** a table? How do we **prove** the result is correct?

   .. rubric:: The Role of Functional Dependencies


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

   .. rubric:: Definition


   A **functional dependency** (FD), written :math:`X \to Y`, states that for each value of :math:`X`, there is exactly one corresponding value of :math:`Y`. The name comes from mathematics: :math:`Y` is a *function* of :math:`X`. Both :math:`X` and :math:`Y` can be single attributes or sets of multiple attributes. Formally, given a relation schema :math:`R` with :math:`X, Y \subseteq R`:

   .. math::

      \forall\, t_{1}, t_{2}\in r(R): \; t_{1}[X] = t_{2}[X] \implies t_{1}[Y] = t_{2}[Y]

   For every pair of tuples :math:`t_1` and :math:`t_2` in the relation: if they have the same values on **all** attributes in :math:`X`, then they must also have the same values on **all** attributes in :math:`Y`.

   .. rubric:: Terminology


   - :math:`X` is the **determinant** (left-hand side), one or more attributes
   - :math:`Y` is the **dependent** (right-hand side), one or more attributes
   - Read :math:`X \to Y` as ":math:`X` determines :math:`Y`"
   - Example: {``student_person_id``, ``course_id``, ``section_no``} :math:`\to` {``grade``} is an FD where :math:`X` has three attributes


.. dropdown:: FDs from University Business Rules
   :class-container: sd-border-secondary

   .. rubric:: Intuition with Examples


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


.. dropdown:: Exercise: Business Rules to FDs
   :class-container: sd-border-secondary

   .. rubric:: Exercise (5 min)


   A university library tracks book loans with this table:

   .. list-table::
      :widths: 15 20 20 20 25
      :header-rows: 1
      :class: compact-table

      * - **loan_id** (PK)
        - isbn
        - book_title
        - borrower_id
        - borrower_name
      * - 5001
        - 978-0133970
        - Databases
        - 201
        - Alice
      * - 5002
        - 978-0133970
        - Databases
        - 202
        - Bob
      * - 5003
        - 978-0596517
        - JavaScript
        - 201
        - Alice

   **Business rules**: each loan is assigned a unique ID; each loan records exactly one book and one borrower; each ISBN corresponds to exactly one book title; each borrower has a unique borrower ID and exactly one name; a borrower may borrow multiple books, and a book may be borrowed by multiple borrowers.

   **Tasks**:

   1. Translate the business rules above into FDs.
   2. Someone claims ``borrower_id`` :math:`\to` ``isbn``. Is that consistent with the business rules? Can the data confirm or disprove it?
   3. What is the smallest set of columns you would need to know to uniquely identify a single row?


.. dropdown:: Trivial and Non-Trivial FDs
   :class-container: sd-border-secondary

   .. rubric:: Trivial FD: :math:`X \to Y` where :math:`Y \subseteq X`


   A trivial FD is one where the dependent is already part of the determinant. It is always true regardless of the data or business rules.

   Examples: {``student_person_id``, ``course_id``} :math:`\to` ``student_person_id``; {``course_id``, ``section_no``} :math:`\to` ``course_id``; ``person_id`` :math:`\to` ``person_id``.

   Normalization cares about FDs that reveal **hidden structure**: which attributes determine other, *different* attributes. Trivial FDs reveal nothing because the answer is already contained in the question.

   .. rubric:: Non-Trivial FD: :math:`X \to Y` where :math:`Y \not\subseteq X`


   A non-trivial FD is one where the dependent contains at least one attribute **not already in** the determinant. These encode real business constraints.

   **Example (no overlap)**: ``person_id`` :math:`\to` ``first_name``. The right side is entirely new information, requiring a business rule: each person has exactly one first name.

   **Example (partial overlap)**: {``course_id``, ``section_no``} :math:`\to` {``course_id``, ``professor_person_id``}. The ``course_id`` part of :math:`Y` is trivial, but ``professor_person_id`` is genuinely new. Because :math:`Y` is not entirely contained in :math:`X`, the overall FD is non-trivial.

   .. card::
       :class-card: sd-border-info

       **In practice**: Partial overlap FDs can always be decomposed into a trivial part plus the useful part with zero overlap. When listing FDs for normalization, we write only the zero-overlap form and discard the trivial component.


.. dropdown:: Armstrong's Axioms
   :class-container: sd-border-secondary
   :open:

   .. rubric:: Why Do We Need Rules for Deriving FDs?


   In practice, a set of known FDs implies **additional FDs** that are not explicitly stated. For example, if ``course_id`` :math:`\to` ``dept_id`` and ``dept_id`` :math:`\to` ``dept_name``, then ``course_id`` :math:`\to` ``dept_name`` also holds via transitivity. **Armstrong's axioms** (1974) provide a small set of inference rules that are **sound** (every derived FD is true) and **complete** (every true FD can be derived).

   .. rubric:: The Three Axioms


   1. **Reflexivity**: If :math:`Y \subseteq X`, then :math:`X \to Y`. A set of attributes always determines any of its subsets. This is why trivial FDs are always true.

   2. **Augmentation**: If :math:`X \to Y`, then :math:`XZ \to YZ` for any attribute set :math:`Z`. Adding extra attributes to both sides cannot break an existing FD. Example: given ``course_id`` :math:`\to` ``dept_id``, we get {``course_id``, ``section_no``} :math:`\to` {``dept_id``, ``section_no``}.

   3. **Transitivity**: If :math:`X \to Y` and :math:`Y \to Z`, then :math:`X \to Z`. If :math:`X` determines :math:`Y` and :math:`Y` determines :math:`Z`, then :math:`X` determines :math:`Z` through the chain.

   .. rubric:: Two Useful Shortcuts


   **Union**: If :math:`X \to Y` and :math:`X \to Z`, then :math:`X \to YZ`. Example: ``course_id`` :math:`\to` ``title`` and ``course_id`` :math:`\to` ``dept_id`` gives ``course_id`` :math:`\to` {``title``, ``dept_id``}.

   **Decomposition**: If :math:`X \to YZ`, then :math:`X \to Y` and :math:`X \to Z`.

   .. card::
       :class-card: sd-border-info

       **Why these matter**: Canonical covers (covered later) require every FD to have a single attribute on the right side. Decomposition lets us split compound right sides. Union lets us recombine them when needed.

   .. rubric:: Putting the Axioms to Work


   **Deriving a new FD using transitivity**:

   - ``course_id`` :math:`\to` ``dept_id`` (given in :math:`F`)
   - ``dept_id`` :math:`\to` ``dept_name`` (given in :math:`F`)
   - By **transitivity**: ``course_id`` :math:`\to` ``dept_name``

   We now know three FDs with ``course_id`` on the left: ``course_id`` :math:`\to` ``title``, ``course_id`` :math:`\to` ``dept_id``, ``course_id`` :math:`\to` ``dept_name``.

   **Combining FDs using union**: ``course_id`` :math:`\to` ``title`` and ``course_id`` :math:`\to` ``dept_id`` gives by union: ``course_id`` :math:`\to` {``title``, ``dept_id``}. Adding ``course_id`` :math:`\to` ``dept_name`` gives: ``course_id`` :math:`\to` {``title``, ``dept_id``, ``dept_name``}.

   .. note::

      **To derive** an FD means to prove it holds using the axioms, starting from the given FDs. If you can build a chain of axiom applications that produces the FD, it is derived. If no chain can reach it, it does not follow from :math:`F`.


.. dropdown:: Exercise: Applying Armstrong's Axioms
   :class-container: sd-border-secondary

   .. rubric:: Exercise (5 min)


   **Given FDs**: :math:`F = \{A \to B, \; B \to C, \; C \to D\}`

   **Tasks**:

   1. Using **transitivity**, derive :math:`A \to D`. Write out each step.
   2. Using **union**, combine your results to show :math:`A \to \{B, C, D\}`.
   3. **Challenge**: Does :math:`C \to A` hold? Can you prove it or disprove it from :math:`F` alone?

   .. card::
       :class-card: sd-border-info

       **Hint**: For the challenge question, think about what the axioms can and cannot derive. Soundness means we only derive true FDs, so if you cannot derive it, it does not follow from :math:`F`.


.. dropdown:: Attribute Closure
   :class-container: sd-border-secondary
   :open:

   .. rubric:: What Is Attribute Closure?


   Given a set of FDs :math:`F` and a set of attributes :math:`X`, the **closure of** :math:`X` **under** :math:`F`, written :math:`X^{+}`, is the set of all attributes that are functionally determined by :math:`X`.

   .. rubric:: Why Is This Useful?


   - **Test if an FD is implied**: Does :math:`X \to Y` follow from :math:`F`? Compute :math:`X^{+}` and check if :math:`Y \subseteq X^{+}`.
   - **Test if** :math:`X` **is a superkey**: Compute :math:`X^{+}` and check if :math:`X^{+} = R` (all attributes of the relation).
   - **Find candidate keys**: Find minimal sets of attributes whose closure equals :math:`R`.

   .. rubric:: Algorithm to Compute :math:`X^{+}`


   1. Initialize: :math:`X^{+} = X`
   2. Repeat until no change: For each FD :math:`Y \to Z` in :math:`F`, if **every attribute** in :math:`Y` is in :math:`X^{+}`, then :math:`X^{+} = X^{+} \cup Z`
   3. Return :math:`X^{+}`

   .. card::
       :class-card: sd-border-info

       **Intuition**: Start with what you know (:math:`X`). Scan the FDs. Whenever you already know the **entire** left side of an FD, add its right side to what you know. Repeat until nothing new is added. If you only know *some* attributes of the left side, you cannot fire that FD.


   .. rubric:: Step-by-Step Closure Example


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


   .. rubric:: A Larger Closure Example


   **Given**: :math:`R(A, B, C, D, E)` with :math:`F = \{A \to B, \; BC \to D, \; D \to E, \; E \to A\}`

   **Compute** :math:`\{A, C\}^{+}`:

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
        - {A, C}
      * - 1
        - :math:`A \to B`
        - A in closure
        - {A, B, C}
      * - 2
        - :math:`BC \to D`
        - B and C both in closure
        - {A, B, C, D}
      * - 3
        - :math:`D \to E`
        - D in closure
        - {A, B, C, D, E}
      * - 4
        - (none)
        - No new attributes
        - Done

   **Result**: :math:`\{A, C\}^{+} = \{A, B, C, D, E\} = R`. This means :math:`\{A, C\}` is a superkey.


.. dropdown:: Using Closures to Test Keys
   :class-container: sd-border-secondary

   .. rubric:: Superkeys and Candidate Keys


   - A **superkey** is any set of attributes whose closure reaches all attributes in the relation. It can uniquely identify every row, but it might contain extra columns.
   - A **candidate key** is a superkey with no unnecessary attributes. Remove any single attribute and it stops being a superkey.

   .. rubric:: Testing {``course_id``, ``section_no``}


   From the previous example, {``course_id``, ``section_no``}\ :sup:`+` includes all attributes, so it is a superkey. Is it minimal?

   - Test {``course_id``} alone: closure = {``course_id``, ``title``, ``dept_id``, ``dept_name``}. Missing ``section_no`` and ``professor_person_id``. **Not a superkey.**
   - Test {``section_no``} alone: closure = {``section_no``}. No FD has ``section_no`` alone on the left side. **Not a superkey.**

   Neither proper subset is a superkey, so {``course_id``, ``section_no``} is a **candidate key**.

   .. card::
       :class-card: sd-border-info

       **This confirms L3**: In the 7-step mapping algorithm, we defined the PK of ``Course_Section`` as (``course_id``, ``section_no``). Attribute closure gives us a formal proof that this choice is correct: it is a minimal superkey.


.. dropdown:: Exercise: Compute a Closure
   :class-container: sd-border-secondary

   .. rubric:: Exercise (7 min)


   **Given**: :math:`R(A, B, C, D, E)` with :math:`F = \{A \to B, \; BC \to D, \; D \to E, \; E \to A\}`

   **Tasks**:

   1. Compute :math:`\{A, C\}^{+}`. Show each step in a table.
   2. Is :math:`\{A, C\}` a superkey? Justify.
   3. Is :math:`\{A, C\}` a candidate key? Test each proper subset.
   4. Can you find a *different* candidate key? (Hint: look at what :math:`E` determines.)

   .. card::
       :class-card: sd-border-info

       **After finishing**: Compare answers with a neighbor. If you found different candidate keys, verify both using closures.


.. dropdown:: Canonical Cover (Minimal Cover)
   :class-container: sd-border-secondary

   .. rubric:: Why Simplify FD Sets?


   FD sets collected from business rules are often messy. Before we can run normalization algorithms, we need to clean them up. Three types of clutter can appear:

   1. **Compound right sides**: :math:`X \to YZ` is really two FDs. Split it into :math:`X \to Y` and :math:`X \to Z`.

   2. **Extraneous attributes on the left side**: If {``course_id``, ``section_no``} :math:`\to` ``title`` but ``course_id`` :math:`\to` ``title`` already holds, the ``section_no`` is unnecessary.

   3. **Redundant FDs**: If ``course_id`` :math:`\to` ``dept_name`` is derivable from ``course_id`` :math:`\to` ``dept_id`` and ``dept_id`` :math:`\to` ``dept_name``, it adds no information.

   .. rubric:: Algorithm


   A **canonical cover** :math:`F_c` is an equivalent, simplified version of :math:`F` with all three types of clutter removed:

   - **Step 1 (Decompose)**: Split all FDs so each right side is a single attribute.
   - **Step 2 (Reduce left sides)**: For each FD :math:`X \to A`, test if any attribute :math:`B \in X` is extraneous. :math:`B` is extraneous if :math:`A \in (X - \{B\})^{+}` under :math:`F`. If so, replace :math:`X` with :math:`X - \{B\}`.
   - **Step 3 (Remove redundant FDs)**: For each FD :math:`X \to A`, check if :math:`A \in X^{+}` using :math:`F - \{X \to A\}`. If yes, the FD is derivable from the others and can be removed.

   .. rubric:: Worked Example: :math:`R(A, B, C)` with :math:`F = \{A \to BC, \; B \to C, \; A \to B, \; AB \to C\}`


   **Step 1 -- Decompose compound right sides**: Split :math:`A \to BC` into :math:`A \to B` and :math:`A \to C`. Remove the duplicate :math:`A \to B`.

   After Step 1: :math:`F = \{A \to B, \; A \to C, \; B \to C, \; AB \to C\}`

   **Step 2 -- Reduce left sides**: Only :math:`AB \to C` has a composite left side. Test whether A is extraneous: compute :math:`\{B\}^{+} = \{B, C\}`. C is in the closure, so A is unnecessary. Test whether B is extraneous: compute :math:`\{A\}^{+} = \{A, B, C\}`. C is in the closure, so B is also unnecessary. Both are extraneous -- we remove one at a time. Dropping B from the left side turns :math:`AB \to C` into :math:`A \to C` (already in :math:`F`, so the duplicate is deleted).

   After Step 2: :math:`F = \{A \to B, \; A \to C, \; B \to C\}`

   **Step 3 -- Remove redundant FDs**: Test :math:`A \to C` by removing it and computing :math:`\{A\}^{+}` with :math:`\{A \to B, \; B \to C\}`: fires :math:`A \to B` then :math:`B \to C`, reaching C. So :math:`A \to C` is redundant -- remove it. The other two FDs are not redundant.

   **Result**: :math:`F_c = \{A \to B, \; B \to C\}`. Four FDs reduced to two, equivalent sets.


.. dropdown:: Exercise: Compute a Canonical Cover
   :class-container: sd-border-secondary

   .. rubric:: Exercise (7 min)


   **Given**: :math:`R(A, B, C, D)` with :math:`F = \{A \to BD, \; B \to C, \; C \to B, \; AB \to D\}`

   **Tasks**:

   1. **Step 1**: Decompose compound right sides. How many FDs do you have now?
   2. **Step 2**: Test for extraneous left-side attributes. In :math:`AB \to D`, is B extraneous? (Hint: compute :math:`\{A\}^{+}` under the current :math:`F`.)
   3. **Step 3**: Test for redundant FDs. Can any remaining FD be derived from the others?
   4. Write out the final :math:`F_c`.

   .. card::
       :class-card: sd-border-info

       **Self-check**: Your canonical cover should have 4 FDs, each with a single attribute on both sides.



Normal Forms: 1NF to BCNF
====================================================


.. dropdown:: From FDs to Normal Forms
   :class-container: sd-border-secondary
   :open:

   .. rubric:: Connecting the Pieces


   Normal forms are tests we apply to a relation to check whether its FDs cause redundancy. Each normal form targets a specific type of problematic FD pattern. If a relation fails a test, we **decompose** it into smaller relations that pass.

   The normal forms are arranged in a hierarchy: each level eliminates a broader class of anomalies. A relation that satisfies a higher normal form automatically satisfies all lower ones.

   .. card::
       :class-card: sd-border-info

       **Workflow**: Collect business rules :math:`\to` translate to FDs :math:`\to` compute canonical cover (uses closures to remove redundancy) :math:`\to` use closures to find candidate keys :math:`\to` test each normal form :math:`\to` decompose if needed :math:`\to` verify lossless join and dependency preservation.


.. dropdown:: First Normal Form (1NF)
   :class-container: sd-border-secondary

   .. rubric:: Definition


   A relation is in **1NF** if every attribute contains only **atomic** (indivisible) values. No repeating groups, no nested relations, no multi-valued attributes.

   .. rubric:: Violation Example


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

   .. rubric:: Fix: Decompose into Two Relations


   **``Person``** (**person_id**, first_name) and **``Person_Phone``** (**person_id**, **phone_number**). The composite PK in ``Person_Phone`` ensures each (person, phone) pair is unique.

   .. card::
       :class-card: sd-border-info

       **Recall L3**: We handled this exact pattern when mapping multi-valued attributes. The ER model flagged ``phone_numbers`` as multi-valued, and the mapping algorithm created a separate table automatically.


.. dropdown:: Second Normal Form (2NF)
   :class-container: sd-border-secondary

   .. rubric:: Definition


   A relation is in **2NF** if it is in 1NF, and no non-prime attribute is partially dependent on any candidate key.

   A **partial dependency** occurs when a non-prime attribute depends on only *part* of a composite candidate key. **Prime attribute**: belongs to at least one candidate key. **Non-prime attribute**: does not belong to any candidate key.

   .. note::

      2NF violations can only occur when the candidate key is **composite** (two or more attributes). If every candidate key is a single attribute, the relation is automatically in 2NF.

   .. rubric:: Step-by-Step 2NF Testing


   Given ``Section_Detail``\(**course_id**, **section_no**, title, professor_person_id, capacity) with FDs:

   - :math:`FD_1`: ``course_id`` :math:`\to` ``title`` (partial)
   - :math:`FD_2`: {``course_id``, ``section_no``} :math:`\to` {``professor_person_id``, ``capacity``} (full)

   **Step 1 -- Find candidate keys**: {``course_id``, ``section_no``}\ :sup:`+` = all attributes. Minimal? {``course_id``}\ :sup:`+` = {``course_id``, ``title``} :math:`\neq R`. {``section_no``}\ :sup:`+` = {``section_no``} :math:`\neq R`. So {``course_id``, ``section_no``} is the only candidate key.

   **Step 2 -- Classify attributes**: Prime: ``course_id``, ``section_no``. Non-prime: ``title``, ``professor_person_id``, ``capacity``.

   **Step 3 -- Test FDs**: :math:`FD_1`: ``course_id`` :math:`\to` ``title``. ``course_id`` is a proper subset of the CK. ``title`` is non-prime. **Partial dependency -- violates 2NF.** :math:`FD_2`: {``course_id``, ``section_no``} :math:`\to` {``professor_person_id``, ``capacity``}. Left side is the full CK. **Full dependency -- passes 2NF.**

   **Fix**: Split into ``Course``\(**course_id**, title) and ``Course_Section``\(**course_id**, **section_no**, professor_person_id, capacity).

   .. rubric:: Violation Example (Summary)


   ``Section_Detail``\(**course_id**, **section_no**, title, professor_person_id, capacity)

   FDs: ``course_id`` :math:`\to` ``title`` (partial dependency on part of the PK); {``course_id``, ``section_no``} :math:`\to` {``professor_person_id``, ``capacity``} (full dependency on the entire PK).

   **Fix**: Split into ``Course``\(**course_id**, title) and ``Course_Section``\(**course_id**, **section_no**, professor_person_id, capacity).


.. dropdown:: Third Normal Form (3NF)
   :class-container: sd-border-secondary

   .. rubric:: Definition


   A relation is in **3NF** if it is in 2NF, and no non-prime attribute is transitively dependent on any candidate key.

   A **transitive dependency** occurs when :math:`A \to B` and :math:`B \to C` (where :math:`B` is not a superkey and :math:`B \not\to A`), creating an indirect path :math:`A \to C`.

   **Formal test**: For every non-trivial FD :math:`X \to Y`, at least one must hold: :math:`X` is a superkey, or every attribute in :math:`Y` is prime (belongs to some candidate key).

   .. card::
       :class-card: sd-border-info

       **Intuition**: 3NF says non-key attributes must depend *directly* on the key, not through another non-key attribute. If ``course_id`` :math:`\to` ``dept_id`` :math:`\to` ``dept_name``, then ``dept_name`` reaches the key only via the middleman ``dept_id``. That middleman creates redundancy.

   .. rubric:: Step-by-Step 3NF Testing


   Given ``Course``\(**course_id**, title, dept_id, dept_name) with FDs:

   - :math:`FD_{1a}`: ``course_id`` :math:`\to` ``title``
   - :math:`FD_{1b}`: ``course_id`` :math:`\to` ``dept_id``
   - :math:`FD_2`: ``dept_id`` :math:`\to` ``dept_name``

   **Step 1 -- Find candidate keys**: {``course_id``}\ :sup:`+` = all attributes (via the chain ``course_id`` :math:`\to` ``dept_id`` :math:`\to` ``dept_name``). The only CK is {``course_id``}.

   **Step 2 -- Classify attributes**: Prime: ``course_id``. Non-prime: ``title``, ``dept_id``, ``dept_name``.

   **Step 3 -- Test FDs**: :math:`FD_{1a}` and :math:`FD_{1b}`: left side is ``course_id``, which is a superkey. **Pass.** :math:`FD_2`: ``dept_id`` :math:`\to` ``dept_name``. ``dept_id``\ :sup:`+` = {``dept_id``, ``dept_name``} :math:`\neq R` -- not a superkey. ``dept_name`` is non-prime. **Violates 3NF.**

   **Fix**: Split into ``Course``\(**course_id**, title, dept_id) and ``Department``\(**dept_id**, dept_name).


.. dropdown:: Boyce-Codd Normal Form (BCNF)
   :class-container: sd-border-secondary

   .. rubric:: Definition


   A relation :math:`R` is in **BCNF** if for every non-trivial FD :math:`X \to Y`, :math:`X` is a superkey. In other words: *every determinant must be a superkey*. No exceptions.

   .. rubric:: How Does BCNF Differ from 3NF?


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

   .. rubric:: A Genuine 3NF-but-not-BCNF Example


   **Relation**: ``Advisor``\(student_id, dept_id, advisor_id)

   **FDs**: :math:`FD_1`: {student_id, dept_id} :math:`\to` advisor_id; :math:`FD_2`: advisor_id :math:`\to` dept_id.

   **Step 1 -- Candidate keys**: {student_id, dept_id}\ :sup:`+` = R, so CK\ :math:`_1`. {student_id, advisor_id}\ :sup:`+` = R, so CK\ :math:`_2`.

   **Step 2 -- Classify attributes**: All three attributes are prime (each appears in at least one CK). No non-prime attributes exist.

   **Step 3 -- Test FDs**: :math:`FD_1`: LHS = {student_id, dept_id} is a superkey. Passes both 3NF and BCNF. :math:`FD_2`: {advisor_id}\ :sup:`+` = {advisor_id, dept_id} :math:`\neq R`. Not a superkey. 3NF: is dept_id prime? Yes -- escape clause fires, passes 3NF. BCNF: no escape clause -- fails BCNF.

   .. card::
       :class-card: sd-border-info

       **This is the real difference**: 3NF allows :math:`advisor\_id \to dept\_id` because dept_id is prime. BCNF does not care whether the RHS is prime. It only asks: is the determinant a superkey? Since advisor_id is not, BCNF is violated.

   .. warning::

      **Remaining anomaly**: If the CS department is renamed, both rows for advisor 101 must be updated. Miss one, and the data is inconsistent. 3NF does not prevent this; BCNF would.

   .. rubric:: When 3NF and BCNF Conflict


   Given the ``Advisor`` relation above, two options exist:

   **Option 1 -- Decompose to BCNF**: Split on :math:`advisor\_id \to dept\_id`. Creates ``Advisor_Dept``\(**advisor_id**, dept_id) and ``Student_Advisor``\(**student_id**, **advisor_id**). Lossless join is guaranteed. All FD-based anomalies are eliminated. However, :math:`FD_1`: {student_id, dept_id} :math:`\to` advisor_id is lost -- it can no longer be enforced within a single table.

   **Option 2 -- Stay at 3NF**: Accept that ``Advisor`` is already in 3NF. All FDs are preserved and checkable without joins. The update anomaly remains.

   .. card::
       :class-card: sd-border-info

       **Decision criterion**: Does :math:`FD_1` need to be enforced on every INSERT? If yes, stay at 3NF. If no, decompose to BCNF for cleaner anomaly elimination. When in doubt, normalize first: start with BCNF and fall back to 3NF only when a lost dependency has a proven operational cost.


.. dropdown:: Normal Form Summary
   :class-container: sd-border-secondary

   .. rubric:: Quick Reference


   .. list-table::
      :widths: 12 40 28 20
      :header-rows: 1
      :class: compact-table

      * - NF
        - Requirement
        - Eliminates
        - Guarantees
      * - **1NF**
        - Atomic values only
        - Multi-valued attributes, nested tables
        - Flat structure
      * - **2NF**
        - 1NF + no partial dependencies
        - Redundancy from attributes depending on part of a composite key
        - Full key dependence
      * - **3NF**
        - 2NF + no transitive dependencies (or RHS all prime)
        - Non-key to non-key chains
        - Dependency preservation
      * - **BCNF**
        - Every determinant is a superkey
        - All anomalies caused by functional dependencies
        - Lossless join

   **Choose BCNF when**: transactional system with frequent writes; data integrity is the priority; lost dependencies can be enforced via application logic or triggers.

   **Fall back to 3NF when**: BCNF decomposition loses a critical dependency; that dependency must be enforced efficiently (single-table constraint, no joins); the remaining redundancy is acceptable.

   .. card::
       :class-card: sd-border-info

       **Practical guideline**: Aim for BCNF in OLTP systems. Fall back to 3NF only when BCNF decomposition loses a dependency that must be enforced efficiently (without joins).


.. dropdown:: Worked Example: Step-by-Step NF Testing
   :class-container: sd-border-secondary

   .. rubric:: End-to-End Normal Form Verification


   **Given**: :math:`R(A, B, C, D)` with :math:`F = \{A \to B, \; BC \to D\}`

   **Step 1 -- Find candidate keys**: A and C never appear on any RHS, so both must be in every CK. :math:`\{A, C\}^{+}`: apply :math:`A \to B`, gives {A, B, C}; apply :math:`BC \to D`, gives {A, B, C, D} = R. Superkey. Both proper subsets fail to reach R, so {A, C} is the only CK.

   **Step 2 -- Classify attributes**: Prime: A, C. Non-prime: B, D.

   **Step 3 -- Test each FD**:

   - :math:`A \to B`: {A}\ :sup:`+` = {A, B} :math:`\neq R`, not a superkey. B is non-prime. A is a proper subset of CK {A, C} -- this is a **partial dependency**. **Violates 2NF.**
   - :math:`BC \to D`: {B, C}\ :sup:`+` = {B, C, D} :math:`\neq R`, not a superkey. D is non-prime. {B, C} is not a subset of any CK (contains non-prime B). Not a partial dependency, but the determinant is not a superkey and the RHS is non-prime. **Violates 3NF.**

   **Conclusion**: :math:`R` is in **1NF only**. :math:`A \to B` prevents 2NF (partial dependency), and :math:`BC \to D` prevents 3NF (non-superkey determinant, non-prime RHS).


.. dropdown:: Exercise: Test Normal Forms
   :class-container: sd-border-secondary

   .. rubric:: Exercise (10 min)


   **Given**: :math:`R(A, B, C, D, E)` with :math:`F = \{AB \to C, \; C \to D, \; D \to B\}`

   **Tasks**:

   1. Find all candidate keys (hint: which attributes never appear on any RHS?)
   2. Classify every attribute as prime or non-prime
   3. Test every FD against 2NF, 3NF, and BCNF
   4. State the highest normal form :math:`R` satisfies
   5. Propose a decomposition that fixes the violations

   .. card::
       :class-card: sd-border-info

       **Hint**: Start by noting that A and E never appear on the right side of any FD. What does that tell you about every candidate key?



Decomposition Algorithms
====================================================


.. dropdown:: Desirable Properties
   :class-container: sd-border-secondary
   :open:

   .. rubric:: Two Critical Properties


   1. **Lossless Join (Non-additive Join)**: Joining the decomposed relations reconstructs the original relation *exactly*. No spurious (phantom) tuples are introduced. **Always required**: Without this, decomposition corrupts data.

   2. **Dependency Preservation**: Every FD in the original set can be checked on at least one decomposed relation (without joining tables). Allows efficient constraint enforcement. **Desirable but not always achievable**: 3NF synthesis guarantees it; BCNF decomposition may sacrifice it.

   .. card::
       :class-card: sd-border-info

       **Trade-off**: 3NF decomposition preserves both properties. BCNF decomposition guarantees lossless join but may lose dependency preservation. Choose based on system requirements.

   .. rubric:: Lossless Join Test


   A decomposition of :math:`R` into :math:`R_1` and :math:`R_2` is lossless if and only if :math:`R_1 \cap R_2 \to R_1` or :math:`R_1 \cap R_2 \to R_2`. The common attributes must be a superkey of at least one side.


.. dropdown:: Lossless Join in Detail
   :class-container: sd-border-secondary

   .. rubric:: What Can Go Wrong Without Lossless Join?


   When we decompose :math:`R` into :math:`R_1` and :math:`R_2` and later join them back, we expect to recover the original tuples exactly. If the common attributes (the join key) are not a superkey of at least one side, the join can produce **spurious tuples** -- rows that look valid but never existed in the original relation.

   .. rubric:: Spurious Tuples: A Concrete Example


   Suppose we decompose ``Course_Section``\(**course_id**, **section_no**, title, dept_id, professor_person_id) incorrectly into :math:`R_1`\(course_id, section_no, professor_person_id) and :math:`R_2`\(section_no, title, dept_id).

   The join key is only ``section_no``. Multiple courses can have the same ``section_no`` (e.g., both ENPM818T and ENPM702 have a section 1). When we join on ``section_no`` alone, the result pairs every ENPM818T professor with every row sharing the same ``section_no``, including rows from ENPM702. These phantom rows never existed in the original data.

   .. card::
       :class-card: sd-border-info

       **Why the test works**: The lossless join condition :math:`R_1 \cap R_2 \to R_1` (or :math:`R_2`) requires the shared attributes to be a superkey of one side. A superkey uniquely identifies rows in that relation, so the join cannot create ambiguous matches.


.. dropdown:: Dependency Preservation in Detail
   :class-container: sd-border-secondary

   .. rubric:: What Is Dependency Preservation?


   A decomposition **preserves dependencies** if every FD in the canonical cover :math:`F_c` can be checked within a single decomposed relation -- without performing any joins. This matters because checking a constraint across multiple tables requires a join on every INSERT or UPDATE, which is expensive.

   .. rubric:: What Can Go Wrong Without Dependency Preservation?


   Suppose we decompose ``Course``\(**course_id**, title, dept_id, dept_name) to remove the 3NF violation. If the resulting relations split the FD ``dept_id`` :math:`\to` ``dept_name`` across two tables so that no single table contains both ``dept_id`` and ``dept_name``, then enforcing that FD requires a join query on every write. In high-volume systems this becomes a serious performance problem.

   .. rubric:: Harmless vs. Genuine Loss


   Not all "lost" FDs matter equally. Trivial FDs or FDs that are implied by primary key constraints are lost without consequence. A genuine loss occurs when an FD that encodes a real business rule -- one that must be checked at write time -- ends up split across tables. This is the case where staying at 3NF (which always preserves all FDs) is preferable.


.. dropdown:: 3NF Synthesis Algorithm
   :class-container: sd-border-secondary

   .. rubric:: Algorithm to Decompose into 3NF


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

   .. rubric:: Worked Example: :math:`R(A, B, C, D)` with :math:`F = \{AB \to C, \; C \to D, \; D \to B\}`


   **Step 1 -- Canonical cover**: Check each condition. All RHS are single attributes. Only :math:`AB \to C` has a composite left side: :math:`\{A\}^{+} = \{A\}` and :math:`\{B\}^{+} = \{B\}`, so neither A nor B is extraneous. No FD is redundant (each closure test fails to reach the right side without its FD). Therefore :math:`F_c = \{AB \to C, \; C \to D, \; D \to B\}` (unchanged).

   **Step 2 -- Create relations**: Each FD produces one relation (no two FDs share a left side). :math:`R_1`\(A, B, C) with key {A, B}; :math:`R_2`\(C, D) with key {C}; :math:`R_3`\(D, B) with key {D}.

   **Step 3 -- Candidate key check**: The candidate keys of :math:`R` are {A, C} and {A, D}. :math:`R_1 = \{A, B, C\} \supseteq \{A, C\}`. A candidate key is already present. No extra relation needed.

   **Step 4 -- Remove subset relations**: No :math:`R_i` is a subset of another.

   **Final result**: :math:`R_1`\(A, B, C), :math:`R_2`\(C, D), :math:`R_3`\(D, B).

   .. card::
       :class-card: sd-border-info

       **Verification**: Every FD in :math:`F_c` has all its attributes in exactly one :math:`R_i` (dependencies preserved). :math:`R_1` contains the candidate key {A, C} (lossless join guaranteed).


.. dropdown:: BCNF Decomposition Algorithm
   :class-container: sd-border-secondary

   .. rubric:: Algorithm to Decompose into BCNF


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

   .. rubric:: Worked Example: :math:`R(A, B, C)` with :math:`F = \{AB \to C, \; C \to B\}`


   **Candidate keys**: A never appears on any RHS, so every CK must contain A. :math:`\{A, B\}^{+} = R` (CK\ :math:`_1`). :math:`\{A, C\}^{+} = R` (CK\ :math:`_2`).

   **Test FDs**: :math:`AB \to C`: {A, B}\ :sup:`+` = R -- superkey. Passes BCNF. :math:`C \to B`: {C}\ :sup:`+` = {C, B} :math:`\neq R` -- not a superkey. **Violates BCNF.**

   **Apply decomposition formula** on :math:`C \to B` (where :math:`X = \{C\}`, :math:`Y = \{B\}`):

   - :math:`R_1 = X \cup Y = \{C, B\}`
   - :math:`R_2 = R - (Y - X) = \{A, B, C\} - \{B\} = \{A, C\}`

   **Verify BCNF**: :math:`R_1`\(C, B): only FD is :math:`C \to B`, and {C}\ :sup:`+` within :math:`R_1` = :math:`R_1`. C is a superkey. In BCNF. :math:`R_2`\(A, C): no non-trivial FDs project onto :math:`R_2` (the FD :math:`AB \to C` requires B, which is not in :math:`R_2`). In BCNF.

   **Verify lossless join**: :math:`R_1 \cap R_2 = \{C\}`. Is C a superkey of :math:`R_1`? Yes. Lossless join confirmed.

   .. warning::

      **Lost dependency**: :math:`AB \to C` cannot be checked within :math:`R_1` or :math:`R_2` alone (no single relation contains A, B, and C together). Enforcing this constraint now requires joining :math:`R_1` and :math:`R_2`, or using application-level logic.


.. dropdown:: BCNF vs. 3NF Trade-offs
   :class-container: sd-border-secondary

   .. rubric:: When to Use Each


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


.. dropdown:: Exercise: End-to-End Normalization
   :class-container: sd-border-secondary

   .. rubric:: Exercise (20 min)


   **Given**: ``Purchase_Order``\(**order_id**, customer_name, customer_city, product_id, product_name, quantity, unit_price, total_price)

   **FDs**:

   - ``order_id`` :math:`\to` {``customer_name``, ``customer_city``}
   - ``product_id`` :math:`\to` {``product_name``, ``unit_price``}
   - {``order_id``, ``product_id``} :math:`\to` {``quantity``, ``total_price``}

   **Tasks**:

   1. Identify the candidate key (use attribute closure)
   2. Test for 2NF, 3NF, and BCNF violations
   3. Decompose step by step to BCNF
   4. Verify the lossless join property at each step
   5. Are all original FDs preserved? If not, which one is lost?



When to Denormalize
====================================================


.. dropdown:: Motivation
   :class-container: sd-border-secondary
   :open:

   .. rubric:: Why Denormalize?


   **Normalization optimizes for write consistency**. Denormalization optimizes for **read performance**.

   1. **Read-heavy workloads**: Reporting dashboards, analytics, data warehouses. Normalized schemas require many joins for complex queries. Denormalization reduces join count, improving query speed.

   2. **Predictable query patterns**: Known, repetitive queries. If 90% of queries need the same joined data, store it pre-joined.

   3. **Performance bottlenecks**: Profiling shows slow joins. Measure first: denormalize only proven pain points.

   .. warning::

      **Golden rule**: Normalize first, denormalize later. Always start with a normalized schema. Add denormalization only when performance testing justifies it.


.. dropdown:: Costs of Denormalization
   :class-container: sd-border-secondary

   .. rubric:: The Price You Pay


   1. **Redundancy returns**: Data is duplicated across tables. Increased storage and risk of stale data.

   2. **Update complexity**: Changes must propagate to multiple locations. Application code or triggers must maintain consistency.

   3. **Anomalies return**: The insertion, deletion, and update anomalies come back, mitigated by triggers, application logic, or periodic reconciliation.

   4. **Schema rigidity**: Denormalized schemas are harder to evolve. Adding a new attribute may require updating multiple tables and their synchronization logic.


.. dropdown:: Concrete Example: The Cost of Redundancy
   :class-container: sd-border-secondary

   .. rubric:: Normalized vs. Denormalized


   **Normalized schema** -- three separate tables (Customers, Products, Orders). Each fact is stored exactly once. Renaming "Widget" to "SuperWidget" requires updating a single row in the Products table.

   **Denormalized schema** -- the Orders table includes copies of ``cust_name`` and ``prod_name`` directly. This eliminates joins for read queries, but the product name "Widget" now appears in every order row that references product P1.

   **The rename scenario**: when "Widget" is renamed to "SuperWidget", every order row where ``prod_name = 'Widget'`` must be updated. In a production system with millions of orders, this is an expensive UPDATE statement that locks many rows. If the update partially fails (timeout or crash), some rows say "Widget" and others say "SuperWidget" -- the exact update anomaly from the beginning of this lecture, reintroduced by denormalization.

   .. warning::

      **Design question**: Should historical orders reflect the *current* product name or the name *at the time of purchase*? Denormalization often forces this question to be resolved explicitly in application code.


.. dropdown:: Denormalization Patterns
   :class-container: sd-border-secondary

   .. rubric:: Common Techniques


   1. **Materialized Views**: Precompute and store query results as a physical table. Database refreshes the view periodically or on demand. Example: Store enrollment counts per course per semester.

   2. **Redundant Columns**: Copy a column from a related table into a frequently queried table. Example: Add ``dept_name`` to ``Course`` (even though it lives in ``Department``). Use triggers to keep copies synchronized.

   3. **Summary Tables**: Precompute aggregates (SUM, COUNT, AVG) into a dedicated table. Example: ``Semester_GPA_Summary`` with average GPA per student per semester.

   4. **Stored Derived Attributes**: Physically store a value that can be computed from other columns. Example: ``total_credits`` in ``Student`` derived from summing completed course credits.


.. dropdown:: Materialized View Example
   :class-container: sd-border-secondary

   .. rubric:: Precomputing Expensive Joins


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

   .. rubric:: Avoiding Repetitive Joins


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

   .. rubric:: Different Needs, Different Schemas


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

   .. rubric:: Best Practices


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


Quick Reference
---------------

.. seealso::

   :doc:`cheat_sheet` -- a condensed, box-by-box reference covering all 15 topics from
   this lecture: anomalies, functional dependencies, Armstrong's axioms, attribute closure,
   candidate keys, canonical cover, normal forms (1NF through BCNF), decomposition
   algorithms, lossless join, dependency preservation, and the full normalization pipeline
   flowchart.