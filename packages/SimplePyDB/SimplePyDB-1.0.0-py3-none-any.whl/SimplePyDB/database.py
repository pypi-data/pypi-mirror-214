import pickle

database = {}

def createBank(name):
    database[name] = {}

def createNotebook(bank, notebook, value):
    if bank not in database:
        raise ValueError("Bank '{}' does not exist.".format(bank))
    database[bank][notebook] = {'__value__': value}

def createKey(bank, notebook, key, value):
    if bank not in database:
        raise ValueError("Bank '{}' does not exist.".format(bank))
    if notebook not in database[bank]:
        raise ValueError("Notebook '{}' does not exist in bank '{}'.".format(notebook, bank))
    database[bank][notebook][key] = value

def createSubKey(bank, notebook, key, subkey, value):
    if bank not in database:
        raise ValueError("Bank '{}' does not exist.".format(bank))
    if notebook not in database[bank]:
        raise ValueError("Notebook '{}' does not exist in bank '{}'.".format(notebook, bank))
    if key not in database[bank][notebook]:
        raise ValueError("Key '{}' does not exist in notebook '{}' of bank '{}'.".format(key, notebook, bank))
    database[bank][notebook][key][subkey] = value

def readKey(bank, notebook):
    if bank not in database:
        raise ValueError("Bank '{}' does not exist.".format(bank))
    if notebook not in database[bank]:
        raise ValueError("Notebook '{}' does not exist in bank '{}'.".format(notebook, bank))
    return database[bank][notebook]['__value__']

def readSubKey(bank, notebook, key):
    if bank not in database:
        raise ValueError("Bank '{}' does not exist.".format(bank))
    if notebook not in database[bank]:
        raise ValueError("Notebook '{}' does not exist in bank '{}'.".format(notebook, bank))
    if key not in database[bank][notebook]:
        raise ValueError("Key '{}' does not exist in notebook '{}' of bank '{}'.".format(key, notebook, bank))
    return database[bank][notebook][key]
