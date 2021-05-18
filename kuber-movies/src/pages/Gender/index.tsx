import './styles.scss';
// import MovieCard from '../../core/components/MovieCard';
const Gender = () => {
    return (
        <div className="gender-container">
            <h4>Escolha seu Gênero:</h4>
            <div className="gender-btn-content">
                <button className="gender-btn">Ação</button>
                <button className="gender-btn">Aventura</button>
                <button className="gender-btn">Ficção Cientifica</button>
                <button className="gender-btn">Suspense</button>
                <button className="gender-btn">Terror</button>
            </div>
            <h4 className="gender-movie-title">Filmes do Gênero:</h4>
            <div className="gender-movie">
                {/* <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard />
                <MovieCard /> */}
            </div>
        </div>
    );
}
 
export default Gender;