ALTER TABLE IF EXISTS public.machine
    ADD COLUMN induction_valid_for_days integer NOT NULL DEFAULT 0;

ALTER TABLE IF EXISTS public.quiz
    ADD COLUMN valid_for_days integer NOT NULL DEFAULT 0;