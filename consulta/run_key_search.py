from model import NF

from lxml import etree
from utils.flags import NAMESPACE_NFE

class SearchKey:

    list = []

    def __init__(self, con, nf):
        self.con = con
        self.nf = nf

    def run(self):
        self.getNumberSerie()
        return list


    def consumption(self):
        key = self.nf.getCompleteNfe()
        try:

            xml = self.con.consulta_nota('nfe', key)
            print(xml.text.encode('utf-8'))

            ns = {'ns': NAMESPACE_NFE}
            prot = etree.fromstring(xml.text.encode('utf-8'))  # SEFAZ SP utilizar envio.content
            status = prot[0][0].xpath('ns:retConsSitNFe/ns:cStat', namespaces=ns)[0].text
        #if status == '100':
        #    prot_nfe = prot[0][0].xpath('ns:retConsSitNFe/ns:protNFe', namespaces=ns)[0]
        #    xml = etree.tostring(prot_nfe, encoding='unicode')
        #    print(xml)
            return status
        except Exception as e:
            print('error', e)
            return '999'



    def getNumberSerie(self):
        for i in range(0, 999):
            self.nf.numberSerie = '%003d' % i
            print('%003d' % i)
            status = self.getNumberNF()
            if status != None:
                if status == '562' or status == '897':
                    continue
                else:
                    return status

    def getNumberNF(self):
        for i in range(0, 999999999):
            self.nf.numberNF = '%000000009d' % i
            print('%000000009d' % i)
            status = self.getNumberCH()
            if status != None:
                if status == '562' or status == '897':
                    continue
                else:
                    return status
        return None

    def getNumberCH(self):
        for i in range(0, 999999999):
            self.nf.numberCH = '%000000009d' % i
            print('%000000009d' % i)
            status = self.getDigitCH()
            if status != None:
                if status == '562' or status == '897':
                    continue
                else:
                    return status
        return None


    def getDigitCH(self):
        for i in range(0, 9):
            self.nf.digitCH = str(i)
            print(i)
            status = self.consumption()
            if status == '100':
                list.append(self.nf.getCompleteNfe())
                continue
            elif status == '562' or status == '897':
                return status
            elif status == '236':
                continue
            else:
                return status
        return None

