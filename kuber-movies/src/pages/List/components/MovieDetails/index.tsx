import './styles.scss';
//import MovieCard from '../../../../core/components/MovieCard';
import { Link, useLocation } from 'react-router-dom';
import { useEffect, useState } from 'react';
import api from '../../../../api';

interface movie_interface {
    id: number
    imageUrl: string
    overview: string
    release_date: string
    title: string
    vote_average: number
}

const MovieDetails = () => {
    const location = useLocation<{id: number}>();
    const id = location.state.id;

    const [movie, setMovie] = useState<movie_interface>()
    
    useEffect(()=>{
        api.get(`/movieDetails/${id}`)
        .then(res => {setMovie(res.data); console.log(res.data)})
    },[id])
    
    return ( 
        <div className="movie-details-container">
            <Link to="/list" className="goback-btn-container"><button className="goback-btn bg-primary">voltar </button></Link>
        <div className="row">
            {
                movie === undefined ? '' :
                    <div className="row col-6">
                        <div className="movie-details-title col-6">
                            <h2>{movie.title}</h2>
                            <p>Data de Laçamento : {movie.release_date} </p>
                            {/* <p>Gêneros : {movie.}</p> */}
                            <p>Avaliação: {movie.vote_average}%</p>
                        </div>
                        <div className="movie-details-img col-6">
                            <img src={movie.imageUrl} alt="" />
                        </div>
                        <div className="movie-details-synopsis">
                            <h3>Sinopse</h3>
                            <p>
                            {movie.overview}
                            </p>
                        </div>
                    </div>
            }
            <div className="col-6">
                <h4>Recomendações: </h4>
                <div className="recommedation-card-movie">
                    <img src="https://www.themoviedb.org/t/p/w220_and_h330_face/klAIFewuqcyEmH1SMtR2XbMyqzM.jpg" alt="" />
                    <img src="https://www.themoviedb.org/t/p/w220_and_h330_face/klAIFewuqcyEmH1SMtR2XbMyqzM.jpg" alt="" />
                    <img src="https://www.themoviedb.org/t/p/w220_and_h330_face/klAIFewuqcyEmH1SMtR2XbMyqzM.jpg" alt="" />
                </div>
            </div>
        </div>
        </div>
    );
}
 
export default MovieDetails;