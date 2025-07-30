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
    price_discounted1 numeric(10,2),
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

COPY public.events (id, event_name, event_name_2, event_description, event_genre, event_tags, event_image, event_link, event_date, event_init_hour, event_end_hour, event_comments_hour, event_language, event_age_restriction, place_id, place_name, place_name_2, place_description, place_address, place_city, place_coordinates, place_link, artist_id, artist_name, artist_description, artist_summary, artist_link, artist_genres, artist2_id, artist2_name, artist2_description, artist2_summary, artist2_link, artist2_genres, artist3_id, artist3_name, artist3_description, artist3_summary, artist3_link, artist3_genres, price_regular, price_discounted1, price_discounted1_comments, price_discounted2, price_discounted2_comments, entrance_link) FROM stdin;
2	Event 2	Secondary Event 2	This is a description for Event 2.	Jazz	{family-friendly,festival}	http://example.com/image_2.jpg	http://example.com/event_2	2025-07-31	17:00:00	22:00:00	Doors open 30 minutes before	Italian	21+	429	Bergamo Venue 2	Bergamo Alt Venue 2	Description of the venue in Bergamo.	2 Main St, Bergamo	Bergamo	(44.901429,2.390104)	http://example.com/venue_2	2178	Artist 2	Description of Artist 2.	Summary of Artist 2.	http://example.com/artist_2	{Hip-Hop,Jazz}	9110	Artist 3	Description of Artist 3.	Summary of Artist 3.	http://example.com/artist_3	{Rock,Pop}	9876	Artist 4	Description of Artist 4.	Summary of Artist 4.	http://example.com/artist_4	{Rock,Pop}	58.26	48.79	Student discount	11.36	Early bird	http://example.com/tickets_2
1	Event 1	Secondary Event 1	This is a description for Event 1.	Rock	{festival}	http://example.com/image_1.jpg	http://example.com/event_1	2025-08-31	17:00:00	21:00:00	Doors open 30 minutes before	Catalan	18+	753	Bergamo Venue 1	Bergamo Alt Venue 1	Description of the venue in Bergamo.	1 Main St, Bergamo	Bergamo	(44.745401,4.007821)	http://example.com/venue_1	3595	Artist 1	Description of Artist 1.	Summary of Artist 1.	http://example.com/artist_1	{Electronic}	1760	Artist 2	Description of Artist 2.	Summary of Artist 2.	http://example.com/artist_2	{Jazz}	8529	Artist 3	Description of Artist 3.	Summary of Artist 3.	http://example.com/artist_3	{Hip-Hop}	27.90	34.24	Student discount	16.35	Early bird	http://example.com/tickets_1
3	Event 3	Secondary Event 3	This is a description for Event 3.	Hip-Hop	{family-friendly,festival}	http://example.com/image_3.jpg	http://example.com/event_3	2025-10-12	17:00:00	22:00:00	Doors open 30 minutes before	Catalan	All Ages	527	Bergamo Venue 3	Bergamo Alt Venue 3	Description of the venue in Bergamo.	3 Main St, Bergamo	Bergamo	(43.463988,6.748456)	http://example.com/venue_3	1044	Artist 3	Description of Artist 3.	Summary of Artist 3.	http://example.com/artist_3	{Electronic,Jazz}	5628	Artist 4	Description of Artist 4.	Summary of Artist 4.	http://example.com/artist_4	{Jazz}	7844	Artist 5	Description of Artist 5.	Summary of Artist 5.	http://example.com/artist_5	{Electronic,Pop}	70.32	36.58	Student discount	20.51	Early bird	http://example.com/tickets_3
4	Event 4	Secondary Event 4	This is a description for Event 4.	Rock	{live,family-friendly,outdoor}	http://example.com/image_4.jpg	http://example.com/event_4	2025-09-28	19:00:00	23:00:00	Doors open 30 minutes before	Spanish	18+	116	Bergamo Venue 4	Bergamo Alt Venue 4	Description of the venue in Bergamo.	4 Main St, Bergamo	Bergamo	(43.236089,6.555707)	http://example.com/venue_4	7052	Artist 4	Description of Artist 4.	Summary of Artist 4.	http://example.com/artist_4	{Pop}	1722	Artist 5	Description of Artist 5.	Summary of Artist 5.	http://example.com/artist_5	{Rock,Electronic}	3051	Artist 6	Description of Artist 6.	Summary of Artist 6.	http://example.com/artist_6	{Pop}	45.61	46.15	Student discount	13.77	Early bird	http://example.com/tickets_4
5	Event 5	Secondary Event 5	This is a description for Event 5.	Electronic	{live}	http://example.com/image_5.jpg	http://example.com/event_5	2025-11-03	20:00:00	22:00:00	Doors open 30 minutes before	English	All Ages	431	Bergamo Venue 5	Bergamo Alt Venue 5	Description of the venue in Bergamo.	5 Main St, Bergamo	Bergamo	(43.967675,3.488402)	http://example.com/venue_5	4101	Artist 5	Description of Artist 5.	Summary of Artist 5.	http://example.com/artist_5	{Jazz}	8701	Artist 6	Description of Artist 6.	Summary of Artist 6.	http://example.com/artist_6	{Rock}	8581	Artist 7	Description of Artist 7.	Summary of Artist 7.	http://example.com/artist_7	{Jazz}	81.29	24.00	Student discount	1.91	Early bird	http://example.com/tickets_5
6	Event 6	Secondary Event 6	This is a description for Event 6.	Electronic	{live,family-friendly}	http://example.com/image_6.jpg	http://example.com/event_6	2025-09-25	16:00:00	21:00:00	Doors open 30 minutes before	Catalan	21+	983	Bergamo Venue 6	Bergamo Alt Venue 6	Description of the venue in Bergamo.	6 Main St, Bergamo	Bergamo	(43.394321,8.105751)	http://example.com/venue_6	9379	Artist 6	Description of Artist 6.	Summary of Artist 6.	http://example.com/artist_6	{Electronic,Jazz}	4714	Artist 7	Description of Artist 7.	Summary of Artist 7.	http://example.com/artist_7	{Electronic,Rock}	1254	Artist 8	Description of Artist 8.	Summary of Artist 8.	http://example.com/artist_8	{Pop}	84.22	30.83	Student discount	18.97	Early bird	http://example.com/tickets_6
7	Event 7	Secondary Event 7	This is a description for Event 7.	Hip-Hop	{live,festival}	http://example.com/image_7.jpg	http://example.com/event_7	2025-09-07	18:00:00	22:00:00	Doors open 30 minutes before	Spanish	All Ages	464	Bergamo Venue 7	Bergamo Alt Venue 7	Description of the venue in Bergamo.	7 Main St, Bergamo	Bergamo	(44.094304,6.639878)	http://example.com/venue_7	8819	Artist 7	Description of Artist 7.	Summary of Artist 7.	http://example.com/artist_7	{Jazz,Hip-Hop}	9327	Artist 8	Description of Artist 8.	Summary of Artist 8.	http://example.com/artist_8	{Pop}	2062	Artist 9	Description of Artist 9.	Summary of Artist 9.	http://example.com/artist_9	{Pop,Rock}	14.55	43.57	Student discount	1.37	Early bird	http://example.com/tickets_7
8	Event 8	Secondary Event 8	This is a description for Event 8.	Rock	{outdoor,festival}	http://example.com/image_8.jpg	http://example.com/event_8	2025-10-20	17:00:00	21:00:00	Doors open 30 minutes before	English	18+	624	Bergamo Venue 8	Bergamo Alt Venue 8	Description of the venue in Bergamo.	8 Main St, Bergamo	Bergamo	(43.155995,6.146619)	http://example.com/venue_8	3303	Artist 8	Description of Artist 8.	Summary of Artist 8.	http://example.com/artist_8	{Electronic}	2921	Artist 9	Description of Artist 9.	Summary of Artist 9.	http://example.com/artist_9	{Rock}	3959	Artist 10	Description of Artist 10.	Summary of Artist 10.	http://example.com/artist_10	{Rock}	76.76	45.11	Student discount	13.69	Early bird	http://example.com/tickets_8
9	Event 9	Secondary Event 9	This is a description for Event 9.	Pop	{family-friendly}	http://example.com/image_9.jpg	http://example.com/event_9	2025-10-26	19:00:00	22:00:00	Doors open 30 minutes before	Spanish	21+	882	Bergamo Venue 9	Bergamo Alt Venue 9	Description of the venue in Bergamo.	9 Main St, Bergamo	Bergamo	(44.034525,8.932914)	http://example.com/venue_9	1830	Artist 9	Description of Artist 9.	Summary of Artist 9.	http://example.com/artist_9	{Hip-Hop,Electronic}	8208	Artist 10	Description of Artist 10.	Summary of Artist 10.	http://example.com/artist_10	{Electronic}	2089	Artist 11	Description of Artist 11.	Summary of Artist 11.	http://example.com/artist_11	{Rock,Hip-Hop}	62.33	46.76	Student discount	1.17	Early bird	http://example.com/tickets_9
10	Event 10	Secondary Event 10	This is a description for Event 10.	Jazz	{live,festival}	http://example.com/image_10.jpg	http://example.com/event_10	2025-10-06	16:00:00	21:00:00	Doors open 30 minutes before	English	All Ages	799	Bergamo Venue 10	Bergamo Alt Venue 10	Description of the venue in Bergamo.	10 Main St, Bergamo	Bergamo	(42.954378,6.384902)	http://example.com/venue_10	2634	Artist 10	Description of Artist 10.	Summary of Artist 10.	http://example.com/artist_10	{Jazz}	2231	Artist 11	Description of Artist 11.	Summary of Artist 11.	http://example.com/artist_11	{Rock}	3405	Artist 12	Description of Artist 12.	Summary of Artist 12.	http://example.com/artist_12	{Electronic,Pop}	39.98	5.71	Student discount	21.83	Early bird	http://example.com/tickets_10
11	Event 11	Secondary Event 11	This is a description for Event 11.	Jazz	{live,family-friendly}	http://example.com/image_11.jpg	http://example.com/event_11	2025-10-28	18:00:00	23:00:00	Doors open 30 minutes before	Italian	21+	366	Milano Venue 1	Milano Alt Venue 1	Description of the venue in Milano.	1 Main St, Milano	Milano	(43.086507,8.723158)	http://example.com/venue_11	7520	Artist 11	Description of Artist 11.	Summary of Artist 11.	http://example.com/artist_11	{Electronic}	2702	Artist 12	Description of Artist 12.	Summary of Artist 12.	http://example.com/artist_12	{Rock}	3697	Artist 13	Description of Artist 13.	Summary of Artist 13.	http://example.com/artist_13	{Jazz}	72.77	47.30	Student discount	9.97	Early bird	http://example.com/tickets_11
12	Event 12	Secondary Event 12	This is a description for Event 12.	Rock	{outdoor}	http://example.com/image_12.jpg	http://example.com/event_12	2025-08-30	18:00:00	23:00:00	Doors open 30 minutes before	English	All Ages	601	Milano Venue 2	Milano Alt Venue 2	Description of the venue in Milano.	2 Main St, Milano	Milano	(43.382923,5.238389)	http://example.com/venue_12	9640	Artist 12	Description of Artist 12.	Summary of Artist 12.	http://example.com/artist_12	{Rock,Pop}	9315	Artist 13	Description of Artist 13.	Summary of Artist 13.	http://example.com/artist_13	{Jazz}	5765	Artist 14	Description of Artist 14.	Summary of Artist 14.	http://example.com/artist_14	{Hip-Hop}	21.53	33.13	Student discount	13.78	Early bird	http://example.com/tickets_12
13	Event 13	Secondary Event 13	This is a description for Event 13.	Electronic	{festival,live}	http://example.com/image_13.jpg	http://example.com/event_13	2025-08-24	16:00:00	21:00:00	Doors open 30 minutes before	Spanish	18+	512	Milano Venue 3	Milano Alt Venue 3	Description of the venue in Milano.	3 Main St, Milano	Milano	(43.389296,5.847864)	http://example.com/venue_13	5538	Artist 13	Description of Artist 13.	Summary of Artist 13.	http://example.com/artist_13	{Pop}	7323	Artist 14	Description of Artist 14.	Summary of Artist 14.	http://example.com/artist_14	{Jazz}	7984	Artist 15	Description of Artist 15.	Summary of Artist 15.	http://example.com/artist_15	{Electronic}	61.23	15.38	Student discount	7.45	Early bird	http://example.com/tickets_13
14	Event 14	Secondary Event 14	This is a description for Event 14.	Hip-Hop	{outdoor,family-friendly}	http://example.com/image_14.jpg	http://example.com/event_14	2025-08-17	19:00:00	22:00:00	Doors open 30 minutes before	English	All Ages	581	Milano Venue 4	Milano Alt Venue 4	Description of the venue in Milano.	4 Main St, Milano	Milano	(43.758143,8.034348)	http://example.com/venue_14	4623	Artist 14	Description of Artist 14.	Summary of Artist 14.	http://example.com/artist_14	{Electronic}	3973	Artist 15	Description of Artist 15.	Summary of Artist 15.	http://example.com/artist_15	{Electronic,Jazz}	9935	Artist 16	Description of Artist 16.	Summary of Artist 16.	http://example.com/artist_16	{Rock}	56.91	37.01	Student discount	25.67	Early bird	http://example.com/tickets_14
15	Event 15	Secondary Event 15	This is a description for Event 15.	Electronic	{outdoor}	http://example.com/image_15.jpg	http://example.com/event_15	2025-09-30	18:00:00	22:00:00	Doors open 30 minutes before	Catalan	21+	145	Milano Venue 5	Milano Alt Venue 5	Description of the venue in Milano.	5 Main St, Milano	Milano	(44.781497,6.369893)	http://example.com/venue_15	5856	Artist 15	Description of Artist 15.	Summary of Artist 15.	http://example.com/artist_15	{Hip-Hop}	5297	Artist 16	Description of Artist 16.	Summary of Artist 16.	http://example.com/artist_16	{Rock,Pop}	1435	Artist 17	Description of Artist 17.	Summary of Artist 17.	http://example.com/artist_17	{Jazz}	67.46	40.49	Student discount	8.63	Early bird	http://example.com/tickets_15
16	Event 16	Secondary Event 16	This is a description for Event 16.	Pop	{festival,live}	http://example.com/image_16.jpg	http://example.com/event_16	2025-09-02	20:00:00	23:00:00	Doors open 30 minutes before	Italian	18+	798	Milano Venue 6	Milano Alt Venue 6	Description of the venue in Milano.	6 Main St, Milano	Milano	(44.889612,2.568617)	http://example.com/venue_16	4226	Artist 16	Description of Artist 16.	Summary of Artist 16.	http://example.com/artist_16	{Pop}	2911	Artist 17	Description of Artist 17.	Summary of Artist 17.	http://example.com/artist_17	{Electronic,Pop}	2523	Artist 18	Description of Artist 18.	Summary of Artist 18.	http://example.com/artist_18	{Jazz}	44.68	30.33	Student discount	6.61	Early bird	http://example.com/tickets_16
17	Event 17	Secondary Event 17	This is a description for Event 17.	Rock	{live}	http://example.com/image_17.jpg	http://example.com/event_17	2025-10-02	20:00:00	23:00:00	Doors open 30 minutes before	Catalan	21+	694	Milano Venue 7	Milano Alt Venue 7	Description of the venue in Milano.	7 Main St, Milano	Milano	(42.555306,3.248057)	http://example.com/venue_17	8430	Artist 17	Description of Artist 17.	Summary of Artist 17.	http://example.com/artist_17	{Hip-Hop}	2252	Artist 18	Description of Artist 18.	Summary of Artist 18.	http://example.com/artist_18	{Jazz,Rock}	9265	Artist 19	Description of Artist 19.	Summary of Artist 19.	http://example.com/artist_19	{Hip-Hop}	91.83	7.08	Student discount	18.55	Early bird	http://example.com/tickets_17
18	Event 18	Secondary Event 18	This is a description for Event 18.	Jazz	{festival}	http://example.com/image_18.jpg	http://example.com/event_18	2025-08-20	18:00:00	22:00:00	Doors open 30 minutes before	Spanish	All Ages	598	Milano Venue 8	Milano Alt Venue 8	Description of the venue in Milano.	8 Main St, Milano	Milano	(43.421582,3.473992)	http://example.com/venue_18	2768	Artist 18	Description of Artist 18.	Summary of Artist 18.	http://example.com/artist_18	{Rock,Electronic}	8881	Artist 19	Description of Artist 19.	Summary of Artist 19.	http://example.com/artist_19	{Pop}	4426	Artist 20	Description of Artist 20.	Summary of Artist 20.	http://example.com/artist_20	{Rock,Pop}	90.03	43.55	Student discount	28.84	Early bird	http://example.com/tickets_18
19	Event 19	Secondary Event 19	This is a description for Event 19.	Hip-Hop	{live}	http://example.com/image_19.jpg	http://example.com/event_19	2025-08-01	18:00:00	22:00:00	Doors open 30 minutes before	English	18+	841	Milano Venue 9	Milano Alt Venue 9	Description of the venue in Milano.	9 Main St, Milano	Milano	(44.986067,6.148743)	http://example.com/venue_19	2414	Artist 19	Description of Artist 19.	Summary of Artist 19.	http://example.com/artist_19	{Hip-Hop}	8397	Artist 20	Description of Artist 20.	Summary of Artist 20.	http://example.com/artist_20	{Pop}	8211	Artist 21	Description of Artist 21.	Summary of Artist 21.	http://example.com/artist_21	{Rock}	76.42	48.47	Student discount	19.49	Early bird	http://example.com/tickets_19
20	Event 20	Secondary Event 20	This is a description for Event 20.	Pop	{family-friendly}	http://example.com/image_20.jpg	http://example.com/event_20	2025-10-14	18:00:00	21:00:00	Doors open 30 minutes before	Italian	21+	895	Milano Venue 10	Milano Alt Venue 10	Description of the venue in Milano.	10 Main St, Milano	Milano	(44.161237,6.237452)	http://example.com/venue_20	1090	Artist 20	Description of Artist 20.	Summary of Artist 20.	http://example.com/artist_20	{Jazz}	6267	Artist 21	Description of Artist 21.	Summary of Artist 21.	http://example.com/artist_21	{Electronic}	1636	Artist 22	Description of Artist 22.	Summary of Artist 22.	http://example.com/artist_22	{Jazz}	92.60	20.85	Student discount	18.77	Early bird	http://example.com/tickets_20
21	Event 21	Secondary Event 21	This is a description for Event 21.	Pop	{festival}	http://example.com/image_21.jpg	http://example.com/event_21	2025-10-27	18:00:00	22:00:00	Doors open 30 minutes before	Catalan	21+	130	Barcelona Venue 1	Barcelona Alt Venue 1	Description of the venue in Barcelona.	1 Main St, Barcelona	Barcelona	(43.291122,7.662152)	http://example.com/venue_21	2205	Artist 21	Description of Artist 21.	Summary of Artist 21.	http://example.com/artist_21	{Pop}	9769	Artist 22	Description of Artist 22.	Summary of Artist 22.	http://example.com/artist_22	{Jazz}	5379	Artist 23	Description of Artist 23.	Summary of Artist 23.	http://example.com/artist_23	{Electronic,Jazz}	65.68	47.96	Student discount	21.55	Early bird	http://example.com/tickets_21
22	Event 22	Secondary Event 22	This is a description for Event 22.	Hip-Hop	{outdoor}	http://example.com/image_22.jpg	http://example.com/event_22	2025-09-20	17:00:00	23:00:00	Doors open 30 minutes before	Spanish	18+	239	Barcelona Venue 2	Barcelona Alt Venue 2	Description of the venue in Barcelona.	2 Main St, Barcelona	Barcelona	(44.38887,5.985527)	http://example.com/venue_22	2951	Artist 22	Description of Artist 22.	Summary of Artist 22.	http://example.com/artist_22	{Electronic}	1360	Artist 23	Description of Artist 23.	Summary of Artist 23.	http://example.com/artist_23	{Rock}	5077	Artist 24	Description of Artist 24.	Summary of Artist 24.	http://example.com/artist_24	{Pop}	36.86	25.74	Student discount	20.20	Early bird	http://example.com/tickets_22
23	Event 23	Secondary Event 23	This is a description for Event 23.	Electronic	{live,outdoor}	http://example.com/image_23.jpg	http://example.com/event_23	2025-08-11	18:00:00	21:00:00	Doors open 30 minutes before	Spanish	All Ages	276	Barcelona Venue 3	Barcelona Alt Venue 3	Description of the venue in Barcelona.	3 Main St, Barcelona	Barcelona	(44.520547,2.921494)	http://example.com/venue_23	6946	Artist 23	Description of Artist 23.	Summary of Artist 23.	http://example.com/artist_23	{Jazz}	3932	Artist 24	Description of Artist 24.	Summary of Artist 24.	http://example.com/artist_24	{Pop}	7911	Artist 25	Description of Artist 25.	Summary of Artist 25.	http://example.com/artist_25	{Electronic}	46.95	45.78	Student discount	26.32	Early bird	http://example.com/tickets_23
24	Event 24	Secondary Event 24	This is a description for Event 24.	Jazz	{festival,live}	http://example.com/image_24.jpg	http://example.com/event_24	2025-08-31	17:00:00	22:00:00	Doors open 30 minutes before	Catalan	All Ages	391	Barcelona Venue 4	Barcelona Alt Venue 4	Description of the venue in Barcelona.	4 Main St, Barcelona	Barcelona	(42.655274,8.403953)	http://example.com/venue_24	7021	Artist 24	Description of Artist 24.	Summary of Artist 24.	http://example.com/artist_24	{Electronic,Jazz}	2228	Artist 25	Description of Artist 25.	Summary of Artist 25.	http://example.com/artist_25	{Jazz}	8762	Artist 26	Description of Artist 26.	Summary of Artist 26.	http://example.com/artist_26	{Hip-Hop,Jazz}	54.22	23.79	Student discount	3.41	Early bird	http://example.com/tickets_24
25	Event 25	Secondary Event 25	This is a description for Event 25.	Rock	{outdoor}	http://example.com/image_25.jpg	http://example.com/event_25	2025-09-23	19:00:00	22:00:00	Doors open 30 minutes before	English	21+	841	Barcelona Venue 5	Barcelona Alt Venue 5	Description of the venue in Barcelona.	5 Main St, Barcelona	Barcelona	(42.088438,8.378051)	http://example.com/venue_25	5959	Artist 25	Description of Artist 25.	Summary of Artist 25.	http://example.com/artist_25	{Jazz}	4011	Artist 26	Description of Artist 26.	Summary of Artist 26.	http://example.com/artist_26	{Pop}	4990	Artist 27	Description of Artist 27.	Summary of Artist 27.	http://example.com/artist_27	{Hip-Hop,Jazz}	84.88	14.62	Student discount	17.95	Early bird	http://example.com/tickets_25
26	Event 26	Secondary Event 26	This is a description for Event 26.	Rock	{live,family-friendly}	http://example.com/image_26.jpg	http://example.com/event_26	2025-09-14	20:00:00	22:00:00	Doors open 30 minutes before	Italian	All Ages	980	Barcelona Venue 6	Barcelona Alt Venue 6	Description of the venue in Barcelona.	6 Main St, Barcelona	Barcelona	(44.961296,3.556474)	http://example.com/venue_26	6674	Artist 26	Description of Artist 26.	Summary of Artist 26.	http://example.com/artist_26	{Rock}	5462	Artist 27	Description of Artist 27.	Summary of Artist 27.	http://example.com/artist_27	{Pop}	7991	Artist 28	Description of Artist 28.	Summary of Artist 28.	http://example.com/artist_28	{Hip-Hop}	35.55	23.08	Student discount	3.71	Early bird	http://example.com/tickets_26
27	Event 27	Secondary Event 27	This is a description for Event 27.	Electronic	{festival}	http://example.com/image_27.jpg	http://example.com/event_27	2025-10-08	17:00:00	23:00:00	Doors open 30 minutes before	Spanish	18+	144	Barcelona Venue 7	Barcelona Alt Venue 7	Description of the venue in Barcelona.	7 Main St, Barcelona	Barcelona	(43.065315,6.937828)	http://example.com/venue_27	2743	Artist 27	Description of Artist 27.	Summary of Artist 27.	http://example.com/artist_27	{Electronic,Jazz}	1206	Artist 28	Description of Artist 28.	Summary of Artist 28.	http://example.com/artist_28	{Hip-Hop}	2748	Artist 29	Description of Artist 29.	Summary of Artist 29.	http://example.com/artist_29	{Rock,Pop}	52.72	9.56	Student discount	2.69	Early bird	http://example.com/tickets_27
28	Event 28	Secondary Event 28	This is a description for Event 28.	Jazz	{family-friendly}	http://example.com/image_28.jpg	http://example.com/event_28	2025-09-06	20:00:00	23:00:00	Doors open 30 minutes before	Catalan	21+	728	Barcelona Venue 8	Barcelona Alt Venue 8	Description of the venue in Barcelona.	8 Main St, Barcelona	Barcelona	(44.124087,2.605402)	http://example.com/venue_28	3194	Artist 28	Description of Artist 28.	Summary of Artist 28.	http://example.com/artist_28	{Electronic}	9603	Artist 29	Description of Artist 29.	Summary of Artist 29.	http://example.com/artist_29	{Hip-Hop}	3471	Artist 30	Description of Artist 30.	Summary of Artist 30.	http://example.com/artist_30	{Pop}	83.24	27.47	Student discount	6.42	Early bird	http://example.com/tickets_28
29	Event 29	Secondary Event 29	This is a description for Event 29.	Rock	{live}	http://example.com/image_29.jpg	http://example.com/event_29	2025-09-18	18:00:00	21:00:00	Doors open 30 minutes before	English	All Ages	169	Barcelona Venue 9	Barcelona Alt Venue 9	Description of the venue in Barcelona.	9 Main St, Barcelona	Barcelona	(42.878076,4.603721)	http://example.com/venue_29	8232	Artist 29	Description of Artist 29.	Summary of Artist 29.	http://example.com/artist_29	{Electronic}	4209	Artist 30	Description of Artist 30.	Summary of Artist 30.	http://example.com/artist_30	{Jazz}	4743	Artist 31	Description of Artist 31.	Summary of Artist 31.	http://example.com/artist_31	{Pop,Rock}	83.34	18.79	Student discount	3.58	Early bird	http://example.com/tickets_29
30	Event 30	Secondary Event 30	This is a description for Event 30.	Hip-Hop	{festival}	http://example.com/image_30.jpg	http://example.com/event_30	2025-08-09	20:00:00	23:00:00	Doors open 30 minutes before	Spanish	18+	747	Barcelona Venue 10	Barcelona Alt Venue 10	Description of the venue in Barcelona.	10 Main St, Barcelona	Barcelona	(42.05111,2.292979)	http://example.com/venue_30	9873	Artist 30	Description of Artist 30.	Summary of Artist 30.	http://example.com/artist_30	{Pop,Hip-Hop}	2713	Artist 31	Description of Artist 31.	Summary of Artist 31.	http://example.com/artist_31	{Hip-Hop}	8019	Artist 32	Description of Artist 32.	Summary of Artist 32.	http://example.com/artist_32	{Electronic,Rock}	92.79	16.60	Student discount	11.60	Early bird	http://example.com/tickets_30
31	Event 31	Secondary Event 31	This is a description for Event 31.	Jazz	{festival}	http://example.com/image_31.jpg	http://example.com/event_31	2025-08-23	20:00:00	23:00:00	Doors open 30 minutes before	English	All Ages	761	Boston Venue 1	Boston Alt Venue 1	Description of the venue in Boston.	1 Main St, Boston	Boston	(44.899104,8.343314)	http://example.com/venue_31	7691	Artist 31	Description of Artist 31.	Summary of Artist 31.	http://example.com/artist_31	{Electronic}	2096	Artist 32	Description of Artist 32.	Summary of Artist 32.	http://example.com/artist_32	{Hip-Hop}	8814	Artist 33	Description of Artist 33.	Summary of Artist 33.	http://example.com/artist_33	{Jazz}	55.59	27.25	Student discount	4.34	Early bird	http://example.com/tickets_31
32	Event 32	Secondary Event 32	This is a description for Event 32.	Hip-Hop	{outdoor,live}	http://example.com/image_32.jpg	http://example.com/event_32	2025-09-13	19:00:00	22:00:00	Doors open 30 minutes before	English	18+	395	Boston Venue 2	Boston Alt Venue 2	Description of the venue in Boston.	2 Main St, Boston	Boston	(42.295847,2.293133)	http://example.com/venue_32	4054	Artist 32	Description of Artist 32.	Summary of Artist 32.	http://example.com/artist_32	{Hip-Hop}	8472	Artist 33	Description of Artist 33.	Summary of Artist 33.	http://example.com/artist_33	{Jazz,Rock}	8976	Artist 34	Description of Artist 34.	Summary of Artist 34.	http://example.com/artist_34	{Electronic}	89.68	20.68	Student discount	10.97	Early bird	http://example.com/tickets_32
33	Event 33	Secondary Event 33	This is a description for Event 33.	Electronic	{live}	http://example.com/image_33.jpg	http://example.com/event_33	2025-09-10	18:00:00	21:00:00	Doors open 30 minutes before	English	All Ages	518	Boston Venue 3	Boston Alt Venue 3	Description of the venue in Boston.	3 Main St, Boston	Boston	(43.590793,3.061073)	http://example.com/venue_33	9818	Artist 33	Description of Artist 33.	Summary of Artist 33.	http://example.com/artist_33	{Pop}	7292	Artist 34	Description of Artist 34.	Summary of Artist 34.	http://example.com/artist_34	{Hip-Hop}	2673	Artist 35	Description of Artist 35.	Summary of Artist 35.	http://example.com/artist_35	{Rock}	60.30	8.78	Student discount	14.61	Early bird	http://example.com/tickets_33
34	Event 34	Secondary Event 34	This is a description for Event 34.	Rock	{festival}	http://example.com/image_34.jpg	http://example.com/event_34	2025-08-22	16:00:00	22:00:00	Doors open 30 minutes before	English	21+	123	Boston Venue 4	Boston Alt Venue 4	Description of the venue in Boston.	4 Main St, Boston	Boston	(43.132672,8.11803)	http://example.com/venue_34	2277	Artist 34	Description of Artist 34.	Summary of Artist 34.	http://example.com/artist_34	{Pop}	1833	Artist 35	Description of Artist 35.	Summary of Artist 35.	http://example.com/artist_35	{Electronic,Jazz}	3572	Artist 36	Description of Artist 36.	Summary of Artist 36.	http://example.com/artist_36	{Hip-Hop}	58.63	45.29	Student discount	15.91	Early bird	http://example.com/tickets_34
35	Event 35	Secondary Event 35	This is a description for Event 35.	Pop	{live,festival}	http://example.com/image_35.jpg	http://example.com/event_35	2025-10-07	20:00:00	23:00:00	Doors open 30 minutes before	English	All Ages	345	Boston Venue 5	Boston Alt Venue 5	Description of the venue in Boston.	5 Main St, Boston	Boston	(44.079565,2.453372)	http://example.com/venue_35	1218	Artist 35	Description of Artist 35.	Summary of Artist 35.	http://example.com/artist_35	{Rock}	9275	Artist 36	Description of Artist 36.	Summary of Artist 36.	http://example.com/artist_36	{Hip-Hop}	4020	Artist 37	Description of Artist 37.	Summary of Artist 37.	http://example.com/artist_37	{Electronic,Rock}	18.76	9.82	Student discount	7.08	Early bird	http://example.com/tickets_35
36	Event 36	Secondary Event 36	This is a description for Event 36.	Jazz	{outdoor}	http://example.com/image_36.jpg	http://example.com/event_36	2025-09-04	17:00:00	22:00:00	Doors open 30 minutes before	English	All Ages	996	Boston Venue 6	Boston Alt Venue 6	Description of the venue in Boston.	6 Main St, Boston	Boston	(43.411435,2.494524)	http://example.com/venue_36	4797	Artist 36	Description of Artist 36.	Summary of Artist 36.	http://example.com/artist_36	{Jazz}	8754	Artist 37	Description of Artist 37.	Summary of Artist 37.	http://example.com/artist_37	{Rock}	4707	Artist 38	Description of Artist 38.	Summary of Artist 38.	http://example.com/artist_38	{Electronic}	28.35	14.13	Student discount	4.00	Early bird	http://example.com/tickets_36
37	Event 37	Secondary Event 37	This is a description for Event 37.	Hip-Hop	{live}	http://example.com/image_37.jpg	http://example.com/event_37	2025-10-17	16:00:00	22:00:00	Doors open 30 minutes before	English	18+	731	Boston Venue 7	Boston Alt Venue 7	Description of the venue in Boston.	7 Main St, Boston	Boston	(42.087054,7.651127)	http://example.com/venue_37	3664	Artist 37	Description of Artist 37.	Summary of Artist 37.	http://example.com/artist_37	{Hip-Hop}	5564	Artist 38	Description of Artist 38.	Summary of Artist 38.	http://example.com/artist_38	{Rock}	8393	Artist 39	Description of Artist 39.	Summary of Artist 39.	http://example.com/artist_39	{Electronic}	62.21	40.89	Student discount	12.90	Early bird	http://example.com/tickets_37
38	Event 38	Secondary Event 38	This is a description for Event 38.	Rock	{family-friendly}	http://example.com/image_38.jpg	http://example.com/event_38	2025-09-16	17:00:00	21:00:00	Doors open 30 minutes before	English	All Ages	951	Boston Venue 8	Boston Alt Venue 8	Description of the venue in Boston.	8 Main St, Boston	Boston	(42.626553,6.438142)	http://example.com/venue_38	2774	Artist 38	Description of Artist 38.	Summary of Artist 38.	http://example.com/artist_38	{Rock}	2225	Artist 39	Description of Artist 39.	Summary of Artist 39.	http://example.com/artist_39	{Jazz}	3801	Artist 40	Description of Artist 40.	Summary of Artist 40.	http://example.com/artist_40	{Hip-Hop}	42.33	30.49	Student discount	3.19	Early bird	http://example.com/tickets_38
39	Event 39	Secondary Event 39	This is a description for Event 39.	Electronic	{outdoor}	http://example.com/image_39.jpg	http://example.com/event_39	2025-09-24	20:00:00	23:00:00	Doors open 30 minutes before	English	21+	460	Boston Venue 9	Boston Alt Venue 9	Description of the venue in Boston.	9 Main St, Boston	Boston	(43.913334,5.978726)	http://example.com/venue_39	2524	Artist 39	Description of Artist 39.	Summary of Artist 39.	http://example.com/artist_39	{Electronic}	3350	Artist 40	Description of Artist 40.	Summary of Artist 40.	http://example.com/artist_40	{Pop}	8210	Artist 41	Description of Artist 41.	Summary of Artist 41.	http://example.com/artist_41	{Hip-Hop}	93.47	45.41	Student discount	11.40	Early bird	http://example.com/tickets_39
40	Event 40	Secondary Event 40	This is a description for Event 40.	Pop	{live}	http://example.com/image_40.jpg	http://example.com/event_40	2025-08-16	20:00:00	23:00:00	Doors open 30 minutes before	English	18+	662	Boston Venue 10	Boston Alt Venue 10	Description of the venue in Boston.	10 Main St, Boston	Boston	(42.39435,2.88476)	http://example.com/venue_40	1022	Artist 40	Description of Artist 40.	Summary of Artist 40.	http://example.com/artist_40	{Electronic}	5413	Artist 41	Description of Artist 41.	Summary of Artist 41.	http://example.com/artist_41	{Hip-Hop,Jazz}	2261	Artist 42	Description of Artist 42.	Summary of Artist 42.	http://example.com/artist_42	{Jazz}	84.26	27.79	Student discount	2.52	Early bird	http://example.com/tickets_40
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
