select
    id
    , timestamp as created_on
    , user_profile_p_k as user_id
    , sleep_time_seconds
    , nap_time_seconds
    , unmeasurable_sleep_seconds
    , deep_sleep_seconds
    , light_sleep_seconds
    , rem_sleep_seconds
    , awake_sleep_seconds
    , average_sp_o2_value
    , lowest_sp_o2_value
    , highest_sp_o2_value
    , average_sp_o2_h_r_sleep
    , average_respiration_value
    , lowest_respiration_value
    , highest_respiration_value
    , awake_count
    , avg_sleep_stress
    , age_group
    , sleep_score_feedback
    , sleep_start_datetime
    , sleep_end_datetime
    , restless_moments_count
from public.raw_sleep_facts
