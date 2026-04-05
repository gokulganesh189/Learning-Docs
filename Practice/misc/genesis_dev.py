import os
import sys
import datetime
import time
from pathlib import Path

import numpy as np
import pyodbc
import traceback
from sqlalchemy.engine import URL, create_engine
import uuid
import pandas as pd
import psutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import platform

# Required utils
import utils.Email
import utils.SNOWCalls
import utils.ConnectionString
import utils.PGPEncryptDecrypt

interface_name = "Genesis"
os.environ["INTERFACE_NAME"] = interface_name

from utils.logger import Logger
logger = Logger.get_logger(interface_name)
from utils import filter_locations
from utils.config_loader import ConfigLoader
config = ConfigLoader(config_path=f"Genesis.ini")
CurrentDT = datetime.datetime.today()


##############################################################
# Loading DB connection
##############################################################
def load_db_param(scriptname, createincident_flag):
    retry_flag = True
    retry_count = 0
    db_retry_interval = config.get("db_retry_interval")
    db_retry_count = config.get("db_retry_count")
    dsn = config.get("dsn")
    config.get("db_retry_count")
    while retry_flag and retry_count < db_retry_count:
        try:
            global conn, cursor, connectionEngine, connection_str
            pyodbc.pooling = False

            if RunningPlatform == "LINUX":
                connection_str = utils.ConnectionString.ConnectionStringFetch_AD(dsn)
            else:
                connection_str = 'DRIVER={ODBC Driver 17 for SQL Server};' \
                                 'SERVER=IZDBM1010' \
                                 ';DATABASE=DBD_HR_INTG_01' \
                                 ';Authentication=ActiveDirectoryIntegrated' \
                                 ';Authentication=ActiveDirectoryPassword;TrustServerCertificate=yes'
            conn = pyodbc.connect(connection_str)
            cursor = conn.cursor()
            cursor.execute("SET TRANSACTION ISOLATION LEVEL READ UNCOMMITTED;")
            connectionURL = URL.create("mssql+pyodbc", query={"odbc_connect": connection_str})
            connectionEngine = create_engine(connectionURL)

            # Fetch ServiceNow values
            sql = f"SELECT ComponentName,Impact,Urgency,Hot,Service,Issue,AssignmentGroup,AssignedTo FROM {hr_intg_db}.dbo.SNOWConfig (NOLOCK) ORDER BY 1"
            snow_data = pd.read_sql(sql, connectionEngine)
            retry_flag = False
            return snow_data
        except Exception as e:
            print(e)
            logger.info("Retry count:" + str(retry_count))
            retry_count = retry_count + 1
            logger.info(traceback.format_exc())
            time.sleep(db_retry_interval)
            if retry_count >= db_retry_count:
                call_servicenow(traceback.format_exc(), scriptname, createincident_flag, pd.DataFrame())
                sys.exit("!!!ERROR!!!")
            else:
                pass


##############################################################
# Execute shell command
##############################################################
def execute_shell_commands(cmd,
                           scriptname,
                           createincident_flag,
                           snow_data):
    try:
        status = os.system(cmd)
        if status == 0:
            logger.info("Executed successfully: " + cmd)
        else:
            logger.info("Executed failed: " + cmd)
            raise ("Executed failed: " + cmd)
    except:
        logger.info(traceback.format_exc())
        call_servicenow(traceback.format_exc(), scriptname, createincident_flag, snow_data)
        sys.exit("!!!ERROR!!!")


##############################################################
# Call ServiceNow
##############################################################
def call_servicenow(error_desc,
                    component_name,
                    createincident_flag,
                    snow_data_all,
                    Impact=3,
                    Urgency=3,
                    Hot='N',
                    Service='Integration',
                    Issue='Performance',
                    AssignmentGroup="Integration Support",
                    AssignedTo='unassigned'
                    ):
    newline = ""
    snow_response = ""
    incidentnumber = ""
    incidenturl = config.get("incidenturl")
    from_address = config.get("from_address")
    send_email_to = config.get("to_email")
    environment = config.get("environment")
    smtphostname = config.get("smtphostname")
    servicenowurl = config.get("servicenowurl")
    snow_data = pd.DataFrame()
    if not snow_data_all.empty:
        snow_data = snow_data_all.query("`ComponentName` == '" + component_name + "'")
        if snow_data.empty:
            snow_data = snow_data_all.query("`ComponentName` == 'Default'")

    try:
        if createincident_flag == "yes":
            logger.info("Service now incident creation started")
            newline = '<br>'
            if snow_data.empty:
                logger.info(
                    "Service now dataframe is empty, so using the default values")
            else:
                Impact = snow_data['Impact'].iloc[0]
                Urgency = snow_data['Urgency'].iloc[0]
                Hot = snow_data['Hot'].iloc[0]
                Service = snow_data['Service'].iloc[0]
                Issue = snow_data['Issue'].iloc[0]
                AssignmentGroup = snow_data['AssignmentGroup'].iloc[0]
                AssignedTo = snow_data['AssignedTo'].iloc[0]

            delay = 0
            logfile_location = f"logs/{os.getenv('LOG_FILE')}"
            error_desc = "Error Details: " + newline + newline + error_desc + newline + newline
            error_desc += "Please check the log file for detailed execution information - " + logfile_location + newline + newline
            short_desc = component_name + ".py script execution failed for file group (" + component_name + ") at " + CurrentDT.strftime(
                "%b %d %Y %H:%M:%S")
            component_type = "PYTHON*" + component_name
            inc_nbr, snow_response = utils.SNOWCalls.SNOWCall_Extended(SNOWUrl=servicenowurl,
                                                                       ShortDesc=short_desc,
                                                                       Desc=str(error_desc),
                                                                       Impact=Impact,
                                                                       Urgency=Urgency,
                                                                       Hot=Hot,
                                                                       Service=Service,
                                                                       Issue=Issue,
                                                                       AssignmentGroup=AssignmentGroup,
                                                                       AssignedTo=AssignedTo,
                                                                       component=component_type,
                                                                       delay=delay)
            print(inc_nbr)
            print(snow_response)
            if inc_nbr.upper().find("INC") < 0:  # If the SNOW Wrapper did not return an INC, something happened,
                raise ("!!!INCIDENT CREATION FAILED!!!")
                sys.exit("!!!ERROR!!!")
            else:
                incidentnumber = inc_nbr
                logger.info(
                    "Service now incident creation completed. Incident number: " + incidentnumber)
        else:
            incidentnumber = ""

    except:
        logger.info(traceback.format_exc())
        incidentnumber = ""

    incidentstring = ""
    if not (incidentnumber):
        incidentstring = "Incident Number: NONE" + newline + newline
    else:
        incidentstring += incidenturl + incidentnumber + newline + newline

    incident_message_body = """\
                   <html>
                     <head></head>
                     <body>
                       <p style="font-family:'Bookman Old Style'"> """ + component_name + """ script failed <br><br>
                          <b>Failed Date Time:</b> <br>""" + CurrentDT.strftime("%b %d %Y %H:%M:%S") + """<br><br>
                          <b>Error Details:</b> <br>""" + error_desc + """<br><br>
                          <b>Snow Wrapper Status:</b> <br>""" + snow_response + """<br><br>
                          <b>Incident Number:</b> """ + str(incidentstring) + """<br><br>
                       </p>
                     </body>
                   </html>
                   """
    utils.Email.sendemail(from_address,
                          send_email_to,
                          environment + " - " + component_name + " script execution failed at " + CurrentDT.strftime(
                              "%b %d %Y %H:%M:%S"),
                          incident_message_body,
                          smtphostname)
    return incidentnumber


##############################################################
# Function to execute DB query based on argument
##############################################################
def execute_db_query(createincident_flag,
                     query,
                     snow_data):
    try:
        dl_retry_flag = True
        dl_retry_count = 0
        dlock_retry_count = config.get("dlock_retry_count")
        dlock_retry_interval = config.get("dlock_retry_interval")
        while dl_retry_flag and dl_retry_count < dlock_retry_count:
            try:
                logger.info("Executing Query: " + query)
                result = cursor.execute(query)
                conn.commit()
                dl_retry_flag = False
                return result
            except Exception as er:
                print(er)
                logger.info(traceback.format_exc())
                dl_retry_count = dl_retry_count + 1
                logger.info("Dead Lock Retry count:" + str(dl_retry_count))
                time.sleep(dlock_retry_interval)
                if dl_retry_count >= dlock_retry_count:
                    sys.exit("!!!ERROR!!!")
                else:
                    pass
    except:
        logger.info(traceback.format_exc())
        call_servicenow(traceback.format_exc(), interface_name + ".py", createincident_flag, snow_data)
        sys.exit("!!!ERROR!!!")


##############################################################
# Function to return result based on query argument
##############################################################
def extract_result_db(createincident_flag,
                      query,
                      scriptname,
                      snow_data):
    try:
        result = []
        result = cursor.execute(query).fetchall()
        return result
    except:
        logger.info(traceback.format_exc())
        call_servicenow(traceback.format_exc(), scriptname, createincident_flag, snow_data)
        sys.exit("!!!ERROR!!!")


##############################################################
# Read File
##############################################################
def read_file(file_path):
    file_content = ""
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content


##############################################################
# get the process id based on the script name
##############################################################
def get_pids_by_script_name(script_name):
    pids = []
    for proc in psutil.process_iter():
        try:
            cmdline = proc.cmdline()
            name = proc.name()
            pid = proc.pid
        except psutil.NoSuchProcess:
            continue
        if (name == "python3" and
                len(cmdline) > 1 and
                cmdline[1].endswith(script_name)):
            pids.append(pid)
    return pids


##############################################################
# column Decryption
##############################################################
def columnDecryption(df, columns_to_decrypt):
    def decrypt_text(x):
        if pd.notnull(x) and x:
            try:
                return unpad(cipher.decrypt(base64.b64decode(x)), AES.block_size).decode()
            except Exception as e:
                logger.debug(f"Error while decrypting text: {x}")
                raise Exception(f"Decryption Failed: {e}")
        else:
            return x

    def is_match(in_text, values):
        # ignore case, strip white space
        in_text = in_text.strip().lower()
        if in_text in [col.lower() for col in values]:
            return True
        else:
            return False

    column_key = config.get("column_key")
    column_decrypt = read_file(column_key)
    column_decrypt_key = base64.b64decode(column_decrypt)
    logger.info("Decrypt key and pgp key fetch completed")
    cipher = AES.new(column_decrypt_key, AES.MODE_ECB)
    decrypt_columns = columns_to_decrypt.split(",")
    logger.info(f"Found cols: {df.columns}")
    for column in decrypt_columns:
        if is_match(column, df.columns):
            logger.info("Decrypting Column: " + column)
            df[column] = df[column].apply(decrypt_text)
            logger.info("Decryption Completed For Column: " + column)
    return df

##############################################################
# pre process for the script to check the run and log
##############################################################
def pre_process_check(JobAuditId,
                      scriptname,
                      snow_data,
                      createincident_flag,
                      script_base_name):
    # log record in job audit table
    audit_insert = f"INSERT INTO {hr_intg_db}.dbo.JobAudit (JobAuditId, " \
                   "JobType, " \
                   "ScriptName, " \
                   "StartTime, " \
                   "Status) values" \
                   " ('" + JobAuditId + "', 'Extract', '" + script_base_name + "', GETDATE(),'STARTED')"

    execute_db_query(createincident_flag,
                     audit_insert,
                     snow_data)

    # Get the process id and chek if the script is already running
    if RunningPlatform == "LINUX":
        pids = get_pids_by_script_name(scriptname)
        log_reason = "SUCCESS"

        print("Process ID for execution:" + str(pids))

        if len(pids) > 1:
            log_reason = "The script " + script_base_name + " is already running, so skipping the execution. Process ID: " + str(
                pids) + ". Please validate"
            # Create incident, since previous instance is already running
            incident_number = call_servicenow(log_reason, createincident_flag, snow_data)

            logger.info(log_reason)

            # Update FileGroupAudit, since previous instance is already running
            audit_update = f"UPDATE{hr_intg_db}.dbo.JobAudit SET EndTime = GETDATE(), " \
                           "Status = 'SKIPPED', " \
                           "ErrorReason = '" + log_reason + "', " \
                                                            "IncidentNumber = '" + incident_number + "' " \
                                                                                                     "WHERE JobAuditId = '" + JobAuditId + "'"

            execute_db_query(createincident_flag,
                             audit_update,
                             snow_data)
    else:
        print("Process ID check is not needed in development VM:")
        log_reason = "SUCCESS"

    return log_reason


##############################################################
# post process after the dataframe is constructed
##############################################################
def post_process(FileAuditId,
                 extract_directory,
                 extract_filename,
                 extract_filename_pgp
                 ):
    file_encrypt = utils.PGPEncryptDecrypt.PGPEncryption(extract_directory, extract_filename, extract_filename_pgp)

    logger.info("PGP encryption completed for file " + extract_directory + extract_filename)

    # remove the source files
    if file_encrypt == "SUCCESS":
        if os.path.isfile(extract_directory + extract_filename):
            os.remove(extract_directory + extract_filename)
    else:
        raise ("File encryption failed for " + extract_directory + extract_filename)

    logger.info("Removed the file" + extract_directory + extract_filename)

    # Update fileaudit success
    audit_update = f"UPDATE {hr_intg_db}.dbo.FileAudit SET EndTime = GETDATE(), Status = 'SUCCESS' " \
                   "WHERE FileAuditId = '" + FileAuditId + "'"

    execute_db_query(createincident_flag,
                     audit_update,
                     snow_data)


##############################################################
# Truncate working tables
##############################################################
def truncate_Tables(truncate_list, createincident_flag, snow_data):
    for trncs in truncate_list:
        query = "TRUNCATE TABLE " + trncs
        execute_db_query(createincident_flag,
                         query,
                         snow_data)
        logger.info("Truncate query executed: " + query)

if __name__ == '__main__':

    ##########################Main Starts Here###############
    scriptname = sys.argv[0]
    execution_mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'DEBUG'
    load_type = sys.argv[2] if len(sys.argv) > 2 and sys.argv[2] in ['FULL', 'DELTA'] else 'FULL'
    createincident_flag = "yes"
    script_base_name = os.path.basename(scriptname)
    RunningPlatform = str(platform.system()).upper()
    logger.info("##################Script Execution Started ##################")
    payroll_db = config.get("payroll_db")
    hr_intg_db = config.get("hr_intg_db")
    snow_data = load_db_param(script_base_name, createincident_flag)
    logger.info("DB Connection Established")
    custom_faiure = False  # To handle snow call for custom failures
    try:
        # Assign job audi id
        JobAuditId = str(uuid.uuid4())

        # Construct the extract filename based on load type
        if load_type.upper() == "FULL":
            extract_file_prefix = "learning_Edcast_Genesis_Full_"
        else:
            extract_file_prefix = "learning_Edcast_Genesis_Delta_"

        # Construct filename
        extract_directory = ""
        extract_filename = extract_file_prefix + time.strftime("%Y%m%d%H%M%S") + ".csv"
        extract_filename_pgp = extract_filename + ".pgp"

        logger.info(f"Extract filename constructed: {extract_filename}")

        # list all the working tables
        tuncate_tbl_list = [f"{hr_intg_db}.Extracts.GENESIS_STAGE_EMP_INFO",
                            f"{hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXPORT_INFO",
                            f"{hr_intg_db}.Extracts.GENESIS_STAGE_GLCOMPANY_INFO",
                            f"{hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXP_COMP_INFO",

                            f"{hr_intg_db}.Extracts.Genesis_STG",
                            f"{hr_intg_db}.Extracts.GENESIS_STAGE_NEW",
                            f"{hr_intg_db}.Extracts.GENESIS_STAGE_UPDATES"]

        tuncate_tbl_list_full = [
            f"{hr_intg_db}.dbo.Genesis"
        ]

        # Common Queries

        GENESIS_STAGE_EMP_INFO_1 = f"""
                    insert into {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_INFO
                    select
                        FIRST_NAME
                        ,LAST_NAME
                        ,ContactDetail_EmailAddress
                        ,[NETWORK_ID]
                        ,[HEALTHSTREAM_ID]
                        ,[Employee]
                        ,[BADGE_NUMBER]
                        ,[MIDDLE_NAME]
                        ,[Preferred_FullName]
                        ,EMPL_STATUS
                        ,[RelationshipToOrganization]
                        ,JOBCODE
                        ,JOBCODE_DESCR
                        ,HIRE_DT
                        ,REHIRE_DT
                        ,TERMINATION_DT
                        ,Years_of_service
                        ,JOBCODE_FLSA_STATUS
                        ,[FTE]
                        ,[WorkSchedule]
                        ,DEPTID
                        ,DEPT_DESCR
                        ,[REPORTING_LOCATION]
                        ,[REPORTING_LOCATION_DESCR]
                        ,[PAYGROUP]
                        ,[Entity]
                        ,[PositionLevel]
                        ,[Position]
                        ,[PostionName]
                        ,[PositionFamily]
                        ,[PositionCategory]
                        ,[PositionSubCategory]
                        ,[MANAGER_NETWORK_ID]
                        ,[MANAGER_ID]
                        ,[MANAGER_HEALTHSTREAM_ID]
                        ,[REPORTS_TO_NAME]
                        ,[MANAGER_EMAIL]
                        ,[BIRTHDATE]
                        ,[RACE_ETHNICITY]
                        ,[Gender_State]
                        ,[LANGUAGE]
                        ,[HOME_PHONE]
                        ,IsManager
                        ,PAYGROUP_DESCR
                        --,LOCATION
                     FROM {hr_intg_db}.dbo.Employee_V  WITH (NOLOCK)
                """

        GENESIS_STAGE_EMP_EXPORT_INFO_2 = f"""
                    insert into {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXPORT_INFO
                    select
                        Employee,
                        MAX_SYS,
                        ActionReason,
                        EffectiveDate  from (
                            select
                                employee,
                                systemtimestamp as max_sys,
                                row_number() over(partition by employee order by cast(systemtimestamp as datetime2 ) DESC) as rn,
                                ActionReason,
                                EffectiveDate
                            from {payroll_db}.[dbo].[REPSET_WorkAssignmentExport_Active]  WITH (NOLOCK)
                            where (ChangedFields LIKE 'POSITION%') AND (ActionReason <> '' or ActionReason  is not null)
                    ) z where rn = 1
                """

        GENESIS_STAGE_GLCOMPANY_INFO_3 = f"""
                    insert into {hr_intg_db}.Extracts.GENESIS_STAGE_GLCOMPANY_INFO
                    SELECT [Company]
                          ,[Name]
                    FROM {hr_intg_db}.[dbo].[Repset_GLCompany_Active]  WITH (NOLOCK)
                """

        GENESIS_STAGE_EMP_EXP_COMP_INFO_4 = f"""
                    insert INTO {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXP_COMP_INFO
                    SELECT
                            FIRST_NAME                                                                          AS      [first_name]
                            ,LAST_NAME                                                                          AS      [last_name]
                            ,ContactDetail_EmailAddress                                                                 AS      [email]
                            ,[NETWORK_ID]                                                                       AS      [external_id]
                            ,[NETWORK_ID]                                                                       AS      [network_id]
                            ,[HEALTHSTREAM_ID]                                                          AS      [healthstream_id]
                            ,A.[Employee]                                                                               AS      [employee_id]
                            ,[BADGE_NUMBER]                                                                     AS      [badge_number]
                            ,[MIDDLE_NAME]                                                                      AS      [middle_name]
                            ,[Preferred_FullName]                                                       AS      [preferred_full_name]
                            ,CASE
                                WHEN EMPL_STATUS = 'ACTIVE'                                     THEN 'active'
                                WHEN EMPL_STATUS = 'INACTIVE'                           THEN 'inactive'
                                WHEN EMPL_STATUS = 'LEAVE'                                      THEN 'inactive'
                                WHEN EMPL_STATUS = 'SUSPENDED'                          THEN 'suspended'
                                WHEN EMPL_STATUS = 'TERMINATED WITH PAY'        THEN 'suspended'
                                WHEN EMPL_STATUS = 'TERMINATED WO PAY'          THEN 'suspended'
                            ELSE EMPL_STATUS END                                                        AS      [status]
                            ,[RelationshipToOrganization]                                       AS      [relationship_to_org]
                            ,JOBCODE                                                                            AS  [job_code]
                            ,JOBCODE_DESCR                                                                      AS      [job_code_descr]
                            ,CONVERT(VARCHAR,CAST(NULLIF(HIRE_DT        ,'')    AS DATE),1)             AS      [initial_hire_date]
                            ,CONVERT(VARCHAR,CAST(NULLIF(REHIRE_DT,'')                  AS DATE),1)     AS      [rehire_date]
                            ,CONVERT(VARCHAR,CAST(NULLIF(B.EFFECTIVEDATE,'')    AS DATE),1) AS  [effective_date]
                            ,[ActionReason]                                                                     AS      [action_reason]
                            ,CONVERT(VARCHAR,CAST(NULLIF(EffectiveDate,'')      AS DATE),1)                     AS      [action_reason_eff_date]
                            ,CONVERT(VARCHAR,CAST(NULLIF(TERMINATION_DT  ,'')   AS DATE),1)     AS      [termination_date]
                            ,CONVERT(DECIMAL(10,2),[Years_of_service])          AS      [years_service]
                            ,JOBCODE_FLSA_STATUS                                                        AS      [flsa]
                            ,CONVERT(DECIMAL(10,2),[FTE])                                       AS      [fte]
                            ,[WorkSchedule]                                                                     AS      [work_schedule]
                            ,DEPTID                                                                                     AS      [department_id]
                            ,DEPT_DESCR                                                                         AS      [department_name]
                            ,[REPORTING_LOCATION]                                                       AS      [reporting_location_id]
                            ,[REPORTING_LOCATION_DESCR]                                         AS      [reporting_location_name]
                            ,[PAYGROUP]                                                                         AS      [paygroup]
                            ,[Entity]                                                                           AS  [entity]
                            ,E.[Name]                                                                           AS      [entity_name]
                            ,[PositionLevel]                                                            AS      [position_level]
                            ,[Position]                                                                         AS      [position_id]
                            ,[PostionName]                                                                      AS      [position_name]
                            ,[PositionFamily]                                                           AS      [position_family]
                            ,[PositionCategory]                                                         AS      [position_category]
                            ,[PositionSubCategory]                                                      AS      [position_sub_category]
                            ,[MANAGER_NETWORK_ID]                                                       AS      [reports_to_network_id]
                            ,[MANAGER_ID]                                                                       AS      [reports_to_employee_id]
                            ,[MANAGER_HEALTHSTREAM_ID]                                          AS      [reports_to_healthstream_id]
                            ,[REPORTS_TO_NAME]                                                          AS      [reports_to_name]
                            ,[MANAGER_EMAIL]                                                            AS      [manager_email]
                            ,CONVERT(VARCHAR,CAST(NULLIF([BIRTHDATE],'')        AS DATE),1)             AS      [birthdate]
                            ,[RACE_ETHNICITY]                                                           AS      [race_ethnicity]
                            ,[Gender_State]                                                                     AS      [gender]
                            ,[LANGUAGE]                                                                         AS      [preferred_language]
                            ,[HOME_PHONE]                                                                       AS      [home_phone]
                            ,CASE
                                WHEN IsManager = 'Yes' THEN 'Y'
                                WHEN IsManager = 'No'  THEN 'N'
                            ELSE '' END AS  [is_manager] ,
                            A.PAYGROUP_DESCR AS MINISTRY
                            --,[LOCATION]
                    FROM        {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_INFO A
                            LEFT JOIN {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXPORT_INFO B ON A.Employee = B.EMPLOYEE
                            LEFT JOIN {hr_intg_db}.[dbo].[Repset_GLCompany_Active] E   WITH (NOLOCK) ON A.Entity = E.Company
                    WHERE (PAYGROUP_DESCR <> 'EXECUTIVE DIV NP' OR PAYGROUP_DESCR <> 'ST VINCENT MIN NP') AND EMPL_STATUS IN ('Active','Leave')
                    OR
                    cast(TERMINATION_DT as date) >=  DATEADD(month, - 3, GETDATE())
                """

        # FULL Load Specific Queries

        Genesis_5 = f"""
                    Insert into {hr_intg_db}.[dbo].[Genesis](
                       [first_name]
                      ,[last_name]
                      ,[email]
                      ,[external_id]
                      ,[network_id]
                      ,[healthstream_id]
                      ,[employee_id]
                      ,[badge_number]
                      ,[middle_name]
                      ,[preferred_full_name]
                      ,[status]
                      ,[relationship_to_org]
                      ,[job_code]
                      ,[job_code_descr]
                      ,[initial_hire_date]
                      ,[rehire_date]
                      ,[effective_date]
                      ,[action_reason]
                      ,[action_reason_eff_date]
                      ,[termination_date]
                      ,[years_service]
                      ,[flsa]
                      ,[fte]
                      ,[work_schedule]
                      ,[department_id]
                      ,[department_name]
                      ,[reporting_location_id]
                      ,[reporting_location_name]
                      ,[paygroup]
                      ,[entity]
                      ,[entity_name]
                      ,[position_level]
                      ,[position_id]
                      ,[position_name]
                      ,[position_family]
                      ,[position_category]
                      ,[position_sub_category]
                      ,[reports_to_network_id]
                      ,[reports_to_employee_id]
                      ,[reports_to_healthstream_id]
                      ,[reports_to_name]
                      ,[manager_email]
                      ,[birthdate]
                      ,[race_ethnicity]
                      ,[gender]
                      ,[preferred_language]
                      ,[home_phone]
                      ,[is_manager]
                      ,[EdCast_Checksum]
                      ,MINISTRY
                      --,LOCATION
                      )
                SELECT
                       [first_name]
                      ,[last_name]
                      ,[email]
                      ,[external_id]
                      ,[network_id]
                      ,[healthstream_id]
                      ,[employee_id]
                      ,[badge_number]
                      ,[middle_name]
                      ,[preferred_full_name]
                      ,[status]
                      ,[relationship_to_org]
                      ,[job_code]
                      ,[job_code_descr]
                      ,[initial_hire_date]
                      ,[rehire_date]
                      ,[effective_date]
                      ,[action_reason]
                      ,[action_reason_eff_date]
                      ,[termination_date]
                      ,[years_service]
                      ,[flsa]
                      ,[fte]
                      ,[work_schedule]
                      ,[department_id]
                      ,[department_name]
                      ,[reporting_location_id]
                      ,[reporting_location_name]
                      ,[paygroup]
                      ,[entity]
                      ,[entity_name]
                      ,[position_level]
                      ,[position_id]
                      ,[position_name]
                      ,[position_family]
                      ,[position_category]
                      ,[position_sub_category]
                      ,[reports_to_network_id]
                      ,[reports_to_employee_id]
                      ,[reports_to_healthstream_id]
                      ,[reports_to_name]
                      ,[manager_email]
                      ,[birthdate]
                      ,[race_ethnicity]
                      ,[gender]
                      ,[preferred_language]
                      ,[home_phone]
                      ,[is_manager]
                    ,hashbytes('SHA2_512',
                        isnull(CONVERT(VARCHAR,[first_name]),'') +
                        isnull(CONVERT(VARCHAR,[last_name]),'') +
                        isnull(CONVERT(VARCHAR,[email]),'') +
                        isnull(CONVERT(VARCHAR,[external_id]),'') +
                        isnull(CONVERT(VARCHAR,[network_id]),'') +
                        isnull(CONVERT(VARCHAR,[healthstream_id]),'') +
                        isnull(CONVERT(VARCHAR,[employee_id]),'') +
                        isnull(CONVERT(VARCHAR,[badge_number]),'') +
                        isnull(CONVERT(VARCHAR,[middle_name]),'') +
                        isnull(CONVERT(VARCHAR,[preferred_full_name]),'') +
                        isnull(CONVERT(VARCHAR,[status]),'') +
                        isnull(CONVERT(VARCHAR,[relationship_to_org]),'') +
                        isnull(CONVERT(VARCHAR,[job_code]),'') +
                        isnull(CONVERT(VARCHAR,[job_code_descr]),'') +
                        isnull(CONVERT(VARCHAR,[initial_hire_date]),'') +
                        isnull(CONVERT(VARCHAR,[rehire_date]),'') +
                        isnull(CONVERT(VARCHAR,[effective_date]),'') +
                        isnull(CONVERT(VARCHAR,[action_reason]),'') +
                        isnull(CONVERT(VARCHAR,[action_reason_eff_date]),'') +
                        isnull(CONVERT(VARCHAR,[termination_date]),'') +
                        isnull(CONVERT(VARCHAR,[years_service]),'') +
                        isnull(CONVERT(VARCHAR,[flsa]),'') +
                        isnull(CONVERT(VARCHAR,[fte]),'') +
                        isnull(CONVERT(VARCHAR,[work_schedule]),'') +
                        isnull(CONVERT(VARCHAR,[department_id]),'') +
                        isnull(CONVERT(VARCHAR,[department_name]),'') +
                        isnull(CONVERT(VARCHAR,[reporting_location_id]),'') +
                        isnull(CONVERT(VARCHAR,[reporting_location_name]),'') +
                        isnull(CONVERT(VARCHAR,[paygroup]),'') +
                        isnull(CONVERT(VARCHAR,[entity]),'') +
                        isnull(CONVERT(VARCHAR,[entity_name]),'') +
                        isnull(CONVERT(VARCHAR,[position_level]),'') +
                        isnull(CONVERT(VARCHAR,[position_id]),'') +
                        isnull(CONVERT(VARCHAR,[position_name]),'') +
                        isnull(CONVERT(VARCHAR,[position_family]),'') +
                        isnull(CONVERT(VARCHAR,[position_category]),'') +
                        isnull(CONVERT(VARCHAR,[position_sub_category]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_network_id]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_employee_id]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_healthstream_id]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_name]),'') +
                        isnull(CONVERT(VARCHAR,[manager_email]),'') +
                        isnull(CONVERT(VARCHAR,[birthdate]),'') +
                        isnull(CONVERT(VARCHAR,[race_ethnicity]),'') +
                        isnull(CONVERT(VARCHAR,[gender]),'') +
                        isnull(CONVERT(VARCHAR,[preferred_language]),'') +
                        isnull(CONVERT(VARCHAR,[home_phone]),'')+
                        isnull(CONVERT(VARCHAR,[is_manager]),'')
                    ) as EdCast_Checksum
                    ,MINISTRY
                    --,LOCATION
                FROM {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXP_COMP_INFO
                """

        # DELTA Load Specific Queries

        Genesis_STG_6 = f"""
                    Insert into {hr_intg_db}.[Extracts].[Genesis_STG](
                    [first_name]
                      ,[last_name]
                      ,[email]
                      ,[external_id]
                      ,[network_id]
                      ,[healthstream_id]
                      ,[employee_id]
                      ,[badge_number]
                      ,[middle_name]
                      ,[preferred_full_name]
                      ,[status]
                      ,[relationship_to_org]
                      ,[job_code]
                      ,[job_code_descr]
                      ,[initial_hire_date]
                      ,[rehire_date]
                      ,[effective_date]
                      ,[action_reason]
                      ,[action_reason_eff_date]
                      ,[termination_date]
                      ,[years_service]
                      ,[flsa]
                      ,[fte]
                      ,[work_schedule]
                      ,[department_id]
                      ,[department_name]
                      ,[reporting_location_id]
                      ,[reporting_location_name]
                      ,[paygroup]
                      ,[entity]
                      ,[entity_name]
                      ,[position_level]
                      ,[position_id]
                      ,[position_name]
                      ,[position_family]
                      ,[position_category]
                      ,[position_sub_category]
                      ,[reports_to_network_id]
                      ,[reports_to_employee_id]
                      ,[reports_to_healthstream_id]
                      ,[reports_to_name]
                      ,[manager_email]
                      ,[birthdate]
                      ,[race_ethnicity]
                      ,[gender]
                      ,[preferred_language]
                      ,[home_phone]
                      ,[is_manager]
                      ,[EdCast_Checksum]
                      ,Ministry
                      --,LOCATION
                      )
                SELECT
                    [first_name]
                      ,[last_name]
                      ,[email]
                      ,[external_id]
                      ,[network_id]
                      ,[healthstream_id]
                      ,[employee_id]
                      ,[badge_number]
                      ,[middle_name]
                      ,[preferred_full_name]
                      ,[status]
                      ,[relationship_to_org]
                      ,[job_code]
                      ,[job_code_descr]
                      ,[initial_hire_date]
                      ,[rehire_date]
                      ,[effective_date]
                      ,[action_reason]
                      ,[action_reason_eff_date]
                      ,[termination_date]
                      ,[years_service]
                      ,[flsa]
                      ,[fte]
                      ,[work_schedule]
                      ,[department_id]
                      ,[department_name]
                      ,[reporting_location_id]
                      ,[reporting_location_name]
                      ,[paygroup]
                      ,[entity]
                      ,[entity_name]
                      ,[position_level]
                      ,[position_id]
                      ,[position_name]
                      ,[position_family]
                      ,[position_category]
                      ,[position_sub_category]
                      ,[reports_to_network_id]
                      ,[reports_to_employee_id]
                      ,[reports_to_healthstream_id]
                      ,[reports_to_name]
                      ,[manager_email]
                      ,[birthdate]
                      ,[race_ethnicity]
                      ,[gender]
                      ,[preferred_language]
                      ,[home_phone]
                      ,[is_manager]
                    ,hashbytes('SHA2_512',
                        isnull(CONVERT(VARCHAR,[first_name]),'') +
                        isnull(CONVERT(VARCHAR,[last_name]),'') +
                        isnull(CONVERT(VARCHAR,[email]),'') +
                        isnull(CONVERT(VARCHAR,[external_id]),'') +
                        isnull(CONVERT(VARCHAR,[network_id]),'') +
                        isnull(CONVERT(VARCHAR,[healthstream_id]),'') +
                        isnull(CONVERT(VARCHAR,[employee_id]),'') +
                        isnull(CONVERT(VARCHAR,[badge_number]),'') +
                        isnull(CONVERT(VARCHAR,[middle_name]),'') +
                        isnull(CONVERT(VARCHAR,[preferred_full_name]),'') +
                        isnull(CONVERT(VARCHAR,[status]),'') +
                        isnull(CONVERT(VARCHAR,[relationship_to_org]),'') +
                        isnull(CONVERT(VARCHAR,[job_code]),'') +
                        isnull(CONVERT(VARCHAR,[job_code_descr]),'') +
                        isnull(CONVERT(VARCHAR,[initial_hire_date]),'') +
                        isnull(CONVERT(VARCHAR,[rehire_date]),'') +
                        isnull(CONVERT(VARCHAR,[effective_date]),'') +
                        isnull(CONVERT(VARCHAR,[action_reason]),'') +
                        isnull(CONVERT(VARCHAR,[action_reason_eff_date]),'') +
                        isnull(CONVERT(VARCHAR,[termination_date]),'') +
                        isnull(CONVERT(VARCHAR,[years_service]),'') +
                        isnull(CONVERT(VARCHAR,[flsa]),'') +
                        isnull(CONVERT(VARCHAR,[fte]),'') +
                        isnull(CONVERT(VARCHAR,[work_schedule]),'') +
                        isnull(CONVERT(VARCHAR,[department_id]),'') +
                        isnull(CONVERT(VARCHAR,[department_name]),'') +
                        isnull(CONVERT(VARCHAR,[reporting_location_id]),'') +
                        isnull(CONVERT(VARCHAR,[reporting_location_name]),'') +
                        isnull(CONVERT(VARCHAR,[paygroup]),'') +
                        isnull(CONVERT(VARCHAR,[entity]),'') +
                        isnull(CONVERT(VARCHAR,[entity_name]),'') +
                        isnull(CONVERT(VARCHAR,[position_level]),'') +
                        isnull(CONVERT(VARCHAR,[position_id]),'') +
                        isnull(CONVERT(VARCHAR,[position_name]),'') +
                        isnull(CONVERT(VARCHAR,[position_family]),'') +
                        isnull(CONVERT(VARCHAR,[position_category]),'') +
                        isnull(CONVERT(VARCHAR,[position_sub_category]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_network_id]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_employee_id]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_healthstream_id]),'') +
                        isnull(CONVERT(VARCHAR,[reports_to_name]),'') +
                        isnull(CONVERT(VARCHAR,[manager_email]),'') +
                        isnull(CONVERT(VARCHAR,[birthdate]),'') +
                        isnull(CONVERT(VARCHAR,[race_ethnicity]),'') +
                        isnull(CONVERT(VARCHAR,[gender]),'') +
                        isnull(CONVERT(VARCHAR,[preferred_language]),'') +
                        isnull(CONVERT(VARCHAR,[home_phone]),'') +
                        isnull(CONVERT(VARCHAR,[is_manager]),'')
                    ) as EdCast_Checksum
                    ,Ministry
                    --,LOCATION
                FROM {hr_intg_db}.Extracts.GENESIS_STAGE_EMP_EXP_COMP_INFO
                """

        GENESIS_STAGE_NEW_7 = f"""
                    insert into {hr_intg_db}.Extracts.GENESIS_STAGE_NEW
                    SELECT distinct a.*
                    FROM {hr_intg_db}.Extracts.Genesis_STG a
                    WHERE (
                        a.employee_id not in (select distinct employee_id from {hr_intg_db}.dbo.Genesis)
                    ) AND ISNULL(NULLIF(a.reporting_location_id, ''), '-') {filter_locations.csv_locations_exclude}

                """

        GENESIS_STAGE_UPDATES_8 = f"""
                    INSERT INTO {hr_intg_db}.Extracts.GENESIS_STAGE_UPDATES
                    SELECT distinct a.*
                    FROM {hr_intg_db}.Extracts.Genesis_STG a
                    inner join {hr_intg_db}.dbo.Genesis b
                    on a.employee_id = b.employee_id
                    and a.EdCast_Checksum <> b.EdCast_Checksum
WHERE ISNULL(NULLIF(a.reporting_location_id, ''), '-') {filter_locations.csv_locations_exclude}

                """

        Genesis_Insert_9 = f"""
                    INSERT INTO {hr_intg_db}.dbo.Genesis
                    select [first_name]
                          ,[last_name]
                          ,[email]
                          ,[external_id]
                          ,[network_id]
                          ,[healthstream_id]
                          ,[employee_id]
                          ,[badge_number]
                          ,[middle_name]
                          ,[preferred_full_name]
                          ,[status]
                          ,[relationship_to_org]
                          ,[job_code]
                          ,[job_code_descr]
                          ,[initial_hire_date]
                          ,[rehire_date]
                          ,[effective_date]
                          ,[action_reason]
                          ,[action_reason_eff_date]
                          ,[termination_date]
                          ,[years_service]
                          ,[flsa]
                          ,[fte]
                          ,[work_schedule]
                          ,[department_id]
                          ,[department_name]
                          ,[reporting_location_id]
                          ,[reporting_location_name]
                          ,[paygroup]
                          ,[entity]
                          ,[entity_name]
                          ,[position_level]
                          ,[position_id]
                          ,[position_name]
                          ,[position_family]
                          ,[position_category]
                          ,[position_sub_category]
                          ,[reports_to_network_id]
                          ,[reports_to_employee_id]
                          ,[reports_to_healthstream_id]
                          ,[reports_to_name]
                          ,[manager_email]
                          ,[birthdate]
                          ,[race_ethnicity]
                          ,[gender]
                          ,[preferred_language]
                          ,[home_phone]
                          ,[is_manager]
                          ,[EdCast_Checksum]
                          ,Ministry
                          ,[InsertDT]
                    from {hr_intg_db}.Extracts.GENESIS_STAGE_NEW
                    where employee_id is not NULL 
                    AND ISNULL(NULLIF(reporting_location_id, ''), '-') {filter_locations.csv_locations_exclude}

                """

        Genesis_Update_10 = f"""
                    UPDATE {hr_intg_db}.dbo.Genesis
                    SET
                           [first_name]                                 =tmp.[first_name]
                          ,[last_name]                                  =tmp.[last_name]
                          ,[email]                                              =tmp.[email]
                          ,[external_id]                                =tmp.[external_id]
                          ,[network_id]                                 =tmp.[network_id]
                          ,[healthstream_id]                    =tmp.[healthstream_id]
                          ,[employee_id]                                =tmp.[employee_id]
                          ,[badge_number]                               =tmp.[badge_number]
                          ,[middle_name]                                =tmp.[middle_name]
                          ,[preferred_full_name]            =tmp.[preferred_full_name]
                          ,[status]                                             =tmp.[status]
                          ,[relationship_to_org]            =tmp.[relationship_to_org]
                          ,[job_code]                                   =tmp.[job_code]
                          ,[job_code_descr]                             =tmp.[job_code_descr]
                          ,[initial_hire_date]                  =tmp.[initial_hire_date]
                          ,[rehire_date]                                =tmp.[rehire_date]
                          ,[effective_date]                             =tmp.[effective_date]
                          ,[action_reason]                              =tmp.[action_reason]
                          ,[action_reason_eff_date]         =tmp.[action_reason_eff_date]
                          ,[termination_date]                   =tmp.[termination_date]
                          ,[years_service]                              =tmp.[years_service]
                          ,[flsa]                                               =tmp.[flsa]
                          ,[fte]                                                =tmp.[fte]
                          ,[work_schedule]                              =tmp.[work_schedule]
                          ,[department_id]                              =tmp.[department_id]
                          ,[department_name]                    =tmp.[department_name]
                          ,[reporting_location_id]          =tmp.[reporting_location_id]
                          ,[reporting_location_name]    =tmp.[reporting_location_name]
                          ,[paygroup]                                   =tmp.[paygroup]
                          ,[entity]                                             =tmp.[entity]
                          ,[entity_name]                                =tmp.[entity_name]
                          ,[position_level]                             =tmp.[position_level]
                          ,[position_id]                                =tmp.[position_id]
                          ,[position_name]                              =tmp.[position_name]
                          ,[position_family]                    =tmp.[position_family]
                          ,[position_category]                  =tmp.[position_category]
                          ,[position_sub_category]          =tmp.[position_sub_category]
                          ,[reports_to_network_id]          =tmp.[reports_to_network_id]
                          ,[reports_to_employee_id]         =tmp.[reports_to_employee_id]
                          ,[reports_to_healthstream_id] =tmp.[reports_to_healthstream_id]
                          ,[reports_to_name]                    =tmp.[reports_to_name]
                          ,[manager_email]                              =tmp.[manager_email]
                          ,[birthdate]                                  =tmp.[birthdate]
                          ,[race_ethnicity]                             =tmp.[race_ethnicity]
                          ,[gender]                                             =tmp.[gender]
                          ,[preferred_language]                 =tmp.[preferred_language]
                          ,[home_phone]                                 =tmp.[home_phone]
                          ,[is_manager]                                 =tmp.[is_manager]
                          ,[EdCast_Checksum]                    =tmp.[EdCast_Checksum]
                          ,[Ministry]                           =tmp.[Ministry]
                          ,[InsertDT]                                   =tmp.[InsertDT]
                    FROM {hr_intg_db}.dbo.Genesis E
                    INNER JOIN {hr_intg_db}.Extracts.GENESIS_STAGE_UPDATES tmp
                    ON E.employee_id = tmp.employee_id
                """

        # Construct the master queries
        master_extract_sql_full = f"""
                    select
                               [first_name]
                              ,[last_name]
                              ,[email]
                              ,[external_id]
                              ,[network_id]
                              ,[healthstream_id]
                              ,[employee_id]
                              ,[badge_number]
                              ,[middle_name]
                              ,[preferred_full_name]
                              ,[status]
                              ,[relationship_to_org]
                              ,[job_code]
                              ,[job_code_descr]
                              ,[initial_hire_date]
                              ,[rehire_date]
                              ,[effective_date]
                              ,[action_reason]
                              ,[action_reason_eff_date]
                              ,[termination_date]
                              ,[years_service]
                              ,[flsa]
                              ,[fte]
                              ,[work_schedule]
                              ,[department_id]
                              ,[department_name]
                              ,[reporting_location_id]
                              ,[reporting_location_name]
                              ,[paygroup]
                              ,[entity]
                              ,[entity_name]
                              ,[position_level]
                              ,[position_id]
                              ,[position_name]
                              ,[position_family]
                              ,[position_category]
                              ,[position_sub_category]
                              ,[reports_to_network_id]
                              ,[reports_to_employee_id]
                              ,[reports_to_healthstream_id]
                              ,[reports_to_name]
                              ,[manager_email]
                              ,[birthdate]
                              ,[race_ethnicity]
                              ,[gender]
                              ,[preferred_language]
                              ,[home_phone]
                              ,[is_manager]
                              ,[InsertDT]
                        from {hr_intg_db}.[dbo].[Genesis]  where ISNULL(NULLIF(reporting_location_id, ''), '-') {filter_locations.csv_locations_exclude}

"""



        master_extract_sql_delta = f"""
                    SELECT
                           [first_name]
                          ,[last_name]
                          ,[email]
                          ,[external_id]
                          ,[network_id]
                          ,[healthstream_id]
                          ,[employee_id]
                          ,[badge_number]
                          ,[middle_name]
                          ,[preferred_full_name]
                          ,[status]
                          ,[relationship_to_org]
                          ,[job_code]
                          ,[job_code_descr]
                          ,[initial_hire_date]
                          ,[rehire_date]
                          ,[effective_date]
                          ,[action_reason]
                          ,[action_reason_eff_date]
                          ,[termination_date]
                          ,[years_service]
                          ,[flsa]
                          ,[fte]
                          ,[work_schedule]
                          ,[department_id]
                          ,[department_name]
                          ,[reporting_location_id]
                          ,[reporting_location_name]
                          ,[paygroup]
                          ,[entity]
                          ,[entity_name]
                          ,[position_level]
                          ,[position_id]
                          ,[position_name]
                          ,[position_family]
                          ,[position_category]
                          ,[position_sub_category]
                          ,[reports_to_network_id]
                          ,[reports_to_employee_id]
                          ,[reports_to_healthstream_id]
                          ,[reports_to_name]
                          ,[manager_email]
                          ,[birthdate]
                          ,[race_ethnicity]
                          ,[gender]
                          ,[preferred_language]
                          ,[home_phone]
                          ,[is_manager]
                          ,[InsertDT]
                    from {hr_intg_db}.Extracts.GENESIS_STAGE_NEW
                    union all
                    SELECT
                        [first_name]
                          ,[last_name]
                          ,[email]
                          ,[external_id]
                          ,[network_id]
                          ,[healthstream_id]
                          ,[employee_id]
                          ,[badge_number]
                          ,[middle_name]
                          ,[preferred_full_name]
                          ,[status]
                          ,[relationship_to_org]
                          ,[job_code]
                          ,[job_code_descr]
                          ,[initial_hire_date]
                          ,[rehire_date]
                          ,[effective_date]
                          ,[action_reason]
                          ,[action_reason_eff_date]
                          ,[termination_date]
                          ,[years_service]
                          ,[flsa]
                          ,[fte]
                          ,[work_schedule]
                          ,[department_id]
                          ,[department_name]
                          ,[reporting_location_id]
                          ,[reporting_location_name]
                          ,[paygroup]
                          ,[entity]
                          ,[entity_name]
                          ,[position_level]
                          ,[position_id]
                          ,[position_name]
                          ,[position_family]
                          ,[position_category]
                          ,[position_sub_category]
                          ,[reports_to_network_id]
                          ,[reports_to_employee_id]
                          ,[reports_to_healthstream_id]
                          ,[reports_to_name]
                          ,[manager_email]
                          ,[birthdate]
                          ,[race_ethnicity]
                          ,[gender]
                          ,[preferred_language]
                          ,[home_phone]
                          ,[is_manager]
                          ,[InsertDT]
                    from {hr_intg_db}.Extracts.GENESIS_STAGE_UPDATES
                """

        print("Script Load Type:" + load_type)

        # Send the run for pre check
        log_reason = pre_process_check(JobAuditId, scriptname, snow_data, createincident_flag,
                                       script_base_name)
        if log_reason == "SUCCESS":
            logger.info("There is no PID's for the script execution")
        else:
            custom_faiure = True
            raise ValueError(log_reason)

        if execution_mode.upper() not in ("DEBUG", "NORMAL"):
            raise ValueError("Please provide valid debug mode. Allowed DEBUG or NORMAL")

        # Truncate tables based on load type
        if load_type.upper() == "FULL":
            # For FULL load, truncate both truncate_tbl_list and truncate_tbl_list_full
            truncate_Tables(tuncate_tbl_list + tuncate_tbl_list_full, createincident_flag, snow_data)
        else:
            # For other load types, truncate only truncate_tbl_list
            truncate_Tables(tuncate_tbl_list, createincident_flag, snow_data)

        # Query the load config table
        load_config_query = f"SELECT TOP 1 * FROM {hr_intg_db}.dbo.VendorExtractConfig (NOLOCK) WHERE ExtractScriptName = '" + script_base_name + "' ORDER BY 1 DESC"
        load_config_result = extract_result_db(createincident_flag, load_config_query, script_base_name, snow_data)

        threshold_data_vol = 0
        columns_to_decrypt = "NoColumnsToDecrypt"
        for record in load_config_result:
            extract_directory = str(record[2])
            threshold_data_vol = int(record[3])
            if record[4]:
                columns_to_decrypt = str(record[4]).replace("NULL", "NoColumnsToDecrypt")

        # Execute common queries
        common_queries = [
                            GENESIS_STAGE_EMP_INFO_1,
                            GENESIS_STAGE_EMP_EXPORT_INFO_2,
                            GENESIS_STAGE_GLCOMPANY_INFO_3,
                            GENESIS_STAGE_EMP_EXP_COMP_INFO_4
                         ]
        for i, query in enumerate(common_queries, start=1):
            logger.info(f"Starting execution of Query {i}")
            execute_db_query(createincident_flag, query, snow_data)
            logger.info(f"Finished execution of Query {i}")

        if load_type.upper() == "FULL":
            # Execute FULL specific queries
            full_queries = [Genesis_5]
            for i, query in enumerate(full_queries, start=5):  # Start numbering from 5 for FULL load queries
                logger.info(f"Starting execution of Query {i} (FULL Load)")
                execute_db_query(createincident_flag, query, snow_data)
                logger.info(f"Finished execution of Query {i}")

            # Execute master query for FULL load
            logger.info("Starting execution of Master Query (FULL Load)")
            master_extract_sql = master_extract_sql_full

        elif load_type.upper() == "DELTA":
            # Execute DELTA specific queries
            delta_queries = [
                                Genesis_STG_6,
                                GENESIS_STAGE_NEW_7,
                                GENESIS_STAGE_UPDATES_8,
                                Genesis_Insert_9,
                                Genesis_Update_10
                            ]
            for i, query in enumerate(delta_queries, start=6):  # Start numbering from 6 for DELTA load queries
                logger.info(f"Starting execution of Query {i} (DELTA Load)")
                execute_db_query(createincident_flag, query, snow_data)
                logger.info(f"Finished execution of Query {i}")

            # Execute master query for DELTA load
            logger.info("Starting execution of Master Query (DELTA Load)")
            master_extract_sql = master_extract_sql_delta

        # Read sql query to dataframe
        df = pd.read_sql(master_extract_sql, connectionEngine)
        logger.info("Master sql to dataframe completed")

        # Write the transformations here

        # List of target columns
        target_columns = [
            'first_name', 'last_name', 'email', 'external_id',
            'network_id', 'healthstream_id', 'employee_id', 'badge_number',
            'middle_name', 'preferred_full_name', 'status', 'relationship_to_org',
            'job_code', 'job_code_descr', 'initial_hire_date', 'rehire_date',
            'effective_date', 'action_reason', 'action_reason_eff_date', 'termination_date',
            'years_service', 'flsa', 'fte', 'work_schedule',
            'department_id', 'department_name', 'reporting_location_id', 'reporting_location_name',
            'paygroup', 'entity', 'entity_name', 'position_level',
            'position_id', 'position_name', 'position_family', 'position_category',
            'position_sub_category', 'reports_to_network_id', 'reports_to_employee_id', 'reports_to_healthstream_id',
            'reports_to_name', 'manager_email', 'birthdate', 'race_ethnicity',
            'gender', 'preferred_language', 'home_phone', 'is_manager'
        ]

        # Column mapping for renaming
        column_mapping = {

        }

        # Update the target columns based on the mapping
        updated_target_columns = [column_mapping.get(col, col) for col in target_columns]

        # Handle empty DataFrame
        if df.empty:
            # Create an empty DataFrame with the renamed target columns
            df = pd.DataFrame(columns=updated_target_columns)
        else:
            # Replace Null Value in DF with empty string
            df.replace(np.nan, '', inplace=True)

            # Apply column mapping to rename columns
            df.rename(columns=column_mapping, inplace=True)

            # Apply Transformations here
            # Format 'fte'  and 'years_service' column to two decimal places

            df['fte'] = df['fte'].apply(
                lambda x: f"{float(x):.2f}" if x != '' else '')

            df['years_service'] = df['years_service'].apply(
                lambda x: f"{float(x):.2f}" if x != '' else '')

            # Reorder the DataFrame to match the target columns order
            df = df[updated_target_columns]

        # Write the transformations here

        # column decryption
        if RunningPlatform == "LINUX":
            df = columnDecryption(df, columns_to_decrypt)

        # Write dataframe to csv
        df.to_csv(extract_directory + extract_filename, index=False)
        df_row, df_col = df.shape
        if df_row < threshold_data_vol:
            logger.info(
                "Dataframe to CSV compeleted: Filename - " + extract_directory + extract_filename + ". Threshold volume: " + str(
                    threshold_data_vol) + ". Total Rows: " + str(df_row))
            raise ValueError("The threshold data volume not met for the extract. Please validate the script")

        logger.info(
            "Dataframe to CSV compeleted: Filename - " + extract_directory + extract_filename + ". Total columns: " + str(
                df_col) + ". Total Rows: " + str(df_row))

        # load file audit
        FileAuditId = str(uuid.uuid4())

        # Audit the file in file audit table
        audit_insert = f"INSERT INTO {hr_intg_db}.dbo.FileAudit (FileAuditId, " \
                       "JobAuditId, " \
                       "FileName, " \
                       "RecordCount, " \
                       "StartTime, " \
                       "Status) values" \
                       " ('" + FileAuditId + "','" + JobAuditId + "','" + extract_directory + extract_filename + "', '" + str(
            df_row) + "',GETDATE(),'STARTED')"

        execute_db_query(createincident_flag,
                         audit_insert,
                         snow_data)

        # Apply PGP encrytption to the file
        if RunningPlatform == "LINUX":
            post_process(FileAuditId, extract_directory, extract_filename, extract_filename_pgp)

        # Truncate the extract working tables
        if execution_mode.upper() == "NORMAL":
            truncate_Tables(tuncate_tbl_list, createincident_flag, snow_data)

        # Update JobAudit
        audit_update = f"UPDATE {hr_intg_db}.dbo.JobAudit SET EndTime = GETDATE(), Status = 'SUCCESS' " \
                       "WHERE JobAuditId = '" + JobAuditId + "'"

        execute_db_query(createincident_flag,
                         audit_update,
                         snow_data)

        logger.info("#######################Extraction Completed#######################")

    except:
        logger.info(traceback.format_exc())
        if not custom_faiure:
            call_servicenow(traceback.format_exc(), script_base_name, createincident_flag, snow_data)
        sys.exit("!!!ERROR!!!")

    # Closing the DB connections at the end of script to avoid reusing connection in the next run
    cursor.close()
    del cursor
    conn.close()
    logger.info("DB Connection Closed")

    if RunningPlatform == "LINUX":
        logfile_dir_location = Path(os.getcwd()).joinpath("logs")
        v_scriptname = scriptname.replace(".py", "")
        logfile_location = logfile_dir_location.joinpath(v_scriptname + "_" + CurrentDT.strftime("%Y%m%d") + ".log")
        logfile_zip_name = logfile_dir_location.joinpath("ArchiveLogs").joinpath(
            v_scriptname + "_" + CurrentDT.strftime(
                "%Y%m%d") + ".7z")

        # Seven Zip Audit Files
        cmd = "find " + str(
            logfile_dir_location) + " -maxdepth 1 -type f -mtime +1 -exec 7za a " + str(logfile_zip_name) + " {} \\;"
        logger.info("Seven Zip Audit Files: " + cmd)
        execute_shell_commands(cmd,
                               script_base_name,
                               createincident_flag,
                               snow_data)

        # Delete Older Audit Files
        cmd = "find " + str(logfile_dir_location) + " -maxdepth 1 -type f -mtime +1 -delete"
        logger.info("Delete Older Audit Files: " + cmd)
        execute_shell_commands(cmd,
                               script_base_name,
                               createincident_flag,
                               snow_data)

    logger.info("##################Script Execution Completed##################")


