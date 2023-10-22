;################################################################################################
;# Google Maps custom keyboard shortcuts
;# Works on Windows with Auto Hotkey
;# Default margin values for 1920 by 1080 resolution and whatever my screen's pixel density is
;# Tested on Windows 10
;################################################################################################

STREET_VIEW_ENTER_XMARGIN := -150 ; from window right edge
STREET_VIEW_ENTER_YMARGIN := -34 ; from window bottom edge
STREET_VIEW_EXIT_XMARGIN := -30 ; from window right edge
STREET_VIEW_EXIT_YMARGIN := 110 ; from window top edge

SetTitleMatchMode, 2 ; to match window if a substring is contained in the title

; Toggle street view on map view
!d::
WindowTitle := "Google Maps"
If WinActive(WindowTitle)
{
    WinGetPos, winx, winy, winw, winh, A
    pressx := winw + STREET_VIEW_ENTER_XMARGIN
    pressy := winh + STREET_VIEW_ENTER_YMARGIN
    SetMouseDelay, 0
    MouseGetPos, x, y ; save current mouse position
    Click, %pressx%`, %pressy%`
    MouseMove, x, y, 0 ; restore mouse position
}
return

; Exit street view
!s::
WindowTitle := "Google Maps"
If WinActive(WindowTitle)
{
    WinGetPos, winx, winy, winw, winh, A
    pressx := winw + STREET_VIEW_EXIT_XMARGIN
    pressy := STREET_VIEW_EXIT_YMARGIN
    SetMouseDelay, 0
    MouseGetPos, x, y
    Click, %pressx%`, %pressy%`
    MouseMove, x, y, 0
}
return