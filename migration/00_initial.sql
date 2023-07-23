--
-- PostgreSQL database dump
--

-- Dumped from database version 13.10 (Debian 13.10-0+deb11u1)
-- Dumped by pg_dump version 14.3

-- Started on 2023-07-23 14:54:27 BST

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
-- TOC entry 3 (class 2615 OID 2200)
-- Name: public; Type: SCHEMA; Schema: -; Owner: -
--

CREATE SCHEMA public;


--
-- TOC entry 3046 (class 0 OID 0)
-- Dependencies: 3
-- Name: SCHEMA public; Type: COMMENT; Schema: -; Owner: -
--

COMMENT ON SCHEMA public IS 'standard public schema';


--
-- TOC entry 653 (class 1247 OID 16465)
-- Name: discourse_invite; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.discourse_invite AS ENUM (
    'no',
    'invited',
    'expired',
    'accepted'
);


--
-- TOC entry 632 (class 1247 OID 16388)
-- Name: induction_state; Type: TYPE; Schema: public; Owner: -
--

CREATE TYPE public.induction_state AS ENUM (
    'valid',
    'expired',
    'banned'
);


SET default_table_access_method = heap;

--
-- TOC entry 203 (class 1259 OID 16414)
-- Name: card; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.card (
    id integer NOT NULL,
    card_serial bigint,
    number_on_front integer,
    member_id integer,
    lost boolean DEFAULT false NOT NULL
);


--
-- TOC entry 202 (class 1259 OID 16412)
-- Name: card_id_seq; Type: SEQUENCE; Schema: public; Owner: -
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
-- TOC entry 209 (class 1259 OID 16451)
-- Name: induction; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.induction (
    id integer NOT NULL,
    member_id integer NOT NULL,
    machine_id integer NOT NULL,
    state public.induction_state NOT NULL,
    inducted_by integer,
    inducted_on date DEFAULT now()
);


--
-- TOC entry 208 (class 1259 OID 16449)
-- Name: induction_id_seq; Type: SEQUENCE; Schema: public; Owner: -
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
-- TOC entry 205 (class 1259 OID 16425)
-- Name: machine; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine (
    id integer NOT NULL,
    name character varying(255) NOT NULL
);


--
-- TOC entry 207 (class 1259 OID 16437)
-- Name: machine_controller; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.machine_controller (
    id integer NOT NULL,
    mac bigint,
    machine_id integer,
    requires_update boolean NOT NULL
);


--
-- TOC entry 206 (class 1259 OID 16435)
-- Name: machine_controller_id_seq; Type: SEQUENCE; Schema: public; Owner: -
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
-- TOC entry 204 (class 1259 OID 16423)
-- Name: machine_id_seq; Type: SEQUENCE; Schema: public; Owner: -
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
-- TOC entry 200 (class 1259 OID 16395)
-- Name: member; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.member (
    id integer NOT NULL,
    first_name character varying(80) NOT NULL,
    last_name character varying(80),
    discourse_id integer,
    discourse public.discourse_invite DEFAULT 'no'::public.discourse_invite NOT NULL,
    mailchimp boolean DEFAULT false NOT NULL,
    email character varying(300),
    alt_email character varying(300),
    payment_ref character varying(200),
    join_date date DEFAULT CURRENT_DATE NOT NULL,
    end_date date,
    end_reason character varying(500),
    address1 character varying(200),
    address2 character varying(200),
    town_city character varying(200),
    county character varying(200),
    postcode character varying(20),
    payment_active boolean DEFAULT false NOT NULL,
    notes text
);


--
-- TOC entry 201 (class 1259 OID 16406)
-- Name: member_data_id_seq; Type: SEQUENCE; Schema: public; Owner: -
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
-- TOC entry 2893 (class 2606 OID 16420)
-- Name: card card_card_serial_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_card_serial_key UNIQUE (card_serial);


--
-- TOC entry 2895 (class 2606 OID 16422)
-- Name: card card_number_on_front_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_number_on_front_key UNIQUE (number_on_front);


--
-- TOC entry 2897 (class 2606 OID 16418)
-- Name: card card_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_pkey PRIMARY KEY (id);


--
-- TOC entry 2905 (class 2606 OID 16455)
-- Name: induction induction_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_pkey PRIMARY KEY (id);


--
-- TOC entry 2901 (class 2606 OID 16443)
-- Name: machine_controller machine_controller_mac_key; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_controller
    ADD CONSTRAINT machine_controller_mac_key UNIQUE (mac);


--
-- TOC entry 2903 (class 2606 OID 16441)
-- Name: machine_controller machine_controller_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_controller
    ADD CONSTRAINT machine_controller_pkey PRIMARY KEY (id);


--
-- TOC entry 2899 (class 2606 OID 16429)
-- Name: machine machine_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine
    ADD CONSTRAINT machine_pkey PRIMARY KEY (id);


--
-- TOC entry 2891 (class 2606 OID 16399)
-- Name: member member_data_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.member
    ADD CONSTRAINT member_data_pkey PRIMARY KEY (id);


--
-- TOC entry 2906 (class 2606 OID 24654)
-- Name: card card_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.card
    ADD CONSTRAINT card_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id) NOT VALID;


--
-- TOC entry 2910 (class 2606 OID 24664)
-- Name: induction induction_inducted_by_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_inducted_by_fkey FOREIGN KEY (inducted_by) REFERENCES public.member(id) ON UPDATE CASCADE ON DELETE SET NULL NOT VALID;


--
-- TOC entry 2908 (class 2606 OID 16456)
-- Name: induction induction_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(id) ON UPDATE RESTRICT ON DELETE RESTRICT;


--
-- TOC entry 2909 (class 2606 OID 24659)
-- Name: induction induction_member_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.induction
    ADD CONSTRAINT induction_member_id_fkey FOREIGN KEY (member_id) REFERENCES public.member(id) ON UPDATE RESTRICT ON DELETE RESTRICT NOT VALID;


--
-- TOC entry 2907 (class 2606 OID 16444)
-- Name: machine_controller machine_controller_machine_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.machine_controller
    ADD CONSTRAINT machine_controller_machine_id_fkey FOREIGN KEY (machine_id) REFERENCES public.machine(id) ON UPDATE CASCADE ON DELETE SET NULL;


-- Completed on 2023-07-23 14:54:28 BST

--
-- PostgreSQL database dump complete
--

