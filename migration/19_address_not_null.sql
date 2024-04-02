UPDATE public.member SET address1 = '' where address1 IS NULL;

UPDATE public.member SET address2 = '' where address2 IS NULL;

UPDATE public.member SET town_city = '' where town_city IS NULL;

UPDATE public.member SET county = '' where county IS NULL;

UPDATE public.member SET postcode = '' where postcode IS NULL;

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN address1 SET DEFAULT '';

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN address1 SET NOT NULL;

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN address2 SET DEFAULT '';

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN address2 SET NOT NULL;

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN town_city SET DEFAULT '';

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN town_city SET NOT NULL;

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN county SET DEFAULT '';

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN county SET NOT NULL;

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN postcode SET DEFAULT '';

ALTER TABLE IF EXISTS public.member
    ALTER COLUMN postcode SET NOT NULL;