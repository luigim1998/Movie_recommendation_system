import React, { FormEvent, useState } from 'react';
import { useHistory, Link } from 'react-router-dom';
import api from '../../api';
import './styles.scss';

const Login = () => {
    const history = useHistory()
    const [user, setUser] = useState("")

    const handleSubmit = (e: FormEvent) =>{
        e.preventDefault()

        api.get('/users')
            .then(res => res.data)
            .then(users => {
                let entrou = 0;
                for (let i = 0; i < users.length; i++){
                    if (users[i]['username'] === user){
                        console.log(users[i]['username'])
                        localStorage.setItem("user", user)
                        history.push('/list')
                        entrou = 1
                        break
                    }
                }
                if (entrou === 0){
                    alert("Usuário não cadastrado")
                }
            })
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
                //     value={user} 
                //     onChange={e => setUser(e.target.value)}
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