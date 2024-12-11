import json
import sqlite3

class ExportadorParaJSON:

    def __init__(self, db):
        self.db = db

    def exportar(self):
        self.db.cursor.execute("SELECT * FROM Livro")
        livros = self.db.cursor.fetchall()
        
        self.db.cursor.execute("SELECT * FROM Comentario")
        comentarios = self.db.cursor.fetchall()

        self.db.cursor.execute("SELECT * FROM Usuario")
        usuarios = self.db.cursor.fetchall()

        self.db.cursor.execute("SELECT * FROM Carrinho")
        carrinho = self.db.cursor.fetchall()

        dados = {
            "livros": [
                {
                    "id": livro[0],
                    "titulo": livro[1],
                    "autor": livro[2],
                    "categoria": livro[3],
                    "descricao": livro[4],
                    "preco": livro[5],
                    "status_livro": livro[6]
                } for livro in livros
            ],
            "comentarios": [
                {
                    "id_usuario": comentario[0],
                    "id_livro": comentario[1],
                    "estrelas": comentario[2],
                    "comentarios": comentario[3]
                } for comentario in comentarios
            ],
            "usuarios": [
                {
                    "id": usuario[0],
                    "nome_usuario": usuario[1],
                    "email": usuario[2],
                    "senha": usuario[3]
                } for usuario in usuarios
            ],
            "carrinho": [
                {
                    "id_pedido": item[0],
                    "id_livro": item[1],
                    "quantidade": item[2],
                    "preco": item[3],
                    "preco_total": item[4]
                } for item in carrinho
            ]
        }

        with open("dados.json", "w", encoding="utf-8") as f:
            json.dump(dados, f, ensure_ascii=False, indent=4)

        print("Exportação concluída com sucesso para o arquivo dados.json.")
