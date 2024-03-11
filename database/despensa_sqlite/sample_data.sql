DELETE FROM aliment;
DELETE FROM sqlite_sequence WHERE name='aliment';
INSERT INTO aliment (name, tags) VALUES
    (
     'Onion',
     'vegetable,good'
    ),
    (
     'Garlic',
     'vegetable'
    ),
    (
     'Chicken',
     'meat'
    )
;

DELETE FROM main.ingredient;
DELETE FROM sqlite_sequence WHERE name='ingredient';
INSERT INTO main.ingredient (aliment_id, quantity, quantity_type, optional) VALUES
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
    )
;

DELETE FROM main.recipe;
DELETE FROM sqlite_sequence WHERE name='recipe';
INSERT INTO main.recipe (name, num_people, steps, category, tags, time) VALUES
    (
     1,
     1,
     'step1%_%step2',
     'main',
     'healthy,quick',
     '15min'
    )
;

DELETE FROM main.recipe_ingredient;
DELETE FROM sqlite_sequence WHERE name='recipe_ingredient';
INSERT INTO main.recipe_ingredient (recipe_id, ingredient_id) VALUES
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
    )
;

DELETE FROM main.pantry;
INSERT INTO main.pantry (aliment_id) VALUES
    (1),
    (2)
;

DELETE FROM main.shopping_list;
INSERT INTO main.shopping_list (item) VALUES
    ('item1'),
    ('item2')
;