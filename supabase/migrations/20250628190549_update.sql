alter table "public"."news" drop column "timestamp";

alter table "public"."news" drop column "title";

alter table "public"."news" add column "datetime" text;

alter table "public"."news" add column "finbert_sentiment" text;

alter table "public"."news" add column "headline" text;

alter table "public"."news" add column "indicator" text;

alter table "public"."news" add column "score" double precision;

alter table "public"."news" add column "summary" text;

alter table "public"."reddit" drop column "timestamp";

alter table "public"."reddit" add column "created_utc" text;

alter table "public"."reddit" add column "vader_sentiment" double precision;


