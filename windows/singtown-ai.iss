#define MyAppName "SingTown AI"
#define MyAppVersion "0.1.0"
#define MyAppPublisher "SingTown LLC"
#define MyAppURL "https://ai.singtown.com/"
#define WslName "SingTownAI"
#define MyAppExe "launcher.dist\launcher.exe"
#define WslKernel "wsl.msi"
#define WslFolder "wsl"

[Setup]
; NOTE: The value of AppId uniquely identifies this application. Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{528A38D3-34B6-46C5-BDE9-20C5F445867D}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
;AppVerName={#MyAppName} {#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={autopf}\{#MyAppName}
UninstallDisplayIcon={app}\{#MyAppExe}
; "ArchitecturesAllowed=x64compatible" specifies that Setup cannot run
; on anything but x64 and Windows 11 on Arm.
ArchitecturesAllowed=x64compatible
; "ArchitecturesInstallIn64BitMode=x64compatible" requests that the
; install be done in "64-bit mode" on x64 or Windows 11 on Arm,
; meaning it should use the native 64-bit Program Files directory and
; the 64-bit view of the registry.
ArchitecturesInstallIn64BitMode=x64compatible
DisableProgramGroupPage=yes
; Uncomment the following line to run in non administrative install mode (install for current user only).
;PrivilegesRequired=lowest
OutputDir=../build
OutputBaseFilename=singtown-ai-installer-v{#MyAppVersion}
SolidCompression=yes
WizardStyle=modern
DisableWelcomePage=yes
LicenseFile=../LICENSE

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"
Name: "chinesesimplified"; MessagesFile: ".\isl\ChineseSimplified.isl"
Name: "arabic"; MessagesFile: "compiler:Languages\Arabic.isl"
Name: "armenian"; MessagesFile: "compiler:Languages\Armenian.isl"
Name: "brazilianportuguese"; MessagesFile: "compiler:Languages\BrazilianPortuguese.isl"
Name: "bulgarian"; MessagesFile: "compiler:Languages\Bulgarian.isl"
Name: "catalan"; MessagesFile: "compiler:Languages\Catalan.isl"
Name: "corsican"; MessagesFile: "compiler:Languages\Corsican.isl"
Name: "czech"; MessagesFile: "compiler:Languages\Czech.isl"
Name: "danish"; MessagesFile: "compiler:Languages\Danish.isl"
Name: "dutch"; MessagesFile: "compiler:Languages\Dutch.isl"
Name: "finnish"; MessagesFile: "compiler:Languages\Finnish.isl"
Name: "french"; MessagesFile: "compiler:Languages\French.isl"
Name: "german"; MessagesFile: "compiler:Languages\German.isl"
Name: "hebrew"; MessagesFile: "compiler:Languages\Hebrew.isl"
Name: "hungarian"; MessagesFile: "compiler:Languages\Hungarian.isl"
Name: "italian"; MessagesFile: "compiler:Languages\Italian.isl"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"
Name: "korean"; MessagesFile: "compiler:Languages\Korean.isl"
Name: "norwegian"; MessagesFile: "compiler:Languages\Norwegian.isl"
Name: "polish"; MessagesFile: "compiler:Languages\Polish.isl"
Name: "portuguese"; MessagesFile: "compiler:Languages\Portuguese.isl"
Name: "russian"; MessagesFile: "compiler:Languages\Russian.isl"
Name: "slovak"; MessagesFile: "compiler:Languages\Slovak.isl"
Name: "slovenian"; MessagesFile: "compiler:Languages\Slovenian.isl"
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"
Name: "swedish"; MessagesFile: "compiler:Languages\Swedish.isl"
Name: "tamil"; MessagesFile: "compiler:Languages\Tamil.isl"
Name: "turkish"; MessagesFile: "compiler:Languages\Turkish.isl"
Name: "ukrainian"; MessagesFile: "compiler:Languages\Ukrainian.isl"

[Code]
var
  ResultCodeCheckWSL: Integer;
  ResultCodeCheckVMP: Integer;
  ResultCodeEnableWSL: Integer;
  ResultCodeEnableVMP: Integer;
  ResultCodeReboot: Integer;

procedure InitializeWizard;
begin
  Exec('powershell.exe',
    '-Command "if ((Get-WindowsOptionalFeature -Online -FeatureName Microsoft-Windows-Subsystem-Linux).State -eq ''Enabled'') { exit 0 } else { exit -1}"', '', SW_HIDE, ewWaitUntilTerminated, ResultCodeCheckWSL)
  Exec('powershell.exe', '-Command "if ((Get-WindowsOptionalFeature -Online -FeatureName VirtualMachinePlatform).State -eq ''Enabled'') { exit 0 } else { exit -1}"', '', SW_HIDE, ewWaitUntilTerminated, ResultCodeCheckVMP)

  if (ResultCodeCheckWSL <> 0) or (ResultCodeCheckVMP <> 0) then
  begin
    WizardForm.StatusLabel.Caption := 'Enable Feature Microsoft-Windows-Subsystem-Linux';
    WizardForm.ProgressGauge.Style := npbstMarquee;
    Exec('dism.exe', '/online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart','', SW_HIDE, ewWaitUntilTerminated, ResultCodeEnableWSL)
    
    WizardForm.StatusLabel.Caption := 'Enable Feature VirtualMachinePlatform';
    WizardForm.ProgressGauge.Style := npbstMarquee;
    Exec('dism.exe', '/online /enable-feature /featurename:VirtualMachinePlatform /all /norestart','', SW_HIDE, ewWaitUntilTerminated, ResultCodeEnableVMP)
    
    RegWriteStringValue(HKCU, 'Software\Microsoft\Windows\CurrentVersion\RunOnce', 'SingTownAIInstaller', ExpandConstant('{srcexe}'))
    MsgBox(ExpandConstant('{cm:WslRebootMsg}'), mbInformation, MB_OK)
    
    Exec('shutdown.exe', '/r /t 0','', SW_HIDE, ewWaitUntilTerminated, ResultCodeReboot)
    Abort;
  end
end;

[Files]
Source: "..\build\launcher.dist\*"; DestDir: "{app}\launcher.dist"; Flags: recursesubdirs createallsubdirs ignoreversion
Source: "..\build\singtown-ai-machine.tar"; DestDir: "{app}"; Flags: ignoreversion
Source: "..\build\{#WslKernel}"; DestDir: "{app}"; Flags: ignoreversion

[UninstallDelete]
Type: files; Name: "{app}\{#WslFolder}"

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; IconFilename: "{app}\launcher.dist\assets\fav.ico"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExe}"; IconFilename: "{app}\launcher.dist\assets\fav.ico"

[Run]
Filename: "msiexec.exe"; Parameters: "/i ""{app}\{#WslKernel}"" /passive /norestart"; Flags: waituntilterminated; StatusMsg: "Installing WSL Kernel"
Filename: "wsl.exe"; Parameters: "--set-default-version 2"; Flags: waituntilterminated runhidden
Filename: "wsl.exe"; Parameters: "--unregister {#WslName}"; Flags: waituntilterminated runhidden; StatusMsg: "Removing old SingTown AI Machine"
Filename: "wsl.exe"; Parameters: "--import {#WslName} ""{app}\{#WslFolder}"" ""{app}\singtown-ai-machine.tar"""; Flags: waituntilterminated runhidden; StatusMsg: "Install new SingTown AI Machine"
Filename: "{app}\{#MyAppExe}"; Flags: nowait postinstall skipifsilent

[CustomMessages]
english.WslRebootMsg=A restart is required to continue the installation. Restart now?
chinesesimplified.WslRebootMsg=需要重新启动才能继续安装。立即重启吗？