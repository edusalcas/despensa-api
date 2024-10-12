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


-- Eliminar todos los registros de la tabla aliment y luego insertar nuevos datos
TRUNCATE TABLE aliment CASCADE ;
INSERT INTO aliment (name, tags) VALUES
    (
     'Onion',
     ARRAY['vegetable', 'good'] -- Usamos ARRAY para representar un array en PostgreSQL
    ),
    (
     'Garlic',
     ARRAY['vegetable']
    ),
    (
     'Chicken',
     ARRAY['meat']
    );

-- Eliminar todos los registros de la tabla ingredient y luego insertar nuevos datos
TRUNCATE TABLE ingredient CASCADE;
INSERT INTO ingredient (aliment_id, quantity, quantity_type, optional) VALUES
    (
     1,
     1,
     'units',
     FALSE
    ),
    (
     2,
     10,
     'gr',
     TRUE
    ),
    (
     3,
     100,
     'gr',
     FALSE
    );

-- Eliminar todos los registros de la tabla recipe y luego insertar nuevos datos
TRUNCATE TABLE recipe CASCADE;
INSERT INTO recipe (name, num_people, steps, category, tags, time) VALUES
    (
     'Recipe1', -- Se asigna un nombre a la receta en lugar de un número
     1,
     ARRAY['step1', 'step2'], -- Usamos ARRAY para representar un array en PostgreSQL
     'main',
     ARRAY['healthy', 'quick'],
     15
    );

-- Eliminar todos los registros de la tabla recipe_ingredient y luego insertar nuevos datos
TRUNCATE TABLE recipe_ingredient CASCADE;
INSERT INTO recipe_ingredient (recipe_id, ingredient_id) VALUES
    (
     1,
     1
    ),
    (
     1,
     2
    ),
    (
     1,
     3
    );

-- Eliminar todos los registros de la tabla pantry y luego insertar nuevos datos
TRUNCATE TABLE pantry CASCADE;
INSERT INTO pantry (aliment_id) VALUES
    (1),
    (2);

-- Eliminar todos los registros de la tabla shopping_list y luego insertar nuevos datos
TRUNCATE TABLE shopping_list CASCADE;
INSERT INTO shopping_list (item) VALUES
    ('item1'),
    ('item2');
