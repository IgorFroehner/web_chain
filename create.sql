CREATE TABLE block (
    index integer primary key,
    version integer not null,
    "user" varchar(64) not null,
    time timestamp not null,
    nonce integer not null,
    hash char(64) not null,
    prev_hash char(64) not null,
    difficulty integer not null,
    data text,
    foreign key ("user") references "user"("user")
);

CREATE TABLE "user" (
    "user" varchar(64) primary key,
    password varchar(64) not null,
    authenticated boolean
);

INSERT INTO "user" ("user", password, authenticated)
VALUES ('adm', '03ac674216f3e15c761ee1a5e255f067953623c8b388b4459e13f978d7c846f4', false); -- password: 1234
