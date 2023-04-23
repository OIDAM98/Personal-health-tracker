select
    ov.user_id as user_id
    , u.name as user_name
    , ov.created_on as created_on
    , ov.total_kilocalories
    , ov.total_steps
    , ov.daily_step_goal
    , ov.total_stress_duration
    , ov.stress_qualifier
    , ov.average_spo2
    , ROUND(CAST(ov.weight as numeric) / 1000.00, 2) weight_kg
    , ov.bmi
    , ov.metabolic_age
    , ROUND(sl.sleep_time_seconds / 3600.00, 2) as sleep_hours
    , sl.average_sp_o2_h_r_sleep as avg_spo2_sleep
    , sl.avg_sleep_stress
    , sl.age_group
    , sl.sleep_score_feedback
    , sl.sleep_start_datetime
    , sl.sleep_end_datetime
    , sl.restless_moments_count as sleep_restless_moments_count
    , count(af.id) as exercises_in_day
from {{ schema }}.overview_facts as ov
left join {{ schema }}.sleep_facts as sl ON ov.created_on::DATE = sl.created_on::DATE AND ov.user_id = sl.user_id
left join {{ schema }}.activities_facts as af ON af.start_time_local::DATE = ov.created_on::DATE AND ov.user_id = af.user_id
left join {{ schema }}.users as u ON ov.user_id = u.id
group by
    ov.user_id
    , u.name
    , ov.created_on
    , ov.total_kilocalories
    , ov.total_steps
    , ov.daily_step_goal
    , ov.average_stress_level
    , ov.total_stress_duration
    , ov.stress_qualifier
    , ov.average_spo2
    , ov.weight
    , ov.bmi
    , ov.metabolic_age
    , sl.sleep_time_seconds
    , sl.average_sp_o2_h_r_sleep
    , sl.avg_sleep_stress
    , sl.age_group
    , sl.sleep_score_feedback
    , sl.sleep_start_datetime
    , sl.sleep_end_datetime
    , sl.restless_moments_count
