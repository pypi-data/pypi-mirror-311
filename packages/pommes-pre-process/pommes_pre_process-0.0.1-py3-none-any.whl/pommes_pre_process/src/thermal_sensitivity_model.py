# thermal_sensitivity_model.py

import xarray as xr

from pommes_pre_process.src.utilities import (
    create_empty_xarray_dataset,
    add_dataarray_to_dataset,
)

# --------------------------------------------------------
# Création des xarrays de demande thermosensible et decomposée
# --------------------------------------------------------


def create_thermal_sensitivity_xarray(
    temperature_xr: xr.DataArray, demand_xr: xr.DataArray, temperature_threshold: float
) -> xr.DataArray:
    """
    Extrait la partie thermique de la demande en fonction d'un seuil de température.
    :param temperature_xr: DataArray contenant les températures par zone et par heure
    :param demand_xr: DataArray contenant les demandes d'énergie par zone, ressource et heure
    :param temperature_threshold: Seuil de température pour calculer la demande thermique
    :return: DataArray contenant la thermosensibilité en fonction de la région
    """
    # Vérifier que 'resource' est une coordonnée
    if "resource" not in demand_xr.coords:
        raise KeyError(
            "La coordonnée 'resource' est absente de la demande (demand_xr)."
        )

    # Identifier les dates où la température est sous le seuil
    cold_condition = temperature_xr <= temperature_threshold

    # Calculer la sensibilité thermique globale ou par dimension temporelle
    thermal_sensitivity = compute_thermal_sensitivity(temperature_xr, demand_xr)

    # Calculer la demande thermique seulement lorsque les conditions sont satisfaites
    thermal_sensitive_demand_xr = xr.where(
        cold_condition & (demand_xr["resource"] == "electricity"),
        thermal_sensitivity * (temperature_threshold - temperature_xr),
        0,
    )

    return thermal_sensitive_demand_xr.rename("thermal_sensitive_demand")


def decompose_demand_with_thermal_sensitivity(
    demand_xr: xr.DataArray, thermal_sensitivity_demand_xr: xr.DataArray
) -> xr.Dataset:
    """
    Calcule un DataArray avec la demande non thermosensible et retourne un Dataset avec la demande totale
    et sa décomposition.
    :param demand_xr:
    :param thermal_sensitivity_demand_xr:
    :return:
    """
    non_thermal_sensitive_demand_xr = demand_xr - thermal_sensitivity_demand_xr

    non_thermal_sensitive_demand_xr = non_thermal_sensitive_demand_xr.rename(
        "non_thermal_sensitive_demand_xr"
    )

    decomposed_demand_xr = create_empty_xarray_dataset("decomposed_demand")

    for dataarray in [
        demand_xr,
        thermal_sensitivity_demand_xr,
        non_thermal_sensitive_demand_xr,
    ]:
        decomposed_demand_xr = add_dataarray_to_dataset(decomposed_demand_xr, dataarray)

    return decomposed_demand_xr


# --------------------------------------------------------
# Calcule des coefficients de thermosensibilité
# --------------------------------------------------------


def compute_thermal_sensitivity(
    temperature_xr: xr.DataArray, demand_xr: xr.DataArray
) -> xr.DataArray:
    """
    Calcule la sensibilité thermique (slope) entre la température et la demande pour chaque groupe.
    """
    return -xr.cov(temperature_xr, demand_xr) / temperature_xr.var()
