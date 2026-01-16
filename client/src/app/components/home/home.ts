import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { firstValueFrom } from 'rxjs';
import { MovieService, Movie, MovieDetail } from '../../services/movie';

@Component({
  selector: 'app-home',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './home.html',
  styleUrl: './home.css'
})
export class HomeComponent {
  private readonly movieService = inject(MovieService);

  movies = signal<MovieDetail[]>([]);
  selectedGenres = signal<Set<string>>(new Set());
  searchQuery = signal<string>('');

  constructor() {
    firstValueFrom(this.movieService.getMovies(0, 100)).then(movies => {
      console.dir(movies);
      this.movies.set(movies);
    });
  }

   filteredMovies = computed(() => {
    const query = this.searchQuery();
    const selectedGenres = this.selectedGenres();
    
    return this.movies().filter(movie => {
      const matchesSearch = movie.title.toLowerCase().startsWith(query.toLowerCase());
      const matchesGenre = selectedGenres.size === 0 ||
        movie.genres.some(genre => selectedGenres.has(genre));
      return matchesSearch && matchesGenre;
    });
  });

   availableGenres = computed(() => {
    const genresSet = new Set<string>();
    this.movies().forEach(movie => {
      movie.genres.forEach(genre => genresSet.add(genre));
    });
    return Array.from(genresSet).sort();
  });

   toggleGenre(genre: string): void {
    const current = new Set(this.selectedGenres());
    if (current.has(genre)) {
      current.delete(genre);
    } else {
      current.add(genre);
    }
    this.selectedGenres.set(current);
  }

  isGenreSelected(genre: string): boolean {
    return this.selectedGenres().has(genre);
  }

  getPoster(id: number): string {
    return this.movieService.getPosterUrl(id);
  }
}
