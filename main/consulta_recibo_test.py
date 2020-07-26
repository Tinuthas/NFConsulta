from processamento.comunicacao import ComunicacaoSefaz

certificado = "C:/Users/andre/OneDrive/Área de Trabalho/17521909_certA1.pfx"
senha = 'Athena2018'
uf = 'sp'
homologacao = False

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_recibo('nfe', '135200535797755')
print (xml.text.encode('utf-8'))