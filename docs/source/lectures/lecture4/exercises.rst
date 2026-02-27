====================================================
Exercises
====================================================

This page contains exercises for Lecture 4. These exercises are designed to reinforce your understanding of functional dependencies, attribute closures, canonical covers, normal forms, and decomposition algorithms.


.. dropdown:: Exercise 1 -- Spot the Anomaly
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Build intuition for why normalization matters by identifying anomalies in a merged table.



    **Specification**

    Consider these two tables from the L3 schema:

    - ``Course``\ (\ **course_id**, title, credits, dept_id)
    - ``Department``\ (\ **dept_id**, dept_name, building, budget)

    **Imagine merging them** into a single flat table:

    ``Course_Dept``\ (\ **course_id**, title, credits, dept_id, dept_name, building, budget)

    **Tasks**:

    1. Which columns would be repeated across rows?
    2. Which of the three anomalies (insertion, deletion, update) would this merged table suffer from?
    3. Write a concrete example row that demonstrates each problem.



    **Deliverables**

    - Identification of repeated columns
    - One concrete example per anomaly type (3 total)


.. dropdown:: Exercise 2 -- Business Rules to FDs
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice translating business rules into formal functional dependencies and reasoning about FD validity.



    **Specification**

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

    **Business rules**:

    - Each loan is assigned a unique loan ID
    - Each loan records exactly one book and one borrower
    - Each ISBN corresponds to exactly one book title
    - Each borrower has a unique borrower ID and exactly one name
    - A borrower may borrow multiple books, and a book may be borrowed by multiple borrowers

    **Tasks**:

    1. Translate the business rules above into FDs.
    2. Someone claims ``borrower_id`` :math:`\to` ``isbn``. Is that consistent with the business rules? Can the data confirm or disprove it?
    3. What is the smallest set of columns you would need to know to uniquely identify a single row?



    **Deliverables**

    - Complete list of FDs derived from business rules
    - Analysis of the claimed FD with justification
    - Candidate key identification with reasoning


.. dropdown:: Exercise 3 -- Applying Armstrong's Axioms
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice applying the three axioms and their shortcuts (union, decomposition) to derive new FDs.



    **Specification**

    **Given FDs**: :math:`F = \{A \to B, \; B \to C, \; C \to D\}`

    **Tasks**:

    1. Using **transitivity**, derive :math:`A \to D`. Write out each step.
    2. Using **union**, combine your results to show :math:`A \to \{B, C, D\}`.
    3. **Challenge**: Does :math:`C \to A` hold? Can you prove it or disprove it from :math:`F` alone?

    .. tip::

       For the challenge question, think about what the axioms can and cannot derive. Soundness means we only derive true FDs, so if you cannot derive it, it does not follow from :math:`F`.



    **Deliverables**

    - Step-by-step derivation of :math:`A \to D`
    - Union derivation of :math:`A \to \{B, C, D\}`
    - Proof or disproof of :math:`C \to A` with explanation


.. dropdown:: Exercise 4 -- Compute a Closure
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice the attribute closure algorithm to test superkeys, candidate keys, and FD implication.



    **Specification**

    **Given**: :math:`R(A, B, C, D, E)` with :math:`F = \{A \to B, \; BC \to D, \; D \to E, \; E \to A\}`

    **Tasks**:

    1. Compute :math:`\{A, C\}^{+}` step by step (use a table like the lecture examples).
    2. Is {A, C} a superkey of :math:`R`?
    3. Is {A, C} a candidate key? (Test each proper subset.)
    4. Can you find a *different* candidate key? (Hint: look at what E determines.)

    .. note::

       After finishing, compare answers with a neighbor. If you found different candidate keys, verify both using closures.



    **Deliverables**

    - Step-by-step closure table for :math:`\{A, C\}^{+}`
    - Superkey and candidate key determination with justification
    - At least one additional candidate key with closure verification


.. dropdown:: Exercise 5 -- Compute a Canonical Cover
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Practice the three-step canonical cover algorithm: decompose, reduce left sides, remove redundant FDs.



    **Specification**

    **Given**: :math:`R(A, B, C, D)` with :math:`F = \{A \to BD, \; B \to C, \; C \to B, \; AB \to D\}`

    **Tasks**:

    1. **Step 1**: Decompose compound right sides. How many FDs do you have now?
    2. **Step 2**: Test for extraneous left-side attributes. In :math:`AB \to D`, is B extraneous? (Hint: compute :math:`\{A\}^{+}` under the current :math:`F`.)
    3. **Step 3**: Test for redundant FDs. Can any remaining FD be derived from the others?
    4. Write out the final :math:`F_c`.

    .. tip::

       Your canonical cover should have 4 FDs, each with a single attribute on both sides.



    **Deliverables**

    - Results after each step of the algorithm
    - Final canonical cover :math:`F_c`


.. dropdown:: Exercise 6 -- End-to-End Normalization
    :icon: gear
    :class-container: sd-border-primary
    :class-title: sd-font-weight-bold

    **Goal**

    Integrate all normalization concepts by performing a complete normalization from an unnormalized relation to BCNF.



    **Specification**

    **Given**: ``Purchase_Order``\ (\ **order_id**, customer_name, customer_city, product_id, product_name, quantity, unit_price, total_price)

    **FDs**:

    - ``order_id`` :math:`\to` {``customer_name``, ``customer_city``}
    - ``product_id`` :math:`\to` {``product_name``, ``unit_price``}
    - {``order_id``, ``product_id``} :math:`\to` {``quantity``, ``total_price``}

    **Tasks**:

    1. Identify the candidate key (use attribute closure).
    2. Test for 2NF, 3NF, and BCNF violations.
    3. Decompose step by step to BCNF.
    4. Verify the lossless join property at each step.
    5. Are all original FDs preserved? If not, which one is lost?



    **Deliverables**

    - Candidate key identification with closure computation
    - Normal form analysis (2NF, 3NF, BCNF) with specific violations identified
    - Step-by-step decomposition with resulting schemas
    - Lossless join verification at each decomposition step
    - Dependency preservation analysis

    .. important::

       This exercise integrates attribute closure, normal form testing, and decomposition algorithms. It is designed to prepare you for GP1, which will involve normalizing your project domain's relational schema to 3NF.
