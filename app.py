from flask import Flask, jsonify, request, render_template, send_from_directory, redirect, url_for # type: ignore
import dados

biblioteca = dados.carregar_do_arquivo()

app = Flask(__name__)

def deletar_livro(isbn):
    for l in biblioteca:
        if l['isbn'] == isbn:
            biblioteca.remove(l)
            dados.salvar_no_arquivo(biblioteca)
            return True
    return False

# Rotas para CSS, JS, Media e afins
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/media/<path:path>')
def serve_media(path):
    return send_from_directory('media', path)

# Rota padrão hello, world!
@app.route('/')
def hello():
    return render_template('hello.html')

# Rota de teste para entrada de dados via uri e escrita na página
@app.route('/<nome>')
def meu_nome(nome=None):
    return render_template('meunome.html', nome=nome)

# Rotas de API - Utilizando o prefixo /api
@app.route('/api/biblioteca', methods=['GET', 'POST'])
@app.route('/api/biblioteca/<isbn>', methods=['GET', 'DELETE', 'PUT'])
def manipula_livros(isbn=None):
    """ Função API para Biblioteca
    """
    if request.method == 'GET':
        if isbn:
            for l in biblioteca:
                if l['isbn'] == isbn:
                    return jsonify(l)
            return jsonify("message: livro não localizado"), 404
        else:
            return jsonify(biblioteca)
    elif request.method == 'POST':
        novo_livro = request.get_json()
        for l in biblioteca:
            if l['isbn'] == novo_livro['isbn']:
                return jsonify("Livro já está cadastrado"), 200
        biblioteca.append(novo_livro)
        dados.salvar_no_arquivo(biblioteca)
        return jsonify("message: livro cadastrado com sucesso"), 201
    elif request.method == 'DELETE':
        for l in biblioteca:
            if l['isbn'] == isbn:
                biblioteca.remove(l)
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("mensagem: livro deletado com sucesso"), 200
        return jsonify("message: livro não localizado"), 404
    elif request.method == 'PUT':
        alteracoes = request.get_json()
        for livro in biblioteca:
            if livro['isbn'] == isbn:
                for key, value in alteracoes.items():
                    livro[key] = value
                dados.salvar_no_arquivo(biblioteca)
                return jsonify("mensagem: livro alterado com sucesso"), 200
        return jsonify("message: livro não localizado"), 404
    else:
        return 'Solicitação não aceita', 503

# Rotas da Interface Web para a Biblioteca
@app.route('/biblioteca', methods=['GET', 'POST'])
def interface_web():
    """ Função para gerenciamento via interface web
    """
    biblioteca = dados.carregar_do_arquivo()
    if request.method == 'POST':
        isbn = request.args.get('isbn')
        if deletar_livro(isbn) == True:
            return redirect(url_for('interface_web'))
        else:
            return "Livro não existe", 404
    else:
        return render_template('biblioteca.html',biblioteca=biblioteca)

if __name__ == '__main__':
    app.run(debug=True)