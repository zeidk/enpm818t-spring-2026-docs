References
==========


.. dropdown:: Lecture 11
    :class-container: sd-border-secondary
    :open:

    .. card::
        :class-card: sd-border-secondary

        **ENPM818T -- L11: Optimizing SQL Queries**

        Covers SQL query optimization in PostgreSQL end-to-end: why
        query optimization is the most cost-effective performance
        lever; the query plan and the query optimizer; ``EXPLAIN`` vs
        ``EXPLAIN ANALYZE`` (and their behavior on mutating queries);
        reading basic plans (``Seq Scan``, cost, rows, width,
        ``Filter``, ``Rows Removed by Filter``, planning and execution
        time); PostgreSQL's cost constants (``seq_page_cost``,
        ``random_page_cost``, ``cpu_tuple_cost``,
        ``cpu_index_tuple_cost``, ``cpu_operator_cost``,
        ``parallel_setup_cost``, ``parallel_tuple_cost``) and what
        they reveal; unwinding advanced plans inside-out; the impact
        of join key selection (Merge Join vs Nested Loop + Index Scan
        + Memoize); debugging CTE / view / temp-table plans;
        ``EXPLAIN (ANALYZE, BUFFERS)`` / ``(ANALYZE, MEMORY)`` /
        ``(ANALYZE, SERIALIZE)``; SARGABLE query design; compound
        indexes and the leftmost-prefix rule; index drawbacks; the
        three physical join strategies (Nested Loop, Merge, Hash) and
        how the planner chooses between them.

        **Before next class**: complete the take-home exercises on
        the exercises page and run ``EXPLAIN ANALYZE`` on the sample
        database from the setup guide.


.. dropdown:: PostgreSQL Official Documentation
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Using EXPLAIN
            :link: https://www.postgresql.org/docs/current/using-explain.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Using EXPLAIN**

            The canonical reference for reading PostgreSQL query
            plans. Covers ``EXPLAIN``, ``EXPLAIN ANALYZE``, the
            ``(ANALYZE, BUFFERS)`` / ``(MEMORY)`` /
            ``(SERIALIZE)`` options, and the meaning of every
            line in the output.

            +++

            - Cost and row estimates
            - Scan methods
            - Join methods
            - Reading complex nested plans

        .. grid-item-card:: Planner Cost Constants
            :link: https://www.postgresql.org/docs/current/runtime-config-query.html#RUNTIME-CONFIG-QUERY-CONSTANTS
            :class-card: sd-border-secondary

            **PostgreSQL -- Planner Cost Constants**

            Reference for the configuration variables that drive the
            planner's cost model: ``seq_page_cost``,
            ``random_page_cost``, ``cpu_tuple_cost``, and friends.

            +++

            - Default values and rationale
            - When (and when not) to tune them
            - Interaction with ``effective_cache_size``

        .. grid-item-card:: Resource Consumption
            :link: https://www.postgresql.org/docs/current/runtime-config-resource.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Resource Consumption**

            Reference for ``shared_buffers``, ``work_mem``,
            ``maintenance_work_mem``, and other memory-related
            settings that influence plan shape and performance.

            +++

            - ``work_mem`` vs ``shared_buffers``
            - Hash Join vs Merge Join thresholds
            - Autovacuum and maintenance memory

        .. grid-item-card:: Indexes
            :link: https://www.postgresql.org/docs/current/indexes.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Indexes**

            Comprehensive guide to PostgreSQL index types: B-tree,
            hash, GiST, SP-GiST, GIN, BRIN, and functional /
            partial / covering indexes.

            +++

            - Compound indexes and leftmost prefix
            - Functional indexes
            - Partial indexes
            - Index-only scans

        .. grid-item-card:: Planner / Optimizer
            :link: https://www.postgresql.org/docs/current/planner-optimizer.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Planner / Optimizer**

            Internal documentation on how PostgreSQL chooses query
            plans, including the generic cost-based optimizer and
            the genetic query optimizer for large join searches.

            +++

            - Plan generation
            - GEQO
            - Statistics collection (``ANALYZE``)

        .. grid-item-card:: Statistics Used by the Planner
            :link: https://www.postgresql.org/docs/current/planner-stats.html
            :class-card: sd-border-secondary

            **PostgreSQL -- Planner Statistics**

            Documentation for ``ANALYZE``, ``pg_stats``, and
            ``CREATE STATISTICS`` (extended statistics). Essential
            reading when the planner's row estimates diverge from
            reality.

            +++

            - Single-column stats
            - Extended stats for correlated columns
            - Refreshing stats after bulk loads


.. dropdown:: Textbook References
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Silberschatz, Korth, Sudarshan
            :class-card: sd-border-secondary

            **Database System Concepts (7th Edition)**

            - Chapter 15: Query Processing -- measures of cost,
              selection operation, sorting, join operation, other
              operations, evaluation of expressions.
            - Chapter 16: Query Optimization -- transformation of
              relational expressions, estimating statistics, choice
              of evaluation plans.
            - Chapter 14: Indexing -- B+ trees, hash indexes, and
              their cost trade-offs.

        .. grid-item-card:: Garcia-Molina, Ullman, Widom
            :class-card: sd-border-secondary

            **Database Systems: The Complete Book**

            - Chapter 15: Query Execution and Optimization -- classic
              treatment of physical join algorithms and
              cost-based optimization.

        .. grid-item-card:: Kleppmann
            :class-card: sd-border-secondary

            **Designing Data-Intensive Applications**

            - Chapter 3: Storage and Retrieval -- B-trees, LSM trees,
              and index internals.
            - Chapter 10: Batch Processing -- related background on
              query execution at scale.

        .. grid-item-card:: Winand
            :class-card: sd-border-secondary

            **SQL Performance Explained (Markus Winand)**

            A focused, readable book on index design and query
            performance across PostgreSQL, MySQL, Oracle, and SQL
            Server. The companion website `use-the-index-luke.com
            <https://use-the-index-luke.com/>`_ is free.


.. dropdown:: Additional Resources
    :class-container: sd-border-secondary

    .. grid:: 1 1 2 2
        :gutter: 2

        .. grid-item-card:: Magic Numbers for Computer Engineers
            :link: https://gist.github.com/jboner/2841832
            :class-card: sd-border-secondary

            **Latency Numbers Every Programmer Should Know**

            Reference list of approximate latencies (L1 / L2 cache,
            RAM, SSD, disk, network). Useful intuition when reading
            ``EXPLAIN (ANALYZE, BUFFERS)`` output.

        .. grid-item-card:: Use The Index, Luke!
            :link: https://use-the-index-luke.com/
            :class-card: sd-border-secondary

            **Use The Index, Luke!**

            Free companion to *SQL Performance Explained*. A
            readable, example-driven tour of SQL indexing across
            PostgreSQL, MySQL, Oracle, and SQL Server.

        .. grid-item-card:: explain.depesz.com
            :link: https://explain.depesz.com/
            :class-card: sd-border-secondary

            **Depesz Explain Visualizer**

            Paste in a PostgreSQL ``EXPLAIN ANALYZE`` plan and get a
            color-coded, sortable view that highlights the most
            expensive steps. Great for complex plans.

        .. grid-item-card:: pgMustard
            :link: https://www.pgmustard.com/
            :class-card: sd-border-secondary

            **pgMustard**

            A commercial query-plan analyzer with a free tier that
            annotates plans with specific, actionable advice. Good
            training wheels when you are still learning what to
            look for.

        .. grid-item-card:: pg_stat_statements
            :link: https://www.postgresql.org/docs/current/pgstatstatements.html
            :class-card: sd-border-secondary

            **pg_stat_statements**

            Built-in PostgreSQL extension that records execution
            statistics per query shape. The standard way to identify
            which queries deserve ``EXPLAIN ANALYZE`` attention in
            production.

        .. grid-item-card:: Index Usage Statistics
            :link: https://www.postgresql.org/docs/current/monitoring-stats.html
            :class-card: sd-border-secondary

            **PostgreSQL Monitoring Views**

            ``pg_stat_user_indexes`` and related views let you find
            unused indexes (safe to drop) and hot indexes (worth
            keeping warm). Essential for periodic index cleanup.
