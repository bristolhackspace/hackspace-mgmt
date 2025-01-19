CREATE TABLE public.quiz_completion
(
    id integer NOT NULL GENERATED ALWAYS AS IDENTITY,
    quiz_id integer NOT NULL,
    member_id integer NOT NULL,
    completed_on timestamp without time zone NOT NULL DEFAULT now(),
    PRIMARY KEY (id),
    FOREIGN KEY (quiz_id)
        REFERENCES public.quiz (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID,
    FOREIGN KEY (member_id)
        REFERENCES public.member (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
        NOT VALID
);

INSERT INTO quiz_completion(quiz_id, member_id, completed_on) SELECT quiz.id, member_id, inducted_on FROM induction INNER JOIN quiz ON induction.machine_id = quiz.machine_id WHERE inducted_by is NULL;

CREATE TABLE public.machine_quiz
(
    machine_id integer NOT NULL,
    quiz_id integer NOT NULL,
    PRIMARY KEY (machine_id, quiz_id),
    FOREIGN KEY (machine_id)
        REFERENCES public.machine (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID,
    FOREIGN KEY (quiz_id)
        REFERENCES public.quiz (id) MATCH SIMPLE
        ON UPDATE CASCADE
        ON DELETE CASCADE
        NOT VALID
);

INSERT INTO machine_quiz(machine_id, quiz_id) SELECT machine_id, id FROM quiz WHERE machine_id is not NULL;