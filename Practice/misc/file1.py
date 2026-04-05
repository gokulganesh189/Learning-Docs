import os
import sys
import datetime
import time
import pyodbc
from configparser import ConfigParser
import logging
import traceback
from sqlalchemy.engine import URL, create_engine
import uuid
import pandas as pd
import numpy as np
import psutil
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64
import platform
import csv

# Required utils
import utils.Email
import utils.SNOWCalls
import utils.ConnectionString
import utils.PGPEncryptDecrypt
from utils.app_query_config_manager import QueryConfigManager, LocationConfigManager

##############################################################
# Common Logger function for this project
##############################################################
def export_table_logger(logfile_loc):
    logger = logging.getLogger(v_scriptname)
    LOG_FORMAT = '%(asctime)s.%(msecs)03d:%(name)s:%(levelname)s:%(message)s'

    logging.basicConfig(
        filename=logfile_loc,
        level=logging.DEBUG,
        format=LOG_FORMAT,
        datefmt='%Y-%m-%d %H:%M:%S')
    return logger


##############################################################
# Loading DB connection
##############################################################
def load_db_param(scriptname, createincident_flag):
    retry_flag = True
    retry_count = 0
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
            export_table_logger(logfile_location).info("Retry count:" + str(retry_count))
            retry_count = retry_count + 1
            export_table_logger(logfile_location).info(traceback.format_exc())
            time.sleep(db_retry_interval)
            if retry_count >= db_retry_count:
                call_servicenow(traceback.format_exc(), scriptname, createincident_flag, pd.DataFrame())
                sys.exit("!!!ERROR!!!")
            else:
                pass


################function to load all parameter####################

def load_param(createincident_flag,
               scriptname):
    try:
        global environment, \
            servicenowurl, \
            incidenturl, \
            to_email, \
            send_email_to, \
            smtphostname, \
            from_address, \
            CurrentDT, \
            db_retry_count, \
            db_retry_interval, \
            paramlogfolder, \
            RunningPlatform, \
            logfile_location, \
            logfile_dir_location, \
            logfile_zip_name, \
            dlock_retry_count, \
            dlock_retry_interval, \
            pass_phrase_index, \
            conn_index, \
            v_scriptname, \
            user_id, \
            column_key, \
            chunk_size, \
            payroll_db,\
            hr_intg_db,\
            dsn

        v_scriptname = scriptname.replace(".py", "")
        CurrentDT = datetime.datetime.today()
        RunningPlatform = str(platform.system()).upper()

        if RunningPlatform == "LINUX":
            paramlogfolder = os.getcwd() + "/logs/"
        else:
            paramlogfolder = os.getcwd() + "\\logs\\"

        logfile_location = paramlogfolder + "Docebo_Outbound" + "_" + CurrentDT.strftime("%Y%m%d") + ".log"
        logfile_dir_location = paramlogfolder
        logfile_zip_name = logfile_dir_location + "ArchiveLogs/" + "Docebo_Outbound" + "_" + CurrentDT.strftime(
            "%Y%m%d") + ".7z"

        # Get the environment from the OS environment variable
        environment = os.getenv('APP_ENV', 'DEVELOPMENT').upper()  # Default to DEVELOPMENT if not set

        print(f"Environment from the OS environment variable: {environment}")

        # Determine the config file path based on the environment and platform
        if environment == 'PRODUCTION':
            if RunningPlatform == "LINUX":
                config_file = f"config/{v_scriptname}.production.ini"
            else:
                config_file = f"config\\{v_scriptname}.production.ini"
        elif environment == 'TEST':
            if RunningPlatform == "LINUX":
                config_file = f"config/{v_scriptname}.staging.ini"
            else:
                config_file = f"config\\{v_scriptname}.staging.ini"
        else:  # Default to DEVELOPMENT
            if RunningPlatform == "LINUX":
                config_file = f"config/{v_scriptname}.ini"
            else:
                config_file = f"config\\{v_scriptname}.ini"

        parser = ConfigParser()
        parser.read(config_file)

        for section_name in parser.sections():
            for name, value in parser.items(section_name):
                if name == "environment":
                    environment = value
                elif name == "servicenowurl":
                    servicenowurl = value
                elif name == "incidenturl":
                    incidenturl = value
                elif name == "to_email":
                    to_email = value
                elif name == "smtphostname":
                    smtphostname = value
                elif name == "from_address":
                    from_address = value
                elif name == "dlock_retry_count":
                    dlock_retry_count = int(value)
                elif name == "dlock_retry_interval":
                    dlock_retry_interval = int(value)
                elif name == "column_key":
                    column_key = value
                elif name == "db_retry_count":
                    db_retry_count = int(value)
                elif name == "db_retry_interval":
                    db_retry_interval = int(value)
                elif name == "chunk_size":
                    chunk_size = int(value)
                elif name == "payroll_db":
                    payroll_db = str(value)
                elif name == "hr_intg_db":
                    hr_intg_db = str(value)
                elif name == "dsn":
                    dsn = str(value)

        send_email_to = to_email.split(',')

        print(f"Config file location: /{config_file}")
        print("Log Folder: " + paramlogfolder)
        export_table_logger(logfile_location).info(
            "###################" + CurrentDT.strftime(" %Y-%m-%d %a %H:%M:%S ") + "#####################")
    except:
        export_table_logger(logfile_location).info(traceback.format_exc())
        call_servicenow(traceback.format_exc(), scriptname, createincident_flag, pd.DataFrame())
        sys.exit("!!!ERROR!!!")


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
            export_table_logger(logfile_location).info("Executed successfully: " + cmd)
        else:
            export_table_logger(logfile_location).info("Executed failed: " + cmd)
            raise ("Executed failed: " + cmd)
    except:
        export_table_logger(logfile_location).info(traceback.format_exc())
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
    snow_data = pd.DataFrame()
    if not snow_data_all.empty:
        snow_data = snow_data_all.query("`ComponentName` == '" + component_name + "'")
        if snow_data.empty:
            snow_data = snow_data_all.query("`ComponentName` == 'Default'")

    try:
        if createincident_flag == "yes":
            export_table_logger(logfile_location).info("Service now incident creation started")
            newline = '<br>'
            if snow_data.empty:
                export_table_logger(logfile_location).info(
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
                export_table_logger(logfile_location).info(
                    "Service now incident creation completed. Incident number: " + incidentnumber)
        else:
            incidentnumber = ""

    except:
        export_table_logger(logfile_location).info(traceback.format_exc())
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
        while dl_retry_flag and dl_retry_count < dlock_retry_count:
            try:
                export_table_logger(logfile_location).info("Executing Query: " + query)
                result = cursor.execute(query)
                conn.commit()
                dl_retry_flag = False
                return result
            except Exception as er:
                print(er)
                export_table_logger(logfile_location).info(traceback.format_exc())
                dl_retry_count = dl_retry_count + 1
                export_table_logger(logfile_location).info("Dead Lock Retry count:" + str(dl_retry_count))
                time.sleep(dlock_retry_interval)
                if dl_retry_count >= dlock_retry_count:
                    sys.exit("!!!ERROR!!!")
                else:
                    pass
    except:
        export_table_logger(logfile_location).info(traceback.format_exc())
        call_servicenow(traceback.format_exc(), scriptname, createincident_flag, snow_data)
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
        export_table_logger(logfile_location).info(traceback.format_exc())
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
    column_decrypt = read_file(column_key)
    column_decrypt_key = base64.b64decode(column_decrypt)
    export_table_logger(logfile_location).info("Decrypt key and pgp key fetch completed")
    cipher = AES.new(column_decrypt_key, AES.MODE_ECB)
    decrypt_columns = columns_to_decrypt.split(",")
    for column in decrypt_columns:
        if column in df.columns:
            df[column] = df[column].apply(
                lambda x: unpad(cipher.decrypt(base64.b64decode(x)), AES.block_size).decode() if pd.notnull(x) else x)
            export_table_logger(logfile_location).info("Decryption Completed For Column: " + column)

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

            export_table_logger(logfile_location).info(log_reason)

            # Update FileGroupAudit, since previous instance is already running
            audit_update = f"UPDATE {hr_intg_db}.dbo.JobAudit SET EndTime = GETDATE(), " \
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

    export_table_logger(logfile_location).info(
        "PGP encryption completed for file " + extract_directory + extract_filename)

    # remove the source files
    if file_encrypt == "SUCCESS":
        if os.path.isfile(extract_directory + extract_filename):
            os.remove(extract_directory + extract_filename)
    else:
        raise ("File encryption failed for " + extract_directory + extract_filename)

    export_table_logger(logfile_location).info("Removed the file" + extract_directory + extract_filename)

    # Update fileaudit success
    audit_update = f"UPDATE {hr_intg_db}.dbo.FileAudit SET EndTime = GETDATE(), Status = 'SUCCESS' " \
                   "WHERE FileAuditId = '" + FileAuditId + "'"

    execute_db_query(createincident_flag,
                     audit_update,
                     snow_data)

##############################################################
# split and save DataFrame in chunks
##############################################################
def split_and_save_csv(df, extract_directory, extract_filename):
    # Split the DataFrame into chunks and write each chunk to a new CSV
    for i, chunk_start in enumerate(range(0, len(df), chunk_size)):
        # Create new filename with _01, _02, etc.
        chunk_filename = f"{extract_filename.rsplit('.', 1)[0]}_{str(i + 1).zfill(2)}.csv"

        # Write chunk to CSV with headers and values enclosed in double quotes
        df[chunk_start:chunk_start + chunk_size].to_csv(
            extract_directory + chunk_filename,
            index=False,
            quoting=csv.QUOTE_ALL  # This ensures both headers and values are quoted
        )

        export_table_logger(logfile_location).info(
            f"Dataframe chunk {i + 1} written to CSV: Filename - {extract_directory + chunk_filename}"
        )

##############################################################
# Truncate working tables
##############################################################
def truncate_Tables(truncate_list, createincident_flag, snow_data):
    for trncs in truncate_list:
        query = "TRUNCATE TABLE " + trncs
        execute_db_query(createincident_flag,
                         query,
                         snow_data)
        export_table_logger(logfile_location).info("Truncate query executed: " + query)


##########################Main Starts Here###############
scriptname = sys.argv[0]
execution_mode = sys.argv[1] if len(sys.argv) > 1 and sys.argv[1] else 'DEBUG'
createincident_flag = "yes"
script_base_name = os.path.basename(scriptname)
load_param(createincident_flag, script_base_name)
export_table_logger(logfile_location).info("##################Script Execution Started ##################")
snow_data = load_db_param(script_base_name, createincident_flag)
export_table_logger(logfile_location).info("DB Connection Established")
query_manager = QueryConfigManager(connectionEngine)
query_manager.load_query_params("DOCEBO","ACCOUNT_FILE_TO_DOCEBO")
location_manager = LocationConfigManager(connectionEngine)
custom_faiure = False  # To handle snow call for custom failures
try:
    # Assign job audi id
    JobAuditId = str(uuid.uuid4())

    # construct the extract filename
    extract_directory = ""
    extract_filename = "Docebo_InforAccounts_" + time.strftime("%Y%m%d%H%M%S") + ".csv"
    extract_filename_pgp = extract_filename + ".pgp"

    # list all the working tables used in the project
    tuncate_tbl_list = [f"{hr_intg_db}.Extracts.DOCEBO_STAGE_EFFDT", f"{hr_intg_db}.Extracts.DOCEBO_STAGE_SYSDATE",
                        f"{hr_intg_db}.Extracts.DOCEBO_STAGE_ACTIONREASON", f"{hr_intg_db}.Extracts.DOCEBO_STAGE_EMP",
                        f"{hr_intg_db}.Extracts.DOCEBO_STAGE_LICENSE_CREDENTIALS", f"{hr_intg_db}.Extracts.DOCEBO_STAGE_COMP_EMP"]

    # Queries to execute one by one
    effdt_1 = f"""
        INSERT INTO {hr_intg_db}.Extracts.DOCEBO_STAGE_EFFDT
        SELECT EMPLOYEE,
               Convert(nvarchar(8), Cast(MAX(W.EffectiveDate) AS Date), 112) AS EFFECTIVEDATE
        FROM {payroll_db}.dbo.Repset_WorkAssignmentExport_Active W  WITH (NOLOCK)
        WHERE (W.ChangedFields {query_manager.get_query_string(8)})
        GROUP BY Employee
    """

    sysdate_2 = f"""
        INSERT INTO {hr_intg_db}.Extracts.DOCEBO_STAGE_SYSDATE
        SELECT EMPLOYEE,
               MAX(W.SystemTimeStamp) AS MAX_SYS
        FROM {payroll_db}.dbo.Repset_WorkAssignmentExport_Active W  WITH (NOLOCK)
        WHERE (W.ChangedFields {query_manager.get_query_string(1)}) AND W.ActionReason <> ''
        GROUP BY Employee
    """

    actionreason_3 = f"""
        INSERT into {hr_intg_db}.Extracts.DOCEBO_STAGE_ACTIONREASON
        SELECT DISTINCT
                A.Employee,
                A.MAX_SYS,
                B.ActionReason,
                B.EffectiveDate
        FROM
            {hr_intg_db}.Extracts.DOCEBO_STAGE_SYSDATE A WITH (NOLOCK)
            LEFT JOIN {payroll_db}.dbo.Repset_WorkAssignmentExport_Active B  WITH (NOLOCK) ON A.Employee = B.Employee
            AND A.MAX_SYS = B.SystemTimeStamp
    """

    DOCEBO_STAGE_COMP_EMP_3_2 = f"""
        INSERT INTO {hr_intg_db}.Extracts.DOCEBO_STAGE_COMP_EMP
        SELECT
            A.EMPL_STATUS
            ,A.[NETWORK_ID]
            ,A.Employee
            ,A.[BADGE_NUMBER]
            ,A.[HEALTHSTREAM_ID]                                                                                                                                                                              
            ,A.[ContactDetail_EmailAddress]
            ,A.PERSONAL_EMAIL
            ,A.FIRST_NAME
            ,A.MIDDLE_NAME
            ,A.LAST_NAME
            ,A.FULL_NAME
            ,A.[Preferred_FullName]
            ,A.FORMER_FULL_NAME
            ,A.GENDER_STATE
            ,A.BIRTHDATE
            ,A.RACE_ETHNICITY
            ,A.AssignmentIsSupervisor
            ,A.MANAGER_NETWORK_ID
            ,A.REPORTS_TO_NAME
            ,A.DEPTID
            ,A.DEPT_DESCR
            ,A.REPORTING_LOCATION
            ,A.REPORTING_LOCATION_DESCR
            ,A.REPORTING_STREET
            ,A.REPORTING_CITY
            ,A.REPORTING_STATE
            ,A.REPORTING_COUNTRY
            ,A.PAYGROUP_DESCR
            ,A.Entity
            ,A.Position
            ,A.PostionName
            ,A.PositionLevelDescr
            ,A.PositionFamily
            ,A.PositionCategory
            ,A.PositionSubCategory
            ,A.JOBCODE
            ,A.JOBCODE_DESCR
            ,A.JobLevelDescr
            ,A.JobFamily
            ,A.JobCategory
            ,A.JobSubCategory
            ,A.WORKSCHEDULE
            ,A.RelationshipToOrganization
            ,A.[HIRE_DT]
            ,A.REHIRE_DT
            ,A.Years_of_service
            ,A.TERMINATION_DT
            ,A.LAST_DATE_WORKED
            ,A.FTE
            ,A.EMPL_TYPE
            ,A.PAYGROUP
            ,A.SERVICE_DT
            ,A.[LOCATION]
            ,A.DatePositionLastChanged
        FROM {hr_intg_db}.DBO.EMPLOYEE_V  A  WITH (NOLOCK)
    """

    emp_ds_4 = f"""
            WITH
            EMP_REHIRE_DT AS (
                SELECT  EMPLOYEE,
                        MAX(CONVERT(varchar(10), CAST(REHIRE_DT as date), 23)) as rehire_date
                FROM {hr_intg_db}.Extracts.DOCEBO_STAGE_COMP_EMP WITH (NOLOCK)
                GROUP BY EMPLOYEE
            ),
            EMP_DS1 AS (
                SELECT
                CASE
                    WHEN A.EMPL_STATUS {query_manager.get_query_string(7)} THEN {query_manager.get_description(7)}
                    ELSE 'Inactive'
                    END                                                             AS [infor_hr_account_active],
                    LOWER(CONVERT(VARCHAR, A.[NETWORK_ID]))                                             AS [network_id],
                    A.Employee                                                                                                          AS [employee_id],
                    A.[BADGE_NUMBER]                                                AS [badge_id],
                    [HEALTHSTREAM_ID]                                                                                           AS [healthstream_id],                                                         
                    A.[ContactDetail_EmailAddress]                                                                      AS [primary_email],
                    A.PERSONAL_EMAIL                                                                                            AS [secondary_email],
                    A.FIRST_NAME                                                                                                        AS [first_name],
                    A.MIDDLE_NAME                                                                                                       AS [middle_name],
                    A.LAST_NAME                                                                                                         AS [last_name],
                    A.FULL_NAME                                                                                                         AS [full_name],
                    A.[Preferred_FullName]                                                                                      AS [preferred_full_name],
                    A.FORMER_FULL_NAME                                                                                          AS [former_full_name],
                    A.GENDER_STATE                                                                                                      AS [gender],
                    --A.BIRTHDATE                                                                                                               AS [birthdate],
                    CONVERT(varchar(10), CAST(A.BIRTHDATE as date), 101)            AS [birthdate],
                    A.RACE_ETHNICITY                                                                                            AS [ethnicity],
                    'English'                                                                                                           AS [preferred_language_name],
                    A.AssignmentIsSupervisor                                                                            AS [is_manager],
                    A.MANAGER_NETWORK_ID                                                                                        AS [reports_to_network_id],
                    A.REPORTS_TO_NAME                                                                                           AS [reports_to_name],
                    A.DEPTID                                                                                                            AS [department_id],
                    A.DEPT_DESCR                                                                                                        AS [department_name],
                    A.REPORTING_LOCATION                                                                                        AS [work_location_id],
                    A.REPORTING_LOCATION_DESCR                                                                          AS [work_location_name],
                    A.REPORTING_STREET                                                                                          AS [work_location_address],
                    A.REPORTING_CITY                                                                                            AS [work_location_city],
                    A.REPORTING_STATE                                                                                           AS [work_location_state],
                    A.REPORTING_COUNTRY                                                                                         AS [work_location_country],
                    A.PAYGROUP                                                                                                          AS [ministry_id],
                    A.PAYGROUP_DESCR                                                                                            AS [ministry_name],
                    A.Entity                                                                                                            AS [entity_id],
                    GLC.[Name]                                                                                                          AS [entity_name],
                    A.Position                                                                                                          AS [position_id],
                    A.PostionName                                                                                                       AS [position_name],
                    A.PositionLevelDescr                                                                                        AS [postion_level],
                    A.PositionFamily                                                                                            AS [position_family],
                    A.PositionCategory                                                                                          AS [position_category],
                    A.PositionSubCategory                                                                                       AS [postion_subcategory],
                    A.JOBCODE                                                                                                           AS [job_id],
                    A.JOBCODE_DESCR                                                                                                     AS [job_name],
                    A.JobLevelDescr                                                                                                     AS [job_level],
                    A.JobFamily                                                                                                         AS [job_family],
                    A.JobCategory                                                                                                       AS [job_category],
                    A.JobCategory                                                                                                       AS [JobCategory],
                    A.JobSubCategory                                                                                            AS [Job_subcategory],
                    A.WORKSCHEDULE                                                                                                      AS [primary_shift],
                    A.EMPL_STATUS                                                                                                       AS [employment_status],
                    A.RelationshipToOrganization                                                                        AS [relationship_to_organization],
                    CONVERT(varchar(10), CAST(A.[HIRE_DT] as date), 23)                         AS [original_hire_date],
                    (SELECT Max(v) FROM
                    (VALUES (Convert(varchar, Convert(date, A.HIRE_DT), 101)),
                    (Convert(varchar, Convert(date, A.REHIRE_DT), 101)),
                    (Convert(varchar, Convert(date, E.EFFECTIVEDATE), 101)))
                    AS value(v))                                                                                                        AS [effective_date],
                    CONVERT(VARCHAR, A.Years_of_service)                                                        AS [years_of_service],
                    A.TERMINATION_DT                                                                                            AS [termination_date],
                    A.LAST_DATE_WORKED                                                                                          AS [termination_last_date_worked],
                    A.FTE                                                                                                                       AS [fte],
                    A.EMPL_TYPE                                                                                                         AS [work_status],
                    A.PAYGROUP                                                                                                          AS [paygroup],
                    AR.ActionReason                                                                                                     AS [action_reason],
                    AR.EffectiveDate                                                                                            AS [action_reason_effective_date],
                    A.SERVICE_DT                                                                                                AS [START_DATE],
                    A.[LOCATION]                                                    AS [LOCATION],
                    dt.[rehire_date],
                    A.DatePositionLastChanged
                FROM {hr_intg_db}.Extracts.DOCEBO_STAGE_COMP_EMP A WITH (NOLOCK)
                    LEFT JOIN {hr_intg_db}.Extracts.DOCEBO_STAGE_EFFDT E WITH (NOLOCK) ON A.Employee = E.Employee
                    LEFT JOIN {hr_intg_db}.dbo.Repset_GLCompany_Active GLC  WITH (NOLOCK) ON A.Entity = GLC.Company
                    LEFT JOIN {hr_intg_db}.Extracts.DOCEBO_STAGE_ACTIONREASON AR WITH (NOLOCK) ON A.Employee = AR.EMPLOYEE
                    LEFT JOIN EMP_REHIRE_DT dt on dt.Employee = A.Employee
                WHERE A.[NETWORK_ID] <> '' OR A.[NETWORK_ID] IS NOT NULL

            ),
            EMP_DS2 AS (
                SELECT
                    a.[infor_hr_account_active]                                                                                         AS [Active],
                    CONCAT(LOWER(a.[network_id]),'@echristus.net')                                              AS [Username],
                    a.[first_name]                                                                                                              AS [First_Name],
                    a.[middle_name]                                                                                                             AS [Middle_Name],
                    a.[last_name]                                                                                                                   AS [Last_Name],
                    [primary_email]                                                                                                             AS [Primary_Email],
                    LOWER(a.[secondary_email])                                                                                  AS [Secondary_Email],
                    LOWER(a.[network_id])                                                                                               AS [Network_ID],
                    --a.[employee_id]                                                                                                       AS [Employee_ID]
                    TRIM(a.[employee_id])                                                                               AS [Employee_ID],
                    a.[badge_id]                                                                                                                AS [Badge_ID],
                    a.[healthstream_id]                                                                                                 AS [Healthstream_ID],
                    a.[gender]                                                                                                                  AS [Gender],
                    --a.[birthdate]                                                                                                     AS [Birthdate],
                    FORMAT(TRY_CONVERT(date, a.[birthdate]),'MM/dd/yyyy')                               AS [Birthdate],
                    a.[is_manager]                                                                                                              AS [Is_Manager],
                    CONCAT(LOWER(a.[reports_to_network_id]),'@echristus.net')                           AS [Direct_Manager],
                    CONCAT_WS(' ', a.[job_id], a.[job_name])                                                        AS [Job_Title],
                    a.[job_level]                                                                                                               AS [Job_Level],
                    a.[job_family]                                                                                                          AS [Job_Family],
                    a.[job_category]                                                                                                AS [job_category],
                    a.[Job_subcategory]                                                                                                 AS [Job_subcategory],
                    CONCAT_WS(' ', a.[department_id], a.[department_name])                                  AS [Department],
                    a.[ministry_name]                                                                                               AS [Ministry],
                    CONCAT_WS(' ', a.[entity_id], a.[entity_name])                                              AS [Reporting_Entity],
                    CONCAT_WS(' ', a.[work_location_id], a.[work_location_name])                    AS [Reporting_Location],
                    a.[work_location_city]                                                                                          AS [Reporting_City],
                    a.[work_location_state]                                                                                         AS [Reporting_State],
                    a.[work_location_country]                                                                                       AS [Reporting_Country],
                    CASE WHEN {query_manager.get_query_string(9)} {query_manager.get_description(9)} END AS [Timezone],
                    a.[relationship_to_organization]                                                                    AS [Relationship_To_Org],
                    a.[original_hire_date]                                                                                          AS [Hire_Date],
                    a.[rehire_date]                                                                                                         AS [Rehire_Date],
                    a.[rehire_date]                                                                                                             AS [HireDate_Category],
                    a.[termination_date]                                                                                            AS [Termination_Date],
                    a.[employment_status]                                                                                               AS [Employment_Status],
                    a.[fte]                                                                                                                         AS [FTE],
                    a.[ministry_id]                                                                                                         AS [Paygroup],
                    a.[preferred_language_name]                                                                                     AS [Language],
                    a.[is_manager]                                                                                                              AS [Is_A_Manager],
                    a.[action_reason]                                                                                                       AS [Change_Reason],
                    a.[effective_date]                                                                                              AS [Change_Date],
                    a.[entity_id]                                                                                                               AS [entity_id],
                    a.[work_location_id]                                                                                                AS [work_location_id],
                    a.[START_DATE]                                                          AS [START_DATE],
                    A.[LOCATION]                                                            AS [LOCATION],
                    A.DatePositionLastChanged
                FROM EMP_DS1 A
                WHERE a.[infor_hr_account_active] {query_manager.get_query_string(2)}
                        OR
                        (
                            a.[infor_hr_account_active] {query_manager.get_query_string(3)} AND
                            TRY_CONVERT(date, a.[termination_date]) >= DATEADD(DAY, 1 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE)) AND
                            TRY_CONVERT(date, a.[termination_date]) <= DATEADD(DAY, 7 - DATEPART(WEEKDAY, GETDATE()), CAST(GETDATE() AS DATE))
                        )
            )
            INSERT INTO {hr_intg_db}.Extracts.DOCEBO_STAGE_EMP
            SELECT * FROM EMP_DS2;
            """

    license_5 = f"""
            WITH LIC AS
            (
                SELECT
                        [NETWORK_ID]                                                                                                    AS [network_id],
                        EMPLOYEE                                                                                                                AS [employee_id],
                        EMAIL_ADDRESS                                                                                                   AS [primary_email],
                        LIC_DESCR                                                                                                               AS [credential_name],
                        CONVERT(varchar(10), CAST([DateRange_Begin] as date), 101)      AS [credential_active_date],
                        CONVERT(varchar(10), CAST(LICENSE_EXPIRATN_DT as date), 101)    AS [credential_expiration_date]
                FROM {hr_intg_db}.dbo.LICENSE_CREDENTIALS_V  WITH (NOLOCK)
            ),
            LICENSE AS (
                SELECT *
                FROM (
                    SELECT
                        [employee_id],
                        [Basic Life Support] AS Basic_Life_Support,
                        [Advanced Cardiovascular Life Support] AS Advanced_Cardiovascular_Life_Support,
                        [Pediatric Advanced Life Support] AS Pediatric_Advanced_Life_Support,
                        [Neonatal Resuscitation Program] AS Neonatal_Resuscitation_Program
                    FROM (
                        SELECT
                            [employee_id],
                            [credential_name],
                            [credential_expiration_date]
                        FROM LIC
                    ) t1
                    PIVOT (
                        MIN([credential_expiration_date])
                        FOR [credential_name] IN
                        (
                            [Basic Life Support],
                            [Advanced Cardiovascular Life Support],
                            [Pediatric Advanced Life Support],
                            [Neonatal Resuscitation Program]
                        )
                    ) AS t2
                ) AS x
            )
            INSERT INTO {hr_intg_db}.Extracts.DOCEBO_STAGE_LICENSE_CREDENTIALS
            SELECT * FROM LICENSE;
    """

    # Construct the master query to get the column details from different views
    master_extract_sql = f"""
        with EmpDetails as (
            select 
                e.employee,
                cast(ee.terminationdate as date) as terminationdate,
                cast(e.REHIRE_DT as date) as rehiredate
            from  Extracts.DOCEBO_STAGE_COMP_EMP e WITH (NOLOCK) left join 
                                    (
                                        select employee,max(cast(EffectiveDate as date)) as terminationdate from Repset_EmployeeExport_Active WITH (NOLOCK)
                                        where action {query_manager.get_query_string(4)} group by employee
                                    ) ee
            on e.Employee = ee.employee where e.empl_status {query_manager.get_query_string(5)}
        ),
        term_details as (
                select Employee,
                    case when terminationdate is not null and rehiredate is not null and rehiredate > terminationdate  then datediff(day,terminationdate ,rehiredate ) else 9999
                    end as DaysBetweenTerminationAndRehire 
                from EmpDetails 
        )
    
            SELECT DISTINCT
                a.[Active],
                a.[Username],
                a.[First_Name],
                a.[Middle_Name],
                a.[Last_Name],
                a.[Primary_Email],
                a.[Secondary_Email],
                a.[Network_ID],
                a.[Employee_ID],
                a.[Badge_ID],
                a.[Healthstream_ID],
                a.[Gender],
                a.[Birthdate],
                a.[Is_Manager],
                a.[Direct_Manager],
                a.[Job_Title],
                a.[Job_Level],
                a.[Job_Family],
                a.[job_category],
                a.[Job_subcategory],
                a.[Department],
                a.[Ministry],
                a.[Reporting_Entity],
                a.[Reporting_Location],
                a.[Reporting_City],
                a.[Reporting_State],
                a.[Reporting_Country],
                a.[Timezone],
                a.[Relationship_To_Org],
                a.[Hire_Date],
                a.[Rehire_Date],
                a.[HireDate_Category] AS [Start_Date_Category],
                a.[Termination_Date],
                a.[Employment_Status],
                a.[FTE],
                a.[Paygroup],
                a.[Language],
                a.[Is_A_Manager],
                a.[Change_Reason],
                a.[Change_Date],
                a.[entity_id],
                a.[work_location_id],
                a.[START_DATE],
                ISNULL(b.[Basic_Life_Support], '') AS [BLS_Expiration],
                ISNULL(b.[Advanced_Cardiovascular_Life_Support], '') AS [ACLS_Expiration],
                ISNULL(b.[Pediatric_Advanced_Life_Support], '') AS [PALS_Expiration],
                ISNULL(b.[Neonatal_Resuscitation_Program], '') AS [NRP_Expiration],
                ISNULL(c.[Branch_Code_Path], '') AS [Branch_Code_Path],
                ISNULL(c.[Branch_Name_Path], '') AS [Branch_Name_Path],
                ISNULL(c.[Branch_Code], '') AS [Branch_Code],
                c.[Facility_Type] AS [facility_type],
                c.[Branch_ID] AS REGION,
                'education' AS PASSWORD,
                'CHRISTUS INFOR' AS [IMPORT_SOURCE],
                case when td.DaysBetweenTerminationAndRehire {query_manager.get_query_string(6)} {query_manager.get_description(6)} end as DaysBetweenTerminationAndRehire
                ,COALESCE(a.DatePositionLastChanged,'') as DatePositionLastChanged
            FROM {hr_intg_db}.Extracts.DOCEBO_STAGE_EMP a WITH (NOLOCK)
            LEFT JOIN {hr_intg_db}.Extracts.DOCEBO_STAGE_LICENSE_CREDENTIALS b WITH (NOLOCK) ON a.[Employee_ID] = b.[employee_id]
            LEFT OUTER JOIN {hr_intg_db}.dbo.Ref_BranchMap_Active c   WITH (NOLOCK) ON CONVERT(varchar, a.[work_location_id]) = CONVERT(varchar, c.[work_location_id])
            LEFT JOIN term_details td on td.Employee = a.[Employee_ID]
            WHERE
                        ( {location_manager.get_location_filter_config("DOCEBO","ACCOUNT_FILE_TO_DOCEBO")} = 0
            OR a.location {query_manager.get_locations("DOCEBO","ACCOUNT_FILE_TO_DOCEBO")}
            OR a.location IS NULL )       
    """

    # Send the run for pre check
    log_reason = pre_process_check(JobAuditId, scriptname, snow_data, createincident_flag, script_base_name)
    if log_reason == "SUCCESS":
        export_table_logger(logfile_location).info("There is no PID's for the script execution")
    else:
        custom_faiure = True
        raise ValueError(log_reason)

    if execution_mode.upper() not in ("DEBUG", "NORMAL"):
        raise ValueError("Please provide valid debug mode. Allowed DEBUG or NORMAL")

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

    # Execute queries one by one
    for i, query in enumerate([effdt_1, sysdate_2, actionreason_3,DOCEBO_STAGE_COMP_EMP_3_2, emp_ds_4, license_5], start=1):
        export_table_logger(logfile_location).info(f"Starting execution of Query {i}")
        execute_db_query(createincident_flag, query, snow_data)
        export_table_logger(logfile_location).info(f"Finished execution of Query {i}")

    # Read sql query to dataframe
    export_table_logger(logfile_location).info(f"Master Extract sql query {master_extract_sql}")
    df = pd.read_sql(master_extract_sql, connectionEngine)
    export_table_logger(logfile_location).info("Master sql to dataframe completed")

    # Write the transformations here

    target_columns = [
        'Active', 'Username', 'First_Name', 'Middle_Name', 'Last_Name', 'Primary_Email',
        'Secondary_Email', 'Network_ID', 'Employee_ID', 'Badge_ID', 'Healthstream_ID',
        'Gender', 'Birthdate', 'Is_Manager', 'Direct_Manager', 'Job_Title', 'Job_Family',
        'Job_Category', 'Job_Subcategory', 'Department', 'Ministry', 'Reporting_Entity',
        'Region', 'Facility_Type', 'Reporting_Location', 'Reporting_City', 'Reporting_State',
        'Reporting_Country', 'Timezone', 'Relationship_To_Org', 'Hire_Date', 'Rehire_Date',
        'Start_Date_Category', 'Termination_Date', 'Employment_Status', 'FTE', 'Paygroup',
        'Language', 'Is_A_Manager', 'Change_Reason', 'Change_Date', 'BLS_Expiration',
        'ACLS_Expiration', 'PALS_Expiration', 'NRP_Expiration', 'Password', 'Import_Source',
        'Branch_Code_Path', 'Branch_Name_Path', 'Branch_Code','DaysBetweenTerminationAndRehire','DatePositionLastChanged'
    ]

    # Create a column mapping from the original column names to the new column names with underscores
    column_mapping = {
        'First_Name': 'First_Name',
        'Middle_Name': 'Middle_Name',
        'Last_Name': 'Last_Name',
        'Primary_Email': 'Primary_Email',
        'Secondary_Email': 'Secondary_Email',
        'Network_ID': 'Network_ID',
        'Employee_ID': 'Employee_ID',
        'Badge_ID': 'Badge_ID',
        'Healthstream_ID': 'Healthstream_ID',
        'Is_Manager': 'Is_Manager',
        'Direct_Manager': 'Direct_Manager',
        'Job_Title': 'Job_Title',
        'Job_Family': 'Job_Family',
        'job_category': 'Job_Category',
        'Job_subcategory': 'Job_Subcategory',
        'Reporting_Entity': 'Reporting_Entity',
        'facility_type': 'Facility_Type',
        'Reporting_Location': 'Reporting_Location',
        'Reporting_City': 'Reporting_City',
        'Reporting_State': 'Reporting_State',
        'Reporting_Country': 'Reporting_Country',
        'Relationship_To_Org': 'Relationship_To_Org',
        'Hire_Date': 'Hire_Date',
        'Rehire_Date': 'Rehire_Date',
        'Start_Date_Category': 'Start_Date_Category',
        'Termination_Date': 'Termination_Date',
        'Employment_Status': 'Employment_Status',
        'Is_A_Manager': 'Is_A_Manager',
        'Change_Reason': 'Change_Reason',
        'Change_Date': 'Change_Date',
        'BLS_Expiration': 'BLS_Expiration',
        'ACLS_Expiration': 'ACLS_Expiration',
        'PALS_Expiration': 'PALS_Expiration',
        'NRP_Expiration': 'NRP_Expiration',
        'IMPORT_SOURCE': 'Import_Source',
        'Branch_Code_Path': 'Branch_Code_Path',
        'Branch_Name_Path': 'Branch_Name_Path',
        'Branch_Code': 'Branch_Code',
        'REGION': 'Region',
        'PASSWORD': 'Password',
        'DaysBetweenTerminationAndRehire':'DaysBetweenTerminationAndRehire',
        'DatePositionLastChanged':'DatePositionLastChanged'
    }

    # Handle empty DataFrame
    if df.empty:
        # Create an empty DataFrame with the target columns
        df = pd.DataFrame(columns=target_columns)

    else:
        # Rename the columns using the mapping
        df.rename(columns=column_mapping, inplace=True)

        # Replace Null values in DataFrame with an empty string
        df.replace(np.nan, '', inplace=True)

        # Active Column Transformation - Apply transformation to convert 'Active' values to '0' or '1'
        df['Active'] = df['Active'].apply(lambda x: '0' if x == 'Inactive' else ('1' if x == 'Active' else x))

        # Primary_Email Column Transformation
        df['Primary_Email'] = df['Primary_Email'].apply(
            lambda x: 'unknown.email@christushealth.org' if x == '' else x.lower()
        )

        # Apply transformation to convert 'Healthstream_ID' to lowercase, handling non-string values
        df['Healthstream_ID'] = df['Healthstream_ID'].apply(lambda x: x.lower() if isinstance(x, str) else x)

        # Gender Column Transformation
        df['Gender'] = df['Gender'].apply(
            lambda x: 'F' if x == 'Female' else ('M' if x == 'Male' else ('U' if x in ['', 'Withhold'] else x))
        )

        # Is_Manager Column Transformation
        df['Is_Manager'] = df['Is_Manager'].apply(lambda x: 'Y' if x != '0' else 'N')

        # Is_A_Manager Column Transformation
        df['Is_A_Manager'] = df['Is_A_Manager'].apply(lambda x: 'Y' if x != '0' else 'N')

        # Start_Date_Category Column Transformation (Custom Logic)
        # Get current date using pandas
        current_date = pd.Timestamp.today().normalize()

        # Define start and end of "This Week", "Last Week", and "Next Week"
        this_week_start = current_date - pd.Timedelta(days=current_date.weekday())
        this_week_end = this_week_start + pd.Timedelta(days=6)

        last_week_start = this_week_start - pd.Timedelta(days=7)
        last_week_end = this_week_start - pd.Timedelta(days=1)

        next_week_start = this_week_end + pd.Timedelta(days=1)
        next_week_end = next_week_start + pd.Timedelta(days=6)


        # Transform 'Start Date Category'
        def categorize_rehire_date(date):
            try:
                parsed_date = pd.to_datetime(date)
                if last_week_start <= parsed_date <= last_week_end:
                    return 'Last Week'
                elif this_week_start <= parsed_date <= this_week_end:
                    return 'This Week'
                elif next_week_start <= parsed_date <= next_week_end:
                    return 'Next Week'
                else:
                    return 'N/A'
            except:
                return 'N/A'  # If conversion fails or date is invalid


        df['Start_Date_Category'] = df['Rehire_Date'].apply(categorize_rehire_date)

        # Handle cases where 'Start_Date_Category' is NULL
        df['Start_Date_Category'] = df['Start_Date_Category'].apply(lambda x: '' if pd.isna(x) else x)

        # Convert the column to datetime, handling errors and missing values
        df['Rehire_Date'] = pd.to_datetime(df['Rehire_Date'], errors='coerce')

        # Define a function to format the date with a default time if missing
        def format_rehire_date(date):
            if pd.isna(date):
                return None

            date_str = None  # Initialize date_str

            # Check if the object is a datetime, otherwise treat as a date
            if isinstance(date, datetime.datetime):  # Check for datetime object
                # Format the date with time if present, otherwise just the date
                date_str = date.strftime('%m/%d/%Y') if date.time() == pd.Timestamp.min.time() else date.strftime(
                    '%m/%d/%Y %I:%M:%S %p')
            elif isinstance(date, datetime.date):  # Handle date object
                date_str = date.strftime('%m/%d/%Y')

            if date_str:
                # Remove leading zeros from both the month and the day
                month_day_fixed = date_str.lstrip("0").replace('/0', '/')
                return month_day_fixed
            else:
                return None  # Fallback in case date_str is not assigned

        # Apply the function to the 'Rehire_Date' column
        df['Rehire_Date'] = df['Rehire_Date'].apply(format_rehire_date)

        # Reorder the DataFrame to match the target columns order
        df = df[target_columns]

    # Write the transformations here

    # column decryption
    if RunningPlatform == "LINUX":
        df = columnDecryption(df, columns_to_decrypt)

    # Write dataframe to csv
    df_row, df_col = df.shape

    # Invoke split and save the CSV
    split_and_save_csv(df, extract_directory, extract_filename)

    if df_row < threshold_data_vol:
        export_table_logger(logfile_location).info(
            "Dataframe to CSV completed: Filename - " + extract_directory + extract_filename + ". Threshold volume: " +
            str(threshold_data_vol) + ". Total Rows: " + str(df_row)
        )
        raise ValueError("The threshold data volume not met for the extract. Please validate the script")

    export_table_logger(logfile_location).info(
        "Dataframe to CSV completed. Total columns: " + str(df_col) + ". Total Rows: " + str(df_row)
    )

    # load file audit
    FileAuditId = str(uuid.uuid4())

    # Audit the file in file audit table
    num_chunks = (df_row // chunk_size) + (1 if df_row % chunk_size != 0 else 0)
    for i in range(num_chunks):
        chunk_filename = f"{extract_filename.rsplit('.', 1)[0]}_{str(i + 1).zfill(2)}.csv"
        audit_insert = f"INSERT INTO {hr_intg_db}.dbo.FileAudit (FileAuditId, JobAuditId, FileName, RecordCount, StartTime, Status) values" \
                       f" ('{FileAuditId}', '{JobAuditId}', '{extract_directory + chunk_filename}', '{df_row}', GETDATE(), 'STARTED')"

        execute_db_query(createincident_flag, audit_insert, snow_data)

    # Apply PGP encryption to each chunk
    if RunningPlatform == "LINUX":
        for i in range(num_chunks):
            chunk_filename = f"{extract_filename.rsplit('.', 1)[0]}_{str(i + 1).zfill(2)}.csv"
            extract_filename_pgp = f"{chunk_filename}.pgp"
            post_process(FileAuditId, extract_directory, chunk_filename, extract_filename_pgp)

    # Truncate the extract working tables
    if execution_mode.upper() == "NORMAL":
        truncate_Tables(tuncate_tbl_list, createincident_flag, snow_data)

    # Update JobAudit
    audit_update =f"UPDATE {hr_intg_db}.dbo.JobAudit SET EndTime = GETDATE(), Status = 'SUCCESS' " \
                   "WHERE JobAuditId = '" + JobAuditId + "'"

    execute_db_query(createincident_flag,
                     audit_update,
                     snow_data)

    export_table_logger(logfile_location).info("#######################Extraction Completed#######################")

except:
    export_table_logger(logfile_location).info(traceback.format_exc())
    if not custom_faiure:
        call_servicenow(traceback.format_exc(), script_base_name, createincident_flag, snow_data)
    sys.exit("!!!ERROR!!!")

# Closing the DB connections at the end of script to avoid reusing connection in the next run
cursor.close()
del cursor
conn.close()
export_table_logger(logfile_location).info("DB Connection Closed")

if RunningPlatform == "LINUX":
    # Seven Zip Audit Files
    cmd = "find " + logfile_dir_location + " -maxdepth 1 -type f -mtime +1 -exec 7za a " + logfile_zip_name + " {} \\;"
    export_table_logger(logfile_location).info("Seven Zip Audit Files: " + cmd)
    execute_shell_commands(cmd,
                           script_base_name,
                           createincident_flag,
                           snow_data)

    # Delete Older Audit Files
    cmd = "find " + logfile_dir_location + " -maxdepth 1 -type f -mtime +1 -delete"
    export_table_logger(logfile_location).info("Delete Older Audit Files: " + cmd)
    execute_shell_commands(cmd,
                           script_base_name,
                           createincident_flag,
                           snow_data)

export_table_logger(logfile_location).info("##################Script Execution Completed##################")
