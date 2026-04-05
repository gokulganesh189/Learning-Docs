str1 = """SELECT FORMAT(MAX(update_stamp_timestamp) AT TIME ZONE ''UTC'' AT TIME ZONE ''Central Standard Time'', ''yyyy-MM-dd HH:mm:ss.fff'') + '' '' +

            CASE WHEN DATEPART(TZOFFSET, MAX(update_stamp_timestamp) AT TIME ZONE ''UTC'' AT TIME ZONE ''Central Standard Time'') < 0

                 THEN ''-'' ELSE ''+'' END +

            RIGHT(''0'' + CAST(ABS(DATEPART(TZOFFSET, MAX(update_stamp_timestamp) AT TIME ZONE ''UTC'' AT TIME ZONE ''Central Standard Time'') / 60) AS varchar), 2) +

            RIGHT(''0'' + CAST(ABS(DATEPART(TZOFFSET, MAX(update_stamp_timestamp) AT TIME ZONE ''UTC'' AT TIME ZONE ''Central Standard Time'') % 60) AS varchar), 2)

     AS max_updatestamp_utc

     FROM {active_table_full}"""

str2 = """
SELECT FORMAT(
         MAX(update_stamp_timestamp) AT TIME ZONE ''UTC''
         AT TIME ZONE ''Central Standard Time'',
         ''yyyy-MM-dd HH:mm:ss.fff''
     ) + '' '' +
     CASE
         WHEN DATEPART(TZOFFSET,
             MAX(update_stamp_timestamp) AT TIME ZONE ''UTC''
             AT TIME ZONE ''Central Standard Time'') < 0
         THEN ''-''
         ELSE ''+''
     END +
     RIGHT(''0'' + CAST(ABS(DATEPART(TZOFFSET,
         MAX(update_stamp_timestamp) AT TIME ZONE ''UTC''
         AT TIME ZONE ''Central Standard Time'') / 60) AS varchar), 2) +
     RIGHT(''0'' + CAST(ABS(DATEPART(TZOFFSET,
         MAX(update_stamp_timestamp) AT TIME ZONE ''UTC''
         AT TIME ZONE ''Central Standard Time'') % 60) AS varchar), 2)
     FROM {active_table_full}"""
 
print(str1==str2)