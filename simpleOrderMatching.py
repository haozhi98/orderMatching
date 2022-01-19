def main():
    orderBook = {"B": [], "S": []}
    while True:
        print(orderBook, "main")
        order = input("Enter your order ").split()
        if order[0] == "END":
            break
        if order[0] == "SUB":
            print(submitOrder(orderBook, order[1:]))
        elif order[0] == "CXL":
            print(cancelOrder(orderBook, order[1]))
        elif order[0] == "CRP":
            print(updateOrder(orderBook, order[1:]))
        else:
            print("Please enter SUB or CXL")
    print("Thank you for using the program, goodbye!")
    
def submitOrder(orderBook, order):
    isIOC = False
    isFOK = False
    if order[0] == "LO" or order[0] == "FOK" or order[0] == "IOC":
        if order[0] == "IOC":
            isIOC = True
        elif order[0] == "FOK":
            isFOK = True
        isMarket = False
    elif order[0] == "MO":
        isMarket = True
    else:
        print("Order type is not recognised")
        return -1

    side = order[1]
    print(side, "side")
    if side != "B" and side != "S":
        print("Order side is not recognised")
        return -1
    if side == "B":
        isBuy = True
    else:
        isBuy = False
    print(order, 'order')
    try:
        if not isMarket:
            price = float(order[4]) 
        qty = float(order[3])
    except ValueError:
        print("Order price and quantity must be in a float or numeric form")
        return -1

    if (isBuy and orderBook["S"] == []) or (not isBuy and orderBook["B"] == []):
        insertOrder(orderBook, side, price, qty, order[2])
        # orderBook[side].append(writeOrder(price, qty, order[2]))
        return 0    #added order to OB
    
    matchSide = "S" if isBuy else "B"
    totalCost = 0
    toRemove = []
    print(orderBook[matchSide])
    for matchId, match in enumerate(orderBook[matchSide]):
        print(match, 'match')
        matchDetails = readOrder(match)
        matchPrice, matchQty = float(matchDetails[1]), float(matchDetails[0])
        if isMarket or (not isBuy and matchPrice >= price) or (isBuy and matchPrice <= price):
            if matchQty > qty:  #match side has excess qty
                matchQty -= qty
                match = writeOrder(matchPrice, matchQty, matchDetails[2])
                print(match, 'match update')
                orderBook[matchSide][matchId] = match
                totalCost += qty * matchPrice
                for item in toRemove:
                    orderBook[matchSide].remove(item)
                return totalCost
            else:               #submit side has excess qty
                qty -= matchQty
                print(match, 'match remove')
                toRemove.append(match)
                totalCost += matchQty * matchPrice
    if not isMarket and not isIOC and not isFOK:
        insertOrder(orderBook, side, price, qty, order[2])
    if isFOK:
        totalCost = 0
    else:
        for item in toRemove:
            orderBook[matchSide].remove(item)
    
    return totalCost

def insertOrder(orderBook, side, price, qty, id):
    isBuy = True if side == "B" else False
    if orderBook[side] == []:
        orderBook[side].append(writeOrder(price, qty, id))
        return
    else:
        for index, order in enumerate(orderBook[side]):
            if (price > float(readOrder(order)[1]) and  isBuy) or (price < float(readOrder(order)[1]) and not isBuy):
                orderBook[side].insert(index, writeOrder(price, qty, id))
                return
    orderBook[side].append(writeOrder(price, qty, id))
    return

def readOrder(orderCode):
    orderCode = orderCode.split("@")
    for i in orderCode.pop().split("#"):
        orderCode.append(i)
    return orderCode

def writeOrder(price, qty, id):
    orderCode = str(qty) + "@" + str(price) + "#" + str(id)
    return orderCode

def cancelOrder(orderBook, id):
    for orderType in orderBook:
        for order in orderBook[orderType]:
            if id == readOrder(order)[2]:
                orderBook[orderType].remove(order)
                return orderBook

def updateOrder(orderBook, order):
    if len(order) != 3:
        print("Wrong input")
        return -1
    id = order[0]
    try:
        qty = float(order[1])
        price = float(order[2])
    except ValueError:
        print("Please enter an integer or float for the quantity and price")
        return -1
    for side in orderBook:
        for index, currOrder in enumerate(orderBook[side]):
            currOrderSplit = readOrder(currOrder)
            if id == currOrderSplit[2]:
                if qty <= float(currOrderSplit[0]) and price == float(currOrderSplit[1]):
                    orderBook[side][index] = writeOrder(price, qty, id)
                    return orderBook
                else:
                    orderBook[side].remove(currOrder)
                    return insertOrder(orderBook, side, price, qty, id)

main()
        
# SUB LO B N1Eh 300 12    
# SUB LO B 0Gxb 250 11   
# SUB LO S JSvU 350 14    
# SUB LO S uH6w 320 15     
# SUB IOC S ckMR 150 10   
# SUB IOC B DVeP 500 14   
# SUB FOK S ejnR 200 12   
# SUB FOK S 8uGs 200 9
# SUB LO B 2VA9 250 12    
# SUB LO B 9zS1 300 11    
# CRP 2VA9 480 11   
# CRP 9zS1 170 11