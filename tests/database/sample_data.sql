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
