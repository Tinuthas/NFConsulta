from processamento.comunicacao import ComunicacaoSefaz
from lxml import etree
from utils.flags import NAMESPACE_NFE
from consulta.run_key_search import SearchKey
from model.NF import NF

certificado = "C:/Users/andre/OneDrive/Área de Trabalho/17521909_certA1.pfx"
senha = 'Athena2018'
uf = 'sp'
homologacao = False

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
"""

xml = con.consulta_nota('nfe', '35200643708379010830550050002904511102904515')
print (xml.text.encode('utf-8'))

ns = {'ns':NAMESPACE_NFE}
prot = etree.fromstring(xml.text.encode('utf-8')) # SEFAZ SP utilizar envio.content
status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
if status == '100':
  prot_nfe = prot[0][0].xpath('ns:retConsSitNFe/ns:protNFe', namespaces=ns)[0]
  xml = etree.tostring(prot_nfe, encoding='unicode')
  print(xml)"""
nf = NF('35', '20', '06', '43708379010830', '55')
search = SearchKey(con, nf)
list = search.run()

"""
2 - cUF - Código da UF do emitente do Documento Fiscal
4 AAMM - Ano e Mês de emissão da NF-e
14 CNPJ - CNPJ do emitente
2 mod - Modelo do Documento Fiscal
3 serie - Série do Documento Fiscal
9 nNF - Número do Documento Fiscal
9 cNF - Código Numérico que compõe a Chave de Acesso
1 cDV - Dígito Verificador da Chave de Acesso
"""
