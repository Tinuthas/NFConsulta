from processamento.comunicacao import ComunicacaoSefaz

certificado = "C:/Users/andre/OneDrive/Área de Trabalho/17521909_certA1.pfx"
senha = 'Athena2018'
uf = 'sp'
homologacao = True

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.status_servico('nfe')
print (xml.text)