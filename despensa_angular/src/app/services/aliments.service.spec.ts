import { TestBed } from '@angular/core/testing';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { AlimentsService } from './aliments.service';
import { Food } from '../entities/food';
import { HttpErrorResponse } from '@angular/common/http';

describe('AlimentsService', () => {
  let service: AlimentsService;
  let httpMock: HttpTestingController;
  const apiUrl = 'http://localhost:5000/rest/aliments';

  beforeEach(() => {
    TestBed.configureTestingModule({
      imports: [HttpClientTestingModule],
      providers: [AlimentsService]
    });

    service = TestBed.inject(AlimentsService);
    httpMock = TestBed.inject(HttpTestingController);
  });

  afterEach(() => {
    httpMock.verify(); // Verifica que no haya solicitudes pendientes.
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });

  describe('#getAllFood', () => {
    it('should return an Observable<Food[]>', () => {
      const mockFoodData = [
        { db_id: 1, name: 'Pizza', tags: ['Italian', 'Fast food'] },
        { db_id: 2, name: 'Burger', tags: ['American', 'Grilled'] }
      ];

      service.getAllFood().subscribe((foods) => {
        expect(foods.length).toBe(2);
        expect(foods[0]._name).toBe('Pizza');
        expect(foods[1]._name).toBe('Burger');
      });

      const req = httpMock.expectOne(apiUrl);
      expect(req.request.method).toBe('GET');
      req.flush(mockFoodData); // Envía datos simulados como respuesta.
    });

    it('should handle an error on getAllFood', () => {
      service.getAllFood().subscribe(
        () => fail('Should have failed with a network error'),
        (error: HttpErrorResponse) => {
          expect(error.status).toBe(500);
        }
      );

      const req = httpMock.expectOne(apiUrl);
      req.flush('Error loading food data', { status: 500, statusText: 'Server Error' });
    });
  });

  describe('#insertFood', () => {
    it('should insert a food and return the inserted food', () => {
      const newFood = new Food(0, 'Salad', ['Healthy']);
      const mockResponse = { db_id: 1, name: 'Salad', tags: ['Healthy'] };

      service.insertFood(newFood).subscribe((response) => {
        expect(response._name).toBe(newFood._name);
        expect(response._tags).toEqual(newFood._tags);
        expect(response._db_id).not.toBe(newFood._db_id);
      });

      const req = httpMock.expectOne(apiUrl);
      expect(req.request.method).toBe('POST');
      expect(req.request.body).toBeInstanceOf(Food);
      req.flush(mockResponse); // Respuesta simulada.
    });

    it('should throw an error when the food is not an instance of Food', () => {
      const invalidFood = { name: 'Invalid Food', tags: [] }; // No es instancia de Food.

      expect(() => {
        service.insertFood(invalidFood).subscribe();
      }).toThrow(new Error('Invalid argument: food must be an instance of Food class'));
    });
  });

  describe('#updateFood', () => {
    it('should update an existing food', () => {
      const updatedFood = new Food(1, 'Updated Pizza', ['Italian', 'Fast food']);

      service.updateFood(updatedFood).subscribe((response) => {
        expect(response).toBeTruthy(); // Asume que la respuesta es exitosa.
      });

      const req = httpMock.expectOne(`${apiUrl}/1`);
      expect(req.request.method).toBe('PUT');
      expect(req.request.body).toEqual(updatedFood);
      req.flush({}); // Respuesta simulada.
    });
  });

  describe('#deleteFood', () => {
    it('should delete a food by id', () => {
      service.deleteFood(1).subscribe((response) => {
        expect(response).toBeTruthy(); // Asume que la respuesta es exitosa.
      });

      const req = httpMock.expectOne(`${apiUrl}/1`);
      expect(req.request.method).toBe('DELETE');
      req.flush({}); // Respuesta simulada.
    });
  });
});