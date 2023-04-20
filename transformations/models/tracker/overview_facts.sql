{{
config(
 materialized='incremental',
 unique_key='id'
)
}}

select
       id
       , timestamp as created_on
       , user_profile_id as user_id
       , total_kilocalories
       , active_kilocalories
       , bmr_kilocalories
       , wellness_kilocalories
       , total_steps
       , total_distance_meters
       , wellness_distance_meters
       , wellness_active_kilocalories
       , daily_step_goal
       , highly_active_seconds
       , active_seconds
       , sedentary_seconds
       , sleeping_seconds
       , moderate_intensity_minutes
       , vigorous_intensity_minutes
       , floors_ascended_in_meters
       , floors_descended_in_meters
       , intensity_minutes_goal
       , min_heart_rate
       , max_heart_rate
       , resting_heart_rate
       , max_stress_level
       , average_stress_level
       , stress_duration
       , rest_stress_duration
       , activity_stress_duration
       , uncategorized_stress_duration
       , total_stress_duration
       , low_stress_duration
       , medium_stress_duration
       , high_stress_duration
       , stress_qualifier
       , body_battery_charged_value
       , body_battery_drained_value
       , body_battery_highest_value
       , body_battery_lowest_value
       , average_spo2
       , lowest_spo2
       , avg_waking_respiration_value
       , highest_respiration_value
       , lowest_respiration_value
       , weight
       , bmi
       , metabolic_age
    FROM public.raw_overview_facts

{% if is_incremental() %}

   where timestamp >= (select max(timestamp) from public.raw_overview_facts)

{% endif %}
