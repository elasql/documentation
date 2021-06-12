# Implemented Systems

This document introduces the systems or algorithms that are implemented in [ElaSQL](https://github.com/elasql/elasql).

## Distributed Transaction Execution

### SIGMOD'12 - Calvin

Calvin is a distributed database system that relies on deterministic execution to execute transactions. Thanks to determinism, Calvin does not need to perform two phase commit to ensure strong consistency among replicas, which also gives it capability to scale out near linearly.

The design of ElaSQL is based on the architecture of Calvin, so it is important to understand Calvin before tracing the code of ElaSQL.

Reference:
- Thomson, Alexander, and Daniel J. Abadi. "The case for determinism in database systems." Proceedings of the VLDB Endowment 3.1-2 (2010): 70-80.
- Thomson, Alexander, et al. "Calvin: fast distributed transactions for partitioned database systems." Proceedings of the 2012 ACM SIGMOD International Conference on Management of Data. 2012.

### SIGMOD'16 - T-Part

T-Part is a deterministic transaction execution mechanism that tries to address the scalability problem on dynamic workloads. The key idea is to analyze transaction dependencies and route the transactions to minimize the number of transactions and balance the loads among machines. It also proposes an optimization that makes a transaction push the records it writes directly to the next transaction that requests the records without going through the storage engine to reduce transaction latency.

Reference:
- Wu, Shan-Hung, et al. "T-part: Partitioning of transactions for forward-pushing in deterministic database systems." Proceedings of the 2016 International Conference on Management of Data. 2016.

### SOCC'10 - G-Store

G-Store is a key-value store that provides an additional protocol to support multi-key access.

Since ElaSQL has already supported multi-key access (transactions), we only implemented the idea of collecting the records on a single master.

Reference:
- Das, Sudipto, Divyakant Agrawal, and Amr El Abbadi. "G-store: a scalable data store for transactional multi key access in the cloud." Proceedings of the 1st ACM symposium on Cloud computing. 2010.

## Data Migrations

### Stop-and-Copy

Stop-and-Copy is a common data migration algorithm that stops the system until a data migration finishes.

### VLDB'11 - Albatross

Albatross is a data migration algorithm that executes incoming requests that access migrating data on the **source** node and migrate data and updates with background threads/processes. It also requires an atomic handover that blocks system service to finish a migration.

Reference:
- Das, Sudipto, et al. "Albatross: Lightweight elasticity in shared storage databases for the cloud using live data migration." Proceedings of the VLDB Endowment 4.8 (2011): 494-505.

### SIGMOD'15 - Squall

Squall is a data migration algorithm that executes incoming requests that access migrating data on the **destination** node. The transactions that touch migrating data help the system transfer the data to the destination node.

Reference:
- Elmore, Aaron J., et al. "Squall: Fine-grained live reconfiguration for partitioned main memory databases." Proceedings of the 2015 ACM SIGMOD International Conference on Management of Data. 2015.

### VLDB'19 - MgCrab

MgCrab is data migration algorithm that executes incoming requests that access migrating data on both the **source** and the **destination** node. The transactions that touch migrating data on the source node can deal with the client requests as soon as possible to make the client feel no additional delay caused by migration. On the other hand, the transaction executing on the destination node can help the system transfer the data.

Reference:
- Lin, Yu-Shan, et al. "MgCrab: transaction crabbing for live migration in deterministic database systems." Proceedings of the VLDB Endowment 12.5 (2019): 597-610.

## Data Re-partitioning

### Clay

Clay is a data re-partitioning planning algorithm. It first collects the workloads in the past and build up a dependency graph based on co-access pattern of records. Then, it generates data partitioning plan by dividing the graph into smaller clumps such that the the number of distributed transactions are minimized and the loads are balanced. Note that Clay is not responsible for performing data migrations, so it needs to employ a data migration mechanism to realize its plan.

Reference:
- Serafini, Marco, et al. "Clay: Fine-grained adaptive partitioning for general database schemas." Proceedings of the VLDB Endowment 10.4 (2016): 445-456.

### SIGMOD'16 - LEAP

LEAP is a data re-partitioning mechanism that migrates data records for each individual transaction. When a transaction collects the records from multiple machine to a single machine (called the master), LEAP transfers not only the data but also the ownerships of the records to the master.

Reference:
- Lin, Qian, et al. "Towards a non-2pc transaction management in distributed database systems." Proceedings of the 2016 International Conference on Management of Data. 2016.

### SIGMOD'21 - Hermes

Hermes is an advanced data re-partitioning mechanism similar to LEAP. However, Hermes not only migrates records for each transaction but also plans how each transaction goes in advance in order to make data partitions always fit future workloads.

Reference:
- Yu-Shan Lin, et al. "Don't Look Back, Look into the Future: Prescient Data Partitioning and Migration for Deterministic Database Systems." Proceedings of the 2021 International Conference on Management of Data. 2021.
