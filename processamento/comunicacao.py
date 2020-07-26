import requests
import re

from lxml import etree

from entidades.certificado import CertificadoA1
from utils.webservices import NFE, NFCE, NFSE

from utils.flags import (
    NAMESPACE_NFE,
    NAMESPACE_XSD,
    NAMESPACE_XSI,
    VERSAO_PADRAO,
    NAMESPACE_SOAP,
    CODIGOS_ESTADOS,
    NAMESPACE_BETHA,
    NAMESPACE_METODO
)
from .assinatura import AssinaturaA1


class Comunicacao(object):
    """
    Classe abstrata responsavel por definir os metodos e logica das classes
    de comunicação com os webservices da NF-e.
    """

    _ambiente = 1   # 1 = Produção, 2 = Homologação
    uf = None
    certificado = None
    certificado_senha = None
    url = None

    def __init__(self, uf, certificado, certificado_senha, homologacao=False):
        self.uf = uf
        self.certificado = certificado
        self.certificado_senha = certificado_senha
        self._ambiente = 2 if homologacao else 1


class ComunicacaoSefaz(Comunicacao):
    """Classe de comunicação que segue o padrão definido para as SEFAZ dos Estados."""

    _versao = VERSAO_PADRAO
    _assinatura = AssinaturaA1

    def consulta_nota(self, modelo, chave):
        """
            Este método oferece a consulta da situação da NF-e/NFC-e na Base de Dados do Portal
            da Secretaria de Fazenda Estadual.
        :param modelo: Modelo da nota
        :param chave: Chave da nota
        :return:
        """
        # url do serviço
        url = self._get_url(modelo=modelo, consulta='CHAVE')
        # Monta XML do corpo da requisição
        raiz = etree.Element('consSitNFe', versao=VERSAO_PADRAO, xmlns=NAMESPACE_NFE)
        etree.SubElement(raiz, 'tpAmb').text = str(self._ambiente)
        etree.SubElement(raiz, 'xServ').text = 'CONSULTAR'
        etree.SubElement(raiz, 'chNFe').text = chave
        # Monta XML para envio da requisição
        xml = self._construir_xml_soap('NFeConsultaProtocolo4', raiz)
        print(etree.tostring(xml, pretty_print=False))
        return self._post(url, xml)

    def consulta_recibo(self, modelo, numero):
        """
        Este método oferece a consulta do resultado do processamento de um lote de NF-e.
        O aplicativo do Contribuinte deve ser construído de forma a aguardar um tempo mínimo de
        15 segundos entre o envio do Lote de NF-e para processamento e a consulta do resultado
        deste processamento, evitando a obtenção desnecessária do status de erro 105 - "Lote em
        Processamento".
        :param modelo: Modelo da nota
        :param numero: Número da nota
        :return:
        """

        # url do serviço
        url = self._get_url(modelo=modelo, consulta='RECIBO')

        # Monta XML do corpo da requisição
        raiz = etree.Element('consReciNFe', versao=VERSAO_PADRAO, xmlns=NAMESPACE_NFE)
        etree.SubElement(raiz, 'tpAmb').text = str(self._ambiente)
        etree.SubElement(raiz, 'nRec').text = numero

        # Monta XML para envio da requisição
        xml = self._construir_xml_soap('NFeRetAutorizacao4', raiz)
        return self._post(url, xml)

    def status_servico(self, modelo):
        """
        Verifica status do servidor da receita.
        :param modelo: modelo é a string com tipo de serviço que deseja consultar, Ex: nfe ou nfce
        :return:
        """
        url = self._get_url(modelo, 'STATUS')
        # Monta XML do corpo da requisição
        raiz = etree.Element('consStatServ', versao=VERSAO_PADRAO, xmlns=NAMESPACE_NFE)
        etree.SubElement(raiz, 'tpAmb').text = str(self._ambiente)
        etree.SubElement(raiz, 'cUF').text = CODIGOS_ESTADOS[self.uf.upper()]
        etree.SubElement(raiz, 'xServ').text = 'STATUS'
        xml = self._construir_xml_soap('NFeStatusServico4', raiz)
        return self._post(url, xml)

    def _get_url_an(self, consulta):
        # producao
        if self._ambiente == 1:
            if consulta == 'DISTRIBUICAO':
                ambiente = 'https://www1.'
            else:
                ambiente = 'https://www.'
        # homologacao
        else:
            ambiente = 'https://hom.'

        self.url = ambiente + NFE['AN'][consulta]
        return self.url

    def _get_url(self, modelo, consulta):
        """ Retorna a url para comunicação com o webservice """
        # estado que implementam webservices proprios
        lista = ['PR', 'MS', 'SP', 'AM', 'CE', 'BA', 'GO', 'MG', 'MT', 'PE', 'RS']
        if self.uf.upper() in lista:
            if self._ambiente == 1:
                ambiente = 'HTTPS'
            else:
                ambiente = 'HOMOLOGACAO'
            if modelo == 'nfe':
                # nfe Ex: https://nfe.fazenda.pr.gov.br/nfe/NFeStatusServico3
                self.url = NFE[self.uf.upper()][ambiente] + NFE[self.uf.upper()][consulta]
            elif modelo == 'nfce':
                # PE e BA são as únicas UF'sque possuem NFE proprio e SVRS para NFCe
                if self.uf.upper() == 'PE' or self.uf.upper() == 'BA':
                    self.url = NFCE['SVRS'][ambiente] + NFCE['SVRS'][consulta]
                else:
                    # nfce Ex: https://homologacao.nfce.fazenda.pr.gov.br/nfce/NFeStatusServico3
                    self.url = NFCE[self.uf.upper()][ambiente] + NFCE[self.uf.upper()][consulta]
            else:
                raise Exception('Modelo não encontrado! Defina modelo="nfe" ou "nfce"')
        # Estados que utilizam outros ambientes
        else:
            lista_svrs = ['AC', 'AL', 'AP', 'DF', 'ES', 'PB', 'PI', 'RJ', 'RN', 'RO', 'RR', 'SC', 'SE', 'TO']
            if self.uf.upper() in lista_svrs:
                if self._ambiente == 1:
                    ambiente = 'HTTPS'
                else:
                    ambiente = 'HOMOLOGACAO'
                if modelo == 'nfe':
                    # nfe Ex: https://nfe.fazenda.pr.gov.br/nfe/NFeStatusServico3
                    self.url = NFE['SVRS'][ambiente] + NFE['SVRS'][consulta]
                elif modelo == 'nfce':
                    # nfce Ex: https://homologacao.nfce.fazenda.pr.gov.br/nfce/NFeStatusServico3
                    self.url = NFCE['SVRS'][ambiente] + NFCE['SVRS'][consulta]
                else:
                    raise Exception('Modelo não encontrado! Defina modelo="nfe" ou "nfce"')
            # unico UF que utiliza SVAN ainda para NF-e
            # SVRS para NFC-e
            elif self.uf.upper() == 'MA':
                if self._ambiente == 1:
                    ambiente = 'HTTPS'
                else:
                    ambiente = 'HOMOLOGACAO'
                if modelo == 'nfe':
                    # nfe Ex: https://nfe.fazenda.pr.gov.br/nfe/NFeStatusServico3
                    self.url = NFE['SVAN'][ambiente] + NFE['SVAN'][consulta]
                elif modelo == 'nfce':
                    # nfce Ex: https://homologacao.nfce.fazenda.pr.gov.br/nfce/NFeStatusServico3
                    self.url = NFCE['SVRS'][ambiente] + NFCE['SVRS'][consulta]
                else:
                    raise Exception('Modelo não encontrado! Defina modelo="nfe" ou "nfce"')
            else:
                raise Exception(f"Url não encontrada para {modelo} e {consulta} {self.uf.upper()}")
        return self.url

    def _construir_xml_soap(self, metodo, dados, cabecalho=False):
        """Mota o XML para o envio via SOAP"""
        raiz = etree.Element('{%s}Envelope' % NAMESPACE_SOAP, nsmap={
          'xsi': NAMESPACE_XSI, 'xsd': NAMESPACE_XSD,'soap': NAMESPACE_SOAP})
        body = etree.SubElement(raiz, '{%s}Body' % NAMESPACE_SOAP)
        ## distribuição tem um corpo de xml diferente
        if metodo == 'NFeDistribuicaoDFe':
            x = etree.SubElement(body, 'nfeDistDFeInteresse', xmlns=NAMESPACE_METODO+metodo)
            a = etree.SubElement(x, 'nfeDadosMsg')
        else:
            a = etree.SubElement(body, 'nfeDadosMsg', xmlns=NAMESPACE_METODO+metodo)
        a.append(dados)
        return raiz

    def _post_header(self):
        """Retorna um dicionário com os atributos para o cabeçalho da requisição HTTP"""
        # PE é a única UF que exige SOAPAction no header
        response = {
            'content-type': 'application/soap+xml; charset=utf-8;',
            'Accept': 'application/soap+xml; charset=utf-8;',
        }
        if self.uf.upper() == 'PE':
            response["SOAPAction"] = ""
        return response

    def _post(self, url, xml):
        certificado_a1 = CertificadoA1(self.certificado)
        chave, cert = certificado_a1.separar_arquivo(self.certificado_senha, caminho=True)
        chave_cert = (cert, chave)
        # Abre a conexão HTTPS
        try:
            xml_declaration = '<?xml version="1.0" encoding="UTF-8"?>'

            # limpa xml com caracteres bugados para infNFeSupl em NFC-e
            xml = re.sub(
                '<qrCode>(.*?)</qrCode>',
                lambda x: x.group(0).replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', ''),
                etree.tostring(xml, encoding='unicode').replace('\n', '')
            )
            xml = xml_declaration + xml
            # Faz o request com o servidor
            result = requests.post(url, xml, headers=self._post_header(), cert=chave_cert, verify=False)
            result.encoding = 'utf-8'
            return result
        except requests.exceptions.RequestException as e:
            raise e
        finally:
            certificado_a1.excluir()