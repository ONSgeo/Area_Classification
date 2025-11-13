# Standard Illness Ratio

## 1.0 Introduction
Standardised Illness Ratio was previously employed in the 2001 Output Area Classification as age was recognised as a key factor in determining prevalence and health issues and disability. The SIR is used as a measure of disability within each area, it provides a comparison between the disability count of an area and the expected illness. We have continued the use of this calculation as a continuation of the work which created the interim [2021 output area classifications for England and Wales](https://data.geods.ac.uk/dataset/output-area-classification-2021).

The national average is 100, so values for each area will be relative to this. For example an area with value of 90 means it has a 10% lower illness rate than the national average, whilst an area with a value of 110 has a 10% higher illness rate. 

[SIR for England and Wales was created by ONS until 2011 ](https://www.ons.gov.uk/peoplepopulationandcommunity/healthandsocialcare/healthandlifeexpectancies/datasets/standardisedillnessratiosbynationalstatisticssocioeconomicclassificationenglandandwales)

## 2.0 Terminology

| Term |	Definition |	
| -------- |   ---------- | 
| expected ill | This is an estimation of the number of people in an area who are expected to have a long term illness or disability, assuming the illness ratio in the area is proportional to the UK national average. The expected ill (`exp_ill`) is calculated by dividing the national proportion for each age range (‘<15 and >=65’ and ‘15-64’) in each LAD by the total population for each age range in each LAD. This represents. | 
| national proportion |   This is the proportion of individuals with a disability in a specific area relative to the total population of that area. In this work, the national proportion (`nat_prop`) is calculated by dividing the disability count for each LAD by the population for each LAD.| 
| total disabled | This is the total count of the people in an area who have a long-term illness or disability. For some data tables the total disabled (`total_disabled`), or it can be calculated by category.  | 


## 3.0 Assumptions and requirements
As the SIR is a relative indicator, a national average value for the UK is needed which requires data for all countries - England, Northern Ireland, Scotland and Wales. In this sense, we are assuming it is appropriate to combine the 2022 for Scotland (UV303a.csv), with 2021 data from England and Wales ('disabilitycensus2021.xlsx') and Northern Ireland ('ni_downloads/census-2021-ms-d02.xlsx').

As SIR is a relative measure that compares a spatial unit with the rest across the study area, the construction of SIR requires the inclusion of the proportions for all four countries.
## 4.0 Methods inputs and outputs
### Method inputs
Three tables are inputted into this data frame, one from each census (EW , NI and Scot). 
Each table must contain at least the following columns, although the column names may vary or require some pre processing:
| area code |	age |	count of those with a disability |	 count of those without a disability **OR** total population for that area  |
| -------- |   ---------- |     ---------- | ---------- |
|string  |int| int     | int |

### Method outputs
The SIR calculation produces a data frame with the following structure:
| area_code | exp_ill_all | disability_count | SIR |
| -------- |   ---------- |   ---------- |   ---------- | 
| string | int | int | int |
| string | int | int | int |

## 5.0 Method
The calculation of SIR has been conducted in line with the formula used by [Wyszomierski, 2023](https://discovery.ucl.ac.uk/id/eprint/10189266/2/THESIS_Jakub_Jan_Wyszomierski.pdf): 

<img width="206" height="65" alt="SIR_equation" src="https://github.com/user-attachments/assets/0de6f6b6-aa87-4335-a396-68a2c61a3178" />

- <img width="29" height="22" alt="SIR_equation_i" src="https://github.com/user-attachments/assets/1fa73eb8-81de-4c9e-bedd-d6833394bee9" />  is the observed count of people with long-term health problems ordisabilities in areal unit 𝑖
- <img width="26" height="26" alt="SIR_equation_rna" src="https://github.com/user-attachments/assets/d0ef38a9-519b-4d9d-bee8-952bf21b9725" /> is a proportion of ill or disabled people in group 𝑎 at the national level 
- <img width="15" height="24" alt="SIR_equation_pia" src="https://github.com/user-attachments/assets/8e165d49-b35d-4d53-a8f4-2efc3b7f4708" />is the population size of an age group 𝑎 in area 𝑖.

### Steps to achieve this: 
1. Each local authority is split into data for <15 and >=65 and 15-64. 
2. For each new group calculate the total disabled (WHAT DOES THIS MEAN IN EACH CENSUS EW, NI, SCOT) and the total population (for each LAD).
3. The national proportion (`nat_prop`) is calculated by dividing the disability count for each LAD by the population for each LAD.
4. The expected ill (`exp_ill`) is calculated by dividing the national proportion for each age range in each LAD by the total population for each age range in each LAD. At this stage there will still be two rows for every LAD. One for ‘<15 and >=65’ and ‘15-64’.
5. Next sum the expected ill and the total disabled for each LAD so there is only one total number for each `exp_ill_sum` and `disability_count`.
6. Then calculate the standard illness ratio by dividing the disability count by the expected illness and times by 100.

### Strengths
SIR provides a single measure of long term illnesss and disability in areas. The SIR replaced the census disability indicator as areas with a higher proportion of older people can be expected to be characterised by higher disability rates, but the SIR accounts for these age groups by looking at the data in two different age bands ‘Aged 0 to 16 and 64 and over’ and ‘Aged 16 to 64’.

### Limitations
Local Authority Districts (LADs) can vary in size and may not be entirely homogeneous so the SIR must be interpreted as an broad relative measure.

Previously, the [Wyszomierski, 2023](https://discovery.ucl.ac.uk/id/eprint/10189266/2/THESIS_Jakub_Jan_Wyszomierski.pdf) used age bands consisting of ‘Aged 0 to 16 and 64 and over’ and ‘Aged 16 to 64’ to calculate the SIR for the interim 2021 OAC England and Wales. However since more data has been made more available and we require consistent age bands across all datasets to enable cross-tabulation, we have used "Under 15 and 65 or older", and "15 to 64" (‘<15 and >=65’ and ‘15-64’). 

Note: Gale (2014) constructed SIR for the 2011 OAC, using ‘Aged 0 to 15 and 65 and over’ and ‘Aged 16 to 64’.
