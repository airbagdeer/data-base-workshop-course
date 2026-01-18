import { Component, inject, AfterViewInit, ViewChildren, QueryList, ElementRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { toSignal } from '@angular/core/rxjs-interop';
import { MovieService } from '../../services/movie';
import { Chart, registerables } from 'chart.js';
import { forkJoin, pipe, first} from 'rxjs';

Chart.register(...registerables);

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics.html',
  styleUrl: './analytics.css'
})

export class AnalyticsComponent implements AfterViewInit {
  
  @ViewChildren('chartCanvas') chartCanvases!: QueryList<ElementRef<HTMLCanvasElement>>;
  
  private readonly movieService = inject(MovieService);
  private charts: Chart[] = [];

  private readonly chartsReady$ = forkJoin({
  popularGenres: this.movieService.getPopularGenres(),
  topActors: this.movieService.getTopActors(),
  avgRuntime: this.movieService.getAverageRuntime(),
  flops: this.movieService.getFlops(),
  directorActors: this.movieService.getDirectorActors(),
  topCountries: this.movieService.getTopProductionCountries(),
  keywordRichMovies: this.movieService.getKeywordRichMovies(),
  genreHeavyMovies: this.movieService.getGenreHeavyMovies(),
  bestYear: this.movieService.getBestYear(),
  multiskilledCrew: this.movieService.getMultiskilledCrew()
});

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

  ngAfterViewInit() {
    // Small delay to ensure DOM is ready
    setTimeout(() => {
      this.createCharts();
    }, 100);
  }

  ngOnDestroy() {
     this.chartsReady$
    .pipe(first())
    .subscribe(() => this.createCharts());
  }

  private createCharts() {
    const canvases = this.chartCanvases.toArray();
    let index = 0;

    // Chart 1: Popular Genres
    if (this.popularGenres().length > 0) {
      this.createBarChart(canvases[index++].nativeElement, 
        this.popularGenres().slice(0, 10).map((g: any) => g.genre),
        [{
          label: 'Movie Count',
          data: this.popularGenres().slice(0, 10).map((g: any) => g.movie_count),
          backgroundColor: '#8b5cf6'
        }]
      );
    }

    // Chart 2: Top Actors
    if (this.topActors().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.topActors().slice(0, 10).map((a: any) => a.actor_name),
        [{
          label: 'Movie Count',
          data: this.topActors().slice(0, 10).map((a: any) => a.movie_count),
          backgroundColor: '#6366f1'
        }]
      );
    }

    // Chart 3: Avg Runtime
    if (this.avgRuntime().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.avgRuntime().slice(0, 10).map((r: any) => r.genre),
        [{
          label: 'Avg Runtime (min)',
          data: this.avgRuntime().slice(0, 10).map((r: any) => r.avg_runtime),
          backgroundColor: '#10b981'
        }]
      );
    }

    // Chart 4: Flops (Multiple bars - Budget, Revenue, Loss)
    if (this.flops().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.flops().slice(0, 10).map((f: any) => f.title),
        [
          {
            label: 'Budget',
            data: this.flops().slice(0, 10).map((f: any) => f.budget),
            backgroundColor: '#3b82f6'
          },
          {
            label: 'Revenue',
            data: this.flops().slice(0, 10).map((f: any) => f.revenue),
            backgroundColor: '#10b981'
          },
          {
            label: 'Loss',
            data: this.flops().slice(0, 10).map((f: any) => f.loss),
            backgroundColor: '#ef4444'
          }
        ]
      );
    }

    // Chart 5: Top Countries
    if (this.topCountries().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.topCountries().slice(0, 10).map((c: any) => c.name),
        [{
          label: 'Movie Count',
          data: this.topCountries().slice(0, 10).map((c: any) => c.movie_count),
          backgroundColor: '#f59e0b'
        }]
      );
    }

    // Chart 6: Keyword Rich Movies
    if (this.keywordRichMovies().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.keywordRichMovies().slice(0, 10).map((k: any) => k.title),
        [{
          label: 'Keyword Count',
          data: this.keywordRichMovies().slice(0, 10).map((k: any) => k.keyword_count),
          backgroundColor: '#ec4899'
        }]
      );
    }

    // Chart 7: Genre Heavy Movies
    if (this.genreHeavyMovies().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.genreHeavyMovies().slice(0, 10).map((g: any) => g.title),
        [{
          label: 'Genre Count',
          data: this.genreHeavyMovies().slice(0, 10).map((g: any) => g.genre_count),
          backgroundColor: '#14b8a6'
        }]
      );
    }

    // Chart 8: Multiskilled Crew
    if (this.multiskilledCrew().length > 0) {
      this.createBarChart(canvases[index++].nativeElement,
        this.multiskilledCrew().slice(0, 10).map((m: any) => m.name),
        [{
          label: 'Department Count',
          data: this.multiskilledCrew().slice(0, 10).map((m: any) => m.dept_count),
          backgroundColor: '#a855f7'
        }]
      );
    }
  }

  private createBarChart(canvas: HTMLCanvasElement, labels: string[], datasets: any[]) {
    const chart = new Chart(canvas, {
      type: 'bar',
      data: {
        labels: labels,
        datasets: datasets
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            display: datasets.length > 1,
            labels: {
              color: '#fff'
            }
          }
        },
        scales: {
          y: {
            beginAtZero: true,
            ticks: {
              color: '#fff'
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          },
          x: {
            ticks: {
              color: '#fff',
              maxRotation: 45,
              minRotation: 45
            },
            grid: {
              color: 'rgba(255, 255, 255, 0.1)'
            }
          }
        }
      }
    });

    this.charts.push(chart);
  }
}