import { TestBed } from '@angular/core/testing';
import { ModalService } from './modal.service';
import { Component, EventEmitter, Type, ViewContainerRef, ComponentRef } from '@angular/core';
import { Subject } from 'rxjs';

// Mock del componente modal para simular un modal con eventos
@Component({
  selector: 'app-mock-modal',
  template: ''
})
class MockModalComponent {
  close = new EventEmitter<void>();
  confirm = new EventEmitter<object>();
  data: any;  // propiedad de datos, usada en el test para inyectar data
}

fdescribe('ModalService', () => {
  let service: ModalService;
  let viewContainerRefSpy: jasmine.SpyObj<ViewContainerRef>;
  let componentRefSpy: ComponentRef<MockModalComponent>; // Define correctamente el ComponentRef con el mock del componente

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ModalService);

    // Crear un mock de ViewContainerRef
    viewContainerRefSpy = jasmine.createSpyObj('ViewContainerRef', ['createComponent']);

    // Crear un mock del ComponentRef
    componentRefSpy = {
        instance: new MockModalComponent(),  // Instancia del mock del componente modal
        destroy: jasmine.createSpy('destroy'),
        location: {} as any,  // Puedes mockear más cosas si lo necesitas
        changeDetectorRef: {} as any,
        injector: {} as any,
        hostView: {} as any,
        setInput: jasmine.createSpy('setInput'),
        componentType: MockModalComponent,  // Tipo del componente
        onDestroy: jasmine.createSpy('onDestroy') // Mock de la función onDestroy
      };

    // Simular que 'createComponent' retorna el mock del ComponentRef
    viewContainerRefSpy.createComponent.and.returnValue(componentRefSpy);
  });

  it('should open modal and set data', () => {
    const testData = { key: 'value' };

    // Abrir el modal con datos
    service.openModal(viewContainerRefSpy, MockModalComponent, testData);

    // Verificar que createComponent fue llamado
    expect(viewContainerRefSpy.createComponent).toHaveBeenCalled();

    // Verificar que el tipo de componente sea el esperado (usamos componentType)
    expect(componentRefSpy.componentType).toBe(MockModalComponent);

    // Verificar que los datos se hayan establecido correctamente en la instancia del componente
    expect(componentRefSpy.instance.data).toEqual(testData);
  });

  it('should emit close and destroy modal when close is called', () => {
    service.openModal(viewContainerRefSpy, MockModalComponent);

    // Simular que el evento close es emitido
    componentRefSpy.instance.close.emit();

    // Verificar que el componente fue destruido al cerrar el modal
    expect(componentRefSpy.destroy).toHaveBeenCalled();
  });

  it('should emit data on confirm and close modal', () => {
    const testData = { key: 'confirmValue' };

    // Abrir el modal
    const modalObservable = service.openModal(viewContainerRefSpy, MockModalComponent);

    // Simular que se confirma la acción en el modal
    componentRefSpy.instance.confirm.emit(testData);

    // Suscribirse para verificar que se emite el dato de confirmación
    modalObservable.subscribe((data) => {
      expect(data).toEqual(testData);
    });

    // Verificar que el modal se destruyó después de la confirmación
    expect(componentRefSpy.destroy).toHaveBeenCalled();
  });

  it('should close modal and complete observable when close is emitted', (done) => {
    const modalObservable = service.openModal(viewContainerRefSpy, MockModalComponent);

    // Simular que el evento close es emitido
    componentRefSpy.instance.close.emit();

    // Suscribirse al observable para detectar el cierre
    modalObservable.subscribe({
      complete: () => {
        expect(componentRefSpy.destroy).toHaveBeenCalled(); // Verificar que se destruyó
        done();
      }
    });
  });
});
