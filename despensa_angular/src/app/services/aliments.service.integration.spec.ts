import { TestBed } from '@angular/core/testing';
import { HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { AlimentsService } from './aliments.service';
import { Food } from '../entities/food';
import { firstValueFrom } from 'rxjs';

describe('AlimentsService Integration', () => {
  let service: AlimentsService;
  const apiUrl = 'http://localhost:5000/rest/aliments'; // URL de la API real

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientModule], // Importa HttpClientModule para solicitudes HTTP reales
      providers: [AlimentsService]
    });

    service = TestBed.inject(AlimentsService);
  });

  it('should fetch all food from the API', (done: DoneFn) => {
    service.getAllFood().subscribe({
      next: (foods) => {
        expect(foods.length).toBeGreaterThan(0); // Verifica que al menos haya un alimento
        expect(foods[0]._name).toBeTruthy(); // Verifica que el primer alimento tenga nombre
        done();
      },
      error: (error) => {
        if (error instanceof HttpErrorResponse) {
          fail(`Should not fail, but got ${error.message}`);
        } else {
          fail(`Unknown error: ${error}`);
        }
        done();
      }
    });
  });

  it('should get a single food', (done: DoneFn) => {
    const db_id = 2;
    service.getFood(db_id).subscribe({
        next: (food) => {
            expect(food._db_id).toBe(db_id)
            done();
        },
        error: (error) => {
          if (error instanceof HttpErrorResponse) {
            fail(`Should not fail, but got ${error.message}`);
          } else {
            fail(`Unknown error: ${error}`);
          }
          done();
        }
    })
  });

  it('should fail for not existing food', (done: DoneFn) => {
    const db_id = 99;
    service.getFood(db_id).subscribe({
        next: (food) => {
            fail(`Should fail, food should be deleted, but got ${food}`);
            done();
        },
        error: (error) => {
          done(); //TODO: Manejar el error con más precisión
        }
    })
  });


  it('should insert a food, verify it exists, and delete it', async () => {
    const testFood = new Food(0, 'Test Food', ['Tag1', 'Tag2']);
    // Paso 1: Insertar el alimento
    const insertedFood = await firstValueFrom(service.insertFood(testFood));
    expect(insertedFood._name).toBe(testFood._name.toLowerCase());

    // Paso 2: Verificar que el alimento existe
    const foods = await firstValueFrom(service.getAllFood());
    const foundFood = foods.find(food => food._db_id === insertedFood._db_id);
    expect(foundFood).toBeTruthy(); // Verifica que el alimento fue encontrado
    expect(foundFood?._name).toBe(testFood._name.toLowerCase()); // Verifica que el nombre coincide

    // Paso 3: Borrar el alimento
    await firstValueFrom(service.deleteFood(insertedFood._db_id));

    // Paso 4: Verificar que fue eliminado
    const foodsAfterDelete = await firstValueFrom(service.getAllFood());
    const foodStillExists = foodsAfterDelete.find(food => food._db_id === insertedFood._db_id);
    expect(foodStillExists).toBeUndefined(); // Verifica que el alimento ya no existe
  });


  it('should insert a food, update, and delete it', async () => {
    const testFood = new Food(0, 'Test Food', ['Tag1', 'Tag2']);
    // Paso 1: Insertar el alimento
    const insertedFood = await firstValueFrom(service.insertFood(testFood));
    expect(insertedFood._name).toBe(testFood._name.toLowerCase());

    // Paso 2: Verificar que el alimento existe
    insertedFood._name = 'Updated Food'
    insertedFood._tags = ['Tag1', 'Tag3']
    const result = await firstValueFrom(service.updateFood(insertedFood));
    expect(result).toBeTruthy();

    const updatedFood = await firstValueFrom(service.getFood(insertedFood._db_id));
    expect(updatedFood._name).toBe('Updated Food'.toLowerCase()); // Verifica que el nombre coincide
    expect(updatedFood._tags).toEqual(['Tag1'.toLowerCase(), 'Tag3'.toLowerCase()]); // Verifica que el nombre coincide

    // Paso 3: Borrar el alimento
    await firstValueFrom(service.deleteFood(insertedFood._db_id));
  });
});
