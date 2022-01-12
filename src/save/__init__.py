import pickle

def reset() :
    table = {"games": 0, "best_score": 0}
    with open("./src/save/data.py", "w") as Table :
        Table.write(f"table = {str(table)}")

def get() :
    table = pickle.load(open("./src/save/data.p", "rb"))
    with open("./src/save/data.py", "w") as Table :
        Table.write(table.decode())
    return eval(table.decode()[8:])

def write(games, best_score) :
    with open("./src/save/data.py", "w") as Table :
        Table.write(f'table = {str({"games": games, "best_score": best_score})}')

def compiler() :
    with open("./src/save/data.py", 'rb') as data:
        to_compile = data.read()
    pickle.dump(to_compile, open( "./src/save/data.p", "wb" ))

def add_game() :
    table = get()
    write(table["games"]+1, table["best_score"])
    compiler()

def set_score(score) :
    table = get()
    write(table["games"], score)
    compiler()

def main() :
    reset()
    compiler()

if __name__ == '__main__' :
    main()