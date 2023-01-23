---
name: Bug report
about: Create a report to help us improve
title: ''
labels: 'bug'
assignees: 'fcusson'

---

# Bug Ticket

## Describe the bug

<A clear and concise description of what the bug is.>

## Troubleshooting

Make sure to validate all the elements before submitting the ticket (Exception to the steps marked as optional)

* [ ] Using latest version of spotcast
* [ ] Using latest stable version of Home Assistant
* [ ] I have setup the Spotify integration in Home Assistant
* [ ] I have renewed my `sp_dc` and `sp_key` values and restarted Home Assistant (see [README](https://github.com/fondberg/spotcast#enabling-debug-log))
* [ ] (optional) I have Spotify Premium
* [ ] (optional) I am using multiple accounts
* [ ] (optional) I'm attaching relevant logs with level debug for component spotcast (see [README](https://github.com/fondberg/spotcast#enabling-debug-log))
* [ ] (optional) I'm using entity_id in the service call and have tried device_name but the issue remains

## Environment

 - Installation type: [HA_OS|Container|Supervised|Core]
 - HA version: [ ]
 - spotcast version: [ ]

## Configuration

````yaml
# please remove any sensitive information like cookies and token keys
<insert configuration here>

````

## Service Call

If relevant, provide a `yaml` of the service call or explain the action taken to replicate the issue.

````yaml
<insert the yaml of the service call here>
````

## Logs

* normal|debug

````log
<please insert any relevent logs here>
````

## Additional context

<Add any other context about the problem here.>
