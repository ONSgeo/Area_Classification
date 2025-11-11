# Standard Illness Ratio

## 1.0 Meta

## 2.0 Terminology

## 3.0 Introduction

### Strengths

### Limitations

## 4.0 Assumptions and requirements

## 5.0 Methods inputs and outputs
### Method inputs

### Method outputs


## 6.0 Method
Each local authority is split into data for <15 and >=65 and 15-64. 
For each new group calculate the total disabled (WHAT DOES THIS MEAN IN EACH CENSUS EW, NI, SCOT) and the total population (for each LAD).
The national proportion (nat_prop) is calculated by dividing the disability count for each LAD by the population for each LAD.
The expected ill (exp_ill) is calculated by dividing the national proportion for each age range in each LAD and the total population for each age range in each LAD. At this stage there will still be two rows for every LAD. One for ‘<15 and >=65’ and ‘15-64’.
Next sum the expected ill and the total disabled for each LAD so there is only one total number for each exp_ill_sum and disability_count.
Then calculate the standard illness ratio by dividing the disability count by the expected illness and times by 100.
