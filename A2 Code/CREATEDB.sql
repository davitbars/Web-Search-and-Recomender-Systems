-- Table: categories
CREATE TABLE IF NOT EXISTS public.categories
(
    category_id integer NOT NULL DEFAULT nextval('categories_category_id_seq'::regclass),
    name character varying(255) COLLATE pg_catalog."default" NOT NULL,
    CONSTRAINT categories_pkey PRIMARY KEY (category_id)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.categories
    OWNER to postgres;


-- Table: document_term_relationship
CREATE TABLE IF NOT EXISTS public.document_term_relationship
(
    doc_number integer NOT NULL,
    term character varying(255) COLLATE pg_catalog."default" NOT NULL,
    count integer NOT NULL,
    CONSTRAINT document_term_relationship_pkey PRIMARY KEY (doc_number, term),
    CONSTRAINT document_term_relationship_doc_number_fkey FOREIGN KEY (doc_number)
        REFERENCES public.documents (doc_number) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION,
    CONSTRAINT document_term_relationship_term_fkey FOREIGN KEY (term)
        REFERENCES public.terms (term) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.document_term_relationship
    OWNER to postgres;


-- Table: documents
CREATE TABLE IF NOT EXISTS public.documents
(
    doc_number integer NOT NULL DEFAULT nextval('documents_doc_number_seq'::regclass),
    text text COLLATE pg_catalog."default" NOT NULL,
    title character varying(255) COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    date date NOT NULL,
    category_id integer NOT NULL,
    CONSTRAINT documents_pkey PRIMARY KEY (doc_number),
    CONSTRAINT documents_category_id_fkey FOREIGN KEY (category_id)
        REFERENCES public.categories (category_id) MATCH SIMPLE
        ON UPDATE NO ACTION
        ON DELETE NO ACTION
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.documents
    OWNER to postgres;


-- Table: terms
CREATE TABLE IF NOT EXISTS public.terms
(
    term character varying(255) COLLATE pg_catalog."default" NOT NULL,
    num_chars integer NOT NULL,
    CONSTRAINT terms_pkey PRIMARY KEY (term)
)

TABLESPACE pg_default;

ALTER TABLE IF EXISTS public.terms
    OWNER to postgres;