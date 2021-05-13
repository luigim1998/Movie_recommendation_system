import { BrowserRouter, Switch , Route} from "react-router-dom";
import NavBar from "./core/components/NavBar";
import Gender from "./pages/Gender";
import List from "./pages/List";
import MovieDetails from "./pages/List/components/MovieDetails";

const Routes = () => {
    return ( 
        <BrowserRouter>
            <NavBar />
            <Switch>
            <Route path="/genres" exact>
                <Gender />
            </Route>
            <Route path="/list" exact>
                <List />
            </Route>
            <Route path="/list/1">
                    <MovieDetails />
            </Route>
            </Switch>
        </BrowserRouter>
     );
}
 
export default Routes;