# App_Patrimonio

O software em questão foi desenvolvido por mim em 2021 para operacionalizar o processo de levantamento patrimonial do Instituto de Física da Universidade de Brasília.
O softtware App_Patrimonio é capaz de adicionar, alterar e excluir bens a uma base de dados com cerca de 10 mil itens.

Na época em que desenvolvi o presente o software, eu ainda não possuía domínio da biblioteca Pandas. Por isso, precisei definir algumas funções de tratamentos de dados a partir de dicionários python.

O software é capaz de ler o código de barras da etiqueta de cada bem do Instituto de Física, retornando os atributos daquele bem e permitindo alterações.
Caso o usuário prefira, ao invés de realizar a leitura do código de barras, ele pode digitar o número de tombamento ou ativar o reconhecimento de fala e pronunciar o número de tombamento. O efeito será o mesmo.
