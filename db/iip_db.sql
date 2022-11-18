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
-- Name: comisiones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.comisiones (
    comision_id bigint NOT NULL,
    influencer_id bigint NOT NULL,
    venta_id bigint NOT NULL,
    producto_id bigint NOT NULL,
    pago_id bigint NOT NULL,
    total double precision DEFAULT 0.0 NOT NULL
);


--
-- Name: comision_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.comision_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: comision_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.comision_id_seq OWNED BY public.comisiones.comision_id;


--
-- Name: composiciones; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.composiciones (
    composicion_id bigint NOT NULL,
    nombre character varying,
    influencer_id bigint
);


--
-- Name: composicion_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.composicion_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: composicion_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.composicion_id_seq OWNED BY public.composiciones.composicion_id;


--
-- Name: influencers; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.influencers (
    influencer_id bigint NOT NULL,
    nombre character varying NOT NULL,
    track_id character varying NOT NULL,
    num_seguidores integer DEFAULT 0 NOT NULL,
    pct_comision integer DEFAULT 0 NOT NULL
);


--
-- Name: influencer_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.influencer_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: influencer_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.influencer_id_seq OWNED BY public.influencers.influencer_id;


--
-- Name: lineas_ventas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.lineas_ventas (
    linea_venta_id bigint NOT NULL,
    venta_id bigint NOT NULL,
    producto_id bigint NOT NULL,
    unidades integer DEFAULT 0 NOT NULL,
    total double precision DEFAULT 0.0 NOT NULL
);


--
-- Name: lineas_venta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.lineas_venta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: lineas_venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.lineas_venta_id_seq OWNED BY public.lineas_ventas.linea_venta_id;


--
-- Name: productos; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.productos (
    producto_id bigint NOT NULL,
    nombre character varying NOT NULL,
    descripcion text NOT NULL,
    categoria character varying NOT NULL,
    precio double precision DEFAULT 0.0 NOT NULL
);


--
-- Name: productos_comp; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.productos_comp (
    producto_comp_id bigint NOT NULL,
    composicion_id bigint,
    producto_id bigint
);


--
-- Name: productos_comp_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.productos_comp_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: productos_comp_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.productos_comp_id_seq OWNED BY public.productos_comp.producto_comp_id;


--
-- Name: producto_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.producto_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: producto_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.producto_id_seq OWNED BY public.productos.producto_id;


--
-- Name: visitas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.visitas (
    visita_id bigint NOT NULL,
    user_id text NOT NULL,
    composicion_id text NOT NULL,
    created_at timestamp(6) without time zone NOT NULL
);


--
-- Name: visita_id_dq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.visita_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: visita_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.visita_id_seq OWNED BY public.visitas.visita_id;


--
-- Name: ventas; Type: TABLE; Schema: public; Owner: -
--

CREATE TABLE public.ventas (
    venta_id bigint NOT NULL,
    user_id text NOT NULL,
    total double precision DEFAULT 0.0 NOT NULL,
    created_at timestamp(6) without time zone NOT NULL
);


--
-- Name: venta_id_seq; Type: SEQUENCE; Schema: public; Owner: -
--

CREATE SEQUENCE public.venta_id_seq
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;


--
-- Name: venta_id_seq; Type: SEQUENCE OWNED BY; Schema: public; Owner: -
--

ALTER SEQUENCE public.venta_id_seq OWNED BY public.ventas.venta_id;


--
-- Name: comisiones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comisiones ALTER COLUMN comision_id SET DEFAULT nextval('public.comision_id_seq'::regclass);


--
-- Name: composiciones id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.composiciones ALTER COLUMN composicion_id SET DEFAULT nextval('public.composicion_id_seq'::regclass);


--
-- Name: influencers id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.influencers ALTER COLUMN influencer_id SET DEFAULT nextval('public.influencer_id_seq'::regclass);


--
-- Name: lineas_ventas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lineas_ventas ALTER COLUMN linea_venta_id SET DEFAULT nextval('public.lineas_venta_id_seq'::regclass);


--
-- Name: productos id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos ALTER COLUMN producto_id SET DEFAULT nextval('public.producto_id_seq'::regclass);


--
-- Name: productos_comp id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos_comp ALTER COLUMN producto_comp_id SET DEFAULT nextval('public.productos_comp_id_seq'::regclass);


--
-- Name: visitas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.visitas ALTER COLUMN visita_id SET DEFAULT nextval('public.visita_id_seq'::regclass);


--
-- Name: ventas id; Type: DEFAULT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ventas ALTER COLUMN venta_id SET DEFAULT nextval('public.venta_id_seq'::regclass);


--
-- Name: comisiones comisiones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.comisiones
    ADD CONSTRAINT comisiones_pkey PRIMARY KEY (comision_id);


--
-- Name: composiciones composiciones_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.composiciones
    ADD CONSTRAINT composiciones_pkey PRIMARY KEY (composicion_id);


--
-- Name: influencers influencers_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.influencers
    ADD CONSTRAINT influencers_pkey PRIMARY KEY (influencer_id);


--
-- Name: lineas_ventas lineas_ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.lineas_ventas
    ADD CONSTRAINT lineas_ventas_pkey PRIMARY KEY (linea_venta_id);


--
-- Name: productos_comp productos_comp_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos_comp
    ADD CONSTRAINT productos_comp_pkey PRIMARY KEY (producto_comp_id);


--
-- Name: productos productos_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.productos
    ADD CONSTRAINT productos_pkey PRIMARY KEY (producto_id);


--
-- Name: visitas visitas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.visitas
    ADD CONSTRAINT visitas_pkey PRIMARY KEY (visita_id);


--
-- Name: ventas ventas_pkey; Type: CONSTRAINT; Schema: public; Owner: -
--

ALTER TABLE ONLY public.ventas
    ADD CONSTRAINT ventas_pkey PRIMARY KEY (venta_id);


--
-- Name: index_comisiones_on_influencer_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_comisiones_on_influencer_id ON public.comisiones USING btree (influencer_id);


--
-- Name: index_comisiones_on_pago_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_comisiones_on_pago_id ON public.comisiones USING btree (pago_id);


--
-- Name: index_comisiones_on_producto_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_comisiones_on_producto_id ON public.comisiones USING btree (producto_id);


--
-- Name: index_comisiones_on_venta_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_comisiones_on_venta_id ON public.comisiones USING btree (venta_id);


--
-- Name: index_composiciones_on_influencer_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_composiciones_on_influencer_id ON public.composiciones USING btree (influencer_id);


--
-- Name: index_lineas_ventas_on_producto_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_lineas_ventas_on_producto_id ON public.lineas_ventas USING btree (producto_id);


--
-- Name: index_lineas_ventas_on_venta_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_lineas_ventas_on_venta_id ON public.lineas_ventas USING btree (venta_id);


--
-- Name: index_productos_comp_on_composicion_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_productos_comp_on_composicion_id ON public.productos_comp USING btree (composicion_id);


--
-- Name: index_productos_comp_on_producto_id; Type: INDEX; Schema: public; Owner: -
--

CREATE INDEX index_productos_comp_on_producto_id ON public.productos_comp USING btree (producto_id);


--
-- PostgreSQL database dump complete
--

SET search_path TO "$user", public;



