ALTER TABLE IF EXISTS public.machine_controller
    ADD COLUMN hostname  NOT NULL character varying(255);
ALTER TABLE IF EXISTS public.machine_controller
    ADD UNIQUE (hostname);
ALTER TABLE IF EXISTS public.machine_controller DROP COLUMN IF EXISTS mac;