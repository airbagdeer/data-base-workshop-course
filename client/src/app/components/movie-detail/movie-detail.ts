import { Component, DestroyRef, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { takeUntilDestroyed } from '@angular/core/rxjs-interop';
import { map, of, switchMap } from 'rxjs';
import { MovieService, MovieDetail } from '../../services/movie';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './movie-detail.html',
  styleUrl: './movie-detail.css'
})
export class MovieDetailComponent {
  private readonly route = inject(ActivatedRoute);
  private readonly movieService = inject(MovieService);
  private readonly destroyRef = inject(DestroyRef);

  readonly movie = signal<MovieDetail | null>(null);

  readonly posterUrl = computed(() => {
    const m = this.movie();
    return m ? this.movieService.getPosterUrl(m.id) : '';
  });

  readonly topCast = computed(() => this.movie()?.cast.slice(0, 10) ?? []);

  readonly userRating = signal(0);
  readonly message = signal('');
  private userId = '';

  constructor() {
    this.userId = this.getUserId();
    this.loadMovieOnRouteChange();
  }

  private getUserId(): string {
    // Get or generate user ID from localStorage
    let userId = localStorage.getItem('cinelearn_user_id');
    if (!userId) {
      userId = 'user_' + Math.random().toString(36).substring(2, 15) + Math.random().toString(36).substring(2, 15);
      localStorage.setItem('cinelearn_user_id', userId);
    }
    return userId;
  }

  private loadMovieOnRouteChange(): void {
    this.route.paramMap
      .pipe(
        map(params => Number(params.get('id'))),
        switchMap(id => id ? this.movieService.getMovie(id) : of(null)),
        takeUntilDestroyed(this.destroyRef)
      )
      .subscribe(movie => {
        this.movie.set(movie);
        // Load user's existing rating if any
        if (movie) {
          const savedRating = localStorage.getItem(`rating_${movie.id}_${this.userId}`);
          if (savedRating) {
            this.userRating.set(Number(savedRating));
          } else {
            this.userRating.set(0);
          }
        }
      });
  }

  private refreshMovie(id: number): void {
    this.movieService.getMovie(id)
      .pipe(takeUntilDestroyed(this.destroyRef))
      .subscribe(movie => this.movie.set(movie));
  }

  submitRating(): void {
    const movie = this.movie();
    const rating = Number(this.userRating());
    if (movie && rating >= 0 && rating <= 10) {
      this.movieService.rateMovie(movie.id, rating, this.userId)
        .pipe(takeUntilDestroyed(this.destroyRef))
        .subscribe({
          next: (response) => {
            this.message.set('Rating submitted successfully!');
            // Save user's rating to localStorage
            localStorage.setItem(`rating_${movie.id}_${this.userId}`, rating.toString());
            // Update movie data with new vote statistics
            const updatedMovie = { ...movie, vote_average: response.vote_average, vote_count: response.vote_count };
            this.movie.set(updatedMovie);
          },
          error: () => {
            this.message.set('Rating should be a whole number between 0 and 10.');
          }
        });
    } else if (rating < 0 || rating > 10) {
      this.message.set('Please enter a rating between 0 and 10.');
    }
  }
}

