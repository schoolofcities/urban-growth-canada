Folder Structure:

ggh-growth
    > census-file-handling
        > Data
            > Census Data
                Census2006.csv
                Census2021.csv

            > gda_000b06a_e
                shapefile of 2006 Census Boundary at Dissemination Area Level, containing DAUID, CSDUID information

            > lcsd000b21a_e
                shapefile of 2021 Census Boundary at Census Sub Division Level, containing CSDDGUID_SDRIDUGD and CSDUID information
                
            > lda_000b21a_e
                shapefile of 2021 Census Boundary at Dissemination Area Level, containing DADGUID_ADIDUGD and DAUID information

            2021_DA_CSDUID_Reference_Table.csv
                This is the file that will bridge the gap between lcsd000b21a_e and lda_000b21a_e (it contains CSDDGUID_SDRIDUGD and DADGUID_ADIDUGD, important for briding the CSD file and the DA file. )
                created from 2021 Census - Dissemination Geographies Relationship File 
                https://www.census.gc.ca/census-recensement/2021/geo/sip-pis/dguid-idugd/index2021-eng.cfm?year=21

    > census-summary-data-2006-2021
        Codes and exported results are saved here
        > part-a-results
            tables generated from Part A - Census Data Cleaning_CSD2006.ipynb code
            the numbers for 2006 uses CSD data for 2006 and DA sum for 2021. This is due to the inconsistency between the DA sum and CSD sum for each geographical region, so we used CSD data for 2006. 

        > part-b-results
            two tables of the DAs in southern Ontario, for 2006 and 2021. 

        > part-c-results
            tables generated from Part A - Census Data Cleaning_DA2006.ipynb code. This data uses number summed from all DAs for 2006. 

            > summarizing-results

                Individual tables of each census variables and their changes within Built Boundary, UGC, and Transit Buffer is saved in the > summarizing-results folder

Census 2006:
    Total Private Dwelling is downloaded from Scholars Geoportal while the others are downloaded from CHASS
    