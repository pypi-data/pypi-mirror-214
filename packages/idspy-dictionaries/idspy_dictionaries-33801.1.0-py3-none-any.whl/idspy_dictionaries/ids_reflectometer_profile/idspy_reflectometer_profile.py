# __version__= "033801.1.0"
# __version_data_dictionary__= "3.38.1"
# __git_version_hash__= "dd6854b4d073482810a23839e6e51386c7f20fd3"
# 
from ..dataclasses_idsschema import _IDSPYDD_USE_SLOTS,IdsBaseClass
from dataclasses import dataclass, field
from numpy import ndarray
from typing import Optional


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
class PsiNormalization(IdsBaseClass):
    """
    Quantities used to normalize psi, as a function of time.

    :ivar psi_magnetic_axis: Value of the poloidal magnetic flux at the
        magnetic axis
    :ivar psi_boundary: Value of the poloidal magnetic flux at the
        plasma boundary
    :ivar time: Time for the R,Z,phi coordinates
    """
    class Meta:
        name = "psi_normalization"

    psi_magnetic_axis: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    psi_boundary: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    time: Optional[str] = field(
        default=None
    )


@dataclass(slots=True)
class ReflectometerProfilePosition(IdsBaseClass):
    """
    R, Z, Phi, psi, rho_tor_norm and theta positions associated to the electron
    density reconstruction (2D, dynamic within a type 1 array of structure)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    :ivar psi: Poloidal flux
    :ivar rho_tor_norm: Normalised toroidal flux coordinate
    :ivar theta: Poloidal angle (oriented clockwise when viewing the
        poloidal cross section on the right hand side of the tokamak
        axis of symmetry, with the origin placed on the plasma magnetic
        axis)
    """
    class Meta:
        name = "reflectometer_profile_position"

    r: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    z: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    phi: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    psi: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    rho_tor_norm: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    theta: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass(slots=True)
class Rzphi0DStatic(IdsBaseClass):
    """
    Structure for R, Z, Phi positions (0D, static)

    :ivar r: Major radius
    :ivar z: Height
    :ivar phi: Toroidal angle (oriented counter-clockwise when viewing
        from above)
    """
    class Meta:
        name = "rzphi0d_static"

    r: float = field(
        default=9e+40
    )
    z: float = field(
        default=9e+40
    )
    phi: float = field(
        default=9e+40
    )


@dataclass(slots=True)
class SignalFlt2D(IdsBaseClass):
    """
    Signal (FLT_2D) with its time base.

    :ivar time: Time
    """
    class Meta:
        name = "signal_flt_2d"

    time: Optional[str] = field(
        default=None
    )

    @dataclass(slots=True)
    class Data(IdsBaseClass):
        """
        :ivar class_of: Class of Data Item
        """
        class_of: str = field(
            init=False,
            default="FLT_2D"
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
class LineOfSight2Points(IdsBaseClass):
    """
    Generic description of a line of sight, defined by two points.

    :ivar first_point: Position of the first point
    :ivar second_point: Position of the second point
    """
    class Meta:
        name = "line_of_sight_2points"

    first_point: Optional[Rzphi0DStatic] = field(
        default=None
    )
    second_point: Optional[Rzphi0DStatic] = field(
        default=None
    )


@dataclass(slots=True)
class ReflectometerChannel(IdsBaseClass):
    """
    Reflectometer channel.

    :ivar name: Name of the channel
    :ivar identifier: ID of the channel
    :ivar mode: Detection mode "X" or "O"
    :ivar line_of_sight_emission: Description of the line of sight of
        the emission antenna. The first point corresponds to the antenna
        mouth. The second point correspond to the interception of the
        line of sight with the reflection surface on the inner wall.
    :ivar line_of_sight_detection: Description of the line of sight of
        the detection antenna, to be filled only if its position is
        distinct from the emission antenna. The first point corresponds
        to the antenna mouth. The second point correspond to the
        interception of the line of sight with the reflection surface on
        the inner wall.
    :ivar sweep_time: Duration of a sweep
    :ivar frequencies: Array of frequencies scanned during a sweep
    :ivar phase: Measured phase of the probing wave for each frequency
        and time slice (corresponding to the begin time of a sweep),
        relative to the phase at launch
    :ivar position: Position of the density measurements
    :ivar n_e: Electron density
    :ivar cut_off_frequency: Cut-off frequency as a function of
        measurement position and time
    """
    class Meta:
        name = "reflectometer_channel"

    name: str = field(
        default=""
    )
    identifier: str = field(
        default=""
    )
    mode: str = field(
        default=""
    )
    line_of_sight_emission: Optional[LineOfSight2Points] = field(
        default=None
    )
    line_of_sight_detection: Optional[LineOfSight2Points] = field(
        default=None
    )
    sweep_time: float = field(
        default=9e+40
    )
    frequencies: list[ndarray[(int,), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )
    phase: Optional[SignalFlt2D] = field(
        default=None
    )
    position: Optional[ReflectometerProfilePosition] = field(
        default=None
    )
    n_e: Optional[SignalFlt2D] = field(
        default=None
    )
    cut_off_frequency: list[ndarray[(int,int), float]] = field(
        default_factory=list,
        metadata={
            "max_occurs": 99,
        }
    )


@dataclass(slots=True)
class ReflectometerProfile(IdsBaseClass):
    """Profile reflectometer diagnostic.

    Multiple reflectometers are considered as independent diagnostics to
    be handled with different occurrence numbers

    :ivar ids_properties:
    :ivar type: Type of reflectometer (frequency_swept, radar, ...)
    :ivar channel: Set of channels, e.g. different reception antennas or
        frequency bandwidths of the reflectometer
    :ivar position: Position associated to the density reconstruction
        from multiple channels
    :ivar n_e: Electron density reconstructed from multiple channels
    :ivar psi_normalization: Quantities to use to normalize psi, as a
        function of time
    :ivar latency: Upper bound of the delay between physical information
        received by the detector and data available on the real-time
        (RT) network.
    :ivar code:
    :ivar time:
    """
    class Meta:
        name = "reflectometer_profile"

    ids_properties: Optional[IdsProperties] = field(
        default=None
    )
    type: str = field(
        default=""
    )
    channel: list[ReflectometerChannel] = field(
        default_factory=list,
        metadata={
            "max_occurs": 5,
        }
    )
    position: Optional[ReflectometerProfilePosition] = field(
        default=None
    )
    n_e: Optional[SignalFlt2D] = field(
        default=None
    )
    psi_normalization: Optional[PsiNormalization] = field(
        default=None
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
