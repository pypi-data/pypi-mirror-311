from dataclasses import dataclass, field
import luminarycloud.params.enum as enum


@dataclass(kw_only=True)
class SpalartAllmarasTurbulenceSpecification:
    """Specification for Spalart-Allmaras turbulence."""

    method: enum.TurbulenceSpecificationSpalartAllmaras = (
        enum.TurbulenceSpecificationSpalartAllmaras.TURBULENT_VISCOSITY_RATIO_SA
    )
    "Method for specifying turbulence."
    viscosity: float = 3.765582173541416e-06
    "Turbulent viscosity."
    viscosity_ratio: float = 0.21043825715555026
    "Turbulent-to-laminar viscosity ratio."
    uniform_nu_tilde: float = 4.166705541552236e-05
    "Uniform value of the turbulent viscosity."


@dataclass(kw_only=True)
class KOmegaTurbulenceSpecification:
    """Specification for K-omega turbulence."""

    method: enum.TurbulenceSpecificationKomega = (
        enum.TurbulenceSpecificationKomega.BC_TURBULENT_VISCOSITY_RATIO_AND_INTENSITY_KOMEGA
    )
    "Method for specifying turbulence."
    intensity: float = 0.05
    "Turbulence intensity."
    viscosity: float = 3.765582173541416e-06
    "Turbulent viscosity."
    viscosity_ratio: float = 0.21043825715555026
    "Turbulent-to-laminar viscosity ratio."
    uniform_tke: float = 4.166705541552236e-05
    "Uniform value of the turbulent kinetic energy."
    uniform_omega: float = 4.166705541552236e-05
    "Uniform value of the specific dissipation rate."


@dataclass(kw_only=True)
class TurbulenceSpecification:
    """Specification for turbulence."""

    spalart_allmaras: SpalartAllmarasTurbulenceSpecification = field(
        default_factory=SpalartAllmarasTurbulenceSpecification
    )
    "Specification for Spalart-Allmaras turbulence."
    komega: KOmegaTurbulenceSpecification = field(default_factory=KOmegaTurbulenceSpecification)
    "Specification for k-omega turbulence."
