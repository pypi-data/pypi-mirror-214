import unittest
import os
import numpy as np
import yaml
from pathlib import Path

from steam_sdk.builders.BuilderLEDET import BuilderLEDET
from steam_sdk.data.DataModelMagnet import DataModelMagnet
from tests.TestHelpers import assert_two_parameters


class TestBuilderLEDET(unittest.TestCase):

    def setUp(self) -> None:
        """
            This function is executed before each test in this class
        """
        self.current_path = os.getcwd()
        os.chdir(os.path.dirname(__file__))  # move to the directory where this file is located
        print('\nCurrent folder:          {}'.format(self.current_path))
        print('\nTest is run from folder: {}'.format(os.getcwd()))

        # Define Inputs parameters that are equal to input file
        self.local_Inputs = {
            'T00': 1.9,
            'l_magnet': 7.15,
            'I00': 10e3,
            'M_m': np.arange(16).reshape(4, 4) / 57,
            'fL_I': [i * 10e3 for i in range(10)],
            'fL_L': [i / 12 + 0.01 for i in range(10)],
            'GroupToCoilSection': [1, 2, 1, 2],
            'polarities_inGroup': [+1, +1, -1, -1],
            'nT': 4 * [40],
            'nStrands_inGroup': 4 * [40],
            'l_mag_inGroup': 4 * [7.15],
            'ds_inGroup': 4 * [0.8],
            'f_SC_strand_inGroup': 4 * [0.54],
            'f_ro_eff_inGroup': 4 * [1],
            'Lp_f_inGroup': 4 * [0.019],
            'RRR_Cu_inGroup': 4 * [100],
            'SCtype_inGroup': 4 * [1],
            'STtype_inGroup': 4 * [1],
            'insulationType_inGroup': 4 * [1],
            'internalVoidsType_inGroup': 4 * [1],
            'externalVoidsType_inGroup': 4 * [1],
            'wBare_inGroup': 4 * [1],
            'hBare_inGroup': 4 * [1],
            'wIns_inGroup': 4 * [1],
            'hIns_inGroup': 4 * [1],
            'Lp_s_inGroup': 4 * [1],
            'R_c_inGroup': 4 * [1],
            'Tc0_NbTi_ht_inGroup': 4 * [1],
            'Bc2_NbTi_ht_inGroup': 4 * [1],
            'c1_Ic_NbTi_inGroup': 4 * [1],
            'c2_Ic_NbTi_inGroup': 4 * [1],
            'Tc0_Nb3Sn_inGroup': 4 * [1],
            'Bc2_Nb3Sn_inGroup': 4 * [1],
            'Jc_Nb3Sn0_inGroup': 4 * [1],
            'el_order_half_turns': list(range(1, 160 + 1)),
            'alphasDEG': 160 * [1],
            'rotation_block': 160 * [1],
            'mirror_block': 160 * [1],
            'mirrorY_block': 160 * [1],
            'iContactAlongWidth_From': 4 * [1],
            'iContactAlongWidth_To': 4 * [1],
            'iContactAlongHeight_From': 4 * [1],
            'iContactAlongHeight_To': 4 * [1],
            'iStartQuench': 4 * [1],
            'tStartQuench': 4 * [1],
            'lengthHotSpot_iStartQuench': 4 * [1],
            'fScaling_vQ_iStartQuench': 4 * [1],
            'R_circuit': 1e-3,
            'R_crowbar': 1E-3,
            'Ud_crowbar': 0.7,
            't_PC': 0,
            't_PC_LUT': [-0.02, 0, 0 + 0.01],
            'I_PC_LUT': [10e3, 10e3, 0],
            'tEE': 99999,
            'R_EE_triggered': .0125,
            'tCLIQ': 0.5e-3,
            'directionCurrentCLIQ': [1, -1],
            'nCLIQ': 1,
            'U0': 1000,
            'C': 0.04,
            'Rcapa': 0.05,
            'tQH': 8 * [0.001],
            'U0_QH': 8 * [1],
            'C_QH': 8 * [1],
            'R_warm_QH': 8 * [1],
            'w_QH': 8 * [1],
            'h_QH': 8 * [1],
            's_ins_QH': 8 * [1],
            'type_ins_QH': 8 * [2],
            's_ins_QH_He': 8 * [1],
            'type_ins_QH_He': 8 * [2],
            'l_QH': 8 * [1],
            'f_QH': 8 * [0.25],
            'iQH_toHalfTurn_From': [1 for i in range(100)],
            'iQH_toHalfTurn_To': [2 for i in range(100)],
            'tQuench': -.02,
            'initialQuenchTemp': 10,
            'HalfTurnToInductanceBlock': list(range(1, 400 + 1)),
            'M_InductanceBlock_m': np.arange(400).reshape(20, 20) / 57
        }

        # Define Options parameters that are equal to input file
        self.local_Options = {
            'time_vector_params': [-0.02, 0.0025, 0],
            'Iref': 16471,
            'flagIron': 1,
            'flagSelfField': 1,
            'headerLines': 1,
            'columnsXY': 4,
            'columnsBxBy': 6,
            'flagPlotMTF': 0,
            'flag_calculateInductanceMatrix': 0,
            'flag_useExternalInitialization': 0,
            'flag_initializeVar': 0,
            'flag_fastMode': 1,
            'flag_controlCurrent': 0,
            'flag_automaticRefinedTimeStepping': 1,
            'flag_IronSaturation': 1,
            'flag_InvertCurrentsAndFields': 0,
            'flag_ScaleDownSuperposedMagneticField': 1,
            'flag_HeCooling': 2,
            'fScaling_Pex': 1,
            'fScaling_Pex_AlongHeight': 1,
            'fScaling_MR': 1,
            'flag_scaleCoilResistance_StrandTwistPitch': 2,
            'flag_separateInsulationHeatCapacity': 0,
            'flag_ISCL': 1,
            'fScaling_Mif': 1,
            'fScaling_Mis': 1,
            'flag_StopIFCCsAfterQuench': 0,
            'flag_StopISCCsAfterQuench': 0,
            'tau_increaseRif': 0.005,
            'tau_increaseRis': 0.01,
            'fScaling_RhoSS': 1.09,
            'maxVoltagePC': 10,
            'flag_symmetricGroundingEE': 0,
            'flag_removeUc': 0,
            'BtX_background': 0,
            'BtY_background': 0,
            'flag_showFigures': 0,
            'flag_saveFigures': 0,
            'flag_saveMatFile': 1,
            'flag_saveTxtFiles': 0,
            'flag_generateReport': 1,
            'flag_hotSpotTemperatureInEachGroup': 0,
        }

        # Define Plots parameters that are equal to input file
        self.local_Plots = {
            'suffixPlot': 0,
            'typePlot': 0,
            'outputPlotSubfolderPlot': 0,
            'variableToPlotPlot': 0,
            'selectedStrandsPlot': 0,
            'selectedTimesPlot': 0,
            'labelColorBarPlot': 0,
            'minColorBarPlot': 0,
            'maxColorBarPlot': 0,
            'MinMaxXYPlot': 0,
            'flagSavePlot': 0,
            'flagColorPlot': 0,
            'flagInvisiblePlot': 0
        }

        # Define Variables parameters that are equal to input file
        self.local_Variables = {
            'variableToSaveTxt': ['time_vector', 'Ia', 'Ib'],
            'typeVariableToSaveTxt': [2, 2, 2],
            'variableToInitialize': ['Ia', 'Ib', 'T_ht']
        }

    def tearDown(self) -> None:
        """
            This function is executed after each test in this class
        """
        os.chdir(self.current_path)  # go back to initial folder

    def test_BuilderLEDET_init(self):
        """
            Check that DataLEDET object can be initialized
        """
        # arrange

        # act
        bLEDET = BuilderLEDET(flag_build=False)

        # assert
        self.assertEqual(hasattr(bLEDET, 'verbose'), True)
        self.assertEqual(hasattr(bLEDET, 'model_data'), True)
        self.assertEqual(hasattr(bLEDET, 'roxie_data'), True)

        self.assertEqual(hasattr(bLEDET, 'Inputs'), True)
        self.assertEqual(hasattr(bLEDET, 'Options'), True)
        self.assertEqual(hasattr(bLEDET, 'Plots'), True)
        self.assertEqual(hasattr(bLEDET, 'Variables'), True)
        self.assertEqual(hasattr(bLEDET, 'Auxiliary'), True)

        self.assertEqual(hasattr(bLEDET, 'descriptionsInputs'), True)
        self.assertEqual(hasattr(bLEDET, 'descriptionsOptions'), True)
        self.assertEqual(hasattr(bLEDET, 'descriptionsPlots'), True)
        self.assertEqual(hasattr(bLEDET, 'descriptionsVariables'), True)

        self.assertEqual(hasattr(bLEDET, 'smic_write_path'), True)
        self.assertEqual(hasattr(bLEDET, 'enableConductorResistanceFraction'), True)

    def test_setAttribute(self):
        """
            **Test that setAttribute works**
        """
        # arrange
        bLEDET = BuilderLEDET(flag_build=False)

        for parameter in self.local_Inputs:
            true_value = self.local_Inputs[parameter]
            setattr(bLEDET.Inputs, parameter, true_value)
            # act
            test_value = bLEDET.getAttribute('Inputs', parameter)
            # assert
            assert_two_parameters(true_value, test_value)

        for parameter in self.local_Options:
            true_value = self.local_Options[parameter]
            setattr(bLEDET.Options, parameter, true_value)
            # act
            test_value = bLEDET.getAttribute('Options', parameter)
            # assert
            assert_two_parameters(true_value, test_value)

        for parameter in self.local_Plots:
            true_value = self.local_Plots[parameter]
            setattr(bLEDET.Plots, parameter, true_value)
            # act
            test_value = bLEDET.getAttribute('Plots', parameter)
            # assert
            assert_two_parameters(true_value, test_value)

        for parameter in self.local_Variables:
            true_value = self.local_Variables[parameter]
            setattr(bLEDET.Variables, parameter, true_value)
            # act
            test_value = bLEDET.getAttribute('Variables', parameter)
            # assert
            assert_two_parameters(true_value, test_value)

    def test_getAttribute(self):
        """
            **Test getAttribute works**
        """
        # arrange
        bLEDET = BuilderLEDET(flag_build=False)

        for parameter in self.local_Inputs:
            true_value = self.local_Inputs[parameter]
            # act
            bLEDET.setAttribute('Inputs', parameter, true_value)
            test_value = getattr(bLEDET.Inputs, parameter)
            # assert
            assert_two_parameters(true_value, test_value)

        for parameter in self.local_Options:
            true_value = self.local_Options[parameter]
            # act
            bLEDET.setAttribute('Options', parameter, true_value)
            test_value = getattr(bLEDET.Options, parameter)
            # assert
            assert_two_parameters(true_value, test_value)

        for parameter in self.local_Plots:
            true_value = self.local_Plots[parameter]
            # act
            bLEDET.setAttribute('Plots', parameter, true_value)
            test_value = getattr(bLEDET.Plots, parameter)
            # assert
            assert_two_parameters(true_value, test_value)

        for parameter in self.local_Variables:
            true_value = self.local_Variables[parameter]
            # act
            bLEDET.setAttribute('Variables', parameter, true_value)
            test_value = getattr(bLEDET.Variables, parameter)
            # assert
            assert_two_parameters(true_value, test_value)

    def test_localParser(self):
        """
            **Test if the method localsParser() **
            Returns error if the local parser does not change the given parameters
            Assumes that getAttribute() works
        """
        # arrange
        bLEDET = BuilderLEDET(flag_build=False)

        # act
        bLEDET.localsParser({**self.local_Inputs, **self.local_Options, **self.local_Plots, **self.local_Variables})

        # assert
        for attribute in self.local_Inputs:
            self.assertIn(attribute, {**bLEDET.Inputs.__annotations__})

            true_value = self.local_Inputs[attribute]
            test_value = bLEDET.getAttribute('Inputs', attribute)
            assert_two_parameters(true_value, test_value)
        for attribute in self.local_Options:
            self.assertIn(attribute, {**bLEDET.Options.__annotations__})

            true_value = self.local_Options[attribute]
            test_value = bLEDET.getAttribute('Options', attribute)
            assert_two_parameters(true_value, test_value)
        for attribute in self.local_Plots:
            self.assertIn(attribute, {**bLEDET.Plots.__annotations__})

            true_value = self.local_Plots[attribute]
            test_value = bLEDET.getAttribute('Plots', attribute)
            assert_two_parameters(true_value, test_value)
        for attribute in self.local_Variables:
            self.assertIn(attribute, {**bLEDET.Variables.__annotations__})

            true_value = self.local_Variables[attribute]
            test_value = bLEDET.getAttribute('Variables', attribute)
            assert_two_parameters(true_value, test_value)

    def test_loadConductorData(self):
        """
            Test loadConductorData() method with content from modelData_MQXF_V2.yaml
        """
        # arrange
        magnet_name = 'MQXF_V2'
        file_model_data = os.path.join('model_library', 'magnets', magnet_name, 'input', 'modelData_' + magnet_name + '.yaml')
        path_magnet = Path(file_model_data).parent
        dictionary = yaml.safe_load(open(file_model_data))
        inputModelData = DataModelMagnet(**dictionary)

        bLEDET = BuilderLEDET(path_magnet=path_magnet, input_model_data=inputModelData, flag_build=False, verbose=True)

        bLEDET.translateModelDataToLEDET()
        bLEDET.loadParametersFromMap2d()

        # act
        bLEDET.loadConductorData()

        # assert

    def test_loadParametersFromMap2d(self):
        """
            Test loadParametersFromMap2d method with content from modelData_MQXF_V2.yaml
        """
        # arrange
        magnet_name = 'MQXF_V2'
        file_model_data = os.path.join('model_library','magnets', magnet_name, 'input', 'modelData_' + magnet_name + '.yaml')
        path_magnet = Path(file_model_data).parent
        dictionary = yaml.safe_load(open(file_model_data))
        input_model_data = DataModelMagnet(**dictionary)

        expected_nT = [16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5]
        expected_polarities_inGroup = [1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, -1, -1, -1, -1, 1, 1, 1, 1, -1, -1, -1, -1, 1, 1, 1, 1]

        bLEDET = BuilderLEDET(path_magnet=path_magnet, input_model_data=input_model_data, flag_build=False)
        bLEDET.translateModelDataToLEDET()

        # act
        bLEDET.loadParametersFromMap2d()

        # assert
        self.assertEqual(expected_polarities_inGroup, bLEDET.Inputs.polarities_inGroup)
        self.assertEqual(expected_nT, bLEDET.Inputs.nT)

    def test_loadParametersFromDataModel(self):
        """
            Test loadParametersFromDataModel() method with content from modelData_MQXF_V2.yaml
        """
        # arrange
        magnet_name = 'MCBRD'
        file_model_data = os.path.join('model_library', 'magnets', magnet_name, 'input', 'modelData_' + magnet_name + '.yaml')
        path_magnet = Path(file_model_data).parent
        dictionary = yaml.safe_load(open(file_model_data))
        inputModelData = DataModelMagnet(**dictionary)

        bLEDET = BuilderLEDET(path_magnet=path_magnet, input_model_data=inputModelData, flag_build=False, verbose=True)

        # act
        bLEDET.loadParametersFromDataModel()

        # assert
        self.assertEqual(inputModelData.CoilWindings.polarities_in_group, bLEDET.Inputs.polarities_inGroup)
        self.assertEqual(inputModelData.CoilWindings.n_half_turn_in_group, bLEDET.Inputs.nT)

    def test_calcElectricalOrder_manualEntries(self):
        """
            Check that calcElectricalOrder calculates correctly. The test use-case is for MQXF_V2 and the input variables are defined manually
        """
        # arrange
        el_order_half_turns_reference_MQXF_V2 = [129, 329, 130, 330, 131, 331, 132, 332, 133, 333, 134, 334, 135, 335,
                                                 136, 336, 137, 337, 138, 338, 139, 339, 140, 340, 141, 341, 142, 342,
                                                 143, 343, 144, 344, 145, 345, 146, 346, 147, 347, 148, 348, 149, 349,
                                                 150, 350, 128, 328, 127, 327, 126, 326, 125, 325, 124, 324, 123, 323,
                                                 122, 322, 121, 321, 120, 320, 119, 319, 118, 318, 117, 317, 116, 316,
                                                 115, 315, 114, 314, 113, 313, 112, 312, 111, 311, 110, 310, 109, 309,
                                                 108, 308, 107, 307, 106, 306, 105, 305, 104, 304, 103, 303, 102, 302,
                                                 101, 301, 251, 51, 252, 52, 253, 53, 254, 54, 255, 55, 256, 56, 257,
                                                 57, 258, 58, 259, 59, 260, 60, 261, 61, 262, 62, 263, 63, 264, 64, 265,
                                                 65, 266, 66, 267, 67, 268, 68, 269, 69, 270, 70, 271, 71, 272, 72, 273,
                                                 73, 274, 74, 275, 75, 276, 76, 277, 77, 278, 78, 300, 100, 299, 99,
                                                 298, 98, 297, 97, 296, 96, 295, 95, 294, 94, 293, 93, 292, 92, 291, 91,
                                                 290, 90, 289, 89, 288, 88, 287, 87, 286, 86, 285, 85, 284, 84, 283, 83,
                                                 282, 82, 281, 81, 280, 80, 279, 79, 351, 151, 352, 152, 353, 153, 354,
                                                 154, 355, 155, 356, 156, 357, 157, 358, 158, 359, 159, 360, 160, 361,
                                                 161, 362, 162, 363, 163, 364, 164, 365, 165, 366, 166, 367, 167, 368,
                                                 168, 369, 169, 370, 170, 371, 171, 372, 172, 373, 173, 374, 174, 375,
                                                 175, 376, 176, 377, 177, 378, 178, 400, 200, 399, 199, 398, 198, 397,
                                                 197, 396, 196, 395, 195, 394, 194, 393, 193, 392, 192, 391, 191, 390,
                                                 190, 389, 189, 388, 188, 387, 187, 386, 186, 385, 185, 384, 184, 383,
                                                 183, 382, 182, 381, 181, 380, 180, 379, 179, 29, 229, 30, 230, 31, 231,
                                                 32, 232, 33, 233, 34, 234, 35, 235, 36, 236, 37, 237, 38, 238, 39, 239,
                                                 40, 240, 41, 241, 42, 242, 43, 243, 44, 244, 45, 245, 46, 246, 47, 247,
                                                 48, 248, 49, 249, 50, 250, 28, 228, 27, 227, 26, 226, 25, 225, 24, 224,
                                                 23, 223, 22, 222, 21, 221, 20, 220, 19, 219, 18, 218, 17, 217, 16, 216,
                                                 15, 215, 14, 214, 13, 213, 12, 212, 11, 211, 10, 210, 9, 209, 8, 208,
                                                 7, 207, 6, 206, 5, 205, 4, 204, 3, 203, 2, 202, 1, 201]

        # Define test input variables
        test_flag_typeWindings = 0
        test_nT = [16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17, 5, 16, 12, 17,
                   5, 16, 12, 17, 5]
        test_elPairs_GroupTogether = [[11, 27], [12, 28], [10, 26], [9, 25], [21, 5], [22, 6], [24, 8], [23, 7],
                                      [29, 13], [30, 14], [32, 16], [31, 15], [3, 19], [4, 20], [2, 18], [1, 17]]
        test_elPairs_RevElOrder = [0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1, 0, 0, 1, 1]

        # Calculate more required variables (they would normally be calculated by the BuilderLEDET object)
        test_indexTstop = np.cumsum(test_nT)
        test_indexTstop = test_indexTstop.tolist()
        test_indexTstart = [1]
        for i in range(len(test_nT) - 1):
            test_indexTstart.extend([test_indexTstart[i] + test_nT[i]])

        # Assign test variables to an empty BuilderLEDET object
        bLEDET = BuilderLEDET(flag_build=False)
        bLEDET.setAttribute(bLEDET.Options, 'flag_typeWindings', test_flag_typeWindings)
        bLEDET.setAttribute(bLEDET.Inputs, 'nT', test_nT)
        bLEDET.setAttribute(bLEDET.Auxiliary, 'elPairs_GroupTogether', test_elPairs_GroupTogether)
        bLEDET.setAttribute(bLEDET.Auxiliary, 'elPairs_RevElOrder', test_elPairs_RevElOrder)
        bLEDET.setAttribute(bLEDET.Auxiliary, 'indexTstart', test_indexTstart)
        bLEDET.setAttribute(bLEDET.Auxiliary, 'indexTstop', test_indexTstop)

        # act
        el_order_half_turns_test = bLEDET.calcElectricalOrder()

        # assert
        self.assertListEqual(list(el_order_half_turns_test),
                             list(el_order_half_turns_reference_MQXF_V2))  # check values are correctly calculated
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'el_order_half_turns')),
                             list(el_order_half_turns_reference_MQXF_V2))  # check values are correctly set

    def test_translateModelDataToLEDET(self):
        """
            Check that calcElectricalOrder calculates correctly. The test use-case if for MQXF_V2
        """
        # arrange
        model_data = DataModelMagnet()
        bLEDET = BuilderLEDET(input_model_data=model_data, flag_build=False)

        # act
        bLEDET.translateModelDataToLEDET()

        # assert
        # TODO: Check that all keys are correctly passed

    def test_addThermalConnections_alongWidth(self):
        """
            Check that addThermalConnections() works correctly. The test use-case is invented and defined manually
        """
        # arrange
        iContactAlongWidth_From_initial   = np.array([1, 2, 3, 3, 5, 6, 7, 8, 9, 10, 13])
        iContactAlongWidth_To_initial     = np.array([101, 102, 103, 104, 104, 106, 107, 108, 109, 110, 113])
        iContactAlongWidth_pairs_to_add   = [[11, 111], [12, 111], [13, 113], [13, 113]]  # Note that this will be passed by the BuilderLEDET as a list of lists and not as a np.array
        iContactAlongWidth_From_reference = np.array([1, 2, 3, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        iContactAlongWidth_To_reference   = np.array([101, 102, 103, 104, 104, 106, 107, 108, 109, 110, 111, 111, 113])  # these entries were manually written

        # Assign test variables to an empty BuilderLEDET object
        bLEDET = BuilderLEDET(flag_build=False)
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongWidth_From', np.array(iContactAlongWidth_From_initial))
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongWidth_To',   np.array(iContactAlongWidth_To_initial))
        bLEDET.setAttribute(bLEDET.Auxiliary, 'iContactAlongWidth_pairs_to_add', np.array(iContactAlongWidth_pairs_to_add))

        # act - This method must add these connections and set the two LEDET parameters
        bLEDET.addThermalConnections()

        # assert - Check that the parameters were correctly set
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongWidth_From')), list(iContactAlongWidth_From_reference))
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongWidth_To')),   list(iContactAlongWidth_To_reference))

    def test_addThermalConnections_alongHeight(self):
        """
            Check that addThermalConnections() works correctly. The test use-case is invented and defined manually
        """
        # arrange
        iContactAlongHeight_From_initial   = np.array([1, 2, 3, 3, 5, 6, 7, 8, 9, 10, 13])
        iContactAlongHeight_To_initial     = np.array([101, 102, 103, 104, 104, 106, 107, 108, 109, 110, 113])
        iContactAlongHeight_pairs_to_add   =[[13, 113], [11, 111], [12, 111], [13, 113]]  # Note that this will be passed by the BuilderLEDET as a list of lists and not as a np.array
        iContactAlongHeight_From_reference = np.array([1, 2, 3, 3, 5, 6, 7, 8, 9, 10, 11, 12, 13])
        iContactAlongHeight_To_reference   = np.array([101, 102, 103, 104, 104, 106, 107, 108, 109, 110, 111, 111, 113])  # these entries were manually written

        # Assign test variables to an empty BuilderLEDET object
        bLEDET = BuilderLEDET(flag_build=False)
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongHeight_From', np.array(iContactAlongHeight_From_initial))
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongHeight_To',   np.array(iContactAlongHeight_To_initial))
        bLEDET.setAttribute(bLEDET.Auxiliary, 'iContactAlongHeight_pairs_to_add', np.array(iContactAlongHeight_pairs_to_add))

        # act - This method must add these connections and set the two LEDET parameters
        bLEDET.addThermalConnections()

        # assert - Check that the parameters were correctly set
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongHeight_From')), list(iContactAlongHeight_From_reference))
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongHeight_To')),   list(iContactAlongHeight_To_reference))

    def test_removeThermalConnections_alongWidth(self):
        """
            Check that addThermalConnections() works correctly. The test use-case is invented and defined manually
        """
        # arrange
        iContactAlongWidth_From_initial = np.array([1, 2, 3, 3, 5, 6, 7, 8, 9, 10])
        iContactAlongWidth_To_initial = np.array([101, 102, 103, 104, 105, 106, 107, 108, 109, 110])
        iContactAlongWidth_pairs_to_remove = [[8, 108], [9, 109], [10, 110], [10, 110]]  # Note that this will be passed by the BuilderLEDET as a list of lists and not as a np.array
        iContactAlongWidth_From_reference = np.array([1, 2, 3, 3, 5, 6, 7])
        iContactAlongWidth_To_reference = np.array([101, 102, 103, 104, 105, 106, 107])  # these entries were manually written

        # Assign test variables to an empty BuilderLEDET object
        bLEDET = BuilderLEDET(flag_build=False)
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongWidth_From', np.array(iContactAlongWidth_From_initial))
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongWidth_To', np.array(iContactAlongWidth_To_initial))
        bLEDET.setAttribute(bLEDET.Auxiliary, 'iContactAlongWidth_pairs_to_remove', np.array(iContactAlongWidth_pairs_to_remove))

        # act - This method must add these connections and set the two LEDET parameters
        bLEDET.removeThermalConnections()

        # assert - Check that the parameters were correctly set
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongWidth_From')), list(iContactAlongWidth_From_reference))
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongWidth_To')), list(iContactAlongWidth_To_reference))

    def test_removeThermalConnections_alongHeight(self):
        """
            Check that removeThermalConnections() works correctly. The test use-case is invented and defined manually
        """
        # arrange
        iContactAlongHeight_From_initial = np.array([1, 2, 3, 4, 5, 5, 7, 8, 9, 10])
        iContactAlongHeight_To_initial = np.array([101, 101, 103, 104, 105, 106, 107, 108, 109, 110])
        iContactAlongHeight_pairs_to_remove = [[10, 110], [8, 108], [9, 109], [10,
                                                                               110]]  # Note that this will be passed by the BuilderLEDET as a list of lists and not as a np.array
        iContactAlongHeight_From_reference = np.array([1, 2, 3, 4, 5, 5, 7])
        iContactAlongHeight_To_reference = np.array(
            [101, 101, 103, 104, 105, 106, 107])  # these entries were manually written

        # Assign test variables to an empty BuilderLEDET object
        bLEDET = BuilderLEDET(flag_build=False)
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongHeight_From', np.array(iContactAlongHeight_From_initial))
        bLEDET.setAttribute(bLEDET.Inputs, 'iContactAlongHeight_To', np.array(iContactAlongHeight_To_initial))
        bLEDET.setAttribute(bLEDET.Auxiliary, 'iContactAlongHeight_pairs_to_remove',
                            np.array(iContactAlongHeight_pairs_to_remove))

        # act - This method must add these connections and set the two LEDET parameters
        bLEDET.removeThermalConnections()

        # assert - Check that the parameters were correctly set
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongHeight_From')),
                             list(iContactAlongHeight_From_reference))
        self.assertListEqual(list(bLEDET.getAttribute(bLEDET.Inputs, 'iContactAlongHeight_To')),
                             list(iContactAlongHeight_To_reference))

    def test_printVariableDescNameValue(self):
        """
            Check that printVariableDescNameValue() works correctly.
        """
        # arrange
        bLEDET = BuilderLEDET(flag_build=False)

        # act - Visualize variable descriptions, names, and values
        print('### "Inputs" variables ###')
        bLEDET.printVariableDescNameValue(bLEDET.Inputs, bLEDET.descriptionsInputs)

        print('')
        print('### "Options" variables ###')
        bLEDET.printVariableDescNameValue(bLEDET.Options, bLEDET.descriptionsOptions)

        print('')
        print('### "Plots" variables ###')
        bLEDET.printVariableDescNameValue(bLEDET.Plots, bLEDET.descriptionsPlots)

        # Visualize variable descriptions, names, and values
        print('')
        print('### "Variables" variables ###')
        bLEDET.printVariableDescNameValue(bLEDET.Variables, bLEDET.descriptionsVariables)

        # assert
        print('Test passed: all variables in LEDET dataclasses have a description defined in the variableNamesDescriptions.xlsx file.')
