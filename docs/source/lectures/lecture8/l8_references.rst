References
==========


.. dropdown:: Lecture 8
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L8: JOINs, Query Execution, and Indexing**

        Covers SQL JOINs from first principles through production use:
        Cartesian products and relational algebra, all SQL join types
        (``INNER``, ``LEFT``, ``RIGHT``, ``FULL OUTER``, ``CROSS``,
        self-join, semi/anti via ``EXISTS`` / ``NOT EXISTS``), ``USING``
        and ``NATURAL JOIN`` caveats, PostgreSQL ``LATERAL`` joins,
        ``ON`` vs ``WHERE`` semantics for inner and outer joins. The
        execution section covers logical vs physical joins, nested loop /
        hash / merge join strategies, reading ``EXPLAIN (ANALYZE, BUFFERS)``
        output, Big O analysis of join algorithms, disk and memory
        architecture (heap pages, ``shared_buffers``, ``work_mem``), and
        index design for join-heavy workloads (B-tree, composite indexes,
        ``INCLUDE`` columns).

        **Before next class**: complete the take-home exercises (Exercises 5
        and 6) and run ``EXPLAIN (ANALYZE, BUFFERS)`` on your own join
        queries in ``university_db``.


.. dropdown:: PostgreSQL Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: SELECT / FROM / JOIN
            :link: https://www.postgresql.org/docs/current/queries-table-expressions.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Table Expressions**

            Complete reference for ``FROM`` clause, join types (``INNER``,
            ``LEFT``, ``RIGHT``, ``FULL``, ``CROSS``), ``LATERAL``
            subqueries, and ``USING`` / ``NATURAL`` syntax.

            +++

            - All join types with examples
            - ``LATERAL`` subqueries
            - ``USING`` and ``NATURAL JOIN``
            - Table aliases and subqueries in ``FROM``

        .. grid-item-card:: EXPLAIN
            :link: https://www.postgresql.org/docs/current/sql-explain.html
            :class-card: sd-border-secondary

            **PostgreSQL -- EXPLAIN Reference**

            Reference for ``EXPLAIN`` including ``ANALYZE``, ``BUFFERS``,
            ``FORMAT``, and ``VERBOSE`` options. Shows how to read query
            plans and interpret cost estimates.

            +++

            - ``EXPLAIN (ANALYZE, BUFFERS)``
            - Estimated vs actual rows
            - Node types (Seq Scan, Index Scan, Hash Join, etc.)
            - Cost model interpretation

        .. grid-item-card:: Indexes
            :link: https://www.postgresql.org/docs/current/indexes.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Indexes**

            Comprehensive guide to PostgreSQL index types, multi-column
            indexes, partial indexes, covering indexes (``INCLUDE``), and
            expression indexes.

            +++

            - B-tree, Hash, GiST, GIN, BRIN
            - Multi-column / composite indexes
            - ``INCLUDE`` for covering indexes
            - ``CREATE INDEX CONCURRENTLY``

        .. grid-item-card:: Query Planning
            :link: https://www.postgresql.org/docs/current/planner-optimizer.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Planner/Optimizer**

            Internal documentation on how PostgreSQL's query planner
            chooses between different join strategies and scan methods.

            +++

            - Cost-based optimization
            - Join order selection
            - Statistics and ``pg_stats``
            - ``CREATE STATISTICS`` for correlated columns


.. dropdown:: Textbook References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Silberschatz, Korth, Sudarshan
            :class-card: sd-border-secondary

            **Database System Concepts (7th Edition)**

            - Chapter 12: Query Processing -- covers join algorithms
              (nested loop, merge, hash), cost analysis, evaluation of
              expressions.
            - Chapter 13: Query Optimization -- covers equivalence rules,
              join ordering, cost estimation, statistics.
            - Chapter 14: Indexing -- B+ trees, hash indexes, bitmap
              indexes, index design.

        .. grid-item-card:: Elmasri & Navathe
            :class-card: sd-border-secondary

            **Fundamentals of Database Systems (7th Edition)**

            - Chapter 8: SQL joins, subqueries, ``EXISTS``, aggregate
              functions.
            - Chapter 18: Query processing and optimization strategies.
            - Chapter 17: Indexing structures for files (B-trees, B+
              trees, hash indexes).


.. dropdown:: Additional Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Use The Index, Luke
            :link: https://use-the-index-luke.com/
            :class-card: sd-border-secondary

            **SQL Indexing and Tuning e-Book**

            Free online resource explaining how indexes work, covering
            ``WHERE``, ``JOIN``, ``ORDER BY`` optimization, and
            partial/covering indexes. Database-agnostic with
            PostgreSQL-specific notes.

        .. grid-item-card:: pgMustard EXPLAIN Glossary
            :link: https://www.pgmustard.com/docs/explain
            :class-card: sd-border-secondary

            **EXPLAIN Plan Node Reference**

            Concise descriptions of every node type that can appear in a
            PostgreSQL ``EXPLAIN`` plan, including join nodes, scan nodes,
            and aggregate nodes.

        .. grid-item-card:: PostgreSQL Wiki -- Performance
            :link: https://wiki.postgresql.org/wiki/Performance_Optimization
            :class-card: sd-border-secondary

            **PostgreSQL Performance Optimization**

            Community-maintained wiki page with tips on ``work_mem``
            tuning, index strategies, ``EXPLAIN`` interpretation, and
            common performance pitfalls.
