CREATE TABLE products(
product_id int generated always as identity primary key , 
product_name varchar(30) , 
category varchar(30) ,
cost_price numeric(10,2) , 
quantity int
)
