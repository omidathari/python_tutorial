import json

jsonData = '{"firstName" : "Edward","lastName"   : "John"}'

dictData= json.loads(jsonData)

print(dictData)

print(dictData['firstName'])

print(dictData['lastName'])

###################

jsonData = {'firstName' : "Edward", "lastName": "John", "coursesMarks":{'English' : 20,"Science":45, "Maths": 48}}

# Get a JSON formatted string
output = json.dumps(jsonData)

print(type(jsonData), jsonData)
print(type(output), output)

############################