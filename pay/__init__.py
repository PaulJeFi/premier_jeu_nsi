import pickle

def reset() :
    table = {"pay": 0, "games": 0}
    with open("./pay/data.py", "w") as Table :
        Table.write(f"table = {str(table)}")

def get() :
    table = pickle.load(open("./pay/data.p", "rb"))
    with open("./pay/data.py", "w") as Table :
        Table.write(table.decode())
    
    import pay.data
    return pay.data.table

def write(pay, games) :
    with open("./pay/data.py", "w") as Table :
        Table.write(f'table = {str({"pay": pay, "games": games})}')

def compiler() :
    with open("./pay/data.py", 'rb') as data:
        to_compile = data.read()
    pickle.dump(to_compile, open( "./pay/data.p", "wb" ))

def pay() :
    write(150, 0)
    compiler()

def add() :
    write(get()["pay"], get()["games"]+1)
    compiler()

if __name__ == '__main__' :
    reset()
    compiler()