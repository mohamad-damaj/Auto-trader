-- Make price table 
create table price (
    timestamp TEXT primary key, -- time of stock price
    open_price DOUBLE PRECISION,
    high_price DOUBLE PRECISION,
    low_price DOUBLE PRECISION,
    close_price DOUBLE PRECISION,
    volume BIGINT,
    dividends DOUBLE PRECISION,
    stock_splits DOUBLE PRECISION

);
comment on table public.profile is 'Table to store price data';

-- Make price table 
create table news (
    timestamp TEXT primary key, -- time of stock price
    open_price DOUBLE PRECISION,
    high_price DOUBLE PRECISION,
    low_price DOUBLE PRECISION,
    close_price DOUBLE PRECISION,
    volume BIGINT,
    dividends DOUBLE PRECISION,
    stock_splits DOUBLE PRECISION

);
comment on table public.profile is 'Table to store price data';

-- Make price table 
create table tweets (
    timestamp TEXT primary key, -- time of stock price
    open_price DOUBLE PRECISION,
    high_price DOUBLE PRECISION,
    low_price DOUBLE PRECISION,
    close_price DOUBLE PRECISION,
    volume BIGINT,
    dividends DOUBLE PRECISION,
    stock_splits DOUBLE PRECISION

);
comment on table public.profile is 'Table to store price data';



















