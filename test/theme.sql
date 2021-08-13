UPDATE twitch.sound_effects s SET user_id = u.id FROM twitch.user_info u where s.sound_name = lower(u.username);


