{{
config(
    materialized='table'
)
}}
select
    distinct sport_type_id as id
    , type_key as key
    , activity_name as name
from public.raw_activities_facts
