const express = require('express')
const firebase = require('firebase')
const bodyParser = require('body-parser')


const app = express()
app.use(bodyParser.json()); // for parsing application/json

// Initialize Firebase
  var config = {
    apiKey: "AIzaSyBzX7gVYuZzocDLN1fdCfbVCfYYm2xTzow",
    authDomain: "thecloset-94652.firebaseapp.com",
    databaseURL: "https://thecloset-94652.firebaseio.com",
    projectId: "thecloset-94652",
    storageBucket: "thecloset-94652.appspot.com",
    messagingSenderId: "727915381699"
  };
  firebase.initializeApp(config);

// Get a reference to the database service
var database = firebase.database();

var test = {
  type: "jeans",
  pos: "bottom",
  color: "#800080",
  style: ["casual", "fancy"],
  weathers: [],
}

var newPostKey = database.ref().child('posts').push().key;

//database.ref('closet/' + newPostKey).set(test);

app.get('/', function (req, res) {
  res.send('Hello World!')
})

app.post('/newArticle', function (req, res) {

  res.sendStatus(200);
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})
