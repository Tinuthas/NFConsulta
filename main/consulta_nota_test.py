from processamento.comunicacao import ComunicacaoSefaz

certificado = "C:/Users/andre/OneDrive/Área de Trabalho/17521909_certA1.pfx"
senha = 'Athena2018'
uf = 'sp'
homologacao = False

con = ComunicacaoSefaz(uf, certificado, senha, homologacao)
xml = con.consulta_nota('nfe', '35200643708379010830550050002904511102904515')
print (xml.text.encode('utf-8'))


from lxml import etree
from utils.flags import NAMESPACE_NFE

ns = {'ns':NAMESPACE_NFE}
prot = etree.fromstring(xml.text.encode('utf-8')) # SEFAZ SP utilizar envio.content
status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
if status == '100':
  prot_nfe = prot[0][0].xpath('ns:retConsSitNFe/ns:protNFe', namespaces=ns)[0]
  xml = etree.tostring(prot_nfe, encoding='unicode')
  print(xml)