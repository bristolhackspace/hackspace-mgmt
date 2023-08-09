ALTER TABLE IF EXISTS public.machine_controller
    ADD COLUMN idle_timeout integer NOT NULL DEFAULT -1;

ALTER TABLE IF EXISTS public.machine_controller
    ADD COLUMN idle_power_threshold integer NOT NULL DEFAULT 50;

ALTER TABLE IF EXISTS public.machine_controller
    ADD COLUMN invert_logout_button boolean NOT NULL DEFAULT false;