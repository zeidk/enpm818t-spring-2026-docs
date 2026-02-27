====================================================
Quiz
====================================================

This quiz covers the key concepts from Lecture 2: Entity-Relationship Modeling,
including entities, attributes, keys, relationships, cardinality, participation
constraints, Chen notation, and advanced ER concepts.

.. note::

   **Instructions:**

   - Answer all questions to the best of your ability.
   - Multiple choice questions have exactly one correct answer.
   - True/False questions require you to determine if the statement is correct.
   - Essay questions require short written responses (2–4 sentences).
   - Click the dropdown after each question to reveal the answer.


----


Multiple Choice
===============

.. admonition:: Question 1
   :class: hint

   What is the primary purpose of conceptual modeling in database design?

   A. To specify storage indexes and partitioning strategies.

   B. To capture what data exists and how it relates, independent of technology.

   C. To write SQL queries for data retrieval.

   D. To optimize database performance and query execution time.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- To capture what data exists and how it relates, independent of technology.

   *Explanation:* Conceptual modeling focuses on understanding the domain and business rules without being constrained by implementation details. Technology decisions come later at the logical and physical levels.


.. admonition:: Question 2
   :class: hint

   In Chen notation, which symbol represents an entity?

   A. Diamond

   B. Oval

   C. Rectangle

   D. Circle

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Rectangle

   *Explanation:* In Chen notation, rectangles represent entities, ovals represent attributes, and diamonds represent relationships.


.. admonition:: Question 3
   :class: hint

   What distinguishes a **weak entity** from a **strong entity**?

   A. Weak entities have fewer attributes than strong entities.

   B. Weak entities cannot have relationships with other entities.

   C. Weak entities do not have a primary key of their own and depend on an owner entity for identification.

   D. Weak entities can only participate in 1:1 relationships.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- Weak entities do not have a primary key of their own and depend on an owner entity for identification.

   *Explanation:* A weak entity's full identity is formed by combining its partial key with the owner entity's key. For example, ``COURSE_SECTION`` uses ``(course_id, section_no)``.


.. admonition:: Question 4
   :class: hint

   Which of the following is an example of a **composite attribute**?

   A. ``student_id`` (a unique identifier)

   B. ``age`` (derived from date of birth)

   C. ``phone_numbers`` (a student can have multiple phones)

   D. ``address`` (subdivided into street, city, state, zip)

.. dropdown:: Answer
   :class-container: sd-border-success

   **D** -- ``address`` (subdivided into street, city, state, zip)

   *Explanation:* A composite attribute can be broken down into smaller sub-attributes. It can be referenced as a whole or by individual parts.


.. admonition:: Question 5
   :class: hint

   In Chen notation, how is a **derived attribute** visually distinguished?

   A. Double oval

   B. Dashed oval

   C. Underlined oval

   D. Shaded rectangle

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Dashed oval

   *Explanation:* Derived attributes (like ``age`` from ``date_of_birth``) are shown with dashed ovals to indicate they are computed rather than stored.


.. admonition:: Question 6
   :class: hint

   What is the difference between a **superkey** and a **candidate key**?

   A. A superkey uniquely identifies entities; a candidate key does not.

   B. A candidate key is a minimal superkey with no unnecessary attributes.

   C. A superkey can have NULL values; a candidate key cannot.

   D. There is no difference; the terms are interchangeable.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A candidate key is a minimal superkey with no unnecessary attributes.

   *Explanation:* A superkey uniquely identifies entities but may include extra attributes. A candidate key is a superkey with nothing extra—removing any attribute would break uniqueness.


.. admonition:: Question 7
   :class: hint

   Why is ``COURSE_SECTION`` modeled as a weak entity dependent on ``COURSE``?

   A. Because course sections have fewer attributes than courses.

   B. Because section numbers like "001" are not unique across all courses.

   C. Because course sections cannot participate in relationships.

   D. Because all weak entities must be related to courses.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Because section numbers like "001" are not unique across all courses.

   *Explanation:* Section "001" exists for many different courses. The section number only identifies a section *within the context of a specific course*, requiring the course_id to form a complete unique identifier.


.. admonition:: Question 8
   :class: hint

   In a **1:N (one-to-many)** relationship between ``DEPARTMENT`` and ``PROFESSOR``, which statement is correct?

   A. Each department has exactly one professor, and each professor belongs to many departments.

   B. Each department has many professors, and each professor belongs to exactly one department.

   C. Each department has many professors, and each professor belongs to many departments.

   D. Each department has at most one professor, and each professor belongs to at most one department.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Each department has many professors, and each professor belongs to exactly one department.

   *Explanation:* In a 1:N relationship, the "one" side (department) can have multiple related instances on the "many" side (professors), but each professor belongs to only one department.


.. admonition:: Question 9
   :class: hint

   What does **total participation** in a relationship mean?

   A. Every instance of the entity may participate in the relationship.

   B. Every instance of the entity must participate in the relationship.

   C. The entity participates in all relationships in the database.

   D. The relationship has attributes attached to it.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Every instance of the entity must participate in the relationship.

   *Explanation:* Total participation means the relationship is mandatory—every entity instance must be involved. Partial participation means it is optional.


.. admonition:: Question 10
   :class: hint

   In Chen notation, what do **double lines** connecting an entity to a relationship indicate?

   A. A multivalued relationship

   B. Total (mandatory) participation

   C. Partial (optional) participation

   D. An identifying relationship with partial key

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Total (mandatory) participation

   *Explanation:* Double lines indicate that every instance of the entity must participate in the relationship. Single lines indicate partial (optional) participation.


.. admonition:: Question 11
   :class: hint

   In **(min, max) notation**, what does **(0, N)** on ``PROFESSOR`` in the ``TEACHES`` relationship mean?

   A. A professor must teach at least one course but can teach many.

   B. A professor may teach zero courses or many courses (optional participation).

   C. A professor teaches exactly N courses.

   D. A professor cannot participate in the relationship.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- A professor may teach zero courses or many courses (optional participation).

   *Explanation:* The min of 0 means participation is optional (the professor might not teach). The max of N means they can teach multiple courses.


.. admonition:: Question 12
   :class: hint

   When should an attribute with a constrained domain (e.g., ``rank`` = {Assistant, Associate, Full}) be **promoted to a lookup entity**?

   A. When the value set is small and stable with no additional attributes.

   B. When the values have their own attributes or change over time.

   C. When only one entity references the values.

   D. Never; constrained attributes should always remain attributes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- When the values have their own attributes or change over time.

   *Explanation:* If rank needs attributes like ``description``, ``min_years_experience``, or ``effective_date``, or if the rank set changes over time, promote it to an entity. Simple stable value sets can remain attributes.


.. admonition:: Question 13
   :class: hint

   What type of relationship exists when a ``STUDENT`` enrolls in many ``COURSE_SECTION`` entities, and each section has many students?

   A. 1:1 (one-to-one)

   B. 1:N (one-to-many)

   C. M:N (many-to-many)

   D. Recursive (unary)

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- M:N (many-to-many)

   *Explanation:* Each student enrolls in many sections, and each section has many students. Both sides have "many" cardinality.


.. admonition:: Question 14
   :class: hint

   Where should the attribute ``grade`` be placed in the relationship between ``STUDENT`` and ``COURSE_SECTION``?

   A. As an attribute of ``STUDENT``

   B. As an attribute of ``COURSE_SECTION``

   C. As an attribute of the ``ENROLLS_IN`` relationship itself

   D. Grades should not be modeled in an ER diagram

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- As an attribute of the ``ENROLLS_IN`` relationship itself

   *Explanation:* Grade belongs to the specific pairing of a student and section, not to either entity alone. Alice has different grades in different courses, and a course has different grades for different students.


.. admonition:: Question 15
   :class: hint

   In a **specialization/generalization hierarchy**, what does the **ISA relationship** represent?

   A. A foreign key constraint between two tables

   B. An "is a" relationship where a subclass inherits attributes from a superclass

   C. An aggregation of multiple entities

   D. A ternary relationship involving three entities

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- An "is a" relationship where a subclass inherits attributes from a superclass

   *Explanation:* ISA (or "is a") represents specialization/generalization. A ``GRAD_STUDENT`` is a ``STUDENT``—they inherit all student attributes plus have their own specific attributes.


.. admonition:: Question 16
   :class: hint

   What distinguishes **disjoint specialization** from **overlapping specialization**?

   A. Disjoint means an entity can belong to multiple subclasses; overlapping means at most one.

   B. Disjoint means an entity belongs to at most one subclass; overlapping allows multiple.

   C. Disjoint applies only to weak entities; overlapping applies to strong entities.

   D. There is no difference; both terms mean the same thing.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Disjoint means an entity belongs to at most one subclass; overlapping allows multiple.

   *Explanation:* Disjoint: a person is either a student or a professor, not both. Overlapping: a person could be both a student and a professor simultaneously.


.. admonition:: Question 17
   :class: hint

   What does a **double diamond** symbol in Chen notation represent?

   A. A multivalued attribute

   B. An identifying relationship connecting a weak entity to its owner

   C. Total participation on both sides of a relationship

   D. A ternary relationship involving three entities

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- An identifying relationship connecting a weak entity to its owner

   *Explanation:* The double diamond, combined with double lines and a double rectangle, marks an identifying relationship that provides identity to a weak entity.


.. admonition:: Question 18
   :class: hint

   In a **ternary relationship** ``TA_ASSIGNMENT`` involving ``GRAD_STUDENT``, ``PROFESSOR``, and ``COURSE_SECTION``, which statement is correct?

   A. The relationship can always be decomposed into three binary relationships without loss of information.

   B. The relationship requires all three entities simultaneously to have meaning.

   C. Ternary relationships are more common than binary relationships.

   D. Ternary relationships cannot have attributes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- The relationship requires all three entities simultaneously to have meaning.

   *Explanation:* A ternary relationship cannot be decomposed into binary relationships without losing information. The TA assignment depends on all three: the grad student, the professor supervising them, and the course section.


.. admonition:: Question 19
   :class: hint

   Why are **M:N (many-to-many)** relationships resolved into **junction tables** at the logical level?

   A. Because relational databases cannot enforce M:N constraints.

   B. Because M:N relationships cannot be implemented directly with foreign keys.

   C. Because M:N relationships always have attributes.

   D. Because Chen notation does not support M:N relationships.

.. dropdown:: Answer
   :class-container: sd-border-success

   **B** -- Because M:N relationships cannot be implemented directly with foreign keys.

   *Explanation:* Relational databases use foreign keys, which work for 1:N relationships but cannot represent M:N directly. A junction table (bridge table) with two foreign keys is required.


.. admonition:: Question 20
   :class: hint

   What is a **recursive (unary) relationship**?

   A. A relationship that repeats multiple times in the diagram.

   B. A relationship between two different entity types.

   C. A relationship where an entity is related to itself.

   D. A relationship with no cardinality constraints.

.. dropdown:: Answer
   :class-container: sd-border-success

   **C** -- A relationship where an entity is related to itself.

   *Explanation:* Recursive relationships connect an entity to itself. Example: ``COURSE`` has ``HAS_PREREQ`` relationship with ``COURSE`` (a course can be a prerequisite for another course). Role labels are required to distinguish the two participations.


True or False
=============

.. admonition:: Question 21
   :class: hint

   **True or False:** Conceptual models are technology-independent and focus on what data exists rather than how it is stored.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Conceptual models capture business rules and data relationships without tying to a specific DBMS or storage technology. Implementation details come at the logical and physical levels.


.. admonition:: Question 22
   :class: hint

   **True or False:** In Chen notation, a double rectangle represents a strong entity with its own primary key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* A **double rectangle** represents a weak entity, not a strong entity. Strong entities are drawn with single rectangles.


.. admonition:: Question 23
   :class: hint

   **True or False:** A multivalued attribute, such as ``phone_numbers``, is drawn as a double oval in Chen notation.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Multivalued attributes (like multiple phone numbers) are visually distinguished by double ovals in Chen notation.


.. admonition:: Question 24
   :class: hint

   **True or False:** Every candidate key is a superkey, but not every superkey is a candidate key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Every candidate key is by definition a superkey (it uniquely identifies entities), but superkeys may contain extra attributes that aren't needed for uniqueness, making them non-minimal.


.. admonition:: Question 25
   :class: hint

   **True or False:** The full identity of a weak entity is formed by combining the owner entity's key with the weak entity's partial key.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Weak entities borrow part of their identity from the owner entity. For example, ``COURSE_SECTION`` has key ``(course_id, section_no)`` where ``course_id`` comes from the owner ``COURSE``.


.. admonition:: Question 26
   :class: hint

   **True or False:** In Chen's cardinality ratios (1:1, 1:N, M:N), the label next to an entity tells you the maximum number of instances of **that entity** per instance of the opposite entity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* In Chen's convention, the label next to entity A tells you how many A's per instance of B. This is opposite to (min, max) notation, which is read locally.


.. admonition:: Question 27
   :class: hint

   **True or False:** Total participation is visually represented in Chen notation with a single line connecting the entity to the relationship.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Total participation is represented by **double lines**, not single lines. Single lines indicate partial (optional) participation.


.. admonition:: Question 28
   :class: hint

   **True or False:** In (min, max) notation, **(1, 1)** means mandatory participation with exactly one related instance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* (1, 1) means minimum 1 (mandatory) and maximum 1 (exactly one). For example, a professor belongs to exactly one department.


.. admonition:: Question 29
   :class: hint

   **True or False:** 1:1 relationships are the most common type of relationship in relational database design.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* 1:N (one-to-many) relationships are the most common in relational databases. 1:1 relationships are relatively rare and often indicate that entities could be merged.


.. admonition:: Question 30
   :class: hint

   **True or False:** Relationship attributes are most commonly found on M:N relationships rather than 1:N or 1:1 relationships.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Relationship attributes make sense when the attribute describes the association itself. On M:N relationships, this is very common (e.g., ``grade`` on ``ENROLLS_IN``). On 1:N, the attribute can often be moved to the "many" side.


.. admonition:: Question 31
   :class: hint

   **True or False:** A derived attribute, such as ``age`` calculated from ``date_of_birth``, should be stored in the database to improve query performance.

.. dropdown:: Answer
   :class-container: sd-border-success

   **False**

   *Explanation:* Derived attributes should not be stored because they can always be recomputed and would become stale. Storing ``age`` means it becomes incorrect after each birthday.


.. admonition:: Question 32
   :class: hint

   **True or False:** Crow's Foot notation is closer to the logical model than Chen notation because attributes appear as columns inside entity boxes.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Crow's Foot notation shows attributes as columns inside entity boxes, making it closer to how tables will look. Chen keeps attributes separate, maintaining clearer conceptual-level abstraction.


.. admonition:: Question 33
   :class: hint

   **True or False:** An identifying relationship always has a cardinality of 1:N from the owner entity to the weak entity.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* An identifying relationship is always 1:N from the owner to the weak entity. One course has many sections; each section belongs to exactly one course.


.. admonition:: Question 34
   :class: hint

   **True or False:** In a disjoint and total specialization, every superclass entity must belong to exactly one subclass.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* "Disjoint" means at most one subclass, and "total" means at least one subclass. Together, they mean exactly one subclass. Every person must be either a student or a professor, but not both.


.. admonition:: Question 35
   :class: hint

   **True or False:** Aggregation in the Enhanced ER (EER) model allows a relationship to be treated as an entity that can participate in other relationships.

.. dropdown:: Answer
   :class-container: sd-border-success

   **True**

   *Explanation:* Aggregation allows treating a relationship (and its participating entities) as a higher-level entity that can then participate in other relationships. This is part of the Enhanced ER (EER) model.


Essay Questions
===============

.. admonition:: Question 36
   :class: hint

   **Explain the difference between entity type, entity set, and entity instance.** How do these concepts relate to the object-oriented programming concepts of class, object, and collection?

   *(2–4 sentences)*

.. dropdown:: Answer
   :class-container: sd-border-success

   *Key points to include:*

   - An **entity type** defines the schema or structure (e.g., ``STUDENT`` with attributes student_id, name, gpa).
   - An **entity set** is the collection of all current instances of that type at a point in time.
   - An **entity instance** is a single occurrence (e.g., Alice, student_id=S101, gpa=3.8).
   - OOP analogy: entity type ≈ class (blueprint), entity instance ≈ object (one student), entity set ≈ collection of all instantiated objects of that class.


.. admonition:: Question 37
   :class: hint

   **When should a constrained attribute be promoted to a lookup entity?** Provide an example where promoting ``rank`` from an attribute of ``PROFESSOR`` to a separate ``ACADEMIC_RANK`` entity would be beneficial.

   *(2–4 sentences)*

.. dropdown:: Answer
   :class-container: sd-border-success

   *Key points to include:*

   - Promote when the values have **their own attributes** beyond just the label.
   - Promote when the value set **changes over time** (adding new values, retiring old ones).
   - Promote when **multiple entities** reference the same set.
   - Example: ``ACADEMIC_RANK`` as an entity can store ``description``, ``min_years_experience``, and ``effective_date``. If you need to answer "when was Associate rank last updated?" or "what ranks require >10 years?", these questions target the rank itself, justifying entity status.


.. admonition:: Question 38
   :class: hint

   **Describe the key differences between cardinality ratios and participation constraints** in ER modeling. How does (min, max) notation resolve ambiguities that exist in standard Chen cardinality labels?

   *(3–4 sentences)*

.. dropdown:: Answer
   :class-container: sd-border-success

   *Key points to include:*

   - **Cardinality ratios** (1:1, 1:N, M:N) specify the **maximum** number of instances that can participate.
   - **Participation constraints** (total/partial) specify the **minimum**—whether participation is mandatory or optional.
   - Chen's cardinality labels like "1:N" are ambiguous about minimums: does the department *must have* at least one professor, or *may have* zero?
   - **(min, max) notation** resolves this by making both bounds explicit: (1, N) means "at least 1, up to N" while (0, N) means "optional, any number".

