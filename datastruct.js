const express = require('express')
const firebase = require('firebase')
const bodyParser = require('body-parser')
const cors = require('cors')

// Initialize Express
const app = express()
app.use(bodyParser.json()); // for parsing application/json
app.use(cors())

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

var bottoms = ["jeans"]; //types of clothing considered bottom
var tops = ["t-shirt", "jacket"]; //types of clothing considered top


// Express routing
// Homepage is redirected to getCloset
app.get('/', function (req, res){
  res.redirect('/getCloset');
})

// Gets the entire closet of clothes and parses it into a JSON array.
app.get('/getCloset', function(req, res) {
  var closet_array = [];

  database.ref('closet').once('value', function(closet) {
    closet.forEach(function(article) {
      closet_array.push(article.val());
    });
    res.send(closet_array);
  });
})

// Takes a new article of clothing, adds the "pos" attribute, and posts it to the database.
app.post('/newArticle', function(req, res) {
  var article = req.body;
  var newPostKey = database.ref().child('closet').push().key;

  if (bottoms.indexOf(article.type) != -1) {
    article.pos = "bottom";
  } else if (tops.indexOf(article.type) != -1) {
    article.pos = "top";
  }

  database.ref('closet/' + newPostKey).set(article);

  res.sendStatus(200);
})

// Takes a new outfit and posts it to the database.
app.post('/newOutfit', function(req, res) {
  var outfit = req.body;
  var newPostKey = database.ref().child('outfits').push().key;

  database.ref('outfits/' + newPostKey).set(outfit);

  res.sendStatus(200);
})

// The server is started.
app.listen(3000, function() {
  console.log('Server started at port 3000')
})
