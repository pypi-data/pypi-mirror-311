# 3) Tutorial -  Understanding the database structure

## Introduction
Datatoolbox does provide a csv-based database like interface that does use git to mangage and 
version control data sets (called "sources" with datatoolbox). Ideally, datatoolbox does manage
all files and folders on the hard disk and manual changes are not required and even unsupported.
Dataoolbox does monitor the internal folder and raises error when detecting manual changes. The
underlying philophosy is to avoide manual changes that are not tracked by the git tracking and 
thus ensure reproducabilty of changes in the dataset. Overall, this should overall allow to 
reproduce analytical results based on given datasets and their fixed version.

The following figure shows the three layers within the data workflow starting from the raw data, 
to the aligned datatable struture, via the local database to the final shared database online.

![](figures/datatoolbox_data_flows.png)

## 1) Data  integration
As done in  the first  two tutorials, always the firsts step is the conversion of  the data  
into the required data fromat  and  aligning to  the  naming  convention. The data is separated
into homogeneous datatables that only consist on variable and with that a set of meta information
for all data values for variable regional and temporal extend.

Please not, that the consisstency in meta data might require to  split data in different datatables, e.g. 
if the same data is switching between historic values to  for example a projection, which should be
indicated in the meta data as different scenarios (historic vs projection), however, the user
itself is adviced to maintain the useful level of consistency. 

## 2) Main repository of the datashelf
The main reposity of the datashelf follows roughtly the following data structure:
```
.
├── database
│   └── [.. indicidual sources ..]
│   └── [.. indicidual sources ..]
├── inventory.csv
├── mappings
│   ├── continent.csv
│   ├── country_codes.csv
│   └── regions.csv
├── rawdata
├── remote_sources
│   └── source_states.csv
└── sources.csv
```
The subfolder "database" does contain folder with indiviual data sources (see next section),
that are combined to one locally available database. For this, the file "sources.csv" does
contain all information about the locally added sources, which includes the meta data of the 
individual sources, the version of the source and its expected git hash.
The "inventory.csv" does contain all tables from all sourcess combined and is used when searching
for specific tables. Each time a source is added, changed or removed, the inventory.csv is updated
to represent the new current database state. Each state is tracked via git commits and.



## 3) Organising data in individual sources (data sets)
Data sets (including all data from on souce and release)  are organized as sources in datatoolbox. Each data set
can contrain an arbitrary number of datatables reflecting different variables and scenario combinations.
In the background, datatoolbox does create a git repository for each new source, that has its own meta data,
inventory of datatables and  is versioned using git.

```
import datatoolbox as  dt
dt.admin.switch_database_to_testing()
print(dt.core.DB._get_source_path('Numbers_2022'))
```

Each source directory does follow the same file structure including a csv for the meta data, 
a source_inventory csv file and a folder containing the individual datatable csv.

```
.
├── meta.csv
├── raw_data
├── source_inventory.csv
└── tables
    ├── Numbers-Fives__Historic__Numbers_2020.csv
    └── Numbers-Ones__Historic__Numbers_2020.csv````
```


## 4) Sharing data sources with other users
Datatoolbox does monitor dataset versions locally and in the shared online repository using 
tags. The following functionality allow to check for new data sources, identify updated data and
allows to contrinbute and share new data or updates.

To check for new data "dt.available_remote_data_updates()" shows to tables, one showing all 
new items that are available online, but are not in the local database. The second, showing
datasets of which a newer version is available online by another contributer. For updated 
data sources, the local and remote tag are displayed.

```
dt.available_remote_data_updates()

New items:
+--------------------------------------+-------+------------------+
|                                      | tag   | last_to_update   |
|--------------------------------------+-------+------------------|
| NEW_DATA_2024                        | v1.0  | Contributer      |
+--------------------------------------+-------+------------------+
Sources with newer data:
+-----------------------+-------------+--------------+
| SOURCE_ID             | local_tag   | remote_tag   |
|-----------------------+-------------+--------------|
| UPDATED_DATASET_2023  | v1.0        | v2.0         |
+-----------------------+-------------+--------------+
```

To update a local data source from the remote dt.pull_source_from_remote() is used with the 
source ID as the only parameter


```
 dt.pull_source_from_remote(source_ID)
 
```


In order to push a updated version to the remote shared database, use the following command:
```
dt.push_source_to_remote(source_ID)
```

For specific available version of a specifc source and also a specific version can
be integrated. Therefore, the specific verision e.g. v1.0 is provided or "latest" for the
newest version. 
```
dt.list_source_versions(source_ID)

dt.checkout_source_version(source_ID: tag = "v1.0")

dt.checkout_source_version(ssource_ID str, tag = "latest")
```

In general, datatoolbox is envisioned that no manual changes in the data folder is 
required by the user. Even more, datatoolbox checking that the database is in a
healthy state, to ensure that compuations that rely on data from the database
are reproducable. In order to to this, datatoolbox will raise Exceptions in
serveral occations:
 - Local changes in the main repository

## 5) Fixing errors in the database
When using data from the datashelf, datatoolbox verifies that the individual 
database git states do match the once listed in the overall repository. Thus, some 
incidence, local changes or bug might break the consistency of the databases . The following
issues might arries that will make datatoolbox stop working or prevent access to individual 
data sources:
- Uncommited changes in the main repository or individual source repositories
- Different git hash of a local data source than in the main sources.csv
- Errorenous table meta in "inventory.csv"

For some errors, dt.admin does offer some limited solution strategies:

```
dt.admin.fix_brocken_DB(sourceID, how):

    how = "commmit_source_changes" # commits all changes in source and integrates new hash in main
    # Only reverts all local changes in source repo using "git reset --hard"  

    how = "reset_source_revision":
    # Resets source to version in main repository.


    how == "fix_sources_inventory": 
    # Restores the data respository based on the last working git hash in the inventory file.
    # After a successfulr restorations, datatoolbox need to be imported from scratch. For notebooks
    # the restart of the python kernel might be required.


```

