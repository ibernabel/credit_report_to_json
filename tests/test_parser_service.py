import pytest
from app.services.parser_service import (
    ParserService,
    ValidationError,
    ParseSectionError,
    ParserError
)

@pytest.mark.asyncio
class TestParserService:
    @pytest.fixture
    def parser_service(self):
        return ParserService()

    @pytest.fixture
    def valid_credit_report_text(self, sample_text_content):
        return """
        SUSCRIPTOR: BANCO TEST
        USUARIO: JOHN DOE
        FECHA: 25/03/2024
        HORA: 14:30

        CEDULA: 001-0000000-0
        NOMBRES: JOHN
        APELLIDOS: DOE
        FECHA NACIMIENTO: 01/01/1990
        EDAD: 34
        OCUPACION: DEVELOPER
        LUGAR NACIMIENTO: SANTO DOMINGO
        PASAPORTE: AB123456
        ESTADO CIVIL: SOLTERO
        
        TELEFONOS:
        CASA: 809-555-0000
        TRABAJO: 809-555-1111
        CELULAR: 809-555-2222
        
        DIRECCIONES:
        * CALLE PRINCIPAL #123, SANTO DOMINGO
        * AVENIDA CENTRAL #456, SANTIAGO
        
        TRANSUNION CREDITVISION SCORE
        PUNTUACION 750
        
        FACTORES QUE AFECTAN SU PUNTUACION:
        * FACTOR 1
        * FACTOR 2
        
        RNC: 123456789
        
        RESUMEN DE CUENTAS ABIERTAS
        
        TIPO DE CUENTA                 CANTIDAD    LIMITE    BALANCE    ATRASO
        TARJETA DE CREDITO            1           50000     25000      0
        PRESTAMO PERSONAL             1           100000    75000      0
        
        TOTAL GENERAL >>              2           150000    100000     0
        
        DETALLE DE CUENTAS ABIERTAS
        
        TARJETA DE CREDITO >> BANCO TEST
        ACTIVA    25/03/2024    01/01/2023    25/12/2025    DOP    50000    25000    0    5000    12    111111111111
        
        PRESTAMO PERSONAL >> BANCO TEST
        ACTIVO    25/03/2024    01/01/2023    25/12/2025    DOP    100000   75000    0    10000   36    111111111111
        
        TOTALES GENERALES RD$: 150000
        """

    async def test_validate_input_empty_text(self, parser_service):
        with pytest.raises(ValidationError, match="Input text cannot be empty"):
            parser_service._validate_input("")

    async def test_validate_input_missing_sections(self, parser_service):
        with pytest.raises(ValidationError, match="Missing required sections"):
            parser_service._validate_input("Some invalid text")

    async def test_parse_inquirer_info(self, parser_service, valid_credit_report_text):
        parser_service.text = valid_credit_report_text
        await parser_service._parse_inquirer_info()
        
        assert parser_service.parsed_data["inquirer"]["suscriptor"] == "BANCO TEST"
        assert parser_service.parsed_data["inquirer"]["usuario"] == "JOHN DOE"
        assert parser_service.parsed_data["inquirer"]["fecha consulta"] == "25/03/2024"
        assert parser_service.parsed_data["inquirer"]["hora consulta"] == "14:30"

    async def test_parse_personal_data(self, parser_service, valid_credit_report_text):
        parser_service.text = valid_credit_report_text
        await parser_service._parse_personal_data()
        
        personal_data = parser_service.parsed_data["personal_data"]
        assert personal_data["cedula"] == "001-0000000-0"
        assert personal_data["nombres"] == "JOHN"
        assert personal_data["apellidos"] == "DOE"
        assert personal_data["fecha nacimiento"] == "01/01/1990"
        assert len(personal_data["direcciones"]) == 2
        assert personal_data["telefonos"]["casa"] == "809-555-0000"

    async def test_parse_credit_score(self, parser_service, valid_credit_report_text):
        parser_service.text = valid_credit_report_text
        await parser_service._parse_credit_score()
        
        assert parser_service.parsed_data["score"]["score"] == "750"
        assert len(parser_service.parsed_data["score"]["factors"]) == 2

    async def test_parse_open_accounts_summary(self, parser_service, valid_credit_report_text):
        parser_service.text = valid_credit_report_text
        await parser_service._parse_open_accounts_summary()
        
        summary = parser_service.parsed_data["summary_open_accounts"]
        assert len(summary) == 2
        assert summary[0]["account_type"] == "TARJETA DE CREDITO"
        assert summary[0]["accounts_amount"] == "1"

    async def test_parse_open_accounts_details(self, parser_service, valid_credit_report_text):
        parser_service.text = valid_credit_report_text
        await parser_service._parse_open_accounts_details()
        
        details = parser_service.parsed_data["details_open_accounts"]
        assert len(details) == 2
        assert details[0]["account_type"] == "TARJETA DE CREDITO"
        assert details[0]["subscriber"] == "BANCO TEST"
        assert details[0]["behavior_vector_last_12_months"] == [1] * 12

    async def test_full_parse_credit_report(self, parser_service, valid_credit_report_text):
        result = await parser_service.parse_credit_report(valid_credit_report_text)
        
        assert result["inquirer"]["suscriptor"] == "BANCO TEST"
        assert result["personal_data"]["cedula"] == "001-0000000-0"
        assert result["score"]["score"] == "750"
        assert len(result["summary_open_accounts"]) == 2
        assert len(result["details_open_accounts"]) == 2

    async def test_parse_invalid_credit_report(self, parser_service):
        invalid_text = "Invalid credit report content"
        with pytest.raises(ValidationError):
            await parser_service.parse_credit_report(invalid_text)

    def test_to_json(self, parser_service):
        parser_service.parsed_data = {
            "test": "data",
            "nested": {"key": "value"}
        }
        json_output = parser_service.to_json()
        assert '"test": "data"' in json_output
        assert '"nested": {' in json_output
        assert '"key": "value"' in json_output
