import { Routes } from '@angular/router';
import { HomeComponent } from './components/home/home';
import { MovieDetailComponent } from './components/movie-detail/movie-detail';
import { AnalyticsComponent } from './components/analytics/analytics';


export const routes: Routes = [
    { path: '', component: HomeComponent, pathMatch: 'full' },
    { path: 'movies/:id', component: MovieDetailComponent },
    { path: 'analytics', component: AnalyticsComponent },
    { path: '**', redirectTo: '' }
];

