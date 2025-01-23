ALTER TABLE IF EXISTS public.machine
    ADD COLUMN requires_in_person boolean NOT NULL DEFAULT false;

ALTER TABLE IF EXISTS public.induction DROP COLUMN IF EXISTS state;

DROP TYPE IF EXISTS public.induction_state;

ALTER TABLE public.induction
    ALTER COLUMN inducted_on TYPE timestamp without time zone;

DELETE FROM public.induction
	WHERE inducted_by is NULL;