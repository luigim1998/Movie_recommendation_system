import { useState, FormEvent } from 'react';
import './styles.scss';
import api from '../../api';
import { useHistory } from 'react-router-dom';

const Create = () => {
    const [name, setName] = useState('');
    const [username, setUsername] = useState('');
    const [password, setPassord] = useState('');

    const [isExist, setIsExist] = useState(false);

    const history = useHistory();

    const handleSubmit = (e: FormEvent) => {
        e.preventDefault();

        api.get(`/user/${username}`)
        .then(res => {
            if(res.data.length !== 0){
                setIsExist(true);
                alert('usuário já existe!')
            }
        })
        .then(() => {
            if (!isExist){
                api.post('/users', {
                    name: `${name}`,
                    username: `${username}`,
                    password: `${password}`
                })
                .then(() => {
                    history.push('/');
                })
            } 
        })
    }
    
    return (  
        <div className="create">
            <h3>Novo Usuário</h3>
            <form onSubmit={handleSubmit}>
                <label>Nome:</label>
                <input 
                    type="text"
                    required
                    placeholder="seu nome"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <label>Nome de Usuário:</label>
                <input 
                    type="text"
                    required
                    placeholder="escolha um apelido"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <label>Senha:</label>
                <input 
                    type="password"
                    required
                    placeholder="crie uma senha"
                    value={password}
                    onChange={(e) => setPassord(e.target.value)}
                />
                <button>Criar Usuário</button>
            </form>
        </div>
    );
}
 
export default Create;