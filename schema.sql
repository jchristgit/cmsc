--
-- PostgreSQL database dump
--

-- Dumped from database version 14.0
-- Dumped by pg_dump version 14.0

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
-- Name: collection; Type: TABLE; Schema: public; Owner: cmsc
--

CREATE TABLE public.collection (
    id integer NOT NULL,
    day date DEFAULT CURRENT_DATE NOT NULL
);


ALTER TABLE public.collection OWNER TO "cmsc";

--
-- Name: collection_id_seq; Type: SEQUENCE; Schema: public; Owner: cmsc
--

ALTER TABLE public.collection ALTER COLUMN id ADD GENERATED ALWAYS AS IDENTITY (
    SEQUENCE NAME public.collection_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1
);


--
-- Name: subreddit; Type: TABLE; Schema: public; Owner: cmsc
--

CREATE TABLE public.subreddit (
    name character varying(100) NOT NULL,
    invite_code character varying(20),
    enabled boolean DEFAULT true
);


ALTER TABLE public.subreddit OWNER TO "cmsc";

--
-- Name: COLUMN subreddit.invite_code; Type: COMMENT; Schema: public; Owner: cmsc
--

COMMENT ON COLUMN public.subreddit.invite_code IS 'Discord invite code for the subreddit, if known';


--
-- Name: COLUMN subreddit.enabled; Type: COMMENT; Schema: public; Owner: cmsc
--

COMMENT ON COLUMN public.subreddit.enabled IS 'Whether to include the subreddit in collections';


--
-- Name: subscriber_count; Type: TABLE; Schema: public; Owner: cmsc
--

CREATE TABLE public.subscriber_count (
    collection_id integer NOT NULL,
    subreddit character varying(100) NOT NULL,
    count integer NOT NULL,
    CONSTRAINT subscriber_count_count_check CHECK ((count >= 0))
);


ALTER TABLE public.subscriber_count OWNER TO "cmsc";

--
-- Name: TABLE subscriber_count; Type: COMMENT; Schema: public; Owner: cmsc
--

COMMENT ON TABLE public.subscriber_count IS 'Subscriber counts collected in a run';


--
-- Name: collection collection_pkey; Type: CONSTRAINT; Schema: public; Owner: cmsc
--

ALTER TABLE ONLY public.collection
    ADD CONSTRAINT collection_pkey PRIMARY KEY (id);


--
-- Name: subreddit subreddit_pkey; Type: CONSTRAINT; Schema: public; Owner: cmsc
--

ALTER TABLE ONLY public.subreddit
    ADD CONSTRAINT subreddit_pkey PRIMARY KEY (name);


--
-- Name: subscriber_count subscriber_count_collection_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cmsc
--

ALTER TABLE ONLY public.subscriber_count
    ADD CONSTRAINT subscriber_count_collection_id_fkey FOREIGN KEY (collection_id) REFERENCES public.collection(id);


--
-- Name: subscriber_count subscriber_count_subreddit_fkey; Type: FK CONSTRAINT; Schema: public; Owner: cmsc
--

ALTER TABLE ONLY public.subscriber_count
    ADD CONSTRAINT subscriber_count_subreddit_fkey FOREIGN KEY (subreddit) REFERENCES public.subreddit(name);


--
-- PostgreSQL database dump complete
--

