ALTER TABLE IF EXISTS public.member
    ADD COLUMN welcome_email_sent boolean NOT NULL DEFAULT true;

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN welcome_email_sent SET DEFAULT false;