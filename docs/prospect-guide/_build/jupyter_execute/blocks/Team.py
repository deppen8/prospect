# Team

A `Team` represents the individuals who will conduct the survey. This building block does not require any spatial information, so defining it can be somewhat more straightforward than the other building blocks.

Each `Team` object is made up of `Surveyor` objects. A `Surveyor` object is meant to define the characteristics for a single person (or an archetype of a hypothetical group of surveyors).

Below we will create six surveyors to make up our `Team`, varying the parameters for each. It is best to simply create each person by hand.

```{tip}
In some cases, it may be more appropriate to use a single archetypal surveyor than to create multiple versions of the same kind of surveyor. For example, in the case where the `Surveyor` parameters are highly uncertain or highly variable, it might be most sensible to begin by creating a single `Surveyor` with wide distributions for the parameters rather than trying to create many surveyors whose parameters differ only slightly.
```

## Create a `Surveyor`

`Surveyor` objects can be created directly.

import prospect

A simple surveyor with the default parameters would look something like this:

simple_surveyor = prospect.Surveyor(
    name="default_surveyor", 
    team_name="demo_team", 
    surveyor_type="default",
    skill=1.0,
    speed_penalty=0.0
)

simple_surveyor.__dict__

## The `surveyor_type` parameter

The `surveyor_type` parameter is merely a convenience included to facilitate grouping surveyors together in the analysis phase. It does not impact anything during the execution of the survey. You could group individuals with whatever schema you decide. 

Below, we use expertise to group individuals so that in the analysis, for example, you could compare results from Experts vs. Novices. Other projects might find it more useful to group people according to Team A vs. Team B vs. Team C. Because it is a `str` parameter, anything goes, really.

## The `skill` parameter

A surveyor's `skill` represents how well they are able to identify `Feature` objects that they encounter. In other words, what is the likelihood that they would recognize and record a `Feature` if all the other discovery parameters were 1.0: the `Feature` (e.g., an artifact) is within their `SurveyUnit`, visibility is perfect, and the `Feature` has an ideal observation rate (`ideal_obs_rate`) of 1.0?

While it might be hard to "guestimate", this parameter could be derived from some controlled experiments with a bit more ease than some other of the discovery parameters. For example, if a surveyor is given twenty objects of which ten are artifacts, how many of the ten are correctly identified as artifacts? (In this case, the researcher may or may not want to count false positives negative results.)

```{tip}
`skill` is another good candidate for the beta distribution (like the `ideal_obs_rate`) where the distribution is defined by the successes ($\alpha$) and failures ($\beta$).
```

Let's define three novice surveyors who each have completed the hypothetical exercise above where they were asked to identify which 10 of 20 objects were artifacts. Their `skill` level is defined by how many of the 10 objects they picked were actually artifacts ($\alpha$) and how many were not ($\beta$).

novice1 = prospect.Surveyor(
    name='novice1', 
    team_name='demo_team', 
    surveyor_type='novice_person', 
    skill=prospect.utils.beta(5, 5), 
    speed_penalty=0.2
)
novice2 = prospect.Surveyor(
    name='novice2', 
    team_name='demo_team', 
    surveyor_type='novice_person', 
    skill=prospect.utils.beta(6, 4), 
    speed_penalty=0.2
)
novice3 = prospect.Surveyor(
    name='novice3', 
    team_name='demo_team', 
    surveyor_type='novice_person', 
    skill=prospect.utils.beta(7, 3),
    speed_penalty=0.2
)

## The `speed_penalty` parameter

`speed_penalty` is a factor that adds time to the survey based on an individual's survey style. Recall that total search time for any given `SurveyUnit` is calculated in the following way:

$$\text{base penalty} = \text{base search time} + \sum \text{artifact time penalties}$$

$$\text{surveyor penalty} = \text{base penalty} \times \text{surveyor speed penalty factor}$$

$$\text{search time} = \text{base penalty} + \text{surveyor penalty}$$

Therefore, one can think of `speed_penalty` as adding some factor to both the base search time (derived from `min_time_per_unit`) and the sum of all the artifact `time_penalty` values. Let's consider a hypothetical example.

Given a radial survey unit where the `min_time_per_unit` is 120 seconds, the sum of all artifact `time_penalty` values is 300 seconds and the surveyor's `speed_penalty` is 0.5, then the time calculation would look as follows:

$$\text{base penalty} = 120 + 300 = 420$$

$$\text{surveyor penalty} = 420 \times 0.5 = 210$$

$$\text{search time} = 420 + 210 = 630$$

```{admonition} Assumptions
:class: caution
An assumption here is that whatever causes the `speed_penalty` will be in effect during general survey time (the `min_time_per_unit` portion) as well as during artifact identification/recording (the artifact `time_penalty` portion). This assumption may not hold well in all cases. For example, if a surveyor is very quick to survey their unit but very slow to record artifacts, then this factor might need to be a compromise between the two deviations.
```

```{tip}
A truncated normal distribution (truncated at 0.0 or above) is a good choice to model this parameter, but any distribution that is bounded by 0.0 would be suitable. This parameter can theoretically take on any value, but practically speaking, it is probably best to stick to positive values. A negative value would have the effect of reducing the base search time, but when determining the `min_time_per_unit` parameter, it is recommended that you assume a surveyor would have `speed_penalty` of 0.0. For this reason, negative values are strongly discouraged.
```

Let's add an expert and two mid-level surveyors to our demo team.

expert = prospect.Surveyor(
    name='expert', 
    team_name='demo_team', 
    surveyor_type='expert_person', 
    skill=1.0, 
    speed_penalty=0.0
)
mid1 = prospect.Surveyor(
    name='mid1', 
    team_name='demo_team', 
    surveyor_type='mid_level_person', 
    skill=0.75, 
    speed_penalty=prospect.utils.truncnorm(mean=0.1, sd=1, lower=0, upper=200)
)
mid2 = prospect.Surveyor(
    name='mid2',
    team_name='demo_team', 
    surveyor_type='mid_level_person', 
    skill=0.75, 
    speed_penalty=prospect.utils.truncnorm(mean=0.1, sd=1, lower=0, upper=200)
)

## Create `Team` from `Surveyor` objects

Above we created six `Surveyor` objects: three novices, an expert, and two mid-level surveyors. To create a `Team`, we can pass those `Surveyor` objects in as a list.

```{note}
The `assignment` parameter is meant to determine how individuals in the team are assigned to survey units during the survey. Currently, only `"naive"` assignment is supported. In this mode, the people in the team are cycled through and assigned to the next `SurveyUnit` until all `SurveyUnit` objects have a `Surveyor` attached. In the future, I hope to support some ways to optimize and randomize this assignment.
```

team_list = [novice1, novice2, novice3, expert, mid1, mid2]
demo_team = prospect.Team(
    name='demo_team', 
    surveyor_list=team_list,
    assignment='naive'
)

Let's inspect the team we just created.

demo_team.df

## Adding and removing `Surveyor` objects later

After we create the `Team` object, if we decide we'd like to add another surveyor, we can use the `add_surveyors()` method of the `Team`. Likewise, if we would like to remove someone from the `Team`, we can use the `drop_surveyors()` method.

Let's add the first `simple_surveyor` we created at the top of this page.

demo_team.add_surveyors([simple_surveyor])

Now let's inspect the `Team` again.

demo_team.df

Now imagine we wanted only a single novice user. We can remove `novice2` and `novice3` by passing in their `Surveyor.name` attribute as a `str`.

demo_team.drop_surveyors(["novice2", "novice3"])

demo_team.df

We can indeed see that the two novices were removed from the `Team`.