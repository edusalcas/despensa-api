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
