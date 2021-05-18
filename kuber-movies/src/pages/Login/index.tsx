import React, { FormEvent, useState } from 'react';
import { useHistory } from 'react-router-dom';
import api from '../../api';

const Login: React.FC = () => {
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
        <form>
            <label>
            login
            <input type="text" value={user} onChange={e => setUser(e.target.value)} />
            </label>

            <button type="submit" value="Enviar" onClick={(e) => handleSubmit(e)}>Entrar</button>
        </form>
    );    
}

export default Login;