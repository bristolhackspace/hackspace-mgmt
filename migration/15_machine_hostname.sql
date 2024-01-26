ALTER TABLE IF EXISTS public.machine_controller
    ADD COLUMN hostname character varying(255) NOT NULL DEFAULT '';
UPDATE public.machine_controller SET hostname = mac WHERE hostname = '';
ALTER TABLE IF EXISTS public.machine_controller
    ADD UNIQUE (hostname);
ALTER TABLE IF EXISTS public.machine_controller DROP COLUMN IF EXISTS mac;