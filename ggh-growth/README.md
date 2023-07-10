

## Looking back, 2006 to 2016

Understanding where growth has occurred in the Greater Golden Horseshoe (GGH) from 2006 to 2021. Has it occurred ….
       
A. Outside the 2006 Growth Boundary
B. Within the 2006 Growth Boundary
C. If within, is it also ‘near’ transit and/or in Urban Growth Centres (UGC)

Report this for the overall GGH, and for each sub-region

How can we do this?

### Preparing Census Data

1. Download census Dissemination Area (DA) boundaries for 2006 and 2021 for the GGH
2. Create a linking table of each DA to it’s corresponding GGH sub-region (file 'ggh-growth-plan-regions.geojson'). Each DA should only be linked to one sub-region. e.g.

DAUID_21, Region
35200001, Toronto
35200002, Toronto
etc. etc.
      
Do this by matching IDs (use the census geography hierarchy or attribute file if needed) rather than any sort of spatial query. The higher level census IDs for each sub-region can be found in 'regions-summary.csv'

Create a table for 2021 DAs and 2006 DAs
    
3. Filter the downloaded DA boundaries for just those in this table (i.e. just those within the GGH)
4. Download and left-join data for population, area (km2), total households, total dwellings (all dwellings, not just occupied), and dwellings by structural type (there are 7-8ish categories) for each DA
5. Create summary table of growth for each sub-region - i.e. change in pop, dwellings, dwellings by structural type - by aggregating and summing DA-level data by sub-region for the two years, then join and compute the difference between the two years

### Classifying DAs

We now need to classify DAs whether they are within or outside the 2006 growth boundary, as well as Urban Growth Centres and near transit

1. Create a binary classification denoting whether DAs INTERSECT the 2006 built boundary, spatial file here -> `ggh-growth-plan-2006-built-boundary.geojson`

2. Do the same for the Urban Growth Centre boundaries and the 1km transit buffers

The final table should look like this:

| DAUID    | in_2006_built_boundary | in_urban_growth_centre | in_1km_transit_buffer |
| -------- | ---------------------- | ---------------------- | --------------------- |
| 35200001 | yes                    | no                     | yes                   |
| 35200002 | yes                    | yes                    | no                    |
| 35200003 | no                     | no                     | no                    |



