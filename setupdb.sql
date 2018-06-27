--Setup Script
CREATE TABLE IF NOT EXISTS security(
    sec_id INTEGER PRIMARY KEY,
    isin,
    sedol,
    ticker,
    ticker_exchange,
    cusip,
    cins
);

CREATE TABLE IF NOT EXISTS model(
    model_id INTEGER PRIMARY KEY,
    model_name,
    date_modified DATE
);


CREATE TABLE IF NOT EXISTS model_holdings(
    model_holdings_id INTEGER PRIMARY KEY,
    model_id INTEGER,
    sec_id INTEGER,
    weight,
    FOREIGN KEY(model_id) REFERENCES model(model_id) ON UPDATE CASCADE,
    FOREIGN KEY(sec_id) REFERENCES security(sec_id) ON UPDATE RESTRICT
);

CREATE TABLE IF NOT EXISTS model_restrictions(
    model_restrictions_id INTEGER PRIMARY KEY,
    model_name,
    function,
    level,
    value,
    min,
    max,
    FOREIGN KEY(model_name) REFERENCES model(model_name) ON UPDATE CASCADE
);
















