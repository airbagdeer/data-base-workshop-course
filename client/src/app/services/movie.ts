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
  genres: string[];
  cast: { id: number; name: string; character_name: string; profile_path: string }[];
  crew: { id: number; name: string; job: string; department: string }[];
}

@Injectable({
  providedIn: 'root'
})
export class MovieService {
  private apiUrl = 'http://localhost:8321';

  constructor(private http: HttpClient) { }

  searchMovies(query: string): Observable<Movie[]> {
    return this.http.get<Movie[]>(`${this.apiUrl}/search?q=${encodeURIComponent(query)}`);
  }

  getMovies(skip: number = 0, limit: number = 20): Observable<MovieDetail[]> {
    return this.http.get<MovieDetail[]>(`${this.apiUrl}/movies?skip=${skip}&limit=${limit}`);
  }

  getMovie(id: number): Observable<MovieDetail> {
    return this.http.get<MovieDetail>(`${this.apiUrl}/movies/${id}`);
  }

  getPosterUrl(id: number): string {
    return `${this.apiUrl}/movies/${id}/poster`;
  }

  rateMovie(id: number, rating: number, userId: string): Observable<{ message: string, vote_average: number, vote_count: number }> {
    return this.http.post<{ message: string, vote_average: number, vote_count: number }>(
      `${this.apiUrl}/movies/${id}/rate`,
      { rating, user_id: userId }
    );
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

  getFlops(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/flops`);
  }

  getDirectorActors(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/director-actors`);
  }

  getTopProductionCountries(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/top-production-countries`);
  }

  getKeywordRichMovies(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/keyword-rich-movies`);
  }

  getGenreHeavyMovies(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/history-war-movies`);
  }

  getBestYear(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/best-year`);
  }

  getMultiskilledCrew(): Observable<any> {
    return this.http.get(`${this.apiUrl}/analytics/multiskilled-crew`);
  }
}
