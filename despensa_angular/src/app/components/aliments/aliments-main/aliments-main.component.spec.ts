import { ComponentFixture, TestBed } from '@angular/core/testing';
import { HttpClientModule } from '@angular/common/http';
import { AlimentsMainComponent } from './aliments-main.component';
import { AlimentsService } from '../../../services/aliments.service';
import { ModalService } from '../../../services/modal.service';
import { Food } from '../../../entities/food';
import { of } from 'rxjs';

fdescribe('AlimentsMainComponent Integration Tests', () => {
  let component: AlimentsMainComponent;
  let fixture: ComponentFixture<AlimentsMainComponent>;
  let alimentsService: AlimentsService;
  let modalService: ModalService;


  beforeEach(async () => {
    await TestBed.configureTestingModule({
        imports: [
            HttpClientModule,
            AlimentsMainComponent,  // IMPORTA el componente standalone
        ],
        providers: [AlimentsService, ModalService]
    }).compileComponents();

    fixture = TestBed.createComponent(AlimentsMainComponent);
    component = fixture.componentInstance;
    alimentsService = TestBed.inject(AlimentsService);
    modalService = TestBed.inject(ModalService);
  });

  it('should call retrieveFoodData and receive food list', async () => {
    spyOn(component, 'retrieveFoodData').and.callThrough();
    
    component.ngOnInit();
    fixture.detectChanges();
    
    expect(component.retrieveFoodData).toHaveBeenCalled();
  });

  it('should verify correct API call for getAllFood', () => {
    spyOn(alimentsService, 'getAllFood').and.callThrough();
    
    component.ngOnInit();
    expect(alimentsService.getAllFood).toHaveBeenCalled();
  });

  it('should retrieve food data from the server', (done: DoneFn) => {
    // Act
    component.ngOnInit();

    // Assert
    setTimeout(() => {
        //fixture.detectChanges();  // Detecta cambios después de la recepción de datos
        let foodList = component.getFoodList();
        expect(foodList.length).toBeGreaterThan(0);
        console.log(foodList); // Puedes ver la salida en la consola para verificar
        done();
    }, 500); 
  });

  it('should open modal and add food', async () => {
    // Simular la apertura del modal y el retorno de un nuevo alimento
    const newFood = new Food(69, 'New Food', ['tag1', 'tag2']);
    spyOn(modalService, 'openModal').and.returnValue(of(newFood));

    // Act
    await component.openModal();
    let foodList = component.getFoodList();

    // Assert
    expect(foodList.length).toBe(1);
    expect(foodList[0].aliment).toEqual(newFood);
  });

  it('should delete food item', async () => {
    let foodList = component.getFoodList();
    // Primero añade un alimento
    const foodToDelete = new Food(69, 'New Food', ['tag1', 'tag2']);
    foodList.push({ aliment: foodToDelete, editable: false });

    // Act
    await component.deleteFood(foodToDelete._db_id);

    // Assert
    setTimeout((done: DoneFn) => {
        fixture.detectChanges();  // Detecta cambios después de la recepción de datos
        let foodList = component.getFoodList();
        expect(foodList.length).toBe(3); // Asegúrate de que se eliminó el alimento
        console.log(foodList); // Puedes ver la salida en la consola para verificar
        done();
    }, 500); 
  });
});
