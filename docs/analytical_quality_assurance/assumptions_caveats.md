# Assumptions, caveats and decisions log

This log contains a list of assumptions, caveats and decisions used in this analysis.

## Definitions

Assumptions are RAG-rated according to the following definitions for quality and
impact[^1]:

[^1]: With thanks to the Home Office Analytical Quality Assurance team for these definitions.

| RAG   | Assumption quality                                                                                                              | Assumption impact                                                                           |
|-------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Green | Reliable assumption, well understood and/or documented; anything up to a validated & recent set of actual data.                 | Marginal assumptions; their changes have no or limited impact on the outputs.               |
| Amber | Some evidence to support the assumption; may vary from a source with poor methodology to a good source that is a few years old. | Assumptions with a relevant, even if not critical, impact on the outputs.                   |
| Red   | Little evidence to support the assumption; may vary from an opinion to a limited data source with poor methodology.             | Core assumptions of the analysis; the output would be drastically affected by their change. |

## Decision 1: Using 2021 censuses data in combination with 2022 censuses

* Quality: Green
* Impact: Red

Census was conducted in a different year for Scotland (2022) than England and Wales (2021), and Northern Ireland (2021). Census is the only source which can provide information on the variables required for this analysis, as Scotland was only a year later, the assumption is that this will not have a great impact on the clusters created, especially when compared with 2011 Census data (the previously census year). 

## Decision 2: Variables are consistent with 2021 Interim Output Area Classification

* Quality: Green
* Impact: Red

A decision was made to use the same variables as used in the interim 2021 Output Area Classification for England and Wales to ensure continuity and comparability with the earlier publication. It is assumed that the 50 selected census variables provide a sufficiently comprehensive representation of demographic characteristics across local authority districts, allowing meaningful comparison and grouping of similar areas within the UK. The impact is rated as red because the clustering results would be impacted if the variables were to change.


## Decision 3: Not including Bangladeshi ethnic group for Northern Ireland

* Quality: Green
* Impact: Red

Values for the Bangladeshi ethnic group are not available to download for Northern Ireland, because of this a decision was made to remove this variable for the other two censuses (EW and Scot), so that all three data sources are aligned. By including this variable for EW and Scot, but not NI affects clustering by grouping NI as one cluster, separate from the others.

## Decision 4: Combined area codes for disability data for the calculation of Standardised Illness Ratio (SIR)

* Quality: Amber
* Impact: Green

The England and Wales disability census data 2021 combines values for the areas below. It is assumed the SIR values are the same for both of the areas within the combined groups as SIR is a proportion. 
* E09000001 and E09000033 - City of London and Westminster
* E06000052 and E06000053 - Cornwall and Isles of Scilly

## Decision 5: Use of the Local Authority District (LAD) look up table for 2022

* Quality: Green
* Impact: Green

This look up is used to replace the LAD names with codes, as some of the census data downloaded comes with the LAD names. Although the census data for England, Wales and Northern Ireland is for 2021, a 2022 look up was chosen so that it is also suitable for use on the Scotland data which is from 2022. A comparision showed no difference between the 2021 lookup and the 2022 lookup.

## Decision 6: Inclusion of ts0440007 
* Quality: Green
* Impact: Amber

In the 2021 interim solution the variable, "ts0440007 - "Accommodation type: Part of another converted building, for example, former school, church or warehouse" was not included when aggregating to create the 'Flats' variable. It was decided to include it for England and Wales so that it aligns with those available for Scot and NI.

| EW Code   | Description                                                                                                           | 
|-----------|-----------------------------------------------------------------------------------------------------------------------|
| ts0440005 |       Accommodation type: In a purpose-built block of flats or tenement | 
| ts0440006 |       Accommodation type: Part of a converted or shared house, including bedsits | 
| ts0440007 |       Accommodation type: Part of another converted building, for example, former school, church or warehouse | 
| ts0440008 |       Accommodation type: In a commercial building, for example, in an office building, hotel or over a shop| 

| NI Code   | NI Description                                                                                                        |
|-----------|-----------------------------------------------------------------------------------------------------------------------| 
| ni0030005 | Household: Accommodation Type: Flat, maisonette or apartment: Purpose-built block of flats |
| ni0030006 | Household: Accommodation Type: Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits) |
| ni0030007 | Household: Accommodation Type: Flat, maisonette or apartment: In a commercial building (for example in an office building, hotel, or over a shop) |

Note, Scotland has a total for 'flat' already in the dataset - UV4010006 - "Flat, maisonette or apartment: Total" so this was used.
Variables included in UV4010006 are:
| Scot Code   | Scot Description                                                                                                    | 
|-------------|---------------------------------------------------------------------------------------------------------------------| 
|UV4010007| Flat, maisonette or apartment: Purpose-built block of flats or tenement|
|UV4010008| Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)|
|UV4010009| Flat, maisonette or apartment: In a commercial building|

## Decision 7: Country of birth in Northern Ireland.
* Quality: Amber
* Impact: Amber

For Northern Ireland, [Country of Birth - 9 Categories](https://build.nisra.gov.uk/en/custom/data?d=PEOPLE&v=LGD14&v=COB_AGG9) has been used. In order to harmonise with England, Wales and Scotland, a total for all EU countries is required. In England and Wales ts0040004 - "Europe: EU countries" variable is used and Scotland, UV2040010 - "Europe: EU countries".

In the Northern Ireland data, The Republic of Ireland is included in EU countries and Northern Ireland is included in the United Kingdom or non-EU. However, if someone answered 'Ireland' (and didn’t state Republic of Ireland) to the country of birth question this could mean they live in either the Republic of Ireland (EU) or Northern Ireland (UK so non-EU). Therefore, they will have been coded to Non-EU as there is no way to determine which is the correct classification for these responses. As a result, ni0330004 - "Europe: Ireland"	and ni0330005 - "Europe: Other EU countries" have been aggregated for Northern Ireland data. 

## Decision 8: Using households for some Scotland variables which are also available at individual and household level
* Quality: Green
* Impact: Green

Household composition data is used for: 
* (v05) one-person household, 
* (v06) families with no children
* (v07) families with dependent children. 

This is available in two versions: *UV112 - Household composition - People* and *UV113 - Household composition - Households*.

Accommodation type data is used for: 
* (v35) detached
* (v36) semi-detached
* (v37) terraced and (v38) flat

This is available in two versions: *UV401 - Accommodation type - People* and *UV402 - Accommodation type - Households*.

A deicsion was made to use the 'Households' versions (UV113 and UV402) to be consistent with the [lookup used in the code](https://github.com/jakubwyszomierski/OAC2021-2/blob/main/Data/Lookups/Final_codes_11_21.csv) 
which was used to create the [2021 interim area classification solution for England and Wales at Output Area Level](https://data.geods.ac.uk/dataset/output-area-classification-2021). 


