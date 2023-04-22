Welcome to your new dbt project!

### Using the starter project

Try running the following commands:
- dbt run
- dbt test

### Using the Profiles YAML

Copy the `profiles-tmpl.yml` file into `~/.dbt/profiles.yml` for DBT to have information regarding the connections of this project.

You could also include this into `~/.dbt/profiles.yml`

``` yaml
healttracker:
  outputs:

    dev:
      type: postgres
      threads: 1
      host: ${HOST}
      port: ${PORT}
      user: ${USER}
      pass: ${PASSWORD}
      dbname: healthtracker
      schema: bronze

    prod:
      type: postgres
      threads: 1
      host: ${HOST}
      port: ${PORT}
      user: ${USER}
      pass: ${PASSWORD}
      dbname: healthtracker
      schema: prod

  target: dev
```

In both cases, put the correct values into the placeholders.

### Deployments

Deployment for default environment (this case `dev`)

``` sh
dbt run
```

Deployment for production environment

``` sh
dbt run -t prod
```
