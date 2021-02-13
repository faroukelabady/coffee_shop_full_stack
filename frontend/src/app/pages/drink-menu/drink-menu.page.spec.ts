import { CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { async, ComponentFixture, TestBed, getTestBed } from '@angular/core/testing';
import { ModalController } from '@ionic/angular';
import { DrinkMenuPage } from './drink-menu.page';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { HttpClientTestingModule, HttpTestingController } from '@angular/common/http/testing';
import { DrinksService } from 'src/app/services/drinks.service';

describe('DrinkMenuPage', () => {
  let component: DrinkMenuPage;
  let fixture: ComponentFixture<DrinkMenuPage>;
  
  let injector: TestBed;
  let service: DrinksService;
  let modalSpy = jasmine.createSpyObj('Modal', ['present']);
  let modalCtrlSpy = jasmine.createSpyObj('ModalController', ['create']);
  modalCtrlSpy.create.and.callFake(function () {
    return modalSpy;
  });
  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ DrinkMenuPage ],
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
    fixture = TestBed.createComponent(DrinkMenuPage);
    component = fixture.componentInstance;
    fixture.detectChanges();
    
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
