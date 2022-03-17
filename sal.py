class Sal:
    def __init__(self) -> None:
        
        self.address = "http://sal.receita.fazenda.gov.br/PortalSalInternet/faces/pages/calcContribuicoesCI/filiadosApos/selecionarOpcoesCalculoApos.xhtml"

        # phase one elements
        self.categoryInputId    = "opcoesCalcContribuicoesCI:categoria"
        self.nitInputId         = "opcoesCalcContribuicoesCI:nome"
        self.captchaInputId     = "captcha_campo_resposta"
        self.firstConfirmButtonId       = "opcoesCalcContribuicoesCI:botaoConfirmar"
        self.secondComfirmButtonName    = "formDadosCadastraisCalcContribuicoesCI:j_id38"
        
        # phase two elements
        self.paymentCodeInputId = "informarSalariosContribuicaoDomestico:selCodigoPagamento"
        self.paymentDateInputId = "informarSalariosContribuicaoDomestico:dataPag"
        self.licenseMaternityInputId = "informarSalariosContribuicaoDomestico:licencaMaternidade:?"
            # replace ? to 0 for YES and 1 for NO

        # payments values
            # Contribuinte Individual
                # 1007 - CONTRIBUINTE INDIVIDUAL - RECOLHIMENTO MENSAL NIT/PIS/PASEP
                # 1163 - CONTRIBUINTE INDIVIDUAL - OPÇÃO 11% (ART. 80 DA LC 123/2006) RECOLHIMENTO MENSAL - NIT/PIS/PASEP
                # 1120 - CONTRIBUINTE INDIVIDUAL - RECOLHIMENTO MENSAL - COM DEDUCAO DE 45% (LEI  9.876/99) - NIT/PIS/PASEP
                # 1236 - CI OPTANTE LC 123 MENSAL RURAL
                # 1287 - CI MENSAL RURAL
                # 1805 - CI COM DIREITO A DEDUCAO MENSAL - RURAL

            # Doméstico
                # 1600 - EMPREGADO DOMESTICO MENSAL - NIT /PIS/PASEP
            
            # Facultativo
                # 1406 - FACULTATIVO MENSAL - NIT/PIS/PASEP
                # 1473 - FACULTATIVO - OPÇÃO 11% (ART. 80 DA LC 123/2006) RECOLHIMENTO MENSAL - NIT/PIS/PASEP
                # 1929 - FACULTATIVO BAIXA RENDA - RECOLHIMENTO MENSAL - NIT/PIS/PASEP

            # Segurado Especial
                # 1503 - SEGURADO ESPECIAL MENSAL - NIT/PIS/PASEP
    
        self.thirdComfirmButtonName = "informarSalariosContribuicaoDomestico:j_id50"

        # phase three elements
        self.generateGPSButtonName = "formExibirDiscriminativoCI:j_id66"

