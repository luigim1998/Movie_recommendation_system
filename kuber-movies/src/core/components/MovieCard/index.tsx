import './styles.scss';
import { Link } from 'react-router-dom';

 
const MovieCard = () => {
    return ( 
    <Link to="/list/1" className="movie-card">
        <img src="https://www.themoviedb.org/t/p/w600_and_h900_bestv2/klAIFewuqcyEmH1SMtR2XbMyqzM.jpg" alt="" />
    </Link>
    );
}
 
export default MovieCard;