# Arguments

This file summaries the arguments to run ElaSQL-Bench.

## Program Argument

### Servers

```
[DB Name] [Server ID] [Is Sequencer]
```

- `DB Name`: the database name
  - Note that if you run servers on the same machine, each server should have an unique name for their database.
- `Server ID`: the ID of the server process
  - Note that this ID should match the ID in the `vanillacomm.properties`
- `Is Sequencer`: to set if it is running in sequencer mode
  - The server with the greatest ID should turn this ON.

#### Examples

Database server with ID 0 with a database called `db-0`

```
db-0 0 0
```

The sequencer server with server ID 1

```
db-seq 1 1
```

The sequencer will not create any database. The reason that you need to give a database name just because it shares the same main class with database servers. This may be changed soon.

### Client

```
[Client ID] [Load or Benchmark?]
```

- `Client ID`: the ID of the client process
- `Load or Benchmark?`:
  - Set `1` if you want to load a new testbed on a clean database
  - Set `2` for benchmarking on a existing testbed

#### Examples

Running client no.0 with loading procedure

```
0 1
```

## VM Argument

VM arguments tell the system where to find the properties files.

```
-Dorg.elasql.config.file=[Path to elasql.properties]
-Dorg.elasql.bench.config.file=[Path to elasqlbench.properties]
-Dorg.vanilladb.comm.config.file=[Path to vanillacomm.properties]
-Dorg.vanilladb.bench.config.file=[Path to vanillabench.properties]
-Dorg.vanilladb.core.config.file=[Path to vanilladb.properties]
-Djava.util.logging.config.file=[Path to logging.properties]
```

### Examples

If you are setting run configurations in Eclipse:

```
-Dorg.elasql.config.file=target/classes/org/elasql/elasql.properties
-Dorg.elasql.bench.config.file=target/classes/org/elasql/elasqlbench.properties 
-Dorg.vanilladb.comm.config.file=target/classes/org/vanilladb/comm/vanillacomm.properties 
-Dorg.vanilladb.bench.config.file=target/classes/org/vanilladb/bench/vanillabench.properties 
-Dorg.vanilladb.core.config.file=target/classes/org/vanilladb/core/vanilladb.properties 
-Djava.util.logging.config.file=target/classes/java/util/logging/logging.properties
```
