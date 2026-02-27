====================================================
Sample Data Generation Guide
====================================================

Once you have created your PostgreSQL schema (``schema.sql``), use the prompt
below to generate realistic sample data that fits **your** table structure.

.. important::

   **How to Use This Guide**

   1. Run your ``schema.sql`` to create all tables
   2. Export your schema definition (see instructions below)
   3. Paste the prompt below into an LLM (e.g., Claude, ChatGPT) along with your schema
   4. Review the generated SQL for correctness
   5. Load into your database


Step 1: Export Your Schema
--------------------------

Run this command to extract your table definitions:

.. code-block:: bash

   pg_dump -d traffic_management --schema-only --no-owner --no-privileges > my_schema.sql

Alternatively, in ``psql``:

.. code-block:: psql

   \d+ intersection
   \d+ traffic_signal
   -- repeat for all tables


Step 2: Generate Data
---------------------

Copy the prompt below and paste it into an LLM along with your schema
definition. Replace ``[PASTE YOUR SCHEMA HERE]`` with the output from Step 1.

.. dropdown:: Data Generation Prompt (click to expand, then copy)
   :icon: gear
   :class-container: sd-border-primary
   :open:

   .. code-block:: text

      I have a PostgreSQL database for a Smart City Traffic Management System.
      Below is my complete schema. Generate realistic INSERT statements for
      all tables, following these requirements:

      SCHEMA:
      [PASTE YOUR SCHEMA HERE]

      DATA REQUIREMENTS:

      1. Traffic Zones: 5-6 zones (downtown, residential, industrial,
         school, commercial). Each with appropriate speed limits and
         enforcement levels.

      2. Intersections: 50-60 intersections arranged in a realistic city
         grid. Use coordinates near Washington, D.C. (latitude ~38.89-38.92,
         longitude ~-77.01 to -77.05). Names should follow the pattern
         "Street A & Street B". Include a mix of 4-way, T-junction, and
         roundabout types.

      3. Traffic Signals: 2-4 signals per intersection (north, south, east,
         west positions). Mix of LED, incandescent, and pedestrian types.
         Various timing modes (fixed, adaptive, emergency).

      4. Sensors: 2-4 sensors per intersection. Types include inductive
         loop, radar, camera, lidar, acoustic. Most should be "active"
         status with a few in "maintenance" or "offline".

      5. Road Segments: 50-70 segments connecting nearby intersections.
         Varying lane counts (2, 4, 6), speed limits, and surface types.
         Include some with bike lanes and sidewalks.

      6. Maintenance Crews: 10-12 crews with different specializations
         (electrical, mechanical, civil, software) and certification levels.

      7. Maintenance Schedules: 100-120 records spanning the last 90 days
         plus 30 days into the future. Mix of preventive, corrective,
         inspection, and upgrade types. Past records should be "completed";
         future records "scheduled" or "in_progress".

      8. Incidents: 75-80 incidents over the last 90 days. Bias toward rush
         hours (7-9 AM, 4-7 PM). Distribution: ~40% minor, ~30% moderate,
         ~20% major, ~10% critical. Some should have NULL resolved_at
         (still open). Types: accident, vehicle_breakdown, road_hazard,
         construction, special_event.

      9. Emergency Facilities: 10-12 facilities including hospitals, fire
         stations, and police stations with realistic names, capacities,
         and contact info.

      10. Emergency Routes: 20-25 routes connecting facilities to
          intersections with varying priorities and average response times.

      11. Weather Stations: 5-6 stations spread across the city grid,
          attached to specific intersections.

      12. Parking Facilities: 10-12 facilities (surface lots, garages,
          street parking) with capacities, EV charging spots, and pricing.

      CONSTRAINTS:
      - All foreign key references must be valid
      - All CHECK constraints in my schema must be satisfied
      - Use NULL where appropriate (optional fields, unresolved incidents)
      - Dates should be realistic (installation dates 2005-2023, incidents
        in last 90 days, maintenance spanning past and future)
      - Geographic coordinates should form a plausible city grid

      OUTPUT FORMAT:
      - Pure SQL INSERT statements, one per table
      - Include a comment header with row counts per table
      - Order tables so that parent tables are populated before child tables
        (e.g., intersection before traffic_signal)
      - Do not include any CREATE TABLE or DROP statements


Step 3: Verify Your Data
-------------------------

After loading the generated data, run these verification queries:

.. code-block:: sql

   -- Row counts
   SELECT 'intersection' AS tbl, COUNT(*) FROM intersection
   UNION ALL SELECT 'traffic_signal', COUNT(*) FROM traffic_signal
   UNION ALL SELECT 'sensor', COUNT(*) FROM sensor
   UNION ALL SELECT 'road_segment', COUNT(*) FROM road_segment
   UNION ALL SELECT 'maintenance_crew', COUNT(*) FROM maintenance_crew
   UNION ALL SELECT 'maintenance_schedule', COUNT(*) FROM maintenance_schedule
   UNION ALL SELECT 'incident', COUNT(*) FROM incident
   UNION ALL SELECT 'emergency_facility', COUNT(*) FROM emergency_facility
   UNION ALL SELECT 'emergency_route', COUNT(*) FROM emergency_route
   UNION ALL SELECT 'weather_station', COUNT(*) FROM weather_station
   UNION ALL SELECT 'parking_facility', COUNT(*) FROM parking_facility
   UNION ALL SELECT 'traffic_zone', COUNT(*) FROM traffic_zone
   ORDER BY tbl;

   -- Check for orphan foreign keys (example for traffic_signal)
   SELECT s.signal_id
   FROM traffic_signal s
   LEFT JOIN intersection i ON s.intersection_id = i.intersection_id
   WHERE i.intersection_id IS NULL;

   -- Verify geographic spread
   SELECT
       MIN(latitude) AS min_lat, MAX(latitude) AS max_lat,
       MIN(longitude) AS min_lon, MAX(longitude) AS max_lon
   FROM intersection;

   -- Verify temporal spread of incidents
   SELECT
       MIN(reported_at) AS earliest,
       MAX(reported_at) AS latest,
       COUNT(*) AS total
   FROM incident;

.. tip::

   If the LLM generates data that violates a constraint, fix the specific
   rows rather than regenerating everything. Common issues include:

   - CHECK constraint violations (values outside allowed ranges)
   - Duplicate primary keys
   - Foreign keys referencing non-existent parent rows
   - NULL in NOT NULL columns

   You can also ask the LLM to fix specific errors by pasting the error
   message back into the conversation.
