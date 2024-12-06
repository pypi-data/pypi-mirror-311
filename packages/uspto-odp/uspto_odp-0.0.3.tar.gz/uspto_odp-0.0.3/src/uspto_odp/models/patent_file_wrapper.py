'''
MIT License

Copyright (c) 2024 Ken Thompson, https://github.com/KennethThompson, all rights reserved.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''
from dataclasses import dataclass, field
from datetime import date
from typing import List, Optional

from uspto_odp.models.patent_status import ApplicationStatus

@dataclass
class Event:
    """Represents a single event in the patent application timeline"""
    event_code: str
    event_description_text: str 
    event_date: date

    @classmethod
    def from_dict(cls, data: dict) -> 'Event':
        return cls(
            event_code=data['eventCode'],
            event_description_text=data['eventDescriptionText'],
            event_date=date.fromisoformat(data['eventDate'])
        )

@dataclass 
class Address:
    """Represents a physical address"""
    city_name: str
    geographic_region_code: Optional[str] = None
    postal_code: Optional[str] = None
    country_code: Optional[str] = None
    address_line_one: Optional[str] = None
    address_line_two: Optional[str] = None
    name_line_one: Optional[str] = None

    @classmethod
    def from_dict(cls, data: dict) -> 'Address':
        return cls(
            city_name=data.get('cityName', ''),
            geographic_region_code=data.get('geographicRegionCode'),
            postal_code=data.get('postalCode'),
            country_code=data.get('countryCode'),
            address_line_one=data.get('addressLineOneText'),
            address_line_two=data.get('addressLineTwoText'),
            name_line_one=data.get('nameLineOneText')
        )

@dataclass
class Inventor:
    """Represents a patent inventor"""
    first_name: str
    last_name: str
    middle_name: Optional[str] = None
    country_code: Optional[str] = None
    addresses: List[Address] = field(default_factory=list)

    @classmethod
    def from_dict(cls, data: dict) -> 'Inventor':
        """
        Create Inventor from API response data with graceful handling of missing fields
        """
        addresses = [Address.from_dict(addr) for addr in data.get('correspondenceAddressBag', [])]
        return cls(
            first_name=data.get('firstName', ''),
            last_name=data.get('lastName', ''),
            middle_name=data.get('middleName'),
            country_code=data.get('countryCode'),
            addresses=addresses
        )

@dataclass
class ApplicationMetadata:
    """Represents patent application metadata"""
    first_inventor_to_file_indicator: str
    application_status_code: int
    application_type_code: str
    filing_date: date
    first_inventor_name: str
    invention_title: str
    patent_number: Optional[str] = None
    grant_date: Optional[date] = None
    
    @property
    def status(self) -> str:
        """Returns the string description of the application status"""
        try:
            return ApplicationStatus(str(self.application_status_code)).name.replace('_', ' ').title()
        except ValueError:
            return f"Unknown Status Code: {self.application_status_code}"
    
    @classmethod
    def from_dict(cls, data: dict) -> 'ApplicationMetadata':
        return cls(
            first_inventor_to_file_indicator=data['firstInventorToFileIndicator'],
            application_status_code=data['applicationStatusCode'],
            application_type_code=data['applicationTypeCode'],
            filing_date=date.fromisoformat(data['filingDate']),
            first_inventor_name=data['firstInventorName'],
            invention_title=data['inventionTitle'],
            patent_number=data.get('patentNumber'),
            grant_date=date.fromisoformat(data['grantDate']) if 'grantDate' in data else None
        )

@dataclass
class PatentFileWrapper:
    """Main class representing a patent file wrapper"""
    application_number: str
    events: List[Event]
    metadata: ApplicationMetadata
    inventors: List[Inventor]

    @classmethod
    def from_dict(cls, data: dict) -> 'PatentFileWrapper':
        wrapper_data = data['patentFileWrapperDataBag'][0]
        
        return cls(
            application_number=wrapper_data['applicationNumberText'],
            events=[Event.from_dict(event) for event in wrapper_data['eventDataBag']],
            metadata=ApplicationMetadata.from_dict(wrapper_data['applicationMetaData']),
            inventors=[Inventor.from_dict(inv) for inv in 
                      wrapper_data['applicationMetaData'].get('inventorBag', [])]
        )

    @classmethod
    def parse_response(cls, response_json: dict) -> 'PatentFileWrapper':
        """Parse the complete USPTO API response"""
        return cls.from_dict(response_json)
