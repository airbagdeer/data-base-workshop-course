import { Component, computed, inject, signal } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { toSignal } from '@angular/core/rxjs-interop';
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

  readonly movie = toSignal(
    this.route.paramMap.pipe(
      map(params => Number(params.get('id'))),
      switchMap(id => id ? this.movieService.getMovie(id) : of(null))
    ),
    { initialValue: null as MovieDetail | null }
  );

  readonly posterUrl = computed(() => {
    const m = this.movie();
    return m ? this.movieService.getPosterUrl(m.id) : '';
  });

  readonly topCast = computed(() => this.movie()?.cast.slice(0, 10) ?? []);

  readonly userRating = signal(0);
  readonly message = signal('');

  submitRating(): void {
    const movie = this.movie();
    const rating = this.userRating();
    if (movie && rating > 0 && rating <= 10) {
      this.movieService.rateMovie(movie.id, rating).subscribe({
        next: () => {
          this.message.set('Rating submitted successfully!');
        },
        error: () => {
          this.message.set('Error submitting rating.');
        }
      });
    }
  }
}
