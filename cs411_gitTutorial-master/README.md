This should just work but if you get this error: "Dev Server has been initialized using an options object that does not match the API schema.
 - options.allowedHosts[0] should be a non-empty string." Then follow these steps...

1. Go to the package.json file and make sure it has "react-scripts": "4.0.3" and not "react-scripts": "5.0.1"

2. Delete the node_modules folder

3. do "npm install" in terminal

4. do "npm start"

5. If still not working change "react-scripts": "4.0.3" to "react-scripts": "5.0.1" and try again
