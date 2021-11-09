# ypool
Ride share matching for the Yale community. 

# Description of Roles and Contributions

@adrianaarcia: primarily responsible for the design of the algorithm, and the implementation of  k-means clustering, match evaluation, as well as analytics, summary, and visualization functions. I authored the following files in the `serverless/flask-server` directory:

* `random_matching.py`
	
and the `serverless/flask-server/matching` directory:

* `main.py`
* `kmeans.py`
* `matching.py`
* `sample_inputs.py`
* `utility.py`
	
as well as the associated test files in the `serverless/flask-server/matching/tests` directory:

* `test_kmeans.py`
* `test_matching.py`
* `test_sample_inputs.py`
* `test_utility.py`
	
@AbrahamMensa: designed and implemented the greedy portion of the algorithm: Authored the following files in the `serverless/flask-server/matching` directory: 

* `greedy.py`
	
and the associated test files in the `serverless/flask-server/matching/tests` directory:

* `test_greedy.py`	

@DanielSanchezDiaz and @Obed-Ababio: responsible for frontend web development and co-authored all files in the `web` directory.

@jtruong99: responsible for backend development and all files in  `serverless` directory excluding those previously mentioned.


# Quick Start 
Running `./test_and_deploy.sh` will run all server tests and deploy to AWS via Serverless. Note that this assumes you have proper AWS configurations set up in your local development environment. (If you are not an administrator of this project, this is probably something you don't want to do.) See web section below on how to run server tests.

To just run the tests but not deploy, call `./run_test_suite.sh`.

# Overview
YPool hopes to match Yale affiliates interested in carpooling to locations such airports and train stations. Individuals enter information related to their trip (such as date, destination, and time of departure) and are then matched with other Yale affiliates who have similar travel plans. The application was live at https://yalepool.com/, and limited to the Yale community with protection via CAS authentication. The project utilizes the Serverless framework with a many AWS services including Lambda, DynamoDB, and APIGateway, and the front end is built with React.

## Project Organization

### `serverless` directory
This directory is a Serverless project to host the backend of YPool on AWS Lambda and API Gateway. Many of the files are config files, and irrelevant to most users. 

For frontend developers, check out api_tester.py to see how to call the different API endpoints. The core logic of the Flask app and api routes can be found in flask-server/app.py. 

Matching algorithm developers should work on code in the directory `flask-server/matching`. The only assumption made by the backend code is that this directory contains a `matching.py` file and a `find_matches(inputs)` method. If you are curious about the callsite, check out the `match()` method in `flask-server/app.py`, which defines the endpoint to invoke the algorithm. 

#### matching algorithm
As stated above, all the code for the matching algorithm resides in `serverless/flask-server/matching`. The matching algorithm uses k-means to cluster ride requests into matches. The algorithm is invoked through an api call only accessible to administrators, and is intended to be run on a fixed schedule, depending on request traffic. (If there is higher request traffic then the algorithm may be invoked more often than when there is lower traffic, as more requests are needed to produce optimal results). A user can only submit a request, and has no control over when the algorithm is run (as this is strictly controlled by administrators). 

### `web` directory
This directory contains all the front end code, which is built in React. For simplicity, we used `create-react-app` to build the front end code. 

#### Some useful commands: 
##### `npm start`

Runs the app in the development mode.\
Open [http://localhost:3000](http://localhost:3000) to view it in the browser.

The page will reload if you make edits.\
You will also see any lint errors in the console.

##### `npm test`

Launches the test runner in the interactive watch mode.\
See the section about [running tests](https://facebook.github.io/create-react-app/docs/running-tests) for more information.

##### `npm run build`

Builds the app for production to the `build` folder.\
It correctly bundles React in production mode and optimizes the build for the best performance.

The build is minified and the filenames include the hashes.\
Your app is ready to be deployed!
