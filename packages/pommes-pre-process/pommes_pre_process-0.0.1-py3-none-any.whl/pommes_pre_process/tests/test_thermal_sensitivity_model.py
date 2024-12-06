from pommes_pre_process.src.utilities import (
    read_csv_dataset,
    save_xarray_into_csv_file,
    create_demand_xarray,
)

from pommes_pre_process.src.temperature import (
    create_temperature_xarray,
    convert_temperature_xarray_to_export_format,
)

from pommes_pre_process.src.thermal_sensitivity_model import (
    create_thermal_sensitivity_xarray,
    decompose_demand_with_thermal_sensitivity,
)


def test_extract_thermal_sensitivity_part_of_demand():
    temperature_df = read_csv_dataset("areas_temperatures.csv")
    demand_df = read_csv_dataset("demand.csv")

    temperature_xr = create_temperature_xarray(temperature_df)
    temperature_xr = convert_temperature_xarray_to_export_format(temperature_xr)
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitive_demand = create_thermal_sensitivity_xarray(
        temperature_xr, demand_xr, 15
    )

    print(thermal_sensitive_demand)
    save_xarray_into_csv_file(thermal_sensitive_demand, "test.csv")


def test_decompose_demand_with_thermal_sensitivity():
    temperature_df = read_csv_dataset("areas_temperatures.csv")
    demand_df = read_csv_dataset("demand.csv")

    temperature_xr = convert_temperature_xarray_to_export_format(
        create_temperature_xarray(temperature_df)
    )
    demand_xr = create_demand_xarray(demand_df)

    thermal_sensitive_demand_xr = create_thermal_sensitivity_xarray(
        temperature_xr, demand_xr, 15
    )

    decomposed_demand_xr = decompose_demand_with_thermal_sensitivity(
        demand_xr, thermal_sensitive_demand_xr
    )

    print(decomposed_demand_xr)

    save_xarray_into_csv_file(decomposed_demand_xr, "decomposed_demand.csv")
