# Scripts

This file summaries the scripts to run ElaSQL Bench with runnable JARs.

We assume that all the JARs and properties files are put along with the following scripts.

## Server Script

```bash
java \
-Dorg.elasql.config.file=elasql.properties \
-Dorg.elasql.bench.config.file=elasqlbench.properties \
-Dorg.vanilladb.comm.config.file=vanilladbcomm.properties \
-Dorg.vanilladb.bench.config.file=vanillabench.properties \
-Dorg.vanilladb.core.config.file=vanilladb.properties \
-Djava.util.logging.config.file=logging.properties \
-jar server.jar \
$1 \
$2 \
$3 \
```

## Client Script

```
java \
-Dorg.elasql.config.file=elasql.properties \
-Dorg.elasql.bench.config.file=elasqlbench.properties \
-Dorg.vanilladb.comm.config.file=vanilladbcomm.properties \
-Dorg.vanilladb.bench.config.file=vanillabench.properties \
-Dorg.vanilladb.core.config.file=vanilladb.properties \
-Djava.util.logging.config.file=logging.properties \
-jar client.jar \
$1 \
$2 \
```
