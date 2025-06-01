[Setup]
AppName=Contract Generator (Demo)
AppVersion=1.0
DefaultDirName={autopf}\Contract Generator
DefaultGroupName=Contract Generator
UninstallDisplayIcon={app}\gui.exe
OutputBaseFilename=ContractGeneratorSetup
OutputDir=.

Compression=lzma
WizardStyle=modern
SolidCompression=yes
SetupIconFile=src\icon-contr.ico

[Files]
Source: "src\dist\gui.exe"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\icon-contr.ico"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\main.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\config.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\create_db.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\database.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\add_customer_gui.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\document_generator.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\act_genetaror.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "src\edit_customer.py"; DestDir: "{app}"; Flags: ignoreversion
Source: "data\*"; DestDir: "{app}\data"; Flags: recursesubdirs ignoreversion


[Tasks]
Name: "desktopicon"; Description: "Create a desktop shortcut"; GroupDescription: "Additional tasks:"; Flags: unchecked

[Icons]
Name: "{group}\Contract Generator"; Filename: "{app}\gui.exe"; IconFilename: "{app}\icon-contr.ico"
Name: "{group}\Uninstall Contract Generator"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Contract Generator"; Filename: "{app}\gui.exe"; Tasks: desktopicon; IconFilename: "{app}\icon-contr.ico"


[Registry]
Root: HKCU; Subkey: "Software\EmailSender_ru"; ValueType: string; ValueName: "Installed"; ValueData: "1"

[Run]
Filename: "{app}\gui.exe"; Description: "Запустить Contract Generator"; Flags: nowait postinstall skipifsilent
