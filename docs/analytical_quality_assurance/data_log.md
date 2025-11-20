# Data log

This log contains a list of data sources used in this analysis.

## Definitions

Assumptions are RAG-rated according to the following definitions for quality and
suitability[^1]:

[^1]: With thanks to the Home Office Analytical Quality Assurance team for these definitions.

| RAG   | Data quality                                                                                                                                                                                 | Data suitability                                                                                                                                                                                            |
|-------|----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------|
| Green | Data is well understood and there are no major issues with quality. Minor issues are understood and documented.                                                                              | Data is best available for the required purpose and has been validated (for example against published statistics).                                                                                          |
| Amber | Data is well understood. There are quality issues (for example missing values, step changes, large number of outliers) that can be explained, documented or shown to have negligible impact. | Not the ideal data set for the analysis, but the best available at the time. Results will reflect the fact that it is not the ideal data set and it will subject to sensitivity analysis where appropriate. |
| Red   | Data is not well understood. There are major quality issues that cannot be fully explained and/or have a significant impact on analysis outputs.                                             | There are concerns about the suitability of the data set for this application, which could negatively affect the quality and accuracy of the analysis. Its derivation / sample size is not known.           |

## Source 1: NOMIS
* Quality: Green
* Suitability: Green <br>

NOMIS is the official data service provided by the ONS. This was the most suitable source of census data for England and Wales. 

## Source 2: NISRA (Northern Ireland Statistics and Research Agency)
* Quality: Green
* Suitability: Green <br>

NISRA is the principal source of official statistics for Northern Ireland.

## Source 3: Scotland's Census
* Quality: Green
* Suitability: Green <br>

Scotland's Census website is the official provider of census statistics for Scotland. 

## Source 4: ONS Open Geography Portal 
* Quality: Green
* Suitability: Green <br>

The source of the Standard Area Measurement product used for population density calculations. Also the source for the Local Authority Districts Names and Codes in the UK Lookup. The portal is the official source of geographic products, web applications, story maps, services and APIs from the ONS.

## ONS website
* Quality: Green
* Suitability: Green <br>

The source of the England and Wales Census 2021 disability data used for calculating the Standardised Illness Ratio. Also the source of National and subnational mid-year population estimates for the UK and its constituent countries used for population density calculations. 

