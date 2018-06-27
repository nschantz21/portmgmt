# given a date and company identifier, I want to know what the latest reported fundamental data is
ORIGINAL_DATE = None
COMPANY = None
FIELD = None

# Latest Full Report date
report_date = LocalTerminal.get_reference(COMPANY, "ANNOUNCEMENT_DT", FUNDAMENTAL_PUBLIC_DATE=ORIGINAL_DATE)

# Period of that report
# Annual will supercede semi-annual and quarterly
report_period = LocalTerminal(COMPANY, "LATEST_ANNOUNCEMENT_PERIOD", FUNDAMENTAL_PUBLIC_DATE=report_date)

# primary periodicity of the company
periodicity = LocalTerminal(COMPANY, "PRIMARY_PERIODICTY")

# Fiscal Year and period of the report, based on the periodicity 
# This will help distinguish annual and other periods for the annual report
fund_yr_prd = LocalTerminal(COMPANY, "FISCAL_YEAR_PERIOD", EQY_FUND_DT= report_date, EQY_FUND_RELATIVE_PERIOD = '-0F' + periodicity[0])


if report_date[-1] == 'A':
    # Take the annual data
    
else:
    # get the trailing LTM
        