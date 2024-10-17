import { ComponentFixture, TestBed } from '@angular/core/testing';

import { WhitepaperComponent } from './whitepaper.component';

describe('WhitepaperComponent', () => {
  let component: WhitepaperComponent;
  let fixture: ComponentFixture<WhitepaperComponent>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [WhitepaperComponent]
    })
    .compileComponents();

    fixture = TestBed.createComponent(WhitepaperComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
