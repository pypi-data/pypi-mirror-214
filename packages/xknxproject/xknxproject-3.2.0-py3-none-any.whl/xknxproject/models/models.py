"""Define internally used data structures."""
from __future__ import annotations

from dataclasses import dataclass
import re

from xknxproject.models.knxproject import DPTType
from xknxproject.models.static import SpaceType
from xknxproject.zip import KNXProjContents


class XMLGroupAddress:
    """Class that represents a group address."""

    def __init__(
        self,
        name: str,
        identifier: str,
        address: str,
        project_uid: int | None,
        description: str,
        dpt: DPTType | None,
    ):
        """Initialize a group address."""
        self.name = name
        self.identifier = identifier.split("_")[1]
        self.raw_address = int(address)
        self.project_uid = project_uid
        self.description = description
        self.dpt = dpt

        self.address = self._parse_address()

    def _parse_address(self) -> str:
        """Parse a given address and returns a string representation of it."""
        main = (self.raw_address & 0b1111100000000000) >> 11
        middle = (self.raw_address & 0b11100000000) >> 8
        sub = self.raw_address & 0b11111111
        return f"{main}/{middle}/{sub}"

    def __repr__(self) -> str:
        """Return string representation."""
        return (
            f"{self.address} ({self.name}) - [DPT: {self.dpt}, ID: {self.identifier}]"
        )


@dataclass
class XMLArea:
    """Class that represents a area."""

    address: int
    name: str
    description: str | None
    lines: list[XMLLine]


@dataclass
class XMLLine:
    """Class that represents a Line."""

    address: int
    description: str | None
    name: str
    medium_type: str
    devices: list[DeviceInstance]
    area: XMLArea


class DeviceInstance:
    """Class that represents a device instance."""

    def __init__(
        self,
        *,
        identifier: str,
        address: str,
        project_uid: int | None,
        name: str,
        description: str,
        last_modified: str,
        product_ref: str,
        hardware_program_ref: str,
        line: XMLLine,
        manufacturer: str,
        additional_addresses: list[str] | None = None,
        com_object_instance_refs: list[ComObjectInstanceRef] | None = None,
        com_objects: list[ComObject] | None = None,
    ):
        """Initialize a Device Instance."""
        self.identifier = identifier
        self.address = address
        self.name = name
        self.description = description
        self.project_uid = project_uid
        self.last_modified = last_modified
        self.product_ref = product_ref
        self.hardware_program_ref = hardware_program_ref
        self.line = line
        self.manufacturer = manufacturer
        self.additional_addresses = additional_addresses or []
        self.com_object_instance_refs = com_object_instance_refs or []
        self.com_objects = com_objects or []
        self.application_program_ref: str | None = None

        self.individual_address = (
            f"{self.line.area.address}.{self.line.address}.{self.address}"
        )
        self.product_name: str = ""
        self.hardware_name: str = ""
        self.manufacturer_name: str = ""

    def add_additional_address(self, address: str) -> None:
        """Add an additional individual address."""
        self.additional_addresses.append(
            f"{self.line.area.address}/{self.line.address}/{address}"
        )

    def application_program_xml(self) -> str:
        """Obtain the file name to the application program XML."""
        return f"{self.manufacturer}/{self.application_program_ref}.xml"


@dataclass
class ComObjectInstanceRef:
    """Class that represents a ComObjectInstanceRef instance."""

    identifier: str | None  # "Id" - xs:ID
    # "RefId" - knx:RELIDREF - required - points to a ComObjectRef Id
    # initially stripped by the devices application_program_ref
    ref_id: str
    text: str | None  # "Text"
    function_text: str | None  # "FunctionText"
    read_flag: bool | None  # "ReadFlag" - knx:Enable_t
    write_flag: bool | None  # "WriteFlag" - knx:Enable_t
    communication_flag: bool | None  # "CommunicationFlag" - knx:Enable_t
    transmit_flag: bool | None  # "TransmitFlag" - knx:Enable_t
    update_flag: bool | None  # "UpdateFlag" - knx:Enable_t
    read_on_init_flag: bool | None  # "ReadOnInitFlag" - knx:Enable_t
    datapoint_types: list[DPTType]  # "DataPointType" - knx:IDREFS
    description: str | None  # "Description" - language dependent
    links: list[str] | None  # "Links" - knx:RELIDREFS

    # resolved via Hardware.xml from the containing DeviceInstance
    com_object_ref_id: str | None = None

    # only available form ComObject and ComObjectRef
    name: str | None = None
    number: int | None = None
    object_size: str | None = None

    def resolve_com_object_ref_id(
        self, application_program_ref: str, knx_proj_contents: KNXProjContents
    ) -> None:
        """Prepend the ref_id with the application program ref."""
        # Remove module and ModuleInstance occurrence as they will not be in the application program directly
        ref_id = re.sub(r"(M-\d+?_MI-\d+?_)", "", self.ref_id)
        if knx_proj_contents.is_ets4_project():
            self.com_object_ref_id = ref_id
        else:
            self.com_object_ref_id = f"{application_program_ref}_{ref_id}"

    def merge_from_application(self, com_object: ComObject | ComObjectRef) -> None:
        """Fill missing information with information parsed from the application program."""
        if self.name is None:
            self.name = com_object.name
        if self.text is None:
            self.text = com_object.text
        if self.function_text is None:
            self.function_text = com_object.function_text
        if self.object_size is None:
            self.object_size = com_object.object_size
        if self.read_flag is None:
            self.read_flag = com_object.read_flag
        if self.write_flag is None:
            self.write_flag = com_object.write_flag
        if self.communication_flag is None:
            self.communication_flag = com_object.communication_flag
        if self.transmit_flag is None:
            self.transmit_flag = com_object.transmit_flag
        if self.update_flag is None:
            self.update_flag = com_object.update_flag
        if self.read_on_init_flag is None:
            self.read_on_init_flag = com_object.read_on_init_flag
        if not self.datapoint_types:
            self.datapoint_types = com_object.datapoint_types
        if isinstance(com_object, ComObject):
            self.number = com_object.number


@dataclass
class ComObject:
    """Class that represents a ComObject instance."""

    __slots__ = (
        "identifier",
        "name",
        "text",
        "number",
        "function_text",
        "object_size",
        "read_flag",
        "write_flag",
        "communication_flag",
        "transmit_flag",
        "update_flag",
        "read_on_init_flag",
        "datapoint_types",
    )

    # all items required in the XML
    identifier: str  # "Id" - xs:ID
    name: str  # "Name"
    text: str  # "Text" - language dependent
    number: int  # "Number" - xs:unsignedInt
    function_text: str  # "FunctionText" - language dependent
    object_size: str  # "ObjectSize" - knx:ComObjectSize_t
    read_flag: bool  # "ReadFlag" - knx:Enable_t
    write_flag: bool  # "WriteFlag" - knx:Enable_t
    communication_flag: bool  # "CommunicationFlag" - knx:Enable_t
    transmit_flag: bool  # "TransmitFlag" - knx:Enable_t
    update_flag: bool  # "UpdateFlag" - knx:Enable_t
    read_on_init_flag: bool  # "ReadOnInitFlag" - knx:Enable_t
    datapoint_types: list[DPTType]  # "DataPointType" - knx:IDREFS - optional


@dataclass
class ComObjectRef:
    """Class that represents a ComObjectRef instance."""

    __slots__ = (
        "identifier",
        "ref_id",
        "name",
        "text",
        "function_text",
        "object_size",
        "read_flag",
        "write_flag",
        "communication_flag",
        "transmit_flag",
        "update_flag",
        "read_on_init_flag",
        "datapoint_types",
    )

    identifier: str  # "Id" - xs:ID - required
    ref_id: str  # "RefId" - knx:IDREF - required - points to a ComObject Id
    name: str | None  # "Name"
    text: str | None  # "Text" - language dependent
    function_text: str | None  # "FunctionText" - language dependent
    object_size: str | None  # "ObjectSize" - knx:ComObjectSize_t
    read_flag: bool | None  # "ReadFlag" - knx:Enable_t
    write_flag: bool | None  # "WriteFlag" - knx:Enable_t
    communication_flag: bool | None  # "CommunicationFlag" - knx:Enable_t
    transmit_flag: bool | None  # "TransmitFlag" - knx:Enable_t
    update_flag: bool | None  # "UpdateFlag" - knx:Enable_t
    read_on_init_flag: bool | None  # "ReadOnInitFlag" - knx:Enable_t
    datapoint_types: list[DPTType]  # "DataPointType" - knx:IDREFS


@dataclass
class XMLSpace:
    """A space in the location XML."""

    identifier: str
    name: str
    space_type: SpaceType
    usage_id: str | None  # SU-<int> resolved from knx_master.xml (with translation)
    usage_text: str  # default to "" - translated
    number: str  # default to ""
    description: str  # default to ""
    project_uid: int | None
    spaces: list[XMLSpace]
    devices: list[str]  # [DeviceInstance.individual_address]


@dataclass
class Product:
    """Model a Product instance."""

    identifier: str
    text: str
    hardware_name: str = ""


HardwareToPrograms = dict[str, str]


@dataclass
class XMLProjectInformation:
    """Model a ProjectInformation instance."""

    # ProjectInformation tag is not required in XSD, thus everything is optional
    project_id: str = ""
    name: str = ""
    last_modified: str | None = None
    group_address_style: str = ""
    guid: str = ""
    created_by: str = ""
    schema_version: str = ""
    tool_version: str = ""
