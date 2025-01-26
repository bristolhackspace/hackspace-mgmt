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

INSERT INTO public.audit_log(logged_at, category, event, member_id, data) SELECT completed_on, 'quiz', 'import', member_id, json_build_object('quiz_id', quiz_id) FROM public.quiz_completion
ORDER BY id ASC;