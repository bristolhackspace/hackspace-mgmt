ALTER TABLE IF EXISTS public.member
    ADD COLUMN preferred_first_name character varying(80);

ALTER TABLE IF EXISTS public.member
    ADD COLUMN preferred_last_name character varying(80);