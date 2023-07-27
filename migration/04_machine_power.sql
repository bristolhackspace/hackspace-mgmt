ALTER TABLE IF EXISTS public.machine_controller
    ADD COLUMN powered boolean NOT NULL DEFAULT false;