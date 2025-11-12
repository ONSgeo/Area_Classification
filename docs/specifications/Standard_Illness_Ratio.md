# Standard Illness Ratio

## 1.0 Summary

## 2.0 Terminology

| Term |	Definition |	
| -------- |   ---------- | 

## 3.0 Introduction
The use of the standard illness ratio is a continuation of the work produced in the creation of [2021 output area classifications](https://data.geods.ac.uk/dataset/output-area-classification-2021).

The SIR is used as a measure of diability within each area, it provides a comparision between the disability count of an area and the expected illness.

### Strengths

### Limitations

## 4.0 Assumptions and requirements

## 5.0 Methods inputs and outputs
### Method inputs
Three tables are inputted into this dataframe, one from each census (EW , NI and Scot). 
Each table must contain at least the following columns, although the column names may vary or require some pre processing:
| area code |	age |	count of those with a disability |	 count of those without a disability **OR** total population for that area  |
| -------- |   ---------- |     ---------- | ---------- |
|string  |int| int     | int |

  
### Method outputs
The SIR calculation produces a dataframe with the following structure:
| area_code | exp_ill_all | disability_count | SIR |
| -------- |   ---------- |   ---------- |   ---------- | 
| string | int | int | int |
| string | int | int | int |

## 6.0 Method
1. Each local authority is split into data for <15 and >=65 and 15-64. 
2. For each new group calculate the total disabled (WHAT DOES THIS MEAN IN EACH CENSUS EW, NI, SCOT) and the total population (for each LAD).
3. The national proportion (nat_prop) is calculated by dividing the disability count for each LAD by the population for each LAD.
4. The expected ill (exp_ill) is calculated by dividing the national proportion for each age range in each LAD and the total population for each age range in each LAD. At this stage there will still be two rows for every LAD. One for ‘<15 and >=65’ and ‘15-64’.
5. Next sum the expected ill and the total disabled for each LAD so there is only one total number for each exp_ill_sum and disability_count.
6. Then calculate the standard illness ratio by dividing the disability count by the expected illness and times by 100.
