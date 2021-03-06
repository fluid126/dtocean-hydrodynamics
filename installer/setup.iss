; Script generated by the Inno Script Studio Wizard.
; SEE THE DOCUMENTATION FOR DETAILS ON CREATING INNO SETUP SCRIPT FILES!

#define MyAppName "DTOcean Hydrodynamic Data"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "DTOcean"
#define MyAppURL "http://www.dtocean.eu/"
#define BinPath "bin"
#define WaveIncludePath "data\dtocean_wec"
#define TidalIncludePath "data\dtocean_tidal"
#define IniDirName "DTOcean Hydrodynamics"


[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{54C4421C-EB34-4D00-A9F3-B37593213A75}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={sd}\DTOcean
DisableDirPage=yes
DefaultGroupName={#MyAppName}
DisableProgramGroupPage=yes
OutputBaseFilename=dtocean-hydrodynamic-data-1.0-standalone
Compression=lzma
SolidCompression=yes
PrivilegesRequired=lowest
UninstallFilesDir={commonappdata}\{#MyAppPublisher}\{#MyAppName}

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"

[Files]
Source: "..\{#BinPath}\*"; DestDir: "{app}\{#BinPath}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\{#WaveIncludePath}\*"; DestDir: "{app}\{#WaveIncludePath}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\{#TidalIncludePath}\*"; DestDir: "{app}\{#TidalIncludePath}"; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "..\dtocean_hydro\config\install.ini"; DestDir: "{commonappdata}\{#MyAppPublisher}\{#IniDirName}"; DestName: "install.ini"; Permissions: users-modify
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Icons]
Name: "{group}\{cm:UninstallProgram,{#MyAppName}}"; Filename: "{uninstallexe}"

[INI]
Filename: "{commonappdata}\{#MyAppPublisher}\{#IniDirName}\install.ini"; Section: "dtocean_tidal"; Key: "include_path"; String: "{app}\{#TidalIncludePath}";
Filename: "{commonappdata}\{#MyAppPublisher}\{#IniDirName}\install.ini"; Section: "dtocean_wec"; Key: "bin_path"; String: "{app}\{#BinPath}";
Filename: "{commonappdata}\{#MyAppPublisher}\{#IniDirName}\install.ini"; Section: "dtocean_wec"; Key: "include_path"; String: "{app}\{#WaveIncludePath}";

[Code]
function GetPath(Value: String): String;
var
  OrigPath: string;
begin
  if RegQueryStringValue(HKCU, 'Software\DTOcean', 'INSTALL_DIR', OrigPath) then
    Result := OrigPath
  else
    MsgBox('DTOcean installation directory not found!', mbError, MB_OK);
end;
