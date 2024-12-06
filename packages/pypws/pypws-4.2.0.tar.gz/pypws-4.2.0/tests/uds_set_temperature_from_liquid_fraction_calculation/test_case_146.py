import os
import pathlib
import sys
import pytest

# When running locally the environment variable PYPWS_RUN_LOCALLY needs to be set to True.
# Check if the environment variable is set
PYPWS_RUN_LOCALLY = os.getenv('PYPWS_RUN_LOCALLY')
if PYPWS_RUN_LOCALLY and PYPWS_RUN_LOCALLY.lower() == 'true':
    # Navigate to the PYPWS directory by searching upwards until it is found.
    current_dir = pathlib.Path(__file__).resolve()

    while current_dir.name.lower() != 'package':
        if current_dir.parent == current_dir:  # Check if the current directory is the root directory
            raise FileNotFoundError("The 'pypws' directory was not found in the path hierarchy.")
        current_dir = current_dir.parent

    # Insert the path to the pypws package into sys.path.
    sys.path.insert(0, f'{current_dir}')


# from pypws.calculations import UDSSetTemperatureFromLiqFracCalculation
from pypws.entities import Material, MaterialComponent
from pypws.enums import Phase, ResultCode

@pytest.mark.skip(reason="Skipping this test unconditionally")
def test_case_147():
    
    """
    Test for UDS set temperature from liq frac calculation with the following inputs
    
    Material = "METHANE+EHTANE+PROPANE"
    Phase = "TWO-PHASE"
    Liquid fraction = 0.1
    
    """
    
    # Define the material
    material = Material(
		name="",
		components=[
			MaterialComponent(
				name="PROPANE",
				mole_fraction=0.6
			),
            MaterialComponent(
				name="METHANE",
				mole_fraction=0.1
			),
            MaterialComponent(
				name="ETHANE",
				mole_fraction=0.3
			)
		],
        component_count = 3
	)
    
    # Define the phase
    phase = Phase.TWO_PHASE
    
    # Define the liquid fraction
    liquid_fraction = 0.1

    # Create a uds set temperature from liq frac calculation.
    uds_set_temperature_from_liq_frac_calculation = UDSSetTemperatureFromLiqFracCalculation(material = material, phase_to_be_released = phase, liquid_fraction = liquid_fraction)
    
    # Run the calculation
    print ('Running uds_set_temperature_from_liq_frac_calculation')
    result_code = uds_set_temperature_from_liq_frac_calculation.run()
    
    # Print any messages.
    if len(uds_set_temperature_from_liq_frac_calculation.messages) > 0:
        print('Messages:')
        for message in uds_set_temperature_from_liq_frac_calculation.messages:
            print(message)

    if result_code == ResultCode.SUCCESS:
        print(f'SUCCESS: uds_set_temperature_from_liq_frac_calculation ({uds_set_temperature_from_liq_frac_calculation.calculation_elapsed_time}ms)')
    else:
        assert False, f'FAILED uds_set_temperature_from_liq_frac_calculation with result code {result_code}'