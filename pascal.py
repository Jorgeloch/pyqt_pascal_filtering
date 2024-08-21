def piramidePascal(n):
    tabela = [[1],[1,1]]
    for i in range(1,n):
        linha = [1]
        for j in range(0,len(tabela[i])-1):
            linha += [ tabela[i][j] + tabela[i][j+1] ]
        linha.append(1)
        tabela.append(linha)
    return tabela
