# User Instructions

## Accessing the App
To interact with the app, first exec into the debug pod.

``` kubectl exec -it <debug_pod> -- /bin/bash ```

From here, the app can be interacted with either through manual curl commands or a consumer script. The consumer script has been provided to run through testing of the multiple endpoints within our API. Running ````python3 consumer.py```` will demonstrate example requests and responses. This file includes endpoints that do all CRUD operations needed to meet the final project requirements but does not include calling the analysis job, which will be described below. 

## Analysis Job Instructions

The analysis job will generate a pie graph of all of the different types of satellite orbits for the specified country. To view this graph, first we have to submit a job for the worker to pick up. We do this by access the endpoint for job submission by running the following from curl:

```` curl --data "country=USA" <flask-ip>:5000/submit ````

Refer to deploydocs.md to find the flask-ip. The country listed within the data of the post request will be what country is used for the analysis job and will be graphed.

We can now check on our analysis job by running:

```` curl <flask-ip>:5000/jobs ````

This will display a list of all jobs submitted with their id, status, and country parameters. We can continue querying this endpoint until we see our job has completed. If this ever has too many jobs that it becomes difficult to read, the jobs database may be cleared by running:

```` curl <flask-ip>:5000/resetjobs ````

Once we can see that our job has a status of completed, we can download the png file of the graph by running:

````curl <flask-ip>:5000/download/<job-id> > output.png ````

where job-id was displayed in the list of jobs when we queried the /jobs endpoint. There is an output.png file within this directory that was generated in this way and shows an example pie graph generated using USA as the country. 

A second analysis job worker is provided to plot another graph that this time takes the orbit type and plots the corresponding countries present in what percentages in this orbit type. This works very similarly to the previous analysis job with the only thing changing is the submission endpoint. This analysis job is submitted using:

```` curl --data "orbit=LEO" <flask-ip>:5000/submit2 ````

The status of the job can be viewed using the exact same endpoint and reseting the jobs using the reset jobs endpoint will reset both types of jobs:

```` curl <flask-ip>:5000/jobs ````

and

```` curl <flask-ip>:5000/resetjobs ````

as done previously. Finally download the image as done before using 

````curl <flask-ip>:5000/download/<job-id> > output2.png ````

An example of this analysis job is also provided as output2.png within this directory.

To retrieve the image on your local system, return back to ISP and transfer the image from the kubernetes cluster to ISP.
```
kubectl cp <debug_pod_name>:/app/output.png ./docs/kube_output.png
```
Then, transfer the image from ISP to your local system using
```
scp <TACC_ID>@isp02.tacc.utexas.edu:/repo_path/coe332-final-project/docs/kube_output.png \local_output_path\kube_output.png
```

## All Endpoints
Unless specified, all endpoints run with GET methods only. 

### /
Accessing this endpoint will reset the satellite data. 

### /all
Returns a list of all satellites in the dataset.

### /name/\<name>
Returns satellite information with a matching name. 

Ex: spaceBEE 1 

### /operator/\<operator>
Returns list of satellites with a matching operator name. 

Ex: NASA

### /country/\<country>
Returns list of satellites with a matching country name. 

Ex: Canada

### /orbit/\<orbit_type>  
Returns list of satellites with a matching orbit type. 

Ex: LEO, GEO, MEO

### /launch/date/\<date1>/\<date2>
Returns list of satellites launched between the two dates. Date format is dd-mm-yyyy.

Ex: 01-01-2020 02-01-2020

### /contractor/\<contractor>
Returns list of satellites with a matching contractor name. 

ex: Lockheed Martin

### /lifetime/\<lifetime>
Returns list of satellites with a lifetime duration longer than or equal to the specified lifetime in years. The Inter-Agency Space Debris Coordination Committee recommends that satellites deorbit within 25 years to minimize space debris. This endpoint is useful to select satellites which do not meet this guideline.

Ex: 25

### /launch/site/\<site>
Returns list of satellites with a matching launch site name. 

Ex: Cape Canaveral

### /launch/vehicle/\<vehicle>
Returns list of satellites with a matching launch vehicle name. 

Ex: Falcon 9

### /total/\<country>
Returns the count of orbit types for a country.

Ex: USA

### /satellite/\<uuid>
This endpoint is where most of the CRUD of the application takes place. GET, POST, and DELETE methods are available at this endpoint to read, update, or delete a satellite's information using its uuid. Refer to the Data Format section to see how to structure satellite data for POST request updating. Note that the uid column of the satellite does not have to be included in the data of the POST request.

### /satellite
This endpoint without a uuid is for use with POST request methods to add a new satellite to the dataset. Refer to the Data Format section to see how to structure satellite data for POST request to submit new satellite data. Note that the uid column of the satellite does not have to be included in the data of the POST request as it will be generated.

### /jobs
Returns a list of jobs submitted.

### /resetjobs
Accessing this endpoint will clear the jobs from the database. 

### /submit
This endpoint is for use with POST requests to submit the first type of analysis job. If no country is provided it will default to producing a graph for USA. 

### /submit2
This endpoint is for use with POST requests to submit the second type of analysis job. If no orbit is provided it will default to producing a graph for LEO. 

### /download/\<job-id>
This endpoint is used to download the analysis job using the job id found by querying the jobs endpoint.

## Data Format
Each satellite is returned as a dictionary with alphabetical keys and a uid. The following shows detailed descriptions for each key.

"uid": "The Uuid of the Satellite"

"A": "Name of Satellite, Alternate Names"

"B": "Current Official Name of Satellite"

"C": "Country/Org of UN Registry"

"D": "Country of Operator/Owner"

"E": "Operator/Owner"

"F": "Users"

"G": "Purpose"

"H": "Detailed Purpose"

"I": "Class of Orbit"

"J": "Type of Orbit"

"K": "Longitude of GEO (degrees)"

"L": "Perigee (km)"

"M": "Apogee (km)"

"N": "Eccentricity"

"O": "Inclination (degrees)"

"P": "Period (minutes)"

"Q": "Launch Mass (kg.)"

"R": "Dry Mass (kg.)"

"S": "Power (watts)"

"T": "Date of Launch"

"U": "Expected Lifetime (yrs.)"

"V": "Contractor"

"W": "Country of Contractor"

"X": "Launch Site"

"Y": "Launch Vehicle"

"Z": "COSPAR Number"

"AA": "NORAD Number"

"AB": "Comments"

"AD": "Source Used for Orbital Data"

"AE": "Source"

"AF": "Source"

"AG": "Source"

"AH": "Source"

"AI": "Source"

"AJ": "Source"

"AK": "Source"
