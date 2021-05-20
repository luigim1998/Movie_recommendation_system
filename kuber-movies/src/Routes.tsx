import { BrowserRouter, Switch , Route} from "react-router-dom";
import NavBar from "./core/components/NavBar";
import Gender from "./pages/Gender";
import List from "./pages/List";
import MovieDetails from "./pages/List/components/MovieDetails";
import Login from "./pages/Login";
import Create from "./pages/Create";
import React, { FormEvent, useState } from "react";
import api from "./api";
import SearchMovie from './pages/Search';

const Routes = () => {
    const [isLogged, setIsLogged] = useState(false);
    const [username, setUsername] = useState('');
    const [password, setPassword] = useState('');
    const [isExist, setIsExist] = useState(false);
    const [name, setName] = useState('');

    const handlerStateUsername = (e: React.ChangeEvent<HTMLInputElement>) => {
        setUsername(e.target.value);
    }

    const handlerStatePassword = (e: React.ChangeEvent<HTMLInputElement>) => {
        setPassword(e.target.value);
    }

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
        })
        .then( () => {
            if (isExist){
                api.get(`user/${username}/${password}`)
                .then( res => {
                    const pass = res.data[0]['resposta'];
                    if(pass){
                        setIsLogged(true);
                        localStorage.setItem("user", username);
                    }
                    else{
                        alert('senha incorreta!');
                    }
                })
            }
        }
            
        )
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
        <BrowserRouter>
            <NavBar isLogged={isLogged}/>
            <Switch>
                <Route exact path="/">
                    <Login
                        isLogged={isLogged}
                        name={name}
                        username={username}
                        password={password}
                        setUsername={handlerStateUsername}
                        setPassword={handlerStatePassword}
                        handleSubmit={handleSubmit}
                        handleLeave={handleLeave}
                    />
                </Route>
                <Route exact path="/create">
                    <Create />
                </Route>
                <Route exact path="/genres">
                    <Gender isLogged={isLogged}/>
                </Route>
                <Route exact path="/list">
                    <List isLogged={isLogged}/>
                </Route>
                <Route exact path="/search">
                    <SearchMovie isLogged={isLogged}/>
                </Route>
                <Route exact path="/movie">
                        <MovieDetails isLogged={isLogged}/>
                </Route>
            </Switch>
        </BrowserRouter>
     );
}
 
export default Routes;