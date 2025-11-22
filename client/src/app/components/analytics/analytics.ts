import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MovieService } from '../../services/movie';

@Component({
  selector: 'app-analytics',
  standalone: true,
  imports: [CommonModule],
  templateUrl: './analytics.html',
  styleUrl: './analytics.css'
})
export class AnalyticsComponent implements OnInit {
  popularGenres: any[] = [];
  topActors: any[] = [];
  avgRuntime: any[] = [];

  constructor(private movieService: MovieService) { }

  ngOnInit(): void {
    this.movieService.getPopularGenres().subscribe(data => this.popularGenres = data);
    this.movieService.getTopActors().subscribe(data => this.topActors = data);
    this.movieService.getAverageRuntime().subscribe(data => this.avgRuntime = data);
  }
}
