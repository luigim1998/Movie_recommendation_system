import './styles.scss';
import { Link, useHistory } from 'react-router-dom';
import { FormEvent } from 'react';

interface props{
    imagem: string,
    id:number
}

const MovieCard = (prop: props) => {  
    const history = useHistory()

    const handleSubmit = (e: FormEvent) =>{
        e.preventDefault()
        history.push('/movie', {id: prop.id})
    }
    return ( 
        <Link to="/movie" className="movie-card" onClick={e=> handleSubmit(e)}>
            {
                <img src={prop.imagem} alt="" />
            }
        </Link>
    );
}
 
export default MovieCard;