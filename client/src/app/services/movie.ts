import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

export interface Movie {
  id: number;
  title: string;
  original_title: string;
  overview: string;
  release_date: string;
  runtime: number;
  budget: number;
  revenue: number;
  popularity: number;
  vote_average: number;
  vote_count: number;
  status: string;
  tagline: string;
}

export interface MovieDetail extends Movie {
  genres: { id: number; name: string }[];
  cast: { id: number; name: string; character: string; profile_path: string }[];
  crew: { id: number; name: string; job: string; department: string }[];
}

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl = 'http://localhost:8000';

  constructor(private http: HttpClient) { }

  getMovies(skip: number = 0, limit: number = 20): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/movies?skip=${skip}&limit=${limit}`);
  }

  getMovie(id: number): Observable<MovieDetail> {
    return this.http.get<MovieDetail>(`${this.apiUrl}/movies/${id}`);
  }

  getPosterUrl(id: number): string {
    return `${this.apiUrl}/movies/${id}/poster`;
  }

  rateMovie(id: number, rating: number): Observable<any> {
    return this.http.post(`${this.apiUrl}/movies/${id}/rate`, { rating });
  }

  // Analytics
  getPopularGenres(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/popular-genres`);
  }

  getTopActors(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/top-actors`);
  }

  getAverageRuntime(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/average-runtime-by-genre`);
  }
}
