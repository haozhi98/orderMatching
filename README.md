#simpleOrderMatching
A simple Matching Engine which maintains an OrderBook. The Matching Engine supports the follow types of orders:

1) Market Order - will match submitted order regardless of price, remaning quantity is cancelled
2) Limit Order - will execute submitted orders if there are matches, remaning quantity is added to the OB
3) Immediate-or-Cancel Order - similar to Limit Order, but remanining quantity is cancelled
4) Fill-or-Kill Order - similar to Limit Order, but will only execute if order is executed fully, else cancel entire order

##Functionalities
1) Submit orders
2) Match and execute orders, executed value as output
3) Store orders in OB if necessary
4) Cancel orders
5) Update orders
