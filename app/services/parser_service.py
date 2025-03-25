import json
import logging
from typing import Dict, Any, Optional, List
from dataclasses import dataclass

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ParserError(Exception):
    """Base exception for parser errors"""
    pass

class ValidationError(ParserError):
    """Exception raised for validation errors"""
    pass

class ParseSectionError(ParserError):
    """Exception raised when parsing a specific section fails"""
    pass

@dataclass
class ParsedSection:
    """Data class to track parsing status of each section"""
    name: str
    success: bool
    error: Optional[str] = None

class ParserService:
    """Service for parsing credit report text and extracting structured data."""
    
    def __init__(self):
        """Initialize the parser service."""
        self.text = ""
        self.parsed_data = {
            "inquirer": {},
            "personal_data": {},
            "score": None,
            "summary_open_accounts": [],
            "details_open_accounts": []
        }
        self.parsing_status: List[ParsedSection] = []

    def _validate_input(self, text: str) -> None:
        """
        Validate the input text before parsing.
        
        Args:
            text (str): The text content to validate
            
        Raises:
            ValidationError: If the input text is invalid
        """
        if not text:
            raise ValidationError("Input text cannot be empty")
        
        required_sections = [
            "suscriptor:",
            "cedula",
            "transunion creditvision score",
            "resumen de cuentas abiertas",
            "detalle de cuentas abiertas"
        ]
        
        missing_sections = [
            section for section in required_sections 
            if section.lower() not in text.lower()
        ]
        
        if missing_sections:
            raise ValidationError(
                f"Missing required sections: {', '.join(missing_sections)}"
            )

    def extract_section(self, start_marker: str, end_marker: str = None) -> Optional[str]:
        """
        Extract a section of text between start and end markers.

        Args:
            start_marker (str): Starting text to find
            end_marker (str): Optional ending text to find
            
        Returns:
            Optional[str]: Extracted text section or None if not found
        """
        try:
            start_index = self.text.lower().find(start_marker.lower())
            if start_index == -1:
                return None

            start_index += len(start_marker)

            if end_marker:
                end_index = self.text.lower().find(end_marker.lower(), start_index)
                return (
                    self.text[start_index:end_index].strip() 
                    if end_index != -1 
                    else self.text[start_index:].strip()
                )

            return self.text[start_index:].strip()
        except Exception as e:
            logger.error(f"Error extracting section {start_marker}: {str(e)}")
            return None

    def _find_next_section_index(self, start_index: int) -> int:
        """
        Find the index of the next section to define section boundaries.

        Args:
            start_index (int): Starting index to search from
            
        Returns:
            int: Index of the next section
        """
        sections = [
            "transunion creditvision score",
            "resumen de cuentas abiertas",
            "detalle de cuentas abiertas",
            "detalle de cuentas cerradas / inactivas",
            "indagaciones ultimos 6 meses"
        ]

        next_indices = [
            self.text.lower().find(section.lower(), start_index) 
            for section in sections
        ]
        valid_indices = [idx for idx in next_indices if idx != -1]

        return min(valid_indices) if valid_indices else len(self.text)

    async def _parse_inquirer_info(self) -> None:
        """Parse inquirer information from the credit report."""
        try:
            self.parsed_data['inquirer'] = {
                "suscriptor": self.extract_section("suscriptor:", "usuario:"),
                "usuario": self.extract_section("usuario:", "fecha:"),
                "fecha consulta": self.extract_section("fecha:", "hora:"),
                "hora consulta": self.extract_section("hora:", "transunion")
            }
            
            # Validate parsed data
            if not all(self.parsed_data['inquirer'].values()):
                raise ParseSectionError("Missing required inquirer information")
                
            self.parsing_status.append(
                ParsedSection("inquirer", True)
            )
        except Exception as e:
            error_msg = f"Error parsing inquirer info: {str(e)}"
            logger.error(error_msg)
            self.parsing_status.append(
                ParsedSection("inquirer", False, error_msg)
            )
            raise ParseSectionError(error_msg)

    async def _parse_personal_data(self) -> None:
        """Parse personal data from the credit report."""
        try:
            # Parse phones
            phones = {
                "casa": self.extract_section("casa:", "trabajo:"),
                "trabajo": self.extract_section("trabajo:", "celular:"),
                "celular": self.extract_section("celular:", "direcciones")
            }

            # Parse addresses
            addresses_start = self.text.lower().find("direcciones")
            addresses_end = self._find_next_section_index(addresses_start)
            addresses_raw = self.text[addresses_start:addresses_end].split('* ')[1:]
            addresses = [
                addr.strip().replace('\n', ' ') 
                for addr in addresses_raw
            ]

            personal_data = {
                "cedula": self.extract_section("cedula", "nombres"),
                "nombres": self.extract_section("nombres", "apellidos"),
                "apellidos": self.extract_section("apellidos", "fecha nacimiento"),
                "fecha nacimiento": self.extract_section("fecha nacimiento", "edad"),
                "edad": self.extract_section("edad", "ocupacion"),
                "ocupacion": self.extract_section("ocupacion", "lugar nacimiento"),
                "lugar nacimiento": self.extract_section("lugar nacimiento", "pasaporte"),
                "pasaporte": self.extract_section("pasaporte", "estado civil"),
                "estado civil": self.extract_section("estado civil", "telefonos"),
                "telefonos": phones,
                "direcciones": addresses
            }

            # Validate required fields
            required_fields = ["cedula", "nombres", "apellidos", "fecha nacimiento"]
            missing_fields = [
                field for field in required_fields 
                if not personal_data.get(field)
            ]
            
            if missing_fields:
                raise ParseSectionError(
                    f"Missing required personal data fields: {', '.join(missing_fields)}"
                )

            self.parsed_data['personal_data'] = personal_data
            self.parsing_status.append(
                ParsedSection("personal_data", True)
            )
        except Exception as e:
            error_msg = f"Error parsing personal data: {str(e)}"
            logger.error(error_msg)
            self.parsing_status.append(
                ParsedSection("personal_data", False, error_msg)
            )
            raise ParseSectionError(error_msg)

    async def _parse_credit_score(self) -> None:
        """Parse credit score and related information."""
        try:
            score_index = self.text.lower().rfind("puntuacion")
            if score_index == -1:
                raise ParseSectionError("Credit score section not found")

            score = self.text[score_index + 10: score_index + 14].strip()
            
            # Validate score
            if not score.isdigit():
                raise ParseSectionError("Invalid credit score format")

            # Parse score factors
            factors_index = self.text.lower().find("factores")
            rnc_index = self.text.lower().find("rnc")

            factors = []
            if factors_index != -1 and rnc_index != -1:
                factors_text = self.text[factors_index + 36: rnc_index - 1]
                factors = [
                    factor.strip() 
                    for factor in factors_text.replace('* ', '').replace(') ', ')').split('\n') 
                    if factor.strip()
                ]

            self.parsed_data['score'] = {
                "score": score,
                "factors": factors
            }
            self.parsing_status.append(
                ParsedSection("credit_score", True)
            )
        except Exception as e:
            error_msg = f"Error parsing credit score: {str(e)}"
            logger.error(error_msg)
            self.parsing_status.append(
                ParsedSection("credit_score", False, error_msg)
            )
            raise ParseSectionError(error_msg)

    async def _parse_open_accounts_summary(self) -> None:
        """Parse summary of open accounts."""
        try:
            summary_index = self.text.lower().find("resumen de cuentas abiertas")
            if summary_index == -1:
                raise ParseSectionError("Open accounts summary section not found")

            # Find section boundaries
            end_sections = [
                "leyenda comportamiento historico",
                "detalle de cuentas abiertas"
            ]
            end_indices = [
                self.text.lower().find(section.lower(), summary_index) 
                for section in end_sections
            ]
            end_indices = [idx for idx in end_indices if idx != -1]
            summary_end_index = min(end_indices) if end_indices else len(self.text)

            # Extract and process summary
            summary_text = self.text[summary_index + 28: summary_end_index]
            summary_lines = summary_text.split('\n')

            try:
                first_row_start = 17
                last_row_end = summary_lines.index("total general >>")
            except ValueError:
                raise ParseSectionError("Could not find summary table boundaries")

            # Process rows
            data_rows = [
                summary_lines[i:i+11] 
                for i in range(first_row_start, last_row_end, 11)
            ]

            # Validate and clean data rows
            processed_rows = []
            for row in data_rows:
                if len(row) != 11:
                    logger.warning(f"Skipping invalid summary row: {row}")
                    continue
                    
                processed_rows.append({
                    "subscriber": row[0],
                    "accounts_amount": row[1],
                    "account_type": row[2],
                    "credit_amount_dop": row[3],
                    "credit_amount_usd": row[4],
                    "current_balance_dop": row[5],
                    "current_balance_usd": row[6],
                    "current_overdue_dop": row[7],
                    "current_overdue_usd": row[8],
                    "utilization_percent_dop": row[9],
                    "utilization_percent_usd": row[10],
                })

            self.parsed_data['summary_open_accounts'] = processed_rows
            self.parsing_status.append(
                ParsedSection("summary_open_accounts", True)
            )
        except Exception as e:
            error_msg = f"Error parsing open accounts summary: {str(e)}"
            logger.error(error_msg)
            self.parsing_status.append(
                ParsedSection("summary_open_accounts", False, error_msg)
            )
            raise ParseSectionError(error_msg)

    def _process_accounts_details_rows(self, details_rows: List[str]) -> List[List[str]]:
        """
        Process the rows of account details.
        
        Args:
            details_rows (List[str]): List of raw details rows
            
        Returns:
            List[List[str]]: Processed list of rows with subscribers
        """
        processed_rows = []
        current_sublist = []

        try:
            for elemento in details_rows:
                if ">>" in elemento:
                    if current_sublist:
                        # Process current sublist
                        details_subscriber = current_sublist[0].split(">>")
                        details_subscriber = [s.strip() for s in details_subscriber]
                        
                        # Process remaining rows
                        remaining_sublists = [
                            current_sublist[i:i+11] 
                            for i in range(1, len(current_sublist), 11)
                        ]
                        
                        for element in remaining_sublists:
                            full_row = details_subscriber + element
                            
                            # Process behavior vector
                            if len(full_row) >= 13:
                                try:
                                    behavior_vector = [
                                        int(char) if char.isdigit() else None 
                                        for char in full_row[12].replace(" ", "")
                                    ]
                                    full_row[12] = behavior_vector
                                except Exception:
                                    logger.warning(
                                        f"Could not parse behavior vector: {full_row[12]}"
                                    )
                            
                            processed_rows.append(full_row)
                        
                        current_sublist = []
                
                current_sublist.append(elemento)

            # Process the last sublist
            if current_sublist:
                details_subscriber = current_sublist[0].split(">>")
                details_subscriber = [s.strip() for s in details_subscriber]
                
                remaining_sublists = [
                    current_sublist[i:i+11] 
                    for i in range(1, len(current_sublist), 11)
                ]
                
                for element in remaining_sublists:
                    full_row = details_subscriber + element
                    if len(full_row) >= 13:
                        try:
                            behavior_vector = [
                                int(char) if char.isdigit() else None 
                                for char in full_row[12].replace(" ", "")
                            ]
                            full_row[12] = behavior_vector
                        except Exception:
                            logger.warning(
                                f"Could not parse behavior vector: {full_row[12]}"
                            )
                    
                    processed_rows.append(full_row)

        except Exception as e:
            logger.error(f"Error processing account details rows: {str(e)}")
            raise ParseSectionError("Failed to process account details rows")

        return processed_rows

    async def _parse_open_accounts_details(self) -> None:
        """Parse details of open accounts."""
        try:
            details_index = self.text.lower().find("detalle de cuentas abiertas")
            if details_index == -1:
                raise ParseSectionError("Open accounts details section not found")

            # Find section boundaries
            end_sections = [
                "detalle de cuentas cerradas / inactivas",
                "indagaciones ultimos 6 meses"
            ]
            end_indices = [
                self.text.lower().find(section.lower(), details_index) 
                for section in end_sections
            ]
            end_indices = [idx for idx in end_indices if idx != -1]
            details_end_index = min(end_indices) if end_indices else len(self.text)

            # Extract and process details
            details_text = self.text[details_index + 28: details_end_index]
            details_lines = details_text.split('\n')

            # Find table boundaries
            try:
                first_row_start = next(
                    (i for i, line in enumerate(details_lines) if ">>" in line), 
                    26
                )
                last_row_marker = "totales generales rd$:"
                last_row_end = next(
                    (i for i, line in enumerate(details_lines[first_row_start:]) 
                     if last_row_marker in line), 
                    len(details_lines)
                )
            except Exception as e:
                raise ParseSectionError(
                    f"Could not find details table boundaries: {str(e)}"
                )

            details_rows = details_lines[first_row_start:first_row_start + last_row_end]
            processed_rows = self._process_accounts_details_rows(details_rows)

            # Convert rows to structured data
            accounts_details = []
            for row in processed_rows:
                if len(row) < 12:
                    logger.warning(f"Skipping invalid details row: {row}")
                    continue
                    
                account_detail = {
                    "account_type": row[0],
                    "subscriber": row[1],
                    "status": row[2],
                    "update_date": row[3],
                    "opening_date": row[4],
                    "expiration_date": row[5],
                    "currency": row[6],
                    "credit_limit": row[7],
                    "current_balance": row[8],
                    "balance_in_arrears": row[9],
                    "minimum_payment_and_installment": row[10],
                    "no_of_installments_and_modality": row[11],
                }
                
                if len(row) > 12:
                    account_detail["behavior_vector_last_12_months"] = row[12]
                
                accounts_details.append(account_detail)

            self.parsed_data['details_open_accounts'] = accounts_details
            self.parsing_status.append(
                ParsedSection("details_open_accounts", True)
            )
        except Exception as e:
            error_msg = f"Error parsing open accounts details: {str(e)}"
            logger.error(error_msg)
            self.parsing_status.append(
                ParsedSection("details_open_accounts", False, error_msg)
            )
            raise ParseSectionError(error_msg)

    async def parse_credit_report(self, text: str) -> Dict[str, Any]:
        """
        Parse credit report text and extract relevant information.
        
        Args:
            text (str): The text content of the credit report
            
        Returns:
            Dict[str, Any]: Extracted credit report data in dictionary format
            
        Raises:
            ValidationError: If the input text is invalid
            ParseSectionError: If parsing of any section fails
        """
        try:
            # Reset state
            self.text = text
            self.parsed_data = {
                "inquirer": {},
                "personal_data": {},
                "score": None,
                "summary_open_accounts": [],
                "details_open_accounts": []
            }
            self.parsing_status = []

            # Validate input
            self._validate_input(text)
            logger.info("Input validation successful")

            # Parse each section
            await self._parse_inquirer_info()
            await self._parse_personal_data()
            await self._parse_credit_score()
            await self._parse_open_accounts_summary()
            await self._parse_open_accounts_details()

            # Validate overall parsing success
            failed_sections = [
                section for section in self.parsing_status 
                if not section.success
            ]
            
            if failed_sections:
                errors = [
                    f"{section.name}: {section.error}" 
                    for section in failed_sections
                ]
                raise ParserError(
                    f"Failed to parse sections: {', '.join(errors)}"
                )

            logger.info("Successfully parsed credit report")
            return self.parsed_data

        except ValidationError as e:
            logger.error(f"Validation error: {str(e)}")
            raise
        except ParseSectionError as e:
            logger.error(f"Section parsing error: {str(e)}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error parsing credit report: {str(e)}")
            raise ParserError(f"Failed to parse credit report: {str(e)}")

    def to_json(self, indent: int = 2) -> str:
        """
        Convert parsed data to JSON string.
        
        Args:
            indent (int): Indentation for JSON formatting
            
        Returns:
            str: JSON string of parsed data
        """
        return json.dumps(
            self.parsed_data,
            indent=indent,
            ensure_ascii=False
        )
