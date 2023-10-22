;################################################################################################
;# Google Earth custom keyboard shortcuts (for mobile view mode)
;# Works on Windows with Auto Hotkey
;# Default margin values for 1920 by 1080 resolution and whatever my screen's pixel density is
;# Tested on Windows 10
;################################################################################################

; Toggle street view on map view
!d::
WindowTitle := "Google Earth - Google Chrome"
If WinActive(WindowTitle)
{
    WinGetPos, winx, winy, winw, winh, A
    pressx := winw - 35
    pressy := winh - 130
    SetMouseDelay, 0
    MouseGetPos, x, y ; save current mouse position
    Click, %pressx%`, %pressy%`
    MouseMove, x, y, 0 ; restore mouse position
}
return

; Exit street view
; Activates search if not in street view
!s::
WindowTitle := "Google Earth - Google Chrome"
If WinActive(WindowTitle)
{
    SetMouseDelay, 0
    MouseGetPos, x, y
    Click, 27, 110
    MouseMove, x, y, 0
}
return

; Reset to north-top angle on map view
!f::
WindowTitle := "Google Earth - Google Chrome"
If WinActive(WindowTitle)
{
    WinGetPos, winx, winy, winw, winh, A
    pressx := winw - 35
    pressy := winh - 202
    ; Check the pixel color because the button disappears when the view angle is already north-top
    ; If street view toggle is on and the view angle button is not visible and this shortcut is activated
    ; street view might be activated by accident so checking the color at the button location prevents that
    PixelGetColor, color, pressx, pressy
    If (color == 0x1f1f1f)
    {
        SetMouseDelay, 0
        MouseGetPos, x, y
        Click, %pressx%`, %pressy%`
        MouseMove, x, y, 0
    }
}
return