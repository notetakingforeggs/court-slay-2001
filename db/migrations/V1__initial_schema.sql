--
-- PostgreSQL database dump
--

-- Dumped from database version 16.8 (Debian 16.8-1.pgdg120+1)
-- Dumped by pg_dump version 16.8 (Debian 16.8-1.pgdg120+1)

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

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: court; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.court (
    id bigint NOT NULL,
    region_id bigint NOT NULL,
    city character varying(255),
    name character varying(255)
);


--
-- Name: court_case; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.court_case (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid() NOT NULL,
    start_time_epoch bigint NOT NULL,
    court_id bigint NOT NULL,
    case_id character varying(255),
    claimant character varying(255),
    defendant character varying(255),
    duration bigint,
    hearing_channel character varying(255),
    hearing_type character varying(255),
    case_details text,
    created_at bigint,
    is_minor boolean,
    UNIQUE (court_id, case_id, start_time_epoch)
);


--
-- Name: region; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.region (
    id bigint NOT NULL,
    region_name character varying(255)
);


--
-- Name: subscription; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.subscription (
    id bigint NOT NULL,
    alert_terms_claimant character varying(255)[],
    alert_terms_defendant character varying(255)[],
    chat_id bigint,
    last_notified_timestamp bigint
);


--
-- Name: subscription_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.subscription_seq
    START WITH 1
    INCREMENT BY 50
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;



--
-- Name: court court_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.court
    ADD CONSTRAINT court_pkey PRIMARY KEY (id);


--
-- Name: region region_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.region
    ADD CONSTRAINT region_pkey PRIMARY KEY (id);


--
-- Name: subscription subscription_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.subscription
    ADD CONSTRAINT subscription_pkey PRIMARY KEY (id);


--
-- Name: court_case fke8talahhg3bc1d1fn1mh4qid3; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.court_case
    ADD CONSTRAINT fke8talahhg3bc1d1fn1mh4qid3 FOREIGN KEY (court_id) REFERENCES public.court(id);


--
-- Name: court fkobevo31jwin8p5ikblfeupjqd; Type: FK CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.court
    ADD CONSTRAINT fkobevo31jwin8p5ikblfeupjqd FOREIGN KEY (region_id) REFERENCES public.region(id);


--
-- PostgreSQL database dump complete
--

