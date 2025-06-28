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
comment on table price is 'Table to store price data';

-- Make price table 
create table news (
    id TEXT primary key, -- news ID
    timestamp TEXT, -- time of news
    title TEXT,
    indicator TEXT,
    score DOUBLE PRECISION,
);
comment on table news is 'Table to store news data';

-- Make price table 
create table reddit (
    id TEXT PRIMARY KEY, -- Reddit post ID 
    timestamp TEXT, -- time of stock price
    subreddit TEXT,
    title TEXT,
    body TEXT,
    indicator TEXT,
    score DOUBLE PRECISION
    

);
comment on table reddit is 'Table to store reddit data';

alter table price enable row level security;

alter table news enable row level security;

alter table reddit enable row level security;



















