const express = require('express')
const firebase = require('firebase')
const bodyParser = require('body-parser')

// Initialize Express
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
  var database = firebase.database();

var bottoms = ["jeans"];

var tops = ["t-shirt", "jacket"];


// Express Stuff
app.get('/', function (req, res) {
  res.send('Hello World!')
})

app.post('/newArticle', function (req, res) {
  var article = req.body;
  var newPostKey = database.ref().child('posts').push().key;

  if (bottoms.indexOf(article.type) != -1)
  {
    article.pos = "bottom";
  } else if (tops.indexOf(article.type) != -1)
  {
    article.pos = "top";
  }

  database.ref('closet/' + newPostKey).set(article);

  res.sendStatus(200);
  console.log("success!");
})

app.listen(3000, function () {
  console.log('Example app listening on port 3000!')
})
