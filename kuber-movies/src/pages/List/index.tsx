import './styles.scss';
import MovieCard from '../../core/components/MovieCard';
import { useEffect, useState } from 'react';
import api from '../../api';

type props = {
    isLogged: boolean
}

interface movie{
    id: number,
    imageUrl: string,
    title: string
}

const List = ({isLogged} : props) => {
    const user = localStorage.getItem("user")
    const [filmes, setFilmes] = useState<movie[]>()

    useEffect(() => {
        api.get(`/movies/${user}`)
            .then(res => setFilmes(res.data))
    },[user])

    return (
        <>
            {!isLogged && <h3>Faça login para acessar esta página</h3>}
            { isLogged && 
                <div className="list-container">
                    <h4 className="movie-list-title">Sua Lista de Filmes, {user}:</h4>
                    <div className="movie-list">
                        {
                            filmes === undefined ? '' :
                                filmes.map(filme => {
                                    return(
                                        <MovieCard key={filme.id} id={filme.id} imagem={filme.imageUrl}/>
                                    )
                                }) 
                        }
                    </div>
                </div>
            }
        </>
    );
}
 
export default List;