# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['expflow']

package_data = \
{'': ['*']}

install_requires = \
['dataclasses_json>=0.5.7,<0.6.0',
 'localnow>=0.1.0,<0.2.0',
 'logmixin>=0.1.4,<0.2.0']

setup_kwargs = {
    'name': 'expflow',
    'version': '0.2.0',
    'description': 'A Python library for controlling the flow of psychological experiments.',
    'long_description': '# Expflow\n  \n## Description  \n  \nExpflow is a Python library that controls the flow and handles the data of psychological experiments. While it isn\'t a \nfull-fledged experiment builder like [PsychoPy](https://www.psychopy.org), it may be used with other tools to create \nrobust experiments with minimal coding.\n  \n## Installation  \n  \nExpflow is available on PyPI and can be installed in the typical way with `pip`:  \n  \n```bash  \npip install expflow\n```  \n  \n## Tutorial  \n  \n### Overview  \n\nExpflow has strong opinions about how psychological experiments should be structered and coded, and performs extensive \nautomatic bookkeeping and numerous validation checks under the hood to ensure that the user\'s code is consistent with \nthese opinions.\n\nExpflow defines an experiment as a sequence of trials presented to a participant. Typically, trials are identical except\nfor a small number of critical details, such as the stimulus. The participant makes a response on each trial, after \nwhich the trial ends. The next trial begins after the previous one. After the last trial, the experiment is finished.\n\n### Logging  \n  \nExpflow makes extensive use of the [logging](https://docs.python.org/3/library/logging.html) module. The first few times\nyou use expflow, I recommend setting up basic logging at the most verbose level at beginning of your experiment script, \nwhich will allow you to see exactly what expflow does. If blazing fast performance is not a major concern — which \ntypically it isn\'t, because psychological experiment are often simple things and modern computers are powerful — you \ncould leave verbose logging switched on all the time (that\'s what I do). \n  \n```python  \nimport logging  \n  \nlogging.basicConfig(level=logging.DEBUG)  \nlogging.debug("Hello, world!")  \n```  \n\nThe rest of this tutorial will now print many log message to the console.\n\n### Importing expflow\n\nImport expflow as follows.\n  \n```python  \nimport expflow  \n```  \n  \n### Directories\n\n#### Temporary directory\n  \nSee the bit about creating a temporary directory in the log output?\n\nExpflow needs somewhere to store data right away, and the default behaviour is to use a temporary directory. This is \nsuitable for testing, but a bad idea for real work, because the data you generate will be lost when the program ends. \nExpflow will bug you with warnings if you don\'t set a permanent data directory. For example, try this:\n\n```python\nexpflow.get_expflow_dir()  # produces a warning\n```\n\n#### Permanent directory\n\nTo set a permanent directory, use the `set_expflow_dir` function. You can pass any valid writable path to a directory. A\ngood choice is a dedicated subdirectory of your home directory. For convenience, expflow provides this as a constant \ncalled `expflow.USER_DIR`. \n  \n```python  \nexpflow.set_expflow_dir(expflow.USER_DIR)  # set a dir\nexpflow.get_expflow_dir()  # prints something like `/Users/username/Expflow`\n```  \n\n#### Subdirectories\n\nThe function `set_expflow_dir` creates several subdirectories if they don\'t already exist. These are used to store \ndifferent types of data. Currently, participant data are stored in the `participants` subdirectory and experiment data \nare stored in the `experiment` subdirectory. The others will be used by future versions of expflow.\n\n### Cleaning up\n  \nBefore we go on, let\'s take a moment delete some files that may exist in your user directory if you ran this tutorial\npreviously. \n  \n```python  \nfor i in range(1, 10):  \n    (expflow.USER_DIR / "Participants" / f"example_p{i}.json").unlink(True)  \n    (expflow.USER_DIR / "Experiments" / f"example_p{i}.example_e1.json").unlink(True) \n```  \n  \n### Participants \n\n#### Creating participants\n  \nA participant is a person who takes part in an experiment. In expflow, a participant is represented by a `Participant` \nobject. You should create an instance of this class for each participant in an experiment.\n\n```python  \np = expflow.Participant("example_p1")  # creates a new participant\n```\n\nParticipant objects are [dataclasses](https://docs.python.org/3/library/dataclasses.html). The single required argument\nbecomes a field called `participant_id`, which must be a unique string for each participant. Other optional fields you \ncan set are:\n\n- `dob`: Date of birth. Should be a `date` object.\n- `age`: Age. Should be an `int` or `float`. Doesn\'t make sense to use this if `dob` is specified.\n- `gender`: Participant gender.\n- `language`: Participant language.\n-  `comments`: Any comments about the participant.\n-  `group`: Participant group.\n\nThere are other fields as well. You can see them all like so:\n  \n```python  \nimport dataclasses  \n  \nfor field in dataclasses.fields(p):  \n    logging.info(f"{field.name}: {getattr(p, field.name)}")  \n```  \n\nHowever, **don\'t go changing the values of the other fields willy-nilly!** Expflow manages them  \nautomatically and uses them for bookkeeping. Generally, I recommend setting participant fields at object instantiation \nand, except perhaps for the `comments` field, never changing them.\n\n#### Saving and loading\n  \nWhen we created our participant object, it automatically saved a [JSON](https://www.json.org/json-en.html) \nrepresentation of itself to a file in the `participants` subdirectory, whose path is given by the `path` field. This \nwill always happen every time we create a participant object and there is no way to stop it, by design. A participant \nobject will also save itself before garbage collection.\n  \n```python  \ndel p  # delete the participant \n```\n\nThis "autosaving" feature allows expflow to enforce ***Golden Rule #1: A given participant can\'t be created twice***. An\nexception will be raised if you try to create a new participant with the same `participant_id` as an existing \nparticipant, even if the older participant was not created during the current Python session.\n\n```python\ntry:\n    p = expflow.Participant("example_p1")  # even though we deleted `p`!\n    raise RuntimeError("You won\'t see this message")\n\nexcept expflow.ParticipantExistsError as er:\n    logging.error(er)\n```\n\nSometimes you may need to load a participant, for example to add something to their `comments` field. You can do so \nusing the `load` class method, which requires the `participant_id`.\n\n```python\np = expflow.Participant.load("example_p1")\np.comments += "- Here\'s a comment\\n"\np.comments += "- Here\'s another\\n"\ndel p  # autosave on deletion\n```\n\nYou can overtly save the participant with the `save` method, but you shouldn\'t need to. If you want to quickly get at \nthe participant data for testing or debugging purposes, you can use the `to_dict` and `to_json` methods. But otherwise,\nparticipant objects will save on garbage collection.\n\n#### Compression\n\nBy default, JSON representations of participants are uncompressed, but you can use [gzip](https://www.gzip.org) \ncompression instead by setting the optional field `compression` to `True` when creating a new participant or setting the\nglobal variable `expflow.using_compression` to `True` to turn on compresson by default. Compressed files usually much \nsmaller, but not human readable, and have the extension `.json.gz` instead of `.json`.\n\n### Experiments and trials\n\n#### Creating experiments\n\nExperiments are represented by the `Experiment` dataclass. You must create an instance of this class each time a new \nparticipant is about to run an experiment. Experiment objects have two required fields: `participant_id` and  \n`experiment_id`. \n\n```python\ne = expflow.Experiment("example_p1", "example_e1")\n```\n\nThe *combination* of these identifiers must be unique. In other words, a single participant can perform multiple \ndifferent experiments, and multiple different participants can perform the same experiment, but  ***Golden Rule #2: A \ngiven participant can\'t perform a given experiment twice.***. You can load an experiment object with an existing \ncombination of identifiers.\n\n```python\ndel e  \ntry:  \n    e = expflow.Experiment("example_p1", "example_e1")  \n    raise RuntimeError("You won\'t see this message")  \nexcept expflow.ExperimentExistsError as er:  \n    logging.error(er)  \ne = expflow.Experiment.load("example_p1", "example_e1")\n```\n\nUnder the hood, this is enforced by saving on creation and garbage collection.\n\nYou also can\'t create an experiment if the participant doesn\'t exist.\n\n```python  \ntry:  \n    _ = expflow.Experiment("example_p2", "example_e1")  \n    raise RuntimeError("You won\'t see this message")  \nexcept expflow.ParticipantDoesNotExistError as er:  \n    logging.error(er)\n```\n\nFinally, experiments have an optional user-specified field called `trials`, which is discussed in the next section. You \ncan set this on instantiation or later via special methods.\n\n#### Creating trials\n\nExperiments contain trials. Trials are represented by instance of the `Trial` dataclass, but unlike participant and \nexperiment dataclasses, they can\'t be saved or loaded individually (maybe in a future version). Expflow doesn\'t insist \non trials having unique identifiers or on required fields, either.\n\nThere are a number of optional fields:\n\n- `stimulus`\n- `response` \n- `trial_number`\n- `block_number`\n- `condition` \n- `practice`\n\nIt should be obvious what each of these is supposed to represent.\n\nLet\'s create a list of trials.\n\n```python  \ntrials = [expflow.Trial(trial_number=i) for i in range(3)]  \n```  \n\n#### Appending trials to an experiment\n  \nInside an experiment object, trials are stored in field called `trials`, which is a list of `Trial` objects. The \nexperiment we created currently has an empty `trials` field.  \n  \n```python  \nassert len(e.trials) == 0  \n```  \n  \nThis is a good time to bring up ***Golden Rule #3: Run experiments by iterating experiment objects***. Accordingly, `e` \nis iterable and its `__len__` method returns the number of trials it contains.  \n  \n```python  \nassert len(e) == 0  \n```  \n  \nWe can append the trials we created to the experiment using the `append_trials` method.  \n  \n```python  \ne.append_trials(trials)  \n```  \n\nYou can append to or otherwise directly modify `e.trials` **but please don\'t**, because the `append_trials` method does \nextra things like checks you are actually appending `Trial` instances and saves the experiment object.\n\nAfter appending, the experiment has three trials.  \n  \n```python  \nassert len(e) == 3  \n```  \n  \nExperiments save themselves after a trial is appended, so if we delete the experiment and reload it, we will see that \nthe appended trials are there.  \n  \n```python  \ndel e  \ne = expflow.Experiment.load("example_p1", "example_e1")\nassert len(e) == 3  \n```  \n  \n#### Other manipulations to the trial list\n\nCurrently, there are only `append_trials`, `append_trial`, and `insert_trial` methods, but more may be added in future \nversions of expflow.\n\n###  Experiment flow\n\nThis section will describe the core features that allows expflow to control experiment flow. First, it is important to \nknow about two variables inside experiment objects: the trial index and the status.\n\n#### Trial index\n\nExperiments have a field called `trial_index`, which is automatically managed. Its value is `None` on instantiation, and\nbecomes an integer when the experiment runs. Predictably, this is used to index the experiment\'s current position in \nthe trial list. User\'s shouldn\'t set this field themselves.\n\n#### Statuses\n  \nExperiments (and trials) have a special `status` property (mirrored by the `current_status` field). Users shouldn\'t set\nthis property or its field themselves, but they can read it or test its value with `is_*` boolean properties. \n\nThere are only six possible statuses and only certain status transitions are possible. The possible statuses, their \nmeanings, and acceptable transitions are given in the table below.\n\n| Status        | Description                          | Acceptable transitions      |\n|---------------| ------------------------------------ |-----------------------------|\n| `"pending"`   | Trial is scheduled to run later      | running, skipped            |\n| `"running"`   | Trial is running right now           | finished, timed_out, paused |\n| `"paused"`    | Trial is temporarily paused          | running                     |\n| `"timed_out"` | Trial went on too long and has ended | -                           |\n| `"finished"`  | Trial ended as expected              | -                           |\n| `"skipped"`   | Trial will not run                   | -                           |\n\nThis is designed to conisistent with the common usage of the words. On instantiation, the status of an experiment is \nalways `"pending"`. This is natural, because experiments are created before they are run. Pending experiments can be \nchanged to `"running"` or `"skipped"`. Running experiments can be changed to `"finished"` if they were completed normally, `"paused"` if they were paused, or `"timed_out"` if they were timed out. Paused experiments must be unpaused (i.e., set back to `"running"`) before they can be `"finished"`. `"finished"`, `"timed_out"`, and `"skipped"` are terminal statuses. Hopefully this all makes intuitive sense.\n\nIndividual trials have a status property that behaves in exactly the same way.\n\nAs we shall see, experiment and trial statuses are managed automatically as we run an experiment. In fact, this is the\nmajor trick expflow employs to ensure proper flow.\n  \n#### Running experiments  \n  \nAs per Golden Rule #3, to run an experiment, you iterate over the experiment object, such as in a  `for` loop.\n  \n```python  \ndef show_stimulus(stimulus):\n\t"""Replace this with something that presents stimuli."""\n    pass  \n  \ndef get_response(): \n\t"""Replace this with something that collects responses."""\n    return "response"  \n  \nfor trial in e:\n\n\t# do experimental stuff here, for example ...\n\tshow_stimulus(trial.stimulus)  \n    trial.response = get_response()\n    # ... end of experimental stuff\n    \n    if not e.is_running:\n\t    break  \n```  \n  \nThis is *almost* a completely normal Python `for` loop. I say almost because it contains an `if` statement that will \nprematurely break the loop if the experiment status is no longer set to `"running"`. This is necessary to catch pauses,\nskips, and time outs (discussed later).\n\nIf your experiment is embedded within a larger program and it is not convenient or possible to use the `for` syntax, \nyou could use `next(e)` instead, but just remember to catch the `StopIteration` exception.\n\n#### Saving data\n\nNotice that in our toy experiment above, the `response` field of the current trial was set to the participant\'s response\non that trial. How do we make sure those responses are recorded?\n\nEach `trial` in the loop was a reference to the experiment\'s current trial (also available via `self.current_trial`). \nTherefore, because we set `trial.response` to `"response"`, participant responses are available after iteration (i.e., \nafter the experiment has finished).\n\n```python\nfor trial in e.trials:  # remember Golden Rule #3  \n    assert trial.response == "response"\n```\n\nFurthermore, experiments save themselves after each iteration and status change, so we have also *serialised* the data \nas well. Let\'s delete the experiment object and reload it. \n  \n```python  \ndel e  \ne = expflow.Experiment.load("example_p1", "example_e1")  \nfor trial in e.trials: # Golden Rule #3 \n    assert trial.response == "response"\n```  \n\nThe responses were recorded! This is important — it means that expflow automatically stores data across Python sessions\nwith no extra effort on the part of the user.\n\n#### Pausing\n\nSuppose an experiment is too long to be completed all in one session: we need to pause it and resume it later. The \nfollowing code simulates a pause halfway through an experiment.\n\n```python\np2 = expflow.Participant("example_p2")\ntrials = [expflow.Trial(trial_number=i) for i in range(10)]\ne3 = expflow.Experiment("example_p2", "example_e1", trials=trials)\n\nfor trial in e:\n\n\tif e.trial_index > 5:\n\t\n\t\tshow_stimulus(trial.stimulus)  \n\t    trial.response = get_response()\n\n\telse:\n\t\te.pause()\n    \n    if not e.is_running:\n\t    break  \n\nassert e.is_paused\nassert e.current_trial.is_paused\n```\n\nYou can resume a paused experiment by iterating over it again.\n\n```python\nfor trial in e:\n\n\tassert e.trial_index > 5\n\t\n\tshow_stimulus(trial.stimulus)  \n\ttrial.response = get_response()\n    \n    if not e.is_running:\n\t    break\n```\n\n#### Timing out\n\nIndividual trials or entire experiments may have time limits. If so, you can use the `trial.time_out` and \n`experiment.time_out` methods to time out a trial or experiment, respectively. Timed out trials and experiments cannot \nbe resumed (unlike paused trials).\n\n#### Skipping\n\nSometimes an experiment may skip upcoming trials, or an experiment may be skipped enitrely (if it is part of a batch of\nexperiments, for example). You can use the `trial.skip` and `experiment.skip` methods to achieve this. You can\'t skip a\ntrial or experiment that was already started, nor can you ever\nstart a skipped trial or experiment.\n\nExperiments don\'t always present every trial to every participant. Sometimes an experiment may have a stopping rule, \nwhere some or all remaining trials are skipped due to poor performance, or trial-specific or whole-experiment time \nlimits. The statuses `"skipped"` and `"timed_out"` — and their respecitve methods, `skip` and `timeout` (or `time_out`) — exist to deal with these circumstances. You can skip or time out individual trials or entire experiments. Skipped or timed out experiments/trials cannot be rerun afterwards under any circumstances.\n\n#### Duration\n\nExperiments and trials have a  `duration` field that is calculated when the experiment/trial is finished or timed out. \nIt represents the total time taken to complete the experiment/trial, minus any time spent in a paused state, in seconds.\n\n#### Crash recovery\n\nExpflow has a rudimentary crash-recovery feature. It doesn\'t work all the time, but it could save your bacon once in a\nwhile.\n\nConsider this example:\n\n```python\np3 = expflow.Participant("example_p3")\ntrials = [expflow.Trial(trial_number=i) for i in range(3)]\ne2 = expflow.Experiment("example_p3", "example_e1", trials=trials)  \n\nfor trial in e3:  \n    \n    show_stimulus(trial.stimulus)  \n    trial.response = get_response()  \n    \n    break  # <- crash!  \n\ndel e3  # <- crash!  \n\ne3 = expflow.Experiment.load("example_p3", "example_e1")  \nassert e3.is_paused  \nassert e3.current_trial.is_paused\n```\n\nHere, we have simulated a computer crash by breaking the trial loop and deleting our experiment object, which is \napproximately what would happen if you encountered an unexpected exception during your experiment. On garbage \ncollection, an experiment object will change its status from running to \npaused if necessary, and save itself. Therefore, when this experiment is loaded again, it behaves as if it were paused \nat the point of garbage collection.',
    'author': 'Sam Mathias',
    'author_email': 'None',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'https://github.com/sammosummo/expflow',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
