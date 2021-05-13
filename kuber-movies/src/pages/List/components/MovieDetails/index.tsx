import './styles.scss';
//import MovieCard from '../../../../core/components/MovieCard';
import { Link } from 'react-router-dom';

const MovieDetails = () => {
    return ( 
        <div className="movie-details-container">
            <Link to="/list" className="goback-btn-container"><button className="goback-btn bg-primary">voltar </button></Link>
        <div className="row">
            <div className="row col-6">
                <div className="movie-details-title col-6">
                    <h2>Godzilla vs. Kong</h2>
                    <p>Data de Laçamento : 01/04/2021 </p>
                    <p>Gêneros : Ficção científica, Ação, Drama</p>
                    <p>Avaliação: 81%</p>
                </div>
                <div className="movie-details-img col-6">
                    <img src="https://www.themoviedb.org/t/p/w220_and_h330_face/klAIFewuqcyEmH1SMtR2XbMyqzM.jpg" alt="" />
                </div>
                <div className="movie-details-synopsis">
                    <h3>Sinopse</h3>
                    <p>
                    Em uma época em que os monstros andam na Terra,
                    a luta da humanidade por seu futuro coloca Godzilla e Kong
                    em rota de colisão que verá as duas forças mais poderosas da natureza no planeta
                    se confrontarem em uma batalha espetacular para as idades. Enquanto Monarch embarca
                    em uma missão perigosa em terreno desconhecido e descobre pistas sobre as origens dos Titãs,
                    uma conspiração humana ameaça tirar as criaturas,
                    boas e más, da face da terra para sempre.
                    </p>
                </div>
            </div>
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