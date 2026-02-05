from flask import Flask, request, jsonify
from db.db_connection import get_connection

app = Flask(__name__)

# --- ROTAS DE USUÁRIOS ---
@app.route('/usuarios', methods=['GET', 'POST'])
def gerenciar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            dados = request.json
            cursor.execute("INSERT INTO usuarios (nome, email) VALUES (%s, %s)", (dados['nome'], dados['email']))
            conn.commit()
            return jsonify({"mensagem": "Usuário criado!"}), 201
        
        cursor.execute("SELECT * FROM usuarios")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

# --- ROTAS DE TÉCNICOS ---
@app.route('/tecnicos', methods=['GET', 'POST'])
def gerenciar_tecnicos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            dados = request.json
            cursor.execute("INSERT INTO tecnicos (nome, especialidade) VALUES (%s, %s)", (dados['nome'], dados['especialidade']))
            conn.commit()
            return jsonify({"mensagem": "Técnico cadastrado!"}), 201
        
        cursor.execute("SELECT * FROM tecnicos")
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

# --- GERENCIAMENTO GERAL DE CHAMADOS ---
@app.route('/chamados', methods=['GET', 'POST'])
def gerenciar_chamados():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        if request.method == 'POST':
            dados = request.json
            # O status nasce como 'Pendente' por padrão
            sql = "INSERT INTO chamados (titulo, descricao, prioridade, status, usuario_id) VALUES (%s, %s, %s, 'Pendente', %s)"
            cursor.execute(sql, (dados['titulo'], dados['descricao'], dados['prioridade'], dados['usuario_id']))
            conn.commit()
            return jsonify({"mensagem": "Chamado aberto!"}), 201
        
        cursor.execute("SELECT * FROM chamados")
        return jsonify(cursor.fetchall()), 200
    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- BUSCAR, ATUALIZAR OU DELETAR CHAMADO ESPECÍFICO ---
@app.route('/chamados/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def chamado_por_id(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        # BUSCAR UM CHAMADO POR ID
        if request.method == 'GET':
            cursor.execute("SELECT * FROM chamados WHERE id = %s", (id,))
            chamado = cursor.fetchone()
            if chamado:
                return jsonify(chamado), 200
            return jsonify({"erro": "Chamado não encontrado"}), 404

        # ATUALIZAR (ATRIBUIR TÉCNICO E STATUS)
        if request.method == 'PUT':
            dados = request.json
            sql = "UPDATE chamados SET tecnico_id = %s, status = %s WHERE id = %s"
            cursor.execute(sql, (dados.get('tecnico_id'), dados.get('status'), id))
            conn.commit()
            return jsonify({"mensagem": "Chamado atualizado!"}), 200

        # DELETAR CHAMADO
        if request.method == 'DELETE':
            cursor.execute("DELETE FROM chamados WHERE id = %s", (id,))
            conn.commit()
            return jsonify({"mensagem": "Chamado excluído!"}), 200

    except Exception as e:
        return jsonify({"erro": str(e)}), 500
    finally:
        cursor.close()
        conn.close()

# --- FILTRO POR STATUS ---
@app.route('/chamados/status/<string:situacao>', methods=['GET'])
def filtrar_chamados(situacao):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    try:
        cursor.execute("SELECT * FROM chamados WHERE status = %s", (situacao,))
        return jsonify(cursor.fetchall()), 200
    finally:
        cursor.close()
        conn.close()

if __name__ == '__main__':
    app.run(debug=True)