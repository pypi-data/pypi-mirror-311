import os
import pathlib
import sys

run_locally = os.getenv('PYPWS_RUN_LOCALLY')
if run_locally and run_locally.lower() == 'true':
    # Navigate to the PYPWS directory by searching upwards until it is found.
    current_dir = pathlib.Path(__file__).resolve()

    while current_dir.name.lower() != 'package':
        if current_dir.parent == current_dir:  # Check if the current directory is the root directory
            raise FileNotFoundError("The 'pypws' directory was not found in the path hierarchy.")
        current_dir = current_dir.parent

    # Insert the path to the pypws package into sys.path.
    sys.path.insert(0, f'{current_dir}')

from pypws.calculations import LoadMassInventoryVesselForLineRuptureScenarioCalculation
from pypws.entities import Material, MaterialComponent, State
from pypws.enums import ResultCode


def test_case_128():
	
	material = Material("N-HEXANE", [MaterialComponent("N-HEXANE", 1.0)], component_count = 1)
	

	# Create a load mass inventory vessel for line rupture scenario calculation using the material.
	load_mass_inventory_vessel_for_line_rupture_scenario_calculation = LoadMassInventoryVesselForLineRuptureScenarioCalculation(material = material, temperature = 250, pressure = float(7e5), mass = float(9876), pipe_length = 33.0, pipe_diameter = 0.1, release_elevation = 1.0, release_angle = 1.1)

	# Run the calculation
	print('Running load_mass_inventory_vessel_for_line_rupture_scenario_calculation...')
	resultCode = load_mass_inventory_vessel_for_line_rupture_scenario_calculation.run()

	# Print any messages.
	if len(load_mass_inventory_vessel_for_line_rupture_scenario_calculation.messages) > 0:
		print('Messages:')
		for message in load_mass_inventory_vessel_for_line_rupture_scenario_calculation.messages:
			print(message)

	if resultCode == ResultCode.SUCCESS:
		print(f'SUCCESS: load_mass_inventory_vessel_for_line_rupture_scenario_calculation ({load_mass_inventory_vessel_for_line_rupture_scenario_calculation.calculation_elapsed_time}ms)')
	else:
		assert False, f'FAILED load_mass_inventory_vessel_for_line_rupture_scenario_calculation with result code {resultCode}'
    
