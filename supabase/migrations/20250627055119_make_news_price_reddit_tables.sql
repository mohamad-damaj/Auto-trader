create table "public"."news" (
    "id" text not null,
    "timestamp" text,
    "title" text
);


create table "public"."price" (
    "timestamp" text not null,
    "open_price" double precision,
    "high_price" double precision,
    "low_price" double precision,
    "close_price" double precision,
    "volume" bigint,
    "dividends" double precision,
    "stock_splits" double precision
);


create table "public"."reddit" (
    "id" text not null,
    "timestamp" text,
    "subreddit" text,
    "title" text,
    "body" text
);


CREATE UNIQUE INDEX news_pkey ON public.news USING btree (id);

CREATE UNIQUE INDEX price_pkey ON public.price USING btree ("timestamp");

CREATE UNIQUE INDEX reddit_pkey ON public.reddit USING btree (id);

alter table "public"."news" add constraint "news_pkey" PRIMARY KEY using index "news_pkey";

alter table "public"."price" add constraint "price_pkey" PRIMARY KEY using index "price_pkey";

alter table "public"."reddit" add constraint "reddit_pkey" PRIMARY KEY using index "reddit_pkey";

grant delete on table "public"."news" to "anon";

grant insert on table "public"."news" to "anon";

grant references on table "public"."news" to "anon";

grant select on table "public"."news" to "anon";

grant trigger on table "public"."news" to "anon";

grant truncate on table "public"."news" to "anon";

grant update on table "public"."news" to "anon";

grant delete on table "public"."news" to "authenticated";

grant insert on table "public"."news" to "authenticated";

grant references on table "public"."news" to "authenticated";

grant select on table "public"."news" to "authenticated";

grant trigger on table "public"."news" to "authenticated";

grant truncate on table "public"."news" to "authenticated";

grant update on table "public"."news" to "authenticated";

grant delete on table "public"."news" to "service_role";

grant insert on table "public"."news" to "service_role";

grant references on table "public"."news" to "service_role";

grant select on table "public"."news" to "service_role";

grant trigger on table "public"."news" to "service_role";

grant truncate on table "public"."news" to "service_role";

grant update on table "public"."news" to "service_role";

grant delete on table "public"."price" to "anon";

grant insert on table "public"."price" to "anon";

grant references on table "public"."price" to "anon";

grant select on table "public"."price" to "anon";

grant trigger on table "public"."price" to "anon";

grant truncate on table "public"."price" to "anon";

grant update on table "public"."price" to "anon";

grant delete on table "public"."price" to "authenticated";

grant insert on table "public"."price" to "authenticated";

grant references on table "public"."price" to "authenticated";

grant select on table "public"."price" to "authenticated";

grant trigger on table "public"."price" to "authenticated";

grant truncate on table "public"."price" to "authenticated";

grant update on table "public"."price" to "authenticated";

grant delete on table "public"."price" to "service_role";

grant insert on table "public"."price" to "service_role";

grant references on table "public"."price" to "service_role";

grant select on table "public"."price" to "service_role";

grant trigger on table "public"."price" to "service_role";

grant truncate on table "public"."price" to "service_role";

grant update on table "public"."price" to "service_role";

grant delete on table "public"."reddit" to "anon";

grant insert on table "public"."reddit" to "anon";

grant references on table "public"."reddit" to "anon";

grant select on table "public"."reddit" to "anon";

grant trigger on table "public"."reddit" to "anon";

grant truncate on table "public"."reddit" to "anon";

grant update on table "public"."reddit" to "anon";

grant delete on table "public"."reddit" to "authenticated";

grant insert on table "public"."reddit" to "authenticated";

grant references on table "public"."reddit" to "authenticated";

grant select on table "public"."reddit" to "authenticated";

grant trigger on table "public"."reddit" to "authenticated";

grant truncate on table "public"."reddit" to "authenticated";

grant update on table "public"."reddit" to "authenticated";

grant delete on table "public"."reddit" to "service_role";

grant insert on table "public"."reddit" to "service_role";

grant references on table "public"."reddit" to "service_role";

grant select on table "public"."reddit" to "service_role";

grant trigger on table "public"."reddit" to "service_role";

grant truncate on table "public"."reddit" to "service_role";

grant update on table "public"."reddit" to "service_role";


