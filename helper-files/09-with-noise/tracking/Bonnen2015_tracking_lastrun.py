﻿#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy3 Experiment Builder (v2024.2.4),
    on Tue Mar 25 00:26:17 2025
If you publish work using this script the most relevant publication is:

    Peirce J, Gray JR, Simpson S, MacAskill M, Höchenberger R, Sogo H, Kastman E, Lindeløv JK. (2019) 
        PsychoPy2: Experiments in behavior made easy Behav Res 51: 195. 
        https://doi.org/10.3758/s13428-018-01193-y

"""

# --- Import packages ---
from psychopy import locale_setup
from psychopy import prefs
from psychopy import plugins
plugins.activatePlugins()
from psychopy import sound, gui, visual, core, data, event, logging, clock, colors, layout, hardware
from psychopy.tools import environmenttools
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER, priority)

import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle, choice as randchoice
import os  # handy system and path functions
import sys  # to get file system encoding

import psychopy.iohub as io
from psychopy.hardware import keyboard

# --- Setup global variables (available in all functions) ---
# create a device manager to handle hardware (keyboards, mice, mirophones, speakers, etc.)
deviceManager = hardware.DeviceManager()
# ensure that relative paths start from the same directory as this script
_thisDir = os.path.dirname(os.path.abspath(__file__))
# store info about the experiment session
psychopyVersion = '2024.2.4'
expName = 'tracking'  # from the Builder filename that created this script
# information about this experiment
expInfo = {
    'participant': f"{randint(0, 999999):06.0f}",
    'session': '001',
    'date|hid': data.getDateStr(),
    'expName|hid': expName,
    'psychopyVersion|hid': psychopyVersion,
}

# --- Define some variables which will change depending on pilot mode ---
'''
To run in pilot mode, either use the run/pilot toggle in Builder, Coder and Runner, 
or run the experiment with `--pilot` as an argument. To change what pilot 
#mode does, check out the 'Pilot mode' tab in preferences.
'''
# work out from system args whether we are running in pilot mode
PILOTING = core.setPilotModeFromArgs()
# start off with values from experiment settings
_fullScr = True
_winSize = [1512, 982]
# if in pilot mode, apply overrides according to preferences
if PILOTING:
    # force windowed mode
    if prefs.piloting['forceWindowed']:
        _fullScr = False
        # set window size
        _winSize = prefs.piloting['forcedWindowSize']

def showExpInfoDlg(expInfo):
    """
    Show participant info dialog.
    Parameters
    ==========
    expInfo : dict
        Information about this experiment.
    
    Returns
    ==========
    dict
        Information about this experiment.
    """
    # show participant info dialog
    dlg = gui.DlgFromDict(
        dictionary=expInfo, sortKeys=False, title=expName, alwaysOnTop=True
    )
    if dlg.OK == False:
        core.quit()  # user pressed cancel
    # return expInfo
    return expInfo


def setupData(expInfo, dataDir=None):
    """
    Make an ExperimentHandler to handle trials and saving.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    dataDir : Path, str or None
        Folder to save the data to, leave as None to create a folder in the current directory.    
    Returns
    ==========
    psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    # remove dialog-specific syntax from expInfo
    for key, val in expInfo.copy().items():
        newKey, _ = data.utils.parsePipeSyntax(key)
        expInfo[newKey] = expInfo.pop(key)
    
    # data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
    if dataDir is None:
        dataDir = _thisDir
    filename = u'data/%s_%s_%s' % (expInfo['participant'], expName, expInfo['date'])
    # make sure filename is relative to dataDir
    if os.path.isabs(filename):
        dataDir = os.path.commonprefix([dataDir, filename])
        filename = os.path.relpath(filename, dataDir)
    
    # an ExperimentHandler isn't essential but helps with data saving
    thisExp = data.ExperimentHandler(
        name=expName, version='',
        extraInfo=expInfo, runtimeInfo=None,
        originPath='/Users/kbonnen/Library/CloudStorage/OneDrive-IndianaUniversity/Courses/V768-Measuring-Perception/V768-Psychophysics-labs/10-continuous-psychophysics/tracking/Bonnen2015_tracking_lastrun.py',
        savePickle=True, saveWideText=True,
        dataFileName=dataDir + os.sep + filename, sortColumns='time'
    )
    thisExp.setPriority('thisRow.t', priority.CRITICAL)
    thisExp.setPriority('expName', priority.LOW)
    # return experiment handler
    return thisExp


def setupLogging(filename):
    """
    Setup a log file and tell it what level to log at.
    
    Parameters
    ==========
    filename : str or pathlib.Path
        Filename to save log file and data files as, doesn't need an extension.
    
    Returns
    ==========
    psychopy.logging.LogFile
        Text stream to receive inputs from the logging system.
    """
    # set how much information should be printed to the console / app
    if PILOTING:
        logging.console.setLevel(
            prefs.piloting['pilotConsoleLoggingLevel']
        )
    else:
        logging.console.setLevel('warning')
    # save a log file for detail verbose info
    logFile = logging.LogFile(filename+'.log')
    if PILOTING:
        logFile.setLevel(
            prefs.piloting['pilotLoggingLevel']
        )
    else:
        logFile.setLevel(
            logging.getLevel('exp')
        )
    
    return logFile


def setupWindow(expInfo=None, win=None):
    """
    Setup the Window
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    win : psychopy.visual.Window
        Window to setup - leave as None to create a new window.
    
    Returns
    ==========
    psychopy.visual.Window
        Window in which to run this experiment.
    """
    if PILOTING:
        logging.debug('Fullscreen settings ignored as running in pilot mode.')
    
    if win is None:
        # if not given a window to setup, make one
        win = visual.Window(
            size=_winSize, fullscr=_fullScr, screen=0,
            winType='pyglet', allowGUI=False, allowStencil=False,
            monitor='testMonitor', color=[0,0,0], colorSpace='rgb',
            backgroundImage='', backgroundFit='none',
            blendMode='avg', useFBO=True,
            units='height',
            checkTiming=False  # we're going to do this ourselves in a moment
        )
    else:
        # if we have a window, just set the attributes which are safe to set
        win.color = [0,0,0]
        win.colorSpace = 'rgb'
        win.backgroundImage = ''
        win.backgroundFit = 'none'
        win.units = 'height'
    if expInfo is not None:
        # get/measure frame rate if not already in expInfo
        if win._monitorFrameRate is None:
            win._monitorFrameRate = win.getActualFrameRate(infoMsg='Attempting to measure frame rate of screen, please wait...')
        expInfo['frameRate'] = win._monitorFrameRate
    win.hideMessage()
    # show a visual indicator if we're in piloting mode
    if PILOTING and prefs.piloting['showPilotingIndicator']:
        win.showPilotingIndicator()
    
    return win


def setupDevices(expInfo, thisExp, win):
    """
    Setup whatever devices are available (mouse, keyboard, speaker, eyetracker, etc.) and add them to 
    the device manager (deviceManager)
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window in which to run this experiment.
    Returns
    ==========
    bool
        True if completed successfully.
    """
    # --- Setup input devices ---
    ioConfig = {}
    
    # Setup iohub keyboard
    ioConfig['Keyboard'] = dict(use_keymap='psychopy')
    
    # Setup iohub experiment
    ioConfig['Experiment'] = dict(filename=thisExp.dataFileName)
    
    # Start ioHub server
    ioServer = io.launchHubServer(window=win, **ioConfig)
    
    # store ioServer object in the device manager
    deviceManager.ioServer = ioServer
    
    # create a default keyboard (e.g. to check for escape)
    if deviceManager.getDevice('defaultKeyboard') is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='iohub'
        )
    # return True if completed successfully
    return True

def pauseExperiment(thisExp, win=None, timers=[], playbackComponents=[]):
    """
    Pause this experiment, preventing the flow from advancing to the next routine until resumed.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    timers : list, tuple
        List of timers to reset once pausing is finished.
    playbackComponents : list, tuple
        List of any components with a `pause` method which need to be paused.
    """
    # if we are not paused, do nothing
    if thisExp.status != PAUSED:
        return
    
    # start a timer to figure out how long we're paused for
    pauseTimer = core.Clock()
    # pause any playback components
    for comp in playbackComponents:
        comp.pause()
    # make sure we have a keyboard
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        defaultKeyboard = deviceManager.addKeyboard(
            deviceClass='keyboard',
            deviceName='defaultKeyboard',
            backend='ioHub',
        )
    # run a while loop while we wait to unpause
    while thisExp.status == PAUSED:
        # check for quit (typically the Esc key)
        if defaultKeyboard.getKeys(keyList=['escape']):
            endExperiment(thisExp, win=win)
        # sleep 1ms so other threads can execute
        clock.time.sleep(0.001)
    # if stop was requested while paused, quit
    if thisExp.status == FINISHED:
        endExperiment(thisExp, win=win)
    # resume any playback components
    for comp in playbackComponents:
        comp.play()
    # reset any timers
    for timer in timers:
        timer.addTime(-pauseTimer.getTime())


def run(expInfo, thisExp, win, globalClock=None, thisSession=None):
    """
    Run the experiment flow.
    
    Parameters
    ==========
    expInfo : dict
        Information about this experiment, created by the `setupExpInfo` function.
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    psychopy.visual.Window
        Window in which to run this experiment.
    globalClock : psychopy.core.clock.Clock or None
        Clock to get global time from - supply None to make a new one.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    # mark experiment as started
    thisExp.status = STARTED
    # make sure window is set to foreground to prevent losing focus
    win.winHandle.activate()
    # make sure variables created by exec are available globally
    exec = environmenttools.setExecEnvironment(globals())
    # get device handles from dict of input devices
    ioServer = deviceManager.ioServer
    # get/create a default keyboard (e.g. to check for escape)
    defaultKeyboard = deviceManager.getDevice('defaultKeyboard')
    if defaultKeyboard is None:
        deviceManager.addDevice(
            deviceClass='keyboard', deviceName='defaultKeyboard', backend='ioHub'
        )
    eyetracker = deviceManager.getDevice('eyetracker')
    # make sure we're running in the directory for this experiment
    os.chdir(_thisDir)
    # get filename from ExperimentHandler for convenience
    filename = thisExp.dataFileName
    frameTolerance = 0.001  # how close to onset before 'same' frame
    endExpNow = False  # flag for 'escape' or other condition => quit the exp
    # get frame duration from frame rate in expInfo
    if 'frameRate' in expInfo and expInfo['frameRate'] is not None:
        frameDur = 1.0 / round(expInfo['frameRate'])
    else:
        frameDur = 1.0 / 60.0  # could not measure, so guess
    
    # Start Code - component code to be run after the window creation
    
    # --- Initialize components for Routine "Wait" ---
    start_trial_text = visual.TextStim(win=win, name='start_trial_text',
        text='Use the red cursor to track the center of the light blob.\n\nClick the mouse or trackpad to start the trial.',
        font='Arial',
        pos=None, draggable=False, height=0.04, wrapWidth=None, ori=0.0, 
        color='white', colorSpace='rgb', opacity=None, 
        languageStyle='LTR',
        depth=0.0);
    start_trial_mouse = event.Mouse(win=win)
    x, y = [None, None]
    start_trial_mouse.mouseClock = core.Clock()
    
    # --- Initialize components for Routine "trial" ---
    response_mouse = event.Mouse(win=win)
    x, y = [None, None]
    response_mouse.mouseClock = core.Clock()
    noise_0 = visual.NoiseStim(
        win=win, name='noise_0',
        noiseImage=None, mask=None,
        ori=0.0, pos=(0, 0), size=(1, 1), sf=None,
        phase=0.0,
        color=[1,1,1], colorSpace='rgb',     opacity=None, blendmode='add', contrast=0.5,
        texRes=512, filter=None,
        noiseType='White', noiseElementSize=[0.0625], 
        noiseBaseSf=8.0, noiseBW=1.0,
        noiseBWO=30.0, noiseOri=0.0,
        noiseFractalPower=0.0,noiseFilterLower=1.0,
        noiseFilterUpper=8.0, noiseFilterOrder=0.0,
        noiseClip=3.0, imageComponent='Phase', interpolate=False, depth=-1.0)
    noise_0.buildNoise()
    noise = visual.NoiseStim(
        win=win, name='noise',
        noiseImage=None, mask=None,
        ori=0.0, pos=(0, 0), size=(1, 1), sf=None,
        phase=0.0,
        color=[1,1,1], colorSpace='rgb',     opacity=None, blendmode='add', contrast=0.5,
        texRes=512, filter=None,
        noiseType='White', noiseElementSize=[0.0625], 
        noiseBaseSf=8.0, noiseBW=1.0,
        noiseBWO=30.0, noiseOri=0.0,
        noiseFractalPower=0.0,noiseFilterLower=1.0,
        noiseFilterUpper=8.0, noiseFilterOrder=0.0,
        noiseClip=3.0, imageComponent='Phase', interpolate=False, depth=-2.0)
    noise.buildNoise()
    blob_0 = visual.GratingStim(
        win=win, name='blob_0',
        tex=None, mask='gauss', anchor='center',
        ori=45.0, pos=[0,0], draggable=False, size=1.0, sf=1.0, phase=0.25,
        color=[1,1,1], colorSpace='rgb',
        opacity=None, contrast=1.0, blendmode='add',
        texRes=512.0, interpolate=True, depth=-3.0)
    blob = visual.GratingStim(
        win=win, name='blob',
        tex=None, mask='gauss', anchor='center',
        ori=45.0, pos=[0,0], draggable=False, size=1.0, sf=1.0, phase=0.25,
        color=[1,1,1], colorSpace='rgb',
        opacity=None, contrast=1.0, blendmode='add',
        texRes=512.0, interpolate=True, depth=-4.0)
    cursor = visual.ShapeStim(
        win=win, name='cursor',
        size=(0.005, 0.005), vertices='circle',
        ori=0.0, pos=[0,0], draggable=False, anchor='center',
        lineWidth=1.0,
        colorSpace='rgb', lineColor='red', fillColor='red',
        opacity=None, depth=-6.0, interpolate=True)
    
    # create some handy timers
    
    # global clock to track the time since experiment started
    if globalClock is None:
        # create a clock if not given one
        globalClock = core.Clock()
    if isinstance(globalClock, str):
        # if given a string, make a clock accoridng to it
        if globalClock == 'float':
            # get timestamps as a simple value
            globalClock = core.Clock(format='float')
        elif globalClock == 'iso':
            # get timestamps in ISO format
            globalClock = core.Clock(format='%Y-%m-%d_%H:%M:%S.%f%z')
        else:
            # get timestamps in a custom format
            globalClock = core.Clock(format=globalClock)
    if ioServer is not None:
        ioServer.syncClock(globalClock)
    logging.setDefaultClock(globalClock)
    # routine timer to track time remaining of each (possibly non-slip) routine
    routineTimer = core.Clock()
    win.flip()  # flip window to reset last flip timer
    # store the exact time the global clock started
    expInfo['expStart'] = data.getDateStr(
        format='%Y-%m-%d %Hh%M.%S.%f %z', fractionalSecondDigits=6
    )
    
    # set up handler to look after randomisation of conditions etc
    trials = data.TrialHandler2(
        name='trials',
        nReps=4.0, 
        method='random', 
        extraInfo=expInfo, 
        originPath=-1, 
        trialList=data.importConditions('Bonnen2015Conditions.csv'), 
        seed=None, 
    )
    thisExp.addLoop(trials)  # add the loop to the experiment
    thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial:
            globals()[paramName] = thisTrial[paramName]
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    for thisTrial in trials:
        currentLoop = trials
        thisExp.timestampOnFlip(win, 'thisRow.t', format=globalClock.format)
        if thisSession is not None:
            # if running in a Session with a Liaison client, send data up to now
            thisSession.sendExperimentData()
        # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
        if thisTrial != None:
            for paramName in thisTrial:
                globals()[paramName] = thisTrial[paramName]
        
        # --- Prepare to start Routine "Wait" ---
        # create an object to store info about Routine Wait
        Wait = data.Routine(
            name='Wait',
            components=[start_trial_text, start_trial_mouse],
        )
        Wait.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the start_trial_mouse
        start_trial_mouse.x = []
        start_trial_mouse.y = []
        start_trial_mouse.leftButton = []
        start_trial_mouse.midButton = []
        start_trial_mouse.rightButton = []
        start_trial_mouse.time = []
        gotValidClick = False  # until a click is received
        # store start times for Wait
        Wait.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        Wait.tStart = globalClock.getTime(format='float')
        Wait.status = STARTED
        thisExp.addData('Wait.started', Wait.tStart)
        Wait.maxDuration = None
        # keep track of which components have finished
        WaitComponents = Wait.components
        for thisComponent in Wait.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "Wait" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        Wait.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            
            # *start_trial_text* updates
            
            # if start_trial_text is starting this frame...
            if start_trial_text.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                start_trial_text.frameNStart = frameN  # exact frame index
                start_trial_text.tStart = t  # local t and not account for scr refresh
                start_trial_text.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(start_trial_text, 'tStartRefresh')  # time at next scr refresh
                # update status
                start_trial_text.status = STARTED
                start_trial_text.setAutoDraw(True)
            
            # if start_trial_text is active this frame...
            if start_trial_text.status == STARTED:
                # update params
                pass
            # *start_trial_mouse* updates
            
            # if start_trial_mouse is starting this frame...
            if start_trial_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                start_trial_mouse.frameNStart = frameN  # exact frame index
                start_trial_mouse.tStart = t  # local t and not account for scr refresh
                start_trial_mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(start_trial_mouse, 'tStartRefresh')  # time at next scr refresh
                # update status
                start_trial_mouse.status = STARTED
                start_trial_mouse.mouseClock.reset()
                prevButtonState = start_trial_mouse.getPressed()  # if button is down already this ISN'T a new click
            if start_trial_mouse.status == STARTED:  # only update if started and not finished!
                x, y = start_trial_mouse.getPos()
                start_trial_mouse.x.append(x)
                start_trial_mouse.y.append(y)
                buttons = start_trial_mouse.getPressed()
                start_trial_mouse.leftButton.append(buttons[0])
                start_trial_mouse.midButton.append(buttons[1])
                start_trial_mouse.rightButton.append(buttons[2])
                start_trial_mouse.time.append(start_trial_mouse.mouseClock.getTime())
                buttons = start_trial_mouse.getPressed()
                if buttons != prevButtonState:  # button state changed?
                    prevButtonState = buttons
                    if sum(buttons) > 0:  # state changed to a new click
                        pass
                        
                        continueRoutine = False  # end routine on response
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                Wait.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in Wait.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "Wait" ---
        for thisComponent in Wait.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for Wait
        Wait.tStop = globalClock.getTime(format='float')
        Wait.tStopRefresh = tThisFlipGlobal
        thisExp.addData('Wait.stopped', Wait.tStop)
        # store data for trials (TrialHandler)
        trials.addData('start_trial_mouse.x', start_trial_mouse.x)
        trials.addData('start_trial_mouse.y', start_trial_mouse.y)
        trials.addData('start_trial_mouse.leftButton', start_trial_mouse.leftButton)
        trials.addData('start_trial_mouse.midButton', start_trial_mouse.midButton)
        trials.addData('start_trial_mouse.rightButton', start_trial_mouse.rightButton)
        trials.addData('start_trial_mouse.time', start_trial_mouse.time)
        # the Routine "Wait" was not non-slip safe, so reset the non-slip timer
        routineTimer.reset()
        
        # --- Prepare to start Routine "trial" ---
        # create an object to store info about Routine trial
        trial = data.Routine(
            name='trial',
            components=[response_mouse, noise_0, noise, blob_0, blob, cursor],
        )
        trial.status = NOT_STARTED
        continueRoutine = True
        # update component parameters for each repeat
        # setup some python lists for storing info about the response_mouse
        response_mouse.x = []
        response_mouse.y = []
        response_mouse.leftButton = []
        response_mouse.midButton = []
        response_mouse.rightButton = []
        response_mouse.time = []
        gotValidClick = False  # until a click is received
        blob_0.setContrast(.5*blobHeight)
        blob_0.setSize([blobWidth*np.ones((2,))])
        blob_0.setTex(np.ones((512,512)))
        blob.setContrast(.5*blobHeight)
        blob.setSize([blobWidth*np.ones((2,))])
        blob.setTex(np.ones((512,512)))
        # Run 'Begin Routine' code from code
        blob.setPos((0,0))
        response_mouse.setPos((0,0))
        response_mouse.setVisible(0)
        blob.x = []
        blob.y = []
        # store start times for trial
        trial.tStartRefresh = win.getFutureFlipTime(clock=globalClock)
        trial.tStart = globalClock.getTime(format='float')
        trial.status = STARTED
        thisExp.addData('trial.started', trial.tStart)
        trial.maxDuration = None
        # keep track of which components have finished
        trialComponents = trial.components
        for thisComponent in trial.components:
            thisComponent.tStart = None
            thisComponent.tStop = None
            thisComponent.tStartRefresh = None
            thisComponent.tStopRefresh = None
            if hasattr(thisComponent, 'status'):
                thisComponent.status = NOT_STARTED
        # reset timers
        t = 0
        _timeToFirstFrame = win.getFutureFlipTime(clock="now")
        frameN = -1
        
        # --- Run Routine "trial" ---
        # if trial has changed, end Routine now
        if isinstance(trials, data.TrialHandler2) and thisTrial.thisN != trials.thisTrial.thisN:
            continueRoutine = False
        trial.forceEnded = routineForceEnded = not continueRoutine
        while continueRoutine and routineTimer.getTime() < 15.5:
            # get current time
            t = routineTimer.getTime()
            tThisFlip = win.getFutureFlipTime(clock=routineTimer)
            tThisFlipGlobal = win.getFutureFlipTime(clock=None)
            frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
            # update/draw components on each frame
            # *response_mouse* updates
            
            # if response_mouse is starting this frame...
            if response_mouse.status == NOT_STARTED and t >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                response_mouse.frameNStart = frameN  # exact frame index
                response_mouse.tStart = t  # local t and not account for scr refresh
                response_mouse.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(response_mouse, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.addData('response_mouse.started', t)
                # update status
                response_mouse.status = STARTED
                response_mouse.mouseClock.reset()
                prevButtonState = response_mouse.getPressed()  # if button is down already this ISN'T a new click
            
            # if response_mouse is stopping this frame...
            if response_mouse.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > response_mouse.tStartRefresh + 15.5-frameTolerance:
                    # keep track of stop time/frame for later
                    response_mouse.tStop = t  # not accounting for scr refresh
                    response_mouse.tStopRefresh = tThisFlipGlobal  # on global time
                    response_mouse.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.addData('response_mouse.stopped', t)
                    # update status
                    response_mouse.status = FINISHED
            if response_mouse.status == STARTED:  # only update if started and not finished!
                x, y = response_mouse.getPos()
                response_mouse.x.append(x)
                response_mouse.y.append(y)
                buttons = response_mouse.getPressed()
                response_mouse.leftButton.append(buttons[0])
                response_mouse.midButton.append(buttons[1])
                response_mouse.rightButton.append(buttons[2])
                response_mouse.time.append(response_mouse.mouseClock.getTime())
            
            # *noise_0* updates
            
            # if noise_0 is starting this frame...
            if noise_0.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                noise_0.frameNStart = frameN  # exact frame index
                noise_0.tStart = t  # local t and not account for scr refresh
                noise_0.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(noise_0, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'noise_0.started')
                # update status
                noise_0.status = STARTED
                noise_0.setAutoDraw(True)
            
            # if noise_0 is active this frame...
            if noise_0.status == STARTED:
                # update params
                pass
            
            # if noise_0 is stopping this frame...
            if noise_0.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > noise_0.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    noise_0.tStop = t  # not accounting for scr refresh
                    noise_0.tStopRefresh = tThisFlipGlobal  # on global time
                    noise_0.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'noise_0.stopped')
                    # update status
                    noise_0.status = FINISHED
                    noise_0.setAutoDraw(False)
            if noise_0.status == STARTED:
                if noise_0._needBuild:
                    noise_0.buildNoise()
                else:
                    if (frameN-noise_0.frameNStart) %             1==0:
                        noise_0.updateNoise()
            
            # *noise* updates
            
            # if noise is starting this frame...
            if noise.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                noise.frameNStart = frameN  # exact frame index
                noise.tStart = t  # local t and not account for scr refresh
                noise.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(noise, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'noise.started')
                # update status
                noise.status = STARTED
                noise.setAutoDraw(True)
            
            # if noise is active this frame...
            if noise.status == STARTED:
                # update params
                pass
            
            # if noise is stopping this frame...
            if noise.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > noise.tStartRefresh + 15-frameTolerance:
                    # keep track of stop time/frame for later
                    noise.tStop = t  # not accounting for scr refresh
                    noise.tStopRefresh = tThisFlipGlobal  # on global time
                    noise.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'noise.stopped')
                    # update status
                    noise.status = FINISHED
                    noise.setAutoDraw(False)
            if noise.status == STARTED:
                if noise._needBuild:
                    noise.buildNoise()
                else:
                    if (frameN-noise.frameNStart) %             1==0:
                        noise.updateNoise()
            
            # *blob_0* updates
            
            # if blob_0 is starting this frame...
            if blob_0.status == NOT_STARTED and tThisFlip >= 0-frameTolerance:
                # keep track of start time/frame for later
                blob_0.frameNStart = frameN  # exact frame index
                blob_0.tStart = t  # local t and not account for scr refresh
                blob_0.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blob_0, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blob_0.started')
                # update status
                blob_0.status = STARTED
                blob_0.setAutoDraw(True)
            
            # if blob_0 is active this frame...
            if blob_0.status == STARTED:
                # update params
                blob_0.setPos((0,0), log=False)
            
            # if blob_0 is stopping this frame...
            if blob_0.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > blob_0.tStartRefresh + .5-frameTolerance:
                    # keep track of stop time/frame for later
                    blob_0.tStop = t  # not accounting for scr refresh
                    blob_0.tStopRefresh = tThisFlipGlobal  # on global time
                    blob_0.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blob_0.stopped')
                    # update status
                    blob_0.status = FINISHED
                    blob_0.setAutoDraw(False)
            
            # *blob* updates
            
            # if blob is starting this frame...
            if blob.status == NOT_STARTED and tThisFlip >= 0.5-frameTolerance:
                # keep track of start time/frame for later
                blob.frameNStart = frameN  # exact frame index
                blob.tStart = t  # local t and not account for scr refresh
                blob.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(blob, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'blob.started')
                # update status
                blob.status = STARTED
                blob.setAutoDraw(True)
            
            # if blob is active this frame...
            if blob.status == STARTED:
                # update params
                blob.setPos([blob.pos+sig*np.random.normal(size=(2,))], log=False)
            
            # if blob is stopping this frame...
            if blob.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > blob.tStartRefresh + 15.0-frameTolerance:
                    # keep track of stop time/frame for later
                    blob.tStop = t  # not accounting for scr refresh
                    blob.tStopRefresh = tThisFlipGlobal  # on global time
                    blob.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'blob.stopped')
                    # update status
                    blob.status = FINISHED
                    blob.setAutoDraw(False)
            # Run 'Each Frame' code from code
            if response_mouse.status == STARTED:
                x,y = blob.pos
                blob.x.append(x)
                blob.y.append(y)
            
            # *cursor* updates
            
            # if cursor is starting this frame...
            if cursor.status == NOT_STARTED and tThisFlip >= 0.0-frameTolerance:
                # keep track of start time/frame for later
                cursor.frameNStart = frameN  # exact frame index
                cursor.tStart = t  # local t and not account for scr refresh
                cursor.tStartRefresh = tThisFlipGlobal  # on global time
                win.timeOnFlip(cursor, 'tStartRefresh')  # time at next scr refresh
                # add timestamp to datafile
                thisExp.timestampOnFlip(win, 'cursor.started')
                # update status
                cursor.status = STARTED
                cursor.setAutoDraw(True)
            
            # if cursor is active this frame...
            if cursor.status == STARTED:
                # update params
                cursor.setPos([response_mouse.getPos()], log=False)
            
            # if cursor is stopping this frame...
            if cursor.status == STARTED:
                # is it time to stop? (based on global clock, using actual start)
                if tThisFlipGlobal > cursor.tStartRefresh + 15.5-frameTolerance:
                    # keep track of stop time/frame for later
                    cursor.tStop = t  # not accounting for scr refresh
                    cursor.tStopRefresh = tThisFlipGlobal  # on global time
                    cursor.frameNStop = frameN  # exact frame index
                    # add timestamp to datafile
                    thisExp.timestampOnFlip(win, 'cursor.stopped')
                    # update status
                    cursor.status = FINISHED
                    cursor.setAutoDraw(False)
            
            # check for quit (typically the Esc key)
            if defaultKeyboard.getKeys(keyList=["escape"]):
                thisExp.status = FINISHED
            if thisExp.status == FINISHED or endExpNow:
                endExperiment(thisExp, win=win)
                return
            # pause experiment here if requested
            if thisExp.status == PAUSED:
                pauseExperiment(
                    thisExp=thisExp, 
                    win=win, 
                    timers=[routineTimer], 
                    playbackComponents=[]
                )
                # skip the frame we paused on
                continue
            
            # check if all components have finished
            if not continueRoutine:  # a component has requested a forced-end of Routine
                trial.forceEnded = routineForceEnded = True
                break
            continueRoutine = False  # will revert to True if at least one component still running
            for thisComponent in trial.components:
                if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                    continueRoutine = True
                    break  # at least one component has not yet finished
            
            # refresh the screen
            if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
                win.flip()
        
        # --- Ending Routine "trial" ---
        for thisComponent in trial.components:
            if hasattr(thisComponent, "setAutoDraw"):
                thisComponent.setAutoDraw(False)
        # store stop times for trial
        trial.tStop = globalClock.getTime(format='float')
        trial.tStopRefresh = tThisFlipGlobal
        thisExp.addData('trial.stopped', trial.tStop)
        # store data for trials (TrialHandler)
        trials.addData('response_mouse.x', response_mouse.x)
        trials.addData('response_mouse.y', response_mouse.y)
        trials.addData('response_mouse.leftButton', response_mouse.leftButton)
        trials.addData('response_mouse.midButton', response_mouse.midButton)
        trials.addData('response_mouse.rightButton', response_mouse.rightButton)
        trials.addData('response_mouse.time', response_mouse.time)
        # Run 'End Routine' code from code
        trials.addData('blob.x', blob.x)
        trials.addData('blob.y', blob.y)
        # using non-slip timing so subtract the expected duration of this Routine (unless ended on request)
        if trial.maxDurationReached:
            routineTimer.addTime(-trial.maxDuration)
        elif trial.forceEnded:
            routineTimer.reset()
        else:
            routineTimer.addTime(-15.500000)
        thisExp.nextEntry()
        
    # completed 4.0 repeats of 'trials'
    
    if thisSession is not None:
        # if running in a Session with a Liaison client, send data up to now
        thisSession.sendExperimentData()
    
    # mark experiment as finished
    endExperiment(thisExp, win=win)


def saveData(thisExp):
    """
    Save data from this experiment
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    """
    filename = thisExp.dataFileName
    # these shouldn't be strictly necessary (should auto-save)
    thisExp.saveAsWideText(filename + '.csv', delim='auto')
    thisExp.saveAsPickle(filename)


def endExperiment(thisExp, win=None):
    """
    End this experiment, performing final shut down operations.
    
    This function does NOT close the window or end the Python process - use `quit` for this.
    
    Parameters
    ==========
    thisExp : psychopy.data.ExperimentHandler
        Handler object for this experiment, contains the data to save and information about 
        where to save it to.
    win : psychopy.visual.Window
        Window for this experiment.
    """
    if win is not None:
        # remove autodraw from all current components
        win.clearAutoDraw()
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed
        win.flip()
    # return console logger level to WARNING
    logging.console.setLevel(logging.WARNING)
    # mark experiment handler as finished
    thisExp.status = FINISHED
    logging.flush()


def quit(thisExp, win=None, thisSession=None):
    """
    Fully quit, closing the window and ending the Python process.
    
    Parameters
    ==========
    win : psychopy.visual.Window
        Window to close.
    thisSession : psychopy.session.Session or None
        Handle of the Session object this experiment is being run from, if any.
    """
    thisExp.abort()  # or data files will save again on exit
    # make sure everything is closed down
    if win is not None:
        # Flip one final time so any remaining win.callOnFlip() 
        # and win.timeOnFlip() tasks get executed before quitting
        win.flip()
        win.close()
    logging.flush()
    if thisSession is not None:
        thisSession.stop()
    # terminate Python process
    core.quit()


# if running this experiment as a script...
if __name__ == '__main__':
    # call all functions in order
    expInfo = showExpInfoDlg(expInfo=expInfo)
    thisExp = setupData(expInfo=expInfo)
    logFile = setupLogging(filename=thisExp.dataFileName)
    win = setupWindow(expInfo=expInfo)
    setupDevices(expInfo=expInfo, thisExp=thisExp, win=win)
    run(
        expInfo=expInfo, 
        thisExp=thisExp, 
        win=win,
        globalClock='float'
    )
    saveData(thisExp=thisExp)
    quit(thisExp=thisExp, win=win)
