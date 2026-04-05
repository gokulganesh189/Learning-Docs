-------------------- Service Now VendorList Staging 

USE [DBP_HR_INTG_01]
GO

/****** Object:  Table [Extracts].[FSM_VENDOR_DATA_STAGE]    Script Date: 1/20/2026 12:34:13 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[Extracts].[FSM_VENDOR_DATA_STAGE]') AND type in (N'U'))
DROP TABLE [Extracts].[FSM_VENDOR_DATA_STAGE]
GO

/****** Object:  Table [Extracts].[FSM_VENDOR_DATA_STAGE]    Script Date: 1/20/2026 12:34:13 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [Extracts].[FSM_VENDOR_DATA_STAGE](
	[Vendor] [varchar](500) NULL,
	[VendorClass] [varchar](500) NULL,
	[VendorName] [varchar](500) NULL,
	[VendorStatus] [varchar](500) NULL,
	[LegalName] [varchar](500) NULL,
	[LavantedidUDF] [varchar](500) NULL,
	[changeHash] [varbinary](64) NULL,
	[load_timestamp] [datetime] NULL
) ON [PRIMARY]
GO

-------------------- Service Now VendorList Repset

USE [DBP_HR_INTG_01]
GO

ALTER TABLE [dbo].[Repset_Fsm_Vendor_Landing] DROP CONSTRAINT [DF__Repset_Fs__REPOR__6C1B70C0]
GO

/****** Object:  Table [dbo].[Repset_Fsm_Vendor_Landing]    Script Date: 1/20/2026 12:35:50 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Repset_Fsm_Vendor_Landing]') AND type in (N'U'))
DROP TABLE [dbo].[Repset_Fsm_Vendor_Landing]
GO

/****** Object:  Table [dbo].[Repset_Fsm_Vendor_Landing]    Script Date: 1/20/2026 12:35:50 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Repset_Fsm_Vendor_Landing](
	[ID] [int] IDENTITY(1,1) NOT NULL,
	[_Action] [varchar](500) NULL,
	[LavanteIdUDF] [varchar](500) NULL,
	[LegacyVendor] [varchar](500) NULL,
	[LegalName] [varchar](500) NULL,
	[RepSet_Variation_ID] [varchar](500) NULL,
	[UniqueID] [varchar](500) NULL,
	[Vendor] [varchar](500) NULL,
	[VendorClass] [varchar](500) NULL,
	[VendorGroup] [varchar](500) NULL,
	[VendorName] [varchar](500) NULL,
	[VendorStatus] [varchar](500) NULL,
	[VendorStatus_State] [varchar](500) NULL,
	[create_stamp_timestamp] [datetime2](3) NULL,
	[update_stamp_timestamp] [datetime2](3) NULL,
	[FileName] [varchar](500) NULL,
	[REPORT_DT] [datetime] NULL,
	[RowHash] [varbinary](32) NULL
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Repset_Fsm_Vendor_Landing] ADD  DEFAULT (getdate()) FOR [REPORT_DT]
GO

USE [DBP_HR_INTG_01]
GO

/****** Object:  Table [dbo].[Repset_Fsm_Vendor_Active]    Script Date: 1/20/2026 12:36:48 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Repset_Fsm_Vendor_Active]') AND type in (N'U'))
DROP TABLE [dbo].[Repset_Fsm_Vendor_Active]
GO

/****** Object:  Table [dbo].[Repset_Fsm_Vendor_Active]    Script Date: 1/20/2026 12:36:48 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Repset_Fsm_Vendor_Active](
	[Repset_Fsm_Vendor_Active_ID] [bigint] IDENTITY(1,1) NOT NULL,
	[_Action] [varchar](500) NULL,
	[LavanteIdUDF] [varchar](500) NULL,
	[LegacyVendor] [varchar](500) NULL,
	[LegalName] [varchar](500) NULL,
	[RepSet_Variation_ID] [varchar](500) NULL,
	[UniqueID] [varchar](500) NULL,
	[Vendor] [varchar](500) NULL,
	[VendorClass] [varchar](500) NULL,
	[VendorGroup] [varchar](500) NULL,
	[VendorName] [varchar](500) NULL,
	[VendorStatus] [varchar](500) NULL,
	[VendorStatus_State] [varchar](500) NULL,
	[create_stamp_timestamp] [datetime2](3) NULL,
	[update_stamp_timestamp] [datetime2](3) NULL,
	[FileName] [varchar](500) NULL,
	[REPORT_DT] [datetime] NULL,
	[RowHash] [varbinary](32) NULL,
 CONSTRAINT [PK_Repset_Fsm_Vendor_Active_ID] PRIMARY KEY CLUSTERED 
(
	[Repset_Fsm_Vendor_Active_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

USE [DBP_HR_INTG_01]
GO

ALTER TABLE [dbo].[Repset_Fsm_Vendor_Archive] DROP CONSTRAINT [DF__Repset_Fs__Archi__70E025DD]
GO

/****** Object:  Table [dbo].[Repset_Fsm_Vendor_Archive]    Script Date: 1/20/2026 12:37:00 PM ******/
IF  EXISTS (SELECT * FROM sys.objects WHERE object_id = OBJECT_ID(N'[dbo].[Repset_Fsm_Vendor_Archive]') AND type in (N'U'))
DROP TABLE [dbo].[Repset_Fsm_Vendor_Archive]
GO

/****** Object:  Table [dbo].[Repset_Fsm_Vendor_Archive]    Script Date: 1/20/2026 12:37:00 PM ******/
SET ANSI_NULLS ON
GO

SET QUOTED_IDENTIFIER ON
GO

CREATE TABLE [dbo].[Repset_Fsm_Vendor_Archive](
	[Repset_Fsm_Vendor_Archive_ID] [bigint] IDENTITY(1,1) NOT NULL,
	[Repset_Fsm_Vendor_Active_ID] [bigint] NULL,
	[_Action] [varchar](500) NULL,
	[LavanteIdUDF] [varchar](500) NULL,
	[LegacyVendor] [varchar](500) NULL,
	[LegalName] [varchar](500) NULL,
	[RepSet_Variation_ID] [varchar](500) NULL,
	[UniqueID] [varchar](500) NULL,
	[Vendor] [varchar](500) NULL,
	[VendorClass] [varchar](500) NULL,
	[VendorGroup] [varchar](500) NULL,
	[VendorName] [varchar](500) NULL,
	[VendorStatus] [varchar](500) NULL,
	[VendorStatus_State] [varchar](500) NULL,
	[create_stamp_timestamp] [datetime2](3) NULL,
	[update_stamp_timestamp] [datetime2](3) NULL,
	[FileName] [varchar](500) NULL,
	[REPORT_DT] [datetime] NULL,
	[BatchID] [varchar](100) NULL,
	[ArchiveDateTime] [datetime] NULL,
	[RowHash] [varbinary](32) NULL,
 CONSTRAINT [PK_Repset_Fsm_Vendor_Archive_ID] PRIMARY KEY CLUSTERED 
(
	[Repset_Fsm_Vendor_Archive_ID] ASC
)WITH (PAD_INDEX = OFF, STATISTICS_NORECOMPUTE = OFF, IGNORE_DUP_KEY = OFF, ALLOW_ROW_LOCKS = ON, ALLOW_PAGE_LOCKS = ON, OPTIMIZE_FOR_SEQUENTIAL_KEY = OFF) ON [PRIMARY]
) ON [PRIMARY]
GO

ALTER TABLE [dbo].[Repset_Fsm_Vendor_Archive] ADD  DEFAULT (getdate()) FOR [ArchiveDateTime]
GO

-------------------- Service Now VendorList DBHRLoadConfig config

INSERT INTO dbo.DBHRLoadConfig
(
    FileGroup,
    SchemaName,
    TableName,
    TableDBName,
    SourceQuery,
    SourceQueryWhere,
    ColumnsToEncrypt,
    LoadType,
    ThresholdRecordsLimit,
    PrimaryKeyColumns,
    LastRunTimestamp,
    DuplicateThresholdLimit,
    ChunkSize,
    ArchivePath
)
VALUES
(
    'Repset_Fsm_Vendor_FULL',
    'dbo',
    'Repset_Fsm_Vendor_Landing',
    'DBP_HR_INTG_01',
    'SELECT  "_Action","LavanteIdUDF", LegacyVendor,LegalName,RepSet_Variation_ID,UniqueID,Vendor,VendorClass,VendorGroup,VendorName,VendorStatus,VendorStatus_State,
     CONVERT(varchar(23), "create_stamp.timestamp", 121) AS create_stamp_timestamp,
     CONVERT(varchar(23), "update_stamp.timestamp", 121) AS update_stamp_timestamp
     FROM "default".Vendor_FSM_DL NOLOCK',
    NULL,
    NULL,
    'FULL',
    1,
    'vendor',
    '2025-12-29 15:36:46.923',
    1,
    10000,
    NULL
);
INSERT INTO dbo.DBHRLoadConfig
(
    FileGroup,
    SchemaName,
    TableName,
    TableDBName,
    SourceQuery,
    SourceQueryWhere,
    ColumnsToEncrypt,
    LoadType,
    ThresholdRecordsLimit,
    PrimaryKeyColumns,
    LastRunTimestamp,
    DuplicateThresholdLimit,
    ChunkSize,
    ArchivePath
)
VALUES
(
    'Repset_Fsm_Vendor_DELTA',
    'dbo',
    'Repset_Fsm_Vendor_Landing',
    'DBP_HR_INTG_01',
    'SELECT  "_Action","LavanteIdUDF", LegacyVendor,LegalName,RepSet_Variation_ID,UniqueID,Vendor,VendorClass,VendorGroup,VendorName,VendorStatus,VendorStatus_State,
     CONVERT(varchar(23), "create_stamp.timestamp", 121) AS create_stamp_timestamp,
     CONVERT(varchar(23), "update_stamp.timestamp", 121) AS update_stamp_timestamp
     FROM "default".Vendor_FSM_DL NOLOCK',
    'SELECT FORMAT(
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
     FROM {active_table_full}',
    NULL,
    'DELTA',
    0,
    'vendor',
    NULL,
    2,
    10000,
    NULL
);
INSERT INTO dbo.DBHRLoadConfig
(
    FileGroup,
    SchemaName,
    TableName,
    TableDBName,
    SourceQuery,
    SourceQueryWhere,
    ColumnsToEncrypt,
    LoadType,
    ThresholdRecordsLimit,
    PrimaryKeyColumns,
    LastRunTimestamp,
    DuplicateThresholdLimit,
    ChunkSize,
    ArchivePath
)
VALUES
(
    'Repset_Fsm_Vendor_INCREMENTAL',
    'dbo',
    'Repset_Fsm_Vendor_Landing',
    'DBP_HR_INTG_01',
    'SELECT  "_Action","LavanteIdUDF", LegacyVendor,LegalName,RepSet_Variation_ID,UniqueID,Vendor,VendorClass,VendorGroup,VendorName,VendorStatus,VendorStatus_State,
     CONVERT(varchar(23), "create_stamp.timestamp", 121) AS create_stamp_timestamp,
     CONVERT(varchar(23), "update_stamp.timestamp", 121) AS update_stamp_timestamp
     FROM "default".Vendor_FSM_DL NOLOCK',
    'SELECT FORMAT(
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
     FROM {active_table_full}',
    NULL,
    'INCREMENTAL',
    0,
    'vendor',
    NULL,
    2,
    10000,
    NULL
);

-------------------- Service Now VendorList VendorExtractConfig config

INSERT INTO dbo.VendorExtractConfig
(
    ExtractScriptName,
    VendorExtractDirectory,
    ExpectedDataVolume,
    DecryptColumnList,
    CreatedDateTime,
    Comments
)
VALUES
(
    'ServiceNow_VendorList_Outbound.py',
    '/data/python/outbound/ServiceNow/',
    0,
    NULL,
    GETDATE(),
    'eSrvicenow Vendorlist config'
);
