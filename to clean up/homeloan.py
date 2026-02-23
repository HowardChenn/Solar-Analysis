# current figures
# total_loan = 620000
# annual_interest_rate = 0.0545
# years = 30
# weeks_per_year = 52
# weekly_interest_rate = annual_interest_rate / weeks_per_year

# offset = 105000
# weekly_offset_increase = 320 

# weekly_payment = 1158.3

# refinance figures 
total_loan = 600000
annual_interest_rate = 0.0545
years = 25
weeks_per_year = 52
weekly_interest_rate = annual_interest_rate / weeks_per_year

offset = 85000
weekly_offset_increase = 0

weekly_payment = 850

for year in range(years):
    total_interest_year = 0
    total_paid_year = 0
    total_principle_year = 0

    for week in range(weeks_per_year):
        offset += weekly_offset_increase
        weekly_interest = (total_loan-offset) * weekly_interest_rate
        total_loan = total_loan + weekly_interest - weekly_payment
        print("Year " + str(year+1))
        print("Week " + str(week+1))
        print("Total offset: " + format(offset, ","))
        print("Total loan remaining: " + format(int(total_loan), ","))
        total_interest_year += weekly_interest
        total_paid_year += weekly_payment
        total_principle_year = total_principle_year + weekly_payment - weekly_interest
        if total_loan <= 0:
            print("Done paying off the loan!")
            break
    print("Total interest paid in year " + str(year+1) + ": " + format(int(total_interest_year), ","))
    print("Total paid in year " + str(year+1) + ": " + format(int(total_paid_year), ","))
    print("Total principle paid in year " + str(year+1) + ": " + format(int(total_principle_year), ","))
    if total_loan <= 0:
        break
    input("Press Enter to continue to the next year...")
