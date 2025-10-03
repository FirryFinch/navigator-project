--
-- PostgreSQL database dump
--

-- Dumped from database version 15.2
-- Dumped by pg_dump version 15.2

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
-- Name: access; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.access (
    id integer NOT NULL,
    category_name character varying NOT NULL
);


ALTER TABLE public.access OWNER TO postgres;

--
-- Name: access_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.access_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.access_id_seq OWNER TO postgres;

--
-- Name: access_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.access_id_seq OWNED BY public.access.id;


--
-- Name: alembic_version; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.alembic_version (
    version_num character varying(32) NOT NULL
);


ALTER TABLE public.alembic_version OWNER TO postgres;

--
-- Name: object; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.object (
    id integer NOT NULL,
    parent_id integer,
    object_type_id integer NOT NULL,
    object_drawing_id integer,
    object_status_id integer NOT NULL,
    object_name character varying NOT NULL,
    object_short_name character varying NOT NULL,
    svg_object json,
    created_time timestamp without time zone NOT NULL,
    edited_time timestamp without time zone NOT NULL
);


ALTER TABLE public.object OWNER TO postgres;

--
-- Name: object_drawing; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.object_drawing (
    id integer NOT NULL,
    parent_id integer,
    creator_id integer NOT NULL,
    editor_id integer NOT NULL,
    object_type_id integer NOT NULL,
    object_drawing_name character varying NOT NULL,
    object_drawing_short_name character varying NOT NULL,
    object_ref character varying(100) NOT NULL,
    plan_ref character varying(100),
    drawing_scale numeric,
    height numeric NOT NULL,
    created_time timestamp without time zone NOT NULL,
    edited_time timestamp without time zone NOT NULL
);


ALTER TABLE public.object_drawing OWNER TO postgres;

--
-- Name: object_drawing_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.object_drawing_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.object_drawing_id_seq OWNER TO postgres;

--
-- Name: object_drawing_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.object_drawing_id_seq OWNED BY public.object_drawing.id;


--
-- Name: object_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.object_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.object_id_seq OWNER TO postgres;

--
-- Name: object_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.object_id_seq OWNED BY public.object.id;


--
-- Name: object_status; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.object_status (
    id integer NOT NULL,
    object_status_name character varying NOT NULL
);


ALTER TABLE public.object_status OWNER TO postgres;

--
-- Name: object_status_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.object_status_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.object_status_id_seq OWNER TO postgres;

--
-- Name: object_status_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.object_status_id_seq OWNED BY public.object_status.id;


--
-- Name: object_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.object_type (
    id integer NOT NULL,
    parent_id integer,
    object_type_name character varying NOT NULL,
    object_type_short_name character varying NOT NULL,
    description_object_type character varying
);


ALTER TABLE public.object_type OWNER TO postgres;

--
-- Name: object_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.object_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.object_type_id_seq OWNER TO postgres;

--
-- Name: object_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.object_type_id_seq OWNED BY public.object_type.id;


--
-- Name: point_connections_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.point_connections_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.point_connections_id_seq OWNER TO postgres;

--
-- Name: point_connections_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.point_connections_id_seq OWNED BY public.access.id;


--
-- Name: point_connections; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.point_connections (
    id integer DEFAULT nextval('public.point_connections_id_seq'::regclass) NOT NULL,
    route_point1_id integer NOT NULL,
    route_point2_id integer NOT NULL,
    route_distance numeric NOT NULL,
    route_time numeric NOT NULL,
    weight_coefficient numeric NOT NULL,
    direction_1_to_2 integer NOT NULL,
    direction_2_to_1 integer NOT NULL
);


ALTER TABLE public.point_connections OWNER TO postgres;

--
-- Name: point_type; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.point_type (
    id integer NOT NULL,
    point_name character varying NOT NULL,
    point_short_name character varying NOT NULL,
    description character varying
);


ALTER TABLE public.point_type OWNER TO postgres;

--
-- Name: point_type_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.point_type_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.point_type_id_seq OWNER TO postgres;

--
-- Name: point_type_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.point_type_id_seq OWNED BY public.point_type.id;


--
-- Name: role; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.role (
    id integer NOT NULL,
    role_name character varying NOT NULL,
    assignment_role_time timestamp without time zone NOT NULL,
    user_id integer NOT NULL,
    access_id integer NOT NULL
);


ALTER TABLE public.role OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.role_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.role_id_seq OWNER TO postgres;

--
-- Name: role_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.role_id_seq OWNED BY public.role.id;


--
-- Name: route_point; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.route_point (
    id integer NOT NULL,
    object_id integer NOT NULL,
    point_type_id integer NOT NULL,
    route_point_name character varying NOT NULL,
    route_point_short_name character varying NOT NULL,
    x_cord double precision NOT NULL,
    y_cord double precision NOT NULL,
    z_cord double precision NOT NULL,
    svg_point json,
    created_time timestamp without time zone NOT NULL,
    edited_time timestamp without time zone NOT NULL
);


ALTER TABLE public.route_point OWNER TO postgres;

--
-- Name: route_point_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.route_point_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.route_point_id_seq OWNER TO postgres;

--
-- Name: route_point_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.route_point_id_seq OWNED BY public.route_point.id;


--
-- Name: users; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.users (
    id integer NOT NULL,
    login character varying NOT NULL,
    password character varying NOT NULL,
    name character varying NOT NULL,
    surname character varying NOT NULL
);


ALTER TABLE public.users OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE; Schema: public; Owner: postgres
--

CREATE SEQUENCE public.users_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    MAXVALUE 2147483647
    CACHE 1;


ALTER TABLE public.users_id_seq OWNER TO postgres;

--
-- Name: users_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: postgres
--

ALTER SEQUENCE public.users_id_seq OWNED BY public.users.id;


--
-- Name: access id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access ALTER COLUMN id SET DEFAULT nextval('public.access_id_seq'::regclass);


--
-- Name: object id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object ALTER COLUMN id SET DEFAULT nextval('public.object_id_seq'::regclass);


--
-- Name: object_drawing id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing ALTER COLUMN id SET DEFAULT nextval('public.object_drawing_id_seq'::regclass);


--
-- Name: object_status id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_status ALTER COLUMN id SET DEFAULT nextval('public.object_status_id_seq'::regclass);


--
-- Name: object_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_type ALTER COLUMN id SET DEFAULT nextval('public.object_type_id_seq'::regclass);


--
-- Name: point_type id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_type ALTER COLUMN id SET DEFAULT nextval('public.point_type_id_seq'::regclass);


--
-- Name: role id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role ALTER COLUMN id SET DEFAULT nextval('public.role_id_seq'::regclass);


--
-- Name: route_point id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.route_point ALTER COLUMN id SET DEFAULT nextval('public.route_point_id_seq'::regclass);


--
-- Name: users id; Type: DEFAULT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users ALTER COLUMN id SET DEFAULT nextval('public.users_id_seq'::regclass);


--
-- Data for Name: access; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.access (id, category_name) FROM stdin;
1	Владелец
2	Администратор
3	Редактор
4	Пользователь
\.


--
-- Data for Name: alembic_version; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.alembic_version (version_num) FROM stdin;
2a75553bd8fb
\.


--
-- Data for Name: object; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.object (id, parent_id, object_type_id, object_drawing_id, object_status_id, object_name, object_short_name, svg_object, created_time, edited_time) FROM stdin;
3	\N	10	7	6	Высотный учебно-лабораторный корпус стр 5 этаж 5	ГУК стр 5 этаж 5	\N	2025-05-25 12:13:03.709297	2025-05-25 12:13:03.709297
4	3	14	\N	6	Аудитория 515ю	515ю	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:05.709297
6	\N	10	6	6	Высотный учебно-лабораторный корпус стр 3 этаж 5	ГУК стр 3 этаж 5	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
5	3	14	\N	6	Аудитория 513ю	513ю	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:05.709297
7	6	14	\N	6	Аудитория 524	524	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
8	6	14	\N	6	Аудитория 522	522	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
9	3	10	5	6	Высотный учебно-лабораторный корпус стр 4 этаж 5	ГУК стр 4 этаж 5	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
10	6	14	\N	6	Аудитория 530	530	\N	2025-05-25 12:15:03.709297	2025-05-25 12:18:06.709227
11	6	12	\N	6	Коридор ГУК стр 4 этаж 5	Коридор стр 4 этаж 5	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
12	6	12	\N	6	Коридор ГУК стр 3 этаж 5	Коридор стр 3 этаж 5	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
13	6	12	\N	6	Коридор ГУК стр 5 этаж 5	Коридор стр 5 этаж 5	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
14	3	14	\N	6	Аудитория 531	531	\N	2025-05-25 12:13:03.709297	2025-05-25 12:13:03.709297
\.


--
-- Data for Name: object_drawing; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.object_drawing (id, parent_id, creator_id, editor_id, object_type_id, object_drawing_name, object_drawing_short_name, object_ref, plan_ref, drawing_scale, height, created_time, edited_time) FROM stdin;
2	\N	3	3	9	Высотный учебно-лабораторный корпус стр 4 этаж 8	ГУК стр 4 этаж 8	C:/Users/Stas/PycharmProjects/backend/svg/str4floor8.svg	C:/Users/Stas/PycharmProjects/backend/Планы ГУК/ГУК стр 4/623aeb511cf16.jpg	0.3	40	2025-05-25 11:51:03.709297	2025-05-25 11:51:03.709297
4	\N	3	3	9	Высотный учебно-лабораторный корпус стр 4 этаж 10	ГУК стр 4 этаж 10	C:/Users/Stas/PycharmProjects/backend/svg/str4floor10.svg	C:/Users/Stas/PycharmProjects/backend/Планы ГУК/ГУК стр 4/6236ef1ae6d4a.jpg	0.3	50	2025-05-25 11:53:03.709297	2025-05-25 11:53:06.709297
5	10	3	3	9	Высотный учебно-лабораторный корпус стр 4 этаж 5	ГУК стр 4 этаж 5	C:/Users/Stas/PycharmProjects/backend/svg/str4floor5.svg	C:/Users/Stas/PycharmProjects/backend/Планы ГУК/ГУК стр 4/625bede5aa18d.jpg	0.3	25	2025-05-25 12:03:03.709297	2025-05-25 12:03:03.709297
6	10	3	3	9	Высотный учебно-лабораторный корпус стр 3 этаж 5	ГУК стр 3 этаж 5	C:/Users/Stas/PycharmProjects/backend/svg/str3floor5.svg	C:/Users/Stas/PycharmProjects/backend/Планы ГУК/ГУК стр 3/63a5703f1ad70.jpg	0.2	25	2025-05-25 12:03:03.709297	2025-05-25 12:03:03.709297
7	10	3	3	9	Высотный учебно-лабораторный корпус стр 5 этаж 5	ГУК стр 5 этаж 5	C:/Users/Stas/PycharmProjects/backend/svg/str5floor5.svg	C:/Users/Stas/PycharmProjects/backend/Планы ГУК/ГУК стр 3/633153ee1d247.jpg	0.2	25	2025-05-25 12:03:03.709297	2025-05-25 12:03:03.709297
10	\N	3	3	9	Объединенный 5 этаж ГУК	ГУК этаж 5	C:/Users/Stas/PycharmProjects/backend/svg/str345floor5.svg	\N	\N	25	2025-05-25 12:03:03.709297	2025-05-25 12:03:03.709297
\.


--
-- Data for Name: object_status; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.object_status (id, object_status_name) FROM stdin;
5	Ремонт
4	Временно закрыто
6	Открыто
\.


--
-- Data for Name: object_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.object_type (id, parent_id, object_type_name, object_type_short_name, description_object_type) FROM stdin;
6	\N	Университет	Университет	\N
7	6	Кампус	Кампус	\N
8	7	Корпус	Корпус	\N
9	8	Строение	Строение	\N
10	9	Этаж	Этаж	\N
11	10	Лифт	Лифт	\N
12	10	Коридор	Коридор	\N
13	10	Проход	Проход	\N
14	10	Аудитория	Аудитория	\N
15	10	Столовая	Столовая	
\.


--
-- Data for Name: point_connections; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.point_connections (id, route_point1_id, route_point2_id, route_distance, route_time, weight_coefficient, direction_1_to_2, direction_2_to_1) FROM stdin;
1	2	7	1	1	1	1	1
2	1	6	1	1	1	1	1
3	3	8	1	1	1	1	1
4	5	9	1	1	1	1	1
5	6	10	1	1	1	1	1
6	10	11	1	1	1	1	1
7	11	12	1	1	1	1	1
8	12	13	1	1	1	1	1
\.


--
-- Data for Name: point_type; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.point_type (id, point_name, point_short_name, description) FROM stdin;
2	Нулевая точка Университета	НТУ	\N
3	Двойная	ДТ	Стыковая точка объектов
4	Начальная/Конечная	Н/К	Вход/выход
5	Прочая	ПТ	Промежуточная
1	Нулевая точка чертежа	НТЧ	Нулевая точка построенного цифрового чертежа
\.


--
-- Data for Name: role; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.role (id, role_name, assignment_role_time, user_id, access_id) FROM stdin;
1	Студент	2025-05-16 20:30:30.551234	3	1
4	Преподаватель	2025-05-24 20:00:32.556721	2	4
\.


--
-- Data for Name: route_point; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.route_point (id, object_id, point_type_id, route_point_name, route_point_short_name, x_cord, y_cord, z_cord, svg_point, created_time, edited_time) FROM stdin;
1	10	4	Точка входа в 530	530	710	265	25	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
2	8	4	Точка входа в 524	524	1075	328	25	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
3	8	4	Точка входа в 522	522	1100	360	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
4	5	4	Точка входа в 513ю	513ю	495	375	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
5	4	4	Точка входа в 515ю	515ю	568	319	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
7	7	5	Точка в коридоре ГУК стр 3 этаж 5 напротив 524	Точка напротив 524	1067	328	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
8	8	5	Точка в коридоре ГУК стр 5 этаж 5 напротив 522	Точка напротив 522	1090	360	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
9	4	5	Точка в коридоре ГУК стр 5 этаж 5 напротив 515ю	Точка напротив 515ю	595	319	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
6	11	5	Точка в коридоре ГУК стр 4 этаж 5 напротив 530	Точка напротив 530	710	276	25	\N	2025-05-25 12:20:03.709297	2025-05-25 12:20:03.709297
10	11	5	Точка в коридоре ГУК стр 4 этаж 5 напротив 535	Точка напротив 535	737	276	25	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
11	11	5	Точка в коридоре ГУК стр 4 этаж 5 напротив 533	Точка напротив 533	778	276	25	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
12	11	5	Точка в коридоре ГУК стр 4 этаж 5 напротив 531	Точка напротив 531	823	276	25	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
13	14	4	Точка входа в 531	531	823	286	25	\N	2025-05-25 12:15:03.709297	2025-05-25 12:15:03.709297
\.


--
-- Data for Name: users; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.users (id, login, password, name, surname) FROM stdin;
2	test	5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5	Новый	Пользователь
3	Arista	5994471abb01112afcc18159f6cc74b4f511b99806da59b3caf5a9c173cacfc5	Станислав	Гришин
\.


--
-- Name: access_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.access_id_seq', 4, true);


--
-- Name: object_drawing_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.object_drawing_id_seq', 10, true);


--
-- Name: object_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.object_id_seq', 14, true);


--
-- Name: object_status_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.object_status_id_seq', 7, true);


--
-- Name: object_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.object_type_id_seq', 15, true);


--
-- Name: point_connections_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.point_connections_id_seq', 8, true);


--
-- Name: point_type_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.point_type_id_seq', 5, true);


--
-- Name: role_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.role_id_seq', 4, true);


--
-- Name: route_point_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.route_point_id_seq', 13, true);


--
-- Name: users_id_seq; Type: SEQUENCE SET; Schema: public; Owner: postgres
--

SELECT pg_catalog.setval('public.users_id_seq', 3, true);


--
-- Name: access accessclass_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access
    ADD CONSTRAINT accessclass_name_key UNIQUE (category_name);


--
-- Name: access accessclass_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.access
    ADD CONSTRAINT accessclass_pkey PRIMARY KEY (id);


--
-- Name: alembic_version alembic_version_pkc; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.alembic_version
    ADD CONSTRAINT alembic_version_pkc PRIMARY KEY (version_num);


--
-- Name: object_drawing object_drawing_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing
    ADD CONSTRAINT object_drawing_name_key UNIQUE (object_drawing_name);


--
-- Name: object_drawing object_drawing_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing
    ADD CONSTRAINT object_drawing_pkey PRIMARY KEY (id);


--
-- Name: object object_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT object_name_key UNIQUE (object_name);


--
-- Name: object object_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT object_pkey PRIMARY KEY (id);


--
-- Name: object_status object_status_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_status
    ADD CONSTRAINT object_status_name_key UNIQUE (object_status_name);


--
-- Name: object_status object_status_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_status
    ADD CONSTRAINT object_status_pkey PRIMARY KEY (id);


--
-- Name: object_type object_type_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_type
    ADD CONSTRAINT object_type_name_key UNIQUE (object_type_name);


--
-- Name: object_type object_type_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_type
    ADD CONSTRAINT object_type_pkey PRIMARY KEY (id);


--
-- Name: point_type pointtype_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_type
    ADD CONSTRAINT pointtype_name_key UNIQUE (point_name);


--
-- Name: point_type pointtype_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_type
    ADD CONSTRAINT pointtype_pkey PRIMARY KEY (id);


--
-- Name: point_type pointtype_short_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_type
    ADD CONSTRAINT pointtype_short_name_key UNIQUE (point_short_name);


--
-- Name: role role_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_name_key UNIQUE (role_name);


--
-- Name: role role_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT role_pkey PRIMARY KEY (id);


--
-- Name: point_connections route_connections_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_connections
    ADD CONSTRAINT route_connections_pkey PRIMARY KEY (id);


--
-- Name: route_point route_point_name_key; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.route_point
    ADD CONSTRAINT route_point_name_key UNIQUE (route_point_name);


--
-- Name: route_point route_point_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.route_point
    ADD CONSTRAINT route_point_pkey PRIMARY KEY (id);


--
-- Name: users users_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.users
    ADD CONSTRAINT users_pkey PRIMARY KEY (id);


--
-- Name: role access_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT access_id_fkey FOREIGN KEY (access_id) REFERENCES public.access(id);


--
-- Name: object_drawing drawing_creator_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing
    ADD CONSTRAINT drawing_creator_id_fkey FOREIGN KEY (creator_id) REFERENCES public.users(id);


--
-- Name: object_drawing drawing_editor_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing
    ADD CONSTRAINT drawing_editor_id_fkey FOREIGN KEY (editor_id) REFERENCES public.users(id);


--
-- Name: object drawing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT drawing_id_fkey FOREIGN KEY (object_drawing_id) REFERENCES public.object_drawing(id);


--
-- Name: object_drawing object_drawing_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing
    ADD CONSTRAINT object_drawing_id_fkey FOREIGN KEY (parent_id) REFERENCES public.object_drawing(id) ON DELETE CASCADE;


--
-- Name: object object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT object_id_fkey FOREIGN KEY (parent_id) REFERENCES public.object(id) ON DELETE CASCADE;


--
-- Name: route_point object_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.route_point
    ADD CONSTRAINT object_id_fkey FOREIGN KEY (object_id) REFERENCES public.object(id);


--
-- Name: object object_status_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT object_status_id_fkey FOREIGN KEY (object_status_id) REFERENCES public.object_status(id);


--
-- Name: object_type object_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_type
    ADD CONSTRAINT object_type_id_fkey FOREIGN KEY (parent_id) REFERENCES public.object_type(id) ON DELETE CASCADE;


--
-- Name: object_drawing object_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object_drawing
    ADD CONSTRAINT object_type_id_fkey FOREIGN KEY (object_type_id) REFERENCES public.object_type(id);


--
-- Name: object object_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.object
    ADD CONSTRAINT object_type_id_fkey FOREIGN KEY (object_type_id) REFERENCES public.object_type(id);


--
-- Name: route_point point_type_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.route_point
    ADD CONSTRAINT point_type_id_fkey FOREIGN KEY (point_type_id) REFERENCES public.point_type(id);


--
-- Name: point_connections route_point1_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_connections
    ADD CONSTRAINT route_point1_id_fkey FOREIGN KEY (route_point1_id) REFERENCES public.route_point(id);


--
-- Name: point_connections route_point2_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.point_connections
    ADD CONSTRAINT route_point2_id_fkey FOREIGN KEY (route_point2_id) REFERENCES public.route_point(id);


--
-- Name: role user_id_fkey; Type: FK CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.role
    ADD CONSTRAINT user_id_fkey FOREIGN KEY (user_id) REFERENCES public.users(id);


--
-- PostgreSQL database dump complete
--

