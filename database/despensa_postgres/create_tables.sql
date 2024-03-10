CREATE TABLE IF NOT EXISTS aliment
(
    aliment_id SERIAL PRIMARY KEY,
    name VARCHAR(64) NOT NULL,
    tags VARCHAR(64)[]
);
CREATE TABLE IF NOT EXISTS ingredient
(
    ingredient_id SERIAL PRIMARY KEY,
    aliment_id INTEGER NOT NULL,
    quantity FLOAT,
    quantity_type VARCHAR(64),
    optional BOOLEAN,
    CONSTRAINT ingredient_aliment_id_fk FOREIGN KEY (aliment_id) REFERENCES aliment (aliment_id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS recipe
(
    recipe_id SERIAL PRIMARY KEY,
    name VARCHAR(256) NOT NULL,
    num_people INTEGER NOT NULL,
    steps TEXT[] NOT NULL,
    category VARCHAR(64) NOT NULL,
    tags VARCHAR(64)[],
    time INTEGER
);
CREATE TABLE IF NOT EXISTS recipe_ingredient
(
    recipe_id INTEGER NOT NULL,
    ingredient_id INTEGER NOT NULL,
    CONSTRAINT recipe_ingredient_recipe_id_fk FOREIGN KEY (recipe_id) REFERENCES recipe (recipe_id) ON UPDATE CASCADE ON DELETE CASCADE,
    CONSTRAINT recipe_ingredient_ingredient_id_fk FOREIGN KEY (ingredient_id) REFERENCES ingredient (ingredient_id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS pantry
(
    aliment_id INTEGER NOT NULL,
    CONSTRAINT pantry_aliment_id_fk FOREIGN KEY (aliment_id) REFERENCES aliment (aliment_id) ON UPDATE CASCADE ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS shopping_list
(
    item VARCHAR(256) NOT NULL
);
