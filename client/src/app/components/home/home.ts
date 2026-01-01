import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { toSignal } from '@angular/core/rxjs-interop';
import { firstValueFrom } from 'rxjs';
import { MovieService, Movie } from '../../services/movie';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent {
  private readonly movieService = inject(MovieService);

  movies = signal<Movie[]>([]);
  searchQuery = signal<string>('');

  constructor() {
    firstValueFrom(this.movieService.getMovies(0, 100)).then(movies => {
      this.movies.set(movies);
    });
  }

  // Computed signal for filtered movies
  filteredMovies = computed(() => {
    const query = this.searchQuery();
    return this.movies().filter(movie =>
      movie.title.toLowerCase().startsWith(query.toLowerCase())
    );
  });

  getPoster(id: number): string {
    return this.movieService.getPosterUrl(id);
  }
}
