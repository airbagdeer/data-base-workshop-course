import { Component, inject } from '@angular/core';
import { CommonModule } from '@angular/common';
import { toSignal } from '@angular/core/rxjs-interop';
import { MovieService } from '../../services/movie';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics.html',
  styleUrl: './analytics.css'
})
export class AnalyticsComponent {
  private readonly movieService = inject(MovieService);

  readonly popularGenres = toSignal(
    this.movieService.getPopularGenres(),
    { initialValue: [] as any[] }
  );
  readonly topActors = toSignal(
    this.movieService.getTopActors(),
    { initialValue: [] as any[] }
  );
  readonly avgRuntime = toSignal(
    this.movieService.getAverageRuntime(),
    { initialValue: [] as any[] }
  );

  readonly flops = toSignal(
    this.movieService.getFlops(),
    { initialValue: [] as any[] }
  );

  readonly directorActors = toSignal(
    this.movieService.getDirectorActors(),
    { initialValue: [] as any[] }
  );

  readonly topCountries = toSignal(
    this.movieService.getTopProductionCountries(),
    { initialValue: [] as any[] }
  );

  readonly keywordRichMovies = toSignal(
    this.movieService.getKeywordRichMovies(),
    { initialValue: [] as any[] }
  );

  readonly genreHeavyMovies = toSignal(
    this.movieService.getGenreHeavyMovies(),
    { initialValue: [] as any[] }
  );

  readonly bestYear = toSignal(
    this.movieService.getBestYear(),
    { initialValue: [] as any[] }
  );

  readonly multiskilledCrew = toSignal(
    this.movieService.getMultiskilledCrew(),
    { initialValue: [] as any[] }
  );
}
