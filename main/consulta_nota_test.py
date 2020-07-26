from processamento.comunicacao import ComunicacaoSefaz

certificado = "/home/user/certificado.pfx"
senha = 'senha'
uf = 'sp'
homologacao = False

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_nota('nfe', '35200643708379010830550050002904511102904515')
print (xml.text.encode('utf-8'))