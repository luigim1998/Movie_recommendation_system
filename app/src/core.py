import requests
import json
import time
from neo4j import GraphDatabase, basic_auth
from flask import Flask, jsonify, request, make_response, render_template
from flask_cors import CORS, cross_origin
from markupsafe import escape
from conf.settings import MOVIE_API

app = Flask(__name__)
CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

class createNode:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password), encrypted=False)

    def close(self):
        self.driver.close()
    
    def delete_duplicate(self):
        with self.driver.session() as session:
            create_user = session.write_transaction(self._delete_duplicate)
            return create_user

    @staticmethod
    def _delete_duplicate(tx):
        result = tx.run("MATCH (c:Filme) WITH c.idfilme AS filmes, COLLECT(c) AS filmes_repet WHERE SIZE(filmes_repet) > 1 UNWIND filmes_repet[1..] AS contact DETACH DELETE contact")
        return result.data()

    # criar filmes
    def create_films(self, id, genre_ids, title, overview, release_date, vote_average, imageUrl):
        with self.driver.session() as session:
            greeting = session.write_transaction(self._create_and_return_greeting, id, genre_ids, title, overview, release_date, vote_average, imageUrl)
            return greeting

    @staticmethod
    def _create_and_return_greeting(tx, id, genre_ids, title, overview, release_date, vote_average, backdrop_path):
        result = tx.run("MERGE (n:Filme {id_filme: $id}) ON CREATE SET n.genre_ids= $genre_ids, n.title= $title, n.overview= $overview, n.release_date= $release_date, n.vote_average= $vote_average, n.imageUrl= $backdrop_path ", id=id, genre_ids=genre_ids, title=title, overview=overview, release_date=release_date, vote_average=vote_average, backdrop_path=backdrop_path)
        # result = tx.run("CREATE (n:Filme {id_filme: $id, genre_ids: $genre_ids, title: $title, overview: $overview, release_date: $release_date, vote_average: $vote_average, imageUrl: $backdrop_path })", id=id, genre_ids=genre_ids, title=title, overview=overview, release_date=release_date, vote_average=vote_average, backdrop_path=backdrop_path)
        return result.data()

    # acha os filmes de um determinado g??nero (atrav??s do id do g??nero)
    def find_popular_genre(self, genre_ids):
        with self.driver.session() as session:
            find_popular_by_genre = session.read_transaction(self._find_popular_by_genre, genre_ids)
            return find_popular_by_genre
    
    @staticmethod
    def _find_popular_by_genre(tx, genre_ids):
        # query = "MATCH (f:Filme) WHERE f.genre_ids[0] ="+genre_ids+"RETURN f ORDER BY f.vote_average DESC"
        query = "MATCH (f:Filme) WHERE {} IN f.genre_ids RETURN id(f) as id, f.title as title, f.imageUrl as imageUrl ORDER BY f.vote_average DESC LIMIT 4".format(genre_ids)
        result = tx.run(query)
        return result.data()

    # cria usuario
    def create_user(self, name, username, password):
        with self.driver.session() as session:
            create_user = session.write_transaction(self._create_user, name, username, password)
            return create_user

    @staticmethod
    def _create_user(tx, name, username, password):
        result = tx.run('MERGE (n:Pessoa {{username: "{}" }}) ON CREATE SET n.name= "{}", n.password= "{}"'.format(username, name, password))
        #result = tx.run("CREATE (n:Pessoa {name: $name, username: $username, password: $password})", name=name, username=username, password=password)
        return result.data()

    # verifica se o usu??rio existe
    def verify_user_exist(self, username):
        with self.driver.session() as session:
            user_exists = session.read_transaction(self._verify_user_exist, username)
            return user_exists
    
    @staticmethod
    def _verify_user_exist(tx, username):
        query = 'MATCH (p:Pessoa {{username: "{}"}}) RETURN p.name as name, p.username as username'.format(username)
        result = tx.run(query)
        return result.data()
    
    # verifica se ?? a senha do usu??rio
    def verify_password(self, username, password):
        with self.driver.session() as session:
            verify = session.read_transaction(self._verify_password, username, password)
            return verify
    
    @staticmethod
    def _verify_password(tx, username, password):
        query = 'MATCH (p:Pessoa {{username: "{}"}}) RETURN p.password="{}" as resposta'.format(username, password)
        result = tx.run(query)
        return result.data()

    
    # achar filmes curtidos pelo usuario
    def find_by_user(self, username):
        with self.driver.session() as session:
            find_movie_by_user = session.read_transaction(self._find_movie_by_user, username)
            return find_movie_by_user
    
    @staticmethod
    def _find_movie_by_user(tx, username):
        result = tx.run('MATCH (f:Filme)<-[:CURTIU]-(n:Pessoa) WHERE n.username = "{}" RETURN id(f) as id, f.title as title, f.imageUrl as imageUrl'.format(username))
        print(result)
        return result.data()

    #recomenda filmes baseado nos filmes que os outros usuarios curtiram, para isso ele analisa os filmes que os usuarios assistiram e que o usuario viu tambem
    def find_by_like(self, username):
        with self.driver.session() as session:
            find_movie_by_like = session.read_transaction(self._find_movie_by_like, username)
            return find_movie_by_like
    
    @staticmethod
    def _find_movie_by_like(tx, username):
        query = 'MATCH (p:Pessoa)-[:CURTIU]->(f:Filme)<-[:CURTIU]-(p2:Pessoa)-[:CURTIU]->(f2:Filme) WHERE p.username = "{}" WITH f2 WHERE NOT (p)-[:CURTIU]->(f2) RETURN id(f2) as id,f2.title as title, f2.imageUrl as imageUrl, COUNT(f2) as f2_t ORDER BY f2_t DESC LIMIT 4'.format(username)
        result = tx.run(query)
        return result.data()

    # usuario curte determinado filme
    def like_movie(self, username, movie_id):
        with self.driver.session() as session:
            movie_liked = session.write_transaction(self._like_movie, username, movie_id)
            return movie_liked

    @staticmethod
    def _like_movie(tx, username, movie_id):
        query = 'MATCH (p:Pessoa), (f:Filme) WHERE p.username = "{}" AND id(f) = {} MERGE (p)-[:CURTIU]->(f)'.format(username, movie_id)
        result = tx.run(query)
        return result.data()
    
    # descurtir filme
    def dislike_movie(self, username, movie_id):
        with self.driver.session() as session:
            movie_disliked = session.write_transaction(self._dislike_movie, username, movie_id)
            return movie_disliked

    @staticmethod
    def _dislike_movie(tx, username, movie_id):
        query = 'MATCH (p:Pessoa)-[c:CURTIU]->(f:Filme) WHERE p.username = "{}" AND id(f) = {} DELETE c'.format(username, movie_id)
        result = tx.run(query)
        return result.data()

    # mostra todos os usuarios
    def show_users(self):
        with self.driver.session() as session:
            users = session.read_transaction(self._show_users)
            return users
    
    @staticmethod
    def _show_users(tx):
        query = "MATCH (n:Pessoa) RETURN id(n) as id, n.name as name, n.username as username"
        result = tx.run(query)
        return result.data()
    
    # recomendar filmes que outros usuarios baseados no filme
    def recommend_movie_by_movie(self, movie_id):
        with self.driver.session() as session:
            movies = session.read_transaction(self._recommend_movie_by_movie, movie_id)
            return movies
    
    @staticmethod
    def _recommend_movie_by_movie(tx, movie_id):
        query = "MATCH (f:Filme)<-[:CURTIU]-(p2:Pessoa)-[:CURTIU]->(f2:Filme) WHERE id(f) = {} AND id(f2) <> {} RETURN id(f2) as id,f2.title as title, f2.imageUrl as imageUrl".format(movie_id, movie_id)
        result = tx.run(query)
        return result.data()

    def search_movie_by_id(self, movie_id):
        with self.driver.session() as session:
            search_movie = session.read_transaction(self._search_movie_by_id, movie_id)
            return search_movie
    
    @staticmethod
    def _search_movie_by_id(tx, movie_id):
        query = "MATCH (f:Filme) WHERE id(f) = {} RETURN f, id(f) as id".format(movie_id)
        result = tx.run(query)
        return result.data()
    
    # def get_user_data(self, username):
    #     with self.driver.session() as session:
    #         user_data = session.read_transaction(self._get_user_data, username)
    #         return user_data

    # @staticmethod
    # def _get_user_data(tx, username):
    #     query = 'MATCH (n:Pessoa) WHERE n.username = "{}" return n.name as name, n.username as username, n.password as password, id(n) as id'.format(username)
    #     result = tx.run(query)
    #     return result.data()
    
    # verifica se o usu??rio j?? curtiu esse filme
    def verify_user_liked(self, username, movie_id):
        with self.driver.session() as session:
            exists = session.read_transaction(self._verify_user_liked, username, movie_id)
            return exists
    
    @staticmethod
    def _verify_user_liked(tx, username, movie_id):
        query = 'MATCH (p:Pessoa {{username: "{}"}}), (f:Filme) WHERE id(f)={} RETURN exists((f)<-[:CURTIU]-(p))'.format(username, movie_id)
        result = tx.run(query)
        return result.data()

    def get_film_by_name(self, movie_name):
        with self.driver.session() as session:
            movies = session.read_transaction(self._get_film_by_name , movie_name)
            return movies
    
    @staticmethod
    def _get_film_by_name(tx, movie_name):
        aux = ".*(?i){}.*".format(str(movie_name))
        query = "MATCH (n: Filme) WHERE n.title =~ \"{}\" return n, id(n) as id".format(aux)
        result = tx.run(query)
        return result.data()


############## front end requests ##############

# GET movie by gender
@app.route('/gender/<int:genre_id>', methods=['GET'])
@cross_origin()
def api_genre_id(genre_id):
    if request.method == 'GET':
        return jsonify(greeter.find_popular_genre(genre_id))

@app.route("/search/<movie_name>", methods=['GET'])
@cross_origin()
def api_search_movie_by_name(movie_name):
    if request.method == 'GET':
        return jsonify(greeter.get_film_by_name(movie_name))

# GET movie by user
@app.route("/movies/<username>", methods=['GET'])
@cross_origin()
def api_user_like_movie(username):
    if request.method == 'GET':
        return jsonify(greeter.find_by_user(username))

# GET movie details
@app.route('/movieDetails/<int:movie_id>', methods=['GET'])
@cross_origin()
def api_movie_details(movie_id):
    if request.method == 'GET':
        return jsonify(greeter.search_movie_by_id(movie_id))

# GET movies by user movies
@app.route('/moviesRecommended/<username>', methods=['GET'])
@cross_origin()
def api_movie_by_like(username):
    if request.method == 'GET':
        return jsonify(greeter.find_by_like(username))

# GET movies by movie
@app.route('/moviesByMovie/<int:movie_id>', methods=['GET'])
@cross_origin()
def api_recommend_movie_by_movie(movie_id):
    if request.method == 'GET':
        return jsonify(greeter.recommend_movie_by_movie(movie_id))

# POST like movie or DELETE dislike movie
@app.route('/likeMovie/<username>/<int:movie_id>', methods=['POST', 'DELETE'])
@cross_origin()
def api_like_movie(username, movie_id):
    if request.method == 'POST':
        greeter.like_movie(username, movie_id)
        return 'OK', 201

    if request.method == 'DELETE':
        greeter.dislike_movie(username, movie_id)
        res = make_response(jsonify({}), 204)
        return res

# GET all users or POST create user
@app.route('/users', methods=['GET', 'POST'])
@cross_origin()
def api_users():
    if request.method == 'GET':
        return jsonify(greeter.show_users())

    if request.method == 'POST':
        # print(request.is_json)
        content = request.json
        greeter.create_user(content['name'], content['username'], content['password'])
        return 'OK', 201

# GET user exist
@app.route('/user/<username>', methods=['GET'])
@cross_origin()
def api_user(username):
    if request.method == 'GET':
        return jsonify(greeter.verify_user_exist(username))

# GET user exist
@app.route('/user/<username>/<password>', methods=['GET'])
@cross_origin()
def api_user_password(username, password):
    if request.method == 'GET':
        return jsonify(greeter.verify_password(username, password))

############## the end ##############

if __name__ == "__main__":
    start = time.time()

    global greeter
    greeter = createNode("bolt://host.docker.internal:7687/", "neo4j", "")
    for page in range(1, 3):
        res = requests.get('https://api.themoviedb.org/3/movie/popular?api_key='+ MOVIE_API + '&page='+str(page))
        response = json.loads(res.text)

        for filme in range(0,len(response['results'])):
            results = response['results'][filme]

            if ('id' in results) and ('original_title' in results) and ('overview' in results) and ('release_date' in results) and ('vote_average' in results) and ('poster_path' in results):
                # if results['genre_ids'] == []:
                    # print(results['original_title'])
                if results['poster_path'] == None and results['genre_ids'] != []:
                    greeter.create_films(results['id'],results['genre_ids'], results['original_title'], results['overview'], results['release_date'], results['vote_average'], "Image not found")
                    
                else:
                    if results['genre_ids'] != []:
                        greeter.create_films(results['id'],results['genre_ids'], results['original_title'], results['overview'], results['release_date'], results['vote_average'], "https://image.tmdb.org/t/p/w500/"+results['poster_path'])

            else:
                continue
    
    # greeter.delete_duplicate()
    greeter.create_user("Luigi Muller", "luigim1998", 'luluzinho')
    # greeter.create_user("Liigi Mylena", "luigim1998", 'luluzinho')
    # print("Verifica luigim1998", greeter.verify_user_exist("luigim1998"))
    # print("Verifica ttzeo", greeter.verify_user_exist("ttzeo"))
    # print("Verifica senha: luigim1998, luluzinho", greeter.verify_password("luigim1998", "luluzinho"))
    # print("Verifica senha: luigim1998, lulu", greeter.verify_password("luigim1998", "lulu"))
    greeter.create_user("Miller", "ttezo", 'Tarlisonzinho')
    greeter.create_user("Pedro Aleph", "pedroaleph", 'password')
    greeter.create_user("Talirson", "magictorto", 'hatsunemiku')
    greeter.create_user("Leandro", "balico", 'kubernates')
    greeter.create_user("Joshua", "joshua", 'joshua')
    greeter.create_user("Victor", "rocha", 'barbosa')
    greeter.create_user("Franscisco", "chico", 'chicael')
    greeter.create_user("Ewelly", "ewelly", 'ewelly')
    greeter.create_user("Josemar", "jukka", 'rodrigo')
    
    # greeter.like_movie("luigim1998", 10)
    # print("luigim1998 gostou de filme 10", greeter.verify_user_liked("luigim1998", 11))
    # print("luigim1998 gostou de filme 11", greeter.verify_user_liked("luigim1998", 10))

    greeter.like_movie("pedroaleph", 0)
    greeter.like_movie("pedroaleph", 2)
    greeter.like_movie("pedroaleph", 24)
    greeter.like_movie("rocha", 24)
    greeter.like_movie("rocha", 6)
    greeter.like_movie("rocha", 5)
    greeter.like_movie("joshua", 5)
    greeter.like_movie("magictorto", 5)
    greeter.like_movie("balico", 5)
    greeter.like_movie("chico", 5)
    greeter.like_movie("jukka", 6)
    greeter.like_movie("ewelly", 26)
    greeter.like_movie("luigim1998", 6)
    greeter.like_movie("luigim1998", 9)
    greeter.like_movie("ttezo", 9)
    greeter.like_movie("ttezo", 14)
    greeter.like_movie("ttezo", 16)
    
    # print("Filmes populares do g??nero 12", greeter.find_popular_genre(12))
    # print("Filmes gostados por ttezo", greeter.find_by_user("ttezo"))
    # greeter.dislike_movie("ttezo", 17)
    # print("Filmes gostados por ttezo", greeter.find_by_user("ttezo"))
    # print("Filmes recomendados por luigim1998", greeter.find_by_like("luigim1998"))
    # print("Filmes recomendados pelo filme 15", greeter.recommend_movie_by_movie(15))
    # print("Nomes dos usu??rios", greeter.show_users())
    # print("Filme 12", greeter.search_movie_by_id(12))

    end = time.time()
    print("tempo", end - start)

    app.run(host="0.0.0.0", debug=True)
    greeter.close()
