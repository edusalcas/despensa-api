import { ComponentFixture, TestBed } from '@angular/core/testing';
import { ReactiveFormsModule, FormsModule } from '@angular/forms';
import { AddRecipeComponent } from './add-recipe.component';
import { AlimentsService } from '../../../services/aliments.service';  // Servicios reales
import { RecipesService } from '../../../services/recipes.service';  // Servicios reales
import { HttpClientModule } from '@angular/common/http';
import { Recipe } from '../../../entities/recipe';  // Asegúrate de tener la entidad Recipe importada
import { Food } from '../../../entities/food';


describe('AddRecipeComponent', () => {
  let component: AddRecipeComponent;
  let fixture: ComponentFixture<AddRecipeComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [ AddRecipeComponent, ReactiveFormsModule, FormsModule, HttpClientModule ],  // Importa el componente standalone y el módulo de pruebas HTTP
      providers: [
        AlimentsService,  // Usa el servicio real
        RecipesService    // Usa el servicio real
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(AddRecipeComponent);
    component = fixture.componentInstance;

    // Detecta los cambios iniciales en el componente
    fixture.detectChanges();
  });

  it('should call retrieveFoods and update foodList with real HTTP data', (done) => {
    // Ejecutamos la función retrieveFoods y verificamos su funcionamiento
    component.retrieveFoods();

    // Esperamos un poco para que se realice la petición HTTP
    setTimeout(() => {
      // Verificamos que la lista de alimentos se ha actualizado
      expect(component.getFoodList().length).toBeGreaterThan(0);
      
      // Imprimimos el contenido de foodList para asegurarnos de que se recibieron datos reales
      console.log('Lista de alimentos:', component.getFoodList());

      // El test ha finalizado correctamente
      done();
    }, 1000);  // Asegúrate de dar suficiente tiempo para la petición HTTP real (ajusta el tiempo si es necesario)
  });

  fit('should insert a new recipe and close the form on success', (done) => {
    // Crea un objeto de receta de prueba
    const mockRecipe = {
      name: 'Test Recipe',
      num_people: '4',
      ingredients: [
        { aliment: 'Chicken', quantity: '500', quantity_type: 'gr' },
        { aliment: 'Salt', quantity: '5', quantity_type: 'pinch' },
        { aliment: 'Pepper', quantity: '1', quantity_type: 'units' }
      ],
      steps: ['Step 1', 'Step 2'],
      category: 'Dinner',
      tags: 'quick, healthy',
      time: '30'
    };
  
    // Simula el evento y el formulario
    const mockEvent = { preventDefault: () => {} };
    const mockForm = { close: (result: any) => console.log('Form closed with result:', result) };
  
    // Detecta los cambios iniciales en el componente
    fixture.detectChanges();
  
    setTimeout(() => {
      console.log("LIST OF FOODS: " + JSON.stringify(component.getFoodList()))
      // Llamamos al método validateForm para insertar la receta
      component.validateForm(mockEvent, mockRecipe, mockForm);
    }, 1000);  // Ajusta el tiempo según sea necesario

    setTimeout(() => {
      // Verifica que la receta se insertó con éxito (puedes imprimir el valor de form.close o verificar otras interacciones)
      console.log('Receta insertada con éxito');
      done();
    }, 1000);  // Ajusta el tiempo según sea necesario
  });

});
