class NF:

    def __init__(self, uf: str, year: str, month: str, cnpj: str, mod: str, numberSerie = '', numberNF = '', numberCH = '', digitCH = ''):
        self.uf = uf
        self.year = year
        self.month = month
        self.cnpj = cnpj
        self.mod = mod
        self.numberSerie = numberSerie
        self.numberNF = numberNF
        self.numberCH = numberCH
        self.digitCH = digitCH

    def getCompleteNfe(self):
        return self.uf + self.year + self.month + self.cnpj + self.mod + self.numberSerie + self.numberNF + self.numberCH + self.digitCH

    def get_new_nf(self):
        return NF(self, self.uf, self.year, self.month, self.cnpj, self.mod)
