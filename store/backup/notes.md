# backup

```sh
# logical backup (prompts for password)
pg_dump --host=localhost --port=5432 --username=postgres --dbname=postgres --verbose \
| gzip > ./backup/data/measurement_pg_dump_$(date +"%Y-%m-%d_%H-%M-%S").sql.gz

# unzip + restore
gunzip -c backup/data/measurement_pg_dump_TTTTTTTTTTT.sql.gz > ./backup/data/measurement_pg_dump.sql
psql --host=localhost --port=5432 --username=postgres postgres < ./backup/data/measurement_pg_dump.sql

```
