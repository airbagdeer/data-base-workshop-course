import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ActivatedRoute, RouterModule } from '@angular/router';
import { FormsModule } from '@angular/forms';
import { MovieService, MovieDetail } from '../../services/movie';

@Component({
  selector: 'app-movie-detail',
  standalone: true,
  imports: [CommonModule, RouterModule, FormsModule],
  templateUrl: './movie-detail.html',
  styleUrl: './movie-detail.css'
})
export class MovieDetailComponent implements OnInit {
  movie: MovieDetail | null = null;
  userRating: number = 0;
  message: string = '';

  constructor(
    private route: ActivatedRoute,
    private movieService: MovieService
  ) { }

  ngOnInit(): void {
    const id = Number(this.route.snapshot.paramMap.get('id'));
    if (id) {
      this.movieService.getMovie(id).subscribe(movie => {
        this.movie = movie;
      });
    }
  }

  getPoster(): string {
    return this.movie ? this.movieService.getPosterUrl(this.movie.id) : '';
  }

  submitRating(): void {
    if (this.movie && this.userRating > 0 && this.userRating <= 10) {
      this.movieService.rateMovie(this.movie.id, this.userRating).subscribe({
        next: () => {
          this.message = 'Rating submitted successfully!';
          // Optionally refresh movie data
        },
        error: () => {
          this.message = 'Error submitting rating.';
        }
      });
    }
  }
}
