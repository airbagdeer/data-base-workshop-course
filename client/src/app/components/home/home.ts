import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { toSignal } from '@angular/core/rxjs-interop';
import { MovieService, Movie } from '../../services/movie';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent {
  private readonly movieService = inject(MovieService);

  readonly movies = toSignal(
    this.movieService.getMovies(0, 100),
    { initialValue: [] as Movie[] }
  );

  getPoster(id: number): string {
    return this.movieService.getPosterUrl(id);
  }
}
