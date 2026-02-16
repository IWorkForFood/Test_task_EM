--
-- PostgreSQL database dump
--

\restrict v6DKABGL4b1y8P1flFoejMjtqUCXSD2krembuIRmV0Vqs07jawJbejXQH2dE4Mx

-- Dumped from database version 18.1 (Debian 18.1-1.pgdg13+2)
-- Dumped by pg_dump version 18.1 (Debian 18.1-1.pgdg13+2)

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET transaction_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

--
-- Name: productcategory; Type: TYPE; Schema: public; Owner: amin
--

CREATE TYPE public.productcategory AS ENUM (
    'SMARTPHONES',
    'LAPTOPS_AND_TABLETS',
    'COMPUTERS_AND_COMPONENTS',
    'TV_AND_VIDEO',
    'AUDIO',
    'PHOTO_AND_VIDEO_CAMERAS',
    'GAMING',
    'SMART_HOME',
    'ACCESSORIES_ELECTRONICS',
    'LARGE_APPLIANCES',
    'SMALL_APPLIANCES',
    'CLIMATE_CONTROL',
    'KITCHEN_APPLIANCES',
    'WOMENS_CLOTHING',
    'MENS_CLOTHING',
    'KIDS_CLOTHING',
    'SHOES',
    'BAGS_AND_WALLETS',
    'ACCESSORIES',
    'UNDERWEAR_AND_SLEEPWEAR',
    'SPORT_CLOTHING',
    'COSMETICS',
    'PERFUMERY',
    'HAIR_CARE',
    'FACE_AND_BODY_CARE',
    'MAKEUP',
    'HEALTH_AND_PHARMACY',
    'FURNITURE',
    'HOME_TEXTILE',
    'KITCHEN_AND_TABLEWARE',
    'LIGHTING',
    'DECOR_AND_INTERIOR',
    'GARDEN_AND_PLANTS',
    'REPAIR_AND_TOOLS',
    'TOYS',
    'BABY_CARE',
    'CHILDREN_FURNITURE',
    'SCHOOL_AND_CREATIVITY',
    'SPORT_EQUIPMENT',
    'FITNESS_AND_GYM',
    'TOURISM_AND_CAMPING',
    'BICYCLES_AND_SCOOTERS',
    'AUTO_PARTS',
    'CAR_ACCESSORIES',
    'MOTORCYCLES_AND_SCOOTERS',
    'TIRES_AND_WHEELS',
    'FOOD_AND_DRINKS',
    'PET_SUPPLIES',
    'PET_FOOD',
    'BOOKS',
    'STATIONERY',
    'BOARD_GAMES_AND_PUZZLES',
    'HANDMADE_AND_HOBBY',
    'COLLECTIBLES',
    'JEWELRY',
    'WATCHES',
    'OTHER'
);


ALTER TYPE public.productcategory OWNER TO amin;

SET default_tablespace = '';

SET default_table_access_method = heap;

--
-- Name: access_roles_rules; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.access_roles_rules (
    id integer NOT NULL,
    role_id integer NOT NULL,
    element_id integer NOT NULL,
    read character varying(10) NOT NULL,
    read_all character varying(10) NOT NULL,
    "create" character varying(10) NOT NULL,
    update character varying(10) NOT NULL,
    update_all character varying(10) NOT NULL,
    delete character varying(10) NOT NULL,
    delete_all character varying(10) NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.access_roles_rules OWNER TO amin;

--
-- Name: access_roles_rules_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.access_roles_rules_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.access_roles_rules_id_seq OWNER TO amin;

--
-- Name: access_roles_rules_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.access_roles_rules_id_seq OWNED BY public.access_roles_rules.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO amin;

--
-- Name: business_elements; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.business_elements (
    id integer NOT NULL,
    name character varying(100) NOT NULL,
    description character varying(500),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.business_elements OWNER TO amin;

--
-- Name: business_elements_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.business_elements_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.business_elements_id_seq OWNER TO amin;

--
-- Name: business_elements_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.business_elements_id_seq OWNED BY public.business_elements.id;


--
-- Name: orders; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.orders (
    id integer NOT NULL,
    name character varying NOT NULL,
    cost double precision NOT NULL,
    description character varying NOT NULL,
    buyer_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.orders OWNER TO amin;

--
-- Name: orders_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.orders_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.orders_id_seq OWNER TO amin;

--
-- Name: orders_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.orders_id_seq OWNED BY public.orders.id;


--
-- Name: products; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.products (
    id integer NOT NULL,
    sku character varying(64) NOT NULL,
    name character varying NOT NULL,
    description character varying NOT NULL,
    price double precision NOT NULL,
    stock integer NOT NULL,
    seller_id integer NOT NULL,
    order_id integer NOT NULL,
    contact_phone character varying NOT NULL,
    category public.productcategory NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.products OWNER TO amin;

--
-- Name: products_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.products_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.products_id_seq OWNER TO amin;

--
-- Name: products_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.products_id_seq OWNED BY public.products.id;


--
-- Name: reviews; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.reviews (
    id integer NOT NULL,
    stars_amount integer NOT NULL,
    title character varying NOT NULL,
    review_content character varying NOT NULL,
    user_id integer NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL,
    product_id integer NOT NULL
);


ALTER TABLE public.reviews OWNER TO amin;

--
-- Name: reviews_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.reviews_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.reviews_id_seq OWNER TO amin;

--
-- Name: reviews_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.reviews_id_seq OWNED BY public.reviews.id;


--
-- Name: roles; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.roles (
    id integer NOT NULL,
    name character varying(50) NOT NULL,
    description character varying(255),
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.roles OWNER TO amin;

--
-- Name: roles_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.roles_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.roles_id_seq OWNER TO amin;

--
-- Name: roles_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.roles_id_seq OWNED BY public.roles.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: amin
--

CREATE TABLE public.users (
    id integer NOT NULL,
    first_name character varying NOT NULL,
    last_name character varying NOT NULL,
    password character varying NOT NULL,
    email character varying NOT NULL,
    is_user boolean DEFAULT true NOT NULL,
    is_seller boolean DEFAULT false NOT NULL,
    is_moderator boolean DEFAULT false NOT NULL,
    is_admin boolean DEFAULT false NOT NULL,
    created_at timestamp without time zone DEFAULT now() NOT NULL,
    updated_at timestamp without time zone DEFAULT now() NOT NULL
);


ALTER TABLE public.users OWNER TO amin;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: amin
--

CREATE SEQUENCE public.users_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


ALTER SEQUENCE public.users_id_seq OWNER TO amin;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: amin
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: access_roles_rules id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.access_roles_rules ALTER COLUMN id SET DEFAULT nextval('public.access_roles_rules_id_seq'::regclass);


--
-- Name: business_elements id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.business_elements ALTER COLUMN id SET DEFAULT nextval('public.business_elements_id_seq'::regclass);


--
-- Name: orders id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.orders ALTER COLUMN id SET DEFAULT nextval('public.orders_id_seq'::regclass);


--
-- Name: products id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.products ALTER COLUMN id SET DEFAULT nextval('public.products_id_seq'::regclass);


--
-- Name: reviews id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.reviews ALTER COLUMN id SET DEFAULT nextval('public.reviews_id_seq'::regclass);


--
-- Name: roles id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.roles ALTER COLUMN id SET DEFAULT nextval('public.roles_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: access_roles_rules; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.access_roles_rules (id, role_id, element_id, read, read_all, "create", update, update_all, delete, delete_all, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.alembic_version (version_num) FROM stdin;
f20053b6e2c9
\.


--
-- Data for Name: business_elements; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.business_elements (id, name, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: orders; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.orders (id, name, cost, description, buyer_id, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: products; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.products (id, sku, name, description, price, stock, seller_id, order_id, contact_phone, category, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: reviews; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.reviews (id, stars_amount, title, review_content, user_id, created_at, updated_at, product_id) FROM stdin;
\.


--
-- Data for Name: roles; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.roles (id, name, description, created_at, updated_at) FROM stdin;
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: amin
--

COPY public.users (id, first_name, last_name, password, email, is_user, is_seller, is_moderator, is_admin, created_at, updated_at) FROM stdin;
\.


--
-- Name: access_roles_rules_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.access_roles_rules_id_seq', 1, false);


--
-- Name: business_elements_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.business_elements_id_seq', 1, false);


--
-- Name: orders_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.orders_id_seq', 1, false);


--
-- Name: products_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.products_id_seq', 1, false);


--
-- Name: reviews_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.reviews_id_seq', 1, false);


--
-- Name: roles_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.roles_id_seq', 1, false);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: amin
--

SELECT pg_catalog.setval('public.users_id_seq', 1, false);


--
-- Name: access_roles_rules access_roles_rules_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.access_roles_rules
    ADD CONSTRAINT access_roles_rules_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: business_elements business_elements_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.business_elements
    ADD CONSTRAINT business_elements_pkey PRIMARY KEY (id);


--
-- Name: orders orders_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_pkey PRIMARY KEY (id);


--
-- Name: products products_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_pkey PRIMARY KEY (id);


--
-- Name: reviews reviews_product_id_key; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_product_id_key UNIQUE (product_id);


--
-- Name: roles roles_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.roles
    ADD CONSTRAINT roles_pkey PRIMARY KEY (id);


--
-- Name: access_roles_rules uq_access_rule_role_element; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.access_roles_rules
    ADD CONSTRAINT uq_access_rule_role_element UNIQUE (role_id, element_id);


--
-- Name: users users_email_key; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_email_key UNIQUE (email);


--
-- Name: users users_password_key; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_password_key UNIQUE (password);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: ix_access_roles_rules_element_id; Type: INDEX; Schema: public; Owner: amin
--

CREATE INDEX ix_access_roles_rules_element_id ON public.access_roles_rules USING btree (element_id);


--
-- Name: ix_access_roles_rules_role_id; Type: INDEX; Schema: public; Owner: amin
--

CREATE INDEX ix_access_roles_rules_role_id ON public.access_roles_rules USING btree (role_id);


--
-- Name: ix_business_elements_name; Type: INDEX; Schema: public; Owner: amin
--

CREATE UNIQUE INDEX ix_business_elements_name ON public.business_elements USING btree (name);


--
-- Name: ix_products_sku; Type: INDEX; Schema: public; Owner: amin
--

CREATE UNIQUE INDEX ix_products_sku ON public.products USING btree (sku);


--
-- Name: ix_roles_name; Type: INDEX; Schema: public; Owner: amin
--

CREATE UNIQUE INDEX ix_roles_name ON public.roles USING btree (name);


--
-- Name: access_roles_rules access_roles_rules_element_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.access_roles_rules
    ADD CONSTRAINT access_roles_rules_element_id_fkey FOREIGN KEY (element_id) REFERENCES public.business_elements(id) ON DELETE CASCADE;


--
-- Name: access_roles_rules access_roles_rules_role_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.access_roles_rules
    ADD CONSTRAINT access_roles_rules_role_id_fkey FOREIGN KEY (role_id) REFERENCES public.roles(id) ON DELETE CASCADE;


--
-- Name: orders orders_buyer_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.orders
    ADD CONSTRAINT orders_buyer_id_fkey FOREIGN KEY (buyer_id) REFERENCES public.users(id);


--
-- Name: products products_order_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_order_id_fkey FOREIGN KEY (order_id) REFERENCES public.orders(id);


--
-- Name: products products_seller_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.products
    ADD CONSTRAINT products_seller_id_fkey FOREIGN KEY (seller_id) REFERENCES public.users(id);


--
-- Name: reviews reviews_product_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_product_id_fkey FOREIGN KEY (product_id) REFERENCES public.products(id);


--
-- Name: reviews reviews_user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: amin
--

ALTER TABLE ONLY public.reviews
    ADD CONSTRAINT reviews_user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

\unrestrict v6DKABGL4b1y8P1flFoejMjtqUCXSD2krembuIRmV0Vqs07jawJbejXQH2dE4Mx

