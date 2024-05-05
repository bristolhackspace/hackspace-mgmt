--
-- PostgreSQL database dump
--

-- Dumped from database version 15.6 (Debian 15.6-1.pgdg120+2)
-- Dumped by pg_dump version 15.6 (Debian 15.6-0+deb12u1)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: discourse_invite; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.discourse_invite AS ENUM (
    'no',
    'invited',
    'emailed',
    'accepted',
    'alumni'
);


ALTER TYPE public.discourse_invite OWNER TO postgres;

--
-- Name: induction_state; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.induction_state AS ENUM (
    'valid',
    'expired',
    'banned'
);


ALTER TYPE public.induction_state OWNER TO postgres;

--
-- Name: legacy_machine_auth; Type: TYPE; Schema: public; Owner: postgres
--

CREATE TYPE public.legacy_machine_auth AS ENUM (
    'none',
    'password',
    'padlock'
);


ALTER TYPE public.legacy_machine_auth OWNER TO postgres;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: card; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.card (
    id integer NOT NULL,
    card_serial bigint,
    number_on_front integer,
    member_id integer,
    lost boolean DEFAULT false NOT NULL,
    unverified_serial bigint,
    door_disabled boolean DEFAULT false NOT NULL
);


ALTER TABLE public.card OWNER TO postgres;

--
-- Name: card_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.card ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.card_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: induction; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.induction (
    id integer NOT NULL,
    member_id integer NOT NULL,
    machine_id integer NOT NULL,
    state public.induction_state NOT NULL,
    inducted_by integer,
    inducted_on date DEFAULT now(),
    can_induct boolean DEFAULT false NOT NULL
);


ALTER TABLE public.induction OWNER TO postgres;

--
-- Name: induction_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.induction ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.induction_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: label; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.label (
    id integer NOT NULL,
    member_id integer,
    expiry date NOT NULL,
    caption character varying(255) NOT NULL,
    printed boolean DEFAULT false NOT NULL
);


ALTER TABLE public.label OWNER TO postgres;

--
-- Name: label_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.label ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.label_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: machine; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.machine (
    id integer NOT NULL,
    name character varying(255) NOT NULL,
    legacy_auth public.legacy_machine_auth DEFAULT 'none'::public.legacy_machine_auth NOT NULL,
    legacy_password character varying(255) DEFAULT ''::character varying NOT NULL,
    hide_from_home boolean DEFAULT false NOT NULL
);


ALTER TABLE public.machine OWNER TO postgres;

--
-- Name: machine_controller; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.machine_controller (
    id integer NOT NULL,
    machine_id integer,
    requires_update boolean NOT NULL,
    powered boolean DEFAULT false NOT NULL,
    idle_timeout integer DEFAULT '-1'::integer NOT NULL,
    idle_power_threshold integer DEFAULT 50 NOT NULL,
    invert_logout_button boolean DEFAULT false NOT NULL,
    hostname character varying(255) DEFAULT ''::character varying NOT NULL
);


ALTER TABLE public.machine_controller OWNER TO postgres;

--
-- Name: machine_controller_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.machine_controller ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.machine_controller_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: machine_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.machine ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.machine_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: member; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.member (
    id integer NOT NULL,
    first_name character varying(80) NOT NULL,
    last_name character varying(80),
    discourse_id integer,
    discourse public.discourse_invite DEFAULT 'no'::public.discourse_invite NOT NULL,
    newsletter boolean DEFAULT false NOT NULL,
    email character varying(300),
    alt_email character varying(300),
    payment_ref character varying(200),
    join_date date DEFAULT CURRENT_DATE NOT NULL,
    end_date date,
    end_reason character varying(500),
    address1 character varying(200) DEFAULT ''::character varying NOT NULL,
    address2 character varying(200) DEFAULT ''::character varying NOT NULL,
    town_city character varying(200) DEFAULT ''::character varying NOT NULL,
    county character varying(200) DEFAULT ''::character varying NOT NULL,
    postcode character varying(20) DEFAULT ''::character varying NOT NULL,
    payment_active boolean DEFAULT false NOT NULL,
    notes text,
    preferred_name character varying(160),
    welcome_email_sent boolean DEFAULT false NOT NULL
);


ALTER TABLE public.member OWNER TO postgres;

--
-- Name: member_data_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.member ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.member_data_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: quiz; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.quiz (
    id integer NOT NULL,
    title character varying(200) NOT NULL,
    description text,
    questions text NOT NULL,
    machine_id integer,
    intro text DEFAULT ''::text NOT NULL,
    hidden boolean DEFAULT false NOT NULL
);


ALTER TABLE public.quiz OWNER TO postgres;

--
-- Name: quiz_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

ALTER TABLE public.quiz ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.quiz_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
0f17df0ee1a8
\.


--
-- Data for Name: card; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.card (id, card_serial, number_on_front, member_id, lost, unverified_serial, door_disabled) FROM stdin;
1	2864434397	111	\N	f	\N	f
2	1122867	112	\N	f	\N	f
3	2882351791	113	\N	f	\N	f
4	0	100	7	f	\N	f
\.


--
-- Data for Name: induction; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.induction (id, member_id, machine_id, state, inducted_by, inducted_on, can_induct) FROM stdin;
1	7	2	valid	\N	2024-04-25	f
\.


--
-- Data for Name: label; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.label (id, member_id, expiry, caption, printed) FROM stdin;
\.


--
-- Data for Name: machine; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.machine (id, name, legacy_auth, legacy_password, hide_from_home) FROM stdin;
1	Machine 1	none		f
2	Machine 2	padlock	1234	f
3	Hidden Machine	none		t
\.


--
-- Data for Name: machine_controller; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.machine_controller (id, machine_id, requires_update, powered, idle_timeout, idle_power_threshold, invert_logout_button, hostname) FROM stdin;
1	1	f	f	-1	50	f	aabbccdd
2	2	f	f	-1	50	f	eeff0011
\.


--
-- Data for Name: member; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.member (id, first_name, last_name, discourse_id, discourse, newsletter, email, alt_email, payment_ref, join_date, end_date, end_reason, address1, address2, town_city, county, postcode, payment_active, notes, preferred_name, welcome_email_sent) FROM stdin;
1	Elliot	Fisher	\N	no	f	elliotf@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
2	Donte	Huang	\N	no	f	donte-huang@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
3	Leo	Gates	\N	no	f	leog@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
4	Annika	Arellano	\N	no	f	aarellano@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
5	Samson	Roth	\N	no	f	sroth@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
6	Quinn	Nobel	\N	no	f	quinnn@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
7	Example	User	\N	no	f	example@example.com	\N	\N	2024-04-25	\N	\N						f	\N	\N	f
\.


--
-- Data for Name: quiz; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.quiz (id, title, description, questions, machine_id, intro, hidden) FROM stdin;
1	Machine 1 Quiz	Quiz for the first machine	q1:\r\n  type: pick_one\r\n  correct_answer: a1\r\n  label: Select the correct answer\r\n  answers:\r\n    a1: This is correct\r\n    a2: This is wrong\r\n    a3: This is also wrong\r\nq2:\r\n  type: select_all\r\n  correct_answers: ["a1", "a2"]\r\n  label: Select the correct answers\r\n  answers:\r\n    a1: This is correct\r\n    a2: This is also correct\r\n    a3: This is wrong\r\nq3:\r\n  type: yes_no\r\n  correct_answer: yes\r\n  label: You must tick this answer.	1	Welcome to the example quiz. Here's some different question types.	f
\.


--
-- Name: card_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.card_id_seq', 4, true);


--
-- Name: induction_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.induction_id_seq', 1, true);


--
-- Name: label_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.label_id_seq', 1, false);


--
-- Name: machine_controller_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.machine_controller_id_seq', 2, true);


--
-- Name: machine_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.machine_id_seq', 3, true);


--
-- Name: member_data_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.member_data_id_seq', 7, true);


--
-- Name: quiz_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.quiz_id_seq', 1, true);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: card card_card_serial_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_card_serial_key UNIQUE (card_serial);


--
-- Name: card card_number_on_front_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_number_on_front_key UNIQUE (number_on_front);


--
-- Name: card card_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- Name: induction induction_member_id_machine_id_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_member_id_machine_id_key UNIQUE (member_id, machine_id);


--
-- Name: induction induction_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_pkey PRIMARY KEY (id);


--
-- Name: label label_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label
    ADD CONSTRAINT label_pkey PRIMARY KEY (id);


--
-- Name: machine_controller machine_controller_hostname_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machine_controller
    ADD CONSTRAINT machine_controller_hostname_key UNIQUE (hostname);


--
-- Name: machine_controller machine_controller_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machine_controller
    ADD CONSTRAINT machine_controller_pkey PRIMARY KEY (id);


--
-- Name: machine machine_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_pkey PRIMARY KEY (id);


--
-- Name: member member_data_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_data_pkey PRIMARY KEY (id);


--
-- Name: quiz quiz_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz
    ADD CONSTRAINT quiz_pkey PRIMARY KEY (id);


--
-- Name: card card_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id) NOT VALID;


--
-- Name: induction induction_inducted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_inducted_by_fkey FOREIGN KEY (inducted_by) REFERENCES public.member(id) ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- Name: induction induction_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- Name: induction induction_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id) ON UPDATE RESTRICT ON DELETE RESTRICT NOT VALID;


--
-- Name: label label_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.label
    ADD CONSTRAINT label_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: machine_controller machine_controller_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.machine_controller
    ADD CONSTRAINT machine_controller_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- Name: quiz quiz_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.quiz
    ADD CONSTRAINT quiz_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(id) ON UPDATE CASCADE ON DELETE SET NULL;


--
-- PostgreSQL database dump complete
--

