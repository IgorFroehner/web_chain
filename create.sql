CREATE TABLE block (
    index integer primary key,
    version integer not null,
    time timestamp not null,
    nonce integer not null,
    hash char(64) not null,
    prev_hash char(64) not null,
    difficulty integer not null,
    data text
);