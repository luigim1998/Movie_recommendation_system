import { BrowserRouter, Switch , Route} from "react-router-dom";
import NavBar from "./core/components/NavBar";
import Gender from "./pages/Gender";
import List from "./pages/List";
import MovieDetails from "./pages/List/components/MovieDetails";
import Login from "./pages/Login";
import Create from "./pages/Create";

const Routes = () => {
    return ( 
        <BrowserRouter>
            <NavBar />
            <Switch>
                <Route exact path="/">
                    <Login />
                </Route>
                <Route path="/create" exact>
                    <Create />
                </Route>
                <Route path="/genres" exact>
                    <Gender />
                </Route>
                <Route path="/list" exact>
                    <List />
                </Route>
                <Route path="/movie">
                        <MovieDetails />
                </Route>
            </Switch>
        </BrowserRouter>
     );
}
 
export default Routes;