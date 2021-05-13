import './styles.scss';
import { Link , NavLink} from 'react-router-dom';

function NavBar() {
    return (
        <nav className="row bg-primary main-nav">
        <div className="col-2">
            <Link to="/" className="nav-logo-txt">
                <h3>KuberMovies</h3>
            </Link>
        </div>
        <div className="col-6 offset-2">
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
            </ul>
        </div>
    </nav>
    );
  }
  
  export default NavBar
;