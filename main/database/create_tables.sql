DROP TABLE IF EXISTS aliment;
CREATE TABLE aliment
(
    aliment_id INTEGER NOT NULL
        constraint table_name_pk
            PRIMARY KEY autoincrement,
    name VARCHAR(64),
    tags VARCHAR(512)
);

DROP TABLE IF EXISTS ingredient;
CREATE TABLE ingredient
(
    ingredient_id INTEGER NOT NULL
        constraint ingredient_pk
            primary key autoincrement,
    aliment_id INTEGER NOT NULL
        constraint ingredient_aliment_id_fk
            references aliment
            on update cascade on delete cascade,
    quantity FLOAT,
    quantity_type VARCHAR(64),
    optional BOOLEAN
);

DROP TABLE IF EXISTS recipe;
CREATE TABLE recipe
(
    recipe_id  integer      not null
        constraint recipe_pk
            primary key autoincrement,
    name       VARCHAR(256) not null,
    num_people integer      not null,
    steps      VARCHAR      not null,
    category   VARCHAR(64)  not null,
    tags       VARCHAR(256),
    time       integer
);

DROP TABLE IF EXISTS recipe_ingredient;
CREATE TABLE recipe_ingredient
(
    recipe_id     integer not null
        constraint recipe_ingredient_recipe_id_fk
            references recipe
            on update cascade on delete cascade,
    ingredient_id integer not null
        constraint recipe_ingredient_ingredient_id_fk
            references ingredient
            on update cascade on delete cascade
);

