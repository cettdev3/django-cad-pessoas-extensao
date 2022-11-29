content = [
    [
        4378,
        "DE",
        46,
        0,
        "6837",
        "VESPERTINO",
        2022,
        1,
        1,
        400,
        4,
        4,
        1600,
        1673740800000,
        1674604800000,
        "Segunda a Sexta",
        null,
        null,
        null,
        17,
        1,
        1,
        "teste",
        5,
        "LUIZ RASSI",
        "GOI\u00c2NIA",
        "PRESENCIAL",
        "CAPACITA\u00c7\u00c3O",
        "TRANSFORMA\u00c7\u00c3O DIGITAL",
        1666828800000,
        1669507200000,
        1666828800000,
        1669507200000,
        46,
        "27 de outubro de 2022",
        "27 de novembro de 2022",
        "27\/10\/2022",
        "27\/11\/2022",
        "27\/10\/2022"
    ],
    [
        4379,
        "DE",
        46,
        0,
        "6838",
        "VESPERTINO",
        2023,
        1,
        1,
        1000,
        4,
        0,
        4000,
        1672531200000,
        1675036800000,
        "Segunda a Sexta",
        null,
        null,
        null,
        17,
        1,
        1,
        "teste",
        5,
        "LUIZ RASSI",
        "GOI\u00c2NIA",
        "PRESENCIAL",
        "CAPACITA\u00c7\u00c3O",
        "DESENVOLVEDOR PYTHON: N\u00cdVEL B\u00c1SICO",
        1666828800000,
        1669507200000,
        1666828800000,
        1669507200000,
        46,
        "27 de outubro de 2022",
        "27 de novembro de 2022",
        "27\/10\/2022",
        "27\/11\/2022",
        "27\/10\/2022"
    ],
    [
        4382,
        "DE",
        46,
        0,
        "6837",
        "VESPERTINO",
        2023,
        1,
        1,
        400,
        10,
        0,
        4000,
        1673308800000,
        1674172800000,
        "Segunda a Sexta",
        null,
        null,
        null,
        17,
        1,
        0,
        "",
        5,
        "LUIZ RASSI",
        "GOI\u00c2NIA",
        "PRESENCIAL",
        "CAPACITA\u00c7\u00c3O",
        "TRANSFORMA\u00c7\u00c3O DIGITAL",
        1666828800000,
        1669507200000,
        1666828800000,
        1669507200000,
        46,
        "27 de outubro de 2022",
        "27 de novembro de 2022",
        "27\/10\/2022",
        "27\/11\/2022",
        "27\/10\/2022"
    ]
]

columns = [
    {"name":"id","type":"integer"},
    {"name":"diretoria","type":"string"},
    {"name":"escola_id","type":"integer"},
    {"name":"tipo_curso_id","type":"integer"},
    {"name":"curso_id","type":"string"},
    {"name":"turno","type":"string"},
    {"name":"ano","type":"integer"},
    {"name":"modalidade_id","type":"integer"},
    {"name":"trimestre","type":"integer"},
    {"name":"carga_horaria","type":"integer"},
    {"name":"vagas_totais","type":"integer"},
    {"name":"vagas_turma","type":"integer"},
    {"name":"carga_horaria_total","type":"integer"},
    {"name":"previsao_inicio","type":"string"},
    {"name":"previsao_fim","type":"string"},
    {"name":"dias_semana","type":"string"},
    {"name":"previsao_abertura_edital","type":"string"},
    {"name":"previsao_fechamento_edital","type":"string"},
    {"name":"data_registro","type":"string"},
    {"name":"eixo_id","type":"integer"},
    {"name":"udepi_id","type":"integer"},
    {"name":"situacao","type":"integer"},
    {"name":"jus_reprovacao","type":"string"},
    {"name":"num_edital_id","type":"integer"},
    {"name":"escola","type":"string"},
    {"name":"municipio","type":"string"},
    {"name":"modalidade","type":"string"},
    {"name":"tipo","type":"string"},
    {"name":"curso","type":"string"},
    {"name":"dt_ini_edit","type":"string"},
    {"name":"dt_fim_edit","type":"string"},
    {"name":"dt_ini_insc","type":"string"},
    {"name":"dt_fim_insc","type":"string"},
    {"name":"escola_id","type":"integer"},
    {"name":"previsao_abertura_edital_estenso","type":"string"},
    {"name":"previsao_fechamento_edital_estenso","type":"string"},
    {"name":"previsao_abertura_edital_normal","type":"string"},
    {"name":"previsao_fechamento_edital_normal","type":"string"},
    {"name":"previsao_inicio_inscricao","type":"string"}
]

mappedJson = []

for cont in range(len(content)):
    for col in range(len(columns)):
        mappedJson.append({columns[col]['name']: content[cont][col]})
