ALTER TABLE IF EXISTS public.quiz
    ADD COLUMN intro text NOT NULL DEFAULT '';

ALTER TABLE IF EXISTS public.quiz
    ADD COLUMN hidden boolean NOT NULL DEFAULT false;