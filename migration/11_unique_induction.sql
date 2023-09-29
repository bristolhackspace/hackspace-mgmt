ALTER TABLE IF EXISTS public.induction
    ADD UNIQUE (member_id, machine_id);