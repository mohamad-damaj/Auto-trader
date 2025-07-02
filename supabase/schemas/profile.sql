    -- Make price table 
    create table price (
        timestamp TEXT primary key, -- time of stock price
        open_price DOUBLE PRECISION,
        high_price DOUBLE PRECISION,
        low_price DOUBLE PRECISION,
        close_price DOUBLE PRECISION,
        volume BIGINT,
        dividends DOUBLE PRECISION,
        stock_splits DOUBLE PRECISION,
        prediction BIGINT

    );
    comment on table price is 'Table to store price data';

    -- Make price table 
    create table news (
        id TEXT primary key, -- news ID
        datetime TEXT, -- time of news
        headline TEXT,
        summary TEXT,
        indicator TEXT,
        score DOUBLE PRECISION,
        finbert_sentiment TEXT
    );
    comment on table news is 'Table to store news data';

    -- Make price table 
    create table reddit (
        id TEXT PRIMARY KEY, -- Reddit post ID 
        created_utc TEXT, -- time of stock price
        subreddit TEXT,
        title TEXT,
        body TEXT,
        vader_sentiment DOUBLE PRECISION
    );
    comment on table reddit is 'Table to store reddit data';

    alter table price enable row level security;

    alter table news enable row level security;

    alter table reddit enable row level security;



















