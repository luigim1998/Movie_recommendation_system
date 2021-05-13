import './styles.scss';
import MovieCard from '../../core/components/MovieCard';

 
const List = () => {
    return (
        <div className="list-container">
            <h4 className="movie-list-title">Sua Lista de Filmes:</h4>
            <div className="movie-list">
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
            </div>
        </div>
    );
}
 
export default List;