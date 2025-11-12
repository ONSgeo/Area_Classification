# Assumptions and caveats log

This log contains a list of assumptions and caveats used in this analysis.

## Definitions

Assumptions are RAG-rated according to the following definitions for quality and
impact[^1]:

[^1]: With thanks to the Home Office Analytical Quality Assurance team for these definitions.

| RAG   | Assumption quality                                                                                                              | Assumption impact                                                                           |
|-------|---------------------------------------------------------------------------------------------------------------------------------|---------------------------------------------------------------------------------------------|
| Green | Reliable assumption, well understood and/or documented; anything up to a validated & recent set of actual data.                 | Marginal assumptions; their changes have no or limited impact on the outputs.               |
| Amber | Some evidence to support the assumption; may vary from a source with poor methodology to a good source that is a few years old. | Assumptions with a relevant, even if not critical, impact on the outputs.                   |
| Red   | Little evidence to support the assumption; may vary from an opinion to a limited data source with poor methodology.             | Core assumptions of the analysis; the output would be drastically affected by their change. |

## Assumption 1: Using 2021 censuses data in combination with 2022 censuses

* Quality: Green
* Impact: Red

Census was conducted in a different year for Scotland (2022) than England and Wales (2021), and Northern Ireland (2021). Census is the only source which can provide information on the variables required for this analysis, as Scotland was only a year later, we are assuming that this will not have a great impact on the clusters created, especially when compared with 2011 Census data (the previously census year). 

## Assumption 2: Not including Bangladeshi ethnic group for NI

* Quality: Green
* Impact: Red

Values for the Bangladeshi ethnic group are not available to download for Northern Ireland, because of this we have decided to remove this group for the other two censuses (EW and Scot), so that all three data sources are aligned. By including this variable for EW and Scot, but not NI we found it to effect clustering by grouping NI as one cluster, separate from the others.

## Assumption 3: Combined area codes for disability data for the calculation of Standard Illness Ratio

* Quality: Amber
* Impact: Green

In the England and Wales disability Census data 2021 provides combined values for the areas below. We have assumed the SIR values is the same for both of the areas within the combined as these are proportions. 
E09000001 and E09000033 - City of London and Westminster
E06000052 and E06000053 - Cornwall and Isles of Scilly

## Assumption 4: Using the Local Authority  District (LAD) look up table for 2022

* Quality: Green
* Impact: Green

This look up is used to replace the LAD names with codes, as some of the census data downloaded comes with the LAD names. Although the census data for England, Wales and Northern Ireland is for 2021, a 2022 look up was chosen so that it is also suitable for use on the Scotland data which is from 2022. We have ran a comparision which shows there is no difference between the 2021 lookup and the 2022 lookup.

## Assumption 6 / Decision log: to include ts0440007 
* Quality: Green
* Impact: Amber

In the 2021 interim solution the variable, "ts0440007 - "Accommodation type: Part of another converted building, for example, former school, church or warehouse" was not included when aggregating to create the 'Flats' variable. 
We have decided to include it for England and Wales so that it aligns with those available for Scot and NI.

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

## Assumption 6: Country of birth in Northern Ireland.
* Quality: Amber
* Impact: Amber

For Northern Ireland, we have used [Country of Birth - 9 Categories](https://build.nisra.gov.uk/en/custom/data?d=PEOPLE&v=LGD14&v=COB_AGG9). In order to harmonise with England, Wales and Scotland, a total for all EU countries is required. In England and Wales ts0040004 - "Europe: EU countries" variable is used and Scotland, UV2040010 - "Europe: EU countries".

In the Northern Ireland data, The Republic of Ireland is included in EU countries and Northern Ireland is included in the United Kingdom or non-EU. However, if someone answered 'Ireland' (and didn’t state Republic of Ireland) to the country of birth question this could mean they live in either the Republic of Ireland (EU) or Northern Ireland (UK so non-EU). Therefore, they will have been coded to Non-EU as there is no way to determine which is the correct classification for these responses. 
As a result, we have aggregated ni0330004 - "Europe: Ireland"	and ni0330005 - "Europe: Other EU countries" for Northern Ireland data. 

## Assumption 7: Education aggregation?
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Plain text

## Assumption 8: Clustergrams for 4d NOW 2d?
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Coded to skip over the clustergram for 4d, as this only contains Oxford and Cambridge so a clustergram is not needed and when ran on 1000 iterations this clustergram errors.

## Assumption 9: Using households for some Scotland variables which are available at individual and household level
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Household composition is used for: (V05) one-person household, (V06) families with no children, and (V07) families with dependent children. 
This is available in two versions: V112 - Household composition - People and UV113 - Household composition - Households.

Accommodation type is used for: (V35) detached, (V36) semi-detached, (V37) terraced and (V38) flat
This is available in two versions: UV401 - Accommodation type - People and UV402 - Accommodation type - Households

We have decided to use the 'Households' versions (UV113 and UV402) to be consistent with the [lookup used in the code](https://github.com/jakubwyszomierski/OAC2021-2/blob/main/Data/Lookups/Final_codes_11_21.csv) 
which was used to create the [2021 interim area classification solution for England and Wales at Output Area Level](https://data.geods.ac.uk/dataset/output-area-classification-2021). 

## Assumption 10: Using the same variables as used in the interim 2021 Output Area Classification for England and Wales
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Plain text

## Assumption 11:
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Plain text


