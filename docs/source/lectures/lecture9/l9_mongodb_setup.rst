====================================================
MongoDB Setup Guide
====================================================

This guide walks you through installing MongoDB, connecting with the
``mongosh`` shell, and loading a sample database that matches the
lecture's order/customer/product domain. Two installation options are
provided: **Docker** (recommended for this course) and **native
installation**.


Option A: Docker (Recommended)
====================================================

Docker provides the fastest, cleanest setup. No system-level packages
are installed, and you can remove everything with a single command.


Prerequisites
----------------------------------------------------

- Docker Desktop installed and running.

  - **macOS / Windows**: download from https://www.docker.com/products/docker-desktop/
  - **Linux**: install Docker Engine via your package manager.

- Verify Docker is working:

  .. code-block:: bash

     docker --version
     # Docker version 27.x.x or later


Pull and Start MongoDB
----------------------------------------------------

.. code-block:: bash

   # Pull the official MongoDB image
   docker pull mongodb/mongodb-community-server:latest

   # Start a MongoDB container
   docker run -d \
     --name mongodb \
     -p 27017:27017 \
     -v mongodb_data:/data/db \
     mongodb/mongodb-community-server:latest

This command:

- Runs MongoDB in the background (``-d``).
- Maps port ``27017`` on your machine to the container.
- Persists data in a Docker volume (``mongodb_data``) so your data
  survives container restarts.


Connect with mongosh
----------------------------------------------------

.. code-block:: bash

   # Install mongosh (if not already installed)
   # macOS:
   brew install mongosh

   # Ubuntu/Debian:
   # Follow: https://www.mongodb.com/docs/mongodb-shell/install/

   # Connect to the running container
   mongosh "mongodb://localhost:27017"

You should see a prompt like:

.. code-block:: text

   test>

You are connected and ready to go.

.. tip::

   If you prefer not to install ``mongosh`` separately, you can run it
   inside the container:

   .. code-block:: bash

      docker exec -it mongodb mongosh


Stop and Restart
----------------------------------------------------

.. code-block:: bash

   # Stop the container
   docker stop mongodb

   # Start it again (data is preserved)
   docker start mongodb

   # Remove the container entirely
   docker rm -f mongodb

   # Remove the data volume too (destroys all data)
   docker volume rm mongodb_data


Option B: Native Installation
====================================================


macOS (Homebrew)
----------------------------------------------------

.. code-block:: bash

   # Tap the MongoDB formula
   brew tap mongodb/brew

   # Install MongoDB Community Edition
   brew install mongodb-community

   # Start MongoDB as a background service
   brew services start mongodb-community

   # Connect
   mongosh


Ubuntu / Debian
----------------------------------------------------

Follow the official instructions for your Ubuntu version. The general
steps are:

.. code-block:: bash

   # Import the MongoDB GPG key
   curl -fsSL https://www.mongodb.org/static/pgp/server-8.0.asc | \
     sudo gpg -o /usr/share/keyrings/mongodb-server-8.0.gpg --dearmor

   # Add the repository (Ubuntu 22.04 example)
   echo "deb [ signed-by=/usr/share/keyrings/mongodb-server-8.0.gpg ] \
     https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/8.0 multiverse" | \
     sudo tee /etc/apt/sources.list.d/mongodb-org-8.0.list

   # Install
   sudo apt-get update
   sudo apt-get install -y mongodb-org

   # Start the service
   sudo systemctl start mongod
   sudo systemctl enable mongod

   # Connect
   mongosh

.. note::

   Check the `MongoDB installation docs
   <https://www.mongodb.com/docs/manual/installation/>`_ for the latest
   instructions matching your OS version.


Windows
----------------------------------------------------

1. Download the MSI installer from the `MongoDB Download Center
   <https://www.mongodb.com/try/download/community>`_.
2. Run the installer -- choose "Complete" setup and install as a Windows
   service.
3. ``mongosh`` is installed alongside. Open a terminal and run:

   .. code-block:: bash

      mongosh


Verify Your Installation
====================================================

Regardless of installation method, verify that MongoDB is running:

.. code-block:: javascript

   // In mongosh
   db.runCommand({ ping: 1 })

Expected output:

.. code-block:: javascript

   { ok: 1 }


Loading the Sample Database
====================================================

The sample database mirrors the lecture's e-commerce domain: **customers**,
**products**, **orders** (with embedded items and shipping), and
**reviews**.


Create the Database and Collections
----------------------------------------------------

Copy and paste the following into ``mongosh``:

.. code-block:: javascript

   // Switch to the sample database
   use enpm818t

   // -- Customers --
   db.customers.insertMany([
     { _id: 1, name: "Ada",     email: "ada@example.com",     city: "Berlin",  memberSince: new Date("2023-01-15") },
     { _id: 2, name: "Bruno",   email: "bruno@example.com",   city: "Lisbon",  memberSince: new Date("2023-03-22") },
     { _id: 3, name: "Chandra", email: "chandra@example.com", city: "Delhi",   memberSince: new Date("2023-06-10") },
     { _id: 4, name: "Diana",   email: "diana@example.com",   city: "Oslo",    memberSince: new Date("2024-01-05") },
     { _id: 5, name: "Emeka",   email: "emeka@example.com",   city: "Lagos",   memberSince: new Date("2024-04-18") }
   ])

   // -- Products --
   db.products.insertMany([
     { _id: "A-42", title: "Mechanical Keyboard", category: "electronics", price: 19.99, inStock: true },
     { _id: "B-07", title: "USB-C Hub",           category: "electronics", price: 7.50,  inStock: true },
     { _id: "C-99", title: "Notebook Stand",      category: "accessories", price: 12.50, inStock: true },
     { _id: "D-15", title: "Webcam HD",           category: "electronics", price: 34.99, inStock: false },
     { _id: "E-33", title: "Desk Lamp",           category: "accessories", price: 22.00, inStock: true }
   ])

   // -- Orders (with embedded items and shipping) --
   db.orders.insertMany([
     {
       _id: 9001,
       customerId: 1,
       status: "PAID",
       createdAt: new Date("2026-03-01"),
       total: 47.48,
       shipping: { country: "DE", city: "Berlin" },
       items: [
         { sku: "A-42", qty: 2, priceAtPurchase: 19.99 },
         { sku: "B-07", qty: 1, priceAtPurchase: 7.50 }
       ]
     },
     {
       _id: 9002,
       customerId: 1,
       status: "PAID",
       createdAt: new Date("2026-03-05"),
       total: 12.50,
       shipping: { country: "DE", city: "Berlin" },
       items: [
         { sku: "C-99", qty: 1, priceAtPurchase: 12.50 }
       ]
     },
     {
       _id: 9003,
       customerId: 3,
       status: "PAID",
       createdAt: new Date("2026-03-07"),
       total: 69.98,
       shipping: { country: "IN", city: "Delhi" },
       items: [
         { sku: "D-15", qty: 2, priceAtPurchase: 34.99 }
       ]
     },
     {
       _id: 9004,
       customerId: 2,
       status: "OPEN",
       createdAt: new Date("2026-03-10"),
       total: 22.00,
       shipping: { country: "PT", city: "Lisbon" },
       items: [
         { sku: "E-33", qty: 1, priceAtPurchase: 22.00 }
       ]
     },
     {
       _id: 9005,
       customerId: 5,
       status: "PAID",
       createdAt: new Date("2026-03-12"),
       total: 41.99,
       shipping: { country: "NG", city: "Lagos" },
       items: [
         { sku: "A-42", qty: 1, priceAtPurchase: 19.99 },
         { sku: "E-33", qty: 1, priceAtPurchase: 22.00 }
       ]
     },
     {
       _id: 9006,
       customerId: 4,
       status: "CANCELLED",
       createdAt: new Date("2026-03-14"),
       total: 7.50,
       shipping: { country: "NO", city: "Oslo" },
       items: [
         { sku: "B-07", qty: 1, priceAtPurchase: 7.50 }
       ]
     }
   ])

   // -- Reviews (separate collection, referenced by product) --
   db.reviews.insertMany([
     { _id: 1, productId: "A-42", customerId: 1, rating: 5, text: "Great keyboard!",      createdAt: new Date("2026-03-03") },
     { _id: 2, productId: "A-42", customerId: 5, rating: 4, text: "Good build quality.",   createdAt: new Date("2026-03-15") },
     { _id: 3, productId: "B-07", customerId: 1, rating: 3, text: "Works but feels cheap.",createdAt: new Date("2026-03-06") },
     { _id: 4, productId: "C-99", customerId: 1, rating: 5, text: "Perfect for my desk.",  createdAt: new Date("2026-03-08") },
     { _id: 5, productId: "D-15", customerId: 3, rating: 2, text: "Arrived broken.",       createdAt: new Date("2026-03-10") },
     { _id: 6, productId: "E-33", customerId: 5, rating: 4, text: "Nice warm light.",      createdAt: new Date("2026-03-16") }
   ])


Verify the Data
----------------------------------------------------

.. code-block:: javascript

   // Check document counts
   db.customers.countDocuments()   // 5
   db.products.countDocuments()    // 5
   db.orders.countDocuments()      // 6
   db.reviews.countDocuments()     // 6

   // Browse a single order
   db.orders.findOne({ _id: 9001 })


Create Useful Indexes
----------------------------------------------------

These indexes support the queries used in the lecture and exercises:

.. code-block:: javascript

   // Compound index for filtering orders by status and date
   db.orders.createIndex({ status: 1, createdAt: -1 })

   // Index on customerId for customer-based lookups
   db.orders.createIndex({ customerId: 1 })

   // Multikey index on embedded item SKUs
   db.orders.createIndex({ "items.sku": 1 })

   // Index on shipping country
   db.orders.createIndex({ "shipping.country": 1, status: 1 })

   // Index for reviews by product
   db.reviews.createIndex({ productId: 1, createdAt: -1 })

   // TTL index example (for sessions -- not used by sample data)
   // db.sessions.createIndex({ expiresAt: 1 }, { expireAfterSeconds: 0 })


Try Some Queries
====================================================

Here are a few queries to confirm everything is working. These map
directly to concepts from the lecture.


Basic Find
----------------------------------------------------

.. code-block:: javascript

   // All paid orders
   db.orders.find({ status: "PAID" })

   // Orders shipping to Germany
   db.orders.find({ "shipping.country": "DE" })

   // Orders containing product A-42
   db.orders.find({ "items.sku": "A-42" })


Projection and Sort
----------------------------------------------------

.. code-block:: javascript

   // Open orders, showing only customerId and total, newest first
   db.orders.find(
     { status: "OPEN" },
     { _id: 0, customerId: 1, total: 1 }
   ).sort({ createdAt: -1 })


Update
----------------------------------------------------

.. code-block:: javascript

   // Mark order 9004 as PAID
   db.orders.updateOne(
     { _id: 9004 },
     { $set: { status: "PAID" } }
   )

   // Add a new item to order 9004
   db.orders.updateOne(
     { _id: 9004 },
     { $push: { items: { sku: "C-99", qty: 1, priceAtPurchase: 12.50 } } }
   )


Aggregation Pipeline
----------------------------------------------------

.. code-block:: javascript

   // Revenue by customer (paid orders only)
   db.orders.aggregate([
     { $match: { status: "PAID" } },
     { $group: { _id: "$customerId", revenue: { $sum: "$total" } } },
     { $sort: { revenue: -1 } }
   ])

   // Join orders with customer names
   db.orders.aggregate([
     {
       $lookup: {
         from: "customers",
         localField: "customerId",
         foreignField: "_id",
         as: "customer"
       }
     },
     { $unwind: "$customer" },
     { $project: { _id: 1, "customer.name": 1, status: 1, total: 1 } }
   ])


Explain Plan
----------------------------------------------------

.. code-block:: javascript

   // Check whether the query uses an index
   db.orders.find({
     status: "OPEN",
     "shipping.country": "DE"
   }).explain("executionStats")

Look for ``IXSCAN`` (index scan) vs ``COLLSCAN`` (full collection scan)
in the output.


Cleanup
====================================================

If you want to start fresh:

.. code-block:: javascript

   // Drop the entire database
   use enpm818t
   db.dropDatabase()

Or, if using Docker:

.. code-block:: bash

   docker rm -f mongodb
   docker volume rm mongodb_data
