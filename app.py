from flask import Flask, request, jsonify # type: ignore
import dados
 

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

@app.route('/', methods=['GET'])
def hello():
    return "Hello World!"

@app.route("/biblioteca', methods=['GET', 'POST']")
def manipula_livros (isbn=None):
        if request.method == "GET":
            if isbn:
                for l in biblioteca:
                    if l['isbn'] == isbn:
                        return l
                return jsonify(f"mensagem: ISBN: {isbn} não encontrado"), 404
            else:
                return biblioteca
        
        elif request.method == 'POST':
            novo_livro = request.get_json()
            biblioteca.append(novo_livro)
            dados.salvar_no_arquivo (biblioteca)
            return jsonify("Livro cadastrado com sucesso"), 201
        elif request.method == 'DELETE':
            for l in biblioteca:
                if l['isbn'] == isbn:
                    biblioteca.remove(l)
                    dados.salvar_no_arquivo (biblioteca)
                return "Livro deletado", 204
            return jsonify(f"mensagem: ISBN: (isbn) não encontrado"), 404
        elif request.method == 'PUT':
            alteracoes = request.get_json()
            for livro in biblioteca:
                if livro['isbn'] == isbn:
                    for key, value in alteracoes.items():
                        livro [key] = value
                    dados.salvar_no_arquivo (biblioteca)
                    return "Livro atualizado com sucesso", 200
            return "Livro não localizado", 404
        else:
            return jsonify("Solicitação não pode ser atendida"), 200
        
if __name__ == '__main__':
    app.run(debug=True)