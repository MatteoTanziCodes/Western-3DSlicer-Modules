############################
# Matteo Tanzi
# Undergrad Thesis Project
# April 10 - 2022
############################
from vpython import *
from time import *
import VesselConstruction as vcon
import VesselDisplay as vd
import Transformations as trans
import Data as data
######## PROGRAM ########

## Define 4 2d lists storing lists of FRE's and TRE's
ICP_Bifurcation = []
ICP_Centerline = []
CPD_Bifurcation = []
CPD_Centerline = []

def program(itr):
    for x in range(itr):
        ##### OVER DEFINED ITERATIONS ####
        ## Create Vessel Construction Object
        vc = vcon
        d = data
        t = trans

        ## Create Vessels
        Main_Vessel = vc.create_vessel()
        Deformed_Vessel = vc.create_deformed_vessel(Main_Vessel)

        ## Get Fiducials for Bifurcation
        main_bifurcation_pts = vc.bifurcation_points(Main_Vessel)
        deform_bifurcation_pts = vc.bifurcation_points(Deformed_Vessel)

        ## Get Fiducials for Centerline
        main_centerline_pts = vc.centerline_points(Main_Vessel[0])
        deform_centerline_pts = vc.centerline_points(Deformed_Vessel[0])

        ## Get Targets
        targets = vc.Targets()
        CT_Target = targets[0]
        US_Target = targets[1]

        ## Apply ICP to orig fiducial sets (Bifurcation) & Target
        ICP_bifurcation_data = t.ICP_Registration(main_bifurcation_pts, deform_bifurcation_pts, CT_Target, US_Target)

        ## Apply ICP to orig fiducial sets (Centerline) & Target
        ICP_centerline_data = t.ICP_Registration(main_centerline_pts, deform_centerline_pts, CT_Target, US_Target)

        ## Apply CPD to orig fiducial sets (Bifurcation) & Target
        CPD_bifurcation_data = t.CPD_Registration(main_bifurcation_pts, deform_bifurcation_pts, CT_Target, US_Target)

        ## Apply CPD to orig fiducial sets (Centerline) & Target
        CPD_centerline_data = t.CPD_Registration(main_centerline_pts, deform_centerline_pts, CT_Target, US_Target)

        ## Measure FRE & TRE of ICP-Bifurcation
        data1 = d.measure_FRE_TRE(ICP_bifurcation_data[0], ICP_bifurcation_data[1], ICP_bifurcation_data[2], ICP_bifurcation_data[3])

        ## Append Data to list 1
        ICP_Bifurcation.append(data1)

        ## Measure FRE & TRE of ICP-Centerline
        data2 = d.measure_FRE_TRE(ICP_centerline_data[0], ICP_centerline_data[1], ICP_centerline_data[2], ICP_centerline_data[3])

        ## Append Data to list 2
        ICP_Centerline.append(data2)

        ## Measure FRE & TRE of CPD-Bifurcation
        data3 = d.measure_FRE_TRE(CPD_bifurcation_data[0], CPD_bifurcation_data[1], CPD_bifurcation_data[2], CPD_bifurcation_data[3])

        ## Append Data to list 3
        CPD_Bifurcation.append(data3)

        ## Measure FRE & TRE of CPD-Centerline
        data4 = d.measure_FRE_TRE(CPD_centerline_data[0], CPD_centerline_data[1], CPD_centerline_data[2], CPD_centerline_data[3])

        ## Append Data to list 4
        CPD_Centerline.append(data4)
    
    data_read(itr)

##################################

##### DATA MEASUREMENT ######
def data_read(itr):
    d = data

    ## Calc mean FRE & TRE for ICP-Bifurcation
    measurements1 = d.data_measurement(ICP_Bifurcation)
    fre1 = measurements1[0]
    tre1 = measurements1[1]
    print("mean FRE for "+str(itr)+" vessel iteration ICP-Bifurcation: " + str(round(fre1,5)))
    print("mean TRE for "+str(itr)+" vessel iteration ICP-Bifurcation: " + str(round(tre1,5)) + "\n")

    ## Calc mean FRE & TRE for ICP-Centerline
    measurements2 = d.data_measurement(ICP_Centerline)
    fre2 = measurements2[0]
    tre2 = measurements2[1]
    print("mean FRE for "+str(itr)+" vessel iteration ICP-Centerline: " + str(round(fre2,5)))
    print("mean TRE for "+str(itr)+" vessel iteration ICP-Centerline: " + str(round(tre2,5)) + "\n")

    ## Calc mean FRE & TRE for CPD-Bifurcation
    measurements3 = d.data_measurement(CPD_Bifurcation)
    fre3 = measurements3[0]
    tre3 = measurements3[1]
    print("mean FRE for "+str(itr)+" vessel iteration CPD-Bifurcation: " + str(round(fre3,5)))
    print("mean TRE for "+str(itr)+" vessel iteration CPD-Bifurcation: " + str(round(tre3,5)) + "\n")

    ## Calc mean FRE & TRE for CPD-Centerline
    measurements4 = d.data_measurement(CPD_Centerline)
    fre4 = measurements4[0]
    tre4 = measurements4[1]
    print("mean FRE for "+str(itr)+" vessel iteration CPD-Centerline: " + str(round(fre4,5)))
    print("mean TRE for "+str(itr)+" vessel iteration CPD-Centerline: " + str(round(tre4,5)) + "\n")


program(1000)
