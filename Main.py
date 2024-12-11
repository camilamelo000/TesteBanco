import sqlite3
import ExportadorParaJS 
import ConteudoTabelas 

class Main:
    exportador = ExportadorParaJS(db)
    exportador.exportar()
