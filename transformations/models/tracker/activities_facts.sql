select
    id
    , owner_id as user_id
    , sport_type_id as sport_id
    , start_time_local
    , distance
    , duration
    , elapsed_duration
    , moving_duration
    , average_speed
    , max_speed
    , calories
    , bmr_calories
    , average_h_r
    , max_h_r
    , steps
    , strokes
    , water_estimated
    , average_running_cadence_in_steps_per_minute
    , max_running_cadence_in_steps_per_minute
    , average_swim_cadence_in_strokes_per_minute
    , max_swim_cadence_in_strokes_per_minute
    , average_swolf
    , active_lengths
    , pool_length
    , avg_strokes
    , min_strokes
    , moderate_intensity_minutes
    , vigorous_intensity_minutes
from public.raw_activities_facts
