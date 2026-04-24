====================================================
Redis Setup Guide
====================================================

This guide walks you through installing Redis, connecting with the
``redis-cli`` shell, and loading a small sample dataset that matches the
lecture's Twitter-clone / leaderboard examples. Two installation options
are provided: **Docker** (recommended for this course) and **native
installation**.

.. tip::

   Use **Redis Stack** (not plain Redis) so that modules like Bloom
   filters (``BF.*``), RedisJSON (``JSON.*``), and RediSearch
   (``FT.*``) are available. The commands in the lecture assume Redis
   Stack.


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


Pull and Start Redis Stack
----------------------------------------------------

.. code-block:: bash

   # Pull the official Redis Stack image (server + modules)
   docker pull redis/redis-stack:latest

   # Start a Redis Stack container
   docker run -d \
     --name redis \
     -p 6379:6379 \
     -p 8001:8001 \
     -v redis_data:/data \
     redis/redis-stack:latest

This command:

- Runs Redis Stack in the background (``-d``).
- Maps port ``6379`` (Redis protocol) and ``8001`` (RedisInsight web UI)
  to your machine.
- Persists data in a Docker volume (``redis_data``) so data survives
  container restarts.

.. tip::

   Visit http://localhost:8001 in your browser to get **RedisInsight**,
   a GUI for exploring keys, inspecting data, and running commands.


Connect with ``redis-cli``
----------------------------------------------------

.. code-block:: bash

   # If you have redis-cli installed locally:
   redis-cli -h localhost -p 6379

   # Otherwise, run it inside the container:
   docker exec -it redis redis-cli

You should see a prompt like:

.. code-block:: text

   127.0.0.1:6379>

Check that Redis is responding:

.. code-block:: text

   PING
   # PONG


Stop and Restart
----------------------------------------------------

.. code-block:: bash

   # Stop the container
   docker stop redis

   # Start it again (data is preserved)
   docker start redis

   # Remove the container entirely
   docker rm -f redis

   # Remove the data volume too (destroys all data)
   docker volume rm redis_data


Option B: Native Installation
====================================================


macOS (Homebrew)
----------------------------------------------------

.. code-block:: bash

   # Install Redis Stack (includes modules used in the lecture)
   brew tap redis-stack/redis-stack
   brew install redis-stack

   # Start Redis Stack as a service
   brew services start redis-stack-server

   # Connect
   redis-cli


Ubuntu / Debian
----------------------------------------------------

Follow the `official Redis install instructions
<https://redis.io/docs/latest/operate/oss_and_stack/install/>`_ for your
Ubuntu version. The general shape:

.. code-block:: bash

   # Add the Redis repository
   curl -fsSL https://packages.redis.io/gpg | sudo gpg --dearmor -o /usr/share/keyrings/redis-archive-keyring.gpg
   echo "deb [signed-by=/usr/share/keyrings/redis-archive-keyring.gpg] https://packages.redis.io/deb $(lsb_release -cs) main" | \
     sudo tee /etc/apt/sources.list.d/redis.list

   sudo apt-get update
   sudo apt-get install -y redis-stack-server

   sudo systemctl start redis-stack-server
   sudo systemctl enable redis-stack-server

   redis-cli


Windows
----------------------------------------------------

Redis is not officially supported on Windows. Use **Docker Desktop**
(Option A) or the **WSL 2** Ubuntu install (Option B) instead.


Verify Your Installation
====================================================

Regardless of installation method, verify Redis is running:

.. code-block:: text

   PING
   # PONG

   INFO server
   # (lots of output, look for redis_version and redis_mode)


Loading the Sample Data
====================================================

The sample data mirrors the lecture's Twitter-clone and leaderboard
examples. Copy and paste into ``redis-cli``.


Users, Feeds, and Direct Messages (String / JSON Style)
-------------------------------------------------------

.. code-block:: text

   SELECT 0

   # -- Users (stored as JSON-serialized strings) --
   SET user:1 '{"name":"Ada",     "email":"ada@example.com",     "city":"Berlin"}'
   SET user:2 '{"name":"Bruno",   "email":"bruno@example.com",   "city":"Lisbon"}'
   SET user:3 '{"name":"Chandra", "email":"chandra@example.com", "city":"Delhi"}'

   # -- Individual messages (one key per message) --
   SET message:ada@example.com:1  '{"user":"ada@example.com",  "text":"Hello world", "ts":1745358379}'
   SET message:ada@example.com:2  '{"user":"ada@example.com",  "text":"second post", "ts":1745358999}'
   SET message:bruno@example.com:1 '{"user":"bruno@example.com","text":"hi from PT",  "ts":1745359100}'

   # -- Per-user feed (as a Redis list of message keys, newest first) --
   LPUSH feed:ada@example.com   message:ada@example.com:1 message:ada@example.com:2
   LPUSH feed:bruno@example.com message:bruno@example.com:1


Friend Lists (Set)
----------------------------------------------------

.. code-block:: text

   SADD friends:ada@example.com   bruno@example.com chandra@example.com
   SADD friends:bruno@example.com ada@example.com
   SADD friends:chandra@example.com ada@example.com

   # Read them back
   SMEMBERS friends:ada@example.com


Leaderboard (Sorted Set)
----------------------------------------------------

.. code-block:: text

   ZADD leaderboard 1500 "ada"
   ZADD leaderboard 1800 "bruno"
   ZADD leaderboard 1200 "chandra"
   ZADD leaderboard 2100 "diana"
   ZADD leaderboard 1750 "emeka"

   # Top 3 (highest scores first)
   ZREVRANGE leaderboard 0 2 WITHSCORES

   # Rank of a user (0-based, highest = 0)
   ZREVRANK leaderboard "ada"


User Profiles (Hash)
----------------------------------------------------

Hashes are a better fit than a JSON-string blob when you want to update
individual fields:

.. code-block:: text

   HSET profile:ada name "Ada Lovelace" email "ada@example.com" city "Berlin" age 30
   HGET profile:ada name
   HINCRBY profile:ada age 1
   HGETALL profile:ada


Key Expiry (TTL)
----------------------------------------------------

.. code-block:: text

   SET session:abc123 "active"
   EXPIRE session:abc123 10
   TTL session:abc123
   # After 10 seconds, the key is gone:
   GET session:abc123


Bloom Filter (Redis Stack Module)
----------------------------------------------------

.. code-block:: text

   # Reserve a bloom filter with 0.1% false-positive rate, 1M expected items
   BF.RESERVE bikes:models 0.001 1000000

   BF.ADD bikes:models "Smoky Mountain Striker"
   BF.EXISTS bikes:models "Smoky Mountain Striker"   # -> 1  (probably yes)
   BF.EXISTS bikes:models "Nonexistent Model"        # -> 0  (definitely no)


Try Some Commands
====================================================

These confirm everything is working and map directly to concepts from
the lecture.


Basic CRUD
----------------------------------------------------

.. code-block:: text

   SET counter 0
   INCR counter
   INCR counter
   INCR counter
   GET counter          # -> "3"
   DEL counter


Feeds with Lists
----------------------------------------------------

.. code-block:: text

   # Add newest post to the front
   LPUSH feed:ada@example.com message:ada@example.com:3

   # Fetch the latest 5 entries
   LRANGE feed:ada@example.com 0 4


Direct Messages (Per-Recipient Inbox)
----------------------------------------------------

.. code-block:: text

   SET message:inbox-msg-90 '{"from":"ada","to":"bruno","text":"hey","unread":true}'

   LPUSH inbox:bruno@example.com message:inbox-msg-90
   LRANGE inbox:bruno@example.com 0 -1


Cleanup
====================================================

Flush the current database:

.. code-block:: text

   FLUSHDB

Or flush everything (all databases in this instance):

.. code-block:: text

   FLUSHALL

Or, if using Docker:

.. code-block:: bash

   docker rm -f redis
   docker volume rm redis_data


Further Reading
====================================================

- Redis install reference: https://redis.io/docs/latest/operate/oss_and_stack/install/
- Redis data types: https://redis.io/docs/latest/develop/data-types/
- Redis commands: https://redis.io/commands/
- RedisInsight (bundled with Redis Stack on port 8001): GUI for
  exploring and running commands against your instance.
