ENPM818T — Data Storage and Databases
=======================================

Course Description
------------------
ENPM818T focuses on modern database technologies and data management
practices, providing students with the skills to design, implement, and
optimize database systems for real-world applications.  This course
introduces students to both relational databases (PostgreSQL) and NoSQL
databases (MongoDB, Redis, Cassandra, Neo4j) through hands-on projects
and practical examples.

The course emphasizes polyglot persistence — using multiple database
technologies within the same application based on specific data
requirements.  Students will learn to integrate databases with Python
applications, deploy to cloud environments, and implement
production-ready database solutions.

Key topics covered include:

- Data modeling: conceptual (ERD), logical, and physical models
- Keys: primary, foreign, composite, surrogate, natural, candidate, and alternate keys
- Normalization, denormalization, and schema design
- SQL fundamentals through advanced queries (JOINs, subqueries, CTEs, window functions)
- Python database integration with psycopg2, SQLAlchemy, PyMongo, and other drivers
- Query optimization, indexing strategies, and performance tuning
- Database scaling: replication, sharding, and caching
- Production operations: migrations, cloud deployment, backup and recovery
- NoSQL databases: document (MongoDB), key-value (Redis), column-family (Cassandra), graph (Neo4j)
- Database security, compliance, and best practices

Prerequisites
-------------
Basic programming experience (Python preferred).  No prior database
experience required.

Learning Outcomes
-----------------
After successfully completing this course, you will be able to:

- Design efficient database schemas using ER diagrams and normalization techniques.
- Select and implement appropriate key strategies (surrogate vs. natural, composite keys).
- Write and optimize complex SQL queries for relational databases.
- Evaluate and implement appropriate NoSQL solutions based on use cases.
- Develop scalable database architectures using partitioning, sharding, and replication.
- Integrate databases with Python applications using industry-standard libraries.
- Deploy and manage databases in cloud environments.
- Select the right database technology for specific data requirements.

.. toctree::
   :maxdepth: 3
   :titlesonly:

   lecture1/index
   lecture2/index