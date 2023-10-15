CREATE TABLE "users" (
    "id" bigserial PRIMARY KEY,
    "email" varchar UNIQUE NOT NULL,
    "name" varchar NOT NULL,
    "hashed_password" varchar NOT NULL,
    "created_at" timestamptz NOT NULL DEFAULT (now())
);

CREATE TABLE "tasks" (
    "id" bigserial PRIMARY KEY,
    "name" varchar NOT NULL,
    "description" varchar,
    "created_at" timestamptz NOT NULL DEFAULT (now()),
    "user_id" bigint NOT NULL,
    FOREIGN KEY ("user_id") REFERENCES "users" ("id") ON DELETE CASCADE
);