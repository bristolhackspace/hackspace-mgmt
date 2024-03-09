CREATE TYPE public.legacy_machine_auth AS ENUM (
    'none',
    'password',
    'padlock'
);

ALTER TABLE IF EXISTS public.machine
    ADD COLUMN legacy_auth public.legacy_machine_auth NOT NULL DEFAULT 'none'::public.legacy_machine_auth;

ALTER TABLE IF EXISTS public.machine
    ADD COLUMN legacy_password NOT NULL character varying(255);