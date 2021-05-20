import './styles.scss';
import { Link , NavLink} from 'react-router-dom';
import { useState } from 'react';

function NavBar() {

    const [isLogged] = useState(true);
    //setIsLogged(true);

    return (
        <nav className="row bg-primary main-nav">
        <div className="col-2">
            <Link to="/list" className="nav-logo-txt">
                <h3>KuberMovies</h3>
            </Link>
        </div>
        <div className="col-6 offset-2">
            { isLogged && 
                <ul className="main-menu">
                    <li>
                        <NavLink to="/genres">
                            GÊNERO
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/list">
                            LISTA
                        </NavLink>
                    </li>
                    <li>
                        <NavLink to="/search">
                            BUSCA
                        </NavLink>
                    </li>
                </ul>
            }
        </div>
    </nav>
    );
  }
  
  export default NavBar
;