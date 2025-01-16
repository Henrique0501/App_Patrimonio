O que fazer antes de executar esse programa?
- Execute o arquivo Adicionar_novos_locais.py da pasta PLANILHAS_LOCALIDADES
- Cheque as últimas linhas do arquivo Locais_geral.xlsx. Caso algum dado esteja vazio, você pode completá-lo, dando novos nomes para essas localidades
- Pronto! Agora você pode executar o Dashboard_patrimonio.
- Caso aconteça algum erro ao iniciar o programa, leia atentamente a mensagem exibida no terminal.   Certamente essa mensagem será do seguinte tipo:
      ind = list(df_bens["Denominação"]).index(bem)
      ValueError: 'XARÍNFOLA' is not in list
  em que XARÍNFOLA é um bem fictício criado para este exemplo.
  Nesse caso você deve adicionar o nome XARÍNFOLA no arquivo Bens_IF.xlsx da pasta PLANILHAS_GERAIS e especificar seu tipo (LABORATORIO/ELETRONICO/TABLET/MOBILIA/NOTEBOOK/MONITOR/COMPUTADOR/AR CONDICIONADO/MATERIAL BIBLIOGRAFICO/QUADRO/OUTROS)


Como esse dashboard será apresentado à entes reguladoras da carga patrimonial do IF, ele já está funcionando com novos nomes das localidades.

O arquivo que contém a relação de nomes antigos e nomes atualizados é o arquivo Locais_geral.xlsx da pasta PLANILHAS_LOCALIDADES.