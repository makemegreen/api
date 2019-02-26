# Make Me Green
Repo for makemegreen API

## Pour se connecter à l'API:

curl -O https://cli-dl.scalingo.io/install && bash install
scalingo -a [app_name] pgsql-console


## Pour importer les recommendations en base
Ouvrir un container scalingo :
scalingo -a makemegreen-api run bash
Puis :
PYTHONPATH=. python scripts/makemegreen.py import_reco -f all_reco.csv