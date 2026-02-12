====================================================
L2: Conceptual Data Modeling
====================================================

Overview
--------

This lecture introduces conceptual data modeling using Entity-Relationship
(ER) diagrams in Chen notation.  You will learn to identify entities,
attributes, and keys; classify attributes by type; model relationships with
cardinality and participation constraints; distinguish strong and weak
entities; and apply Extended ER (EER) concepts including
specialization/generalization, aggregation, and categories.  The session
includes a complete walkthrough of a university course management system
use case.


Learning Objectives
-------------------

By the end of this lecture, you will be able to:

- Explain the role of conceptual modeling in the database design lifecycle.
- Define entities, attributes, and keys in Chen notation.
- Classify attributes (simple, composite, multivalued, derived, constrained domain).
- Identify when to promote an attribute to a lookup entity.
- Specify cardinality ratios (1:1, 1:N, M:N) and participation constraints (total, partial, min-max).
- Model weak entities with identifying relationships and partial keys.
- Apply Extended ER concepts: specialization/generalization, aggregation, and categories.
- Evaluate design trade-offs and detect common modeling errors.


Contents
--------

.. toctree::
   :maxdepth: 2
   :titlesonly:

   lecture
   quiz
   exercises
   glossary
   references

Next Steps
----------

- In the next lecture, we will cover **Logical Data Modeling & Normalization**:

  - ER-to-Relational mapping algorithm (7-step process).
  - Relational algebra (σ, π, ⋈, ∪, −, ×).
  - Functional dependencies and normalization (1NF → BCNF).
  - Handling weak entities, M:N relationships, and specialization in schemas.
  - Denormalization trade-offs.

- Complete Exercise 1 and Exercise 2 (entity and relationship modeling).
- Begin thinking about your project domain's conceptual model.
- Read (optional): Elmasri & Navathe Ch. 3–4 *or* Silberschatz Ch. 2.
