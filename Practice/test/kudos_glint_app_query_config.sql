UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'ACCOUNTABLE' AND INTERFACE_NAME = 'ACCOUNTABLE_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'ACA_BIWEEKLY';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'ACA_MONTHLY';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'CENSUS';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'DEDUCTIONS_DEDLOAD_Biweekly';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'DEDUCTIONS_DEDLOAD_Monthly';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'DEDUCTIONS_STMLOAD_Biweekly';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'DEDUCTIONS_STMLOAD_Monthly';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'PAYROLL_BIWEEKLY';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'BUSINESSOLVER' AND INTERFACE_NAME = 'PAYROLL_MONTHLY';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'CONCUR' AND INTERFACE_NAME = 'CONCUR_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'DOCEBO' AND INTERFACE_NAME = 'ACCOUNT_FILE_TO_DOCEBO';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'DSF_MYPOD_TMF' AND INTERFACE_NAME = 'DSF_MYPOD_TMF_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'DSF_MYPOD_TMF' AND INTERFACE_NAME = 'DSF_SSO_ACCOUNT_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'DSF_MYPOD_TMF' AND INTERFACE_NAME = 'DSF_SSO_MAPPING_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'FIRSTUP' AND INTERFACE_NAME = 'OUTBOUND_CENTRAL_FEED';

-- Frontier not required

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'GENESIS' AND INTERFACE_NAME = 'EMPLOYEE_DATA_DELTA';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'GLINT' AND INTERFACE_NAME = 'GLINT_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'GUILD' AND INTERFACE_NAME = 'GUILD_EMPLOYEE';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'HII' AND INTERFACE_NAME = 'HII_BIWEEKLY';

-- HII BI WEEKLY CSV not required

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'HII' AND INTERFACE_NAME = 'HII_GHR';

-- HII HII GHR CSV not required

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'HII' AND INTERFACE_NAME = 'HII_MONTHLY';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'HII' AND INTERFACE_NAME = 'PROVIDER_ROOSTER';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'KUDOS' AND INTERFACE_NAME = 'EMPLOYEE_DEMO_DATA';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'LFG' AND INTERFACE_NAME = 'LFG';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'LFG' AND INTERFACE_NAME = 'LFG_CSV';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'MCI' AND INTERFACE_NAME = 'OUTBOUND_FULL_EMPLOYEE_EXPORT';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'MCI' AND INTERFACE_NAME = 'OUTBOUND_RTW_EMPLOYEE_EXPORT';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'MCI' AND INTERFACE_NAME = 'OUTBOUND_SUPPLEMENT_EMPLOYEE_EXPORT';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'ODYSSEY' AND INTERFACE_NAME = 'OUTBOUND_DAILY_ASSOCIATE';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'OIG' AND INTERFACE_NAME = 'OUTBOUND_ASSOCIATE_DEMOGRAPHICS';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'PARADOX' AND INTERFACE_NAME = 'PARADOX_LOCATION';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'PARADOX' AND INTERFACE_NAME = 'PARADOX_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'PARADOX' AND INTERFACE_NAME = 'PARADOX_USER';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'PRECHECK' AND INTERFACE_NAME = 'INBOUND_PRECHECK_FILE';

-- PRECHECK OUTBOUND_CREDENTIAL_FILE not required

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'PROTENUS' AND INTERFACE_NAME = 'PROTENUS_OUTBOUND';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'READYSET' AND INTERFACE_NAME = 'OUTBOUND_READYSET_OPTIMIZATION';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'SERVICENOW' AND INTERFACE_NAME = 'OUTBOUND_HR_LOCATION_DETAILS';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'SERVICENOW' AND INTERFACE_NAME = 'OUTBOUND_HR_USER_DEMOGRAPHICS';

UPDATE dbo.ref_locations_filter_config 
SET flag = 0, created_on = GETDATE()
WHERE APPLICATION_NAME = 'VIGILANZ' AND INTERFACE_NAME = 'VIGILANZ_OUTBOUND';