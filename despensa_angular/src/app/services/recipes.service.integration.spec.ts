import { TestBed } from '@angular/core/testing';
import { HttpClientModule } from '@angular/common/http';
import { RecipesService } from './recipes.service';
import { Recipe } from '../entities/recipe';
import { Ingredient } from '../entities/ingredient';
import { Food } from '../entities/food';
import { AlimentsService } from './aliments.service';
import { firstValueFrom } from 'rxjs';

describe('RecipesService Integration', () => {
  let service: RecipesService;
  let alimentService: AlimentsService;

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientModule], // Importa HttpClientModule para solicitudes HTTP reales
      providers: [RecipesService, AlimentsService]
    });

    service = TestBed.inject(RecipesService);
    alimentService = TestBed.inject(AlimentsService);
  });

  const testAliment1 = new Food(0, 'Integration test aliment 1', [])
  const testAliment2 = new Food(0, 'Integration test aliment 2', [])

  it('should retrieve all recipes from the API', (done: DoneFn) => {
    service.getAllRecipes().subscribe({
      next: (recipes) => {
        expect(recipes.length).toBeGreaterThan(0); // Verifica que hay al menos una receta
        expect(recipes[0]._name).toBeTruthy(); // Verifica que la primera receta tiene un nombre
        done();
      },
      error: (err) => {
        fail(`Failed to retrieve recipes: ${err.message}`);
        done();
      }
    });
  });
  
  it('should insert and delete a recipe', async () => {
    // Paso 1: Insertar el alimento
    const insertedFood1 = await firstValueFrom(alimentService.insertFood(testAliment1));
    const insertedFood2 = await firstValueFrom(alimentService.insertFood(testAliment2));

    const testIngredient1 = new Ingredient(insertedFood1, 100, 'gr', false, 0);
    const testIngredient2 = new Ingredient(insertedFood2, 2, 'units', false, 0); 
    const testRecipe = new Recipe(0, 'Integration Test Recipe', 2, [testIngredient1, testIngredient2], ['Step 1'], 'Dessert', ['TestTag'], 20);
  
    const insertedRecipe = await firstValueFrom(service.insertRecipe(testRecipe));

    expect(insertedRecipe._db_id).not.toBe(testRecipe._db_id)
    expect(insertedRecipe._name).toBe(testRecipe._name)

    // Paso 2: Borrar elementos
    await firstValueFrom(service.deleteRecipe(insertedRecipe._db_id));
    await firstValueFrom(alimentService.deleteFood(insertedFood1._db_id));
    await firstValueFrom(alimentService.deleteFood(insertedFood2._db_id));

  });

  it('should insert, update and delete a recipe', async () => {
    // Insertar el alimento
    const insertedFood1 = await firstValueFrom(alimentService.insertFood(testAliment1));
    const insertedFood2 = await firstValueFrom(alimentService.insertFood(testAliment2));

    const testIngredient1 = new Ingredient(insertedFood1, 100, 'gr', false, 0);
    const testIngredient2 = new Ingredient(insertedFood2, 2, 'units', false, 0); 
    const testRecipe = new Recipe(0, 'Integration Test Recipe', 2, [testIngredient1, testIngredient2], ['Step 1'], 'Dessert', ['TestTag'], 20);
  
    const insertedRecipe = await firstValueFrom(service.insertRecipe(testRecipe));

    expect(insertedRecipe._db_id).not.toBe(testRecipe._db_id)
    expect(insertedRecipe._name).toBe(testRecipe._name)

    insertedRecipe._name = 'Integration Test Recipe Update'
    insertedRecipe._num_people = 4

    const response = await firstValueFrom(service.updateRecipe(insertedRecipe))
    expect(response).toBeTruthy()

    const updatedRecipe = await firstValueFrom(service.get(insertedRecipe._db_id))

    expect(updatedRecipe._db_id).toBe(insertedRecipe._db_id)
    expect(updatedRecipe._name).toBe('Integration Test Recipe Update')
    expect(updatedRecipe._num_people).toBe(4)

    // Borrar elementos
    await firstValueFrom(service.deleteRecipe(insertedRecipe._db_id));
    await firstValueFrom(alimentService.deleteFood(insertedFood1._db_id));
    await firstValueFrom(alimentService.deleteFood(insertedFood2._db_id));
  });

});
