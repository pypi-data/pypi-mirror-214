# __version__= "033801.1.0"
# __version_data_dictionary__= "3.38.1"
# __git_version_hash__= "dd6854b4d073482810a23839e6e51386c7f20fd3"
# 
from ..dataclasses_idsschema import _IDSPYDD_USE_SLOTS,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


@dataclass(slots=True)
class CameraIrCalibration(IdsBaseClass):
    """
    Calibration data.

    :ivar luminance_to_temperature: Luminance to temperature conversion
        table
    :ivar transmission_barrel: Transmission of the optical barrel
    :ivar transmission_mirror: Transmission of the mirror
    :ivar transmission_window: Transmission of the window
    :ivar optical_temperature: Temperature of the optical components
        (digital levels)
    """
    class Meta:
        name = "camera_ir_calibration"

    luminance_to_temperature: list[ndarray[(int, int), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    transmission_barrel: list[ndarray[(int, int), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    transmission_mirror: list[ndarray[(int, int), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    transmission_window: list[ndarray[(int, int), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    optical_temperature: list[ndarray[(int, int), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass(slots=True)
class CameraIrFrame(IdsBaseClass):
    """
    Frame of a camera.

    :ivar surface_temperature: Surface temperature image. First
        dimension : line index (horizontal axis). Second dimension:
        column index (vertical axis).
    :ivar time: Time
    """
    class Meta:
        name = "camera_ir_frame"

    surface_temperature: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class CameraIrFrameAnalysis(IdsBaseClass):
    """
    Frame analysis.

    :ivar sol_heat_decay_length: Heat flux decay length in SOL at
        divertor entrance, mapped to the mid-plane, this is the lambda_q
        parameter defined in reference T. Eich et al, Nucl. Fusion 53
        (2013) 093031
    :ivar distance_separatrix_midplane: Distance between the measurement
        position and the separatrix, mapped along flux surfaces to the
        outboard midplane, in the major radius direction. Positive value
        means the measurement is outside of the separatrix.
    :ivar power_flux_parallel: Parallel heat flux received by the
        element monitored by the camera, along the
        distance_separatrix_midplane coordinate
    :ivar time: Time
    """
    class Meta:
        name = "camera_ir_frame_analysis"

    sol_heat_decay_length: float = field(
        default=9e+40
    )
    distance_separatrix_midplane: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    power_flux_parallel: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[float] = field(
        default=None
    )


@dataclass(slots=True)
class IdentifierStatic(IdsBaseClass):
    """Standard type for identifiers (static).

    The three fields: name, index and description are all
    representations of the same information. Associated with each
    application of this identifier-type, there should be a translation
    table defining the three fields for all objects to be identified.

    :ivar name: Short string identifier
    :ivar index: Integer identifier (enumeration index within a list).
        Private identifier values must be indicated by a negative index.
    :ivar description: Verbose description
    """
    class Meta:
        name = "identifier_static"

    name: str = field(
        default=""
    )
    index: int = field(
        default=999999999
    )
    description: str = field(
        default=""
    )


@dataclass(slots=True)
class IdsProperties(IdsBaseClass):
    """Interface Data Structure properties.

    This element identifies the node above as an IDS

    :ivar comment: Any comment describing the content of this IDS
    :ivar homogeneous_time: This node must be filled (with 0, 1, or 2)
        for the IDS to be valid. If 1, the time of this IDS is
        homogeneous, i.e. the time values for this IDS are stored in the
        time node just below the root of this IDS. If 0, the time values
        are stored in the various time fields at lower levels in the
        tree. In the case only constant or static nodes are filled
        within the IDS, homogeneous_time must be set to 2
    :ivar provider: Name of the person in charge of producing this data
    :ivar creation_date: Date at which this data has been produced
    """
    class Meta:
        name = "ids_properties"

    comment: str = field(
        default=""
    )
    homogeneous_time: int = field(
        default=999999999
    )
    provider: str = field(
        default=""
    )
    creation_date: str = field(
        default=""
    )


@dataclass(slots=True)
class IdsProvenanceNode(IdsBaseClass):
    """
    Provenance information for a given node of the IDS.

    :ivar path: Path of the node within the IDS, following the syntax
        given in the link below. If empty, means the provenance
        information applies to the whole IDS.
    :ivar sources: List of sources used to import or calculate this
        node, identified as explained below. In case the node is the
        result of of a calculation / data processing, the source is an
        input to the process described in the "code" structure at the
        root of the IDS. The source can be an IDS (identified by a URI
        or a persitent identifier, see syntax in the link below) or non-
        IDS data imported directly from an non-IMAS database (identified
        by the command used to import the source, or the persistent
        identifier of the data source). Often data are obtained by a
        chain of processes, however only the last process input are
        recorded here. The full chain of provenance has then to be
        reconstructed recursively from the provenance information
        contained in the data sources.
    """
    class Meta:
        name = "ids_provenance_node"

    path: str = field(
        default=""
    )
    sources: Optional[list[str]] = field(
        default=None
    )


@dataclass(slots=True)
class Library(IdsBaseClass):
    """
    Library used by the code that has produced this IDS.

    :ivar name: Name of software
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    """
    class Meta:
        name = "library"

    name: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )


@dataclass(slots=True)
class Code(IdsBaseClass):
    """
    Generic decription of the code-specific parameters for the code that has
    produced this IDS.

    :ivar name: Name of software generating IDS
    :ivar commit: Unique commit reference of software
    :ivar version: Unique version (tag) of software
    :ivar repository: URL of software repository
    :ivar parameters: List of the code specific parameters in XML format
    :ivar output_flag: Output flag : 0 means the run is successful,
        other values mean some difficulty has been encountered, the
        exact meaning is then code specific. Negative values mean the
        result shall not be used.
    :ivar library: List of external libraries used by the code that has
        produced this IDS
    """
    class Meta:
        name = "code"

    name: str = field(
        default=""
    )
    commit: str = field(
        default=""
    )
    version: str = field(
        default=""
    )
    repository: str = field(
        default=""
    )
    parameters: str = field(
        default=""
    )
    output_flag: list[ndarray[(int,), int]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    library: list[Library] = field(
        default_factory=list,
        metadata={
            "max_occurs": 10,
        }
    )


@dataclass(slots=True)
class IdsProvenance(IdsBaseClass):
    """
    Provenance information about the IDS.

    :ivar node: Set of IDS nodes for which the provenance is given. The
        provenance information applies to the whole structure below the
        IDS node. For documenting provenance information for the whole
        IDS, set the size of this array of structure to 1 and leave the
        child "path" node empty
    """
    class Meta:
        name = "ids_provenance"

    node: list[IdsProvenanceNode] = field(
        default_factory=list,
        metadata={
            "max_occurs": 20,
        }
    )


@dataclass(slots=True)
class CameraIr(IdsBaseClass):
    """
    Infrared camera for monitoring of Plasma Facing Components.

    :ivar ids_properties:
    :ivar name: Name of the camera
    :ivar calibration: Calibration data
    :ivar frame: Set of frames
    :ivar midplane: Choice of midplane definition for the mapping of
        measurements on an equilibrium
    :ivar frame_analysis: Quantities deduced from frame analysis for a
        set of time slices
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "camera_ir"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    name: str = field(
        default=""
    )
    calibration: Optional[CameraIrCalibration] = field(
        default=None
    )
    frame: list[CameraIrFrame] = field(
        default_factory=list
    )
    midplane: Optional[IdentifierStatic] = field(
        default=None
    )
    frame_analysis: list[CameraIrFrameAnalysis] = field(
        default_factory=list
    )
    latency: float = field(
        default=9e+40
    )
    code: Optional[Code] = field(
        default=None
    )
    time: Optional[str] = field(
        default=None
    )
