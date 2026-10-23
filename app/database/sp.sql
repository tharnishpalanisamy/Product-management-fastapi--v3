CREATE PROCEDURE restock_product(
    p_product_id INTEGER,
    p_quantity INTEGER
)
LANGUAGE plpgsql
AS $$
BEGIN
    IF p_quantity <= 0 THEN
        RAISE EXCEPTION 'Quantity must be greater than zero';
    END IF;

    UPDATE products
    SET quantity = quantity + p_quantity
    WHERE id = p_product_id;

    IF NOT FOUND THEN
        RAISE EXCEPTION 'Product not found';
    END IF;
END;
$$;





CREATE PROCEDURE display_summary(
p_product_id INTEGER 
)
LANGUAGE plpgsql 
AS $$
DECLARE 
v_cost_price NUMERIC ; 
v_quantity INTEGER ; 
v_margin NUMERIC ; 
v_total_cost NUMERIC ;

v_selling_price NUMERIC ; 
v_estimate_sale_value NUMERIC ; 
v_profit_per_item  NUMERIC ; 
v_expected_profit NUMERIC ; 
BEGIN 
	IF NOT EXISTS (SELECT 1 FROM products WHERE id = p_product_id) THEN
        RAISE EXCEPTION 'Product with ID % does not exist', p_product_id;
    END IF 


	SELECT p.cost_price , p.quantity , c.margin FROM products p 
	JOIN categories c on p.category_id = c.id 
	INTO v_cost_price , v_quantity , v_margin  

	SET v_selling_price := cost_price +  v_cost_price * (v_margin / 100) ; 
	SET v_total_cost := v_cost_price * v_quantity ; 
	SET v_profit_per_item := v_cost_price * (v_margin / 100) ; 
	SET v_expected_profit := v_profit_per_item * v_quantity ;  

	
	



//correct function 
CREATE FUNCTION display_summary
(
    p_product_id integer
)
 RETURNS TABLE(
    product_id integer,
    product_name text,
    cost_price numeric,
    quantity integer, 
    margin numeric, 
    stock_value numeric, 
    selling_price numeric, 
    profit_per_item numeric, 
    sales_value numeric, 
    expected_profit numeric)
 LANGUAGE plpgsql
AS $$
BEGIN

RETURN QUERY 
SELECT 
	p.id ,
	p.product_name::TEXT , 
	p.cost_price::NUMERIC , 
	p.quantity , 
	c.margin::NUMERIC , 
	p.cost_price * p.quantity,
	p.cost_price +   p.cost_price * (c.margin /  100.0),
	p.cost_price * (c.margin / 100.0), 
	(p.cost_price  + p.cost_price *   (c.margin /  100.0)) *  p.quantity,
	(p.cost_price * (c.margin / 100.0) )  * p.quantity 

	FROM products p JOIN categories c 
	ON p.category_id = c.id 
	WHERE p.id = p_product_id;

	IF NOT FOUND THEN 
		RAISE EXCEPTION 
			'PRoduct not found with id %' ,
			p_product_id; 
	END IF ; 
END ; 
$$
