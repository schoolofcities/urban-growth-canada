
# Sustainable Urban Growth in the Greater Golden Horseshoe?

Data preparation for a SofC IMFG report

## Part 1) Looking back, 2006 to 2021

Trying where growth has occurred in the Greater Golden Horseshoe (GGH) from 2006 to 2021 in terms of sprawl versus intensification, specifically in relation to the built-up boundary in the 2006 Growth Plan. We will try to find to what extent growth has occurred...
       
A. Outside the 2006 Growth Boundary
B. Within the 2006 Growth Boundary
C. If within, to what extent is growth ‘near’ transit and/or within Urban Growth Centres (UGC)

Report this for the overall GGH, and for each sub-region

The following describes the technical steps:


### A) Preparing Census Data

1. Download census Dissemination Area (DA) boundaries for 2006 and 2021 for the GGH
2. Create a linking table of each DA to it’s corresponding GGH sub-region (file 'ggh-growth-plan-regions.geojson'). Each DA should only be linked to one sub-region. e.g.

| DAUID_21 | Region  |
|----------|---------|
| 35200001 | Toronto |
| 35200002 | Toronto |
| ...      | ...     |
      
- Do this by matching IDs (use the census geography hierarchy or attribute file if needed) rather than any sort of spatial query. The higher level census IDs for each sub-region can be found in 'regions-summary.csv'

- Create a table for 2021 DAs and 2006 DAs
    
3. Filter the downloaded DA boundaries for just those in this table (i.e. just those within the GGH)
4. Download and left-join data for population, area (km2), total households, total dwellings (all dwellings, not just occupied), and dwellings by structural type (there are 7-8ish categories) for each DA
5. Create summary table of growth for each sub-region - i.e. change in pop, households, dwellings, dwellings by structural type - by aggregating and summing DA-level data by sub-region for the two years, then join and compute the difference between the two years

### B) Classifying DAs

We now need to classify DAs whether they are within or outside the 2006 growth boundary, as well as Urban Growth Centres and near transit

1. Create a binary classification denoting whether DAs are CONTAINED within 2006 built boundary, spatial file here -> `ggh-growth-plan-2006-built-boundary.geojson`

2. Create a binary classification denoting whether DAs INTERSECT the 2006 Urban Growth Centres (UGC) and 1km transit station buffers.

The final table should look like the following

| DAUID    | in_2006_built_boundary | in_urban_growth_centre | in_1km_transit_buffer |
| -------- | ---------------------- | ---------------------- | --------------------- |
| 35200001 | yes                    | no                     | yes                   |
| 35200002 | yes                    | yes                    | no                    |
| 35200003 | no                     | no                     | no                    |
| ... | ...                     | ...                     | ...                    |

### C) Summarizing Results

1. Create a summary table showing the growth in population, households, and dwellings within each scenario (within and outside the built boundary) by aggregating DA-level data by region. Here's an example for population (then do similarly for households, dwellings, etc.)

| Region  | population_growth | in_2006_built_boundary | in_urban_growth_centre | in_1km_transit_buffer |
| ------- | ----------------- | ---------------------- | ---------------------- | --------------------- |
| Toronto | 300000            | 90%                    | 40%                    | 50%                   |
| Peel    | 100000            | 40%                    | 20%                    | 25%                   |
| ...    | ...            | ...                   | ...                    | ...                   |
| Total    | 1500000            | 30%                   | 10%                    | 10%                   |

This will tell us what percent of a region's new development is new 'greenfield' sprawl versus infill/intensification


## Part 2) GHG Emission Estimates and Scenario Testing

TBD