import React, { FormEvent, useState } from 'react';
import {Search} from 'react-feather'
import api from '../../api';
import MovieCard from '../../core/components/MovieCard';

type props = {
  isLogged: boolean
}

interface movie_interface {
  n :{
      id: number
      imageUrl: string
      overview: string
      release_date: string
      title: string
      vote_average: number
  }
}

const SearchMovie = ({isLogged} : props) => {
  const [movies, setMovies] = useState<movie_interface[]>()
  const [entrada, setEntrada] = useState("")

  const handleClick = (e: FormEvent) => {
    e.preventDefault()

    api.get(`/search/${entrada}`)
     .then(res => {setMovies(res.data)})
  }

  return (
    <>
      {!isLogged && <h3>Faça login para acessar esta página</h3>}
      { isLogged && 
          <div className="search-container">

          <div className="search-bar">
            <input 
                type="text" 
                required
                value={entrada} 
                placeholder="nome do filme" 
                onChange={e => setEntrada(e.target.value)}
            />
            <Search onClick={e => {handleClick(e)}}/>

          </div>

          <div className="movie-list">
          {
              movies === undefined ? '' :
                  movies.map(movie => {
                      return(
                          <MovieCard key={movie.n.id} id={movie.n.id} imagem={movie.n.imageUrl}/>
                      )
                  }) 
          }
          </div>
        </div>
      }
    </>
  );
}

export default SearchMovie;