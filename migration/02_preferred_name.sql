ALTER TABLE IF EXISTS public.member DROP COLUMN IF EXISTS preferred_last_name;

ALTER TABLE IF EXISTS public.member
    RENAME preferred_first_name TO preferred_name;

ALTER TABLE public.member
    ALTER COLUMN preferred_name TYPE character varying(160) COLLATE pg_catalog."default";