# upload-files

# Installation

```shell
# install the dependencies
poetry install
```

```shell
# Up the localstack container
docker compose -f infra/compose.yml up -d
```

```shell
# initialize terraform plan
tflocal -chdir=./infra/terraform init

# apply terraform plan
tflocal -chdir=./infra/terraform apply -auto-approve
```
