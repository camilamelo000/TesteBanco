import sqlite3

class GerenciadorBD:

  def __init__(self, nome_banco):
    self.conexao = sqlite3.connect(nome_banco)
    self.cursor = self.conexao.cursor()
    self.criar_tabelas()

  def criar_tabelas(self):
    self.cursor.execute('''
           CREATE TABLE IF NOT EXISTS Usuario(
            IdUsuario INTEGER PRIMARY KEY AUTOINCREMENT,
            NomeUsuario TEXT NOT NULL,
            Email TEXT NOT NULL,
            Senha TEXT NOT NULL
           );
      ''')
    self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS Livro(
            IdLivro INTEGER PRIMARY KEY AUTOINCREMENT,
            Titulo TEXT NOT NULL,
            Autor TEXT NOT NULL,
            Categoria TEXT NOT NULL,
            Descricao TEXT NOT NULL,
            Preco DECIMAL(7,2),
            StatusLivro TEXT
          )
      ''')
    self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS Comentario(
            IdComentario INTEGER PRIMARY KEY AUTOINCREMENT,
            IdUsuario INTEGER,
            IdLivro INTEGER,
            Estrelas INTEGER,
            Comentarios TEXT NOT NULL,
            FOREIGN KEY(IdUsuario) REFERENCES Usuario(IdUsuario),
            FOREIGN KEY(IdLivro) REFERENCES Livro(IdLivro)
          )
      ''')
    self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS Pedido(
            IdPedido INTEGER PRIMARY KEY AUTOINCREMENT,
            IdUsuario INTEGER,
            ValorPedido DECIMAL(7,2),
            StatusPedido TEXT,
            FOREIGN KEY(IdUsuario) REFERENCES Usuario(IdUsuario)
          )
      ''')
    self.cursor.execute('''
          CREATE TABLE IF NOT EXISTS Carrinho(
            IdCarrinho INTEGER PRIMARY KEY AUTOINCREMENT,
            IdPedido INTEGER,
            IdLivro INTEGER,
            Quantidade INTEGER,
            Preco DECIMAL(7,2), 
            PrecoTotal DECIMAL(7,2),
            FOREIGN KEY(IdPedido) REFERENCES Pedido(IdPedido),
            FOREIGN KEY(IdLivro) REFERENCES Livro(IdLivro)
          )
      ''')
    
    self.cursor.execute("DROP TRIGGER IF EXISTS AtualizaPrecoTotalInsert")
    self.cursor.execute("DROP TRIGGER IF EXISTS AtualizaPrecoTotalUpdate")

    self.cursor.execute('''
        CREATE TRIGGER AtualizaPrecoTotalInsert
        AFTER INSERT ON Carrinho
        FOR EACH ROW
        BEGIN
            UPDATE Carrinho
            SET PrecoTotal = NEW.Quantidade * NEW.Preco
            WHERE IdCarrinho = NEW.IdCarrinho;
        END;
        ''')
    self.cursor.execute('''
        CREATE TRIGGER AtualizaPrecoTotalUpdate
        AFTER UPDATE OF Quantidade, Preco 
        ON Carrinho FOR EACH ROW
        BEGIN
          UPDATE Carrinho
          SET PrecoTotal = Quantidade * Preco
          WHERE IdCarrinho = NEW.IdCarrinho;
        END;
        ''')
    self.conexao.commit()

    def fechar_conexao(self):
      self.conexao.close()
