CREATE TABLE public.label
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    member_id integer,
    expiry date NOT NULL,
    caption character varying(255) NOT NULL,
    printed boolean NOT NULL DEFAULT false,
    PRIMARY KEY (id),
    FOREIGN KEY (member_id)
        REFERENCES public.member (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
        NOT VALID
);