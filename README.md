# Knight Moves - Coding Challenge

Braulio De La Torre 


# How It works - Endpoints

There are 2 endpoints, POST and GET with the same URL 

URL - https://us-central1-pedregosa-sb.cloudfunctions.net/knightpath

 **POST** endpoint takes in the following payload 
``` 
{
	"source": "A3",
	"target": "H7"
}
```

**GET** endpoint takes in the following arguments as **query parameters**
```
	operationId=<operationId>
```


**Auth**
You will need the following header for this endpoint to function
```
headers={
	"Authorization":"powp32-nMn2-UEyuz-23bNqe"
}
```


## Validations

For both source and target positions, you must enter in first an alphabetic character followed by a numeric character. The alphabetic character must be from A-H and the numeric must be between 1-8


## Files

### knightpath
This is the endpoint that is client facing and has the 2* serverless compute functions. 

### knightpath-calculate
This is the endpoint that calculates the knight move paths


## Key Design Choices

### Google Cloud - Functions and Database
I created this project using google cloud functions to their feasibility in usage as well as firebase to easily communicate with the cloud functions as authentication is handled by google. Firebase being a nosql database, it was easy to implement and can scale using something like pydantic, classes, and validations.

### Async
The POST function uses threading to asynchronously compute the shortest path and number of moves. There are a number of ways to do this but many can be overkill (redis) for the size of this project.

### DTO
I did not choose to use DTO (data transfer objects) mainly due to timing, this would create structure to the endpoints, validating their payloads and helps when scaling a project -- especially when onboarding.

### Using a Single Endpoint
I figured it was easier to just use one serverless function instead of creating 2 as the project states. The one function hosts the same url and can be used with both POST and GET, using different payload methods. Depending on how an organization architects their endpoints, this can either be a pro or a con. Due to the size of the project, the decision is definitely a pro because of time to complete, complexity of code, and number of coders.

### Logging and Errors
There is a simple logging file in the project that is centralized. Although now it doesn't seem like much, it can be used later in order to take in all the current logs and more carefully send them to a central logger. As for Errors, I did not explicitly start to define errors in the project due to time constraints but I believe that it is best to define exceptions in an organization so that they are handled properly. For example, giving specific internal error codes to specific exceptions that provided clear messaging to the client and logging to servers. 

### Security
The security of this endpoint is quite weak, using only an authorization key. This key makes it so that any attackers will not so easily reach this endpoint but can be breached with time. This was chosen so that you guys can easily use this endpoint. For stronger security, constantly updated JWT tokens can be used with an authentication service as well as service accounts from a cloud provider. 



