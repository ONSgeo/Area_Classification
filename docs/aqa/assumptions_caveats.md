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

## Assumption 5: 
* Quality: Insert RAG rating here
* Impact: Insert RAG rating here

Plain text
