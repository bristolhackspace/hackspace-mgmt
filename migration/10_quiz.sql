CREATE TABLE public.quiz
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    title character varying(200) NOT NULL,
    description text,
    questions text NOT NULL,
    machine_id integer,
    PRIMARY KEY (id),
    FOREIGN KEY (machine_id)
        REFERENCES public.machine (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE SET NULL
        NOT VALID
);