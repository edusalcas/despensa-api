import { TestBed } from '@angular/core/testing';
import { HttpClientModule, HttpErrorResponse } from '@angular/common/http';
import { AlimentsService } from './aliments.service';
import { Food } from '../entities/food';

fdescribe('AlimentsService Integration', () => {
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
        console.log(foods.map(food => {return food._name}));
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
            console.log(food._name);
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

  fit('should fail for not existing food', (done: DoneFn) => {
    const db_id = 99;
    service.getFood(db_id).subscribe({
        next: (food) => {
            fail(`Should fail, food should be deleted, but got ${food}`);
        },
        error: (error) => {
            done(); //TODO: Manejar el error con más precisión
        }
    })
  });

  it('should delete a food by id from the API', (done: DoneFn) => {
    const db_id = 3;
    service.deleteFood(db_id).subscribe({
      next: (response) => {
        expect(response).toBeTruthy(); // Verifica que la respuesta sea positiva
        service.getFood(db_id).subscribe({
            next: (food) => {
                fail(`Should fail, food should be deleted, but got ${food}`);
            },
            error: (error) => {}
        })
        done();
      },
      error: (error) => {
        if (error instanceof HttpErrorResponse) {
          fail(`Delete failed with error: ${error.message}`);
        } else {
          fail(`Unknown error: ${error}`);
        }
        done();
      }
    });
  });


  it('should insert a food into the API', (done: DoneFn) => {
    const newFood = new Food(0, 'Integration Test Food', ['Test']);
    
    service.insertFood(newFood).subscribe({
      next: (response) => {
        expect(response._name).toBe('Integration Test Food'); // Verifica el nombre del alimento insertado
        done();
      },
      error: (error) => {
        if (error instanceof HttpErrorResponse) {
          fail(`Insert failed with error: ${error.message}`);
        } else {
          fail(`Unknown error: ${error}`);
        }
        done();
      }
    });
  });

  it('should update a food in the API', (done: DoneFn) => {
    const updatedFood = new Food(1, 'Updated Food', ['Test']);

    service.updateFood(updatedFood).subscribe({
      next: (response) => {
        expect(response).toBeTruthy(); // Verifica que la respuesta sea positiva
        done();
      },
      error: (error) => {
        if (error instanceof HttpErrorResponse) {
          fail(`Update failed with error: ${error.message}`);
        } else {
          fail(`Unknown error: ${error}`);
        }
        done();
      }
    });
  });

  it('should handle error on invalid insert', (done: DoneFn) => {
    const invalidFood = { name: 'Invalid Food', tags: [] }; // No es instancia de Food

    // Esto lanza un error sin hacer la solicitud HTTP real
    try {
      service.insertFood(invalidFood).subscribe();
    } catch (error) {
      if (error instanceof Error) {
        expect(error.message).toBe('Invalid argument: food must be an instance of Food class');
      } else {
        fail(`Unknown error: ${error}`);
      }
      done();
    }
  });
});
