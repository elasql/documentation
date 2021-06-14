# ElaSQL Architecture

This document summaries the architecture of ElaSQL.

The following figure show the modules inside ElaSQL.

![ElaSQL Architecture](elasql-architecture.png)

Here is the functionality of each module:

- Group Communication
  - Responsible for communication with other server and client processes.
  - Two types of communication protocols are supported:
    - Zookeeper Atomic Broadcast (ZAB): for ordering client requests
    - Point-to-Point (P2P): for sending messages between any pair of nodes
  - Backed by [VanillaComm](https://github.com/vanilladb/vanillacomm)
- Scheduler
  - Responsible for receiving total ordered requests, analyzing the requests and scheduling the requests to worker threads.
  - Single-threaded
- Migration
  - Responsible for issuing a data migration task and managing the progress of data migrations.
  - This module is turned off by default and can be turned on in `elasql.properties`.
- Stored Procedures
  - Responsible for executing transaction logic.
- Cache Manager
  - Responsible for managing a cache for temporarily saving records coming from remote machines and between transactions.
  - In Hermes [3], this layer also caches the data of other partitions for data-fusion.
- Query Engine & Storage Engine
  - Responsible for answering SQLs and storing data on disks.
  - Here we reuse the query engine and storage engine of [VanillaCore](https://github.com/vanilladb/vanillacore), and we create a class, `org.elasql.cache.VanillaCoreCrud`, as the CRUD interface to interact with VanillaCore. All the data queries and manipulations will go through this interface.
- Transaction (TX)
  - Concurrency Manger
    - Responsible for ensuring transactional consistency and isolation via locking mechanism.
    - In order to ensure determinism, we implement Conservative Ordered Locking Protocol.
  - Recovery Manager
    - Responsible for logging client requests.
    - VanillaCore already has a recovery mechanism to ensure durability. This recovery manager only logs transaction requests. The algorithm of recovering the system using request logs has not been implemented yet.

## Transaction Workflow (Calvin [1])

In order to better understand the codebase, we suggest readers to follow the workflow of a transaction.

The following figure shows the workflow of a transaction in the Calvin implementation of ElaSQL.

![Calvin Workflow](calvin-workflow.png)

Note that, in addition to Calvin, ElaSQL also has other transaction execution engine, such as T-Part [2]. Each engine has its own implementation in each module. For example, both Calvin and T-Part have their own schedulers:

- `org.elasql.schedule.calvin.CalvinScheduler`
- `org.elasql.schedule.tpart.TPartPartitioner`

When following the above transaction workflow, remember to check the right (Calvin's) implementation.

Once you know how a transaction is processed in Calvin, it will be easier to trace the code of other execution engines.

## References

[1]: Thomson, Alexander, et al. "Calvin: fast distributed transactions for partitioned database systems." Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data. 2012.

[2]: Wu, Shan-Hung, et al. "T-part: Partitioning of transactions for forward-pushing in deterministic database systems." Proceedings of the 2016 International Conference on Management of Data. 2016.

[3]: Yu-Shan Lin, et al. "Don't Look Back, Look into the Future: Prescient Data Partitioning and Migration for Deterministic Database Systems." Proceedings of the 2021 International Conference on Management of Data. 2021.
