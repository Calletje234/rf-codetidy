*** Setting *** 
Resource            ${CURDIR}${/}..${/}..${/}..${/}resources${/}resources.robot    
Suite Setup         Setup 

*** Test Cases ***
Login and run behandelaar workflows
    Log to console    \n
    Login to BPM with user ${ONC_BEHANDELAAR} and password ${ONC_PASSWORD}
    ${signals}=       Read signal file zelfmeldersignals.txt
    ${sig}=           evaluate    json.loads('''${signals}''')    json
    Connect to BPM-DB ONCDB schema ${DB2_SCHEMA_BPMONC}
    FOR    ${TESTCASE}    IN    @{sig}
        Run Behandelaar WorkFlow    ${TESTCASE}
    END 
    
Create files
    ${json}=    evaluate    json.dumps(${gsvlist})    json
    Append To File    ${FILE_PATH}${fngsvzelf}    ${json}
    ${json}=    evaluate    json.dumps(${zrclist})    json
    Append To File    ${FILE_PATH}${fnzrczelf}    ${json}      

    
*** Keywords ***
Setup
    ${AUTH}    Create List    ${ONC_ALL}    ${ONC_PASSWORD}    
    Start browser with delay 500ms
    Create datafile            ${fngsvzelf}
    Create datafile            ${fnzrczelf} 
    ${gsvlist}                 create list
    ${zrclist}                 create list
    Set Suite Variable         ${gsvlist}
    Set Suite Variable         ${zrclist}
    Set Suite Variable         ${AUTH}
    
Run Behandelaar WorkFlow
    [Arguments]    ${TESTCASE}
    ${signalid}=       get from dictionary    ${TESTCASE}    signaal
    ${uitnodiging}=    get from dictionary    ${TESTCASE}    uitnodiging
    ${tcname}=         get from dictionary    ${TESTCASE}    testcase
    log to console    Running case: ${tcname}
    ${instanceid}=    Retrieve BPM instanceid from schema ${DB2_SCHEMA_BPMONC} for signal ${signalid}
    Append To File    ${filepath}${fninstanceids}    ${instanceid}\n
    Run keyword if    '${tcname}' == 'Zelf-BehIsTestuser'    Handle ONC uitzendkracht workflow for intanceid ${instanceid} when not allowed
    Run keyword if    '${tcname}' != 'Zelf-BehIsTestuser'    Run Keywords    Handle ONC behandelaar worfklow for instanceid ${instanceid} with uitnodiging ${uitnodiging}
    ...    AND    Add verification for gsv    ${tcname}    ${signalid}      ${uitnodiging}
    ...    AND    Run keyword if    '${uitnodiging}' == 'Behandelen'    Add verification for zrc    ${tcname}    ${instanceid}    ${uitnodiging}    

Filter tasks by string ${search} and start first task containing ${label}
    Fill text                          css=input[ng-model='searchFilter']    ${search}   
    Browser.Press Keys                 css=input[ng-model='searchFilter']    Enter
    wait for elements state            css=a[title*='${search}']:nth-of-type(1)    visible   
    Hover                              css=a[title*='${search}']:nth-of-type(1)
    Click                              css=a[title*='${search}']:nth-of-type(1)     

Handle ONC behandelaar worfklow for instanceid ${instanceid} with uitnodiging ${keuze}
    click    xpath=//div[@class='menu-link-body']//a[@title='Werk']
    Wait for tasklist To become available
    Filter tasks by string ${instanceid} and start first task containing zelfmelder

    wait for elements state              ${iframecheck}    attached
    ${typezaak}=      browser.get text     ${iframe} css=p[id*='zaakTypeOmschrijving']
    ${shortid}=       browser.get text     ${iframe} css=p[id*='zaakShortId']
    ${bsn}=           browser.get text     ${iframe} css=p[id*='zaakSubject']
    ${regdat}=        browser.get text     ${iframe} css=p[id*='zaakRegistratie']
    ${status}=        browser.get text     ${iframe} css=p[id*='zaakStatusOmschrijving']
    ${aanleiding}=    browser.get text     ${iframe} css=p[id*='zaakAanleiding']
    click        ${iframe} css=button[id*='Comments'][class='btn btn-labeled']
    Fill text    ${iframe} css=textarea[id*='Comments']    Robot Test
    Keyboard Key                       press    Tab
    Keyboard Key                       press    Tab
    Keyboard Key                       press    Enter
    Select Dropdown Menu    ${iframe} css=select[id='singleselect-Actions_Stack_CV1:ActionSelectDropdownID']    ${keuze}
    Run keyword if    '${keuze}' == 'Behandelen'    Run Keywords
    ...    Select Dropdown Menu    ${iframe} css=select[id='singleselect-selectInvorderingPauzeerd']    Ja
    ...    AND    Select Dropdown Menu    ${iframe} css=select[id='singleselect-selectOntBevBriefVerstuurd']    Ja
    Run keyword if    '${keuze}' == 'Afgehandeld'    Run Keyword    Select Dropdown Menu    ${iframe} css=select[id='singleselect-selectAfwBriefVerstuurd']    Ja
    Click    ${iframe} css=button[id='button-button-UitzendkrachtOK']
    Wait for elements state            ${iframe} css=button[id='button-button-Confirm_and_Validate_Button_Extension_CV1:OKButton']    attached   
    Click                              ${iframe} css=button[id='button-button-Confirm_and_Validate_Button_Extension_CV1:OKButton']    noWaitAfter=True   
    Wait for elements state            xpath=//div[@class='menu-link-body']//a[@title='Werk']    visible 
    
Add verification for gsv
    [Arguments]    ${tcname}    ${signalid}    ${uitnodiging}
    ${gsvdict}     create dictionary
    set to dictionary    ${gsvdict}    testcase      ${tcname}
    set to dictionary    ${gsvdict}    signaal       ${signalid}
    Run Keyword If    '${uitnodiging}' == 'Behandelen'      set to dictionary    ${gsvdict}    status        INPROGRESS
    Run Keyword If    '${uitnodiging}' == 'Afgehandeld'     set to dictionary    ${gsvdict}    status        FINISHED
    append to list       ${gsvlist}    ${gsvdict}      

Add verification for zrc
    [Arguments]    ${tcname}    ${instanceid}    ${uitnodiging}
    ${zrcdict}     create dictionary
    set to dictionary    ${zrcdict}    testcase      ${tcname}
    set to dictionary    ${zrcdict}    instance      ${instanceid}
    Run Keyword If    '${uitnodiging}' == 'Behandelen'      set to dictionary    ${zrcdict}    status        IN_BEHANDELING
    Run Keyword If    '${uitnodiging}' == 'Afgehandeld'     set to dictionary    ${zrcdict}    status        AFGEHANDELD
    append to list       ${zrclist}    ${zrcdict}     
 
*** Variables ***
${gsvlist}       ${EMPTY}
${zrclist}       ${EMPTY}
${gsvdict}       ${EMPTY}
${zrcdict}       ${EMPTY}
${DB2_SCHEMA_BPMONC}
${AUTH}          ${EMPTY}