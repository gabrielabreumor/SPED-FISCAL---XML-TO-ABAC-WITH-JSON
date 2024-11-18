import json

def carregar_dados_json():
    with open('saida.json', 'r', encoding='utf-8') as f:
        return json.load(f)

def verificar_acesso(usuario_atributos, dados_atributos):
    for atributo, valor in dados_atributos.items():
        if usuario_atributos.get(atributo) != valor:
            return False
    return True

usuario_atributos = {
    'cargo': 'gerente',
    'localizacao': 'BR',
    'perm_leitura': True
}

def executar_teste_abac():
    dados_json = carregar_dados_json()

    dados_atributos = {
        'localizacao': dados_json['eFinanceira']['loteEventos']['evento']['eFinanceira']['evtMovOpFin']['ideDeclarado']['paisResid']['Pais'],
        'tipo_operacao': 'interna' 
    }

    if verificar_acesso(usuario_atributos, dados_atributos):
        print("Acesso permitido.")
    else:
        print("Acesso negado.")

if __name__ == "__main__":
    executar_teste_abac()
