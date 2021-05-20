import React, { ReactEventHandler} from 'react';
import { Link } from 'react-router-dom';
import './styles.scss';

type props = {
    isLogged: boolean,
    name: string,
    username: string,
    password: string,
    setUsername: ReactEventHandler,
    setPassword: ReactEventHandler,
    handleSubmit: ReactEventHandler,
    handleLeave: ReactEventHandler
}

const Login = (
    {isLogged, name, username, password, setUsername, setPassword, handleSubmit, handleLeave}
     :props) => {
    
    return (
        <div className="login">
            { !isLogged && 
                <>
                    <h3>Login</h3>
                    <form>
                        <label>Usuário:</label>
                        <input 
                            type="text" 
                            required
                            value={username} 
                            placeholder="nome de usuário" 
                            onChange={setUsername}
                        />
                        <label>Senha:</label>
                        <input 
                            type="password"
                            required
                            placeholder="senha" 
                            value={password}
                            onChange={setPassword}
                        />

                        <button 
                            type="submit"
                            value="Enviar" 
                            onClick={(e) => handleSubmit(e)}
                            >
                            Entrar
                        </button>
                    </form>
                    <Link to="/create" className="create-user">criar usuário</Link>
                </>
            }
            { isLogged && 
                <>
                <h3>Bem Vindo, 
                    {name}
                </h3>
                <p>
                    Aqui você pode : <br />
                    - ver a sua lista de filmes <br />
                    - ver as recomendações de filmes para você <br />
                    - ver detalhes do seu filme favorito <br />
                    - ver as recomendações do seu filme favorito <br />
                    - adicionar filmes a sua lista de filmes buscando pelo gênero
                </p>
                <button
                    onClick={handleLeave}
                >
                    Sair
                </button>
                </>
            }
        </div>
    );    
}

export default Login;