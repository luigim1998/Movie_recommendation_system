import './styles.scss';

const Create = () => {
    return (  
        <div className="create">
            <h3>Novo Usuário</h3>
            <form>
                <label>Nome:</label>
                <input 
                    type="text"
                    placeholder="seu nome"
                />
                <label>Nome de Usuário:</label>
                <input 
                    type="text"
                    placeholder="escolha um apelido"
                />
                <label>Senha:</label>
                <input 
                    type="text"
                    placeholder="senha"
                />
                <button 
                    type="submit"
                    value="Enviar" 
                    // onClick={(e) => 
                    // handleSubmit(e)}
                    >
                    Criar Usuário
                </button>
            </form>
        </div>
    );
}
 
export default Create;