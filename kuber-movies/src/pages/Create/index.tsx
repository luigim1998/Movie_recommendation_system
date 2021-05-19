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

        // api.get(`/user/${username}`)
        // .then( res => {
        //     const userDetails = res.data;
        //     if (userDetails.length === 0){
        //         alert("usuário cadastrado!")
        //     }
        //     else {
        //         setIsExist(true);
        //         alert("nome de usuário já existe!")
        //     }
        // })
        if (isExist === false){
            api.post('/users', {
                name: `${name}`,
                username: `${username}`,
                password: `${password}`
            })
            .then(() => {
                history.push('/');
            })
        }   

    }
    
    return (  
        <div className="create">
            <h3>Novo Usuário</h3>
            <form onSubmit={handleSubmit}>
                <label>Nome:</label>
                <input 
                    type="text"
                    placeholder="seu nome"
                    value={name}
                    onChange={(e) => setName(e.target.value)}
                />
                <label>Nome de Usuário:</label>
                <input 
                    type="text"
                    placeholder="escolha um apelido"
                    value={username}
                    onChange={(e) => setUsername(e.target.value)}
                />
                <label>Senha:</label>
                <input 
                    type="password"
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