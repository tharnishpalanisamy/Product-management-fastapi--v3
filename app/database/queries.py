GET_QUERY = '''
    SELECT 
        product_id , 
        product_name , 
        category , 
        cost_price , 
        quantity, 
        stock_value , 
        margin ,
        selling_price , 
        sale_value , 
        profit_per_item ,
        expected_profit 
    FROM products 
''' 


POST_QUERY = '''
    INSERT INTO products(
        product_name , 
        category , 
        cost_price  , 
        quantity, 
        stock_value , 
        margin ,
        selling_price , 
        sale_value , 
        profit_per_item ,
        expected_profit 
    ) 
    VALUES(
        %s , 
        %s , 
        %s , 
        %s , 
        %s , 
        %s , 
        %s , 
        %s , 
        %s , 
        %s 
    )
    RETURNING product_id 
'''



UPDATE_QUERY = '''
    UPDATE products 
    SET 
        product_name = %s , 
        category = %s , 
        cost_price = %s ,
        quantity = %s ,
        stock_value = %s ,
        margin = %s ,
        selling_price = %s ,
        sale_value = %s ,
        profit_per_item = %s ,
        expected_profit = %s
    WHERE product_id = %s 
    RETURNING product_id 
'''
