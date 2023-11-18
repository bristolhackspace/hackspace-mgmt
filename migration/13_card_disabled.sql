ALTER TABLE IF EXISTS public.card
    ADD COLUMN door_disabled boolean NOT NULL DEFAULT false;