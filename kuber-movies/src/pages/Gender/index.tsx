import { useEffect, useState } from 'react';
import api from '../../api';
import MovieCard from '../../core/components/MovieCard';
import './styles.scss';

interface movie{
    id: number,
    imageUrl: string,
    title: string
}

const Gender = () => {
    const [genero, setGenero] = useState(0);
    const [filmes, setFilmes] = useState<movie[]>()

    useEffect(()=>{
        api.get(`/gender/${genero}`)
            .then(res => setFilmes(res.data))
    },[genero])

    return (
        <div className="gender-container">
            <h4>Escolha seu Gênero:</h4>
            <div className="gender-btn-content">
                <button className="gender-btn" onClick={e =>{e.preventDefault(); setGenero(28)}}>Ação</button>
                <button className="gender-btn" onClick={e =>{e.preventDefault(); setGenero(12)}}>Aventura</button>
                <button className="gender-btn" onClick={e =>{e.preventDefault(); setGenero(878)}}>Ficção Cientifica</button>
                <button className="gender-btn" onClick={e =>{e.preventDefault(); setGenero(53)}}>Suspense</button>
                <button className="gender-btn" onClick={e =>{e.preventDefault(); setGenero(27)}}>Terror</button>
            </div>
            <h4 className="gender-movie-title">Filmes do Gênero:</h4>
            <div className="gender-movie">
                {
                    filmes === undefined ? '':
                        filmes.map( filme =>{
                            return(
                                <MovieCard key={filme.id} id={filme.id} imagem={filme.imageUrl}/>
                            )  
                        }  
                    )
                }
            </div>
        </div>
    );
}
 
export default Gender;