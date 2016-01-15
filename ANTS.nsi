;NSIS Modern User Interface
;Basic Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

  ;Name and file
  Name "ANTS"
  OutFile "setup-ANTS.exe"

  ;Default installation folder
  InstallDir "$PROGRAMFILES\ANTS-Transfer_System"
  
  ;Get installation folder from registry if available
  InstallDirRegKey HKCU "Software\ANTS-Transfer_System" ""

  ;Request application privileges for Windows Vista
  RequestExecutionLevel admin

;--------------------------------
;Interface Settings

  !define MUI_HEADERIMAGE
  !define MUI_HEADERIMAGE_BITMAP "C:\Users\gw234478\Dropbox\ants\ANTS.bmp" ; optional
  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_WELCOME
  !insertmacro MUI_PAGE_LICENSE "C:\Users\gw234478\Dropbox\ants\LICENSE.txt"
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  !insertmacro MUI_PAGE_FINISH
  
  !insertmacro MUI_UNPAGE_WELCOME
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  !insertmacro MUI_UNPAGE_FINISH
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

# start default section
Section
 
    # set the installation directory as the destination for the following actions
    SetOutPath $INSTDIR
 
    # write program files
    File "C:\Users\gw234478\Dropbox\ants\ANTS.exe"
    File "C:\Users\gw234478\Dropbox\ants\antsFromBoot.exe"
    File "C:\Users\gw234478\Dropbox\ants\LICENSE.txt"
    File "C:\Users\gw234478\Dropbox\ants\README.md"
    File /r "C:\Users\gw234478\Dropbox\ants\tools"
	
	SetOutPath "$APPDATA\ANTS-Transfer_System"
	IfFileExists "$EXEDIR\config.xml" ConfigExists
	ConfigExists:
		CopyFiles "$EXEDIR\config.xml"  "$APPDATA\ANTS-Transfer_System\config.xml"
	goto PastConfigTest
	PastConfigTest:
	
	;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall-ANTS.exe"
 
    
SectionEnd

Section "Start Menu Shortcut" SecStart

  SetOutPath $INSTDIR
    
  ;Store installation folder
  WriteRegStr HKCU "Software\ANTS-Transfer_System" "" $INSTDIR
  
  # create a shortcut named "new shortcut" on the Desktop
  # point the new shortcut at the program uninstaller
  CreateShortCut "$SMPROGRAMS\ANTS.lnk" "$INSTDIR\ANTS.exe"

SectionEnd

Section "Add Option to the Context Menu" SecContext

  SetOutPath $INSTDIR
    
  WriteRegStr HKCR "Directory\Shell\Send to the Archives with ANTS\command"  "" "$\"$INSTDIR\ANTS.exe$\" %1" 
  WriteRegStr HKCR "Directory\Shell\Send to the Archives with ANTS"  "Icon" "$\"$INSTDIR\ANTS.exe$\"" 
  WriteRegStr HKCR "*\Shell\Send to the Archives with ANTS\command"  "" "$\"$INSTDIR\ANTS.exe$\" %1" 
  WriteRegStr HKCR "*\Shell\Send to the Archives with ANTS"  "Icon" "$\"$INSTDIR\ANTS.exe$\"" 

SectionEnd

Section /o "Create Desktop Shortcut" SecDesktop

  SetOutPath $INSTDIR
    
  ;Store installation folder
  WriteRegStr HKCU "Software\ANTS-Transfer_System" "" $INSTDIR
  
  # create a shortcut named "new shortcut" in the start menu programs directory
  # point the new shortcut at the program uninstaller
  CreateShortCut "$DESKTOP\ANTS.lnk" "$INSTDIR\ANTS.exe"

SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecDesktop ${LANG_ENGLISH} "This places a shortcut to ANTS on your desktop."
  LangString DESC_SecStart ${LANG_ENGLISH} "This places a shortcut to ANTS in the Start Menu."
  LangString DESC_SecContext ${LANG_ENGLISH} "This places an option to use ANTS in the context (right-click) menu. If you select this option, you will be able to right-click on any file or folder and transfer it using ANTS."

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecDesktop} $(DESC_SecDesktop)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecStart} $(DESC_SecStart)
    !insertmacro MUI_DESCRIPTION_TEXT ${SecContext} $(DESC_SecContext)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  Delete "$INSTDIR\Uninstall-ANTS.exe"
  
  Delete "$INSTDIR\ANTS.exe"
  Delete "$INSTDIR\antsFromBoot.exe"
  Delete "$INSTDIR\LICENSE.txt"
  Delete "$INSTDIR\README.md"
  
  Delete "$DESKTOP\ANTS.lnk"
  
  Delete "$SMPROGRAMS\ANTS.lnk"

  RMDir  /r "$APPDATA\ANTS-Transfer_System"
  RMDir  /r "$INSTDIR\tools"
  RMDir "$INSTDIR"

  DeleteRegKey /ifempty HKCU "Software\ANTS-Transfer_System"
  DeleteRegKey  HKCR "Directory\Shell\Send to the Archives with ANTS" 
  DeleteRegKey  HKCR "*\Shell\Send to the Archives with ANTS" 

SectionEnd