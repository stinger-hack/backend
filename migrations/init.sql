CREATE TYPE user_role AS ENUM ('company', 'investor', 'startup');
CREATE TABLE public.user (
  user_id uuid NOT NULL,
  email varchar(50) NOT NULL,
  created_at timestamp NOT NULL,
  first_name varchar(50) NOT NULL,
  phone integer NOT NULL,
  rating integer DEFAULT 0 NOT NULL,
  device_id varchar(255) DEFAULT NULL,
  user_password varchar(255) NOT NULL,
  user_role user_role NOT NULL,
  second_name varchar(255) NOT NULL,
  middle_name varchar(255) DEFAULT NULL,
  PRIMARY KEY (user_id)
);

CREATE TABLE public.company (
  company_id uuid NOT NULL,
  user_id uuid NOT NULL,
  user_position varchar(255) NOT NULL,
  company_name varchar(50) NOT NULL,
  company_website varchar(50) NOT NULL,
  company_email varchar(50) NOT NULL,
  PRIMARY KEY (company_id),
  CONSTRAINT company_user_id_user_user_id_foreign FOREIGN KEY (user_id) REFERENCES public.user (user_id)
);

CREATE TYPE investor_type AS ENUM (
  'venture_fund', 'business_angel',
  'family_office', 'development_institute'
);
CREATE TABLE public.investor (
  investor_id uuid NOT NULL,
  user_id uuid NOT NULL,
  investor_type investor_type NOT NULL,
  company_name varchar(50) DEFAULT NULL,
  company_website varchar(50) DEFAULT NULL,
  company_email varchar(50) DEFAULT NULL,
  user_position varchar(255) DEFAULT NULL,
  PRIMARY KEY (investor_id),
  CONSTRAINT investor_user_id_user_user_id_foreign FOREIGN KEY (user_id) REFERENCES public.user (user_id)
);

CREATE TABLE news (
  news_id uuid NOT NULL,
  header varchar(255) NOT NULL,
  news_text varchar(255) NOT NULL,
  user_id uuid NOT NULL,
  PRIMARY KEY (news_id),
  CONSTRAINT news_user_id_user_user_id_foreign FOREIGN KEY (user_id) REFERENCES public.user (user_id)
);

create type project_stage as enum   ('idea', 'prototype', 'first_sales');
CREATE TABLE public.startup (
  startup_id uuid NOT NULL,
  project_name varchar(50) NOT NULL,
  description varchar(255) NOT NULL,
  presentation_link varchar(255) NOT NULL,
  stage project_stage NOT NULL,
  study_facility integer NOT NULL,
  user_id uuid NOT NULL,
  PRIMARY KEY (startup_id),
  CONSTRAINT startup_user_id_user_user_id_foreign FOREIGN KEY (user_id) REFERENCES public.user (user_id)
);

CREATE TABLE startup_cost (
  cost_id uuid NOT NULL,
  price decimal(18, 2) NOT NULL,
  startup_id uuid NOT NULL,
  created_at timestamp NOT NULL,
  PRIMARY KEY (cost_id),
  CONSTRAINT startup_cost_startup_id_startup_startup_id_foreign FOREIGN KEY (startup_id) REFERENCES public.startup (startup_id)
);