select
    distinct user_profile_id as id
    , user_fullname as name
from
    public.raw_overview_facts
