# graphqltest
 xerp API backend with graphql implementation.
 
 Run the following commands from terminal ->
 python manage.py migrate &&
 python manage.py init_core_data &&
 python manage.py runserver

 #API call for countries
 ```json
query{
  countries{
    id,
    name,
    shortName,
    phoneCode
  }
}
```
 
 #API call for modules/apps
 ```json
query{
  modules{
    id,
    name,
    slug,
    description,
    status
  }
}
```

 #API call for checking unique company domain
 ```json
mutation{
  checkDomain(domain: "Provide domain"){
    domain
  }
}
```
 
 #API call for register
 ```json
 mutation{
    createUser(name: "", username: "", email: "", password: "", phone: "", company: "", domain: "", country: 18){
        user{
            firstName,
            username,
            email
        }
    }
 }
 ```
 
 #API call for activation
 ```json
mutation{
    activateUser(code: ""){
        user{
            firstName,
            email,
            username
        }
    }
 }
```
 
 #API call for login
 ```json
 mutation{
    tokenAuth(username: "provide username or email, both works", password: ""){
        user{
            token,
            refreshToken
        }
    }
 }
 ```
 
 #API call for verify token
 ```json
mutation{
    verifyToken(token: "provide token"){
        payload
    }
}
```

#API call for refresh token
```json
mutation{
    refreshToken(refreshToken: "refresh token here"){
        token,
        refreshToken,
        payload
    }
}
```
 
 #API call for buy a module/app license
 Provide Authorization header with value "JWT token"
 ```json
mutation{
  createLicense(checkout: [{module: 1, type: "Basic", duration: 30}, {module: 2, type: "Basic", duration: 30}]){
    license{
      id,
      user{},
      module{},
      type,
      duration
    }
  }
}
``` 

 #API call for sending invitation
 Provide Authorization header with value "JWT token" | Provide domain header with company domain 
 ```json
mutation{
  sendInvitation(email: "Provide email", module: 1, department: 2, role: 2){
    id,
    user{},
    module{},
    type,
    duration
  }
}
``` 

 #API call for accepting invitation as new user
 Provide Authorization header with value "JWT token" | Provide domain header with company domain  
 ```json
mutation{
  acceptNew(email: "Provide email", module: 1, department: 2, role: 2, name: "", username: "", password: ""){
    user{
      id,
      username,
      firstName,
      email
    }
  }
}
```

 #API call for accepting invitation as existing user
 Provide Authorization header with value "JWT token" | Provide domain header with company domain  
 ```json
mutation{
  acceptNew(email: "Provide email", module: 1, department: 2, role: 2){
    user{
      id,
      username,
      name,
      email
    }
  }
}
```

#API call for user companies
Provide Authorization header with value "JWT token"
 ```json
query{
  companies{
         id,
         name,
         domain,
         phone,
         country{
             id,
             name
         }
     }
}
```

 #API call for company apps of an user
 Provide Authorization header with value "JWT token" | Provide domain header with company domain  
 ```json
query{
    member{
        app{
            name
        },
        department{
            id,
            name,
            shortName
        },
        role{
            id,
            name
        }
    }
}
```
#API call for creating project
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createProject(title: "", description: "", startDate: "", endDate: ""  ){
      project{
          title,
          description,
          startDate,
          endDate

      }
  }
}

#API call for creating project
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createProject(title: "", description: "", startDate: "", endDate: ""  ){
      project{
          id,
          title,
          description,
          startDate,
          endDate

      }
  }
}


#API call for updating project
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateProject(project: "", title: "", description: "" startDate: "", endDate: ""  ){
      projectUpdated{
          id,
          title,
          description,
          startDate,
          endDate

      }
  }
}

#API call for deleting project
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteProject(project: "" ){
      projectDeleted{
          id


      }
  }
}

#API call for creating goal
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createGoal(project: "", title: "", description: "" startDate: "", endDate: ""   ){
      goal{
          id,
          title,
          description,
          startDate,
          endDate
      }
  }
}

#API call for updating goal
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateGoal(goal: "", title: "", description: "" startDate: "", endDate: ""  ){
      goalUpdated{
          id,
          title,
          description,
          startDate,
          endDate

      }
  }
}

#API call for deleting goal
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteGoal(goal: "" ){
      goalDeleted{
          id


      }
  }
}

#API call for creating task
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createTask(goal: "", title: "", description: "" startDate: "", endDate: ""   ){
      task{
          id,
          title,
          description,
          startDate,
          endDate
      }
  }
}

#API call for updating task
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateTask(task: "", title: "", description: "" startDate: "", endDate: ""  ){
      taskUpdated{
          id,
          title,
          description,
          startDate,
          endDate

      }
  }
}

#API call for deleting task
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteTask(task: "" ){
      taskDeleted{
          id


      }
  }
}

#API call for creating issue
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createIssue(task: "", title: "", description: "" startDate: "", endDate: ""   ){
      issue{
          id,
          title,
          description,
          startDate,
          endDate
      }
  }
}

#API call for updating issue
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateIssue(issue: "", title: "", description: "" startDate: "", endDate: ""  ){
      issueUpdated{
          id,
          title,
          description,
          startDate,
          endDate

      }
  }
}


#API call for deleting issue
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteIssue(issue: "" ){
      issueDeleted{
          id


      }
  }
}

#API call for creating project details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createProjectDetails(project:"", details: [{key: "", value: "" }]){
      details{
          id,
          key,
          value

      }
  }
}

#API call for updating project details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateProjectDetails(details: "", key: "", value: "" }]){
      detailsUpdated{
          id,
          key,
          value

      }
  }
}

#API call for  deleting  project details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteProjectDetails(details: ""}]){
      detailsDeleted{
          id

      }
  }
}


#API call for creating goal details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createGoalDetails(goal:"", details: [{key: "", value: "" }]){
      details{
          id,
          key,
          value

      }
  }
}


#API call for updating goal details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateGoalDetails(details: "", key: "", value: "" }]){
      detailsUpdated{
          id,
          key,
          value

      }
  }
}


#API call for  deleting  goal details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteGoalDetails(details: ""}]){
      detailsDeleted{
          id

      }
  }
}


#API call for creating task details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createTaskDetails(task:"", details: [{key: "", value: "" }]){
      details{
          id,
          key,
          value

      }
  }
}


#API call for updating task details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateTaskDetails(details: "", key: "", value: "" }]){
      detailsUpdated{
          id,
          key,
          value

      }
  }
}

#API call for  deleting  task details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteTaskDetails(details: ""}]){
      detailsDeleted{
          id

      }
  }
}


#API call for creating issue details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  createIssueDetails(issue:"", details: [{key: "", value: "" }]){
      details{
          id,
          key,
          value

      }
  }
}

#API call for updating issue details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  updateIssueDetails(details: "", key: "", value: "" }]){
      detailsUpdated{
          id,
          key,
          value

      }
  }
}


#API call for  deleting  issue details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteIssueDetails(details: ""}]){
      detailsDeleted{
          id

      }
  }
}


#API call for  deleting  issue details
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

 mutation{
  deleteIssueDetails(details: ""}]){
      detailsDeleted{
          id

      }
  }
}

#API call for projects
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 projects {
       id

   }
}

#API call for project
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 project(project:"") {
       id

   }
}

#API call for goals
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 goals {
       id

   }
}

#API call for goal
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 goal(goal:"") {
       id

   }
}

#API call for tasks
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 tasks {
       id

   }
}

#API call for task
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 task(task:"") {
       id

   }
}

#API call for issues
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 issues{
       id

   }
}


#API call for issue
 Provide Authorization header with value "JWT token" | Provide domain header with company domain
 ```json

query{
 issue(issue:"") {
       id

   }
}