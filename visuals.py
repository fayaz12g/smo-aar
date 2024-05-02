
def create_visuals(do_screenshot, do_disable_fxaa, do_disable_dynamicres):

    screenshot = "disabled"
    disablefxaa = "disabled"
    disabledynamicres = "disabled"

    do_island = False
    
    visual_fixes = []

    if do_screenshot:
        screenshot = "enabled"
    if do_disable_fxaa:
        disablefxaa = "enabled"
    if do_disable_dynamicres:
        disabledynamicres = "enabled"
        
    visuals1_0_0 = f'''// Screenshot Mode Graphics
@{screenshot}
00A56568 68008052
00A55CD0 1F2003D5
00A55CD4 1F2003D5
@disabled

// Disable FXAA
@{disablefxaa}
00B92318 08000014
@disabled

// Disable Dynamic Resolution
@{disabledynamicres}
00A583B4 1F2003D5
00A583C8 1F2003D5
@stop
'''

    visuals1_3_0= f'''// Screenshot Mode Graphics
@{screenshot}
008fe52c 00103E1E
0098b648 E003271E
@disabled

// Disable FXAA
@{disablefxaa}
009BD3A8 08000014
@disabled

// Disable Dynamic Resolution
@{disabledynamicres}
005EE438 1F2003D5
004e27bc 03408152
004e27c0 04B48052
004e27d8 03408152
004e27dc 04B48052
004bf34c 04408152
004bf350 05B48052
004bf354 06408152
004bf358 07B48052
004bf2a4 094081D2
004bf2a8 09B4C0F2
@stop
'''

    visuals1_2_0 = f'''// Screenshot Mode Graphics
@disabled
00A56568 68008052
00A55CD0 1F2003D5
00A55CD4 1F2003D5
@disabled

// Disable FXAA
@disabled
00B92318 08000014
@disabled

// Disable Dynamic Resolution
@disabled
00A583B4 1F2003D5
00A583C8 1F2003D5
@stop
'''

    visual_fixes.append(visuals1_0_0)
    visual_fixes.append(visuals1_3_0)
    visual_fixes.append(visuals1_2_0)
    
    return visual_fixes