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


# from pypws.calculations import (
#     UDSSetLiqFracFromTemperatureCalculation,
#     UDSSetTemperatureFromLiqFracCalculation,
# )

from pypws.entities import Material, MaterialComponent
from pypws.enums import Phase, ResultCode

@pytest.mark.skip(reason="Skipping this test unconditionally")
def test_case_145():
    
    """
    Test for UDS set liq frac from temperature calculation with the following inputs
    
    Material = "N-PENTANE+N-HEXANE"
    Phase = "TWO-PHASE"
    Temperature = 311.43
    
    """
    
    # Define the material
    material = Material(
		name="N-PENTANE+N-HEXANE",
		components=[
			MaterialComponent(
				name="N-PENTANE",
				mole_fraction=0.9
			),
            MaterialComponent(
				name="N-HEXANE",
				mole_fraction=0.1
			)
		],
        component_count = 2
	)
    
    # Define the phase
    phase = Phase.TWO_PHASE
    
    # Define the temperature
    temperature = 311.43

    # Create a uds set liq frac from temperature calculation.
    uds_set_liq_frac_from_temperature_calculation = UDSSetLiqFracFromTemperatureCalculation(material = material, phase_to_be_released = phase, temperature = temperature)
    
    # Run the calculation
    print ('Running uds_set_liq_frac_from_temperature_calculation')
    result_code = uds_set_liq_frac_from_temperature_calculation.run()
    
    # Print any messages.
    if len(uds_set_liq_frac_from_temperature_calculation.messages) > 0:
        print('Messages:')
        for message in uds_set_liq_frac_from_temperature_calculation.messages:
            print(message)

    if result_code == ResultCode.SUCCESS:
        print(f'SUCCESS: uds_set_liq_frac_from_temperature_calculation ({uds_set_liq_frac_from_temperature_calculation.calculation_elapsed_time}ms)')
    else:
        assert False, f'FAILED uds_set_liq_frac_from_temperature_calculation with result code {result_code}'