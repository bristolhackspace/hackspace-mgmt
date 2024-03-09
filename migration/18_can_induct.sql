ALTER TABLE IF EXISTS public.induction
    ADD COLUMN can_induct boolean NOT NULL DEFAULT false;