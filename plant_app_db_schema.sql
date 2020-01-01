CREATE TABLE IF NOT EXISTS AppUser (
    UserID INT NOT NULL ,
    Username VARCHAR  NOT NULL ,
    PasswordHash VARCHAR  NOT NULL ,
    DateJoined VARCHAR  NOT NULL ,
    Email VARCHAR  NOT NULL ,
    RoleID INT  NOT NULL ,
    PRIMARY KEY (
        UserID
    ),
    CONSTRAINT uc_AppUser_Username UNIQUE (
        Username
    ),
    CONSTRAINT uc_AppUser_Email UNIQUE (
        Email
    )
);

CREATE TABLE IF NOT EXISTS AppUserPrivileges (
    RoleID INT  NOT NULL ,
    RoleDescription VARCHAR(20)  NOT NULL ,
    PRIMARY KEY (
        RoleID
    )
);

CREATE TABLE IF NOT EXISTS PlotInfo (
    PlotID INT  NOT NULL ,
    PlotName varchar(60)  NOT NULL ,
    UserID INT  NOT NULL ,
    DateCreated VARCHAR  NOT NULL ,
    PlotTypeID INT  NOT NULL ,
    SensorSetID INT  NOT NULL ,
    PlantID INT  NOT NULL ,
    PRIMARY KEY (
        PlotID
    ),
    CONSTRAINT uc_PlotInfo_PlotName UNIQUE (
        PlotName
    )
);

CREATE TABLE IF NOT EXISTS PlotTypes (
    PlotTypeID INT  NOT NULL ,
    PlotTypeDescription varchar(50)  NOT NULL ,
    PRIMARY KEY (
        PlotTypeID
    )
);

CREATE TABLE IF NOT EXISTS UserNotes (
    NoteID INT  NOT NULL ,
    UserID INT  NOT NULL ,
    NoteContent varchar(250)  NOT NULL ,
    NoteTag varchar(20)  NOT NULL ,
    PRIMARY KEY (
        NoteID
    )
);

CREATE TABLE IF NOT EXISTS PlantEncyclopedia (
    PlantID INT  NOT NULL ,
    PlantName varchar(50)  NOT NULL ,
    PlantAltName varchar(50)  NOT NULL ,
    PrimarySource varchar(150)  NOT NULL ,
    SecondarySource varchar(150)  NOT NULL ,
    PlantRequirementsSetID INT  NOT NULL ,
    PRIMARY KEY (
        PlantID
    )
);

CREATE TABLE IF NOT EXISTS PlantRequirementSetItem (
    PlantRequirementItemID INT  NOT NULL ,
    PlantRequirementsSetID INT  NOT NULL ,
    RequirementValue float  NOT NULL ,
    RequirementMetricID INT  NOT NULL ,
    PRIMARY KEY (
        PlantRequirementItemID
    )
);

CREATE TABLE IF NOT EXISTS RequirementMetricDefinition (
    RequirementMetricID INT  NOT NULL ,
    RequirementDescription varchar(20)  NOT NULL ,
    RequirementUnit varchar(10)  NOT NULL ,
    PRIMARY KEY (
        RequirementMetricID
    )
);

CREATE TABLE IF NOT EXISTS SensorSetItems (
    SensorSetItemID INT  NOT NULL ,
    SensorSetID INT  NOT NULL ,
    SensorValue float  NOT NULL ,
    SensorItemID INT  NOT NULL ,
    PRIMARY KEY (
        SensorSetItemID
    )
);

CREATE TABLE IF NOT EXISTS SensorItemDefinition (
    SensorItemID INT  NOT NULL ,
    SensorDescription varchar(20)  NOT NULL ,
    SensorUnit varchar(10)  NOT NULL ,
    PRIMARY KEY (
        SensorItemID
    )
);

--
--ALTER TABLE AppUser ADD CONSTRAINT fk_AppUser_RoleID FOREIGN KEY(RoleID)
--REFERENCES AppUserPrivileges (RoleID);
--
--ALTER TABLE PlotInfo ADD CONSTRAINT fk_PlotInfo_UserID FOREIGN KEY(UserID)
--REFERENCES AppUser (UserID);
--
--ALTER TABLE PlotInfo ADD CONSTRAINT fk_PlotInfo_PlotTypeID FOREIGN KEY(PlotTypeID)
--REFERENCES PlotTypes (PlotTypeID);
--
--ALTER TABLE PlotInfo ADD CONSTRAINT fk_PlotInfo_PlantID FOREIGN KEY(PlantID)
--REFERENCES PlantEncyclopedia (PlantID);
--
--ALTER TABLE UserNotes ADD CONSTRAINT fk_UserNotes_UserID FOREIGN KEY(UserID)
--REFERENCES AppUser (UserID);
--
--ALTER TABLE PlantEncyclopedia ADD CONSTRAINT fk_PlantEncyclopedia_PlantRequirementsSetID FOREIGN KEY(PlantRequirementsSetID)
--REFERENCES PlantRequirementSetItem (PlantRequirementsSetID);
--
--ALTER TABLE PlantRequirementSetItem ADD CONSTRAINT fk_PlantRequirementSetItem_RequirementMetricID FOREIGN KEY(RequirementMetricID)
--REFERENCES RequirementMetricDefinition (RequirementMetricID);
--
--ALTER TABLE SensorSetItems ADD CONSTRAINT fk_SensorSetItems_SensorSetID FOREIGN KEY(SensorSetID)
--REFERENCES PlotInfo (SensorSetID);
--
--ALTER TABLE SensorItemDefinition ADD CONSTRAINT fk_SensorItemDefinition_SensorItemID FOREIGN KEY(SensorItemID)
--REFERENCES SensorSetItems (SensorItemID);
--
