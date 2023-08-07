# -*- coding: utf-8 -*-
"""
@author: ftong
"""
import numpy as np
import bisect #used for bisecting list of events by start time
from tdasha.window import Window
import sys

try:    #make dask optional
    from dask import delayed
    import dask
    from dask.diagnostics import ProgressBar # use Dask progress bar
except:
    dask = lambda x: x
    
try:    #make tqdm optional
    from tqdm import tqdm
except:
    tqdm = lambda x: x
    
def time_window_length(t_input, time_unit='day'):
        
    t = assure_order(t_input, chrono='forward')
    
    n_events = len(t) # number of events in the catalog
    t_start = t[0] # time of first event, assumes event list sorted by time
    t_end = t[-1] # time of last event
    time_span= t_end-t_start #length of data set between first and last event
    
    if time_unit == 'day':
        time_span = time_span / 86400 #convert time span from seconds to days
    elif time_unit == 'hour':
        time_span = time_span / 3600 #convert time span from seconds to hours
    elif time_unit == 'minute':
        time_span = time_span / 60 #convert time span from seconds to minutes

    activity_rate = n_events / time_span
    
    window_length = np.ceil(80 / activity_rate) # use window length such that there are 80 events per window
    
    return window_length,activity_rate

def assure_order(t, chrono, x=[None]):
    
    # t is a list of time values, x must be a numpy array
    
    # check ordering of time based on first two events and reverses it if necessary
    if chrono=="forward" and t[1]<t[0] or chrono=="backward" and t[1]>t[0]:
        t_new = list(reversed(t))
        
        if len(x)>1: # x provided, so reverse also x then return both t and x
            x_new = np.flip(x)
            return t_new, x_new
        
        else: # x is empty, return only t
            return t_new

    
    else: # ordering is already as desired based on test
    
        if len(x)>1: # x provided, so return both t and x
            return t, x
        
        else: # x is empty, return only t
            return t
        
def parse_time(t, t_unit, t_step_raw, win_size_raw=False):

    t_start = t[0]
    t_end = t[-1]

    # convert step and window size to seconds
    if t_unit == 'day':
        t_step = t_step_raw*86400
        win_size = win_size_raw*86400 
    elif t_unit == 'hour':
        t_step = t_step_raw*3600
        win_size = win_size_raw*3600 
    elif t_unit == 'minute':
        t_step = t_step_raw*60
        win_size = win_size_raw*60
    
    if not win_size_raw: 
        return t_start, t_end, t_step #CNE windows
    else:
        return t_start, t_end, t_step, win_size #CTL windows

# def comp_exc_prob_CNE(M_input, Mc, rum, t_input, t_unit, t_step_raw, t_period, win_size, M_max=None, verbose=False, ci = False, parallel = True, **kwargs):

#     t, M = assure_order(t_input, chrono='backward', x=M_input)
    
#     t_start, t_end, t_step = parse_time(t, t_unit, t_step_raw)
    
#     windows = np.arange(t_start,t_end,-t_step)
#     exc_pr = [] # exceedance probability for each window
#     exc_pr_ci = [] # confidence interval for exc_pr
#     tc = [] # timestamp of end of each window

#     # Iterate through all the windows, select desired number of events and compute exceedance probability
#     nwin = len(windows)

#     if parallel:
#         print("Processing windows in parallel using Dask")
#         pbar = ProgressBar()
#         pbar.register()
#         iter = windows
#     else:
#         print("Processing windows")
#         iter = tqdm(windows) # use tqdm progress bar
        
#     for idx, tt in enumerate(iter): # tt is the end time of each window
#         j = len(t) - bisect.bisect_right(t[::-1], tt)

#         # fetch the next win_size number of events after event t[j], event times and their magnitudes
#         T_sel = t[j:j+win_size] # event times for window
#         M_sel = M[j:j+win_size] # event magnitudes for window
        
#         if len(T_sel) < win_size:
#             print("Not enough events left to fill window starting at", tt)
#             break
        
#         tc.append(tt)
        
#         if parallel: #run in parallel using dask
#             win = delayed(Window)(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
#             # exc_pr.append(delayed(win.exc_prob)()) 
#             exc_pr.append(win.exc_prob())
            
#             if ci: # estimate confidence interval
#                 exc_pr_ci.append(delayed(win.exc_prob_ci)(**kwargs))

#         else: #run without parallel computing
#             win = Window(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
#             exc_pr.append(win.exc_prob())
            
#             if ci: # estimate confidence interval
#                 exc_pr_ci.append(win.exc_prob_ci(**kwargs))
                
#             if verbose==True:
#                 print("\nWindow", idx+1, "of", nwin)
#                 print("\tbandwidth:", round(win.h,3))
#                 print("\texceedance probability:", round(100*exc_pr[idx],2), "%")

#                 # print(exc_pr[idx])
#                 if ci==True:
#                     print("\tconfidence interval:", round(100*exc_pr_ci[idx][0],2), "to", round(100*exc_pr_ci[idx][1],2), "%")

    
#     if parallel:
#         exc_pr = dask.compute(*exc_pr, scheduler='processes')
#         exc_pr_ci = dask.compute(*exc_pr_ci, scheduler='processes')
#         # exc_pr = dask.compute(*exc_pr)
#         exc_pr = exc_pr[::-1] #because reverse is not working when using tuples with dask    
#         exc_pr_ci = exc_pr_ci[::-1]    
#     else: #reverse operation is faster than slicing
#         exc_pr.reverse()
#         exc_pr_ci.reverse()

#     tc.reverse()
    
#     print("Exceedance Probability computed from", tc[0], "to", tc[-1])
    
#     return exc_pr, exc_pr_ci, tc

def comp_exc_prob(M_input, Mc, rum, t_input, t_unit, t_step_raw, t_period, win_size_raw, win_method, M_max=None, verbose = False, ci = False, parallel = True, **kwargs):
    t, M = assure_order(t_input, chrono='backward', x=M_input)
    
    if win_method == 'CNE':
        t_start, t_end, t_step = parse_time(t, t_unit, t_step_raw)
        win_size = win_size_raw
    elif win_method == 'CTL':
        t_start, t_end, t_step, win_size = parse_time(t, t_unit, t_step_raw, win_size_raw)
    else:
        print("Abort! Please select either CNE or CTL method for windowing...")
        sys.exit()

    windows = np.arange(t_start,t_end,-t_step)
    exc_pr = [] # exceedance probability for each window
    exc_pr_ci = [] # confidence interval for exc_pr
    tc = [] # timestamp of end of each window
    nwin = len(windows)
    
    if parallel:
        print("Processing windows in parallel using Dask")
        pbar = ProgressBar()
        pbar.register()
        iter = windows
    else:
        print("Processing windows")
        iter = tqdm(windows) # use tqdm progress bar

    # Iterate through all the windows, select desired number of events and compute exceedance probability
    for idx, tt in enumerate(iter): # tt is the end time of each window

        if win_method == 'CNE':
            j = len(t) - bisect.bisect_right(t[::-1], tt)
    
            # fetch the next win_size number of events after event t[j], event times and their magnitudes
            T_sel = t[j:j+win_size] # event times for window
            M_sel = M[j:j+win_size] # event magnitudes for window
            
            if len(T_sel) < win_size:
                print("Not enough events left to fill window starting at", tt)
                break

        elif win_method == 'CTL':
            j1 = len(t) - bisect.bisect_right(t[::-1], tt)
            j2 = len(t) - bisect.bisect_right(t[::-1], tt-win_size)
            
            # fetch all events within the time window
            T_sel = t[j1:j2] # event times
            M_sel = M[j1:j2] # event magnitudes
            
            num_events = len(T_sel)
    
            if num_events<50:
                # print("Insufficient events at time window", tt)
                exc_pr.append(float("NaN")) # insufficient events, set to null
                exc_pr_ci.append([float("NaN"),float("NaN")]) # insufficient events, set to null
                tc.append(tt)
                continue            # move on to next window

        tc.append(tt)

        if parallel: #run in parallel using dask
            win = delayed(Window)(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
            # exc_pr.append(delayed(win.exc_prob)()) 
            exc_pr.append(win.exc_prob())
            
            if ci: # estimate confidence interval
                exc_pr_ci.append(delayed(win.exc_prob_ci)(**kwargs))

        else: #run without parallel computing
            win = Window(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
            exc_pr.append(win.exc_prob())
            
            if ci: # estimate confidence interval
                exc_pr_ci.append(win.exc_prob_ci(**kwargs))
                
            if verbose==True:
                print("\nWindow", idx+1, "of", nwin)
                print("\tbandwidth:", round(win.h,3))
                print("\texceedance probability:", round(100*exc_pr[idx],2), "%")

                # print(exc_pr[idx])
                if ci==True:
                    print("\tconfidence interval:", round(100*exc_pr_ci[idx][0],2), "to", round(100*exc_pr_ci[idx][1],2), "%")


    if parallel:
        exc_pr = dask.compute(*exc_pr, scheduler='processes')
        exc_pr_ci = dask.compute(*exc_pr_ci, scheduler='processes')
        # exc_pr = dask.compute(*exc_pr)
        exc_pr = exc_pr[::-1] #because reverse is not working when using tuples with dask    
        exc_pr_ci = exc_pr_ci[::-1]    
    else: #reverse operation is faster than slicing
        exc_pr.reverse()
        exc_pr_ci.reverse()

    tc.reverse()
    
    print("Exceedance Probability computed from", tc[0], "to", tc[-1])
    
    return exc_pr, exc_pr_ci, tc



# def comp_exc_prob_CTL(M_input, Mc, rum, t_input, t_unit, t_step_raw, t_period, win_size_raw, M_max=None, verbose = False, ci = False, parallel = True, **kwargs):
        
#     t, M = assure_order(t_input, chrono='backward', x=M_input)
    
#     t_start, t_end, t_step, win_size = parse_time(t, t_unit, t_step_raw, win_size_raw)
    
#     windows = np.arange(t_start,t_end,-t_step)
#     exc_pr = [] # exceedance probability for each window
#     exc_pr_ci = [] # confidence interval for exc_pr
#     tc = [] # timestamp of end of each window
        
#     # Iterate through all the windows, select desired number of events and compute exceedance probability
    
#     nwin = len(windows)

#     if parallel:
#         print("Processing windows in parallel using Dask")
#         pbar = ProgressBar()
#         pbar.register()
#         iter = windows
#     else:
#         print("Processing windows")
#         iter = tqdm(windows) # use tqdm progress bar

#     for idx, tt in enumerate(iter): # tt is the end time of each window
#         j1 = len(t) - bisect.bisect_right(t[::-1], tt)
#         j2 = len(t) - bisect.bisect_right(t[::-1], tt-win_size)
        
#         # fetch all events within the time window
#         T_sel = t[j1:j2] # event times
#         M_sel = M[j1:j2] # event magnitudes
        
#         num_events = len(T_sel)

#         if num_events<50:
#             # print("Insufficient events at time window", tt)
#             exc_pr.append(float("NaN")) # insufficient events, set to null
#             exc_pr_ci.append([float("NaN"),float("NaN")]) # insufficient events, set to null
#             tc.append(tt)
#             continue            # move on to next window
        

#         if parallel: #run in parallel using dask
#             win = delayed(Window)(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
#             # exc_pr.append(delayed(win.exc_prob)())
#             exc_pr.append(win.exc_prob())
            
#             if ci: # estimate confidence interval
#                 exc_pr_ci.append(delayed(win.exc_prob_ci)(**kwargs))
        
#         else: #run without parallel computing

#             win = Window(Mc, rum, M_sel, T_sel, t_unit, t_step, t_period, **kwargs)
#             exc_pr.append(win.exc_prob())
        
#             if ci: # estimate confidence interval
#                 exc_pr_ci.append(win.exc_prob_ci(**kwargs))
                
#             if verbose==True:
#                 print("\nWindow", idx+1, "of", nwin)
#                 print("\tbandwidth:", round(win.h,3))
#                 print("\texceedance probability:", round(100*exc_pr[idx],2), "%")

#                 # print(exc_pr[idx])
#                 if ci==True:
#                     print("\tconfidence interval:", round(100*exc_pr_ci[idx][0],2), "to", round(100*exc_pr_ci[idx][1],2), "%")
        
#         tc.append(tt)
        
        

#         # break
    
#     if parallel:
#         exc_pr = dask.compute(*exc_pr, scheduler='processes')
#         exc_pr_ci = dask.compute(*exc_pr_ci, scheduler='processes')
#         # exc_pr = dask.compute(*exc_pr)
#         exc_pr = exc_pr[::-1] #because reverse is not working when using tuples with dask    
#         exc_pr_ci = exc_pr_ci[::-1]    
#     else: #reverse operation is faster than slicing
#         exc_pr.reverse()
#         exc_pr_ci.reverse()
    
#     tc.reverse()
    
#     print("Exceedance Probability computed from", tc[0], "to", tc[-1])
    
#     return exc_pr, exc_pr_ci, tc





