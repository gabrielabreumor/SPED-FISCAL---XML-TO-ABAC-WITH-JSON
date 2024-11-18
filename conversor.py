def converter_xml_para_json_com_metadados(xml_path, json_path):
    with open(xml_path, 'r', encoding='utf-8') as xml_file:
        xml_data = xml_file.read()

    xml_dict = xmltodict.parse(xml_data)

    xml_dict['eFinanceira']['loteEventos']['metadados'] = {
        "acesso_restrito": True,
        "nivel_acesso": "gerente",
        "tipo_operacao": "interna"
    }

    json_data = json.dumps(xml_dict, indent=4)

    with open(json_path, 'w', encoding='utf-8') as json_file:
        json_file.write(json_data)