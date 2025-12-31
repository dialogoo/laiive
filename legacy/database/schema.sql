--
-- PostgreSQL database dump
--

-- Dumped from database version 15.4 (Debian 15.4-2.pgdg120+1)
-- Dumped by pg_dump version 15.4 (Debian 15.4-2.pgdg120+1)

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
-- Name: vector; Type: EXTENSION; Schema: -; Owner: -
--

CREATE EXTENSION IF NOT EXISTS vector WITH SCHEMA public;


--
-- Name: EXTENSION vector; Type: COMMENT; Schema: -; Owner:
--

COMMENT ON EXTENSION vector IS 'vector data type and ivfflat and hnsw access methods';


SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: events; Type: TABLE; Schema: public; Owner: oscar
--

CREATE TABLE public.events (
    id integer NOT NULL,
    event_name text,
    event_name_2 text,
    event_description text,
    event_genre text,
    event_tags text[],
    event_image text,
    event_link text,
    event_date date,
    event_init_hour time without time zone,
    event_end_hour time without time zone,
    event_comments_hour text,
    event_language text,
    event_age_restriction text,
    place_id integer,
    place_name text,
    place_name_2 text,
    place_description text,
    place_address text,
    place_city text,
    place_coordinates point,
    place_link text,
    artist_id integer,
    artist_name text,
    artist_description text,
    artist_summary text,
    artist_link text,
    artist_genres text[],
    artist2_id integer,
    artist2_name text,
    artist2_description text,
    artist2_summary text,
    artist2_link text,
    artist2_genres text[],
    artist3_id integer,
    artist3_name text,
    artist3_description text,
    artist3_summary text,
    artist3_link text,
    artist3_genres text[],
    price_regular numeric(10,2),
    price_discounted1	 numeric(10,2),
    price_discounted1_comments text,
    price_discounted2 numeric(10,2),
    price_discounted2_comments text,
    entrance_link text
);


ALTER TABLE public.events OWNER TO oscar;

--
-- Name: events_id_seq; Type: SEQUENCE; Schema: public; Owner: oscar
--

CREATE SEQUENCE public.events_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER TABLE public.events_id_seq OWNER TO oscar;

--
-- Name: events_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: oscar
--

ALTER SEQUENCE public.events_id_seq OWNED BY public.events.id;


--
-- Name: events id; Type: DEFAULT; Schema: public; Owner: oscar
--

ALTER TABLE ONLY public.events ALTER COLUMN id SET DEFAULT nextval('public.events_id_seq'::regclass);


--
-- Data for Name: events; Type: TABLE DATA; Schema: public; Owner: oscar
--

COPY public.events (id, event_name, event_name_2, place, place_description, address, coordinates, place_link, artist, artist_description, artist_summary, price_reg, price_2, comments_price_2, price_3, comments_price_3, entrance_link, date, init_hour, end_hour, comments_hour, genre, language, age_restriction, tags) FROM stdin;
\.


--
-- Name: events_id_seq; Type: SEQUENCE SET; Schema: public; Owner: oscar
--

SELECT pg_catalog.setval('public.events_id_seq', 1, false);


--
-- Name: events events_pkey; Type: CONSTRAINT; Schema: public; Owner: oscar
--

ALTER TABLE ONLY public.events
    ADD CONSTRAINT events_pkey PRIMARY KEY (id);


--
-- PostgreSQL database dump complete
--
