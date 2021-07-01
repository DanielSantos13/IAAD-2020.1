-- Introdução ao Armazenamento e Análise de Dados (IAAD) - BSI/UFRPE
-- Script do Banco de Dados Best Food

-- Banco de dados Original
-- RECIPES("id_recipes", description, ingredients, n_ingredients, name, nutrition, steps, tags)

-- Banco de Dados BestFood Normalizado (os atributos que estão entre "", são as chaves primárias das tabelas)
-- RECIPES("id_recipes", description, n_ingredientes, name)
-- INGREDIENTS(id_recipes, "id_ingredients", ingredients)
-- NUTRITION("id_recipes", calorias, gordura total, açucar, sodio, proteina, gordura_saturada, carboidratos)
-- STEPS(id_recipes, "id_step", step)
-- TAGS(id_recipes, "id_tag", tag)

begin;
create schema bd_bestfood;
use bd_bestfood;

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

COMMIT;