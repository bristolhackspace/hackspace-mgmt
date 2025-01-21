CREATE TABLE public.audit_log
(
    id bigint NOT NULL GENERATED ALWAYS AS IDENTITY,
    logged_at timestamp without time zone NOT NULL,
    category character varying NOT NULL,
    event character varying NOT NULL,
    member_id integer,
    data jsonb,
    PRIMARY KEY (id),
    FOREIGN KEY (member_id)
        REFERENCES public.member (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

CREATE INDEX ON public.audit_log USING brin (logged_at);