from tkinter import *
from tkinter import ttk
import mysql.connector
 
root = Tk()
 
class Funcs():
    def limpa_receita(self):
        self.codigo_entry.delete(0, END)
        self.nome_entry.delete(0, END)
        self.calorias_entry.delete(0, END)
        self.gordura_total_entry.delete(0, END)
        self.acucar_entry.delete(0, END)
        self.sodio_entry.delete(0, END)
        self.proteina_entry.delete(0, END)
        self.gordura_saturada_entry.delete(0, END)
        self.carboidratos_entry.delete(0, END)
        self.descricao_entry.delete(0, END)
        self.qtd_ingredientes_entry.delete(0, END)
        self.tags_text.delete(1.0, END)
        self.ingredientes_text.delete(1.0, END)
        self.steps_text.delete(1.0, END)
 
    def conecta_bd(self):
        self.conn = mysql.connector.connect(host='localhost', database='bd_bestfood', user='root', password='')
        self.cursor = self.conn.cursor()
        self.cursor.execute("select database();")
        self.linha = self.cursor.fetchone()
    
    def desconecta_bd(self):
        self.conn.close()
 
    def montaTabelas(self):
        self.conecta_bd()
        try:
            self.criar_tabelas_SQL = """   
                                        CREATE TABLE tb_recipes(
                                            id_recipes INT NOT NULL,
                                            name VARCHAR(100) NOT NULL,
                                            description VARCHAR(255) NOT NULL,
                                            n_ingredients VARCHAR(3) NOT NULL,
                                            PRIMARY KEY(id_recipes));
                                            
                                        CREATE TABLE tb_ingredients(
                                            id_recipes INT NOT NULL,
                                            id_ingredients INT NOT NULL AUTO_INCREMENT,
                                            ingredients VARCHAR(100) NOT NULL,
                                            PRIMARY KEY(id_ingredients));
                                        
                                        CREATE TABLE tb_nutrition(
                                            id_recipes INT NOT NULL,
                                            calories VARCHAR(10) NOT NULL,
                                            total_fat VARCHAR(10) NOT NULL,
                                            sugar VARCHAR(10) NOT NULL,
                                            sodium VARCHAR(10) NOT NULL,
                                            protein VARCHAR(10) NOT NULL,
                                            saturated_fat VARCHAR(10) NOT NULL,
                                            carbohydrates VARCHAR(10) NOT NULL,
                                            PRIMARY KEY(id_recipes));    
        
                                        CREATE TABLE tb_steps(
                                            id_recipes INT NOT NULL,
                                            id_step INT NOT NULL AUTO_INCREMENT,
                                            step VARCHAR(255) NOT NULL,
                                            PRIMARY KEY(id_step));
 
                                        CREATE TABLE tb_tags(
                                            id_recipes INT NOT NULL,
                                            id_tag INT NOT NULL AUTO_INCREMENT,    
                                            tag VARCHAR(50) NOT NULL,
                                            PRIMARY KEY(id_tag));
 
                                        ALTER TABLE tb_nutrition ADD FOREIGN KEY(id_recipes) REFERENCES tb_recipes(id_recipes) ON DELETE CASCADE;
                                        ALTER TABLE tb_ingredients ADD FOREIGN KEY(id_recipes) REFERENCES tb_recipes(id_recipes) ON DELETE CASCADE;
                                        ALTER TABLE tb_steps ADD FOREIGN KEY(id_recipes) REFERENCES tb_recipes(id_recipes) ON DELETE CASCADE;
                                        ALTER TABLE tb_tags ADD FOREIGN KEY(id_recipes) REFERENCES tb_recipes(id_recipes) ON DELETE CASCADE;

                                        CREATE PROCEDURE ingredientes (id INT)
                                            SELECT GROUP_CONCAT(ingredients) AS ingredientes
                                            FROM tb_ingredients WHERE id_recipes = id;    

                                        COMMIT;  """
 
            self.cursor = self.conn.cursor()
            self.cursor.execute(self.criar_tabelas_SQL)
            print("Tabelas criadas com sucesso!")
        except mysql.connector.Error as erro:
            print("Falha ao criar tabela no MySQL: {}".format(erro))
        finally:
            self.desconecta_bd()
 
    def variaveis(self):
        self.idRecipes = self.codigo_entry.get()
        self.description = self.descricao_entry.get()
        self.name = self.nome_entry.get()
        self.QTDingredientes = self.qtd_ingredientes_entry.get()
        self.calories = self.calorias_entry.get()
        self.total_fat = self.gordura_total_entry.get()
        self.sugar = self.acucar_entry.get()
        self.sodium = self.sodio_entry.get()
        self.protein = self.proteina_entry.get()
        self.saturated_fat = self.gordura_saturada_entry.get()
        self.carbohydrates = self.carboidratos_entry.get()
        self.ingredients = self.ingredientes_text.get("1.0",END)
        self.tag = self.tags_text.get("1.0", END)
        self.step = self.steps_text.get("1.0", END) 
 
    def adiciona_receita(self):
        self.conecta_bd()
        self.variaveis()
 
        self.inserir_receitas = """ INSERT INTO tb_recipes(id_recipes, description, name, n_ingredients)
                                    VALUES (%s, %s, %s, %s) """, (self.idRecipes, self.description, self.name, self.QTDingredientes)
 
        self.inserir_valoresNutricionais = """INSERT INTO tb_nutrition(id_recipes, calories, total_fat, sugar, sodium, protein, saturated_fat, carbohydrates)
                                            VALUES (%s, %s, %s, %s, %s, %s, %s, %s) """, (self.idRecipes, self.calories, self.total_fat, self.sugar, self.sodium, self.protein, self.saturated_fat, self.carbohydrates)
 
        self.cursor = self.conn.cursor()
        self.cursor.execute(*self.inserir_receitas)
        self.cursor.execute(*self.inserir_valoresNutricionais)
        self.conn.commit()
        
        lista_ingredientes = self.ingredients.split(",")
        for x_ing in lista_ingredientes:
            self.inserir_ingredientes = """INSERT INTO tb_ingredients (id_recipes, ingredients) VALUES(%s, %s)""", (self.idRecipes, x_ing)
            self.cursor.execute(*self.inserir_ingredientes)
            self.conn.commit()
        
        lista_tags = self.tag.split(",")
        for x_tag in lista_tags:
            self.inserir_tag = """INSERT INTO tb_tags (id_recipes, tag) VALUES(%s, %s)""", (self.idRecipes, x_tag)
            self.cursor.execute(*self.inserir_tag)
            self.conn.commit()
        
        lista_steps = self.step.split(",")
        for x_step in lista_steps:
            self.inserir_step = """INSERT INTO tb_steps (id_recipes, step) VALUES(%s, %s)""", (self.idRecipes, x_step)
            self.cursor.execute(*self.inserir_step)
            self.conn.commit()
        
        print(self.cursor.rowcount, "Registros inseridos na tabela!")
        self.desconecta_bd()
        self.select_lista()
        self.limpa_receita()
    
    def deleta_receita(self):
        self.variaveis()
        self.conecta_bd()
        self.deletar_dados = """DELETE FROM tb_recipes WHERE id_recipes =""" + str(self.idRecipes)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.deletar_dados)
        self.conn.commit()
        self.desconecta_bd()
        self.limpa_receita()
        self.select_lista()
    
    def altera_receita(self):
        self.variaveis()
        self.conecta_bd()

        ### ATUALIZAR RECEITA E VALORES NUTRICIONAIS ###
        self.dados = """UPDATE tb_recipes NATURAL JOIN tb_nutrition SET description= %s, name= %s, n_ingredients= %s, calories= %s, total_fat= %s, sugar= %s, sodium= %s, protein= %s, saturated_fat= %s, carbohydrates= %s
                        WHERE id_recipes=%s """
        self.valor = (self.description, self.name, self.QTDingredientes, self.calories, self.total_fat, self.sugar, self.sodium, self.protein, self.saturated_fat, self.carbohydrates, self.idRecipes)
        self.cursor = self.conn.cursor()
        self.cursor.execute(self.dados, self.valor)
        self.conn.commit()
 
        ### ATUALIZAR INGREDIENTES ###
        lista=[]
        atualiza_ing = """SELECT id_ingredients FROM tb_ingredients WHERE id_recipes ="""+ str(self.idRecipes)
        self.cursor.execute(atualiza_ing)
        id_ing = self.cursor.fetchall()

        for w_ing in range(len(id_ing)):
            lista.append(id_ing[w_ing][0])
 
        lista_ingredientes = self.ingredients.split(",")
        if len(lista_ingredientes) < len(lista):
            lista_ingredientes.extend( [None] * (len(lista) - len(lista_ingredientes)))
            for (y_ing, x_ing) in zip(lista, lista_ingredientes):
                self.altera_ingredientes = """UPDATE tb_ingredients SET ingredients=%s WHERE id_ingredients=%s """, (x_ing, y_ing)
                self.cursor.execute(*self.altera_ingredientes)
                self.conn.commit()
                if not x_ing:
                    deleta_receita = """DELETE FROM tb_ingredients WHERE id_ingredients =""" + str(y_ing)
                    self.cursor.execute(deleta_receita)
                    self.conn.commit()
        elif len(lista_ingredientes) > len(lista):
            lista.extend( [None] * (len(lista_ingredientes) - len(lista)))
            for (y_ing, x_ing) in zip(lista_ingredientes, lista):
                self.altera_ingredientes = """UPDATE tb_ingredients SET ingredients=%s WHERE id_ingredients=%s """, (y_ing, x_ing)
                self.cursor.execute(*self.altera_ingredientes)
                self.conn.commit()
                if not x_ing:
                    inserir_receita = """INSERT INTO tb_ingredients (id_recipes, ingredients) VALUES(%s, %s)""", (self.idRecipes, y_ing)
                    self.cursor.execute(*inserir_receita)
                    self.conn.commit()
        else:
            for (y_ing, x_ing) in zip(lista, lista_ingredientes):
                self.altera_ingredientes = """UPDATE tb_ingredients SET ingredients=%s WHERE id_ingredients=%s """, (x_ing, y_ing)
                self.cursor.execute(*self.altera_ingredientes)
                self.conn.commit()

 
        ### ATUALIZAR TAGS ###
        lista=[]
        atualiza_tag = """SELECT id_tag FROM tb_tags WHERE id_recipes ="""+ str(self.idRecipes)
        self.cursor.execute(atualiza_tag)
        id_tag = self.cursor.fetchall()

        for x_tag in range(len(id_tag)):
            lista.append(id_tag[x_tag][0])

        lista_tag = self.tag.split(",")
        if len(lista_tag) < len(lista):
            lista_tag.extend( [None] * (len(lista) - len(lista_tag)))
            for (y_tag, x_tag) in zip(lista, lista_tag):
                self.altera_tag = """UPDATE tb_tags SET tag=%s WHERE id_tag=%s """, (x_tag, y_tag)
                self.cursor.execute(*self.altera_tag)
                self.conn.commit()
                if not x_tag:
                    deleta_tag = """DELETE FROM tb_tags WHERE id_tag =""" + str(y_tag)
                    self.cursor.execute(deleta_tag)
                    self.conn.commit()
        elif len(lista_tag) > len(lista):
            lista.extend( [None] * (len(lista_tag) - len(lista)))
            for (y_tag, x_tag) in zip(lista_tag, lista):
                self.altera_tag = """UPDATE tb_tags SET tag=%s WHERE id_tag=%s """, (y_tag, x_tag)
                self.cursor.execute(*self.altera_tag)
                self.conn.commit()
                if not x_tag:
                    inserir_tag = """INSERT INTO tb_tags (id_recipes, tag) VALUES(%s, %s)""", (self.idRecipes, y_tag)
                    self.cursor.execute(*inserir_tag)
                    self.conn.commit()
        else:
            for (y_tag, x_tag) in zip(lista_tag, lista):
                self.altera_tag = """UPDATE tb_tags SET tag=%s WHERE id_tag=%s """, (y_tag, x_tag)
                self.cursor.execute(*self.altera_tag)
                self.conn.commit()
 
        ### ATUALIZAR STEPS ###
        lista=[]
        atualiza_step = """SELECT id_step FROM tb_steps WHERE id_recipes ="""+ str(self.idRecipes)
        self.cursor.execute(atualiza_step)
        id_step = self.cursor.fetchall()

        for x_step in range(len(id_step)):
            lista.append(id_step[x_step][0])

        lista_step = self.step.split(",")
        if len(lista_step) < len(lista):
            lista_step.extend( [None] * (len(lista) - len(lista_step)))
            for (y_step, x_step) in zip(lista, lista_step):
                self.altera_step = """UPDATE tb_steps SET step=%s WHERE id_step=%s """, (x_step, y_step)
                self.cursor.execute(*self.altera_step)
                self.conn.commit()
                if not x_step:
                    deleta_step = """DELETE FROM tb_steps WHERE id_step =""" + str(y_step)
                    self.cursor.execute(deleta_step)
                    self.conn.commit()
        elif len(lista_step) > len(lista):
            lista.extend( [None] * (len(lista_step) - len(lista)))
            for (y_step, x_step) in zip(lista_step, lista):
                self.altera_step = """UPDATE tb_steps SET step=%s WHERE id_step=%s """, (y_step, x_step)
                self.cursor.execute(*self.altera_step)
                self.conn.commit()
                if not x_step:
                    inserir_step = """INSERT INTO tb_steps (id_recipes, step) VALUES(%s, %s)""", (self.idRecipes, y_step)
                    self.cursor.execute(*inserir_step)
                    self.conn.commit()
        else:
            for (y_step, x_step) in zip(lista_step, lista):
                self.altera_step = """UPDATE tb_steps SET step=%s WHERE id_step=%s """, (y_step, x_step)
                self.cursor.execute(*self.altera_step)
                self.conn.commit()
 
        self.desconecta_bd()
        self.select_lista()
        self.limpa_receita()
 
    def busca_receita(self):
        self.conecta_bd()
        self.listaRec.delete(*self.listaRec.get_children())
 
        self.nome_entry.insert(END, '%')
        nome = self.nome_entry.get()
        self.busca = """SELECT id_recipes, name, description, n_ingredients, calories, total_fat, sugar, sodium, protein, 
                                saturated_fat, carbohydrates, GROUP_CONCAT(DISTINCT ingredients), GROUP_CONCAT(DISTINCT tag), 
                                GROUP_CONCAT(DISTINCT step) FROM tb_recipes NATURAL JOIN tb_nutrition 
                                NATURAL JOIN tb_ingredients NATURAL JOIN tb_tags NATURAL JOIN tb_steps WHERE name LIKE '%s' GROUP BY id_recipes """ %nome
        self.cursor.execute(self.busca)
        buscanomeRec = self.cursor.fetchall()
        for i in buscanomeRec:
            self.listaRec.insert("", END, values=i)
        self.limpa_receita()
        self.desconecta_bd()

    def consulta_1(self):
        self.conecta_bd()
        self.listaRec.delete(*self.listaRec.get_children())

        self.qtd_ingredientes_entry.insert(END, '%')
        qtd_ingredientes = self.qtd_ingredientes_entry.get()
 
        self.busca = """SELECT id_recipes, name, description, n_ingredients, calories, total_fat, sugar, sodium, protein, 
                                saturated_fat, carbohydrates, GROUP_CONCAT(DISTINCT ingredients), GROUP_CONCAT(DISTINCT tag), 
                                GROUP_CONCAT(DISTINCT step) FROM tb_recipes NATURAL JOIN tb_nutrition 
                                NATURAL JOIN tb_ingredients NATURAL JOIN tb_tags NATURAL JOIN tb_steps WHERE n_ingredients LIKE '%s' GROUP BY id_recipes """ %qtd_ingredientes
        self.cursor.execute(self.busca)
        buscaQTDRec = self.cursor.fetchall()
        for i in buscaQTDRec:
            self.listaRec.insert("", END, values=i)
        self.limpa_receita()
        self.desconecta_bd()
    
    def consulta_2(self):
        self.conecta_bd()
        self.listaRec.delete(*self.listaRec.get_children())

        self.calorias_entry.insert(END, '%')
        calorias = self.calorias_entry.get()
 
        self.busca = """SELECT id_recipes, name, description, n_ingredients, calories, total_fat, sugar, sodium, protein, 
                                saturated_fat, carbohydrates, GROUP_CONCAT(DISTINCT ingredients), GROUP_CONCAT(DISTINCT tag), 
                                GROUP_CONCAT(DISTINCT step) FROM tb_recipes NATURAL JOIN tb_nutrition 
                                NATURAL JOIN tb_ingredients NATURAL JOIN tb_tags NATURAL JOIN tb_steps WHERE calories LIKE '%s' GROUP BY id_recipes """ %calorias
        self.cursor.execute(self.busca)
        buscaCaloriasRec = self.cursor.fetchall()
        for i in buscaCaloriasRec:
            self.listaRec.insert("", END, values=i)
        self.limpa_receita()
        self.desconecta_bd()

    def stored_procedure(self):
        self.conecta_bd()     

        chamada_SP = """ CALL ingredientes(1) """
        self.cursor = self.conn.cursor()
        self.cursor.execute(chamada_SP)
        ing = self.cursor.fetchall()
        print("Os ingredientes são: ", ing)

        self.desconecta_bd()
 
    def select_lista(self):
        self.variaveis()
        self.listaRec.delete(*self.listaRec.get_children())
        self.conecta_bd()
 
        self.consultaSQL = """SELECT id_recipes, name, description, n_ingredients, calories, total_fat, sugar, sodium, protein, 
                                saturated_fat, carbohydrates, GROUP_CONCAT(DISTINCT ingredients), GROUP_CONCAT(DISTINCT tag), 
                                GROUP_CONCAT(DISTINCT step) FROM tb_recipes NATURAL JOIN tb_nutrition 
                                NATURAL JOIN tb_ingredients NATURAL JOIN tb_tags NATURAL JOIN tb_steps GROUP BY id_recipes; """
 
        self.cursor.execute(self.consultaSQL)
        lista = self.cursor.fetchall()
        for i in lista or []:
            self.listaRec.insert("", END, values=i)
        self.desconecta_bd()
 
    def onDoubleClick(self, event):
        self.limpa_receita()
        self.listaRec.selection()
 
        for n in self.listaRec.selection():
            col1, col2, col3, col4, col5, col6, col7, col8, col9, col10, col11, col12, col13, col14 = self.listaRec.item(n, 'values')
            self.codigo_entry.insert(END, col1)
            self.nome_entry.insert(END, col2)
            self.descricao_entry.insert(END, col3)
            self.qtd_ingredientes_entry.insert(END, col4)
            self.calorias_entry.insert(END, col5)
            self.gordura_total_entry.insert(END, col6)
            self.acucar_entry.insert(END, col7)
            self.sodio_entry.insert(END, col8)
            self.proteina_entry.insert(END, col9)
            self.gordura_saturada_entry.insert(END, col10)
            self.carboidratos_entry.insert(END, col11)
            self.ingredientes_text.insert(END, col12)
            self.tags_text.insert(END, col13)
            self.steps_text.insert(END, col14)
 
class Application(Funcs):
    def __init__(self):
        self.root = root
        self.tela()
        self.frames_da_tela()
        self.widgets_frame1()
        self.lista_frame2()
        self.Menus()
        self.montaTabelas()
        self.select_lista()
        #self.stored_procedure()
        root.mainloop()
    def tela(self):
        self.root.title("BestFood")
        self.root.configure(background= '#1e3743')
        self.root.geometry("1400x780")
        self.root.resizable(True, True)
        self.root.maxsize(width= 1400, height= 780)
        self.root.minsize(width=500, height= 400)
    def frames_da_tela(self):
        self.frame_1 = Frame(self.root, bd = 4, bg= '#dfe3ee', highlightbackground= '#759fe6', highlightthickness=3 )
        self.frame_1.place(relx= 0.01, rely=0.02, relwidth= 0.98, relheight= 0.57)
 
        self.frame_2 = Frame(self.root, bd=4, bg='#dfe3ee', highlightbackground='#759fe6', highlightthickness=3)
        self.frame_2.place(relx=0.01, rely=0.6, relwidth=0.98, relheight=0.38)
    def widgets_frame1(self):
        ### CRIAÇÃO DOS BOTÕES
 
        ### Criação do botao limpar
        self.bt_limpar = Button(self.frame_1, text= "Limpar", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command= self.limpa_receita)
        self.bt_limpar.place(relx= 0.88, rely=0.08, relwidth=0.08, relheight= 0.1)
        ### Criação do botao cadastrar
        self.bt_novo = Button(self.frame_1, text="Cadastrar", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command= self.adiciona_receita)
        self.bt_novo.place(relx=0.66, rely=0.8, relwidth=0.08, relheight=0.1)
        ### Criação do botao buscar
        self.bt_buscar = Button(self.frame_1, text="Buscar", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command= self.busca_receita)
        self.bt_buscar.place(relx=0.74, rely=0.8, relwidth=0.08, relheight=0.1)
        ### Criação do botao alterar
        self.bt_alterar = Button(self.frame_1, text="Alterar", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command=self.altera_receita)
        self.bt_alterar.place(relx=0.82, rely=0.8, relwidth=0.08, relheight=0.1)
        ### Criação do botao apagar
        self.bt_apagar = Button(self.frame_1, text="Apagar", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command= self.deleta_receita)
        self.bt_apagar.place(relx=0.90, rely=0.8, relwidth=0.08, relheight=0.1)
 
        ### Criação do botao consulta 1
        self.bt_consulta_1 = Button(self.frame_1, text="Consulta 1", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command= self.consulta_1)
        self.bt_consulta_1.place(relx=0.40, rely=0.8, relwidth=0.08, relheight=0.1)
        ### Criação do botao consulta 2
        self.bt_consulta_2 = Button(self.frame_1, text="Consulta 2", bd=2, bg = '#107db2',fg = 'white', font = ('verdana', 8, 'bold'), command= self.consulta_2)
        self.bt_consulta_2.place(relx=0.48, rely=0.8, relwidth=0.08, relheight=0.1)
 
        ###CRIAÇÃO DAS LABELS E ENTRADAS
 
        ## Criação da label e entrada do codigo
        self.lb_codigo = Label(self.frame_1, text = "Código", bg= '#dfe3ee', fg = '#107db2')
        self.lb_codigo.place(relx= 0.01, rely= 0.05 )
 
        self.codigo_entry = Entry(self.frame_1 )
        self.codigo_entry.place(relx= 0.01, rely= 0.12, relwidth= 0.05)
 
        ## Criação da label e entrada Calorias
        self.lb_calorias = Label(self.frame_1, text = "Calorias", bg= '#dfe3ee', fg = '#107db2')
        self.lb_calorias.place(relx= 0.01, rely= 0.7)
 
        self.calorias_entry = Entry(self.frame_1 )
        self.calorias_entry.place(relx= 0.07, rely= 0.7, relwidth= 0.05)
 
        ## Criação da label e entrada Gordura Total
        self.lb_gordura_total = Label(self.frame_1, text = "Gordura Total", bg= '#dfe3ee', fg = '#107db2')
        self.lb_gordura_total.place(relx= 0.01, rely= 0.75 )
 
        self.gordura_total_entry = Entry(self.frame_1 )
        self.gordura_total_entry.place(relx= 0.07, rely= 0.75, relwidth= 0.05)
 
        ## Criação da label e entrada Açucar
        self.lb_acucar = Label(self.frame_1, text = "Açucar", bg= '#dfe3ee', fg = '#107db2')
        self.lb_acucar.place(relx= 0.01, rely= 0.8 )
 
        self.acucar_entry = Entry(self.frame_1 )
        self.acucar_entry.place(relx= 0.07, rely= 0.8, relwidth= 0.05)
 
        ## Criação da label e entrada Sódio
        self.lb_sodio = Label(self.frame_1, text = "Sódio", bg= '#dfe3ee', fg = '#107db2')
        self.lb_sodio.place(relx= 0.01, rely= 0.85 )
 
        self.sodio_entry = Entry(self.frame_1 )
        self.sodio_entry.place(relx= 0.07, rely= 0.85, relwidth= 0.05)
 
        ## Criação da label e entrada Proteína
        self.lb_proteina = Label(self.frame_1, text = "Proteína", bg= '#dfe3ee', fg = '#107db2')
        self.lb_proteina.place(relx= 0.01, rely= 0.9 )
 
        self.proteina_entry = Entry(self.frame_1 )
        self.proteina_entry.place(relx= 0.07, rely= 0.9, relwidth= 0.05)
 
        ## Criação da label e entrada Gordura saturada
        self.lb_gordura_saturada = Label(self.frame_1, text = "Gordura saturada", bg= '#dfe3ee', fg = '#107db2')
        self.lb_gordura_saturada.place(relx= 0.15, rely= 0.7 )
 
        self.gordura_saturada_entry = Entry(self.frame_1 )
        self.gordura_saturada_entry.place(relx= 0.23, rely= 0.7, relwidth= 0.05)
 
        ## Criação da label e entrada Carboidratos
        self.lb_carboidratos = Label(self.frame_1, text = "Carboidratos", bg= '#dfe3ee', fg = '#107db2')
        self.lb_carboidratos.place(relx= 0.15, rely= 0.75 )
 
        self.carboidratos_entry = Entry(self.frame_1 )
        self.carboidratos_entry.place(relx= 0.23, rely= 0.75, relwidth= 0.05)
 
        ## Criação da label e entrada do nome da receita
        self.lb_nome = Label(self.frame_1, text="Nome da Receita", bg= '#dfe3ee', fg = '#107db2')
        self.lb_nome.place(relx=0.1, rely=0.05)
 
        self.nome_entry = Entry(self.frame_1)
        self.nome_entry.place(relx=0.1, rely=0.12, relwidth=0.2)
 
        ## Criação da label e entrada das tags
        self.lb_tags = Label(self.frame_1, text="Tags", bg= '#dfe3ee', fg = '#107db2')
        self.lb_tags.place(relx=0.01, rely=0.22)
 
        self.tags_text = Text(self.frame_1)
        self.tags_text.place(relx=0.01, rely=0.30, relwidth=0.29, relheight=0.3)
 
        ## Criação da label e entrada dos ingredientes
        self.lb_ingredientes = Label(self.frame_1, text="Ingredientes", bg= '#dfe3ee', fg = '#107db2')
        self.lb_ingredientes.place(relx=0.35, rely=0.22)
 
        self.ingredientes_text = Text(self.frame_1)
        self.ingredientes_text.place(relx=0.35, rely=0.30, relwidth=0.30, relheight=0.3)
 
        ## Criação da label e entrada da QTD_ingredientes
        self.lb_qtd_ingredientes = Label(self.frame_1, text="Quantidade de Ingredientes", bg= '#dfe3ee', fg = '#107db2')
        self.lb_qtd_ingredientes.place(relx=0.70, rely=0.05)
 
        self.qtd_ingredientes_entry = Entry(self.frame_1)
        self.qtd_ingredientes_entry.place(relx=0.70, rely=0.12, relwidth=0.10)
 
        ## Criação da label e entrada do passo a passo
        self.lb_steps = Label(self.frame_1, text="Passo a passo", bg= '#dfe3ee', fg = '#107db2')
        self.lb_steps.place(relx=0.70, rely=0.22)
 
        self.steps_text = Text(self.frame_1)
        self.steps_text.place(relx=0.70, rely=0.30, relwidth=0.28, relheight=0.3)
 
        ## Criação da label e entrada da descrição
        self.lb_descricao = Label(self.frame_1, text="Descrição", bg= '#dfe3ee', fg = '#107db2')
        self.lb_descricao.place(relx=0.35, rely=0.05)
 
        self.descricao_entry = Entry(self.frame_1)
        self.descricao_entry.place(relx=0.35, rely=0.12, relwidth=0.3)
    
    def lista_frame2(self):
        self.listaRec = ttk.Treeview(self.frame_2, height=3, column=("col1", "col2", "col3", "col4", "col5", "col6", "col7", "col8","col9", "col10", "col11", "col12", "col13", "col14"))
        self.listaRec.heading("#0", text="")
        self.listaRec.heading("#1", text="Codigo")
        self.listaRec.heading("#2", text="Nome da Receita")
        self.listaRec.heading("#3", text="Descrição")
        self.listaRec.heading("#4", text="QTD_Ingredientes")
        self.listaRec.heading("#5", text="Calorias")
        self.listaRec.heading("#6", text="Gordura total")
        self.listaRec.heading("#7", text="Açucar")
        self.listaRec.heading("#8", text="Sódio")
        self.listaRec.heading("#9", text="Proteína")
        self.listaRec.heading("#10", text="Gordura saturada")
        self.listaRec.heading("#11", text="Carboidratos")
        self.listaRec.heading("#12", text="Ingredientes")
        self.listaRec.heading("#13", text="Tags")
        self.listaRec.heading("#14", text="Steps")
 
        self.listaRec.column("#0", width=1)
        self.listaRec.column("#1", width=30)
        self.listaRec.column("#2", width=100)
        self.listaRec.column("#3", width=100)
        self.listaRec.column("#4", width=50)
        self.listaRec.column("#5", width=50)
        self.listaRec.column("#6", width=50)
        self.listaRec.column("#7", width=50)
        self.listaRec.column("#8", width=50)
        self.listaRec.column("#9", width=50)
        self.listaRec.column("#10", width=50)
        self.listaRec.column("#11", width=50)
        self.listaRec.column("#12", width=100)
        self.listaRec.column("#13", width=100)
        self.listaRec.column("#14", width=100)
        self.listaRec.place(relx=0.01, rely=0.1, relwidth=0.98, relheight=0.85)
 
        self.scroolLista = Scrollbar(self.frame_2, orient='vertical')
        self.listaRec.configure(yscroll=self.scroolLista.set)
        self.scroolLista.place(relx=0.98, rely=0.1, relwidth=0.02, relheight=0.85)
 
        self.scroolLista2 = Scrollbar(self.frame_2, orient='horizontal')
        self.listaRec.configure(yscroll=self.scroolLista2.set)
        self.scroolLista2.place(relx=0.01, rely=0.85, relwidth=0.97, relheight=0.1)
 
        self.listaRec.bind("<Double-1>", self.onDoubleClick)
    
    def Menus(self):
        menubar = Menu(self.root)
        self.root.config(menu = menubar)
        filemenu = Menu(menubar)
 
        def Quit(): self.root.destroy()
 
        menubar.add_cascade(label= "Opções", menu = filemenu)
 
        filemenu.add_command(label = "Sair", command = Quit)
 
 
Application()
