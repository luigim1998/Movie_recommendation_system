import { useHistory, useLocation } from 'react-router-dom';
import { FormEvent, useEffect, useState } from 'react';
import {ThumbsUp, ThumbsDown} from 'react-feather';

import api from '../../../../api';
import MovieCard from '../../../../core/components/MovieCard';
import './styles.scss';

type props = {
    isLogged: boolean
}

interface movie_interface {
    f : {
        id: number
        imageUrl: string
        overview: string
        release_date: string
        title: string
        vote_average: number
    }
}

interface filme{
    id: number,
    imageUrl: string,
    title: string
}

const MovieDetails = ({isLogged}: props) => {
    const history = useHistory();
    const location = useLocation<{id: number}>();
    const id = location.state.id;

    const [movie, setMovie] = useState<movie_interface[]>()
    const [recomendados, setRecomendados] = useState<filme[]>()

    const handleLike = (e: FormEvent) => {
        e.preventDefault()

        api.post(`/likeMovie/${localStorage.getItem('user')}/${id}`)
            .then(res => console.log(res.data))
        alert(`Filme adicionado a sua lista`)
    }

    const handleDislike = (e: FormEvent) => {
        e.preventDefault()

        api.delete(`/likeMovie/${localStorage.getItem('user')}/${id}`)
            .then(res => console.log(res.data))
        alert(`Filme removido da sua lista`)
    }

    
    useEffect(()=>{
        api.get(`/movieDetails/${id}`)
        .then(res => {setMovie(res.data); console.log(res.data)});

        api.get(`/moviesByMovie/${id}`)
            .then(res => {setRecomendados(res.data); console.log(res.data)})
    },[id])
    
    return ( 
        <>
            {!isLogged && <h3>Faça login para acessar esta página</h3>}
            { isLogged &&
                <div className="movie-details-container">
                    <button 
                        className="goback-btn-container goback-btn bg-primary"
                        onClick={() => { history.push("/list")}}
                        >
                            voltar 
                    </button>
                    <div className="row">
                        {
                            movie === undefined ? '' :
                                <div className="row col-6">
                                    <div className="movie-details-title col-6">
                                        <h2>{movie[0]['f']['title']}</h2>
                                        <p>Data de Laçamento : {movie[0]['f']['release_date']} </p>
                                        {/* <p>Gêneros : {movie.}</p> */}
                                        <p>Avaliação: {movie[0]['f']['vote_average']}%</p>
                                    </div>
            
                                    <div className="movie-details-img col-6">
                                        <img src={movie[0]['f']['imageUrl']} alt="" />
                                    </div>
                                    <div className="movie-details-synopsis">
                                        <h3>Sinopse</h3>
                                        <p>
                                        {movie[0]['f']['overview']}
                                        </p>
                                    </div>
            
                                    <div className="like">
                                        <ThumbsUp color="white" size={24} onClick={e => handleLike(e)}/>
                                        <ThumbsDown color="white" size={24} onClick={e => handleDislike(e)}/>
                                    </div>
                                </div>
                        }
                        <div className="col-6">
                            <h4>Recomendações: </h4>
                            <div className="recommedation-card-movie">
                                {
                                    recomendados === undefined ? '' :
                                        recomendados.map(rec => {
                                            return(
                                                <MovieCard key={id} id={id} imagem={rec.imageUrl}/>
                                            )
                                        })
                                }
                            </div>
                        </div>
                    </div>
                </div>
            }
        </>
    );
}
 
export default MovieDetails;