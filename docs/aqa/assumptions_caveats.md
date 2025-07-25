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

* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

As census was conducted a year later in Scotland than England and Wales, and Northern Ireland (NI), we are assuming this will not have a great impact on the clusters created.

## Assumption 2: Not including Bangladeshi ethnic group for NI

* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Values for the Bangladsehi ethnic group are not avaialble to download for Northern Ireland as the values are so low they could be classed as disclosive. However we have decided to continue to factor in the is group for the other two censuses (EW and Scot).

## Assumption 3: Standard Illness Ratio calculated from XX age
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Origionally in the 2021 area classification ages were grouped into <15 and >65. This is not possible due to the split of ages across all three census' there gore we have tried to replicate with best data we had but couldn't split at XX age because this data was not available for all three census.

## Assumption 4: Combined area codes for disability data
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

In the England and Wales disability Census data 2021 provides combined values for the areas below. We have assumed the SIR values is the same for both of the areas within the combined as these are proprotions. 
E09000001 and E09000033 - City of London and Westminster
E06000052 and E06000053 - Cornwall and Isles of Scilly

## Assumption 5: Using the Local Authoirty District look up table for 2022
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Plain text

## Assumption 6 / Decision log: to include ts0440007 
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

In the interim solution for the aggregation of 'Flat', Jakub aggregated flat = NM_1549_1_7 + NM_1549_1_8 + NM_1549_1_9,
Accommodation type
Flat = 
NM_1549_1_7       (Unshared dwelling: Flat, maisonette or apartment: Purpose-built block of flats or tenement) + 
NM_1549_1_8       (Unshared dwelling: Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)) +
NM_1549_1_9       (Unshared dwelling: Flat, maisonette or apartment: In commercial building)

This did not include "ts0440007 - Accommodation type: Part of another converted building, for example, former school, church or warehouse" we have made the decision to include this in the England and Wales aggregation for Flats since NI and Scot includes: 
NI - Aggregation to produce 'flat' from ni0030005 + ni0030006 + ni0030007
- ni0030005 Household: Accommodation Type: Flat, maisonette or apartment: Purpose-built block of flats
- ni0030006 Household: Accommodation Type: Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)
- ni0030007 Household: Accommodation Type: Flat, maisonette or apartment: In a commercial building (for example in an office building, hotel, or over a shop)

Scotland includes UV4010006 which is "Flat, maisonette or apartment: Total" and includes:
- UV4010007 Flat, maisonette or apartment: Purpose-built block of flats or tenement
- UV4010008 Flat, maisonette or apartment: Part of a converted or shared house (including bed-sits)
- UV4010009 Flat, maisonette or apartment: In a commercial building

## Assumption 7: 
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

[Country of Birth - 9 Categories](https://build.nisra.gov.uk/en/custom/data?d=PEOPLE&v=LGD14&v=COB_AGG9) was used for NI. To harmonise with EW and Scot, we require the total for all EU countries. We have there for “Europe: Ireland” and “Europe: Other EU countries” together however with a caveat. The Republic of Ireland is included in EU countries and Northern Ireland is included in the United Kingdom or non-EU. However if someone just answered Ireland (and didn’t state Republic of Ireland) to the country of birth question this could mean they live in either the Republic of Ireland (EU) or Northern Ireland (UK so non-EU) so they are coded to Non-EU as there is no way to determine which is the correct classification for these responses.

## Assumption 8: 
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Plain text




