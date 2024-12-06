
# DNV PyPWS

![Phast Web Services](https://pwsassets.blob.core.windows.net/dev/LandingImage.png)

## Introduction
Welcome to ***PyPWS*** - the Python Library for Phast Web Services.  PyPWS provides an easy and efficient way of consuming the Phast Cloud APIs from your Python solutions.

## What is Phast?
Phast is the world's most comprehensive process hazard analysis software which models the progress of a potential incident from the initial release to far-field dispersion including modelling of pool spreading and evaporation and resulting flammable and toxic effects. In Phast Web Services we have taken the same state of the art consequence modelling calculations and made them available as web services so you can use them in your own applications.

## Concepts
Phast Web Services have been designed to use "entities" that are easy to grasp conceptually. So you work with physical objects like a vessel or a pipe and associated data objects like leaks, pipe ruptures and weathers. These are used when calling a vessel leak or pipe breach calculation for example.

## Getting started

> To jump to the reference documentation please click [here](#reference).

### Developing with Python

Developing solutions using Python is beyond the scope of this help file.  For more information on developing solutions using Python please refer to these useful links:

- [Python home](https://www.python.org/)
- [Downloads for all platforms](https://www.python.org/downloads/)
- [Documentation](https://www.python.org/doc/)

### Installing PyPWS
> Installation of Python itself is not covered by this documentation but there is significant help available [online](https://www.python.org/).

PyPWS can be installed from the Python Package Index (PyPI) which is a repository of software for the Python programming language.  You can find the PyPWS package on PyPI [here](https://pypi.org/project/pypws/).

To install PyPWS simply type:

`pip install pypws`

### Registering to get access to Phast Web Services
In order to use Phast Web Services you need to...

### Obtaining an access token
Once registered with Veracity you can download your access token from ...

### Registering the access token with PyPWS

### Un-installing

To uninstall PyPWS simply type:

`pip uninstall pypws`

and when prompted select ***y***.

## The basics

## Performing calculations

### Running calculations


## Reference
The following items are available:

* [Constants](#constants)
* [Enums](#enums)
* [Entities](#entities)
* [Calculations](#calculations)

### Constants
The following is a list of available constants.

| Name | Value | Description |
| --- | ---: | --- |
| ABS_TOL_RAD | 0.0000000001 | Absolute tolerance for radiation calculations. |
| ADJUST_GROUND_FLAME | 1 | Flame shape adjusted if grounded for jet fires. |
| ATM_EXP_METHOD | 4 | DNV recommended atmospheric expansion method from orifice to final state. |
| ATM_MOLWT | 28.9505 | Atmospheric molecular weight (kg/kmol). |
| ATM_PRESSURE | 101325.0 | Atmospheric pressure (Pa). |
| AWD_FLAG | 3 | Along wind diffusion method for non instantaneous dispersion. |
| BUND_AREA_MULTIPLIER_FOR_RUPTURE | 1.5 | Bund area multiplier for catastrophic ruptures. |
| BUND_CANNOT_FAIL | 0 | Bund cannot fail - liquid overspill not possible. |
| CALC_METHOD_SEP_FIREBALLS | -1 | Calculate surface emissive power for fireballs. |
| CALC_METHOD_SEP_JET_FIRES | 0 | Calculate surface emissive power for jet fires. |
| CRIT_SEP_RATIO | 0.2 | Critical separation ratio for concentration grids. |
| CRIT_WEBER | 12.5 | Critical Webber number used in the droplet size calculations. |
| DROPLET_METHOD | 6 | Modified CCPS droplet method. |
| EXPL_LOCATION | 0 | Explosion located at the cloud front (LFL fraction). |
| FIREBALL_MODEL | 0 | Roberts/TNO hybrid fireball model. |
| FLAM_AVR_TIME_PHAST_DEFAULT | 18.75 | Default value for flammable averaging time in Phast. |
| FLAMM_MASS_CALC_METHOD | 2 | Use mass between LFL and UFL for flammable mass estimation in explosion calculations. |
| FRACTION_TOTAL_TO_KINETIC | 0.04 | Kinetic energy fraction of discharge expansion energy. |
| HORIZONTAL_OPTION | 0 | Standard method for jet fire horizontal options. |
| INEX_FLAG | 2 | New standard method for modelling of instantaneous expansion. |
| JET_FIRE_AVR_TIME | 20.0 | Jet fire averaging time (s). |
| JET_FIRE_CORRELATION | 0 | Recommended jet fire correlation. |
| JET_FIRE_EXP_DUR | 20.0 | Jet fire maximum exposure duration (s). |
| JET_RATE_MOD_FACTOR | 3.0 | Jet fire rate modification factor. |
| LFL_FRACTION_EXPLOSIONS | 0.5 | LFL fraction used to define the flammable cloud for explosions. |
| MASS_MOD_FACTOR | 3.0 | Mass modification factor used in calculating the mass of material involved in the fireball. |
| MAX_DISP_STEP_SIZE | 300.0 | Maximum integration step for dispersion calculations (s). |
| MAX_DROP_DIAMETER | 0.01 | Upper limit of the droplet diameter (m). |
| MAX_NUMBER_FLAME_COORDINATES | 10 | Maximum number of flame coordinates for jet fires. |
| MAX_RELEASE_DURATION | 3600.0 | Maximum release duration (s). |
| MAX_SEP_FIREBALL | 400000.0 | Maximum surface emissive power for fireballs (W/m2). |
| MAX_SEP_JET_FIRE | 350000.0 | Maximum surface emissive power for a jet fire (W/m2). |
| MAX_SEP_POOL_FIRE | 350000.0 | Maximum surface emissive power for pool fires (W/m2). |
| MAX_TIMESTEPS | 900 | Maximum number of time steps for time varying releases. |
| MAX_VELOCITY | 100000000.0 | Maximum release velocity (m/s). |
| MAX_VELOCITY_FLAG | 0 | Fixed velocity capping method. |
| MAXIMUM_COMPONENT_COUNT | 20 | Maximum number of components. |
| MAXIMUM_LEAK_DIAMETERS_COUNT | 5 | Maximum number of leak diameters for scenario generation. |
| MAXIMUM_PT_STEPS | 441 | Maximum number of steps in an iteration over PT space. |
| MAXIMUM_TEMPERATURE_LIMIT | 1200.0 | Maximum temperature allowed for dispersion calculations (K). |
| MAXIMUM_WEATHER_COUNT | 10 | Maximum number of weathers. |
| ME_EXPL_EFFICIENCY_UNCONFINED | 100.0 | Explosion efficiency for unconfined multi-energy explosions (%). |
| ME_EXPL_EFFICIENCY_UNIFORM_CONFINED | 12.5 | Explosion efficiency for uniform confined multi-energy explosions (%). |
| MILLER_CROSSWIND_METHOD | 0 | Method for modelling crosswind effects for Miller model: 0 = modified Johnson approach; 1 = Full deflection. |
| MILLER_FLAME_RAD_FRACTION_METHOD | 0 | Miller jet flame radiative fraction calculation method: 0 = Miller method; 2 = Sandia method. |
| MILLER_FLAME_TRAJECTORY | 0 | Miller jet flame trajectory: 0 = Line segments; 1 = Curved line. |
| MILLER_LIFT_OFF_OPTION | 1 | Method for modelling flame lift-off for Miller model: 0 = Miller method; 1 = DNV. |
| MILLER_NG_FLOWRATE_METHOD | 1 | Miller natural gas flow rate matching method: 0 = Miller (2017); 1 = DNV [similarity approach]. |
| MILLER_RAD_INTENSITY_CAP_METHOD | 2 | Radiation intensity capping method: 0 = No capping; 1 = Max intensity capping; 2 = Stefan Boltzmann's law. |
| MIN_DROP_DIAMETER | 0.00000001 | Cut-off droplet diameter below which droplets are no longer modelled (m). |
| MIN_EXPL_MASS | 0.0 | Minimum explosive mass (kg). |
| MINIMUM_TEMPERATURE_LIMIT | 11.0 | Minimum temperature allowed for dispersion calculations (K). |
| MIX_LAYER_HEIGHT_FOR_A | 1300 | Mixing layer height for Pasquill stability class A (m). |
| MIX_LAYER_HEIGHT_FOR_AB | 1080 | Mixing layer height for Pasquill stability class A/B (m). |
| MIX_LAYER_HEIGHT_FOR_B | 920 | Mixing layer height for Pasquill stability class B (m). |
| MIX_LAYER_HEIGHT_FOR_BC | 880 | Mixing layer height for Pasquill stability class B/C (m). |
| MIX_LAYER_HEIGHT_FOR_C | 840 | Mixing layer height for Pasquill stability class C (m). |
| MIX_LAYER_HEIGHT_FOR_CD | 820 | Mixing layer height for Pasquill stability class C/D (m). |
| MIX_LAYER_HEIGHT_FOR_D | 800 | Mixing layer height for Pasquill stability class D (m). |
| MIX_LAYER_HEIGHT_FOR_E | 400 | Mixing layer height for Pasquill stability class E (m). |
| MIX_LAYER_HEIGHT_FOR_F | 100 | Mixing layer height for Pasquill stability class F (m). |
| MIX_LAYER_HEIGHT_FOR_G | 100 | Mixing layer height for Pasquill stability class G (m). |
| N_VTIMES_CONT | 5 | Number of time steps for continuous clouds used in explosion calculations. |
| N_VTIMES_MAX | 100 | Maximum number of time steps for explosion calculations. |
| N_VTIMES_TV | 15 | Number of time steps for time-varying clouds used in explosion calculations. |
| NUM_FIXED_STEPS | 20 | Number of fixed size output steps for dispersion calculations. |
| NUM_X_VIEW | 21 | Number of steps in the downwind direction per explosion cloud view. |
| OBSERVER_TYPE | 1 | Planar observer type for radiation modelling. |
| PIPE_NODES_COUNT | 2 | Number of nodes on the pipe (start, end + intermediate). |
| RAD_FRAC_GENERAL | 0.4 | Radiative fraction for general pool fires. |
| RAD_LEVEL_GRID | 1600.0 | The radiation level used for calculating radiation grids. The value is set equal to the lowest default radiation value present in the VesselLeak apps. |
| RAD_PROBIT_A | -36.38 | Probit value A for radiation. |
| RAD_PROBIT_B | 2.56 | Probit value B for radiation. |
| RAD_PROBIT_N | 1.33 | Probit value N for radiation. |
| RADS_INTEGRATOR_TYPE | 2 | Integration method for multi-point flame sources: 0 = Discrete; 1 = QSIMP; 2 = Gauss-Lobatto. |
| RADS_NUM_INTEGRATOR_POINTS | 30 | Number of integration points to use for multi-point sources: 30 by default. |
| REF_HT_WIND_SPEED | 10.0 | Reference height for wind speed. |
| REPORTING_HEIGHT_FLAG | 1 | Centreline height is used for explosion calculations. |
| RESULT_GRID_STEP | 10.0 | Flammable result grid step in x-direction (m). |
| SHORT_DURATION_CUTOFF | 20.0 | Cutoff for short duration effects. Only mass released until this time is used in the fireball calculation (s). |
| SHORT_PIPE_ROUGHNESS | 0.000045 | Short pipe roughness (m). |
| STOICH_MASS_FRAC_METHOD | 0 | Use old method (valid for paraffins only) for calculating the stoichiometric mass fraction. |
| TNO_FLAME_TEMP | 2000.0 | Flame temperature for TNO fireball model (K). |
| TOXIC_MIN_LETHALITY | 0.001 | Toxics: minimum probability of death. |
| TOXIC_MIX_CALC_METHOD | 3 | Product of each as the multi component toxic calculation method. |
| TOXIC_PD_TOLERANCE | 0.01 | Toxics: tolerance on minimum probability of death. |
| TOXIC_PROBIT_METHOD | 1 | Prefer Probit as the toxic calculation method, i.e. if probit data is available that will be the preferred method to use. |
| TOXIC_TAIL_TIME | 1800.0 | Tail time for indoor toxic calculations (s). |
| UDS_MAX_TEMPERATURE | 1200.0 | The absolute maximum temperature allowed for a user-defined source. |
| UDS_MIN_TEMPERATURE | 11.0 | The absolute minimum temperature allowed for a user-defined source. |
| UNCONFINED_EXPLOSION_STRENGTH | 2.0 | Unconfined explosion strength (Multi energy method). |
| UNIFORM_CONFINED_EXPLOSION_METHOD_OPTION | 3 | Uniform confined Multi Energy explosion method. |
| USE_SHAPE_CORRELATION | -1 | Use shape correlation for fireballs. |
| USE_SOLAR | 0 | Exclude solar radiation from radiation calculations. |
| USE_VOLUMES | 2 | Use volumes when specifying size of confined sources. |
| USER_DEFINED_CONFINED_EXPLOSION_METHOD_OPTION | 1 | Unconfined Multi-Energy explosion method. |
| USER_INPUT_POST_EXPANSION_VELOCITY | 0 | Velocity for jet fire calculations must be user supplied. |
| WIND_CUTOFF_HEIGHT | 1.0 | Cut-off height for wind speed calculations. |
| WIND_PROFILE_FLAG | 2 | Logarithmic wind profile. |

### Enums
The following is a list of available enums.

* [AtmosphericStabilityClass](#atmosphericstabilityclass)
* [ContourType](#contourtype)
* [DayNight](#daynight)
* [DesignVariable](#designvariable)
* [DynamicType](#dynamictype)
* [FireType](#firetype)
* [FlammableToxic](#flammabletoxic)
* [FlashAtOrifice](#flashatorifice)
* [FluidSpec](#fluidspec)
* [LuminousSmokyFlame](#luminoussmokyflame)
* [MEConfinedMethod](#meconfinedmethod)
* [MessageResultCode](#messageresultcode)
* [MixtureModelling](#mixturemodelling)
* [Phase](#phase)
* [PoolFireType](#poolfiretype)
* [PoolSurfaceType](#poolsurfacetype)
* [PropertyTemplate](#propertytemplate)
* [RadiationType](#radiationtype)
* [RainoutThermoFlag](#rainoutthermoflag)
* [ReleaseDirection](#releasedirection)
* [Resolution](#resolution)
* [ResultCode](#resultcode)
* [Scope](#scope)
* [SolidModelling](#solidmodelling)
* [SpecialConcentration](#specialconcentration)
* [SurfaceType](#surfacetype)
* [TargetVariable](#targetvariable)
* [TimeVaryingOption](#timevaryingoption)
* [ToxicResultType](#toxicresulttype)
* [VesselConditions](#vesselconditions)
* [VesselShape](#vesselshape)

Back to [reference home](#reference)

### AtmosphericStabilityClass
> Atmospheric stability classes.

| Name | Value | Description |
| --- | ---: | --- |
StabilityA | 1 | A. |
StabilityAB | 2 | A/B. |
StabilityB | 3 | B. |
StabilityBC | 4 | B/C. |
StabilityC | 5 | C. |
StabilityCD | 6 | C/D. |
StabilityD | 7 | D. |
StabilityE | 8 | E. |
StabilityF | 9 | F. |
StabilityG | 10 | G. |

Back to [reference home](#reference)
### ContourType
> Type of contour plot or grid.

| Name | Value | Description |
| --- | ---: | --- |
Footprint | 1 | Footprint (XY plane). |
FootprintAtTime | 2 | Footprint (XY plane) at given time. |
FootprintEllipse | 3 | Footprint ellipse (XY plane). |
Sideview | 4 | Sideview (XZ plane). |
Crosswind | 5 | Crosswind (YZ plane). |
FlameFootprint | 6 | Flame shape footprint (XY plane). |
FlameSideview | 7 | Flame shape side view (XZ plane). |
FlameCrosswind | 8 | Flame shape crosswind (YZ plane). |

Back to [reference home](#reference)
### DayNight
> Flag to indicate wheather we are in day or nightime.

| Name | Value | Description |
| --- | ---: | --- |
Unset | 0 | Day/night flag not set. |
Day | 1 | Day. |
Night | 2 | Night. |

Back to [reference home](#reference)
### DesignVariable
> Choice of input to vary to achieve target design.

| Name | Value | Description |
| --- | ---: | --- |
PipeLength | 1 | The length of the flare stack. |
PipeDiameter | 2 | The diameter of the flare stack. |
OperatingPressure | 3 | The driving pressure in the tank feeding the flare stack. |

Back to [reference home](#reference)
### DynamicType
> Type of release or cloud.

| Name | Value | Description |
| --- | ---: | --- |
Unset | 0 | Unset. |
Instantaneous | 1 | Instantaneous. |
Continuous | 2 | Continuous. |
TimeVarying | 3 | Time-varying. |

Back to [reference home](#reference)
### FireType
> Fire type.

| Name | Value | Description |
| --- | ---: | --- |
NoFire | 0 | No fire. |
Fire_ball | 1 | Fireball. |
Pool | 2 | Pool fire. |
APIJet | 3 | API jet fire. |
ConeJet | 4 | Cone jet fire. |
MultiPointSourceJet | 10 | Multi-point [e.g. Miller] source jet fire model. |

Back to [reference home](#reference)
### FlammableToxic
> Flag to indicate if the material is flammable, toxic, both or inert.

| Name | Value | Description |
| --- | ---: | --- |
Inert | -2 | Inert. |
Toxic | -1 | Toxic. |
Both | 0 | Both. |
Flammable | 1 | Flammable. |

Back to [reference home](#reference)
### FlashAtOrifice
> Allow phase change upstream of orifice.

| Name | Value | Description |
| --- | ---: | --- |
NoFlashAtOrifice | 0 | No phase change to the orifice. |
FlashAllowed | 1 | Flashing allowed to the orifice. |
DisallowLiquidFlash | 2 | No flashing of liquid (metastable liquid). |

Back to [reference home](#reference)
### FluidSpec
> Fluid state specification.

| Name | Value | Description |
| --- | ---: | --- |
PTLf | 0 | Specify all of P,T,LF. |
TP | 1 | Specify temperature and pressure. |
TBub | 2 | Bubble point at fixed temperature. |
PBub | 3 | Bubble point at fixed pressure. |
TDew | 4 | Dew point at fixed temperature. |
PDew | 5 | Dew point at fixed pressure. |
PLf | 6 | Fixed pressure and liquid fraction. |
TLf | 7 | Fixed temperature and liquid fraction. |

Back to [reference home](#reference)
### LuminousSmokyFlame
> Luminous smoky flame.

| Name | Value | Description |
| --- | ---: | --- |
NonFlammable | -1 | Non flammable. |
Luminous | 0 | Luminous flame. |
Smoky | 1 | Smoky flame. |
General | 2 | General type flame. |

Back to [reference home](#reference)
### MEConfinedMethod
> Multi-energy confined method.

| Name | Value | Description |
| --- | ---: | --- |
UserDefined | 1 | User defined method. |
UniformConfined | 3 | Uniform confined method. |

Back to [reference home](#reference)
### MessageResultCode
> A message code used to communicate additional information between the APIs and the client applications.

| Name | Value | Description |
| --- | ---: | --- |
UserNotAuthorizedToUpgradeEntity | 20000 | Authenticated user is not authorized to upgrade the requested entity. |

Back to [reference home](#reference)
### MixtureModelling
> Method for modelling a mixture.

| Name | Value | Description |
| --- | ---: | --- |
PC | 0 | Pseudo-component treatment of mixtures. |
MC_SingleAerosol | 1 | Multi-component single aerosol. |
MC_MultipleAerosol | 3 | Multi-component multiple aerosol hybrid method. |

Back to [reference home](#reference)
### Phase
> Fluid phase (vapour, liquid or two-phase).

| Name | Value | Description |
| --- | ---: | --- |
Unset | 0 | Unset. |
Vapour | 1 | Vapour. |
TwoPhase | 2 | Two-phase. |
Liquid | 3 | Liquid. |

Back to [reference home](#reference)
### PoolFireType
> Pool fire type.

| Name | Value | Description |
| --- | ---: | --- |
Immediate | 0 | Immediate pool fire. |
Early | 1 | Early pool fire. |
Late | 2 | Late pool fire. |

Back to [reference home](#reference)
### PoolSurfaceType
> Surface type for pools and bunds.

| Name | Value | Description |
| --- | ---: | --- |
WetSoil | 1 | Wet soil. |
DrySoil | 2 | Dry soil. |
Concrete | 3 | Concrete. |
InsulatedConcrete | 4 | Insulated concrete. |
DeepOpenWater | 5 | Deep open water. |
ShallowOpenWater | 6 | Shallow open water. |
DeepRiver | 7 | Deep river. |
ShallowRiver | 8 | Shallow river. |

Back to [reference home](#reference)
### PropertyTemplate
> Choice of property template.

| Name | Value | Description |
| --- | ---: | --- |
PhastMC | 100 | The PhastMC is the default Phast template. |
Phast64 | 101 | Old default Phast property template. |
AcidAssociation | 102 | Acid association template for modelling reactive Hydrogen Fluoride. |
SoaveRedlickKwong | 103 | Template using the Soave-Redlich-Kwong cubic equation of state. |
PengRobinson | 104 | Template using the Peng-Robinson cubic equation of state. |
PRIdealFugacity | 106 | The Peng-Robinson template but with ideal fugacities for improved robustness. |
SRKIdealFugacity | 107 | The Soave-Redlich-Kwong template but with ideal fugacities for improved robustness. |

Back to [reference home](#reference)
### RadiationType
> Radiation type.

| Name | Value | Description |
| --- | ---: | --- |
Unset | 0 | Radiation type not set. |
Dose | 1 | Radiation dose. |
Probit | 2 | Radiation probit. |
Lethality | 3 | Radiation lethality. |
ViewFactor | 4 | View factor. |
Intensity | 5 | Radiation intensity. |

Back to [reference home](#reference)
### RainoutThermoFlag
> Rainout and thermodynamic modelling.

| Name | Value | Description |
| --- | ---: | --- |
NoRainoutEquilibrium | -1 | No rainout, equilibrium. |
RainoutEquilibrium | 1 | Rainout, equilibrium. |
RainoutNonEquilibrium | 2 | Rainout, non-equilibrium. |

Back to [reference home](#reference)
### ReleaseDirection
> Release direction.

| Name | Value | Description |
| --- | ---: | --- |
Horizontal | 0 | Horizontal. |
Vertical | 1 | Vertical. |

Back to [reference home](#reference)
### Resolution
> Output resolution (and performance).

| Name | Value | Description |
| --- | ---: | --- |
High | 1 | High. |
Medium | 2 | Medium. |
Low | 3 | Low. |
VeryHigh | 4 | Very high. |
Extreme | 5 | Extremely high. |

Back to [reference home](#reference)
### ResultCode
> Result codes returned from calls to the MDE.

| Name | Value | Description |
| --- | ---: | --- |
Fail_Validation | -1 | Validation fail. |
Success | 0 | Success. |
Fail_Execution | 1 | Execution fail. |
InputFileNotSpecifiedError | 21008 | Input file not specified error. |
InputFileNotFoundError | 21009 | Input file not found error. |
OutputFileNotSpecifiedError | 21010 | Output file not specified error. |
ErrorReadingInputFileError | 21011 | Error reading input file error. |
FailedToInitialiseMdeErrorReportingError | 21012 | Failed to initialise mde error reporting error. |
FailedToInitialisePropertySystemError | 21013 | Failed to initialise property system error. |
InvalidAccessTokenError | 21014 | Invalid access token error. |
NoDischargeRecordsError | 21100 | No discharge records error. |
NoDispersionRecordsError | 21102 | No dispersion records error. |
NoFlameRecordsError | 21103 | No flame records error. |
MDEInitializationError | 21104 | MDE initialization error. |
MDEErrorReportingInitializationError | 21105 | MDE error reporting initialization error. |
PhysicalPropertySystemInitializationError | 21106 | Physical property system initialization error. |
DischargeCalculationInitializationError | 21107 | Discharge calculation initialization error. |
DispersionCalculationInitializationError | 21108 | Dispersion calculation initialization error. |
UnableToReadDataError | 21109 | Unable to read data error. |

Back to [reference home](#reference)
### Scope
> Determines whether an entity is globally or workspace scoped.

| Name | Value | Description |
| --- | ---: | --- |
Global | 1 | Entity has global scope. |
Workspace | 2 | Entity has workspace scope. |

Back to [reference home](#reference)
### SolidModelling
> Flag for whether we want to deploy or disable solid modelling. In addition to this flag, each component has its own allowSolids flag.

| Name | Value | Description |
| --- | ---: | --- |
DisableSolidModelling | 0 | Solid modelling will not be used, even if it is allowed by the component in question. |
DeploySolidModelling | 1 | Solid modelling will be deployed if it is supported by the component in question. |

Back to [reference home](#reference)
### SpecialConcentration
> Concentrations of interest.

| Name | Value | Description |
| --- | ---: | --- |
NotDefined | 0 | Not Defined. |
LFLFraction | 1 | LFL Fraction. |
LFL | 2 | LFL. |
UFL | 3 | UFL. |
Min | 4 | Minimum concentration. |

Back to [reference home](#reference)
### SurfaceType
> Dispersing surface type (land or water).

| Name | Value | Description |
| --- | ---: | --- |
Land | 1 | Dispersion over land. |
Water | 2 | Dispersion over water. |

Back to [reference home](#reference)
### TargetVariable
> Type of result for design constraint.

| Name | Value | Description |
| --- | ---: | --- |
MassFlowRate | 1 | Specify a target mass flow rate. |
ExpandedReleaseVelocity | 2 | Specify a target expanded release velocity. |
PipeExitPressure | 3 | Specify a target pipe exit pressure. |
RadiationLevelTransectEndpoint | 4 | Specify a target radiation level at the endpoint of the radiation transect. |

Back to [reference home](#reference)
### TimeVaryingOption
> Dynamic modelling of leaks and lines.

| Name | Value | Description |
| --- | ---: | --- |
InitialRate | 1 | Use initial rate. |
TimeVaryingRate | 2 | Use time-varying rates. |

Back to [reference home](#reference)
### ToxicResultType
> Type of toxic result.

| Name | Value | Description |
| --- | ---: | --- |
Unset | 0 | Toxic result type not set. |
ToxicLethality | 1 | Probability of death. |
ToxicProbit | 2 | Toxic probit number. |
ToxicDose | 3 | Toxic dose. |

Back to [reference home](#reference)
### VesselConditions
> The vessel conditions expected by the user.

| Name | Value | Description |
| --- | ---: | --- |
Unset | 0 | Unset. |
PureGas | 1 | Pressurised gas vessel. |
HomogeneousVesselType | 2 | Input fluid state expected to be homogenesously mixed two phase. |
StratifiedTwoPhaseVessel | 3 | Two phase vessel. |
PressurizedLiquidVessel | 4 | Pressurised liquid vessel. |
AtmosphericLiquidVessel | 5 | Input fluid state expected to be liquid stored at atmospheric pressure. |

Back to [reference home](#reference)
### VesselShape
> Vessel shape.

| Name | Value | Description |
| --- | ---: | --- |
VerticalCylinder | 1 | Vertical cylinder. |
HorizontalCylinder | 2 | Horizontal cylinder. |
VesselSphere | 3 | Sphere. |
VesselCuboid | 4 | Cuboid. |

Back to [reference home](#reference)

### Entities
The following is a list of available entities.

* [AtmosphericStorageTank](#atmosphericstoragetank)
* [Bund](#bund)
* [CatastrophicRupture](#catastrophicrupture)
* [ConcentrationRecord](#concentrationrecord)
* [ConstantMaterialResult](#constantmaterialresult)
* [Constraint](#constraint)
* [DischargeParameters](#dischargeparameters)
* [DischargeRecord](#dischargerecord)
* [DischargeResult](#dischargeresult)
* [DispersionOutputConfig](#dispersionoutputconfig)
* [DispersionParameters](#dispersionparameters)
* [DispersionRecord](#dispersionrecord)
* [ExplosionConfinedVolume](#explosionconfinedvolume)
* [ExplosionOutputConfig](#explosionoutputconfig)
* [ExplosionOverpressureResult](#explosionoverpressureresult)
* [ExplosionParameters](#explosionparameters)
* [FlameRecord](#flamerecord)
* [FlameResult](#flameresult)
* [FlammableOutputConfig](#flammableoutputconfig)
* [FlammableParameters](#flammableparameters)
* [FlareStack](#flarestack)
* [FlashResult](#flashresult)
* [Interval](#interval)
* [Leak](#leak)
* [LineRupture](#linerupture)
* [LocalPosition](#localposition)
* [Material](#material)
* [MaterialComponent](#materialcomponent)
* [MaterialComponentData](#materialcomponentdata)
* [MaterialComponentDataItem](#materialcomponentdataitem)
* [MixtureConstantPropertiesResult](#mixtureconstantpropertiesresult)
* [Pipe](#pipe)
* [PipeBreach](#pipebreach)
* [PoolFireFlameResult](#poolfireflameresult)
* [PoolRecord](#poolrecord)
* [PoolVapourisationParameters](#poolvapourisationparameters)
* [PropertiesDipprPT1](#propertiesdipprpt1)
* [PropertiesDipprPT2](#propertiesdipprpt2)
* [PropertiesDipprPT3](#propertiesdipprpt3)
* [PropertiesDnvPT1](#propertiesdnvpt1)
* [PropertiesDnvPT2](#propertiesdnvpt2)
* [PropertiesDnvPT3](#propertiesdnvpt3)
* [PTRange](#ptrange)
* [RadiationRecord](#radiationrecord)
* [ReliefValve](#reliefvalve)
* [ScalarUdmOutputs](#scalarudmoutputs)
* [ShortPipeRupture](#shortpiperupture)
* [State](#state)
* [Structure](#structure)
* [Substrate](#substrate)
* [ThermoPathRecord](#thermopathrecord)
* [ToxicRecord](#toxicrecord)
* [Transect](#transect)
* [Vessel](#vessel)
* [VesselLeakMaxFlammableCloudResults](#vesselleakmaxflammablecloudresults)
* [VesselRuleSet](#vesselruleset)
* [VesselSphere](#vesselsphere)
* [Weather](#weather)
* [WeatherStationData](#weatherstationdata)

Back to [reference home](#reference)


### AtmosphericStorageTank
> Atmospheric storage tank.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| State | State (temperature). | [State](#state) |  |  |  |
| Diameter | Diameter of the tank. | double |  | Length |  [m] |
| Height | Height of the tank. | double |  | Length |  [m] |
| Material | Material. | [Material](#material) |  |  |  |
| LiquidFillFractionByVolume | Liquid fill fraction by volume. | double | 0.9 | Fraction |  [fraction] |

Back to [reference home](#reference)

### Bund
> Bund.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| BundHeight | Bund height. | double | 0.0 | Length |  [m] |
| BundDiameter | Bund diameter. | double | 0.0 | Length |  [m] |
| SpecifyBund | Specify a bund. | bool | false |  |  |

Back to [reference home](#reference)

### CatastrophicRupture
> Catastrophic rupture of a vessel scenario.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |

Back to [reference home](#reference)

### ConcentrationRecord
> Concentration record.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Concentration | Cloud concentration at an x, y, z position. | double |  | Fraction |  [fraction] |
| Position | x, y, z position. | [LocalPosition](#localposition) |  |  |  |

Back to [reference home](#reference)

### ConstantMaterialResult
> Constant material properties, i.e. critical pressure, temperature, mole weight.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| CriticalPressure | The critical pressure of the material. | double |  | Pressure |  [Pa] |
| CriticalTemperature | The critical temperature of the material. | double |  | Temperature |  [K] |
| TotalMolecularWeight | The total molecular weight of the material. | double |  | MolecularWeight |  [kg/kmol] |

Back to [reference home](#reference)

### Constraint
> A set of data describing a design constraint. This includes the result target of interest  (e.g. mass flow) and the design variable (e.g. stack diameter).

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| TargetVariable | The result type to be prescribed as a design target. | [TargetVariable](#targetvariable) | MassFlowRate |  |  |
| TargetVariableValue | User-defined target value for the chosen result type. | double |  |  |  |
| DesignVariable | The input type to vary to achieve the design target. | [DesignVariable](#designvariable) | PipeDiameter |  |  |
| PermittedDesignVariableInterval | An interval of permitted values for the design variable. | [Interval](#interval) |  |  |  |

Back to [reference home](#reference)

### DischargeParameters
> Discharge parameters.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| FlashAtOrifice | Flashing at orifice. | [FlashAtOrifice](#flashatorifice) | DisallowLiquidFlash |  |  |

Back to [reference home](#reference)

### DischargeRecord
> Discharge results at a given time.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Time | Time. | double |  | Time |  [s] |
| MassFlow | Mass flow rate (continuous and time-varying). | double |  | MassFlowRate |  [kg/s] |
| FinalState | Final fluid state. | [State](#state) |  |  |  |
| FinalVelocity | Final velocity. | double |  | Velocity |  [m/s] |
| OrificeState | Orifice fluid state. | [State](#state) |  |  |  |
| OrificeVelocity | Orifice velocity. | double |  | Velocity |  [m/s] |
| StorageState | Storage fluid state. | [State](#state) |  |  |  |
| DropletDiameter | Representative droplet size. | double |  | Length |  [m] |
| ExpandedDiameter | Expanded diameter. | double | 0.0 | Length |  [m] |

Back to [reference home](#reference)

### DischargeResult
> Scalar discharge results.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ExpansionEnergy | Specific expansion energy (instantaneous releases only). | double |  | Energy |  [J] |
| ReleaseMass | Released mass. | double |  | Mass |  [kg] |
| Height | Release height above ground. | double |  | Length |  [m] |
| Angle | Release angle (non-instantaneous releases only). | double |  | Angle |  [Radians] |
| ReleaseType | Instantaneous, continuous or time-varying. | [DynamicType](#dynamictype) | Unset |  |  |
| HoleDiameter | Diameter of the hole. | double |  | Length |  [m] |
| PreDilutionAirRate | Pre-dilution air rate. | double | 0 | MassFlowRate |  [kg/s] |

Back to [reference home](#reference)

### DispersionOutputConfig
> Dispersion plotting and reporting control parameters.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| DownwindDistance | Downwind distance. | double | 100 | Length |  [m] |
| Time | Time since start of the release. | double | 60 | Time |  [s] |
| Resolution | Output resolution of results and gird. | [Resolution](#resolution) | Medium |  |  |
| Elevation | Height of interest above ground level. | double | 1 | Length |  [m] |
| SpecialConcentration | Pre-defined concentration. | [SpecialConcentration](#specialconcentration) | Min |  |  |
| Concentration | Concentration (vol fraction). Not used unless SpecialConcentration is undefined. | double | 0 | Fraction |  [fraction] |
| CrosswindDistance | Crosswind distance. | double | 0 | Length |  [m] |
| ContourType | List of view types. | [ContourType](#contourtype) | Footprint |  |  |
| LFLFractionValue | Value of the lower flammable limit fraction. | double | 0.5 | Fraction |  [fraction] |
| ComponentToTrackIndex | Index of the component to track. | int | -1 |  |  |
| ComponentToTrackName | Name of the property to track. | string |  |  |  |

Back to [reference home](#reference)

### DispersionParameters
> Dispersion Parameters.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| RelativeTolerance | Relative tolerance. | double | 0.001 | Fraction |  [fraction] |
| RainoutThermoFlag | Rainout and equilibrium method. | [RainoutThermoFlag](#rainoutthermoflag) | RainoutNonEquilibrium |  |  |
| FixedStepSize | Fixed step size. | double | 0.01 | Time |  [s] |
| OutputStepMultiplier | Ratio to increase step size. | double | 1.2 |  |  |
| MaxDispersionDistance | Absolute maximum distance for dispersion calculations. | double | 50000 | Length |  [m] |
| MaxDispersionHeight | Absolute maximum height for dispersion calculations. | double | 1000 | Length |  [m] |
| NumberOfReleaseObservers | Number of release observers for time-varying releases. | int | 5 |  |  |
| NumberOfPoolObservers | Number of pool observers for rainout cases. | int | 10 |  |  |
| AveragingTime | Core averaging time. | double | 18.75 | Time |  [s] |
| LFLFractionToStop | The lowest LFL fraction of interest. | double | 0.5 | Fraction |  [fraction] |

Back to [reference home](#reference)

### DispersionRecord
> Observer dispersion record at a given time.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ObserverIndex | Id of the observer associated with this record. | int |  |  |  |
| CentrelineConcentration | Centreline concentraton (molar). | double |  | Fraction |  [fraction] |
| DownwindDistance | Distance downwind. | double |  | Length |  [m] |
| Time | Time after the start of the release. | double |  | Time |  [s] |
| CentrelineConcentrationUncorrected | Uncorrected centreline concentraton (molar). | double |  | Fraction |  [fraction] |
| CrosswindRadius | Crosswind radius. | double |  | Length |  [m] |
| VerticalRadius | Vertical radius. | double |  | Length |  [m] |
| CrosswindExponent | Crosswind exponent. | double |  |  |  |
| VerticalExponent | Vertical exponent. | double |  |  |  |
| Theta | Centreline angle from horizontal. | double |  | Angle |  [Radians] |
| CentrelineHeight | Centreline height. | double |  | Length |  [m] |
| LiquidFraction | Liquid mass fraction. | double |  | Fraction |  [fraction] |
| VapourTemperature | Vapour temperature. | double |  | Temperature |  [K] |
| MassConc | Mass concentration. | double |  | Density |  [kg/m3] |
| Velocity | Velocity. | double |  | Velocity |  [m/s] |
| MassFlow | Mass flow rate (non-instantaneous). | double |  | MassFlowRate |  [kg/s] |
| InstCon | Instantanous or continuous (time-varying not permitted). | [DynamicType](#dynamictype) | Unset |  |  |
| ProfileFlag | Profile flag. | int |  |  |  |
| ElevFlag | Elevation flag. | int |  |  |  |
| RhoCloud | Cloud density. | double |  | Density |  [kg/m3] |
| LiqTemp | Liquid temperature. | double |  | Temperature |  [K] |
| EffectiveWidth | Effective width. | double |  | Length |  [m] |
| EffectiveHeight | Effective height. | double |  | Length |  [m] |
| PassTranDist | Passive transition distance. | double |  | Length |  [m] |
| DownwindRadius | Downwind radius. | double |  | Length |  [m] |
| DropletDiameter | Droplet diameter. | double |  | Length |  [m] |
| DropletHeight | Droplet height. | double |  | Length |  [m] |
| DropletDistance | Droplet downwind distance. | double |  | Length |  [m] |
| Mass | Mass (instantaneous). | double |  | Mass |  [kg] |

Back to [reference home](#reference)

### ExplosionConfinedVolume
> Confined explosion volume data.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ConfinedStrength | Explosion strength of confined volume. | double | 7 |  |  |
| ConfinedVolume | Explosion volume of confined source. | double | 1 | Volume |  [m3] |

Back to [reference home](#reference)

### ExplosionOutputConfig
> Explosion output configuration.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| OverpressureLevel | Overpressure of interest for explosions. | double | 2068 | Pressure |  [Pa] |
| MEConfinedMethod | Explosion ME confined method where Uniform Confined = 3, User Defined = 1. | [MEConfinedMethod](#meconfinedmethod) | UniformConfined |  |  |

Back to [reference home](#reference)

### ExplosionOverpressureResult
> Worst case explosion summary results for a given overpressure.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Overpressure | Overpressure for this result. | double |  | Pressure |  [Pa] |
| ExplosionCentre | Centre of the explosion (distance downwind). | double |  | Length |  [m] |
| MaximumDistance | Maximum distance to overpressure (downwind edge). | double |  | Length |  [m] |
| ExplodedMass | Flammable mass used in the explosion. | double |  | Mass |  [kg] |
| IgnitionTime | Time of ignition. | double |  | Time |  [s] |
| Radius | Radius of the explosion at the explosion centre. | double |  | Length |  [m] |

Back to [reference home](#reference)

### ExplosionParameters
> Explosion parameters.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ExplosionUniformStrength | Explosion strength for uniform unconfined (Multi-energy method). | double | 10.0 |  |  |

Back to [reference home](#reference)

### FlameRecord
> Flame geometry description.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| xCoordinate | Distance downwind. | double |  | Length |  [m] |
| zCoordinate | Height above ground. | double |  | Length |  [m] |
| rCoordinate | Flame radius. | double |  | Length |  [m] |
| phiCoordinate | Inclination from vertical. | double |  | Angle |  [Radians] |

Back to [reference home](#reference)

### FlameResult
> Fire results.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Time | Time of fire, or duration if initial rate. | double |  | Time |  [s] |
| SurfaceEmissivePower | Surface emissive power of flame. | double |  | RadiationIntensity |  [W/m2] |
| FireType | Fire type  (Fireball, pool, cone jet, API jet, Multi point source jet). | [FireType](#firetype) | NoFire |  |  |
| FlameLength | Length of the flame. | double |  | Length |  [m] |
| FlameDiameter | Diameter of the flame. | double |  | Length |  [m] |

Back to [reference home](#reference)

### FlammableOutputConfig
> Fire and radiation output configuration.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Position | Position used for radiation calculations (including contours). | [LocalPosition](#localposition) | LocalPosition() |  |  |
| RadiationType | Radiation type. | [RadiationType](#radiationtype) | Intensity |  |  |
| ContourType | Plane orientation for contouring. | [ContourType](#contourtype) | FootprintEllipse |  |  |
| RadiationLevel | Radiation level (could be dose, probit, intensity, etc). | double | 4000 |  |  |
| RadiationResolution | Spatial resolution for radiation calculations. | [Resolution](#resolution) | Medium |  |  |
| Transect | Definition of line segment of interest for radiation transects. | [Transect](#transect) | Transect() |  |  |
| FixedOrientation | If disabled orientation optimized to give maximum radiation. | int | 0 |  |  |
| Orientation | Horizontal angle with respect to the downwind direction. | double | 0 | Angle |  [Radians] |
| FixedInclination | If disabled inclination optimized to give maximum radiation. | int | 0 |  |  |
| Inclination | Angle between the normal to the surface and the horizontal plane. | double | 0 |  |  |

Back to [reference home](#reference)

### FlammableParameters
> Fire and radiation parameters.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| MaxExposureDuration | Maximum exposure duration to radiation effects. | double | 20 | Time |  [s] |
| RadiationRelativeTolerance | Relative tolerance for radiation calculations. | double | 0.01 | Fraction |  [fraction] |
| PoolFireType | Type of pool fire modelling. | [PoolFireType](#poolfiretype) | Late |  |  |
| JetFireAutoSelect | Option to automatically select jet fire modelling. | bool | false |  |  |
| TimeAveraging | Average between 0 s and the time of interest?. | bool | true |  |  |
| TimeOfInterest | Time of interest. | double | 20 |  |  |

Back to [reference home](#reference)

### FlareStack
> Contains inputs required for running a flare stack calculation.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| FlareStackMaterial | Material being flared. | [Material](#material) |  |  |  |
| FlareStackFluidState | Fluid state in flare stack (driving the outflow). | [State](#state) |  |  |  |
| FlareStackHeight | Flare stack tip height above ground level. | double |  | Length |  [m] |
| FlareStackTipDiameter | Diameter of flare stack tip. | double |  | Length |  [m] |
| FlareStackConditions | Phase of the stored material. | [VesselConditions](#vesselconditions) | PureGas |  |  |

Back to [reference home](#reference)

### FlashResult
> Physical properties for a material generated at a particular pressure and temperature.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Pressure | Pressure. | double |  | Pressure |  [Pa] |
| Temperature | Temperature. | double |  | Temperature |  [K] |
| LiquidMoleFraction | Liquid fraction (mole). | double |  | Fraction |  [fraction] |
| LiquidDensity | Density of liquid phase. | double |  | Density |  [kg/m3] |
| VapourDensity | Density of vapour phase. | double |  | Density |  [kg/m3] |
| LiquidEntropy | Entropy of liquid phase. | double |  | Entropy |  [J/kg.K] |
| VapourEntropy | Entropy of vapour phase. | double |  | Entropy |  [J/kg.K] |
| LiquidEnthalpy | Enthalpy of liquid phase. | double |  | SpecificEnergy |  [J/kg] |
| VapourEnthalpy | Enthalpy of vapour phase. | double |  | SpecificEnergy |  [J/kg] |
| FluidPhase | Vapour, liquid or two-phase. | [Phase](#phase) | Unset |  |  |
| BubblePointPressure | Mixture bubble point pressure at given temperature. | double |  | Pressure |  [Pa] |
| BubblePointTemperature | Mixture bubble point temperature at given pressure. | double |  | Temperature |  [K] |
| DewPointPressure | Mixture dew point pressure at given temperature. | double |  | Pressure |  [Pa] |
| DewPointTemperature | Mixture dew point temperature at given pressure. | double |  | Temperature |  [K] |
| TotalFluidDensity | Total fluid density (mass-based). | double |  | Density |  [kg/m3] |
| LiquidMassFraction | Liquid mass fraction. | double |  | Fraction |  [fraction] |

Back to [reference home](#reference)

### Interval
> A range of permitted values for the design variable when carrying out a design optimization workflow.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| LowerBoundary | The lower boundary of the interval. | double |  |  |  |
| UpperBoundary | The upper boundary of the interval. | double |  |  |  |

Back to [reference home](#reference)

### Leak
> Leak scenario.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| HoleDiameter | Diameter of the hole. | double |  | Length |  [m] |
| HoleHeightFraction | Location of the hole above the base of the vessel as a fraction of vessel height. | double | 0.5 | Fraction |  [fraction] |

Back to [reference home](#reference)

### LineRupture
> Line rupture scenario.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| PipeDiameter | Internal diameter of the short pipe. | double |  | Length |  [m] |
| PipeLength | Length of the short pipe. | double |  | Length |  [m] |
| PipeRoughness | Roughness of the short pipe. | double | 0.000045 | Length |  [m] |
| PipeHeightFraction | Location of the pipe connection above the base of the vessel. | double | 0.5 | Fraction |  [fraction] |

Back to [reference home](#reference)

### LocalPosition
> Position with reference to some arbitrary local origin and axes.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| X | X. | double | 0 | Length |  [m] |
| Y | Y. | double | 0 | Length |  [m] |
| Z | Z. | double | 0 | Length |  [m] |

Back to [reference home](#reference)

### Material
> Material.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Name | Material name. | string |  |  |  |
| ComponentCount | Number of components in the material. | int | 1 |  |  |
| Components | Constituent components. | [MaterialComponent](#materialcomponent) |  |  |  |
| PropertyTemplate | Property used template for material. | [PropertyTemplate](#propertytemplate) | PhastMC |  |  |

Back to [reference home](#reference)

### MaterialComponent
> Constituent component of a material.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Name | Name of the component. | string |  |  |  |
| MoleFraction | Mole fraction of the component in the material. | double | 1 | Fraction |  [fraction] |

Back to [reference home](#reference)

### MaterialComponentData
> Material component data.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Name | Name of the material component data. | string |  |  |  |
| DipprVersion | DIPPR version number. | int |  |  |  |
| CasId | CAS id. | int |  |  |  |
| DataItem | List of data items defining the material component data. | [MaterialComponentDataItem](#materialcomponentdataitem) |  |  |  |

Back to [reference home](#reference)

### MaterialComponentDataItem
> Material component data item.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Description | Material component data item description. | string |  |  |  |
| EquationNumber | Equation number. | int |  |  |  |
| EquationString | Equation string. | string |  |  |  |
| EquationCoefficients | Equation coefficients. | double |  |  |  |
| CalculationLimits | Calculation limits. | double |  |  |  |
| SupercriticalExtrapolation | Super critical extrapolation flag. | double | 0 |  |  |
| FractionTc | Fraction of critical temperature. | double | 1 |  |  |

Back to [reference home](#reference)

### MixtureConstantPropertiesResult
> Mixture constant properties.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| LowerFlammabilityLimit | Description of new property. | double |  | Fraction |  [fraction] |
| UpperFlammabilityLimit | Description of new property. | double |  | Fraction |  [fraction] |
| CriticalPressure | Critical pressure. | double |  | Pressure |  [Pa] |
| CriticalTemperature | Critical temperature. | double |  | Temperature |  [K] |
| FlammableToxicFlag | Flammable or toxic flag. | [FlammableToxic](#flammabletoxic) | Inert |  |  |
| FlashPoint | Flash point. | double |  | Temperature |  [K] |
| HeatCombustion | Heat of combustion. | double |  |  |  |
| MaximumBurnRate | Maximum burn rate. | double |  |  |  |
| MaximumSEP | Maximum surface emissive power. | double |  |  |  |
| MolecularWeight | Molecular weight. | double |  | MolecularWeight |  [kg/kmol] |
| BubblePoint | Bubble point at atmospheric pressure. | double |  | Temperature |  [K] |
| PoolFireBurnRateLength | Pool fire burn rate length. | double |  | Length |  [m] |
| LuminousSmokyFlame | Luminous or smoky flame. | [LuminousSmokyFlame](#luminoussmokyflame) | General |  |  |
| DewPoint | Dew point at atmospheric pressure. | double |  | Temperature |  [K] |
| EmissivePowerLengthScale | Emissive power length scale. | double |  | Length |  [m] |
| LaminarBurningVelocity | Laminar burning velocity of mixture. | double |  | Velocity |  [m/s] |

Back to [reference home](#reference)

### Pipe
> All pipe types.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Nodes | Pipeline nodes. | [LocalPosition](#localposition) |  |  |  |
| NodeCount | Number of nodes. | int |  |  |  |
| Diameter | Pipe diameter. | double |  | Length |  [m] |
| Roughness | Pipe roughness. | double | 4.5e-5 | Length |  [m] |
| Material | Material. | [Material](#material) |  |  |  |
| State | Fluid state. | [State](#state) |  |  |  |
| PumpedInflow | Upstream pumped inflow. | double | 0 | MassFlowRate |  [kg/s] |

Back to [reference home](#reference)

### PipeBreach
> Breach in a long pipe (runs GSPP / PBRK).

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| DistanceDownstream | Distance downstream. | double |  | Length |  [m] |
| RelativeAperture | Breach relative aperture. | double | 1 | Fraction |  [fraction] |

Back to [reference home](#reference)

### PoolFireFlameResult
> Pool fire flame result.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| PoolZoneSEP | Surface emissive power from each of the two pool fire zones. | double |  | RadiationIntensity |  [W/m2] |

Back to [reference home](#reference)

### PoolRecord
> Pool results at a given time.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Time | Time since rainout. | double |  | Time |  [s] |
| MassSpilt | Mass spilled. | double |  | Mass |  [kg] |
| MassVaporised | Mass vaporised. | double |  | Mass |  [kg] |
| MassDissolved | Mass dissolved. | double |  | Mass |  [kg] |
| MassRemaining | Mass remaining. | double |  | Mass |  [kg] |
| VapourisationRate | Vapourisation rate. | double |  | MassFlowRate |  [kg/s] |
| SolutionRate | Solution rate. | double |  | MassFlowRate |  [kg/s] |
| EffectiveRadius | Effective radius. | double |  | Length |  [m] |
| Depth | Pool depth. | double |  | Length |  [m] |
| Temperature | Pool temperature. | double |  | Temperature |  [K] |
| SpillRate | Spill rate. | double |  | MassFlowRate |  [kg/s] |
| ActualRadius | Actual pool radius. | double |  | Length |  [m] |
| PoolCentre | Pool centre. | double |  | Length |  [m] |

Back to [reference home](#reference)

### PoolVapourisationParameters
> Pool vapourisation parameters.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ToxicsCutoffRate | Cutoff rate for toxic materials. | double | 0.001 | MassFlowRate |  [kg/s] |
| FlammableCutoffRate | Cutoff rate for flammable materials. | double | 0.1 | MassFlowRate |  [kg/s] |
| RelativeTolerance | Relative tolerance. | double | 0.001 | Fraction |  [fraction] |

Back to [reference home](#reference)

### PropertiesDipprPT1
> Properties DIPPR part 1.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| TotalStepsUsed | Description of new property. | int |  |  |  |
| Pressure | Array of pressure values. | double |  | Pressure |  [Pa] |
| Temperature | Array of temperatures. | double |  | Temperature |  [K] |
| MassComp | Mass of the composition. | double |  |  |  |
| MWComp | Description of new property. | double |  |  |  |
| DangerousToxicLoad | Dangerous Toxic Load. | double |  |  |  |
| PCrit | Critical pressure . | double |  | Pressure |  [Pa] |
| TCrit | Description of new property. | double |  | Temperature |  [K] |
| TMelt | Melting point. | double |  | Temperature |  [K] |
| TBoil | Boiling point. | double |  | Temperature |  [K] |
| TFlash | Flash point. | double |  | Temperature |  [K] |
| HComb | Heat of combustion. | double |  |  |  |
| LFL | Lower flammability limit - vol%. | double |  |  |  |
| UFL | upper flammability limit. | double |  |  |  |
| CombAt | Combustion coefficient At. | double |  |  |  |
| CombCt | Combustion coefficient Ct. | double |  |  |  |

Back to [reference home](#reference)

### PropertiesDipprPT2
> Properties DIPPR part 2.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| IgnitionCategory | Ignotion category. | double |  |  |  |
| LamBurnVelocity | Laminar burn velocity. | double |  | Velocity |  [m/s] |
| RhoLiqSat | Saturated liquid density. | double |  |  |  |
| PVap | Vapour pressure. | double |  |  |  |
| CpIdeal | Ideal gas heat capacity. | double |  |  |  |
| CpLiq | Liquid heat capacity. | double |  |  |  |
| CpRatio | Ratio of specific heat capacities. | double |  |  |  |
| Virial2 | Second virial coefficient. | double |  |  |  |
| MuVap | Vapour viscosity. | double |  |  |  |
| MuLiq | Liquid viscosity. | double |  |  |  |
| KVap | Vapour thermal conductivity. | double |  |  |  |
| KLiq | Liquid thermal conductivity. | double |  |  |  |
| HeatVap | Heat of vaporisation. | double |  |  |  |
| HVapIdeal | Ideal gas enthalpy. | double |  |  |  |
| HLiqSat | Saturated liquid enthalpy. | double |  |  |  |

Back to [reference home](#reference)

### PropertiesDipprPT3
> Properties DIPPR part 3.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| SVapSat | Saturated vapour entropy. | double |  |  |  |
| SLiqSat | Saturated liquid entropy. | double |  |  |  |
| RhoVapSat | Saturated vapour density. | double |  |  |  |
| HVapSat | Saturated vapour enthalpy. | double |  |  |  |
| RhoVapAtm | Vapour density at 1 atm. | double |  |  |  |
| TVapSat | Saturated vapour temperature. | double |  | Temperature |  [K] |
| SurfaceTension | Surface tension. | double |  |  |  |
| RhoLiq | Liquid density. | double |  |  |  |
| HLiq | Liquid enthalpy. | double |  |  |  |
| SLiq | Liquid entropy. | double |  |  |  |
| RhoVap | Vapour density. | double |  |  |  |
| HVap | Vapour enthalpy. | double |  |  |  |
| SVap | Vapour entropy. | double |  |  |  |
| ZVap | Vapour compressibility. | double |  |  |  |
| SonicVelVap | Vapour sonic velocity. | double |  |  |  |

Back to [reference home](#reference)

### PropertiesDnvPT1
> Properties DNV part 1.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| TotalStepsUsed | Total PT steps. | int |  |  |  |
| Pressure | Pressure. | double |  | Pressure |  [Pa] |
| Temperature | Temperature. | double |  | Temperature |  [K] |
| MassComp | Composition. | double |  |  |  |
| FlamTox |  Flammable/toxic flag. | double |  |  |  |
| LumSmoky | Luminous smoky flame flag. | double |  |  |  |
| SepMax | Maximum surface emissive power. | double |  |  |  |
| SepLength | Emissive power length scale. | double |  |  |  |
| PoolFireBurnRate | Pool fire burn rate length. | double |  | Length |  [m] |
| BurnRateMax | Maximum burn rate. | double |  |  |  |
| TNTEfficiency | TNT explosion efficiency. | double |  |  |  |
| ERPG1 | ERPG1 concentration. | double |  |  |  |
| ERPG2 | ERPG2 concentration. | double |  |  |  |
| ERPG3 | ERPG3 concentration. | double |  |  |  |
| IDLH | IDLH concentration. | double |  |  |  |
| STEL | STEL concentration. | double |  |  |  |

Back to [reference home](#reference)

### PropertiesDnvPT2
> Properties DNV part 2.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ToxicN | Toxic property N. | double |  |  |  |
| ToxicA | Toxic property A. | double |  |  |  |
| ToxicB | Toxic property B. | double |  |  |  |
| HIntRange | Enthalpy interpolation range. | double |  | Temperature |  [K] |
| LiqWaterSurfTen | Liquid water surface tension. | double |  |  |  |
| SolubilityWater | Solubility in water. | double |  |  |  |
| HeatSolution | Heat of solution. | double |  |  |  |
| WaterReactionFlag | Reaction with water flag. | double |  |  |  |
| AlphaWater | Water heat transfer coefficient. | double |  |  |  |
| ProbDelayedExpCont | Probability of delayed explosion (continuous). | double |  |  |  |
| ProbDelayedExpInst | Probability of delayed explosion (instantaneous & QI). | double |  |  |  |
| ProbDelayedFlashFireCont | Probability of delayed flash fire (continuous). | double |  |  |  |
| ProbDelayedFlashFireInst | Probability of delayed flash fire (instantaneous & QI). | double |  |  |  |
| ProbDelayedIgnition | Probability of delayed ignition (cont., inst. & QI). | double |  |  |  |
| ProbEarlyIgnitionCont | Probability of early ignition (continuous). | double |  |  |  |

Back to [reference home](#reference)

### PropertiesDnvPT3
> Properties DNV part 3.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ProbEarlyIgnitionInst | Probability of early ignition (instantaneous & QI). | double |  |  |  |
| ProbEarlyPoolFire | Probability of early pool fire. | double |  |  |  |
| ProbFireball | Probability of fireball. | double |  |  |  |
| ProbFreeJetExp | Probability of free jet explosion. | double |  |  |  |
| ProbFreeJetFire | Probability of free jet fire. | double |  |  |  |
| ProbLatePoolFire | Probability of late pool fire. | double |  |  |  |
| DimerCoeff | Dimer coefficient. | double |  |  |  |
| TrimerCoeff | Trimer coefficient. | double |  |  |  |
| HexamerCoeff | Hexamer coefficient. | double |  |  |  |
| OctamerCoeff | Octamer coefficient. | double |  |  |  |
| HLiqWater | Liquid water enthalpy . | double |  |  |  |
| PVapSatLn | Natural log of the saturated vap. pressure. | double |  |  |  |
| DPVapSatLnDT | First derivative of the natural log of sat.vap.pres. w.r.t. temp. | double |  |  |  |
| D2PVapSatLnDT2 | Second der. of the natural log. of sat.vap.pres. w.r.t. temp. | double |  |  |  |

Back to [reference home](#reference)

### PTRange
> Range of pressure and temperature.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| PressureLow | Start value of pressure range. | double |  | Pressure |  [Pa] |
| PressureHigh | End value of pressure range. | double |  | Pressure |  [Pa] |
| TempLow | Start value of temperature range. | double |  | Temperature |  [K] |
| TempHigh | End value of temperature range. | double |  | Temperature |  [K] |
| StepsPerVariable | Description of new property. | int | 20 |  |  |

Back to [reference home](#reference)

### RadiationRecord
> Radiation type and level at specific point (x,y,z).

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Position | Cartesian coordinates of a specific point. | [LocalPosition](#localposition) |  |  |  |
| RadiationType | Type of radiation result. | [RadiationType](#radiationtype) | Unset |  |  |
| RadiationResult | Radiation level. | double |  |  |  |

Back to [reference home](#reference)

### ReliefValve
> Relief valve scenario.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ReliefValveConstrictionDiameter | Constriction at the upstream end of the pipe. | double |  | Length |  [m] |
| PipeDiameter | Internal diameter of the short pipe. | double |  | Length |  [m] |
| PipeLength | Length of the short pipe. | double |  | Length |  [m] |
| PipeRoughness | Roughness of the short pipe. | double | 0.000045 | Length |  [m] |
| PipeHeightFraction | Location of the pipe connection above the base of the vessel. | double | 0.5 | Fraction |  [fraction] |

Back to [reference home](#reference)

### ScalarUdmOutputs
> Scalar UDM output values required for post processing dispersion results.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ObserverCount | Number of observers. | int |  |  |  |
| RecordCount | Number of records. | int |  |  |  |
| CloudType | Cloud type. | [DynamicType](#dynamictype) | Unset |  |  |
| MinimumConcentration | Minimum concentration. | double |  | Fraction |  [fraction] |
| WindPower | Wind power. | double |  |  |  |
| FrictionVelocity | Friction velocity. | double |  | Velocity |  [m/s] |
| DispersionReleaseDuration | When is the last release observer released?. | double |  | Time |  [s] |

Back to [reference home](#reference)

### ShortPipeRupture
> Short pipe rupture scenario.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| PipeLength | Length of short pipe. | double |  | Length |  [m] |
| PipeDiameter | Inner diameter of the short pipe. | double |  | Length |  [m] |
| PipeRoughness | Roughness of the short pipe. | double | 0.000045 | Length |  [m] |
| PipeHeightFraction | Location of the pipe connection above the base of the vessel. | double | 0.5 | Fraction |  [fraction] |

Back to [reference home](#reference)

### State
> Description of the fluid state.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Pressure | Absolute pressure of the fluid. | double |  | Pressure |  [Pa] |
| Temperature | Temperature of the fluid. | double |  | Temperature |  [K] |
| LiquidFraction | Mole fraction of liquid in the fluid. | double |  | Fraction |  [fraction] |
| FlashFlag | How fluid equilibrium is specified. | [FluidSpec](#fluidspec) | TP |  |  |
| MixtureModelling | Mixture modelling: Pseudo-component (=0), MC single aerosol (=1), MC multiple aerosol (=3). | [MixtureModelling](#mixturemodelling) | PC |  |  |

Back to [reference home](#reference)

### Structure
> A building or process plant structure.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| ExplosionConfinedVolume | Explosion confined volume. | [ExplosionConfinedVolume](#explosionconfinedvolume) |  |  |  |
| Location | Location of the structure. | [LocalPosition](#localposition) | LocalPosition() |  |  |

Back to [reference home](#reference)

### Substrate
> The ground over which a release is taking place.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| SurfaceRoughness | Surface roughness length. | double | 0.183 | Length |  [m] |
| SurfaceType | Dispersing surface type. | [SurfaceType](#surfacetype) | Land |  |  |
| PoolSurfaceType | Pool or bund surface type. | [PoolSurfaceType](#poolsurfacetype) | Concrete |  |  |
| Bund | Bund data. | [Bund](#bund) | Bund() |  |  |

Back to [reference home](#reference)

### ThermoPathRecord
> Contains a point on the thermodynamic depressurization trajectory for each of isothermal, isentropic and isenthalpic assumptions.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Pressure | Absolute pressure value at specific point on the thermodynamic path. | double |  | Pressure |  [Pa] |
| BubbleTemperature | Bubble point temperature at given pressure. | double |  | Temperature |  [K] |
| DewTemperature | Dew point temperature at given pressure. | double |  | Temperature |  [K] |
| IsentropicTemperature | Temperature at given pressure following isentropic depressurization. | double |  | Temperature |  [K] |
| IsenthalpicTemperature | Temperature at given pressure following isenthalpic depressurization. | double |  | Temperature |  [K] |
| IsothermalTemperature | Temperature at given pressure following isothermal depressurization. | double |  | Temperature |  [K] |

Back to [reference home](#reference)

### ToxicRecord
> Toxic result: dose, probit or lethality.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Position | Cartesian coordinates of a specific point. | [LocalPosition](#localposition) |  |  |  |
| ToxicResultType | Type of toxic result. | [ToxicResultType](#toxicresulttype) | Unset |  |  |
| ToxicResult | Dose, probit or lethality level. | double |  |  |  |

Back to [reference home](#reference)

### Transect
> Definition of transect (line segment).

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| TransectStartPoint | Cartesian coordinates of start point of transect. | [LocalPosition](#localposition) | LocalPosition() |  |  |
| TransectEndPoint | Cartesian coordinates of end point of transect. | [LocalPosition](#localposition) | LocalPosition() |  |  |

Back to [reference home](#reference)

### Vessel
> All vessel types.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| State | Fluid specification (at liquid surface). | [State](#state) |  |  |  |
| Diameter | Internal diameter of the vessel. | double | 2 | Length |  [m] |
| Height | Internal height of the vessel. | double | 4 | Length |  [m] |
| Length | Internal length of the vessel. | double | 4 | Length |  [m] |
| Width | Internal width of the vessel. | double | 0.0 | Length |  [m] |
| Shape | Shape. | [VesselShape](#vesselshape) | HorizontalCylinder |  |  |
| Material | Material. | [Material](#material) |  |  |  |
| VesselConditions | Vessel conditions. | [VesselConditions](#vesselconditions) | Unset |  |  |
| LiquidFillFractionByVolume | The liquid fill fraction in the vessel by volume. | double | 0.0 | Fraction |  [fraction] |

Back to [reference home](#reference)

### VesselLeakMaxFlammableCloudResults
> Results for a linked run of vessel leak followed by dispersion and views from the cloud.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| DischargeRate | Leak discharge mass rate. | double |  | MassFlowRate |  [kg/s] |
| ExpandedTemperature | Post atmospheric expansion temperature. | double |  | Temperature |  [K] |
| Phase | Post atmospheric expansion fluid phase. | [Phase](#phase) | Unset |  |  |
| LFLExtent | Maximum downwind distance to LFL. | double |  | Length |  [m] |
| LFLArea | Horizontal area within LFL envelope. | double |  | Area |  [m2] |
| LFLHeight | Height of maximum LFL extent. | double |  | Length |  [m] |

Back to [reference home](#reference)

### VesselRuleSet
> Rule set for generating scenarios from a vessel.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| UseTimeVarying | Use time-varying leaks. | bool | false |  |  |
| IncludeCatastrophicRupture | Include catastrophic rupture scenarios. | bool | false |  |  |
| HoleDiameters | Hole diameters for leaks. | double |  | Length |  [m] |
| NumberOfDiameters | Number of hole diameters (<= 5). | int | 3 |  |  |

Back to [reference home](#reference)

### VesselSphere
> Vessel sphere.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| State | The thermodynamic state of the fluid. | [State](#state) |  |  |  |
| Material | Material. | [Material](#material) |  |  |  |
| MassInventory | Mass inventory. | double |  | Mass |  [kg] |

Back to [reference home](#reference)

### Weather
> A sum of the meteorological conditions at the time.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| WindSpeed | Wind speed at reference height. | double | 5 | Velocity |  [m/s] |
| StabilityClass | Stability class. | [AtmosphericStabilityClass](#atmosphericstabilityclass) | StabilityD |  |  |
| Temperature | Ambient temperature. | double | 283 | Temperature |  [K] |
| RelativeHumidity | Relative humidity. | double | 0.7 | Fraction |  [fraction] |
| MixingLayerHeight | Mixing layer height. | double | 800 | Length |  [m] |
| SolarRadiation | Solar radiation flux. | double | 500 | RadiationIntensity |  [W/m2] |

Back to [reference home](#reference)

### WeatherStationData
> Compiled data from weather live service.

#### Properties
| Name | Description | Type | Default | Unit class | SI Unit |
| --- | --- | --- | ---: | :--- | ---: |
| Latitude | Latitude measured in degrees. | double | 0.0 | Angle |  [Radians] |
| Longitude | Longitude coordinate in degrees. | double | 0.0 | Angle |  [Radians] |
| DayNightOption | Indicates if it is day or night. | [DayNight](#daynight) | Unset |  |  |
| Cloudiness | Cloud coverage in percentage. | double |  |  |  |
| WindSpeed | Wind speed at reference height. | double |  | Velocity |  [m/s] |
| Temperature | Ambient temperature. | double |  | Temperature |  [K] |
| RelativeHumidity | Relative humidity. | double |  | Fraction |  [fraction] |
| SolarRadiation | Solar radiation flux. | double | 500 | RadiationIntensity |  [W/m2] |

Back to [reference home](#reference)

### Calculations
The following is a list of the available calculations.

* [ConcentrationAtPoint](#concentrationatpoint)
* [ConvertCompositionMassToMole](#convertcompositionmasstomole)
* [ConvertCompositionMoleToMass](#convertcompositionmoletomass)
* [Dispersion](#dispersion)
* [DistancesAndEllipsesToRadiationLevels](#distancesandellipsestoradiationlevels)
* [DistancesAndEllipsesToRadiationLevelsForPoolFires](#distancesandellipsestoradiationlevelsforpoolfires)
* [DistancesAndFootprintsToConcentrationLevels](#distancesandfootprintstoconcentrationlevels)
* [DistancesToConcLevels](#distancestoconclevels)
* [DistancesToRadiationLevels](#distancestoradiationlevels)
* [DistanceToRadiation](#distancetoradiation)
* [Fireball](#fireball)
* [FlareStackDesigner](#flarestackdesigner)
* [Flash](#flash)
* [GetMassFromVessel](#getmassfromvessel)
* [JetFire](#jetfire)
* [LateExplosion](#lateexplosion)
* [LateExplosionToOPLevels](#lateexplosiontooplevels)
* [LethalityDistance](#lethalitydistance)
* [LoadMassInventoryVesselForLeakScenario](#loadmassinventoryvesselforleakscenario)
* [LoadMassInventoryVesselForLineRuptureScenario](#loadmassinventoryvesselforlinerupturescenario)
* [LoadMassInventoryVesselForReliefValveScenario](#loadmassinventoryvesselforreliefvalvescenario)
* [LongPipeBreach](#longpipebreach)
* [MaxConcDistance](#maxconcdistance)
* [MaxConcFootprint](#maxconcfootprint)
* [MaxDistanceToConc](#maxdistancetoconc)
* [MixtureConstantProperties](#mixtureconstantproperties)
* [PoolFire](#poolfire)
* [RadiationAtAPoint](#radiationatapoint)
* [RadiationAtAPointForPoolFires](#radiationatapointforpoolfires)
* [RadiationAtPoints](#radiationatpoints)
* [RadiationAtPointsForPoolFires](#radiationatpointsforpoolfires)
* [RadiationContour](#radiationcontour)
* [RadiationTransect](#radiationtransect)
* [RadiationTransectForPoolFires](#radiationtransectforpoolfires)
* [ReliefValveMinTemperature](#reliefvalvemintemperature)
* [SetMixingLayerHeight](#setmixinglayerheight)
* [SetPhaseToReleaseForLeakScenario](#setphasetoreleaseforleakscenario)
* [SetPhaseToReleaseForLineRuptureScenario](#setphasetoreleaseforlinerupturescenario)
* [SetPhaseToReleaseForReliefValveScenario](#setphasetoreleaseforreliefvalvescenario)
* [SetReleaseElevationForScenario](#setreleaseelevationforscenario)
* [SideviewAtTime](#sideviewattime)
* [TankFire](#tankfire)
* [UDSSetLiqFracFromTemperature](#udssetliqfracfromtemperature)
* [UDSSetTemperatureFromLiqFrac](#udssettemperaturefromliqfrac)
* [UDSTemperatureLimits](#udstemperaturelimits)
* [UserDefinedSourceLinkedRun](#userdefinedsourcelinkedrun)
* [VesselCatastrophicRupture](#vesselcatastrophicrupture)
* [VesselLeak](#vesselleak)
* [VesselLeakFlammableLinkedRun](#vesselleakflammablelinkedrun)
* [VesselLeakFlammableLinkedRunH2](#vesselleakflammablelinkedrunh2)
* [VesselLeakFlamToxSimpleLinkedRun](#vesselleakflamtoxsimplelinkedrun)
* [VesselLeakLinkedRun](#vesselleaklinkedrun)
* [VesselLeakMaxFlammableCloud](#vesselleakmaxflammablecloud)
* [VesselLineRupture](#vessellinerupture)
* [VesselLineRuptureLinkedRun](#vessellinerupturelinkedrun)
* [VesselReliefValve](#vesselreliefvalve)
* [VesselReliefValveLinkedRun](#vesselreliefvalvelinkedrun)
* [VesselState](#vesselstate)

### ConcentrationAtPoint
> Calculate the concentration at a specified point in time.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfig | Dispersion view configuration. | [DispersionOutputConfig](#dispersionoutputconfig) |
| Material | Material with post-discharge composition. | [Material](#material) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Concentration | Concentration at a position of interest. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### ConvertCompositionMassToMole
> Converts mixture composition from mass to mole basis.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Mixture | Mixture to have composition converted. | [Material](#material) |
| CompositionMass | Input composition of mixture in mass basis. | double |
| CompositionMassCount | Number of components in mixture. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| CompositionMole | Output composition of mixture in mole basis. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### ConvertCompositionMoleToMass
> Converts mixture composition from mole to mass basis.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Mixture | Mixture to have composition converted. | [Material](#material) |
| CompositionMoles | Input composition of mixture in mole basis. | double |
| CompositionMolesCount | Number of components in mixture. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| CompositionMass | Output composition of mixture in mass basis. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### Dispersion
> Outdoor dispersion calculations.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DischargeResult | Discharge / source term definition. | [DischargeResult](#dischargeresult) |
| DischargeRecords | Discharge / source term definition. | [DischargeRecord](#dischargerecord) |
| DischargeRecordCount | Number of discharge records. | int |
| Weather | Weather. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| WriteDispersionRecordCallback | Array of Dispersion records. | [DispersionRecord](#dispersionrecord) |
| WritePoolRecordCallback | Array of Pool records. | [PoolRecord](#poolrecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### DistancesAndEllipsesToRadiationLevels
> Distances and ellipses to prescribed radiation intensity levels.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfigs | Settings of radiation calculations. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Distances | Distances to radiation levels. | double |
| WriteContourPointCallback | Contour points of radiation ellipses to radiation levels. | [LocalPosition](#localposition) |
| NContourPoints | Number of contour points per radiation level. | int |
| Areas | Area of the ellipse to radiation levels. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### DistancesAndEllipsesToRadiationLevelsForPoolFires
> Distances and ellipses to prescribed radiation intensity levels for pool fires.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PoolFireFlameResult | Scalar pool fire flame results. | [PoolFireFlameResult](#poolfireflameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfigs | Settings of radiation calculations. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Distances | Distances to radiation levels. | double |
| WriteContourPointCallback | Contour points of radiation ellipses to radiation levels. | [LocalPosition](#localposition) |
| NContourPoints | Number of contour points per radiation level. | int |
| Areas | Area of the ellipse to radiation levels. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### DistancesAndFootprintsToConcentrationLevels
> Distances and maximum footprints to prescribed concentration of interest levels.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs (i.e. one per scenario/weather). | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfigs | Dispersion view configurations. | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionOutputConfigCount | Number of dispersion view configurations. | int |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| Material | Material with post-discharge composition. | [Material](#material) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ConcsUsed | Concentrations of interest. | double |
| NContourPoints | Number of contour points per concentration level. | int |
| AreasContour | Areas of footprint contours. | double |
| DistancesConcentration | Maximum distances downwind per concentration level. | double |
| WriteContourPointCallback | Contour points of maximum footprints to concentration level. | [LocalPosition](#localposition) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### DistancesToConcLevels
> Calculates the maximum distance to a number of concentration levels.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfigs | Concentration levels. | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionOutputConfigCount | Number of concentration levels. | int |
| Material | Material with post-discharge composition. | [Material](#material) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ConcUsed | Concentrations of interest. | double |
| Distances | Distances to concentration of interest. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### DistancesToRadiationLevels
> Distances to prescribed radiation intensity levels.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfigs | Flammable output configurations. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of flammable output configurations. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Distances | Distances to radiation level. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### DistanceToRadiation
> Distance to radiation calculation.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Settings of flammable contours view. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Distance | Distance to radiation level. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### Fireball
> Fireball calculation.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| State | The thermodynamic conditions. | [State](#state) |
| DischargeRecords | Discharge / source term definition. | [DischargeRecord](#dischargerecord) |
| DischargeRecordCount | Number of discharge records. | int |
| DischargeResult | Discharge / source term definition. | [DischargeResult](#dischargeresult) |
| Weather | Weather. | [Weather](#weather) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Flame scalar result. | [FlameResult](#flameresult) |
| WriteFlameRecordCallback | Array of fireball flame records. | [FlameRecord](#flamerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### FlareStackDesigner
> Flare stack designer application.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlareStack | Flare stack asset. | [FlareStack](#flarestack) |
| FlareStackConstraint | Data that defines the design requirements. | [Constraint](#constraint) |
| Weather | Weather. | [Weather](#weather) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | Substrate data. | [Substrate](#substrate) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Defines the flammable results of interest. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DesignSolution | Value of design variable that satisfies the design target. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### Flash
> Generates properties for a material at specific input fluid conditions.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | User-defined input material, pure component or mixture (max 20 components). | [Material](#material) |
| MaterialState | Describes the fluid pressure, temperature, liquid fraction. | [State](#state) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| FlashResult | Fluid properties at given conditions. | [FlashResult](#flashresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### GetMassFromVessel
> Calculates the mass in a vessel.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel (pressurised). | [Vessel](#vessel) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| MassInventory | Mass inventory in the vessel (kg). | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### JetFire
> Cone jet fire calculations.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| DischargeRecords | Discharge / source term definition. | [DischargeRecord](#dischargerecord) |
| DischargeRecordCount | Number of discharge records. | int |
| DischargeResult | Discharge / source term definition. | [DischargeResult](#dischargeresult) |
| Weather | Weather. | [Weather](#weather) |
| Substrate | Substrate. | [Substrate](#substrate) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Flame scalar results. | [FlameResult](#flameresult) |
| WriteFlameRecordCallback | Array of jet fire flame records. | [FlameRecord](#flamerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LateExplosion
> Explosion calculations using the multi-energy method.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| ScalarUdmOutputs | Dispersion scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Cloud definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | Substrate. | [Substrate](#substrate) |
| DispersionOutputConfig | Specification of cloud view. | [DispersionOutputConfig](#dispersionoutputconfig) |
| ExplosionOutputConfig | Explosion output configuration. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExplosionUnifConfOverpressureResult | Uniform confined explosion overpressure result. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| ExplosionUnconfOverpressureResult | Unconfined explosion overpressure result. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| ResultCode | Eror code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LateExplosionToOPLevels
> Explosion calculations using the multi-energy method to multiple over-pressure levels.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| ScalarUdmOutputs | Dispersion scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Cloud definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | Substrate. | [Substrate](#substrate) |
| DispersionOutputConfig | Specification of cloud view. | [DispersionOutputConfig](#dispersionoutputconfig) |
| ExplosionOutputConfigs | Explosion output configurations. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of explosion output configurations. | int |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExplosionUnifConfOverpressureResults | Uniform confined explosion overpressure results. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| ExplosionUnconfOverpressureResults | Unconfined explosion overpressure results. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| ResultCode | Eror code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LethalityDistance
> Calculates toxic lethality vs distance.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfig | Dispersion view configuration. | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| WriteToxicRecordCallback | Array of toxic results. | [ToxicRecord](#toxicrecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LoadMassInventoryVesselForLeakScenario
> Sets up a vessel and a leak scenario from a mass inventory, pressure, temperature and hole size specifications.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Vessel material. | [Material](#material) |
| Mass | Total vessel mass inventory. | double |
| Pressure | Vessel pressure in absolute scale. | double |
| Temperature | Vessel temperature. | double |
| HoleSize | Leak hole size. | double |
| ReleaseElevation | Release elevation. | double |
| ReleaseAngle | Release angle. | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| Leak | Leak scenario. | [Leak](#leak) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LoadMassInventoryVesselForLineRuptureScenario
> Sets up a vessel and a line rupture scenario from a mass inventory, pressure, temperature, pipe diameter and length specifications.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Vessel material. | [Material](#material) |
| Mass | Total vessel mass inventory. | double |
| Pressure | Vessel pressure in absolute scale. | double |
| Temperature | Vessel temperature. | double |
| PipeDiameter | Pipe diameter. | double |
| PipeLength | Pipe length. | double |
| ReleaseElevation | Release elevation. | double |
| ReleaseAngle | Release angle. | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| LineRupture | Line rupture. | [LineRupture](#linerupture) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LoadMassInventoryVesselForReliefValveScenario
> Sets up a vessel and a relief valve scenario from a mass inventory, pressure, temperature, pipe diameter, lenght and constriction size specifications.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Vessel material. | [Material](#material) |
| Mass | Total vessel mass inventory. | double |
| Pressure | Vessel pressure in absolute scale. | double |
| Temperature | Vessel temperature. | double |
| ConstrictionSize | Constriction size. | double |
| PipeDiameter | Pipe diameter. | double |
| PipeLength | Pipe length. | double |
| ReleaseElevation | Release elevation. | double |
| ReleaseAngle | Release angle. | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| ReliefValve | Relief valve. | [ReliefValve](#reliefvalve) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### LongPipeBreach
> Release from a breach in a long pipeline.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Pipe | Pipe equipment item. | [Pipe](#pipe) |
| PipeBreach | Long pipeline scenario. | [PipeBreach](#pipebreach) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExitMaterial | Composition of the released material (indentical to storage composition - using PC mode). | [Material](#material) |
| DischargeResult | Scalar discharge results. | [DischargeResult](#dischargeresult) |
| WriteDischargeRecordCallback | Array of discharge records. | [DischargeRecord](#dischargerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### MaxConcDistance
> Maximum concentration vs distance for a dispersing cloud.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfig | Dispersion view configuration. | [DispersionOutputConfig](#dispersionoutputconfig) |
| Material | Material with post-discharge composition. | [Material](#material) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ConcUsed | Concentration of interest. | double |
| WriteConcentrationRecordCallback | Array of maximum concentration at x, y, z coordinates. | [ConcentrationRecord](#concentrationrecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### MaxConcFootprint
> Maximum concentration footprint to a specified concentration.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfig | Dispersion view configuration. | [DispersionOutputConfig](#dispersionoutputconfig) |
| Material | Material with post-discharge composition. | [Material](#material) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ConcUsed | Concentration of interest. | double |
| WriteContourPointCallback | Array of footprint results. | [LocalPosition](#localposition) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### MaxDistanceToConc
> Calculate the maximum distance to a specified concentration.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfig | Dispersion view configuration. | [DispersionOutputConfig](#dispersionoutputconfig) |
| Material | Material with post-discharge composition. | [Material](#material) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ConcUsed | Concentration of interest. | double |
| Distance | Maximum distance to concentration of interest. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### MixtureConstantProperties
> Generates constant properties for a mixture.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | User-defined input material (max 20 components). | [Material](#material) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| MixConstantPropResult | Constant properties of the mixture. | [MixtureConstantPropertiesResult](#mixtureconstantpropertiesresult) |
| ResultCode | Response code. | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### PoolFire
> Pool fire calculations.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material with post-discharge composition. | [Material](#material) |
| PoolRecords | Pool / source term definition. | [PoolRecord](#poolrecord) |
| PoolRecordCount | Number of pool records. | int |
| Weather | Weather. | [Weather](#weather) |
| Substrate | Substrate. | [Substrate](#substrate) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| PoolFireFlameResult | Flame scalar result. | [PoolFireFlameResult](#poolfireflameresult) |
| WriteFlameRecordCallback | Array of pool fire flame records. | [FlameRecord](#flamerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationAtAPoint
> Radiation at a point calculations for flammable models.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Settings of flammable contours view. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Radiation | Radiation at a point. | double |
| ResultCode | Response code. | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationAtAPointForPoolFires
> Radiation at a point calculations for pool fires.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PoolFireFlameResult | Scalar flame results. | [PoolFireFlameResult](#poolfireflameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Settings of flammable contours view. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Radiation | Radiation at a point. | double |
| ResultCode | Response code. | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationAtPoints
> Radiation at point calculations for flammable models.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfigs | Settings for radiation coordinates. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation coordinates. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Radiation | Array of radiation at a point. | double |
| ResultCode | Response code. | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationAtPointsForPoolFires
> Radiation at point calculations for pool fires.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PoolFireFlameResult | Scalar flame results. | [PoolFireFlameResult](#poolfireflameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfigs | Settings for radiation coordinates. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation coordinates. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Radiation | Array of radiation at a point. | double |
| ResultCode | Response code. | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationContour
> Radiation contour calculations.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Settings of flammable contours view. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| WriteContourPointCallback | Array of contour points. | [LocalPosition](#localposition) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationTransect
> Radiation transect calculations.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| FlameResult | Scalar flame results. | [FlameResult](#flameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Settings of flammable contours view. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| WriteRadiationRecordCallback | Array of radiation results along transect. | [RadiationRecord](#radiationrecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### RadiationTransectForPoolFires
> Radiation transect calculations for pool fires.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PoolFireFlameResult | Pool fire flame results. | [PoolFireFlameResult](#poolfireflameresult) |
| FlameRecords | Flame definition. | [FlameRecord](#flamerecord) |
| FlameRecordCount | Number of flame records. | int |
| Weather | Weather. | [Weather](#weather) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |
| FlammableOutputConfig | Settings of flammable contours view. | [FlammableOutputConfig](#flammableoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| WriteRadiationRecordCallback | Array of radiation results along transect. | [RadiationRecord](#radiationrecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### ReliefValveMinTemperature
> Calculates minimum allowed input temperature for the Phast Online Relief Valve app.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material. | [Material](#material) |
| Pressure | Input pressure (absolute) at which to evaluate bubble point temperature. | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| MinTemperature | Calculated lower temperature limit for relief valve scenario. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### SetMixingLayerHeight
> Sets the mixing layer height according to the stability class, based on default weather parameters from Phast.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Weather | Weather data. | [Weather](#weather) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| UpdatedWeather | Updated weather data. | [Weather](#weather) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### SetPhaseToReleaseForLeakScenario
> Calculates the hole height fraction and vessel z coordinate to release the requested phase (vapour or liquid).

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PhaseToRelease | Requested fluid phase to release. | [Phase](#phase) |
| ReleaseElevation | Release point elevation above ground. | double |
| Vessel | Vessel definition input. | [Vessel](#vessel) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ZCoordUpdated | Updated z-coordinate of vessel to accommodate requested phase to release. | double |
| HoleHeightFractionUpdated | Updated hole height fraction to accommodate requested phase to release. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### SetPhaseToReleaseForLineRuptureScenario
> Calculates the pipe height fraction and vessel z coordinate to release the requested phase (vapour or liquid).

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PhaseToRelease | Requested fluid phase to release. | [Phase](#phase) |
| ReleaseElevation | Release point elevation above ground. | double |
| Vessel | Vessel definition input. | [Vessel](#vessel) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ZCoordUpdated | Updated z-coordinate of vessel to accommodate requested phase to release. | double |
| PipeHeightFractionUpdated | Updated pipe height fraction to accommodate requested phase to release. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### SetPhaseToReleaseForReliefValveScenario
> Calculates the pipe height fraction and vessel z coordinate to release the requested phase.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| PhaseToRelease | Requested fluid phase to release. | [Phase](#phase) |
| ReleaseElevation | Release point elevation above ground. | double |
| Vessel | Vessel definition input. | [Vessel](#vessel) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ZCoordUpdated | Updated z-coordinate of vessel to accommodate requested phase to release. | double |
| PipeHeightFractionUpdated | Updated pipe height fraction to accommodate requested phase to release. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### SetReleaseElevationForScenario
> Calculates the vessel z coordinate to release at the requested elevation. This method sets the vessel defined by its dimensions and shape to be elevated at a particular height such as to guarantee that the discharge result height is at the requested elevation.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ReleaseElevation | Release point elevation above ground. | double |
| ReleaseHeightFraction | Release height fraction off the total vessel height. | double |
| Vessel | Vessel definition input. | [Vessel](#vessel) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| UpdatedVessel | Updated vessel definition output with modified z coordinate. | [Vessel](#vessel) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### SideviewAtTime
> Cloud sideview at a given concentration level and time of interest.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| ScalarUdmOutputs | UDM scalar outputs. | [ScalarUdmOutputs](#scalarudmoutputs) |
| Weather | Weather. | [Weather](#weather) |
| DispersionRecords | Dispersion definition. | [DispersionRecord](#dispersionrecord) |
| DispersionRecordCount | Number of dispersion records. | int |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DispersionOutputConfig | Dispersion view configuration. | [DispersionOutputConfig](#dispersionoutputconfig) |
| Material | Material with post-discharge composition. | [Material](#material) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ConcUsed | Concentration of interest. | double |
| WriteContourPointCallback | Array of sideview results. | [LocalPosition](#localposition) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### TankFire
> Tank fire model.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| AtmosphericStorageTank | Atmospheric storage tank. | [AtmosphericStorageTank](#atmosphericstoragetank) |
| Weather | Weather. | [Weather](#weather) |
| Substrate | Substrate. | [Substrate](#substrate) |
| FlammableParameters | Flammable parameters. | [FlammableParameters](#flammableparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| PoolFireFlameResult | Flame scalar result. | [PoolFireFlameResult](#poolfireflameresult) |
| WriteFlameRecordCallback | Pool fire flame records. | [FlameRecord](#flamerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### UDSSetLiqFracFromTemperature
> Sets the liquid fraction for a given temperature.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material. | [Material](#material) |
| PhaseToBeReleased | Phase to be released (should be Two-Phase, if not this method simply returns). | [Phase](#phase) |
| Temperature | Input temperature. | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| LiquidFraction | Calculated liquid fraction. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### UDSSetTemperatureFromLiqFrac
> Sets the temperature for a given liquid fraction.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material. | [Material](#material) |
| PhaseToBeReleased | Phase to be released (should be Two-Phase, if not this method simply returns). | [Phase](#phase) |
| LiquidFraction | Input liquid fraction. | double |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| Temperature | Calculated temperature. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### UDSTemperatureLimits
> Calculates valid temperature range for a material for a given fluid phase.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material. | [Material](#material) |
| PhaseToBeReleased | Phase to be released (Vapour, Two-phase or Liquid). | [Phase](#phase) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| MinTemperature | Lower temperature limit to ensure consistency. | double |
| MaxTemperature | Upper temperature limit to ensure consistency. | double |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### UserDefinedSourceLinkedRun
> Calculates maximum distance to a number of concentration, radiation and overpressure levels for flammable.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | Material. | [Material](#material) |
| DischargeResult | Scalar discharge data. | [DischargeResult](#dischargeresult) |
| DischargeRecords | Discharge records. | [DischargeRecord](#dischargerecord) |
| DischargeRecordCount | Number of discharge records. | int |
| PhaseToBeReleased | Phase to be released (Vapour, Two-phase or Liquid). | [Phase](#phase) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionParameterCount | Number of dispersion parameters. | int |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionFlamOutputConfigs | Flammable concentration levels (LFL fraction, LFL, UFL). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionFlamOutputConfigCount | Number of flammable concentration levels (LFL fraction, LFL, UFL). | int |
| DispersionToxicOutputConfigs | Toxic concentration levels (concentration of interest). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionToxicOutputConfigCount | Number of toxic concentration levels (concentration of interest). | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Callback function for jet fire radiation contour points. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of points for jet fire contours per radiation level. | int |
| AreaContourJet | Areas of jet fire contours. | double |
| DistancesToFlamConcentration | Distances to concentration levels (LFL fraction, LFL and UFL). | double |
| FlamConcentrationsUsed | Concentration levels (LFL fraction, LFL and UFL). | double |
| WriteFlamConcContourPointCallback | Maximum concentration footprints at given concentration levels (LFL fraction, LFL and UFL). | [LocalPosition](#localposition) |
| NFlamConcContourPoints | Number of contour points per concentration level (LFL fraction, LFL and UFL). | int |
| AreaFootprintFlamConc | Areas of maximum concentration footprints (LFL fraction, LFL and UFL). | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Callback function for pool fire radiation contour points. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of points for pool fire contours per radiation level. | int |
| AreaContourPool | Areas of pool fire contours. | double |
| ExplosionOverpressureResults | Explosion results to overpressure levels. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| DistancesToToxicConcentration | Distance to concentration of interest (using toxic averaging time). | double |
| ToxicConcentrationUsed | Concentration of interest. | double |
| WriteToxicConcContourPointCallback | Maximum concentration footprint to concentration of interest (using toxic averaging time). | [LocalPosition](#localposition) |
| NToxicConcContourPoints | Number of contour points for maximum concentration footprint to concentration of interest. | int |
| AreaFootprintToxicConc | Area of maximum concentration footprints to concentration of interest (using toxic averaging time). | double |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselCatastrophicRupture
> Catastrophic rupture from a vessel.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel (pressurised or atmospheric). | [Vessel](#vessel) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExitMaterial | Composition of the released material (indentical to storage composition). | [Material](#material) |
| DischargeResult | Scalar discharge results. | [DischargeResult](#dischargeresult) |
| WriteDischargeRecordCallback | Array of discharge record. | [DischargeRecord](#dischargerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLeak
> Leak calculations from a vessel.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel (pressurised or atmospheric). | [Vessel](#vessel) |
| Leak | Leak failure case. | [Leak](#leak) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExitMaterial | Composition of the released material (may differ from storage composition). | [Material](#material) |
| DischargeResult | Scalar discharge results. | [DischargeResult](#dischargeresult) |
| WriteDischargeRecordCallback | Array of discharge records. | [DischargeRecord](#dischargerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLeakFlammableLinkedRun
> Calculates maximum distance to a number of concentration, radiation and overpressure levels.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| Leak | Leak scenario. | [Leak](#leak) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionOutputConfigs | Concentration levels. | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionOutputConfigCount | Number of concentration levels. | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DischargeRecord | Discharge data for table. | [DischargeRecord](#dischargerecord) |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Ellipses to jet fire radiation levels. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of contour points for jet fire ellipses per radiation level. | int |
| AreaEllipseJet | Areas of jet fire ellipses. | double |
| DistancesToConcentration | Distances to concentration levels. | double |
| ConcentrationsUsed | Concentration levels. | double |
| WriteConcContourPointCallback | Maximum concentration footprints at given concentration levels. | [LocalPosition](#localposition) |
| NConcContourPoints | Number of contour points per concentration level. | int |
| AreaFootprintConc | Areas of maximum concentration footprints. | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Ellipses to pool fire radiation levels. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of contour points for pool fire ellipses per radiation level. | int |
| AreaEllipsePool | Areas of pool fire ellipses. | double |
| ExplosionOverpressureResults | Explosion overpressure results. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLeakFlammableLinkedRunH2
> VesselLeakFlammableLinkedRun for hydrogen.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| Leak | Leak scenario. | [Leak](#leak) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionParameterCount | Number of dispersion parameters. | int |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionOutputConfigs | Concentration levels. | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionOutputConfigCount | Number of concentration levels. | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DischargeRecord | Discharge data for table. | [DischargeRecord](#dischargerecord) |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Callback function for jet fire radiation contour points. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of points for jet fire contours per radiation level. | int |
| AreaEllipseJet | Areas of jet fire contours. | double |
| DistancesToConcentration | Distances to concentration levels. | double |
| ConcentrationsUsed | Concentration levels. | double |
| WriteConcContourPointCallback | Maximum concentration footprints at given concentration levels. | [LocalPosition](#localposition) |
| NConcContourPoints | Number of contour points per concentration level. | int |
| AreaFootprintConc | Areas of maximum concentration footprints. | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Callback function for pool fire radiation contour points. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of points for pool fire contours per radiation level. | int |
| AreaEllipsePool | Areas of pool fire contours. | double |
| ExplosionOverpressureResults | Explosion results to overpressure levels. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLeakFlamToxSimpleLinkedRun
> Calculates maximum distance to a number of concentration, radiation and overpressure levels for flammable.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| Leak | Leak scenario. | [Leak](#leak) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionParameterCount | Number of dispersion parameters. | int |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionFlamOutputConfigs | Flammable concentration levels (LFL fraction, LFL, UFL). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionFlamOutputConfigCount | Number of flammable concentration levels (LFL fraction, LFL, UFL). | int |
| MoleFractionToxic | Mole fraction of toxic component. | double |
| DispersionToxicOutputConfigs | Toxic concentration levels (concentration of interest). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionToxicOutputConfigCount | Number of toxic concentration levels (concentration of interest). | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DischargeRecord | Discharge data for table. | [DischargeRecord](#dischargerecord) |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Callback function for jet fire radiation contour points. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of points for jet fire contours per radiation level. | int |
| AreaEllipseJet | Areas of jet fire contours. | double |
| DistancesToFlamConcentration | Distances to concentration levels (LFL fraction, LFL and UFL). | double |
| FlamConcentrationsUsed | Concentration levels (LFL fraction, LFL and UFL). | double |
| WriteFlamConcContourPointCallback | Maximum concentration footprints at given concentration levels (LFL fraction, LFL and UFL). | [LocalPosition](#localposition) |
| NFlamConcContourPoints | Number of contour points per concentration level (LFL fraction, LFL and UFL). | int |
| AreaFootprintFlamConc | Areas of maximum concentration footprints (LFL fraction, LFL and UFL). | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Callback function for pool fire radiation contour points. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of points for pool fire contours per radiation level. | int |
| AreaEllipsePool | Areas of pool fire contours. | double |
| ExplosionOverpressureResults | Explosion results to overpressure levels. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| DistancesToToxicConcentration | Distance to concentration of interest (using toxic averaging time). | double |
| ToxicConcentrationUsed | Concentration of interest. | double |
| WriteToxicConcContourPointCallback | Maximum concentration footprint to concentration of interest (using toxic averaging time). | [LocalPosition](#localposition) |
| NToxicConcContourPoints | Number of contour points for maximum concentration footprint to concentration of interest. | int |
| AreaFootprintToxicConc | Area of maximum concentration footprints to concentration of interest (using toxic averaging time). | double |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLeakLinkedRun
> Calculates maximum distance to a number of concentration, radiation and overpressure levels for flammable.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| Leak | Leak scenario. | [Leak](#leak) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionParameterCount | Number of dispersion parameters. | int |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionFlamOutputConfigs | Flammable concentration levels (LFL fraction, LFL, UFL). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionFlamOutputConfigCount | Number of flammable concentration levels (LFL fraction, LFL, UFL). | int |
| DispersionToxicOutputConfigs | Toxic concentration levels (concentration of interest). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionToxicOutputConfigCount | Number of toxic concentration levels (concentration of interest). | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DischargeRecord | Discharge data for table. | [DischargeRecord](#dischargerecord) |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Callback function for jet fire radiation contour points. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of points for jet fire contours per radiation level. | int |
| AreaEllipseJet | Areas of jet fire contours. | double |
| DistancesToFlamConcentration | Distances to concentration levels (LFL fraction, LFL and UFL). | double |
| FlamConcentrationsUsed | Concentration levels (LFL fraction, LFL and UFL). | double |
| WriteFlamConcContourPointCallback | Maximum concentration footprints at given concentration levels (LFL fraction, LFL and UFL). | [LocalPosition](#localposition) |
| NFlamConcContourPoints | Number of contour points per concentration level (LFL fraction, LFL and UFL). | int |
| AreaFootprintFlamConc | Areas of maximum concentration footprints (LFL fraction, LFL and UFL). | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Callback function for pool fire radiation contour points. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of points for pool fire contours per radiation level. | int |
| AreaEllipsePool | Areas of pool fire contours. | double |
| ExplosionOverpressureResults | Explosion results to overpressure levels. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| DistancesToToxicConcentration | Distance to concentration of interest (using toxic averaging time). | double |
| ToxicConcentrationUsed | Concentration of interest. | double |
| WriteToxicConcContourPointCallback | Maximum concentration footprint to concentration of interest (using toxic averaging time). | [LocalPosition](#localposition) |
| NToxicConcContourPoints | Number of contour points for maximum concentration footprint to concentration of interest. | int |
| AreaFootprintToxicConc | Area of maximum concentration footprints to concentration of interest (using toxic averaging time). | double |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLeakMaxFlammableCloud
> Linked vessel leak followed, dispersion, and calculation of flammable extents.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel (pressurised or atmospheric). | [Vessel](#vessel) |
| Leak | Leak failure case. | [Leak](#leak) |
| Weather | Weather. | [Weather](#weather) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionOutputConfig | Options for controlling dispersion results (here used to set height of interest only). | [DispersionOutputConfig](#dispersionoutputconfig) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| VesselLeakMaxFlammableCloudResults | Collated discharge and flammable cloud characterisation results. | [VesselLeakMaxFlammableCloudResults](#vesselleakmaxflammablecloudresults) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLineRupture
> Calculations of discharge from a short pipe attached to a vessel.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel (pressurised or atmospheric). | [Vessel](#vessel) |
| LineRupture | Line rupture scenario. | [LineRupture](#linerupture) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExitMaterial | Composition of the released material (may differ from storage composition). | [Material](#material) |
| DischargeResult | Scalar discharge results. | [DischargeResult](#dischargeresult) |
| WriteDischargeRecordCallback | Array of discharge records. | [DischargeRecord](#dischargerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselLineRuptureLinkedRun
> Calculates maximum distance to a number of concentration, radiation and overpressure levels for flammable.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| LineRupture | Line rupture. | [LineRupture](#linerupture) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionParameterCount | Number of dispersion parameters. | int |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionFlamOutputConfigs | Flammable concentration levels (LFL fraction, LFL, UFL). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionFlamOutputConfigCount | Number of flammable concentration levels (LFL fraction, LFL, UFL). | int |
| DispersionToxicOutputConfigs | Toxic concentration levels (concentration of interest). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionToxicOutputConfigCount | Number of toxic concentration levels (concentration of interest). | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DischargeRecord | Discharge data for table. | [DischargeRecord](#dischargerecord) |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Callback function for jet fire radiation contour points. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of points for jet fire contours per radiation level. | int |
| AreaContourJet | Areas of jet fire contours. | double |
| DistancesToFlamConcentration | Distances to concentration levels (LFL fraction, LFL and UFL). | double |
| FlamConcentrationsUsed | Concentration levels (LFL fraction, LFL and UFL). | double |
| WriteFlamConcContourPointCallback | Maximum concentration footprints at given concentration levels (LFL fraction, LFL and UFL). | [LocalPosition](#localposition) |
| NFlamConcContourPoints | Number of contour points per concentration level (LFL fraction, LFL and UFL). | int |
| AreaFootprintFlamConc | Areas of maximum concentration footprints (LFL fraction, LFL and UFL). | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Callback function for pool fire radiation contour points. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of points for pool fire contours per radiation level. | int |
| AreaContourPool | Areas of pool fire contours. | double |
| ExplosionOverpressureResults | Explosion overpressure results. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| DistancesToToxicConcentration | Distance to concentration of interest (using toxic averaging time). | double |
| ToxicConcentrationUsed | Concentration of interest. | double |
| WriteToxicConcContourPointCallback | Maximum concentration footprint to concentration of interest (using toxic averaging time). | [LocalPosition](#localposition) |
| NToxicConcContourPoints | Number of contour points for maximum concentration footprint to concentration of interest. | int |
| AreaFootprintToxicConc | Area of maximum concentration footprints to concentration of interest (using toxic averaging time). | double |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselReliefValve
> Calculations of venting from a relief valve attached to a vessel.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel (pressurised or atmospheric). | [Vessel](#vessel) |
| ReliefValve | Relief valve scenario. | [ReliefValve](#reliefvalve) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| ExitMaterial | Composition of the released material (may differ from storage composition). | [Material](#material) |
| DischargeResult | Scalar discharge results. | [DischargeResult](#dischargeresult) |
| WriteDischargeRecordCallback | Array of discharge records. | [DischargeRecord](#dischargerecord) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselReliefValveLinkedRun
> Calculates maximum distance to a number of concentration, radiation and overpressure levels for flammable.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Vessel | Vessel definition. | [Vessel](#vessel) |
| ReliefValve | Relief valve. | [ReliefValve](#reliefvalve) |
| DischargeParameters | Discharge parameters. | [DischargeParameters](#dischargeparameters) |
| Substrate | The dispersing surface. | [Substrate](#substrate) |
| Weather | Weather definition. | [Weather](#weather) |
| DispersionParameters | Dispersion parameters. | [DispersionParameters](#dispersionparameters) |
| DispersionParameterCount | Number of dispersion parameters. | int |
| EndPointConcentration | Concentration at which the dispersion calculations will terminate (v/v fraction). | double |
| FlammableParameters | Fire model parameters. | [FlammableParameters](#flammableparameters) |
| ExplosionParameters | Explosion parameters. | [ExplosionParameters](#explosionparameters) |
| DispersionFlamOutputConfigs | Flammable concentration levels (LFL fraction, LFL, UFL). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionFlamOutputConfigCount | Number of flammable concentration levels (LFL fraction, LFL, UFL). | int |
| DispersionToxicOutputConfigs | Toxic concentration levels (concentration of interest). | [DispersionOutputConfig](#dispersionoutputconfig) |
| DispersionToxicOutputConfigCount | Number of toxic concentration levels (concentration of interest). | int |
| FlammableOutputConfigs | Radiation levels. | [FlammableOutputConfig](#flammableoutputconfig) |
| FlammableOutputConfigCount | Number of radiation levels. | int |
| ExplosionOutputConfigs | Overpressure levels. | [ExplosionOutputConfig](#explosionoutputconfig) |
| ExplosionOutputConfigCount | Number of overpressure levels. | int |
| ExplosionConfinedVolumes | Explosion confined volumes. | [ExplosionConfinedVolume](#explosionconfinedvolume) |
| ExplosionConfinedVolumeCount | Number of confined explosion sources. | int |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| DischargeRecord | Discharge data for table. | [DischargeRecord](#dischargerecord) |
| DistancesToJetFireRadiation | Distances to jet fire radiation levels. | double |
| WriteJetContourPointCallback | Callback function for jet fire radiation contour points. | [LocalPosition](#localposition) |
| NJetContourPoints | Number of points for jet fire contours per radiation level. | int |
| AreaContourJet | Areas of jet fire contours. | double |
| DistancesToFlamConcentration | Distances to concentration levels (LFL fraction, LFL and UFL). | double |
| FlamConcentrationsUsed | Concentration levels (LFL fraction, LFL and UFL). | double |
| WriteFlamConcContourPointCallback | Maximum concentration footprints at given concentration levels (LFL fraction, LFL and UFL). | [LocalPosition](#localposition) |
| NFlamConcContourPoints | Number of contour points per concentration level (LFL fraction, LFL and UFL). | int |
| AreaFootprintFlamConc | Areas of maximum concentration footprints (LFL fraction, LFL and UFL). | double |
| DistancesToPoolFireRadiation | Distances to pool fire radiation levels. | double |
| WritePoolContourPointCallback | Callback function for pool fire radiation contour points. | [LocalPosition](#localposition) |
| NPoolContourPoints | Number of points for pool fire contours per radiation level. | int |
| AreaContourPool | Areas of pool fire contours. | double |
| ExplosionOverpressureResults | Explosion overpressure results. | [ExplosionOverpressureResult](#explosionoverpressureresult) |
| DistancesToToxicConcentration | Distance to concentration of interest (using toxic averaging time). | double |
| ToxicConcentrationUsed | Concentration of interest. | double |
| WriteToxicConcContourPointCallback | Maximum concentration footprint to concentration of interest (using toxic averaging time). | [LocalPosition](#localposition) |
| NToxicConcContourPoints | Number of contour points for maximum concentration footprint to concentration of interest. | int |
| AreaFootprintToxicConc | Area of maximum concentration footprints to concentration of interest (using toxic averaging time). | double |
| JetFireFlameResult | Flame results for jet fire. | [FlameResult](#flameresult) |
| PoolFireFlameResult | Flame results for pool fire. | [PoolFireFlameResult](#poolfireflameresult) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)
### VesselState
> Calculates the fluid storage state for a material and thermodynamic conditions.

***Input data***

| Name | Description | Type |
| --- | --- | --- |
| Material | User-defined input material, pure component or mixture (max 20 components). | [Material](#material) |
| MaterialState | Describes the fluid pressure, temperature, liquid fraction. | [State](#state) |

***Output data***

| Name | Description | Type |
| --- | --- | --- |
| VesselConditions | Describes the vessel storage conditions (Pure gas, Stratified Two-Phase or Pressurised liquid). | [VesselConditions](#vesselconditions) |
| OutputState | Describes the fluid pressure, temperature and liquid fraction after the flash calculation. | [State](#state) |
| ResultCode | Error code (0 = OK, < 0 data input error, > 0 execution error). | [ResultCode](#resultcode) |

Back to [reference home](#reference)