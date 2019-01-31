--
-- PostgreSQL database dump
--

SET client_encoding = 'UTF8';


--
-- Name: plpgsql; Type: EXTENSION; Schema: -; Owner: 
--

CREATE EXTENSION IF NOT EXISTS plpgsql WITH SCHEMA pg_catalog;


--
-- Name: EXTENSION plpgsql; Type: COMMENT; Schema: -; Owner: 
--



SET search_path = public, pg_catalog;

--
-- Name: activitystatus; Type: TYPE; Schema: public; Owner: mmg_postgres
--

CREATE TYPE activitystatus AS ENUM (
  'success',
  'fail',
  'pending'
);


--
-- Name: footprinttype; Type: TYPE; Schema: public; Owner: mmg_postgres
--

CREATE TYPE footprinttype AS ENUM (
  'home',
  'food',
  'road'
);


--
-- Name: propositionstatus; Type: TYPE; Schema: public; Owner: mmg_postgres
--

CREATE TYPE propositionstatus AS ENUM (
  'accepted',
  'refused',
  'skipped'
);


SET default_tablespace = '';

SET default_with_oids = false;

--
-- Name: activity; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE activity (
  id bigint NOT NULL,
  user_id bigint NOT NULL,
  recommendation_id bigint NOT NULL,
  date_start timestamp without time zone NOT NULL,
  date_end timestamp without time zone,
  is_success boolean,
  status activitystatus NOT NULL
);


--
-- Name: activity_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE activity_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: activity_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE activity_id_seq OWNED BY activity.id;


--
-- Name: footprint; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE footprint (
  id bigint NOT NULL,
  user_id bigint NOT NULL,
  date_created timestamp without time zone NOT NULL,
  type footprinttype,
  value double precision NOT NULL
);


--
-- Name: footprint_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE footprint_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: footprint_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE footprint_id_seq OWNED BY footprint.id;


--
-- Name: proposition; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE proposition (
  id bigint NOT NULL,
  user_id bigint NOT NULL,
  recommendation_id bigint NOT NULL,
  probability double precision NOT NULL,
  state propositionstatus,
  date_write timestamp without time zone,
  date_created timestamp without time zone NOT NULL
);


--
-- Name: proposition_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE proposition_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: proposition_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE proposition_id_seq OWNED BY proposition.id;


--
-- Name: question; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE question (
  id bigint NOT NULL,
  property_name text NOT NULL,
  display_text text,
  date_created timestamp without time zone NOT NULL
);


--
-- Name: question_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE question_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: question_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE question_id_seq OWNED BY question.id;


--
-- Name: recommendation; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE recommendation (
  id bigint NOT NULL,
  title character varying(120) NOT NULL,
  content text NOT NULL,
  benefit double precision NOT NULL,
  benefit_description text,
  did_you_know text,
  how_to text,
  type footprinttype,
  date_created timestamp without time zone
);


--
-- Name: recommendation_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE recommendation_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: recommendation_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE recommendation_id_seq OWNED BY recommendation.id;


--
-- Name: user; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE "user" (
  id bigint NOT NULL,
  email character varying(80) NOT NULL,
  password bytea NOT NULL,
  username character varying(80) NOT NULL,
  "dateCreated" timestamp without time zone NOT NULL
);


--
-- Name: user_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE user_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: user_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE user_id_seq OWNED BY "user".id;


--
-- Name: user_property; Type: TABLE; Schema: public; Owner: mmg_postgres
--

CREATE TABLE user_property (
  id bigint NOT NULL,
  user_id bigint NOT NULL,
  question_id bigint NOT NULL,
  value double precision NOT NULL,
  date_created timestamp without time zone NOT NULL
);


--
-- Name: user_property_id_seq; Type: SEQUENCE; Schema: public; Owner: mmg_postgres
--

CREATE SEQUENCE user_property_id_seq
  AS bigint
  START WITH 1
  INCREMENT BY 1
  NO MINVALUE
  NO MAXVALUE
  CACHE 1;


--
-- Name: user_property_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: mmg_postgres
--

ALTER SEQUENCE user_property_id_seq OWNED BY user_property.id;


--
-- Name: activity id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY activity ALTER COLUMN id SET DEFAULT nextval('activity_id_seq'::regclass);


--
-- Name: footprint id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY footprint ALTER COLUMN id SET DEFAULT nextval('footprint_id_seq'::regclass);


--
-- Name: proposition id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY proposition ALTER COLUMN id SET DEFAULT nextval('proposition_id_seq'::regclass);


--
-- Name: question id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY question ALTER COLUMN id SET DEFAULT nextval('question_id_seq'::regclass);


--
-- Name: recommendation id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY recommendation ALTER COLUMN id SET DEFAULT nextval('recommendation_id_seq'::regclass);


--
-- Name: user id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY "user" ALTER COLUMN id SET DEFAULT nextval('user_id_seq'::regclass);


--
-- Name: user_property id; Type: DEFAULT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY user_property ALTER COLUMN id SET DEFAULT nextval('user_property_id_seq'::regclass);


--
-- Name: activity_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('activity_id_seq', 1, false);


--
-- Name: footprint_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('footprint_id_seq', 1, false);


--
-- Name: proposition_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('proposition_id_seq', 1, false);


--
-- Name: question_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('question_id_seq', 1, false);


--
-- Name: recommendation_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('recommendation_id_seq', 1, false);


--
-- Name: user_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('user_id_seq', 1, false);


--
-- Name: user_property_id_seq; Type: SEQUENCE SET; Schema: public; Owner: mmg_postgres
--

SELECT pg_catalog.setval('user_property_id_seq', 1, false);


--
-- Name: activity activity_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY activity
  ADD CONSTRAINT activity_pkey PRIMARY KEY (id);


--
-- Name: footprint footprint_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY footprint
  ADD CONSTRAINT footprint_pkey PRIMARY KEY (id);


--
-- Name: proposition proposition_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY proposition
  ADD CONSTRAINT proposition_pkey PRIMARY KEY (id);


--
-- Name: question question_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY question
  ADD CONSTRAINT question_pkey PRIMARY KEY (id);


--
-- Name: question question_property_name_key; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY question
  ADD CONSTRAINT question_property_name_key UNIQUE (property_name);


--
-- Name: recommendation recommendation_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY recommendation
  ADD CONSTRAINT recommendation_pkey PRIMARY KEY (id);


--
-- Name: user user_email_key; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY "user"
  ADD CONSTRAINT user_email_key UNIQUE (email);


--
-- Name: user user_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY "user"
  ADD CONSTRAINT user_pkey PRIMARY KEY (id);


--
-- Name: user_property user_property_pkey; Type: CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY user_property
  ADD CONSTRAINT user_property_pkey PRIMARY KEY (id);


--
-- Name: activity activity_recommendation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY activity
  ADD CONSTRAINT activity_recommendation_id_fkey FOREIGN KEY (recommendation_id) REFERENCES recommendation(id);


--
-- Name: activity activity_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY activity
  ADD CONSTRAINT activity_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: footprint footprint_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY footprint
  ADD CONSTRAINT footprint_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: proposition proposition_recommendation_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY proposition
  ADD CONSTRAINT proposition_recommendation_id_fkey FOREIGN KEY (recommendation_id) REFERENCES recommendation(id);


--
-- Name: proposition proposition_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY proposition
  ADD CONSTRAINT proposition_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: user_property user_property_question_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY user_property
  ADD CONSTRAINT user_property_question_id_fkey FOREIGN KEY (question_id) REFERENCES question(id);


--
-- Name: user_property user_property_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: mmg_postgres
--

ALTER TABLE ONLY user_property
  ADD CONSTRAINT user_property_user_id_fkey FOREIGN KEY (user_id) REFERENCES "user"(id);


--
-- Name: public; Type: ACL; Schema: -; Owner: postgres
--

GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

