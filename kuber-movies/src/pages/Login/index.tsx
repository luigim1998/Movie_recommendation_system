import React, { FormEvent, useState } from 'react';
import { useHistory, Link } from 'react-router-dom';
import api from '../../api';
import './styles.scss';

const Login = () => {
    const history = useHistory();
    const [user, setUser] = useState('');
    const [password, setPassword] = useState('');
    const [isExist, setIsExist] = useState(false);

    const handleSubmit = (e: FormEvent) =>{
        e.preventDefault()

        api.get(`user/${user}`)
        .then(res => {
            if (res.data.length !== 0){
                setIsExist(true);
            }
            else{
                alert('usuário inexistente!');
            }
        });

        if (isExist === true){
            api.get(`user/${user}/${password}`)
            .then( res => {
                const pass = res.data[0]['resposta'];
                if(pass){
                    localStorage.setItem("user", user)
                    history.push('/list')
                }
                else{
                    alert('senha incorreta!');
                }
            })
        }
    }

    return (
        <div className="login">
            <h3>Login</h3>
            <form>
                <label>Usuário:</label>
                <input 
                    type="text" 
                    value={user} 
                    placeholder="nome de usuário" 
                    onChange={e => setUser(e.target.value)}
                />
                <label>Senha:</label>
                <input 
                    type="password"
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
        </div>
    );    
}

export default Login;