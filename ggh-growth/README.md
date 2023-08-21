
# Sustainable Urban Growth in the Greater Golden Horseshoe?

Data preparation for a SofC IMFG report


## Part 1) Looking back, 2006 to 2021

Trying to understand where growth has occurred in the Greater Golden Horseshoe (GGH) from 2006 to 2021 in terms of sprawl versus intensification, specifically in relation to the built-up boundary in the 2006 Growth Plan. We will try to find to what extent growth has occurred...
       
A. Outside the 2006 Growth Boundary
B. Within the 2006 Growth Boundary
C. If within, to what extent is growth ‘near’ transit and/or within Urban Growth Centres (UGC)

Report this for the overall GGH, and for each sub-region (see `regions-summary.csv` for a list of each)

The following describes the technical steps:


### A) Preparing Census Data

1. Download census Dissemination Area (DA) boundaries for 2006 and 2021 for Ontario
2. Create a linking table of each DA to it’s corresponding GGH sub-region (file 'ggh-growth-plan-regions.geojson'). Each DA should only be linked to one sub-region. e.g.

| DAUID_21 | Region  |
|----------|---------|
| 35200001 | Toronto |
| 35200002 | Toronto |
| ...      | ...     |
      
- Do this by matching IDs (use the census geography hierarchy or attribute file if needed) rather than any sort of spatial query. The higher level census IDs for each sub-region can be found in 'regions-summary.csv'

- Create separate tables for 2021 DAs and 2006 DAs
    
3. Filter the downloaded DA boundaries for just those within the GGH.
4. Download and left-join data for each DA. Do this for 2006 and 2021.
5. Create summary table of growth for each sub-region - i.e. change in pop, households, dwellings, dwellings by structural type - by aggregating and summing DA-level data by sub-region for the two years, then join by the sub-region and compute the difference between the two years

|Census Variables                    |              2006                     |              2021              |              Notes        |
|---|---|---|---|
|Population,                           ||||       
|Area (km2),                            ||||
|Total households,                     |||
|Total dwellings                     |||(all dwellings, not just occupied), and|
|Dwellings by structural type        ||| (there are 7-8ish categories)|

### B) Classifying DAs

We now need to classify DAs whether they are within or outside the 2006 growth boundary, as well as Urban Growth Centres and near transit

1. Create a binary classification denoting whether DAs are CONTAINED within 2006 built boundary, spatial file here -> `ggh-growth-plan-2006-built-boundary.geojson`

2. Create a binary classification denoting whether DAs INTERSECT the 2006 Urban Growth Centres (UGC) and 1km transit station buffers.

- Do the above steps in QGIS or `geopandas`

- The final table should look like the following. Have a table for 2021 and another for 2006

| DAUID_21    | in_2006_built_boundary | in_urban_growth_centre | in_1km_transit_buffer |
| -------- | ---------------------- | ---------------------- | --------------------- |
| 35200001 | yes                    | no                     | yes                   |
| 35200002 | yes                    | yes                    | no                    |
| 35200003 | no                     | no                     | no                    |
| ... | ...                     | ...                     | ...                    |


### C) Summarizing Results

1. Create summary tables showing the growth in population, households, and dwellings within each scenario (e.g. within and outside the built boundary) by aggregating DA-level data by region. Here's an example for population (then do similarly for households, dwellings, etc.)

| Region  | population_growth_06_to_21 | in_2006_built_boundary | in_urban_growth_centre | in_1km_transit_buffer |
| ------- | ----------------- | ---------------------- | ---------------------- | --------------------- |
| Toronto | 300000            | 90%                    | 40%                    | 50%                   |
| Peel    | 100000            | 40%                    | 20%                    | 25%                   |
| ...    | ...            | ...                   | ...                    | ...                   |
| Total    | 1500000            | 30%                   | 10%                    | 10%                   |

This will tell us what percent of a region's new development is new 'greenfield' sprawl versus infill/intensification


## Part 2) GHG Emission Estimates and Scenario Testing

All work within `ghg-analysis` folder. All data are linked to 2021 DAs. Do all work in Python/Jupyter, since there's a chance the input data will be updated.

### A) Estimating Household Transport Emissions

The file `input-vkt-by-da-estimate.csv` are estimates of average Vehicle Kilometres Travelled (VKT) per household for each DA in the study area. This is a daily total for a weekday in 2016 (yes this isn't great, but the best we have)

The goal for this part is to estimate the average level of yearly GHG emissions per household for transport for each DA based on this data.

This will be a rough estimate, but should be possible based on the following.

### A1

$$ \bar{g_o} = \frac{e_o*1000}{h_o} $$

where: </br>
-  $\bar{g_o}$ is the average household travel ghg emission in Ontario (tons / household)
- $e_o$ is the total household travel ghg emissions in Ontario in 2020, obtained from [Stats Canada](https://www150.statcan.gc.ca/t1/tbl1/en/cv.action?pid=3810009701)
(kilo-tons)
- $h_o$ is the Total Household Count of Ontario (households)
- By averaging ghg emissions for 2019 and 2020, we get $\bar{g_o} = 0.0052$


### A2
Calulating the weights to weight average ontario household travel ghg emission 

$$ \bar{v_i} = \frac{\sum_i v_i h_i}{\sum_i hr_i} $$

where:
- $\bar{v_i}$ is the average daily household VKT in a region (km/household)
- $v_i$ is the average daily VKT per household in DA $i$ (km/household)
- $hr_i$ is the number of households in Da $i$ (household)
- $\sum_i v_i h_i$ is summing the total VKT of each DAs in each region
- $\sum_i hr_i$ is summing the 


### A3

To calulate household travel ghg emission in the Greater Golden Horseshoe (GGH), $\bar{g_o}$ is then up-or-down-weighted by the average daily VKT per household at the DA level.

$$ g_i = \bar{g_o} \frac{v_i}{\bar{v_i}} $$

where:
- $g_i$ is the transportation fuel emissions per household for each DA (ton / household)
-  $\bar{g_o}$ is the average household travel ghg emission in Ontario (tons / household)
- $v_i$ is the average daily VKT per household in DA $i$ (km / household)
- $\bar{v_i}$ is the average daily household VKT in a region (km/household)


<b> Assumption: </b><br>
The assumption would be that daily VKT is proportional to yearly transport emissions. This might require more research to see what the best method here is, and validating against any other published aggregate statistics (to make sure we're in the right ballpark).


Create an output table that is the same as the input, but with a column for estimate yearly emissions.

### B) Summarizing Emissions by Region

Using the output of A) plus the data in `input-ghg-ontario.csv` which is an estimate of GHG emissions stemming from household energy use by DA to summarize...

- Total emissions for each municipality, outer-ring, inner-ring, and overall
- Average emissions by household for each region, outer-ring, inner-ring, and overall (these averages should be weighted by the number of households in each DA)
- Do the above for energy, transport, and total emissions

### C) Estimating Average GHG Emissions for Different Neighbourhood Types

For the following types of neighbourhoods, estimate average household emissions (transport + energy). Use the same interpolation method created in Part 1B where necessary.

## C1)
- Inside and outside Urban Growth Centres
- Inside and outside 1km transit buffers
- Inside and outside the 2006 Built boundary
$$ R_i = \frac{\sum G_i w_i}{\sum H_i w_i} $$
-  where <br>
    $G_i$ is the total GHG emission in $DA_i$ <br>
    $H_i$ is the total household in $DA_i$ <br>
    $w_i$ is the ratio of area within / outside of BLT, UGC, TBF <br>
    $R_i$ is the ghg emission per household within BLT, UGC, TBF

## C2)
- Outside the built boundary AND population density of >= 100 people/km2 (i.e. not rural)
- Inside the built boundary AND population density >= 5000 people/km2
- Inside the built boundary AND population density >= 10000 people/km2

