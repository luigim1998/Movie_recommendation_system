import React, { FormEvent, useState } from 'react';
import { useHistory, Link } from 'react-router-dom';
import api from '../../api';
import './styles.scss';

const Login = () => {
    const history = useHistory();
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isExist, setIsExist] = useState(false);
    const [name, setName] = useState('');
    const [isLogged, setIsLogged] = useState(false);


    const handleSubmit = (e: FormEvent) =>{
        e.preventDefault()

        api.get(`user/${username}`)
        .then(res => {
            const user = res.data;
            if (user.length !== 0){
                setName(user[0]['name']);
                setIsExist(true);
            }
            else{
                alert('usuário inexistente!');
            }
        });

        if (isExist === true){
            api.get(`user/${username}/${password}`)
            .then( res => {
                const pass = res.data[0]['resposta'];
                if(pass){
                    setIsLogged(true);
                    localStorage.setItem("user", username);
                    history.push('/')
                }
                else{
                    alert('senha incorreta!');
                }
            })
        }
    }

    const handleLeave = (e: FormEvent) => {
        e.preventDefault()

        setName('');
        setUsername('');
        setPassword('');
        setIsExist(false);
        setIsLogged(false);
    }

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
                            onChange={e => setUsername(e.target.value)}
                        />
                        <label>Senha:</label>
                        <input 
                            type="password"
                            required
                            placeholder="senha" 
                            value={password}
                            onChange={e => setPassword(e.target.value)}
                        />

                        <button 
                            type="submit"
                            value="Enviar" 
                            onClick={(e) => 
                            handleSubmit(e)}>
                            Entrar
                        </button>
                    </form>
                    <Link to="/create" className="create-user">criar usuário</Link>
                </>
            }
            { isLogged && 
                <>
                <h3>Bem Vindo, {name}</h3>
                <p>
                    Aqui você pode : <br />
                    - ver a sua lista de filmes <br />
                    - ver as recomendações de filmes para você <br />
                    - ver detalhes do seu filme favorito <br />
                    - ver as recomendações do seu filme favorito <br />
                    - adicionar filmes a sua lista de filmes buscando pelo gênero
                </p>
                <button onClick={handleLeave} >Sair</button>
                </>
            }
        </div>
    );    
}

export default Login;