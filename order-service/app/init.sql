CREATE SEQUENCE IF NOT EXISTS orders_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647

CREATE SEQUENCE IF NOT EXISTS order_items_id_seq
    INCREMENT 1
    START 1
    MINVALUE 1
    MAXVALUE 2147483647
    CACHE 1;
    CACHE 1;

CREATE TABLE IF NOT EXISTS public.orders
(
    id integer NOT NULL DEFAULT nextval('orders_id_seq'::regclass),
    user_id integer NOT NULL,
    status character varying(255) COLLATE pg_catalog."default" NOT NULL,
    total_price numeric(10,2) NOT NULL,
    creation_date date NOT NULL,
    update_date date NOT NULL,
    CONSTRAINT orders_pkey PRIMARY KEY (id)
)

CREATE TABLE IF NOT EXISTS public.order_items
(
    id integer NOT NULL DEFAULT nextval('order_items_id_seq'::regclass),
    order_id integer NOT NULL,
    product_id integer NOT NULL,
    amount integer NOT NULL,
    price numeric(10,2) NOT NULL,
    CONSTRAINT order_items_pkey PRIMARY KEY (id),
    CONSTRAINT fk_orders FOREIGN KEY (order_id)
        REFERENCES public.orders (id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)
