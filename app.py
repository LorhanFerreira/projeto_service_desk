from flask import Flask, request, jsonify
from db.db_connection import get_connection

app = Flask(__name__)

# --- ROTAS DE USUÁRIOS ---
@app.route('/usuarios', methods=['GET', 'POST'])
def gerenciar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        dados = request.json
        cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (dados['nome'], dados['email']))
        conn.commit()
        return jsonify({"mensagem": "Usuário criado!"}), 201
    cursor.execute("SELECT * FROM usuarios")
    return jsonify(cursor.fetchall()), 200

@app.route('/usuarios/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def usuario_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM usuarios WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"mensagem": "Usuário removido!"}), 200
    if request.method == 'PUT':
        dados = request.json
        cursor.execute("UPDATE usuarios SET nome = %s, email = %s WHERE id = %s", (dados['nome'], dados['email'], id))
        conn.commit()
        return jsonify({"mensagem": "Usuário atualizado!"}), 200
    cursor.execute("SELECT * FROM usuarios WHERE id = %s", (id,))
    return jsonify(cursor.fetchone()), 200

# --- ROTAS DE TÉCNICOS ---
@app.route('/tecnicos', methods=['GET', 'POST'])
def gerenciar_tecnicos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        dados = request.json
        cursor.execute("INSERT INTO tecnicos (nome, especialidade) VALUES (%s, %s)", (dados['nome'], dados['especialidade']))
        conn.commit()
        return jsonify({"mensagem": "Técnico cadastrado!"}), 201
    cursor.execute("SELECT * FROM tecnicos")
    return jsonify(cursor.fetchall()), 200

# --- GERENCIAMENTO DE CHAMADOS ---
@app.route('/chamados', methods=['GET', 'POST'])
def gerenciar_chamados():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'POST':
        dados = request.json
        # Chamado nasce Pendente e técnico como NULL
        sql = "INSERT INTO chamados (titulo, descricao, prioridade, status, usuario_id) VALUES (%s, %s, %s, 'Pendente', %s)"
        cursor.execute(sql, (dados['titulo'], dados['descricao'], dados['prioridade'], dados['usuario_id']))
        conn.commit()
        return jsonify({"mensagem": "Chamado aberto!"}), 201
    cursor.execute("SELECT * FROM chamados")
    return jsonify(cursor.fetchall()), 200

@app.route('/chamados/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def chamado_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    if request.method == 'GET':
        cursor.execute("SELECT * FROM chamados WHERE id = %s", (id,))
        chamado = cursor.fetchone()
        return jsonify(chamado) if chamado else (jsonify({"erro": "Não encontrado"}), 404)
    
    if request.method == 'PUT':
        dados = request.json
        sql = "UPDATE chamados SET tecnico_id = %s, status = %s WHERE id = %s"
        cursor.execute(sql, (dados.get('tecnico_id'), dados.get('status'), id))
        conn.commit()
        return jsonify({"mensagem": "Chamado atualizado!"}), 200
    
    if request.method == 'DELETE':
        cursor.execute("DELETE FROM chamados WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"mensagem": "Chamado excluído!"}), 200

# --- FILTRO POR STATUS (PADRONIZADO) ---
@app.route('/chamados/status/<string:situacao>', methods=['GET'])
def filtrar_chamados(situacao):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    # Agora você filtra por 'Pendente', 'Em_Andamento' ou 'Resolvido'
    cursor.execute("SELECT * FROM chamados WHERE status = %s", (situacao,))
    return jsonify(cursor.fetchall()), 200

if __name__ == '__main__':
    app.run(debug=True)
