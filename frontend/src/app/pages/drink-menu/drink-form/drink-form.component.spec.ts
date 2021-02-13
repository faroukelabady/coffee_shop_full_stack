import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed, getTestBed } from '@angular/core/testing';
import { ModalController } from '@ionic/angular';
import { DrinkFormComponent } from './drink-form.component';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DrinksService } from 'src/app/services/drinks.service';

describe('DrinkFormComponent', () => {
  let component: DrinkFormComponent;
  let fixture: ComponentFixture<DrinkFormComponent>;
  let modalSpy = jasmine.createSpyObj('Modal', ['present']);
  let modalCtrlSpy = jasmine.createSpyObj('ModalController', ['create']);
  modalCtrlSpy.create.and.callFake(function () {
    return modalSpy;
  });
  let injector: TestBed;
  let service: DrinksService;
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DrinkFormComponent ],
      schemas: [CUSTOM_ELEMENTS_SCHEMA],
      providers: [
        { provide: ModalController, useValue: modalCtrlSpy},
      ],
      imports: [HttpClientTestingModule],
    })
    .compileComponents();
    injector = getTestBed();
    service = injector.get(DrinksService);
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(DrinkFormComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
