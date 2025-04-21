from datetime import date

def calcular_idade_animal(data_nascimento):
    hoje = date.today()
    if data_nascimento > hoje:
        raise ValueError("Data de nascimento não pode ser no futuro.")
    return hoje.year - data_nascimento.year - (
        (hoje.month, hoje.day) < (data_nascimento.month, data_nascimento.day)
    )