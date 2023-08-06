from pydantic import BaseModel
import pydantic
from typing import (List, Dict, Union, Literal)

from steam_sdk.data.DataConductor import Conductor


############################
# Source files
class SourceFiles(BaseModel):
    """
        Level 1: Class for the source files
    """
    coil_fromROXIE: str = None    # ROXIE .data file
    conductor_fromROXIE: str = None  # ROXIE .cadata file
    iron_fromROXIE: str = None    # ROXIE .iron file
    BH_fromROXIE: str = None      # ROXIE .bhdata file (BH-curves)
    magnetic_field_fromROXIE: str = None # ROXIE .map2d file
    sm_inductance: str = None


############################
# General parameters
class Model(BaseModel):
    """
        Level 2: Class for information on the model
    """
    name: str = None  # magnetIdentifier (ProteCCT)
    version: str = None
    case: str = None
    state: str = None


class General(BaseModel):
    """
        Level 1: Class for general information on the case study
    """
    magnet_name: str = None
    circuit_name: str = None
    model: Model = Model()
    magnet_type: str = None
    T_initial: float = None               # T00 (LEDET), Top (SIGMA)
    magnetic_length: float = None   # l_magnet (LEDET), magLength (SIGMA), magneticLength (ProteCCT)


############################
# Coil Windings
class ElectricalOrder(BaseModel):
    """
        Level 2: Class for the order of the electrical pairs
    """
    group_together: List[List[int]] = []   # elPairs_GroupTogether
    reversed: List[int] = []         # elPairs_RevElOrder
    overwrite_electrical_order: List[int] = []


class Multipole(BaseModel):
    """
        Level 2: Class for multi-pole coil data
    """
    tbc: str = None

class SolenoidCoil(BaseModel):
    """
        Level 3: Class for Solenoid windings
    """
    name: str = None            # -             solenoid name
    a1: float = None            # m             smaller radial dimension of solenoid
    a2: float = None            # m             larger radial dimension of solenoid
    b1: float = None            # m             smaller axial dimension of solenoid
    b2: float = None            # m             larger axial dimension of solenoid
    conductor_name: str = None  # -             wire name - name must correspond to existing conductor name in the same yaml file
    ntpl: int = None            # -             number of turns per layer
    nl: int = None              # -             number of layers
    pre_preg: float = None     # m              Pre-preg thicknes (radial) i.e. in LEDET in width direction
    section: int = None         # Section in ledet for the block

class Solenoid(BaseModel):
    """
        Level 2: Class for Solenoid windings
    """
    coils: List[SolenoidCoil] = [SolenoidCoil()]

class Pancake(BaseModel):
    """
        Level 2: Class for Pancake windings
    """
    tbc: str = None

class CCT_straight(BaseModel):
    """
        Level 2: Class for straight CCT windings
    """
    winding_order: List[int] = None
    winding_numberTurnsFormers: List[int] = None            # total number of channel turns, ProteCCT: numTurnsPerStrandTotal, FiQuS: n_turnss
    winding_numRowStrands: List[int] = None                 # number of rows of strands in channel, ProteCCT: numRowStrands, FiQuS: windings_wwns
    winding_numColumnStrands: List[int] = None              # number of columns of strands in channel, ProteCCT: numColumnStrands, FiQuS: windings_whns
    winding_chws: List[float] = None                          # width of winding slots, ProteCTT: used to calc. wStrandSlot=winding_chws/numRowStrands, FiQuS: wwws
    winding_chhs: List[float] = None                          # width of winding slots, ProteCTT: used to calc. wStrandSlot=winding_chhs/numColumnStrands, FiQuS: wwhs
    former_inner_radiuses: List[float] = []                  # innerRadiusFormers (ProteCCT)
    former_outer_radiuses: List[float] = []                  # innerRadiusFormers (ProteCCT)
    former_RRRs: List[float] = []                   # RRRFormer (ProteCCT)
    #former_thickness_underneath_coil: float = None          # formerThicknessUnderneathCoil. Thickness of the former underneath the slot holding the strands in [m] (ProteCCT)
    cylinder_inner_radiuses: List[float] = []              # innerRadiusOuterCylinder (ProteCCT)
    cylinder_outer_radiuses: List[float] = []                  # ProteCCT: thicknessOuterCylinder = cylinder_outer_radiuses - cylinder_inner_radiuses
    cylinder_RRRs: List[float] = []                         # ProteCCT: RRROuterCylinder


class CCT_curved(BaseModel):
    """
        Level 2: Class for curved CCT windings
    """
    tbc: str = None


class CoilWindings(BaseModel):
    """
        Level 1: Class for winding information
    """
    conductor_to_group: List[int] = []  # This key assigns to each group a conductor of one of the types defined with Conductor.name
    group_to_coil_section: List[int] = []  # This key assigns groups of half-turns to coil sections
    polarities_in_group: List[int] = []  # This key assigns the polarity of the current in each group # TODO: Consider if it is convenient to remove this (and check DictionaryLEDET when you do)
    n_half_turn_in_group: List[int] = []
    half_turn_length: List[float] = []
    electrical_pairs: ElectricalOrder = ElectricalOrder()  # Variables used to calculate half-turn electrical order
    multipole: Multipole = Multipole()
    pancake: Pancake = Pancake()
    solenoid: Solenoid = Solenoid()
    CCT_straight: CCT_straight = CCT_straight()
    CCT_curved: CCT_curved = CCT_curved()


############################
# Conductor keys are defined in data\DataConductor()

############################
# Circuit
class Circuit(BaseModel):
    """
        Level 1: Class for the circuit parameters
    """
    R_circuit: float = None             # R_circuit
    L_circuit: float = None             # Lcir (SIGMA)
    R_parallel: float = None


############################
# Power Supply (aka Power Converter)
class PowerSupply(BaseModel):
    """
        Level 1: Class for the power supply (aka power converter)
    """
    I_initial: float = None          # I00 (LEDET), I_0 (SIGMA), I0 (BBQ)
    t_off: float = None            # t_PC
    t_control_LUT: List[float] = []    # t_PC_LUT
    I_control_LUT: List[float] = []    # I_PC_LUT
    R_crowbar: float = None     # Rcrow (SIGMA), RCrowbar (ProteCCT)
    Ud_crowbar: float = None


############################
# Quench Protection
class EnergyExtraction(BaseModel):
    """
        Level 2: Class for the energy extraction parameters
    """
    t_trigger: float = None                 # tEE (LEDET), tSwitchDelay (ProteCCT)
    R_EE: float = None       # R_EE_triggered (LEDET)
    power_R_EE: float = None # RDumpPower (ProteCCT), variable used to simulate varistors used in an EE system
    L: float = None
    C: float = None


class QuenchHeater(BaseModel):
    """
        Level 2: Class for the quench heater parameters
    """
    N_strips: int = None                              # nHeaterStrips
    t_trigger: List[float] = []                        # tQH
    U0: List[float] = []
    C: List[float] = []
    R_warm: List[float] = []
    w: List[float] = []                             # In Sigma this
    h: List[float] = []
    s_ins: Union[List[float], List[List[float]]] = []
    type_ins: Union[List[str], List[List[str]]] = []
    s_ins_He: Union[List[float], List[List[float]]] = []
    type_ins_He: Union[List[str], List[List[str]]] = []
    l: List[float] = []
    l_copper: List[float] = []
    l_stainless_steel: List[float] = []
    f_cover: List[float] = []
    iQH_toHalfTurn_From: List[int] = []
    iQH_toHalfTurn_To: List[int] = []
    turns_sides: List[str] = []


class CLIQ(BaseModel):
    """
        Level 2: Class for the CLIQ parameters
    """
    t_trigger: float = None                        # tCLIQ
    current_direction: List[int] = []    # directionCurrentCLIQ
    sym_factor: float = None               # symFactor
    N_units: int = None                          # nCLIQ
    U0: float = None                       # V_cliq_0 (SIGMA)
    C: float = None                        # C_cliq (SIGMA)
    R: float = None                        # Rcapa (LEDET), R_cliq (SIGMA)
    L: float = None                        # L_cliq
    I0: float = None                       # I_cliq_0


class FQPCs(BaseModel):  # Geometry related fqpls _inputs
    """
        Level 2: Class for the FQPLs parameters for protection
    """
    enabled: List[bool] = None  # list specifying which fqpl is enabled
    names: List[str] = None  # name to use in gmsh and getdp
    fndpls: List[int] = None  # fqpl number of divisions per length
    fwws: List[float] = None  # fqpl wire widths (assuming rectangular) for theta = 0 this is x dimension
    fwhs: List[float] = None  # fqpl wire heights (assuming rectangular) for theta = 0 this is y dimension
    r_ins: List[float] = None  # radiuses for inner diameter for fqpl (radial (or x direction for theta=0) for placing the fqpl
    r_bs: List[float] = None  # radiuses for bending the fqpl by 180 degrees
    n_sbs: List[int] = None  # number of 'bending segmetns' for the 180 degrees turn
    thetas: List[float] = None  # rotation in deg from x+ axis towards y+ axis about z axis.
    z_starts: List[str] = None  # which air boundary to start at. These is string with either: z_min or z_max key from the Air region.
    z_ends: List[float] = None  # z coordinate of loop end
    currents: List[float] = None  # current in the wire
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability
    th_conns_def: List[List] = None


class QuenchProtection(BaseModel):
    """
        Level 1: Class for quench protection
    """
    Energy_Extraction: EnergyExtraction = EnergyExtraction()
    Quench_Heaters: QuenchHeater = QuenchHeater()
    CLIQ: CLIQ = CLIQ()
    FQPCs: FQPCs = FQPCs()


############################
# BBQ options
class GeometryBBQ(BaseModel):
    """
        Level 2: Class for geometry options in BBQ
    """
    thInsul: float = None
    lenBusbar: float = None


class SimulationBBQ(BaseModel):
    """
        Level 2: Class for simulation options in BBQ
    """
    meshSize: float = None


class PhysicsBBQ(BaseModel):
    """
        Level 2: Class for physics options in BBQ
    """
    adiabaticZoneLength: float = None
    aFilmBoilingHeliumII: float = None
    aKap: float = None
    BBackground: float = None
    BPerI: float = None
    IDesign: float = None
    jointLength: float = None
    jointResistancePerMeter: float = None
    muTInit: float = None
    nKap: float = None
    QKapLimit: float = None
    Rjoint: float = None
    symmetryFactor: float = None
    tauDecay: float = None
    TInitMax: float = None
    TInitOp: float = None
    TLimit: float = None
    tValidation: float = None
    TVQRef: float = None
    VThreshold: float = None
    withCoolingToBath: float = None


class QuenchInitializationBBQ(BaseModel):
    """
        Level 2: Class for quench initialization parameters in BBQ
    """
    sigmaTInit: float = None


############################
# FiQuS options

# Pancake3D

class Winding_g(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    r_i: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="innerRadius"
    )  # inner radius
    t: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="thickness"
    )  # thickness
    N: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="numberOfTurns"
    )  # number of turns
    h: pydantic.PositiveFloat = pydantic.Field(default=None, alias="height")  # height

    # Optionals:
    name: str = pydantic.Field(default="winding")  # name to be used in mesh
    NofVolPerTurn: pydantic.PositiveInt = pydantic.Field(
        default=2, alias="numberOfVolumesPerTurn"
    )
    theta_i: float = pydantic.Field(
        default=0.0, alias="startAngle"
    )  # start angle in radians

    # 2) To be calculated:
    r_o: pydantic.PositiveFloat = None  # outer radius
    turnTol: pydantic.PositiveFloat = None  # turn tolerance
    spt: pydantic.PositiveFloat = None  # section per turn

class Insulation_g(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    tsa: bool = pydantic.Field(
        default=None, alias="thinShellApproximation"
    )  # thin shell approximation (TSA) or full 3D model
    t: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="thickness"
    )  # thickness

    # Optionals:
    name: str = pydantic.Field(default="insulation")  # name to be used in mesh

class Terminal_g(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    name: str = pydantic.Field(
        default=None, alias="name"
    )  # names to be used in gmsh and getdp
    t: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="thickness"
    )  # thickness

    # 2) To be calculated:
    r: pydantic.PositiveFloat = None  # inner radius of the inner terminal

class Terminals_g(pydantic.BaseModel):
    # 1) User inputs:
    i: Terminal_g = pydantic.Field(Terminal_g(), alias="inner")
    o: Terminal_g = pydantic.Field(Terminal_g(), alias="outer")
    # Mandatory:

    # Optionals:
    firstName: str = pydantic.Field(
        default="firstTerminal"
    )  # name of the first terminal
    lastName: str = pydantic.Field(default="lastTerminal")  # name of the last terminal

class Air_g(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    r: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="radius"
    )  # radius (for cylinder)
    a: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="sideLength"
    )  # side length (for cuboid)
    margin: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="axialMargin"
    )  # axial margin

    # Optionals:
    name: str = pydantic.Field(default="air")  # name to be used in mesh
    type: Literal["cylinder", "cuboid"] = pydantic.Field(
        default="cylinder"
    )  # either cylinder or cuboid
    shellTransformation: bool = pydantic.Field(
        default=False, alias="shellTransformation"
    )
    shellTransformationMultiplier: pydantic.PositiveFloat = pydantic.Field(
        default=1.2, alias="shellTransformationMultiplier",
        description="multiplier for the shell transformation"
    )
    cutName: str = pydantic.Field(default="AirCut")  # name of the cut (cochain)
    shellVolumeName: str = pydantic.Field(
        default="airShellVolume"
    )  # name of the shell volume

    # 2) To be calculated:
    h: pydantic.PositiveFloat = None  # total height

class Winding_m(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    axne: List[pydantic.PositiveInt] = pydantic.Field(
        default=None, alias="axialNumberOfElements", description="axial number of elements"
    )  # axial number of elements

    ane: List[pydantic.PositiveInt] = pydantic.Field(
        default=None, alias="azimuthalNumberOfElementsPerTurn", description="azimuthal number of elements per turn"
    )  # azimuthal number of elements

    rne: List[pydantic.PositiveInt] = pydantic.Field(
        default=None, alias="radialNumberOfElementsPerTurn", description="radial number of elements per turn"
    )  # radial number of elements

    # Optionals:
    axbc: List[pydantic.PositiveFloat] = pydantic.Field(
        default=[1], alias="axialBumpCoefficients"
    )  # axial bump coefficient (axial elemnt distribution)

    recombine: List[bool] = pydantic.Field(
        default=[False], alias="recombineIntoHexahedra"
    )  # recombine tetrahedron elements into hexahedron elements

class Insulation_m(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:

    rne: List[pydantic.PositiveInt] = pydantic.Field(
        default=None, alias="radialNumberOfElementsPerTurn"
    )  # radial number of elements

class Air_m(pydantic.BaseModel):
    # 1) User inputs:

    # Optionals:
    structured: bool = pydantic.Field(
        default=False, alias="structureTopAndBottomParts"
    )  # Structure the top and bottom parts of the air mesh

class Air_s(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    permeability: pydantic.PositiveFloat = None  # permeability [H/m]

class Conductor_s(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    resistivity: pydantic.PositiveFloat = None  # resistivity [Ohm*m]

class Time_s(pydantic.BaseModel):
    # 1) User inputs:

    # Mandatory:
    start: float = None  # start time [s]
    end: float = None  # end time [s]
    step: float = None  # time step [s]
    rampEnd: float = None  # ramp end time [s]
    plateauEnd: float = None  # plateau end time [s]
    rampDownEnd: float = None  # ramp down end time [s]

    # Optionals:
    timesToBeSaved: List[float] = None

class GeometryPancake3DFiQuS(pydantic.BaseModel):
    # 1) User inputs:

    wi: Winding_g = pydantic.Field(Winding_g(), alias="winding")  # winding information

    ii: Insulation_g = pydantic.Field(
        Insulation_g(), alias="insulation"
    )  # insulation information

    ti: Terminals_g = pydantic.Field(
        Terminals_g(), alias="terminals"
    )  # terminals information

    ai: Air_g = pydantic.Field(Air_g(), alias="air")  # air information

    # Mandatory:

    N: pydantic.PositiveInt = pydantic.Field(
        default=None, alias="numberOfPancakes"
    )  # the number of pancake coils stacked on top of each other

    gap: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="gapBetweenPancakes"
    )  # the gap between the pancake coils

    # Optionals:
    dimTol: pydantic.PositiveFloat = pydantic.Field(
        default=1e-8, alias="dimensionTolerance"
    )  # dimension tolerance (every dimension is a multiple of this)
    pancakeBoundaryName: str = pydantic.Field(
        default="PancakeBoundary"
    )  # name of the pancake's surface that touches the air
    insulationBoundaryName: str = pydantic.Field(
        default="InsulationBoundary"
    )  # name of the insulation's curves that touches the air (only for TSA)

class MeshPancake3DFiQuS(pydantic.BaseModel):
    # 1) User inputs:

    # winding information:
    wi: Winding_m = pydantic.Field(Winding_m(), alias="winding")
    # insulation information:
    ii: Insulation_m = pydantic.Field(Insulation_m(), alias="insulation")
    # air information:
    ai: Air_m = pydantic.Field(Air_m(), alias="air")

    # Mandatory:

    # The values below are in terms of the winding thickness. Mesh element sizes grow
    # from the geometry's center to the air's outer part.
    sizeMin: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="minimumMaximumElementSize"
    )
    sizeMax: pydantic.PositiveFloat = pydantic.Field(
        default=None, alias="maximumMaximumElementSize"
    )

class SolvePancake3DFiQuS(pydantic.BaseModel):
    proTemplate: str = None  # file name of .pro template file
    t: Time_s = pydantic.Field(Time_s(), alias="time")
    wi: Conductor_s = pydantic.Field(Conductor_s(), alias="winding")
    ii: Conductor_s = pydantic.Field(Conductor_s(), alias="insulation")
    ti: Conductor_s = pydantic.Field(Conductor_s(), alias="terminals")
    ai: Air_s = pydantic.Field(Air_s(), alias="air")

class FiQuSPancake3D(pydantic.BaseModel):
    """
    Level 1: Class for FiQuS Pancake3D
    """

    geometry: GeometryPancake3DFiQuS = GeometryPancake3DFiQuS()
    mesh: MeshPancake3DFiQuS = MeshPancake3DFiQuS()
    solve: SolvePancake3DFiQuS = SolvePancake3DFiQuS()

# Multipole
class ConvectionBoundaryCondition(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    boundaries: List[str] = []
    heat_transfer_coefficient: float = None
    coolant_temperature: float = None


class OneParBoundaryCondition(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    boundaries: List[str] = []
    value: float = None


class TimeParameters(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    initial_time: float = None
    final_time: float = None
    time_step: float = None


class QuenchInitiation(BaseModel):
    """
        Level 5: Class for FiQuS Multipole
    """
    turns: List[int] = []
    temperatures: List[float] = []


class BoundaryConditionsElectromagnetics(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    currents: List[float] = []


class BoundaryConditionsThermal(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    temperature: Dict[str, OneParBoundaryCondition] = {}
    heat_flux: Dict[str, OneParBoundaryCondition] = {}
    cooling: Dict[str, ConvectionBoundaryCondition] = {}


class TransientElectromagnetics(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    time_pars: TimeParameters = TimeParameters()
    initial_current: float = None


class TransientThermal(BaseModel):
    """
        Level 4: Class for FiQuS Multipole
    """
    time_pars: TimeParameters = TimeParameters()
    initial_temperature: float = None
    quench_initiation: QuenchInitiation = QuenchInitiation()


class Electromagnetics(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    solved: str = None
    boundary_conditions: BoundaryConditionsElectromagnetics = BoundaryConditionsElectromagnetics()
    transient: TransientElectromagnetics = TransientElectromagnetics()


class Thermal(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    solved: str = None
    boundary_conditions: BoundaryConditionsThermal = BoundaryConditionsThermal()
    transient: TransientThermal = TransientThermal()


class Threshold(BaseModel):
    """
        Level 3: Class for FiQuS Multipole
    """
    SizeMin: float = None
    SizeMax: float = None
    DistMin: float = None
    DistMax: float = None


class MultipoleGeometry(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    simplified_coil: bool = None
    with_iron_yoke: bool = None
    with_wedges: bool = None
    symmetry: str = None


class MultipoleMesh(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    default_mesh: bool = None
    mesh_iron: Threshold = Threshold()
    mesh_coil: Threshold = Threshold()
    Algorithm: int = None  # sets gmsh Mesh.Algorithm
    ElementOrder: int = None  # sets gmsh Mesh.ElementOrder
    Optimize: int = None  # sets gmsh Mesh.Optimize


class MultipoleSolve(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    electromagnetics: Electromagnetics = Electromagnetics()
    thermal: Thermal = Thermal()
    thin_shells: bool = None
    pro_template: str = None  # file name of .pro template file


class MultipolePostProc(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    compare_to_ROXIE: str = None
    plot_all: str = None
    variables: List[str] = None  # Name of variables to post-process, like "b" for magnetic flux density
    volumes: List[str] = None  # Name of domains to post-process, like "powered"
    file_exts: List[str] = None  # Name of file extensions to output to, like "pos"
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like "LEDET3D"


class FiQuSMultipole(BaseModel):
    """
        Level 2: Class for FiQuS Multipole
    """
    geometry: MultipoleGeometry = MultipoleGeometry()
    mesh: MultipoleMesh = MultipoleMesh()
    solve: MultipoleSolve = MultipoleSolve()
    postproc: MultipolePostProc = MultipolePostProc()


# CCT

class Winding_g(BaseModel):  # Geometry related windings _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    names: List[str] = None  # name to use in gmsh and getdp
    r_wms: List[float] = None  # radius of the middle of the winding
    #n_turnss: List[float] = None  # number of turns
    ndpts: List[int] = None  # number of divisions of turn, i.e. number of hexagonal elements for each turn
    ndpt_ins: List[int] = None  # number of divisions of terminals in
    ndpt_outs: List[int] = None  # number of divisions of terminals in
    lps: List[float] = None  # layer pitch
    alphas: List[float] = None  # tilt angle
    wwws: List[float] = None  # winding wire widths (assuming rectangular)
    wwhs: List[float] = None  # winding wire heights (assuming rectangular)


class Winding_s(BaseModel):  # Solution time used windings _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    currents: List[float] = None  # current in the wire
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability


class Former_g(BaseModel):  # Geometry related formers _inputs
    """
        Level 2: Class for FiQuS CCT Options
    """
    names: List[str] = None  # name to use in gmsh and getdp
    z_mins: List[float] = None  # extend of former  in negative z direction
    z_maxs: List[float] = None  # extend of former in positive z direction


class Former_s(BaseModel):  # Solution time used formers _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigmas: List[float] = None  # electrical conductivity
    mu_rs: List[float] = None  # relative permeability


class Air_g(BaseModel):  # Geometry related air_region _inputs
    """
        Level 2: Class for FiQuS CCT
    """
    name: str = None  # name to use in gmsh and getdp
    sh_type: str = None  # cylinder or cuboid are possible
    ar: float = None  # if box type is cuboid a is taken as a dimension, if cylinder then r is taken
    z_min: float = None  # extend of air region in negative z direction
    z_max: float = None  # extend of air region in positive z direction


class Air_s(BaseModel):  # Solution time used air _inputs (materials and BC)
    """
        Level 2: Class for FiQuS CCT
    """
    sigma: float = None  # electrical conductivity
    mu_r: float = None  # relative permeability


class GeometryCCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    windings: Winding_g = Winding_g()
    formers: Former_g = Former_g()
    air: Air_g = Air_g()


class MeshCCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    MaxAspectWindings: float = None  # used in transfinite mesh_generators settings to define mesh_generators size along two longer lines of hex elements of windings
    ThresholdSizeMin: float = None  # sets field control of Threshold SizeMin
    ThresholdSizeMax: float = None  # sets field control of Threshold SizeMax
    ThresholdDistMin: float = None  # sets field control of Threshold DistMin
    ThresholdDistMax: float = None  # sets field control of Threshold DistMax


class SolveCCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    windings: Winding_s = Winding_s()  # windings solution time _inputs
    formers: Former_s = Former_s()  # former solution time _inputs
    air: Air_s = Air_s()  # air solution time _inputs
    pro_template: str = None  # file name of .pro template file
    variables: List[str] = None  # Name of variable to post-process by GetDP, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by GetDP, line Winding_1
    file_exts: List[str] = None  # Name of file extensions to post-process by GetDP, like .pos


class PostprocCCT(BaseModel):
    """
        Level 2: Class for Options FiQuS CCT
    """

    # windings_wwns: List[int] = None  # wires in width direction numbers
    # windings_whns: List[int] = None  # wires in height direction numbers
    additional_outputs: List[str] = None  # Name of software specific input files to prepare, like :LEDET3D
    fqpl_export_trim_tol: List[float] = None  # this multiplier times winding extend gives 'z' coordinate above(below) which hexes are exported for LEDET, length of this list must match number of fqpls
    variables: List[str] = None  # Name of variable to post-process by python Gmsh API, like B for magnetic flux density
    volumes: List[str] = None  # Name of volume to post-process by python Gmsh API, line Winding_1
    file_exts: List[str] = None  # Name of file extensions o post-process by python Gmsh API, like .pos


class FiQuSCCT(BaseModel):
    """
        Level 2: Class for FiQuS CCT
    """
    geometry: GeometryCCT = GeometryCCT()
    mesh: MeshCCT = MeshCCT()
    solve: SolveCCT = SolveCCT()
    postproc: PostprocCCT = PostprocCCT()


class RunFiQuS(BaseModel):
    """
        Class for FiQuS run
    """
    type: str = None
    geometry: str = None
    mesh: str = None
    solution: str = None
    launch_gui: bool = None
    overwrite: bool = None


class FiQuS(BaseModel):
    """
        Level 1: Class for FiQuS options
    """
    run: RunFiQuS = RunFiQuS()
    cct: FiQuSCCT = FiQuSCCT()
    multipole: FiQuSMultipole = FiQuSMultipole()
    Pancake3D: FiQuSPancake3D = FiQuSPancake3D()


############################
# LEDET options
class TimeVectorLEDET(BaseModel):
    """
        Level 2: Class for simulation time vector in LEDET
    """
    time_vector_params: List[float] = []


class MagnetInductance(BaseModel):
    """
        Level 2: Class for magnet inductance assignment
    """
    flag_calculate_inductance: bool = None
    overwrite_inductance_coil_sections: List[List[float]] = [[]]
    overwrite_HalfTurnToInductanceBlock: List[int] = []
    LUT_DifferentialInductance_current: List[float] = []
    LUT_DifferentialInductance_inductance: List[float] = []


class HeatExchange(BaseModel):
    """
        Level 2: Class for heat exchange information
    """
    heat_exchange_max_distance: float = None  # heat exchange max_distance
    iContactAlongWidth_pairs_to_add: List[List[int]] = [[]]
    iContactAlongWidth_pairs_to_remove: List[List[int]] = [[]]
    iContactAlongHeight_pairs_to_add: List[List[int]] = [[]]
    iContactAlongHeight_pairs_to_remove: List[List[int]] = [[]]
    th_insulationBetweenLayers: float = None


class ConductorGeometry(BaseModel):
    """
        Level 2: Class for multipole geometry parameters - ONLY USED FOR ISCC/ISCL CALCULATION
    """
    alphaDEG_ht: List[float] = []  # Inclination angle of each half-turn, alphaDEG (LEDET)
    rotation_ht: List[float] = []  # Rotation of each half-turn, rotation_block (LEDET)
    mirror_ht: List[int]   = []  # Mirror around quadrant bisector line for half-turn, mirror_block (LEDET)
    mirrorY_ht: List[int]  = []  # Mirror around Y axis for half-turn, mirrorY_block (LEDET)


class FieldMapFilesLEDET(BaseModel):
    """
        Level 2: Class for field map file parameters in LEDET
    """
    Iref: float = None
    flagIron: int = None
    flagSelfField: int = None
    headerLines: int = None
    columnsXY: List[int] = []
    columnsBxBy: List[int] = []
    flagPlotMTF: int = None
    fieldMapNumber: int = None
    flag_modify_map2d_ribbon_cable: int = None
    flag_calculateMagneticField: int = None


class InputGenerationOptionsLEDET(BaseModel):
    """
        Level 2: Class for input generation options in LEDET
    """
    # flag_typeWindings: int = None
    flag_calculateInductanceMatrix: int = None
    flag_useExternalInitialization: int = None
    flag_initializeVar: int = None
    selfMutualInductanceFileNumber: int = None


class SimulationLEDET(BaseModel):
    """
        Level 2: Class for simulation options in LEDET
    """
    flag_fastMode: int = None
    flag_controlCurrent: int = None
    flag_automaticRefinedTimeStepping: int = None


class PhysicsLEDET(BaseModel):
    """
        Level 2: Class for physics options in LEDET
    """
    flag_IronSaturation: int = None
    flag_InvertCurrentsAndFields: int = None
    flag_ScaleDownSuperposedMagneticField: int = None
    flag_HeCooling: int = None
    fScaling_Pex: float = None
    fScaling_Pex_AlongHeight: float = None
    fScaling_MR: float = None
    flag_scaleCoilResistance_StrandTwistPitch: int = None
    flag_separateInsulationHeatCapacity: int = None
    flag_persistentCurrents: int = None
    flag_ISCL: int = None
    fScaling_Mif: float = None
    fScaling_Mis: float = None
    flag_StopIFCCsAfterQuench: int = None
    flag_StopISCCsAfterQuench: int = None
    tau_increaseRif: float = None
    tau_increaseRis: float = None
    fScaling_RhoSS: float = None
    maxVoltagePC: float = None
    minCurrentDiode: float = None
    flag_symmetricGroundingEE: int = None
    flag_removeUc: int = None
    BtX_background: float = None
    BtY_background: float = None


class QuenchInitializationLEDET(BaseModel):
    """
        Level 2: Class for quench initialization parameters in LEDET
    """
    iStartQuench: List[int] = []
    tStartQuench: List[float] = []
    lengthHotSpot_iStartQuench: List[float] = []
    fScaling_vQ_iStartQuench: List[float] = []


class PostProcessingLEDET(BaseModel):
    """
        Level 2: Class for post processing options in LEDET
    """
    flag_showFigures: int = None
    flag_saveFigures: int = None
    flag_saveMatFile: int = None
    flag_saveTxtFiles: int = None
    flag_generateReport: int = None
    flag_saveResultsToMesh: int = None
    tQuench: List[float] = []
    initialQuenchTemp: List[float] = []
    flag_hotSpotTemperatureInEachGroup: int = None
    flag_importFieldWhenCalculatingHotSpotT: int = None


class Simulation3DLEDET(BaseModel):
    """
        Level 2: Class for 3D simulation parameters and options in lEDET
    """
    # Variables in the "Options" sheet
    flag_3D: int = None
    flag_adaptiveTimeStepping: int = None
    sim3D_flag_Import3DGeometry: int = None
    sim3D_import3DGeometry_modelNumber: int = None

    # Variables in the "Inputs" sheet
    sim3D_uThreshold: float = None
    sim3D_f_cooling_down: Union[float, List[float]] = None
    sim3D_f_cooling_up: Union[float, List[float]] = None
    sim3D_f_cooling_left: Union[float, List[float]] = None
    sim3D_f_cooling_right: Union[float, List[float]] = None
    sim3D_f_cooling_LeadEnds: List[int] = []
    sim3D_fExToIns: float = None
    sim3D_fExUD: float = None
    sim3D_fExLR: float = None
    sim3D_min_ds_coarse: float = None
    sim3D_min_ds_fine: float = None
    sim3D_min_nodesPerStraightPart: int = None
    sim3D_min_nodesPerEndsPart: int = None
    sim3D_idxFinerMeshHalfTurn: List[int] = []
    sim3D_flag_checkNodeProximity: int = None
    sim3D_nodeProximityThreshold: float = None
    sim3D_Tpulse_sPosition: float = None
    sim3D_Tpulse_peakT: float = None
    sim3D_Tpulse_width: float = None
    sim3D_tShortCircuit: float = None
    sim3D_coilSectionsShortCircuit: List[int] = []
    sim3D_R_shortCircuit: float = None
    sim3D_shortCircuitPosition: Union[float, List[List[float]]] = None
    sim3D_durationGIF: float = None
    sim3D_flag_saveFigures: int = None
    sim3D_flag_saveGIF: int = None
    sim3D_flag_VisualizeGeometry3D: int = None
    sim3D_flag_SaveGeometry3D: int = None


class PlotsLEDET(BaseModel):
    """
        Level 2: Class for plotting parameters in lEDET
    """
    suffixPlot: List[str] = []
    typePlot: List[int] = []
    outputPlotSubfolderPlot: List[str] = []
    variableToPlotPlot: List[str] = []
    selectedStrandsPlot: List[str] = []
    selectedTimesPlot: List[str] = []
    labelColorBarPlot: List[str] = []
    minColorBarPlot: List[str] = []
    maxColorBarPlot: List[str] = []
    MinMaxXYPlot: List[int] = []
    flagSavePlot: List[int] = []
    flagColorPlot: List[int] = []
    flagInvisiblePlot: List[int] = []


class VariablesToSaveLEDET(BaseModel):
    """
        Level 2: Class for variables to save in lEDET
    """
    variableToSaveTxt: List[str] = []
    typeVariableToSaveTxt: List[int] = []
    variableToInitialize: List[str] = []
    writeToMesh_fileNameMeshPositions: List[str] = []
    writeToMesh_suffixFileNameOutput: List[str] = []
    writeToMesh_selectedVariables: List[str] = []
    writeToMesh_selectedTimeSteps: List[str] = []
    writeToMesh_selectedMethod: List[str] = []


class LEDET(BaseModel):
    """
        Level 1: Class for LEDET options
    """
    time_vector: TimeVectorLEDET = TimeVectorLEDET()
    magnet_inductance: MagnetInductance = MagnetInductance()
    heat_exchange: HeatExchange = HeatExchange()
    conductor_geometry_used_for_ISCL: ConductorGeometry = ConductorGeometry()
    field_map_files: FieldMapFilesLEDET = FieldMapFilesLEDET()
    input_generation_options: InputGenerationOptionsLEDET = InputGenerationOptionsLEDET()
    simulation: SimulationLEDET = SimulationLEDET()
    physics: PhysicsLEDET = PhysicsLEDET()
    quench_initiation: QuenchInitializationLEDET = QuenchInitializationLEDET()
    post_processing: PostProcessingLEDET = PostProcessingLEDET()
    simulation_3D: Simulation3DLEDET = Simulation3DLEDET()
    plots: PlotsLEDET = PlotsLEDET()
    variables_to_save: VariablesToSaveLEDET = VariablesToSaveLEDET()



############################
# ProteCCT options
class TimeVectorProteCCT(BaseModel):
    """
        Level 2: Class for ProteCCT time vector options
    """
    tMaxStopCondition: float = None
    minTimeStep: float = None


class GeometryGenerationOptionsProteCCT(BaseModel):
    """
        Level 2: Class for ProteCCT geometry generation options
    """
    totalConductorLength: float = None
    #numTurnsPerStrandTotal: int = None
    thFormerInsul: float = None
    #wStrandSlot: float = None
    #numRowStrands: int = None
    #numColumnStrands: int = None
    IcFactor: float = None
    polyimideToEpoxyRatio: float = None



class PhysicsProteCCT(BaseModel):
    """
        Level 2: Class for ProteCCT physics options
    """
    M: List[List[float]] = [[]]
    BMaxAtNominal: float = None
    BMinAtNominal: float = None
    INominal: float = None
    fieldPeriodicity: float = None
    #RRRFormer: float = None
    #RRROuterCylinder: float = None
    coolingToHeliumBath: int = None
    fLoopLength: float = None
    addedHeCpFrac: float = None
    addedHeCoolingFrac: float = None


class SimulationProteCCT(BaseModel):
    """
        Level 2: Class for ProteCCT physics options
    """
    tempMaxStopCondition: float = None
    IOpFractionStopCondition: float = None
    fracCurrentChangeMax: float = None
    resultsAtTimeStep: float = None
    deltaTMaxAllowed: float = None
    turnLengthElements: int = None
    externalWaveform: int = None
    saveStateAtEnd: int = None
    restoreStateAtStart: int = None
    silentRun: int = None


class PlotsProteCCT(BaseModel):
    """
        Level 2: Class for ProteCCT plots options
    """
    withPlots: int = None
    plotPauseTime: float = None


class PostProcessingProteCCT(BaseModel):
    """
        Level 2: Class for ProteCCT post-processing options
    """
    withVoltageEvaluation: int = None
    voltageToGroundOutputSelection: str = None  # Note: it will be written in a single cell in the ProteCCT file


class PROTECCT(BaseModel):
    """
        Level 1: Class for ProteCCT options
    """
    time_vector: TimeVectorProteCCT = TimeVectorProteCCT()
    geometry_generation_options: GeometryGenerationOptionsProteCCT = GeometryGenerationOptionsProteCCT()
    simulation: SimulationProteCCT = SimulationProteCCT()
    physics: PhysicsProteCCT = PhysicsProteCCT()
    post_processing: PostProcessingProteCCT = PostProcessingProteCCT()
    plots: PlotsProteCCT = PlotsProteCCT()


############################
# SIGMA options

class TimeVectorSolutionSIGMA(BaseModel):
    """
        Level 2: Class for simulation time vector in SIGMA
    """
    time_step: List[List[float]] = None

class TimeVectorSIGMA(BaseModel):
    """
        Level 2: Class for simulation time vector in SIGMA
    """
    time_vector_solution: TimeVectorSolutionSIGMA =TimeVectorSolutionSIGMA()


class SimulationSIGMA(BaseModel):
    """
        Level 2: Class for simulation parameters in SIGMA
    """
    generate_study: bool = None
    study_type: str = None
    make_batch_mode_executable: bool = None
    nbr_elements_mesh_width: int = None
    nbr_elements_mesh_height: int = None

class PhysicsSIGMA(BaseModel):
    """
        Level 2: Class for physics parameters in SIGMA
    """
    FLAG_M_pers: int = None
    FLAG_ifcc: int = None
    FLAG_iscc_crossover: int = None
    FLAG_iscc_adjw: int = None
    FLAG_iscc_adjn: int = None
    tauCC_PE: float = None


class QuenchInitializationSIGMA(BaseModel):
    """
        Level 2: Class for quench initialization parameters in SIGMA
    """
    PARAM_time_quench: float = None
    FLAG_quench_all: int = None
    FLAG_quench_off: int = None
    num_qh_div: List[int] = None
    quench_init_heat: float = None
    quench_init_HT: List[str] = None
    quench_stop_temp: float = None

class Out2DAtPointsSIGMA(BaseModel):
    coordinate_source: str = None
    variables: List[str] = None
    time: List[List[float]] = None
    map2d: str = None


class Out1DVsTimeSIGMA(BaseModel):
    variables: List[str] = None
    time: List[List[float]] = None


class Out1DVsAllTimesSIGMA(BaseModel):
    variables: List[str] = None

class QuenchHeatersSIGMA(BaseModel):
    """
        Level 2: Class for postprocessing parameters in SIGMA
    """
    quench_heater_positions: List[List[int]] = None
    th_coils: List[float] = None


class PostprocessingSIGMA(BaseModel):
    """
        Level 2: Class for postprocessing parameters in SIGMA
    """
    out_2D_at_points: Out2DAtPointsSIGMA = Out2DAtPointsSIGMA()
    out_1D_vs_times: Out1DVsTimeSIGMA = Out1DVsTimeSIGMA()
    out_1D_vs_all_times: Out1DVsAllTimesSIGMA = Out1DVsAllTimesSIGMA()


class SIGMA(BaseModel):
    """
        Level 1: Class for SIGMA options
    """
    time_vector_solution: TimeVectorSolutionSIGMA = TimeVectorSolutionSIGMA()
    simulation: SimulationSIGMA = SimulationSIGMA()
    physics: PhysicsSIGMA = PhysicsSIGMA()
    quench_initialization: QuenchInitializationSIGMA = QuenchInitializationSIGMA()
    postprocessing: PostprocessingSIGMA = PostprocessingSIGMA()
    quench_heaters: QuenchHeatersSIGMA=QuenchHeatersSIGMA()


############################
# Highest level
class DataModelMagnet(BaseModel):
    """
        **Class for the STEAM inputs**

        This class contains the data structure of STEAM model inputs.

        :param N: test 1
        :type N: int
        :param n: test 2
        :type n: int

        :return: DataModelMagnet object
    """

    Sources: SourceFiles = SourceFiles()
    GeneralParameters: General = General()
    CoilWindings: CoilWindings = CoilWindings()
    Conductors: List[Conductor] = [Conductor(cable={'type': 'Rutherford'}, strand={'type': 'Round'}, Jc_fit={'type': 'CUDI1'})]
    Circuit: Circuit = Circuit()
    Power_Supply: PowerSupply = PowerSupply()
    Quench_Protection: QuenchProtection = QuenchProtection()
    Options_FiQuS: FiQuS = FiQuS()
    Options_LEDET: LEDET = LEDET()
    Options_ProteCCT: PROTECCT = PROTECCT()
    Options_SIGMA: SIGMA = SIGMA()
