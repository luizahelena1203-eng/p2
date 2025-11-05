def consultar_andamentos(numero, tribunal):
    # Aqui futuramente você pode conectar a uma API real de tribunal
    # Por enquanto, simulamos os andamentos:
    return [
        {"data": "2025-11-05", "descricao": "Processo recebido no tribunal"},
        {"data": "2025-11-06", "descricao": "Concluso ao juiz para decisão"},
        {"data": "2025-11-10", "descricao": "Despacho publicado"}
    ]
